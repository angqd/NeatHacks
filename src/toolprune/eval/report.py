"""Build reports/results.json and reports/baseline_v0_tables.md from the saved retrieval runs.

Every metric comes from toolprune.eval.score. The only computation outside score.py is the
latency p50 and p95, taken as percentiles of the per-query latency_ms values.
Run with: python -m toolprune.eval.report
"""

import json
from collections import defaultdict
from typing import Any

import numpy as np

from toolprune.eval.score import bootstrap_ci, mean, paired_difference, score_query, top_ids
from toolprune.models import ROOT, EvalQuery, RetrievedSet, load_eval_set, read_jsonl

RUNS_DIR = ROOT / "reports" / "runs"
REPORTS_DIR = ROOT / "reports"
RESULTS_PATH = REPORTS_DIR / "results.json"
TABLES_PATH = REPORTS_DIR / "baseline_v0_tables.md"

OVERALL_ROWS = [
    "slot_recall@1",
    "slot_recall@5",
    "slot_recall@10",
    "full_coverage@5",
    "precision@5",
    "r_precision",
    "mrr",
    "confusion@5",
    "confuser_first@5",
    "unjudged@5",
    "tokens@5",
    "latency_ms",
]
BUCKET_METRICS = ["slot_recall@5", "full_coverage@5", "r_precision", "confusion@5"]
FAMILY_METRICS = ["slot_recall@5"]
SPLIT_METRICS = ["slot_recall@5", "full_coverage@5"]
PAIRED_METRICS = ["slot_recall@5", "full_coverage@5", "r_precision", "mrr"]


def load_runs() -> dict[str, dict[str, RetrievedSet]]:
    """System name -> {query_id: RetrievedSet}, one entry per runs file, in filename order."""
    runs: dict[str, dict[str, RetrievedSet]] = {}
    for path in sorted(RUNS_DIR.glob("*.jsonl")):
        sets = [RetrievedSet(**row) for row in read_jsonl(path)]
        names = {rs.system for rs in sets}
        if len(names) != 1:
            raise ValueError(f"{path.name} holds {len(names)} system names, expected one")
        by_query: dict[str, RetrievedSet] = {}
        for rs in sets:
            if rs.query_id in by_query:
                raise ValueError(f"{path.name} repeats query_id {rs.query_id}")
            by_query[rs.query_id] = rs
        runs[names.pop()] = by_query
    return runs


def score_system(
    queries: list[EvalQuery], by_query: dict[str, RetrievedSet]
) -> tuple[dict[str, dict[str, Any]], list[tuple[EvalQuery, dict[str, Any]]]]:
    per_query: dict[str, dict[str, Any]] = {}
    rows: list[tuple[EvalQuery, dict[str, Any]]] = []
    for q in queries:
        rs = by_query.get(q.task_id)
        if rs is None:
            raise KeyError(f"no returned set for query {q.task_id}")
        metrics = score_query(q, rs)
        per_query[q.task_id] = {**metrics, "returned_ids": top_ids(rs, 10)}
        rows.append((q, metrics))
    return per_query, rows


def summarize(values: list[float | None]) -> dict[str, Any]:
    ci = bootstrap_ci(values)
    return {"mean": mean(values), "ci95": list(ci) if ci else None}


def group_summary(rows: list[tuple[EvalQuery, dict[str, Any]]], field: str) -> dict[str, Any]:
    """Micro mean per group (mean over its queries), n per group, and macro (mean of group means)."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for q, m in rows:
        groups[str(getattr(q, field))].append(m)
    keys = list(rows[0][1].keys())
    out: dict[str, Any] = {}
    for g in sorted(groups):
        entry: dict[str, Any] = {"n": len(groups[g])}
        for k in keys:
            entry[k] = mean([m[k] for m in groups[g]])
        out[g] = entry
    macro = {k: mean([out[g][k] for g in out]) for k in keys}
    return {"groups": out, "macro": macro}


def aggregate(rows: list[tuple[EvalQuery, dict[str, Any]]]) -> dict[str, Any]:
    keys = list(rows[0][1].keys())
    overall = {k: summarize([m[k] for _, m in rows]) for k in keys}
    latencies = [m["latency_ms"] for _, m in rows if m["latency_ms"] is not None]
    overall["latency_p50_ms"] = float(np.percentile(latencies, 50))
    overall["latency_p95_ms"] = float(np.percentile(latencies, 95))
    return {
        "overall": overall,
        "by_bucket": group_summary(rows, "bucket"),
        "by_family": group_summary(rows, "family"),
        "by_split": group_summary(rows, "split"),
    }


def paired(systems: list[str], rows: dict[str, list[tuple[EvalQuery, dict[str, Any]]]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for a in systems:
        for b in systems:
            if a == b:
                continue
            out[f"{a} - {b}"] = {
                k: paired_difference([m[k] for _, m in rows[a]], [m[k] for _, m in rows[b]])
                for k in PAIRED_METRICS
            }
    return out


def fmt(x: float | None) -> str:
    return "n/a" if x is None else f"{x:.3f}"


def fmt_ci(s: dict[str, Any]) -> str:
    if s["mean"] is None:
        return "n/a"
    if s["ci95"] is None:
        return fmt(s["mean"])
    lo, hi = s["ci95"]
    return f"{fmt(s['mean'])} [{fmt(lo)}, {fmt(hi)}]"


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines)


def render_tables(systems: list[str], n_queries: int, agg: dict[str, Any], paired_res: dict[str, Any]) -> str:
    sections: list[str] = [
        "# Baseline v0 tables",
        "",
        "Scores are deterministic. Challenge bucket and task family are eval annotations. "
        f"n={n_queries} queries, so intervals are wide.",
        "",
    ]

    # 1. Overall
    sections.append("## 1. Overall (all %d queries)" % n_queries)
    sections.append("Cells are mean [95% bootstrap CI]. Latency p50 and p95 are point values.")
    sections.append("")
    rows = []
    for metric in OVERALL_ROWS:
        rows.append([metric] + [fmt_ci(agg[s]["overall"][metric]) for s in systems])
    rows.append(["latency p50 (ms)"] + [fmt(agg[s]["overall"]["latency_p50_ms"]) for s in systems])
    rows.append(["latency p95 (ms)"] + [fmt(agg[s]["overall"]["latency_p95_ms"]) for s in systems])
    sections.append(md_table(["Metric", *systems], rows))
    sections.append("")

    # 2. Bucket
    sections.append("## 2. Per challenge bucket (mean over queries)")
    sections.append("")
    rows = []
    buckets = agg[systems[0]]["by_bucket"]["groups"].keys()
    for b in buckets:
        for s in systems:
            g = agg[s]["by_bucket"]["groups"][b]
            rows.append([b, s, str(g["n"])] + [fmt(g[k]) for k in BUCKET_METRICS])
    sections.append(md_table(["Bucket", "System", "n", *BUCKET_METRICS], rows))
    sections.append("")

    # 3. Family
    sections.append("## 3. Per task family (mean over queries)")
    sections.append("")
    rows = []
    for fam in agg[systems[0]]["by_family"]["groups"].keys():
        for s in systems:
            g = agg[s]["by_family"]["groups"][fam]
            rows.append([fam, s, str(g["n"])] + [fmt(g[k]) for k in FAMILY_METRICS])
    sections.append(md_table(["Family", "System", "n", *FAMILY_METRICS], rows))
    sections.append("")

    # 4. Split
    sections.append("## 4. Per split (mean over queries)")
    sections.append("")
    rows = []
    for sp in agg[systems[0]]["by_split"]["groups"].keys():
        for s in systems:
            g = agg[s]["by_split"]["groups"][sp]
            rows.append([sp, s, str(g["n"])] + [fmt(g[k]) for k in SPLIT_METRICS])
    sections.append(md_table(["Split", "System", "n", *SPLIT_METRICS], rows))
    sections.append("")

    # 5. Paired
    sections.append("## 5. Paired comparisons (A minus B, same queries)")
    sections.append("")
    for pair, metrics in paired_res.items():
        sections.append(f"### {pair}")
        sections.append("")
        rows = []
        for k in PAIRED_METRICS:
            d = metrics[k]
            if d["n"] == 0:
                rows.append([k, "n/a", "n/a", "0", "0", "0", "0"])
                continue
            lo, hi = d["ci95"]
            rows.append(
                [
                    k,
                    fmt(d["mean_diff"]),
                    f"[{fmt(lo)}, {fmt(hi)}]",
                    str(d["wins"]),
                    str(d["losses"]),
                    str(d["ties"]),
                    str(d["n"]),
                ]
            )
        sections.append(md_table(["Metric", "Mean diff", "CI95", "Wins", "Losses", "Ties", "n"], rows))
        sections.append("")

    return "\n".join(sections)


def main() -> None:
    queries = load_eval_set()
    runs = load_runs()
    systems = list(runs)

    per_query: dict[str, dict[str, Any]] = {}
    rows: dict[str, list[tuple[EvalQuery, dict[str, Any]]]] = {}
    by_system: dict[str, Any] = {}
    for s in systems:
        per_query[s], rows[s] = score_system(queries, runs[s])
        by_system[s] = aggregate(rows[s])
    paired_res = paired(systems, rows)

    results = {
        "systems": systems,
        "per_query": per_query,
        "aggregates": {"by_system": by_system, "paired": paired_res},
    }
    REPORTS_DIR.mkdir(exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    TABLES_PATH.write_text(render_tables(systems, len(queries), by_system, paired_res), encoding="utf-8")
    print(f"wrote {RESULTS_PATH}")
    print(f"wrote {TABLES_PATH}")


if __name__ == "__main__":
    main()
