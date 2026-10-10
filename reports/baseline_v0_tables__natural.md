# Baseline v0 tables

Scores are deterministic. Challenge bucket and task family are eval annotations. n=94 queries, so intervals are wide.

## 1. Overall (all 94 queries)
Cells are mean [95% bootstrap CI]. Latency p50 and p95 are point values.

| Metric | bm25:name_desc_server | emb:text-embedding-3-small:name_desc_server | full_catalog:gpt-6-luna |
|---|---|---|---|
| slot_recall@1 | 0.155 [0.106, 0.207] | 0.182 [0.130, 0.237] | 0.274 [0.216, 0.337] |
| slot_recall@5 | 0.361 [0.288, 0.437] | 0.446 [0.372, 0.521] | 0.596 [0.517, 0.677] |
| slot_recall@10 | 0.442 [0.369, 0.518] | 0.568 [0.497, 0.641] | 0.634 [0.551, 0.715] |
| full_coverage@5 | 0.181 [0.106, 0.255] | 0.223 [0.138, 0.309] | 0.404 [0.309, 0.500] |
| precision@5 | 0.166 [0.134, 0.200] | 0.204 [0.170, 0.240] | 0.551 [0.473, 0.630] |
| r_precision | 0.231 [0.171, 0.293] | 0.293 [0.230, 0.357] | 0.544 [0.461, 0.628] |
| mrr | 0.454 [0.370, 0.542] | 0.534 [0.451, 0.618] | 0.650 [0.566, 0.736] |
| confusion@5 | n/a | n/a | n/a |
| confuser_first@5 | n/a | n/a | n/a |
| unjudged@5 | 0.834 [0.800, 0.866] | 0.796 [0.760, 0.830] | 0.449 [0.370, 0.527] |
| tokens@5 | 1166.149 [1015.462, 1333.043] | 1088.745 [911.159, 1285.778] | 582.319 [480.550, 701.566] |
| latency_ms | 0.399 [0.312, 0.536] | 168.452 [127.930, 214.928] | 4073.033 [3776.159, 4383.076] |
| latency p50 (ms) | 0.279 | 125.847 | 3854.341 |
| latency p95 (ms) | 0.763 | 387.355 | 6838.862 |

## 2. Per challenge bucket (mean over queries)

| Bucket | System | n | slot_recall@5 | full_coverage@5 | r_precision | confusion@5 |
|---|---|---|---|---|---|---|
| natural | bm25:name_desc_server | 94 | 0.361 | 0.181 | 0.231 | n/a |
| natural | emb:text-embedding-3-small:name_desc_server | 94 | 0.446 | 0.223 | 0.293 | n/a |
| natural | full_catalog:gpt-6-luna | 94 | 0.596 | 0.404 | 0.544 | n/a |

## 3. Per task family (mean over queries)

| Family | System | n | slot_recall@5 |
|---|---|---|---|
| Finance | bm25:name_desc_server | 14 | 0.310 |
| Finance | emb:text-embedding-3-small:name_desc_server | 14 | 0.327 |
| Finance | full_catalog:gpt-6-luna | 14 | 0.395 |
| Leisure | bm25:name_desc_server | 14 | 0.446 |
| Leisure | emb:text-embedding-3-small:name_desc_server | 14 | 0.679 |
| Leisure | full_catalog:gpt-6-luna | 14 | 0.696 |
| Lifestyle | bm25:name_desc_server | 15 | 0.339 |
| Lifestyle | emb:text-embedding-3-small:name_desc_server | 15 | 0.489 |
| Lifestyle | full_catalog:gpt-6-luna | 15 | 0.667 |
| Office | bm25:name_desc_server | 30 | 0.422 |
| Office | emb:text-embedding-3-small:name_desc_server | 30 | 0.403 |
| Office | full_catalog:gpt-6-luna | 30 | 0.592 |
| Shopping | bm25:name_desc_server | 9 | 0.167 |
| Shopping | emb:text-embedding-3-small:name_desc_server | 9 | 0.389 |
| Shopping | full_catalog:gpt-6-luna | 9 | 0.444 |
| Travel | bm25:name_desc_server | 12 | 0.338 |
| Travel | emb:text-embedding-3-small:name_desc_server | 12 | 0.408 |
| Travel | full_catalog:gpt-6-luna | 12 | 0.751 |

## 4. Per split (mean over queries)

| Split | System | n | slot_recall@5 | full_coverage@5 |
|---|---|---|---|---|
| test | bm25:name_desc_server | 94 | 0.361 | 0.181 |
| test | emb:text-embedding-3-small:name_desc_server | 94 | 0.446 | 0.223 |
| test | full_catalog:gpt-6-luna | 94 | 0.596 | 0.404 |

## 5. Paired comparisons (A minus B, same queries)

### bm25:name_desc_server - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.085 | [-0.168, -0.004] | 15 | 25 | 54 | 94 |
| full_coverage@5 | -0.043 | [-0.117, 0.032] | 5 | 9 | 80 | 94 |
| r_precision | -0.062 | [-0.132, 0.008] | 15 | 26 | 53 | 94 |
| mrr | -0.080 | [-0.168, 0.007] | 22 | 36 | 36 | 94 |

### bm25:name_desc_server - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.236 | [-0.335, -0.134] | 14 | 54 | 26 | 94 |
| full_coverage@5 | -0.223 | [-0.330, -0.117] | 6 | 27 | 61 | 94 |
| r_precision | -0.313 | [-0.404, -0.224] | 10 | 51 | 33 | 94 |
| mrr | -0.196 | [-0.304, -0.089] | 18 | 43 | 33 | 94 |

### emb:text-embedding-3-small:name_desc_server - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.085 | [0.004, 0.168] | 25 | 15 | 54 | 94 |
| full_coverage@5 | 0.043 | [-0.032, 0.117] | 9 | 5 | 80 | 94 |
| r_precision | 0.062 | [-0.008, 0.132] | 26 | 15 | 53 | 94 |
| mrr | 0.080 | [-0.007, 0.168] | 36 | 22 | 36 | 94 |

### emb:text-embedding-3-small:name_desc_server - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.151 | [-0.240, -0.061] | 15 | 44 | 35 | 94 |
| full_coverage@5 | -0.181 | [-0.287, -0.085] | 5 | 22 | 67 | 94 |
| r_precision | -0.251 | [-0.336, -0.165] | 11 | 48 | 35 | 94 |
| mrr | -0.116 | [-0.215, -0.018] | 22 | 38 | 34 | 94 |

### full_catalog:gpt-6-luna - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.236 | [0.134, 0.335] | 54 | 14 | 26 | 94 |
| full_coverage@5 | 0.223 | [0.117, 0.330] | 27 | 6 | 61 | 94 |
| r_precision | 0.313 | [0.224, 0.404] | 51 | 10 | 33 | 94 |
| mrr | 0.196 | [0.089, 0.304] | 43 | 18 | 33 | 94 |

### full_catalog:gpt-6-luna - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.151 | [0.061, 0.240] | 44 | 15 | 35 | 94 |
| full_coverage@5 | 0.181 | [0.085, 0.287] | 22 | 5 | 67 | 94 |
| r_precision | 0.251 | [0.165, 0.336] | 48 | 11 | 35 | 94 |
| mrr | 0.116 | [0.018, 0.215] | 38 | 22 | 34 | 94 |
