"""Deterministic Okapi BM25 retriever over the raw-text tool-document variants.

Term order, score accumulation and ties are fixed by sorted query terms and input order,
so the ranking does not depend on the hash seed.
"""

import math
import sys
from collections import Counter

from toolprune.models import RankedTool, Tool, load_tools
from toolprune.text import tokenize, tool_document

DEFAULT_QUERY = "find research papers about transformers"


class BM25Retriever:
    def __init__(self, tools: list[Tool], variant: str = "name_desc_server", k1: float = 1.5, b: float = 0.75):
        self.name = f"bm25:{variant}"
        self.k1 = k1
        self.b = b
        self.tool_ids = [tool.id for tool in tools]
        self.doc_tf = [Counter(tokenize(tool_document(tool, variant))) for tool in tools]
        self.doc_len = [sum(tf.values()) for tf in self.doc_tf]
        self.n_docs = len(tools)
        self.avg_len = sum(self.doc_len) / self.n_docs if self.n_docs else 0.0
        self.df: Counter[str] = Counter()
        for tf in self.doc_tf:
            self.df.update(tf.keys())

    def _idf(self, term: str) -> float:
        n = self.df[term]
        return math.log(1 + (self.n_docs - n + 0.5) / (n + 0.5))

    def retrieve(self, query: str, k: int) -> list[RankedTool]:
        if k <= 0:
            return []
        terms = sorted(set(tokenize(query)))
        scores: dict[int, float] = {}
        for term in terms:
            if self.df[term] == 0:
                continue
            idf = self._idf(term)
            for idx, tf_map in enumerate(self.doc_tf):
                freq = tf_map.get(term, 0)
                if freq == 0:
                    continue
                norm = 1 - self.b + self.b * self.doc_len[idx] / self.avg_len
                weight = idf * freq * (self.k1 + 1) / (freq + self.k1 * norm)
                scores[idx] = scores.get(idx, 0.0) + weight
        ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
        return [RankedTool(tool_id=self.tool_ids[idx], score=score) for idx, score in ranked[:k] if score > 0]


def main(argv: list[str]) -> None:
    query = " ".join(argv) if argv else DEFAULT_QUERY
    retriever = BM25Retriever(load_tools())
    for hit in retriever.retrieve(query, 5):
        print(f"{hit.score:.4f} {hit.tool_id}")


if __name__ == "__main__":
    main(sys.argv[1:])
