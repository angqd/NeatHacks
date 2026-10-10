"""Shared Pydantic types, data paths and loaders for the tool catalog and frozen eval set.

Reads data/processed/tools.jsonl and data/processed/eval_set.jsonl. The eval set is
checked against a pinned SHA-256 before use, so a silent edit fails loudly.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).resolve().parents[2]
PROC_DIR = ROOT / "data" / "processed"
EVAL_SET_PATH = PROC_DIR / "eval_set.jsonl"
FROZEN_EVAL_SHA256 = "305447a13c3359e40b0193a2857c69d99430414bed2f337976db9d53ff0f4afc"


class Tool(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    server: str
    server_category: str
    server_description: str
    name: str
    description: str
    input_schema: dict[str, Any]
    annotations: dict[str, Any] | None
    name_collision_count: int


class Slot(BaseModel):
    model_config = ConfigDict(extra="allow")

    gold_name: str
    pick: str | None
    alternates: list[str] = Field(default_factory=list)


class Confuser(BaseModel):
    model_config = ConfigDict(extra="allow")

    tool_id: str
    reason: str


class EvalQuery(BaseModel):
    model_config = ConfigDict(extra="allow")

    task_id: str
    question: str
    category: str
    bucket: str
    family: str
    slots: list[Slot]
    confusers: list[Confuser]
    needs_clarification: bool
    derived: bool
    split: Literal["dev", "test"]


class RankedTool(BaseModel):
    tool_id: str
    score: float


class RetrievedSet(BaseModel):
    query_id: str
    system: str
    ranked: list[RankedTool]
    latency_ms: float | None = None
    tokens: int | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


class Retriever(Protocol):
    name: str

    def retrieve(self, query: str, k: int) -> list[RankedTool]:
        ...


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_tools() -> list[Tool]:
    return [Tool(**row) for row in read_jsonl(PROC_DIR / "tools.jsonl")]


def load_eval_set(split: str | None = None) -> list[EvalQuery]:
    raw = EVAL_SET_PATH.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != FROZEN_EVAL_SHA256:
        raise RuntimeError(f"eval_set.jsonl sha256 {digest} does not match frozen {FROZEN_EVAL_SHA256}")
    queries = [EvalQuery(**row) for row in read_jsonl(EVAL_SET_PATH)]
    if split is None:
        return queries
    return [q for q in queries if q.split == split]
