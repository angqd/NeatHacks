"""Run the hierarchical router over the frozen eval set and write one returned set per query.

Each query is timed as a whole, so latency includes every LLM stage. The returned set's tokens
are the raw definition tokens of the returned tools (eval/tokens.py). A query whose retrieve call
raises is recorded with an empty set and its error text, and the run carries on.

Run with: python -m toolprune.eval.route_run --group-by server|domain [--limit N] [--no-cache] [--tag NAME] [--annotations pass1|final]
"""

import argparse
import re
import time

import numpy as np

from toolprune.eval.sets import SET_NAMES, load_queries, run_suffix
from toolprune.eval.tokens import tool_tokens
from toolprune.models import ROOT, RetrievedSet, load_tools
from toolprune.route.router import HierarchicalRouter

K = 10
RUNS_DIR = ROOT / "reports" / "runs"
TAG_PATTERN = re.compile(r"[A-Za-z0-9_-]+")
ERROR_CHARS = 300
PROGRESS_EVERY = 10


def print_summary(system: str, sets: list[RetrievedSet], errors: int) -> None:
    latencies = np.array([item.latency_ms for item in sets], dtype=float)
    input_tokens = np.array([item.meta["llm_input_tokens"] for item in sets], dtype=float)
    llm_calls = np.array([item.meta["llm_calls"] for item in sets], dtype=float)
    widened = sum(1 for item in sets if item.meta.get("widened"))
    sizes = np.array([len(item.ranked) for item in sets], dtype=float)
    empty = sum(1 for item in sets if not item.ranked)
    print(system)
    print(f"  queries: {len(sets)}  errors: {errors}")
    print(f"  mean llm_input_tokens: {input_tokens.mean():.1f}")
    print(f"  mean llm_calls: {llm_calls.mean():.2f}")
    print(f"  widened: {widened}/{len(sets)} ({widened / len(sets):.1%})")
    print(f"  latency_ms p50: {np.percentile(latencies, 50):.2f}  p95: {np.percentile(latencies, 95):.2f}")
    print(f"  mean returned set size: {sizes.mean():.2f}")
    print(f"  empty sets: {empty}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Hierarchical router over the frozen eval set.")
    parser.add_argument("--group-by", required=True, choices=["server", "domain"], help="grouping level of the router")
    parser.add_argument("--limit", type=int, default=None, help="run only the first N queries of the eval set")
    parser.add_argument("--no-cache", action="store_true", help="bypass the LLM cache for reads and writes")
    parser.add_argument("--tag", default=None, help="run tag, added to the system name and output file name")
    parser.add_argument("--annotations", default="pass1", choices=["pass1", "final"], help="tag cards to route over")
    parser.add_argument("--eval-set", choices=SET_NAMES, default="frozen", help="query set to run")
    args = parser.parse_args()

    if args.tag is not None and not TAG_PATTERN.fullmatch(args.tag):
        raise SystemExit("--tag may contain only letters, digits, '_' and '-'")

    router = HierarchicalRouter(group_by=args.group_by, annotations=args.annotations, use_cache=not args.no_cache)
    tools_by_id = {tool.id: tool for tool in load_tools()}
    queries = load_queries(args.eval_set)
    if args.limit is not None:
        queries = queries[: args.limit]

    system = router.name
    if args.tag:
        system = f"{system}:{args.tag}"

    sets: list[RetrievedSet] = []
    errors = 0
    for index, query in enumerate(queries, start=1):
        start = time.perf_counter()
        error = None
        try:
            ranked = router.retrieve(query.question, K)
        except Exception as exc:  # record the failure and keep the run going
            ranked = []
            errors += 1
            error = f"{type(exc).__name__}: {str(exc)[:ERROR_CHARS]}"
            print(f"error on {query.task_id}: {error}")
        latency_ms = (time.perf_counter() - start) * 1000

        per_tool = {item.tool_id: tool_tokens(tools_by_id[item.tool_id]) for item in ranked}
        meta = {"k": K, "tool_tokens": per_tool, "split": query.split, **router.last_meta}
        if error is not None:
            meta["error"] = error
        sets.append(
            RetrievedSet(
                query_id=query.task_id,
                system=system,
                ranked=ranked,
                latency_ms=latency_ms,
                tokens=sum(per_tool.values()),
                meta=meta,
            )
        )
        if index % PROGRESS_EVERY == 0 or index == len(queries):
            print(f"progress: {index}/{len(queries)} queries")

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    file_name = f"{router.name}{run_suffix(args.eval_set)}"
    if args.tag:
        file_name = f"{file_name}:{args.tag}"
    path = RUNS_DIR / f"{file_name.replace(':', '__')}.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for item in sets:
            handle.write(item.model_dump_json() + "\n")

    print_summary(system, sets, errors)
    print(f"  wrote {path}")


if __name__ == "__main__":
    main()
