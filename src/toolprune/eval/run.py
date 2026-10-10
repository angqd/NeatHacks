"""Run retrieval systems over the frozen eval set and save the returned sets.

For each system and query, one retrieve call is timed and saved as a RetrievedSet.
Output goes to reports/runs/<system name with ':' replaced by '__'>.jsonl, one set per
line, in eval-set order. Latency is the only field that changes between runs.

Run with: python -m toolprune.eval.run [--systems bm25,emb] [--k 10] [--split dev|test]
"""

import argparse
import time
from pathlib import Path

import numpy as np

from toolprune.bm25 import BM25Retriever
from toolprune.embeddings import EmbeddingRetriever
from toolprune.eval.tokens import tool_tokens
from toolprune.models import ROOT, EvalQuery, RetrievedSet, Retriever, Tool, load_eval_set, load_tools
from toolprune.tracing import init_tracing

RUNS_DIR = ROOT / "reports" / "runs"
VARIANT = "name_desc_server"
DEFAULT_SYSTEMS = "bm25,emb"


def build_retrievers(names: list[str], tools: list[Tool]) -> dict[str, Retriever]:
    builders = {
        "bm25": lambda: BM25Retriever(tools, VARIANT),
        "emb": lambda: EmbeddingRetriever(tools, VARIANT),
    }
    unknown = [name for name in names if name not in builders]
    if unknown:
        raise SystemExit(f"unknown system(s): {', '.join(unknown)}; choose from {', '.join(builders)}")
    return {name: builders[name]() for name in names}


def run_system(retriever: Retriever, queries: list[EvalQuery], tools_by_id: dict[str, Tool], k: int) -> list[RetrievedSet]:
    sets: list[RetrievedSet] = []
    for query in queries:
        start = time.perf_counter()
        ranked = retriever.retrieve(query.question, k)
        latency_ms = (time.perf_counter() - start) * 1000

        returned = [tools_by_id[hit.tool_id] for hit in ranked]
        per_tool = {tool.id: tool_tokens(tool) for tool in returned}
        meta: dict = {"k": k, "tool_tokens": per_tool, "split": query.split}
        if retriever.name.startswith("emb:"):
            meta["query_embedding_cached"] = True
        sets.append(
            RetrievedSet(
                query_id=query.task_id,
                system=retriever.name,
                ranked=ranked,
                latency_ms=latency_ms,
                tokens=sum(per_tool.values()),
                meta=meta,
            )
        )
    return sets


def save_sets(name: str, sets: list[RetrievedSet]) -> Path:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    path = RUNS_DIR / f"{name.replace(':', '__')}.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for item in sets:
            handle.write(item.model_dump_json() + "\n")
    return path


def print_summary(name: str, sets: list[RetrievedSet]) -> None:
    latencies = np.array([item.latency_ms for item in sets], dtype=float)
    tokens = np.array([item.tokens for item in sets], dtype=float)
    print(f"{name}")
    print(f"  queries: {len(sets)}")
    print(f"  latency_ms p50: {np.percentile(latencies, 50):.2f}  p95: {np.percentile(latencies, 95):.2f}")
    print(f"  mean tokens: {tokens.mean():.1f}")
    for item in sets[:3]:
        top = ", ".join(hit.tool_id for hit in item.ranked[:3])
        print(f"  {item.query_id}: {top}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run retrieval systems over the frozen eval set.")
    parser.add_argument("--systems", default=DEFAULT_SYSTEMS, help="comma list of: bm25, emb")
    parser.add_argument("--k", type=int, default=10, help="number of tools to return per query")
    parser.add_argument("--split", choices=["dev", "test"], default=None, help="restrict to one split")
    args = parser.parse_args()

    init_tracing("tool-retrieval-eval")
    names = [name.strip() for name in args.systems.split(",") if name.strip()]
    tools = load_tools()
    tools_by_id = {tool.id: tool for tool in tools}
    queries = load_eval_set(args.split)
    retrievers = build_retrievers(names, tools)

    for name, retriever in retrievers.items():
        sets = run_system(retriever, queries, tools_by_id, args.k)
        path = save_sets(retriever.name, sets)
        print_summary(retriever.name, sets)
        print(f"  wrote {path}")


if __name__ == "__main__":
    main()
