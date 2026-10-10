"""Deterministic per-query metrics for one returned set against the eval annotations.

Definitions live in benchmark_plan.md (Stage 6 spec). No LLM is involved. A metric that has no
defined value for a query (for example the confusion rate when the query lists no confuser)
is returned as None and is skipped when averaging.
"""

import numpy as np

from toolprune.models import EvalQuery, RetrievedSet

KS = (1, 5, 10)
BOOTSTRAP_RESAMPLES = 10_000
BOOTSTRAP_SEED = 0


def acceptable_by_slot(query: EvalQuery) -> list[set[str]]:
    """One set of acceptable tool ids per slot. A slot without a pick is skipped."""
    return [{s.pick, *s.alternates} for s in query.slots if s.pick]


def top_ids(returned: RetrievedSet, k: int) -> list[str]:
    return [r.tool_id for r in returned.ranked[:k]]


def slot_recall(query: EvalQuery, returned: RetrievedSet, k: int) -> float:
    slots = acceptable_by_slot(query)
    ids = set(top_ids(returned, k))
    return sum(1 for acc in slots if acc & ids) / len(slots)


def full_coverage(query: EvalQuery, returned: RetrievedSet, k: int) -> float:
    return 1.0 if slot_recall(query, returned, k) == 1.0 else 0.0


def precision(query: EvalQuery, returned: RetrievedSet, k: int) -> float | None:
    ids = top_ids(returned, k)
    if not ids:
        return None
    acceptable = set().union(*acceptable_by_slot(query))
    return sum(1 for i in ids if i in acceptable) / len(ids)


def r_precision(query: EvalQuery, returned: RetrievedSet) -> float | None:
    return precision(query, returned, len(acceptable_by_slot(query)))


def reciprocal_rank(query: EvalQuery, returned: RetrievedSet) -> float:
    acceptable = set().union(*acceptable_by_slot(query))
    for rank, tool in enumerate(returned.ranked, start=1):
        if tool.tool_id in acceptable:
            return 1.0 / rank
    return 0.0


def confusion(query: EvalQuery, returned: RetrievedSet, k: int) -> float | None:
    """1 if at least one slot is missed and a listed confuser is returned, else 0. None if no confuser is listed."""
    if not query.confusers:
        return None
    confusers = {c.tool_id for c in query.confusers}
    missed = slot_recall(query, returned, k) < 1.0
    return 1.0 if missed and confusers & set(top_ids(returned, k)) else 0.0


def confuser_first(query: EvalQuery, returned: RetrievedSet, k: int) -> float | None:
    """1 if a listed confuser ranks above the first acceptable tool, or a confuser is present and no acceptable is."""
    if not query.confusers:
        return None
    confusers = {c.tool_id for c in query.confusers}
    acceptable = set().union(*acceptable_by_slot(query))
    first_confuser = first_acceptable = None
    for rank, tool in enumerate(returned.ranked[:k], start=1):
        if first_confuser is None and tool.tool_id in confusers:
            first_confuser = rank
        if first_acceptable is None and tool.tool_id in acceptable:
            first_acceptable = rank
    if first_confuser is None:
        return 0.0
    return 1.0 if first_acceptable is None or first_confuser < first_acceptable else 0.0


def unjudged_rate(query: EvalQuery, returned: RetrievedSet, k: int) -> float | None:
    ids = top_ids(returned, k)
    if not ids:
        return None
    known = set().union(*acceptable_by_slot(query)) | {c.tool_id for c in query.confusers}
    return sum(1 for i in ids if i not in known) / len(ids)


def tokens_at_k(returned: RetrievedSet, k: int) -> float | None:
    per_tool = returned.meta.get("tool_tokens")
    if not per_tool:
        return None
    return float(sum(per_tool.get(i, 0) for i in top_ids(returned, k)))


def score_query(query: EvalQuery, returned: RetrievedSet) -> dict[str, float | None]:
    """All metrics for one query, keyed like 'slot_recall@5'."""
    out: dict[str, float | None] = {}
    for k in KS:
        out[f"slot_recall@{k}"] = slot_recall(query, returned, k)
        out[f"full_coverage@{k}"] = full_coverage(query, returned, k)
        out[f"precision@{k}"] = precision(query, returned, k)
        out[f"confusion@{k}"] = confusion(query, returned, k)
        out[f"confuser_first@{k}"] = confuser_first(query, returned, k)
        out[f"unjudged@{k}"] = unjudged_rate(query, returned, k)
        out[f"tokens@{k}"] = tokens_at_k(returned, k)
    out["r_precision"] = r_precision(query, returned)
    out["mrr"] = reciprocal_rank(query, returned)
    out["latency_ms"] = returned.latency_ms
    return out


def mean(values: list[float | None]) -> float | None:
    kept = [v for v in values if v is not None]
    return float(np.mean(kept)) if kept else None


def bootstrap_ci(values: list[float | None], seed: int = BOOTSTRAP_SEED) -> tuple[float, float] | None:
    """95% percentile interval of the mean over queries. Queries with None are dropped first."""
    kept = np.array([v for v in values if v is not None], dtype=float)
    if kept.size == 0:
        return None
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, kept.size, size=(BOOTSTRAP_RESAMPLES, kept.size))
    means = kept[idx].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def paired_difference(a: list[float | None], b: list[float | None], seed: int = BOOTSTRAP_SEED) -> dict:
    """System a minus system b on the same queries (pairs with a None are dropped)."""
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if not pairs:
        return {"n": 0}
    diff = np.array([x - y for x, y in pairs], dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, diff.size, size=(BOOTSTRAP_RESAMPLES, diff.size))
    means = diff[idx].mean(axis=1)
    return {
        "n": int(diff.size),
        "mean_diff": float(diff.mean()),
        "ci95": [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))],
        "wins": int((diff > 0).sum()),
        "losses": int((diff < 0).sum()),
        "ties": int((diff == 0).sum()),
    }
