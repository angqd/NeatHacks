"""Hierarchical router: three LLM stages over groups of tools, then over tools.

Stage 1 (plan) reads the group cards and returns the capabilities the request needs, each with
its best groups. Stage 2 (select) reads the tag cards of every tool in the chosen groups and
picks tools per capability. Stage 3 (widen) runs only when a capability is still uncovered and
reads the tag cards of every tool that stage 2 did not see.

Every LLM call goes through the OpenAI Agents SDK with a Pydantic output type built from the
loaded groups and tools, so the model cannot return a name or id that does not exist. Calls are
cached in data/cache/route.sqlite, keyed by the full request, unless use_cache is False.

Run through the eval harness: python -m toolprune.eval.route_run --group-by server
"""

import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agents import Agent, Runner
from pydantic import BaseModel

from toolprune.models import ROOT, RankedTool, read_jsonl
from toolprune.route.models import MAX_GROUPS_PER_CAPABILITY, ROUTER_VERSION, plan_model, selection_model
from toolprune.route.prompts import PLAN_INSTRUCTIONS, SELECT_INSTRUCTIONS, WIDEN_INSTRUCTIONS, plan_input, select_input
from toolprune.tracing import init_tracing

MODEL = "gpt-6-luna"
WORKFLOW = "tool-route"
ENRICHED_DIR = ROOT / "data" / "enriched"
CACHE_PATH = ROOT / "data" / "cache" / "route.sqlite"
ANNOTATION_PATHS = {
    "pass1": ENRICHED_DIR / "pass1_annotations.jsonl",
    "final": ENRICHED_DIR / "annotations.jsonl",
}
STAGES = ("plan", "select", "widen")


@dataclass
class LlmResult:
    output: BaseModel
    input_tokens: int
    output_tokens: int
    latency_ms: float
    from_cache: bool


def _open_cache() -> sqlite3.Connection:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(CACHE_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS route_calls ("
        "key TEXT PRIMARY KEY, stage TEXT, model TEXT, output_json TEXT, "
        "input_tokens INTEGER, output_tokens INTEGER, latency_ms REAL, created_at TEXT)"
    )
    return conn


def _load_groups(group_by: str) -> list[dict[str, Any]]:
    path = ENRICHED_DIR / f"groups_{group_by}.json"
    if not path.is_file():
        raise FileNotFoundError(f"{path} does not exist")
    groups = json.loads(path.read_text(encoding="utf-8"))
    names = [group["name"] for group in groups]
    if len(set(names)) != len(names):
        raise ValueError(f"{path} holds duplicate group names")
    return groups


def _record(meta: dict[str, Any], stage: str, result: LlmResult) -> None:
    meta["stage_tokens"][stage] = [result.input_tokens, result.output_tokens]
    meta["stage_latency_ms"][stage] = round(result.latency_ms, 2)
    meta["llm_calls"] += 1
    meta["llm_input_tokens"] += result.input_tokens
    meta["llm_output_tokens"] += result.output_tokens
    if result.from_cache:
        meta["from_cache_calls"] += 1


def _align(choices: list[Any], needs: list[str], meta: dict[str, Any], stage: str) -> list[list[str]]:
    """Map the model's choices to the needs by position. Count any echoed need that does not match."""
    picks: list[list[str]] = [[] for _ in needs]
    for index, choice in enumerate(choices[: len(needs)]):
        if choice.need != needs[index]:
            meta["need_echo_mismatch"] += 1
        picks[index] = list(dict.fromkeys(choice.tool_ids))
    if len(choices) != len(needs):
        meta["choice_count_mismatch"].append(stage)
    return picks


class HierarchicalRouter:
    """Route a query to groups, then to tools in those groups, widening only if a need is uncovered."""

    def __init__(self, group_by: str = "server", annotations: str = "pass1", use_cache: bool = True) -> None:
        if annotations not in ANNOTATION_PATHS:
            raise ValueError(f"annotations must be one of {sorted(ANNOTATION_PATHS)}")
        annotations_path = ANNOTATION_PATHS[annotations]
        if not annotations_path.is_file():
            raise FileNotFoundError(f"{annotations_path} does not exist")

        init_tracing(WORKFLOW)
        self.group_by = group_by
        self.name = f"router:{group_by}"
        self.groups = _load_groups(group_by)
        self.group_by_name = {group["name"]: group for group in self.groups}
        self.tags = {row["tool_id"]: row for row in read_jsonl(annotations_path)}
        self.use_cache = use_cache
        self._conn = _open_cache() if use_cache else None
        self.last_meta: dict[str, Any] = {}

    def _call(self, stage: str, instructions: str, user_message: str, output_model: type[BaseModel]) -> LlmResult:
        schema = json.dumps(output_model.model_json_schema(), sort_keys=True)
        key = hashlib.sha256(
            json.dumps([ROUTER_VERSION, stage, instructions, user_message, schema]).encode("utf-8")
        ).hexdigest()

        if self._conn is not None:
            row = self._conn.execute(
                "SELECT output_json, input_tokens, output_tokens, latency_ms FROM route_calls WHERE key = ?",
                (key,),
            ).fetchone()
            if row is not None:
                return LlmResult(output_model.model_validate_json(row[0]), row[1], row[2], row[3], True)

        agent = Agent(name=f"route_{stage}", model=MODEL, instructions=instructions, output_type=output_model)
        start = time.perf_counter()
        result = Runner.run_sync(agent, user_message)
        latency_ms = (time.perf_counter() - start) * 1000
        output = result.final_output_as(output_model, raise_if_incorrect_type=True)
        usage = result.context_wrapper.usage
        input_tokens = int(usage.input_tokens)
        output_tokens = int(usage.output_tokens)

        if self._conn is not None:
            self._conn.execute(
                "INSERT OR REPLACE INTO route_calls (key, stage, model, output_json, input_tokens, "
                "output_tokens, latency_ms, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    key,
                    stage,
                    MODEL,
                    output.model_dump_json(),
                    input_tokens,
                    output_tokens,
                    latency_ms,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            self._conn.commit()
        return LlmResult(output, input_tokens, output_tokens, latency_ms, False)

    def retrieve(self, query: str, k: int) -> list[RankedTool]:
        meta: dict[str, Any] = {
            "stage_tokens": {stage: None for stage in STAGES},
            "stage_latency_ms": {stage: None for stage in STAGES},
            "widened": False,
            "groups_chosen": [],
            "capabilities": [],
            "llm_calls": 0,
            "llm_input_tokens": 0,
            "llm_output_tokens": 0,
            "from_cache_calls": 0,
            "need_echo_mismatch": 0,
            "choice_count_mismatch": [],
        }
        self.last_meta = meta

        # Stage 1: capabilities and their groups.
        plan = self._call("plan", PLAN_INSTRUCTIONS, plan_input(query, self.groups), plan_model(list(self.group_by_name)))
        _record(meta, "plan", plan)
        capabilities: list[dict[str, Any]] = []
        for capability in plan.output.capabilities:
            groups = list(dict.fromkeys(capability.groups))[:MAX_GROUPS_PER_CAPABILITY]
            capabilities.append({"need": capability.need, "groups": groups})
        groups_chosen = list(dict.fromkeys(group for cap in capabilities for group in cap["groups"]))
        meta["capabilities"] = capabilities
        meta["groups_chosen"] = groups_chosen
        needs = [cap["need"] for cap in capabilities]

        # Stage 2: choose tools among the tools of the chosen groups.
        candidate_ids = list(dict.fromkeys(
            tool_id for group in groups_chosen for tool_id in self.group_by_name[group]["tool_ids"]
        ))
        picks: list[list[str]] = [[] for _ in needs]
        covered = [False for _ in needs]
        if needs and candidate_ids:
            select = self._call(
                "select",
                SELECT_INSTRUCTIONS,
                select_input(query, needs, [self.tags[tool_id] for tool_id in candidate_ids]),
                selection_model(candidate_ids),
            )
            _record(meta, "select", select)
            picks = _align(select.output.choices, needs, meta, "select")
            covered = [bool(choice.covered) for choice in select.output.choices[: len(needs)]]
            covered += [False] * (len(needs) - len(covered))

        # A capability whose model returned no groups is uncovered by definition.
        uncovered = [
            index for index, cap in enumerate(capabilities)
            if not cap["groups"] or not covered[index] or not picks[index]
        ]

        # Stage 3: widen to every tool stage 2 did not see, only for the uncovered needs.
        seen = set(candidate_ids)
        remaining = [tool_id for tool_id in self.tags if tool_id not in seen]
        if uncovered and remaining:
            widen = self._call(
                "widen",
                WIDEN_INSTRUCTIONS,
                select_input(query, [needs[i] for i in uncovered], [self.tags[tool_id] for tool_id in remaining]),
                selection_model(remaining),
            )
            _record(meta, "widen", widen)
            meta["widened"] = True
            widened_picks = _align(widen.output.choices, [needs[i] for i in uncovered], meta, "widen")
            for offset, index in enumerate(uncovered):
                picks[index] = list(dict.fromkeys(picks[index] + widened_picks[offset]))

        # Output: capability by capability, best first, de-duplicated, score 1/rank.
        ordered = list(dict.fromkeys(tool_id for tool_ids in picks for tool_id in tool_ids))[:k]
        self.last_meta = meta
        return [RankedTool(tool_id=tool_id, score=1 / rank) for rank, tool_id in enumerate(ordered, start=1)]
