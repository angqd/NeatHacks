"""OpenAI embeddings with an on-disk SQLite cache, and the embedding retriever.

Texts are truncated to MAX_CHARS and cached by sha256 of "{model}\\n{text}" as float32 bytes.
Only cache misses reach the API, in batches of at most BATCH_SIZE distinct texts.
Run the check with: python -m toolprune.embeddings
"""

import hashlib
import logging
import os
import sqlite3
from contextlib import closing
from dataclasses import dataclass

import numpy as np
from openai import OpenAI

from toolprune.bm25 import DEFAULT_QUERY
from toolprune.env import load_env
from toolprune.models import ROOT, RankedTool, Tool, load_eval_set, load_tools
from toolprune.text import tool_document
from toolprune.tracing import init_tracing

logger = logging.getLogger(__name__)

MODEL = "text-embedding-3-small"
CACHE_PATH = ROOT / "data" / "cache" / "embeddings.sqlite"
MAX_CHARS = 8000
BATCH_SIZE = 128


@dataclass
class EmbeddingStats:
    cache_hits: int = 0
    cache_misses: int = 0
    api_tokens: int = 0


STATS = EmbeddingStats()


def _key(text: str, model: str) -> str:
    return hashlib.sha256(f"{model}\n{text}".encode("utf-8")).hexdigest()


def _open_cache() -> sqlite3.Connection:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(CACHE_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS embeddings ("
        "key TEXT PRIMARY KEY, model TEXT, dim INTEGER, vector BLOB, tokens INTEGER)"
    )
    return conn


def _client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=api_key)


def embed_texts(texts: list[str], model: str = MODEL) -> np.ndarray:
    """Return a float32 array of shape (len(texts), dim) in input order, using the cache first."""
    if not texts:
        return np.empty((0, 0), dtype=np.float32)
    load_env()
    clipped = [text[:MAX_CHARS] for text in texts]
    keys = [_key(text, model) for text in clipped]
    found: dict[str, np.ndarray] = {}
    missing: dict[str, str] = {}

    with closing(_open_cache()) as conn:
        for key, text in zip(keys, clipped):
            if key in found:
                STATS.cache_hits += 1
            elif key in missing:
                STATS.cache_misses += 1
            else:
                row = conn.execute("SELECT vector FROM embeddings WHERE key = ?", (key,)).fetchone()
                if row is None:
                    missing[key] = text
                    STATS.cache_misses += 1
                else:
                    found[key] = np.frombuffer(row[0], dtype=np.float32)
                    STATS.cache_hits += 1

        if missing:
            client = _client()
            pending = list(missing.items())
            for start in range(0, len(pending), BATCH_SIZE):
                batch = pending[start : start + BATCH_SIZE]
                resp = client.embeddings.create(model=model, input=[text for _, text in batch])
                tokens = resp.usage.total_tokens
                STATS.api_tokens += tokens
                logger.info("embeddings: model=%s inputs=%d tokens=%d", model, len(batch), tokens)
                rows = []
                ordered = sorted(resp.data, key=lambda item: item.index)
                for i, ((key, _), item) in enumerate(zip(batch, ordered)):
                    share = tokens // len(batch) + (i < tokens % len(batch))
                    vector = np.asarray(item.embedding, dtype=np.float32)
                    found[key] = vector
                    rows.append((key, model, vector.size, vector.tobytes(), share))
                conn.executemany(
                    "INSERT OR REPLACE INTO embeddings (key, model, dim, vector, tokens) VALUES (?, ?, ?, ?, ?)",
                    rows,
                )
                conn.commit()

    return np.stack([found[key] for key in keys]).astype(np.float32)


class EmbeddingRetriever:
    def __init__(self, tools: list[Tool], variant: str = "name_desc_server", model: str = MODEL):
        self.name = f"emb:{model}:{variant}"
        self.model = model
        self.tool_ids = [tool.id for tool in tools]
        matrix = embed_texts([tool_document(tool, variant) for tool in tools], model)
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


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    init_tracing("tool-retrieval-eval")
    tools = load_tools()
    questions = [query.question for query in load_eval_set()]
    retriever = EmbeddingRetriever(tools)
    question_vectors = embed_texts(questions)
    ranked = retriever.retrieve(DEFAULT_QUERY, 5)

    print(f"tools: {len(tools)}")
    print(f"eval questions: {len(questions)}")
    print(f"vector shape: {retriever.matrix.shape}, question vectors: {question_vectors.shape}")
    print(f"cache hits: {STATS.cache_hits}")
    print(f"cache misses: {STATS.cache_misses}")
    print(f"api tokens: {STATS.api_tokens}")
    print(f"top 5 for {DEFAULT_QUERY!r} ({retriever.name}):")
    for rank in ranked:
        print(f"  {rank.score:.4f} {rank.tool_id}")


if __name__ == "__main__":
    main()
