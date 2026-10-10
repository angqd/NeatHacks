# Baseline report: BM25, embeddings, full catalog

Date: 2026-10-11. Frozen eval set, 60 queries (sha256 `305447a1...bf4afc`). Three baselines, all on raw tool documents. Every number comes from `toolprune.eval.score`. Cells show mean [95% bootstrap interval over queries]. Terms are defined in `glossary.md`.

| System | What it is |
| --- | --- |
| BM25 | Okapi BM25 (k1=1.5, b=0.75) over tool name, description, and server name. |
| Embeddings | OpenAI `text-embedding-3-small` cosine top-k over the same text. |
| Full catalog | All 527 tool definitions (about 104,800 tokens) in one `gpt-6-luna` prompt. The model returns the tool ids it would use. Run twice, because `gpt-6-luna` rejects `temperature` and the calls are not strictly deterministic. |

## Overall

| Metric | BM25 | Embeddings | Full catalog (run 1) | Full catalog (run 2) |
|---|---|---|---|---|
| Slot recall@1 | 0.172 [0.099, 0.254] | 0.242 [0.161, 0.328] | 0.348 [0.264, 0.435] | 0.328 [0.239, 0.421] |
| Slot recall@5 | 0.412 [0.312, 0.512] | 0.517 [0.425, 0.608] | 0.599 [0.498, 0.694] | 0.637 [0.534, 0.734] |
| Slot recall@10 | 0.467 [0.368, 0.568] | 0.625 [0.535, 0.714] | 0.634 [0.532, 0.731] | 0.662 [0.557, 0.760] |
| Full coverage@5 | 0.250 [0.150, 0.367] | 0.283 [0.167, 0.400] | 0.400 [0.283, 0.517] | 0.467 [0.333, 0.600] |
| Precision@5 | 0.177 [0.137, 0.217] | 0.253 [0.207, 0.303] | 0.618 [0.516, 0.714] | 0.610 [0.514, 0.705] |
| R-precision | 0.221 [0.146, 0.301] | 0.374 [0.283, 0.467] | 0.638 [0.533, 0.737] | 0.614 [0.510, 0.715] |
| MRR | 0.428 [0.326, 0.533] | 0.589 [0.491, 0.685] | 0.701 [0.592, 0.801] | 0.678 [0.574, 0.778] |
| Confusion rate@5 | 0.237 [0.136, 0.339] | 0.288 [0.169, 0.407] | 0.136 [0.051, 0.220] | 0.102 [0.034, 0.186] |
| Confuser-first rate@5 | 0.186 [0.102, 0.288] | 0.153 [0.068, 0.254] | 0.068 [0.017, 0.136] | 0.068 [0.017, 0.136] |
| Unjudged@5 | 0.733 [0.677, 0.790] | 0.623 [0.557, 0.690] | 0.331 [0.241, 0.426] | 0.328 [0.239, 0.420] |
| Returned-tool tokens@5 | 1153 | 1028 | 576 | 569 |
| Retrieval LLM input tokens per query | 0 | 0 | 104,840 | 104,840 |
| Latency p50 / p95 (ms) | 0.24 / 0.91 | 0.18 / 0.23 | 4279.19 / 7347.75 | 4227.98 / 8110.00 |
| Returned set size (mean) | 5 (fixed) | 5 (fixed) | 2.92 | 2.88 |

Notes: BM25 and embeddings return a fixed top-k, so their precision is capped by k. R-precision (precision at k equal to the number of slots) is the size-fair comparison. The full-catalog model returns a short set (about 3 tools), so its "@5" numbers are set-level. The embedding latency excludes the OpenAI call for the query, which comes from the cache.

## Slot recall@5 by challenge bucket

| Bucket | n | BM25 | Embeddings | Full catalog (run 1) | Full catalog (run 2) |
|---|---|---|---|---|---|
| ambiguity | 10 | 0.592 | 0.600 | 0.225 | 0.475 |
| multi_capability | 15 | 0.211 | 0.383 | 0.572 | 0.633 |
| near_duplicate | 9 | 0.519 | 0.500 | 0.685 | 0.722 |
| none | 4 | 1.000 | 0.750 | 1.000 | 0.750 |
| semantic_distance | 12 | 0.208 | 0.500 | 0.662 | 0.579 |
| taxonomy_collision | 10 | 0.450 | 0.575 | 0.700 | 0.750 |

## R-precision by challenge bucket

| Bucket | n | BM25 | Embeddings | Full catalog (run 1) | Full catalog (run 2) |
|---|---|---|---|---|---|
| ambiguity | 10 | 0.408 | 0.533 | 0.500 | 0.528 |
| multi_capability | 15 | 0.194 | 0.222 | 0.478 | 0.530 |
| near_duplicate | 9 | 0.333 | 0.333 | 0.685 | 0.722 |
| none | 4 | 0.000 | 0.250 | 1.000 | 0.750 |
| semantic_distance | 12 | 0.083 | 0.458 | 0.792 | 0.625 |
| taxonomy_collision | 10 | 0.225 | 0.425 | 0.617 | 0.650 |

## Confusion rate@5 by challenge bucket

| Bucket | n | BM25 | Embeddings | Full catalog (run 1) | Full catalog (run 2) |
|---|---|---|---|---|---|
| ambiguity | 10 | 0.300 | 0.300 | 0.300 | 0.300 |
| multi_capability | 15 | 0.333 | 0.267 | 0.200 | 0.067 |
| near_duplicate | 9 | 0.125 | 0.375 | 0.000 | 0.000 |
| none | 4 | 0.000 | 0.000 | 0.000 | 0.000 |
| semantic_distance | 12 | 0.167 | 0.167 | 0.167 | 0.167 |
| taxonomy_collision | 10 | 0.300 | 0.500 | 0.000 | 0.000 |

Bucket cells use recall cut at 5 (the stability paragraph in `full_catalog_v0.md` quotes set-level recall with no cut, so its bucket figures differ slightly). Bucket cells hold 4 to 15 queries and carry no intervals. Treat them as pointers. The two full-catalog runs differ by up to 0.25 in a bucket, which shows how noisy a single cell is.

## Stability of the full-catalog run

The two runs returned the identical tool set on 27 of 60 queries. Averages agree within their intervals.

## Other results

- Noise scaling (pool of 50, 100, 250, 527 tools): `noise_scaling.md`. Slot recall@5 falls from 0.60 to 0.41 for BM25 and from 0.78 to 0.52 for embeddings.
- BM25 sanity check against the self-reported 31.68 Recall@5 on the original bench: `sanity_bm25.md` (36.06 for the default document).
- Catalog audit: `catalog_audit.md` (100,496 tokens, 13 shared names across 30 tools, 66 weak descriptions).
- Detailed tables and paired comparisons: `baseline_v0_tables.md`. Interpretation: `baseline_v0.md` and `full_catalog_v0.md`.

## Missing from this report

Embedding plus LLM rerank, LLM-judge scores (sufficiency, labels for unjudged tools), cold latency, miss-cause analysis, and every ToolPrune system (enriched embeddings, router).

