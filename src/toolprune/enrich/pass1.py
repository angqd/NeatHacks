"""Enrichment pass 1: one search card per tool, one LLM call per server.

Each server's tools go to gpt-6-luna in one call through the OpenAI Agents SDK, so sibling tools
are seen together. A draft that fails check_draft gets one retry with the problems appended. Tags
take tool_id, server, name and doc_hash from the source tool, and effect from the source
annotations when they settle it. Every call is cached in data/cache/enrich.sqlite.

Outputs in data/enriched/: pass1_annotations.jsonl (one ToolTag per line, catalog order),
servers.json (ServerCards) and manifest.json. A run with --servers writes the same files with a
_dry suffix, so it never overwrites a full run.

Run with: python -m toolprune.enrich.pass1 [--servers "A,B,C"] [--workers 4] [--no-cache]
"""

import argparse
import hashlib
import json
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone

from agents import Agent, Runner

from toolprune.enrich.models import (
    PROMPT_VERSION,
    ServerCard,
    ServerEnrichment,
    ToolTag,
    ToolTagDraft,
    check_draft,
)
from toolprune.enrich.prompts import INSTRUCTIONS, render_server_input
from toolprune.models import ROOT, Tool, load_tools
from toolprune.tracing import init_tracing

MODEL = "gpt-6-luna"
WORKFLOW = "tool-enrich"
AGENT_NAME = "tool-enrich"
CACHE_PATH = ROOT / "data" / "cache" / "enrich.sqlite"
OUT_DIR = ROOT / "data" / "enriched"
SHORT_DESCRIPTION_CHARS = 30
RETRY_HEADING = "Fix these problems from your previous answer:"


@dataclass
class CallResult:
    draft: ServerEnrichment
    input_tokens: int
    output_tokens: int
    latency_ms: float
    from_cache: bool


@dataclass
class ServerResult:
    server: str
    tags: list[ToolTag]
    card: ServerCard
    retries: int
    problems: list[str]
    unmatched: list[str]
    calls: list[CallResult]
    seconds: float


def _open_cache() -> sqlite3.Connection:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(CACHE_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS enrich_calls ("
        "key TEXT PRIMARY KEY, model TEXT, prompt_version TEXT, output_json TEXT, "
        "input_tokens INTEGER, output_tokens INTEGER, latency_ms REAL, created_at TEXT)"
    )
    return conn


def _key(user_message: str) -> str:
    return hashlib.sha256(f"{MODEL}\n{PROMPT_VERSION}\n{user_message}".encode("utf-8")).hexdigest()


def call_model(agent: Agent, user_message: str, use_cache: bool) -> CallResult:
    """One server call. Cache first when enabled; errors propagate to the caller."""
    key = _key(user_message)
    conn = _open_cache() if use_cache else None
    try:
        if conn is not None:
            row = conn.execute(
                "SELECT output_json, input_tokens, output_tokens, latency_ms FROM enrich_calls WHERE key = ?",
                (key,),
            ).fetchone()
            if row is not None:
                return CallResult(ServerEnrichment.model_validate_json(row[0]), row[1], row[2], row[3], True)

        start = time.perf_counter()
        result = Runner.run_sync(agent, user_message)
        latency_ms = (time.perf_counter() - start) * 1000
        draft = result.final_output_as(ServerEnrichment, raise_if_incorrect_type=True)
        usage = result.context_wrapper.usage
        input_tokens = int(usage.input_tokens)
        output_tokens = int(usage.output_tokens)

        if conn is not None:
            conn.execute(
                "INSERT OR REPLACE INTO enrich_calls (key, model, prompt_version, output_json, input_tokens, "
                "output_tokens, latency_ms, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    key,
                    MODEL,
                    PROMPT_VERSION,
                    draft.model_dump_json(),
                    input_tokens,
                    output_tokens,
                    latency_ms,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.commit()
        return CallResult(draft, input_tokens, output_tokens, latency_ms, False)
    finally:
        if conn is not None:
            conn.close()


def align(draft: ServerEnrichment, tools: list[Tool]) -> tuple[list[tuple[Tool, ToolTagDraft]], list[str]]:
    """Pair source tools with draft tools. By position when the names match, else by name."""
    expected = [tool.name for tool in tools]
    if [item.name for item in draft.tools] == expected:
        return list(zip(tools, draft.tools)), []

    by_name: dict[str, list[ToolTagDraft]] = {}
    for item in draft.tools:
        by_name.setdefault(item.name, []).append(item)
    pairs: list[tuple[Tool, ToolTagDraft]] = []
    unmatched: list[str] = []
    for tool in tools:
        candidates = by_name.get(tool.name)
        if candidates:
            pairs.append((tool, candidates.pop(0)))
        else:
            unmatched.append(tool.id)
    return pairs, unmatched


def build_tag(tool: Tool, item: ToolTagDraft) -> ToolTag:
    flags = list(item.flags)
    if len((tool.description or "").strip()) < SHORT_DESCRIPTION_CHARS:
        flags.append("missing_description")

    annotations = tool.annotations or {}
    if annotations.get("destructiveHint") is True:
        effect, effect_source = "destructive", "source_annotation"
    elif annotations.get("readOnlyHint") is True:
        effect, effect_source = "read", "source_annotation"
    else:
        effect, effect_source = item.effect, "model"

    doc = json.dumps(
        {"name": tool.name, "description": tool.description, "input_schema": tool.input_schema},
        sort_keys=True,
    )
    return ToolTag(
        tool_id=tool.id,
        server=tool.server,
        name=tool.name,
        domain=None,
        topic=item.topic,
        summary=item.summary,
        intents=item.intents,
        effect=effect,
        flags=list(dict.fromkeys(flags)),
        effect_source=effect_source,
        doc_hash=hashlib.sha256(doc.encode("utf-8")).hexdigest(),
        model=MODEL,
    )


def enrich_server(agent: Agent, server: str, tools: list[Tool], use_cache: bool) -> ServerResult:
    start = time.perf_counter()
    base_message = render_server_input(server, tools)
    expected = [tool.name for tool in tools]

    first = call_model(agent, base_message, use_cache)
    calls = [first]
    draft = first.draft
    problems = check_draft(draft, expected)
    retries = 0
    if problems:
        retries = 1
        retry_message = base_message + f"\n\n{RETRY_HEADING}\n" + "\n".join(f"- {p}" for p in problems)
        second = call_model(agent, retry_message, use_cache)
        calls.append(second)
        draft = second.draft
        problems = check_draft(draft, expected)

    pairs, unmatched = align(draft, tools)
    tags = [build_tag(tool, item) for tool, item in pairs]
    card = ServerCard(server=server, server_summary=draft.server_summary, n_tools=len(tools), model=MODEL)
    return ServerResult(
        server=server,
        tags=tags,
        card=card,
        retries=retries,
        problems=problems,
        unmatched=unmatched,
        calls=calls,
        seconds=time.perf_counter() - start,
    )


def parse_servers(text: str | None) -> list[str] | None:
    if text is None:
        return None
    return [part.strip() for part in text.split(",") if part.strip()]


def write_outputs(suffix: str, tags: list[ToolTag], cards: list[ServerCard], manifest: dict) -> list:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = [
        OUT_DIR / f"pass1_annotations{suffix}.jsonl",
        OUT_DIR / f"servers{suffix}.json",
        OUT_DIR / f"manifest{suffix}.json",
    ]
    paths[0].write_text("".join(tag.model_dump_json() + "\n" for tag in tags), encoding="utf-8")
    paths[1].write_text(
        json.dumps([card.model_dump() for card in cards], ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    paths[2].write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrichment pass 1: one LLM call per server.")
    parser.add_argument("--servers", default=None, help="comma-separated server names; writes the _dry outputs")
    parser.add_argument("--workers", type=int, default=4, help="servers enriched concurrently")
    parser.add_argument("--no-cache", action="store_true", help="bypass the LLM cache for reads and writes")
    args = parser.parse_args()

    if args.workers < 1:
        raise SystemExit("--workers must be at least 1")

    init_tracing(WORKFLOW)
    started = time.perf_counter()
    tools = load_tools()
    groups: dict[str, list[Tool]] = {}
    for tool in tools:
        groups.setdefault(tool.server, []).append(tool)

    requested = parse_servers(args.servers)
    if requested is not None:
        unknown = [name for name in requested if name not in groups]
        if unknown:
            raise SystemExit(f"unknown server names: {unknown}")
        servers = [name for name in groups if name in set(requested)]
        suffix = "_dry"
    else:
        servers = list(groups)
        suffix = ""

    agent = Agent(
        name=AGENT_NAME,
        instructions=INSTRUCTIONS,
        model=MODEL,
        output_type=ServerEnrichment,
    )

    results: dict[str, ServerResult] = {}
    failures: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(enrich_server, agent, server, groups[server], not args.no_cache): server
            for server in servers
        }
        for index, future in enumerate(as_completed(futures), start=1):
            server = futures[future]
            try:
                res = future.result()
            except Exception as exc:
                failures[server] = f"{type(exc).__name__}: {exc}"
                print(f"[{index}/{len(servers)}] {server}: FAILED {failures[server]}")
                continue
            results[server] = res
            cached = sum(1 for call in res.calls if call.from_cache)
            status = f"problems {len(res.problems)}" if res.problems else "valid"
            print(
                f"[{index}/{len(servers)}] {server}: {len(groups[server])} tools, {status}, "
                f"retries {res.retries}, cached calls {cached}/{len(res.calls)}, "
                f"tokens in {sum(c.input_tokens for c in res.calls)} out {sum(c.output_tokens for c in res.calls)}, "
                f"{res.seconds:.1f}s"
            )

    tags: list[ToolTag] = []
    cards: list[ServerCard] = []
    for server in servers:
        if server in results:
            tags.extend(results[server].tags)
            cards.append(results[server].card)

    all_calls = [call for res in results.values() for call in res.calls]
    fresh_calls = [call for call in all_calls if not call.from_cache]
    manifest = {
        "model": MODEL,
        "prompt_version": PROMPT_VERSION,
        "workflow": WORKFLOW,
        "dry_run": requested is not None,
        "servers_requested": servers,
        "n_servers": len(servers),
        "n_servers_ok": len(results),
        "n_source_tools": sum(len(groups[server]) for server in servers),
        "n_tools_tagged": len(tags),
        "retries": sum(res.retries for res in results.values()),
        "unresolved_servers": [
            {"server": res.server, "problems": res.problems} for res in results.values() if res.problems
        ],
        "unmatched_tools": [tool_id for res in results.values() for tool_id in res.unmatched],
        "failed_servers": failures,
        "llm_calls": len(all_calls),
        "cache_hits": len(all_calls) - len(fresh_calls),
        "total_input_tokens": sum(call.input_tokens for call in all_calls),
        "total_output_tokens": sum(call.output_tokens for call in all_calls),
        "fresh_input_tokens": sum(call.input_tokens for call in fresh_calls),
        "fresh_output_tokens": sum(call.output_tokens for call in fresh_calls),
        "workers": args.workers,
        "no_cache": args.no_cache,
        "run_seconds": round(time.perf_counter() - started, 2),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    paths = write_outputs(suffix, tags, cards, manifest)

    print("summary")
    print(f"  servers ok: {len(results)}/{len(servers)}  failed: {len(failures)}")
    print(f"  tools tagged: {len(tags)}/{manifest['n_source_tools']}  unmatched: {len(manifest['unmatched_tools'])}")
    print(f"  retries: {manifest['retries']}  unresolved servers: {len(manifest['unresolved_servers'])}")
    print(f"  llm calls: {manifest['llm_calls']}  cache hits: {manifest['cache_hits']}")
    print(f"  tokens total in/out: {manifest['total_input_tokens']}/{manifest['total_output_tokens']}")
    print(f"  tokens fresh in/out: {manifest['fresh_input_tokens']}/{manifest['fresh_output_tokens']}")
    print(f"  run seconds: {manifest['run_seconds']}")
    for path in paths:
        print(f"  wrote {path}")


if __name__ == "__main__":
    main()
