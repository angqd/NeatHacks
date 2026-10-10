# Full-catalog drop-in baseline (gpt-6-luna)

Date: 2026-10-11. All 527 tool definitions (id, description, input schema) go into one prompt of about 104,800 tokens, followed by the query. `gpt-6-luna` returns the tool ids it would use, most important first, through the OpenAI Agents SDK with a Pydantic output type. Scored with the same deterministic scorer as the other systems. Full tables are in `baseline_v0_tables.md` (systems `full_catalog:gpt-6-luna` and the uncached repeat `...:run2`).

`gpt-6-luna` rejects the `temperature` parameter, so calls are not strictly deterministic. The run was repeated once without the cache to measure that.

## Results

| Metric | BM25 | Embeddings | Full catalog, run 1 | Full catalog, run 2 |
| --- | --- | --- | --- | --- |
| Slot recall@5 | 0.412 | 0.517 | 0.599 [0.498, 0.694] | 0.637 [0.534, 0.734] |
| Full coverage@5 | 0.250 | 0.283 | 0.400 | 0.467 |
| R-precision | 0.221 | 0.374 | 0.638 | 0.614 |
| MRR | 0.428 | 0.589 | 0.701 | 0.678 |
| Confusion rate@5 | 0.237 | 0.288 | 0.136 | 0.102 |
| Unjudged@5 | 0.733 | 0.623 | 0.331 | 0.328 |
| LLM input tokens per query | none | none | 104,840 | 104,840 |
| Latency p50 | 0.24 ms | 0.18 ms (cached query) | 4.3 s | 4.1 s |

- The model returns a short list: 2.9 tools on average (0 to 13). So its "@5" numbers are set-level. Set-level recall is 0.64 and 0.66, precision 0.62 and 0.61, full coverage 0.47 and 0.50. R-precision (precision at k equal to the number of slots) is the size-fair comparison, and the model leads there (0.638 against 0.374 for embeddings).
- Paired against embeddings, run 1: slot recall@5 is +0.083 with an interval of [-0.045, 0.203], so not separated. R-precision is +0.269 [0.141, 0.395], with 32 wins and 7 losses. Against BM25: recall@5 +0.187 [0.044, 0.321], R-precision +0.427 [0.297, 0.550].
- Confusions are lower than both retrievers (0.10 to 0.14 against 0.24 and 0.29), which fits the idea that a reasoning model avoids look-alike tools better than similarity search. Confidence intervals are wide (n=59 queries with a listed confuser).
- No returned id was missing from the catalog (0 invalid ids in both runs).
- Cost in tokens: about 6.3M input tokens per full run of 60 queries. At the $0.01 per 1M input tokens quoted for `gpt-6-luna` that is about $0.06. Verify the current price.

## Stability

Two runs returned exactly the same tool set for 27 of 60 queries (45%). The averages agree (recall@5 0.599 and 0.637, a paired difference of -0.037 with an interval of [-0.114, 0.039]), but single-query answers move between runs. Per-bucket cells swing a lot (ambiguity recall 0.30 against 0.55, semantic distance 0.70 against 0.58, with 10 to 12 queries each). One or two queries returned an empty set in each run. Read bucket-level numbers from this baseline as noisy.

## What this changes

The bar for ToolPrune is higher than "beat BM25 and embeddings". Dropping the entire catalog into context with a cheap reasoning model already beats both retrievers on precision and confusions, at about 105k tokens and 4 seconds per query. The router's case must therefore rest on one of these:
- matching this accuracy with far fewer tokens (for example, a few thousand) and lower latency or cost per query,
- fewer confusions or higher coverage than this baseline on the hard buckets, once the enricher exists,
- scale: the catalog already uses 105k tokens, and a larger catalog will not fit in context at all.

Not yet shown: whether the full-catalog result holds on a catalog larger than the context window, how it behaves with more tools than 527, and how it compares to the embedding-plus-rerank baseline, which is the next one to run.
