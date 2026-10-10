"""Noise-scaling curve: how BM25 and embedding retrieval degrade as the tool pool grows noisier.

For each query the pool holds every acceptable tool (each slot's pick and alternates) plus tools
sampled uniformly at random from the rest of the catalog, up to the pool size. Listed confusers are
not kept specially: they enter the pool only if sampled. Pool size 527 is the full catalog, unsampled.

BM25 is rebuilt per pool, so its IDF follows the pool. The embedding ranking comes from the
full-catalog retriever once and is restricted to the pool, since cosine order does not depend on it.
Every returned set is cut to the top 10 before scoring with toolprune.eval.score.score_query.

Only cached embeddings are read. The run stops before any retrieval if a text is missing from the
cache, and it checks afterwards that no API call was made.
Run with: python -m toolprune.eval.noise
"""

import hashlib
import json
from collections import defaultdict
from contextlib import closing
from typing import Any

import numpy as np

from toolprune.bm25 import BM25Retriever
from toolprune.embeddings import MAX_CHARS, MODEL, STATS, EmbeddingRetriever, _key, _open_cache
from toolprune.eval.score import mean, score_query
from toolprune.models import ROOT, EvalQuery, RankedTool, RetrievedSet, Tool, load_eval_set, load_tools
from toolprune.text import tool_document

REPORTS_DIR = ROOT / "reports"
JSON_PATH = REPORTS_DIR / "noise_scaling.json"
MD_PATH = REPORTS_DIR / "noise_scaling.md"

VARIANT = "name_desc_server"
POOL_SIZES = (50, 100, 250, 527)
SEEDS = (0, 1, 2, 3, 4)
TOP_K = 10
SLOT_METRIC = "slot_recall@5"
TABLE_METRICS = ("slot_recall@5", "full_coverage@5", "mrr")
BUCKET_ORDER = ("semantic_distance", "taxonomy_collision", "multi_capability", "near_duplicate", "ambiguity", "none")


def stable_seed(seed: int, size: int, task_id: str) -> int:
    """A 64-bit seed from sha256, so the sample does not depend on Python's hash() salt."""
    digest = hashlib.sha256(f"{seed}|{size}|{task_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def acceptable_ids(query: EvalQuery) -> set[str]:
    """Every acceptable tool id of the query: each slot's pick and alternates."""
    return {tid for slot in query.slots if slot.pick for tid in (slot.pick, *slot.alternates)}


def check_cache(tools: list[Tool], queries: list[EvalQuery]) -> None:
    """Stop before any retrieval if a tool document or query text is not in the embedding cache."""
    texts = [tool_document(tool, VARIANT)[:MAX_CHARS] for tool in tools]
    texts += [query.question[:MAX_CHARS] for query in queries]
    needed = {_key(text, MODEL) for text in texts}
    with closing(_open_cache()) as conn:
        cached = {row[0] for row in conn.execute("SELECT key FROM embeddings WHERE model = ?", (MODEL,))}
    missing = needed - cached
    if missing:
        raise SystemExit(f"{len(missing)} texts are missing from the embedding cache; stopped before any API call")


def build_pool(query: EvalQuery, tools: list[Tool], size: int, seed: int) -> list[Tool]:
    """Acceptable tools plus a seeded random sample of the other tools, in catalog order."""
    acceptable = acceptable_ids(query)
    if size >= len(tools):
        return list(tools)
    if size <= len(acceptable):
        return [tool for tool in tools if tool.id in acceptable]
    others = [tool for tool in tools if tool.id not in acceptable]
    rng = np.random.default_rng(stable_seed(seed, size, query.task_id))
    picked = rng.choice(len(others), size=size - len(acceptable), replace=False)
    keep = acceptable | {others[i].id for i in picked}
    return [tool for tool in tools if tool.id in keep]


def score_row(query: EvalQuery, system: str, ranked: list[RankedTool]) -> dict[str, Any]:
    returned = RetrievedSet(query_id=query.task_id, system=system, ranked=ranked[:TOP_K])
    scores = score_query(query, returned)
    return {"slot_recall@5": scores["slot_recall@5"], "full_coverage@5": scores["full_coverage@5"], "mrr": scores["mrr"], "bucket": query.bucket}


def run_curve(tools: list[Tool], queries: list[EvalQuery]) -> dict[str, dict[int, dict[int, list[dict[str, Any]]]]]:
    """System name -> pool size -> seed -> one scored row per query."""
    catalog_ids = {tool.id for tool in tools}
    for query in queries:
        missing = acceptable_ids(query) - catalog_ids
        if missing:
            raise SystemExit(f"query {query.task_id} lists tools not in the catalog: {sorted(missing)}")

    embedder = EmbeddingRetriever(tools, VARIANT)
    full_ranking = {query.task_id: embedder.retrieve(query.question, len(tools)) for query in queries}

    rows: dict[str, dict[int, dict[int, list[dict[str, Any]]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for size in POOL_SIZES:
        for seed in SEEDS:
            bm25_cache: dict[tuple[str, ...], BM25Retriever] = {}
            for query in queries:
                pool = build_pool(query, tools, size, seed)
                pool_ids = {tool.id for tool in pool}

                key = tuple(tool.id for tool in pool)
                if key not in bm25_cache:
                    bm25_cache[key] = BM25Retriever(pool, VARIANT)
                bm25 = bm25_cache[key]
                rows[bm25.name][size][seed].append(score_row(query, bm25.name, bm25.retrieve(query.question, TOP_K)))

                ranked = [hit for hit in full_ranking[query.task_id] if hit.tool_id in pool_ids]
                rows[embedder.name][size][seed].append(score_row(query, embedder.name, ranked))
    return rows


def summarise(rows: dict[str, dict[int, dict[int, list[dict[str, Any]]]]], queries: list[EvalQuery]) -> dict[str, Any]:
    systems: dict[str, Any] = {}
    buckets: dict[str, Any] = {}
    for system, by_size in rows.items():
        systems[system] = {}
        buckets[system] = {}
        for size in POOL_SIZES:
            by_seed = by_size[size]
            systems[system][str(size)] = {}
            for metric in TABLE_METRICS:
                seed_means = [mean([row[metric] for row in by_seed[seed]]) for seed in SEEDS]
                sd = float(np.std(seed_means, ddof=1)) if len(seed_means) > 1 else 0.0
                systems[system][str(size)][metric] = {
                    "mean": float(np.mean(seed_means)),
                    "sd_across_seeds": sd,
                    "per_seed": seed_means,
                }
            buckets[system][str(size)] = {}
            for bucket in BUCKET_ORDER:
                values = [row[SLOT_METRIC] for seed in SEEDS for row in by_seed[seed] if row["bucket"] == bucket]
                buckets[system][str(size)][bucket] = mean(values)
    counts = defaultdict(int)
    for query in queries:
        counts[query.bucket] += 1
    return {
        "pool_sizes": list(POOL_SIZES),
        "seeds": list(SEEDS),
        "n_queries": len(queries),
        "k": TOP_K,
        "bucket_n": {bucket: counts[bucket] for bucket in BUCKET_ORDER},
        "systems": systems,
        "slot_recall@5_by_bucket": buckets,
    }


def fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def render_markdown(summary: dict[str, Any]) -> str:
    sizes = summary["pool_sizes"]
    systems = list(summary["systems"])
    lines = [
        "# Noise-scaling curve",
        "",
        "Pool construction rules:",
        "",
        "- Every acceptable tool of the query (each slot's pick and alternates) is always in the pool.",
        "- The rest of the pool is a uniform random sample without replacement from the other catalog tools, up to the pool size.",
        "- The sample uses numpy `default_rng`, seeded from a sha256 of (seed, pool size, query task_id).",
        "- Listed confusers are not specially kept. They enter the pool only if sampled.",
        "- Pool size 527 is the full catalog, with no sampling.",
        "- BM25 is rebuilt per pool (`name_desc_server`). Embeddings rank the full catalog once, and the order is restricted to the pool.",
        "- Each returned set is cut to the top 10 and scored with `toolprune.eval.score.score_query`.",
        "",
        f"{summary['n_queries']} queries, {len(summary['seeds'])} seeds (0 to {summary['seeds'][-1]}).",
        "Cells are the mean over queries and seeds, with ± the sample standard deviation (ddof=1) across seeds of the per-seed query means.",
        "At size 527 every seed gives the same pool, so the ± is 0.",
        "",
    ]
    for metric in TABLE_METRICS:
        lines += [f"## {metric} by pool size", "", "| System | " + " | ".join(str(s) for s in sizes) + " |", "|---" * (len(sizes) + 1) + "|"]
        for system in systems:
            cells = []
            for size in sizes:
                cell = summary["systems"][system][str(size)][metric]
                cells.append(f"{cell['mean']:.3f} ± {cell['sd_across_seeds']:.3f}")
            lines.append(f"| {system} | " + " | ".join(cells) + " |")
        lines.append("")
    lines += ["## slot_recall@5 by challenge bucket and pool size", "", "Mean over queries and seeds. n is the number of queries in the bucket.", ""]
    lines += ["| System | Bucket | n | " + " | ".join(str(s) for s in sizes) + " |", "|---" * (len(sizes) + 3) + "|"]
    for system in systems:
        for bucket in BUCKET_ORDER:
            cells = [fmt(summary["slot_recall@5_by_bucket"][system][str(size)][bucket]) for size in sizes]
            lines.append(f"| {system} | {bucket} | {summary['bucket_n'][bucket]} | " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    tools = load_tools()
    queries = load_eval_set()
    check_cache(tools, queries)

    rows = run_curve(tools, queries)
    if STATS.cache_misses or STATS.api_tokens:
        raise SystemExit(f"unexpected API activity: misses={STATS.cache_misses} tokens={STATS.api_tokens}")

    summary = summarise(rows, queries)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    MD_PATH.write_text(render_markdown(summary), encoding="utf-8")

    print(f"queries: {len(queries)}, tools: {len(tools)}, cache misses: {STATS.cache_misses}, api tokens: {STATS.api_tokens}")
    for system in summary["systems"]:
        print(system)
        for size in POOL_SIZES:
            cell = summary["systems"][system][str(size)][SLOT_METRIC]
            print(f"  size {size}: slot_recall@5 {cell['mean']:.3f} ± {cell['sd_across_seeds']:.3f}")
    print(f"wrote {JSON_PATH}")
    print(f"wrote {MD_PATH}")


if __name__ == "__main__":
    main()
