# Noise-scaling curve

Pool construction rules:

- Every acceptable tool of the query (each slot's pick and alternates) is always in the pool.
- The rest of the pool is a uniform random sample without replacement from the other catalog tools, up to the pool size.
- The sample uses numpy `default_rng`, seeded from a sha256 of (seed, pool size, query task_id).
- Listed confusers are not specially kept. They enter the pool only if sampled.
- Pool size 527 is the full catalog, with no sampling.
- BM25 is rebuilt per pool (`name_desc_server`). Embeddings rank the full catalog once, and the order is restricted to the pool.
- Each returned set is cut to the top 10 and scored with `toolprune.eval.score.score_query`.

60 queries, 5 seeds (0 to 4).
Cells are the mean over queries and seeds, with ± the sample standard deviation (ddof=1) across seeds of the per-seed query means.
At size 527 every seed gives the same pool, so the ± is 0.

## slot_recall@5 by pool size

| System | 50 | 100 | 250 | 527 |
|---|---|---|---|---|
| bm25:name_desc_server | 0.597 ± 0.007 | 0.537 ± 0.018 | 0.473 ± 0.021 | 0.412 ± 0.000 |
| emb:text-embedding-3-small:name_desc_server | 0.782 ± 0.023 | 0.705 ± 0.006 | 0.608 ± 0.012 | 0.517 ± 0.000 |

## full_coverage@5 by pool size

| System | 50 | 100 | 250 | 527 |
|---|---|---|---|---|
| bm25:name_desc_server | 0.420 ± 0.018 | 0.353 ± 0.014 | 0.317 ± 0.017 | 0.250 ± 0.000 |
| emb:text-embedding-3-small:name_desc_server | 0.600 ± 0.049 | 0.500 ± 0.012 | 0.377 ± 0.015 | 0.283 ± 0.000 |

## mrr by pool size

| System | 50 | 100 | 250 | 527 |
|---|---|---|---|---|
| bm25:name_desc_server | 0.674 ± 0.023 | 0.630 ± 0.024 | 0.529 ± 0.012 | 0.428 ± 0.000 |
| emb:text-embedding-3-small:name_desc_server | 0.865 ± 0.014 | 0.804 ± 0.015 | 0.687 ± 0.026 | 0.589 ± 0.000 |

## slot_recall@5 by challenge bucket and pool size

Mean over queries and seeds. n is the number of queries in the bucket.

| System | Bucket | n | 50 | 100 | 250 | 527 |
|---|---|---|---|---|---|---|
| bm25:name_desc_server | semantic_distance | 12 | 0.246 | 0.217 | 0.208 | 0.208 |
| bm25:name_desc_server | taxonomy_collision | 10 | 0.530 | 0.505 | 0.470 | 0.450 |
| bm25:name_desc_server | multi_capability | 15 | 0.569 | 0.444 | 0.274 | 0.211 |
| bm25:name_desc_server | near_duplicate | 9 | 0.889 | 0.815 | 0.730 | 0.519 |
| bm25:name_desc_server | ambiguity | 10 | 0.707 | 0.655 | 0.652 | 0.592 |
| bm25:name_desc_server | none | 4 | 1.000 | 1.000 | 1.000 | 1.000 |
| emb:text-embedding-3-small:name_desc_server | semantic_distance | 12 | 0.705 | 0.608 | 0.542 | 0.500 |
| emb:text-embedding-3-small:name_desc_server | taxonomy_collision | 10 | 0.890 | 0.825 | 0.725 | 0.575 |
| emb:text-embedding-3-small:name_desc_server | multi_capability | 15 | 0.688 | 0.599 | 0.479 | 0.383 |
| emb:text-embedding-3-small:name_desc_server | near_duplicate | 9 | 0.848 | 0.770 | 0.674 | 0.500 |
| emb:text-embedding-3-small:name_desc_server | ambiguity | 10 | 0.818 | 0.765 | 0.648 | 0.600 |
| emb:text-embedding-3-small:name_desc_server | none | 4 | 0.850 | 0.800 | 0.750 | 0.750 |
