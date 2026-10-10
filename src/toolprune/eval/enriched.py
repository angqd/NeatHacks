"""Ablation: does enrichment alone, with no hierarchy, help retrieval?

Each tool gets one card text per variant, built from its pass-1 tag: the summary and intents,
plus the topic for tag_topic, and the raw tool document for raw_tag. Effect text and the
domain are never used. The systems run on the same 60 eval queries as the baselines, are
saved in the same RetrievedSet format, and are scored with the same scorer.

Run with: python -m toolprune.eval.enriched
"""

from collections import Counter

import numpy as np

from toolprune.bm25 import BM25Retriever
from toolprune.embeddings import MODEL, STATS, embed_texts
from toolprune.enrich.models import ToolTag
from toolprune.eval import score
from toolprune.eval.run import run_system, save_sets
from toolprune.models import ROOT, EvalQuery, RankedTool, RetrievedSet, Retriever, Tool, load_eval_set, load_tools, read_jsonl
from toolprune.text import tokenize, tool_document
from toolprune.tracing import init_tracing

TAGS_PATH = ROOT / "data" / "enriched" / "pass1_annotations.jsonl"
RUNS_DIR = ROOT / "reports" / "runs"
VARIANTS = ("tag", "raw_tag", "tag_topic")
BM25_VARIANTS = ("raw_tag", "tag")
BASELINE_RUNS = {
    "bm25:name_desc_server": RUNS_DIR / "bm25__name_desc_server.jsonl",
    f"emb:{MODEL}:name_desc_server": RUNS_DIR / f"emb__{MODEL}__name_desc_server.jsonl",
}
METRICS = ("slot_recall@5", "full_coverage@5", "r_precision", "mrr")
K = 10


def load_tags() -> dict[str, ToolTag]:
    return {row["tool_id"]: ToolTag(**row) for row in read_jsonl(TAGS_PATH)}


def card_text(tool: Tool, tag: ToolTag, variant: str) -> str:
    if variant == "tag":
        parts = [tag.summary, *tag.intents]
    elif variant == "raw_tag":
        parts = [tool_document(tool, "name_desc_server"), tag.summary, *tag.intents]
    elif variant == "tag_topic":
        parts = [tag.topic.replace("_", " "), tag.summary, *tag.intents]
    else:
        raise ValueError(f"unknown variant {variant!r}; expected one of {VARIANTS}")
    return "\n".join(p for p in parts if p)


class EnrichedEmbeddingRetriever:
    def __init__(self, tools: list[Tool], texts: list[str], variant: str, model: str = MODEL):
        self.name = f"emb:{model}:enriched_{variant}"
        self.model = model
        self.tool_ids = [tool.id for tool in tools]
        matrix = embed_texts(texts, model)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        self.matrix = matrix / np.maximum(norms, 1e-12)

    def retrieve(self, query: str, k: int) -> list[RankedTool]:
        if k <= 0:
            return []
        vector = embed_texts([query], self.model)[0]
        vector = vector / max(float(np.linalg.norm(vector)), 1e-12)
        scores = self.matrix @ vector
        order = np.argsort(-scores, kind="stable")[:k]
        return [RankedTool(tool_id=self.tool_ids[i], score=float(scores[i])) for i in order]


class EnrichedBM25Retriever(BM25Retriever):
    """BM25Retriever scoring over card_text documents instead of tool_document variants."""

    def __init__(self, tools: list[Tool], texts: list[str], variant: str, k1: float = 1.5, b: float = 0.75):
        self.name = f"bm25:enriched_{variant}"
        self.k1 = k1
        self.b = b
        self.tool_ids = [tool.id for tool in tools]
        self.doc_tf = [Counter(tokenize(text)) for text in texts]
        self.doc_len = [sum(tf.values()) for tf in self.doc_tf]
        self.n_docs = len(tools)
        self.avg_len = sum(self.doc_len) / self.n_docs if self.n_docs else 0.0
        self.df: Counter[str] = Counter()
        for tf in self.doc_tf:
            self.df.update(tf.keys())


def build_retrievers(tools: list[Tool], tags: dict[str, ToolTag]) -> list[Retriever]:
    texts = {variant: [card_text(tool, tags[tool.id], variant) for tool in tools] for variant in VARIANTS}
    retrievers: list[Retriever] = [EnrichedEmbeddingRetriever(tools, texts[variant], variant) for variant in VARIANTS]
    retrievers += [EnrichedBM25Retriever(tools, texts[variant], variant) for variant in BM25_VARIANTS]
    return retrievers


def summarize(sets: list[RetrievedSet], queries_by_id: dict[str, EvalQuery]) -> dict[str, float | None]:
    rows = [score.score_query(queries_by_id[item.query_id], item) for item in sets]
    return {metric: score.mean([row[metric] for row in rows]) for metric in METRICS}


def load_sets(path) -> list[RetrievedSet]:
    return [RetrievedSet(**row) for row in read_jsonl(path)]


def fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


def main() -> None:
    init_tracing("tool-retrieval-eval")
    tools = load_tools()
    tools_by_id = {tool.id: tool for tool in tools}
    tags = load_tags()
    missing = [tool.id for tool in tools if tool.id not in tags]
    if missing:
        raise SystemExit(f"{len(missing)} tool(s) have no pass-1 tag, first: {missing[0]}")
    queries = load_eval_set()
    queries_by_id = {query.task_id: query for query in queries}

    table: list[tuple[str, dict[str, float | None]]] = []
    for name, path in BASELINE_RUNS.items():
        table.append((name, summarize(load_sets(path), queries_by_id)))

    for retriever in build_retrievers(tools, tags):
        sets = run_system(retriever, queries, tools_by_id, K)
        path = save_sets(retriever.name, sets)
        print(f"wrote {path} ({len(sets)} queries)")
        table.append((retriever.name, summarize(sets, queries_by_id)))

    print(f"api tokens: {STATS.api_tokens}  embedding cache misses: {STATS.cache_misses}")
    width = max(len(name) for name, _ in table)
    header = "system".ljust(width) + "".join(f"  {metric:>16}" for metric in METRICS)
    print(header)
    for name, summary in table:
        print(name.ljust(width) + "".join(f"  {fmt(summary[metric]):>16}" for metric in METRICS))


if __name__ == "__main__":
    main()
