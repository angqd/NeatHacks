"""Named query sets for the evaluation runners.

"frozen" is the pinned 60-query eval set. "natural" is the uncurated set built from the original
LiveMCPBench tasks (data/processed/natural_set_v1.jsonl, written by toolprune.eval.build_natural).
"""

import hashlib
import json

from toolprune.models import PROC_DIR, EvalQuery, load_eval_set

NATURAL_PATH = PROC_DIR / "natural_set_v1.jsonl"
SET_NAMES = ("frozen", "natural")


def load_queries(name: str = "frozen", split: str | None = None) -> list[EvalQuery]:
    if name == "frozen":
        return load_eval_set(split)
    if name == "natural":
        rows = [json.loads(line) for line in NATURAL_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
        queries = [EvalQuery(**row) for row in rows]
        return queries if split is None else [q for q in queries if q.split == split]
    raise ValueError(f"unknown query set {name!r}; expected one of {SET_NAMES}")


def natural_sha256() -> str:
    return hashlib.sha256(NATURAL_PATH.read_bytes()).hexdigest()


def run_suffix(name: str) -> str:
    """Suffix for run files, so natural-set runs never overwrite frozen-set runs."""
    return "" if name == "frozen" else f"__{name}"
