# Baseline v0 tables

Scores are deterministic. Challenge bucket and task family are eval annotations. n=60 queries, so intervals are wide.

## 1. Overall (all 60 queries)
Cells are mean [95% bootstrap CI]. Latency p50 and p95 are point values.

| Metric | bm25:name_desc_server | emb:text-embedding-3-small:name_desc_server | full_catalog:gpt-6-luna | full_catalog:gpt-6-luna:run2 |
|---|---|---|---|---|
| slot_recall@1 | 0.172 [0.099, 0.254] | 0.242 [0.161, 0.328] | 0.348 [0.264, 0.435] | 0.328 [0.239, 0.421] |
| slot_recall@5 | 0.412 [0.312, 0.512] | 0.517 [0.425, 0.608] | 0.599 [0.498, 0.694] | 0.637 [0.534, 0.734] |
| slot_recall@10 | 0.467 [0.368, 0.568] | 0.625 [0.535, 0.714] | 0.634 [0.532, 0.731] | 0.662 [0.557, 0.760] |
| full_coverage@5 | 0.250 [0.150, 0.367] | 0.283 [0.167, 0.400] | 0.400 [0.283, 0.517] | 0.467 [0.333, 0.600] |
| precision@5 | 0.177 [0.137, 0.217] | 0.253 [0.207, 0.303] | 0.618 [0.516, 0.714] | 0.610 [0.514, 0.705] |
| r_precision | 0.221 [0.146, 0.301] | 0.374 [0.283, 0.467] | 0.638 [0.533, 0.737] | 0.614 [0.510, 0.715] |
| mrr | 0.428 [0.326, 0.533] | 0.589 [0.491, 0.685] | 0.701 [0.592, 0.801] | 0.678 [0.574, 0.778] |
| confusion@5 | 0.237 [0.136, 0.339] | 0.288 [0.169, 0.407] | 0.136 [0.051, 0.220] | 0.102 [0.034, 0.186] |
| confuser_first@5 | 0.186 [0.102, 0.288] | 0.153 [0.068, 0.254] | 0.068 [0.017, 0.136] | 0.068 [0.017, 0.136] |
| unjudged@5 | 0.733 [0.677, 0.790] | 0.623 [0.557, 0.690] | 0.331 [0.241, 0.426] | 0.328 [0.239, 0.420] |
| tokens@5 | 1153.383 [978.464, 1355.054] | 1028.367 [817.961, 1277.101] | 575.966 [434.964, 752.063] | 569.390 [414.553, 772.289] |
| latency_ms | 0.416 [0.285, 0.626] | 0.187 [0.179, 0.198] | 4488.554 [4083.077, 4892.737] | 4457.276 [3996.070, 4962.172] |
| latency p50 (ms) | 0.239 | 0.176 | 4262.340 | 4113.480 |
| latency p95 (ms) | 0.910 | 0.229 | 7349.983 | 8166.312 |

## 2. Per challenge bucket (mean over queries)

| Bucket | System | n | slot_recall@5 | full_coverage@5 | r_precision | confusion@5 |
|---|---|---|---|---|---|---|
| ambiguity | bm25:name_desc_server | 10 | 0.592 | 0.400 | 0.408 | 0.300 |
| ambiguity | emb:text-embedding-3-small:name_desc_server | 10 | 0.600 | 0.400 | 0.533 | 0.300 |
| ambiguity | full_catalog:gpt-6-luna | 10 | 0.225 | 0.000 | 0.500 | 0.300 |
| ambiguity | full_catalog:gpt-6-luna:run2 | 10 | 0.475 | 0.300 | 0.528 | 0.300 |
| multi_capability | bm25:name_desc_server | 15 | 0.211 | 0.000 | 0.194 | 0.333 |
| multi_capability | emb:text-embedding-3-small:name_desc_server | 15 | 0.383 | 0.067 | 0.222 | 0.267 |
| multi_capability | full_catalog:gpt-6-luna | 15 | 0.572 | 0.267 | 0.478 | 0.200 |
| multi_capability | full_catalog:gpt-6-luna:run2 | 15 | 0.633 | 0.333 | 0.530 | 0.067 |
| near_duplicate | bm25:name_desc_server | 9 | 0.519 | 0.222 | 0.333 | 0.125 |
| near_duplicate | emb:text-embedding-3-small:name_desc_server | 9 | 0.500 | 0.222 | 0.333 | 0.375 |
| near_duplicate | full_catalog:gpt-6-luna | 9 | 0.685 | 0.444 | 0.685 | 0.000 |
| near_duplicate | full_catalog:gpt-6-luna:run2 | 9 | 0.722 | 0.556 | 0.722 | 0.000 |
| none | bm25:name_desc_server | 4 | 1.000 | 1.000 | 0.000 | 0.000 |
| none | emb:text-embedding-3-small:name_desc_server | 4 | 0.750 | 0.750 | 0.250 | 0.000 |
| none | full_catalog:gpt-6-luna | 4 | 1.000 | 1.000 | 1.000 | 0.000 |
| none | full_catalog:gpt-6-luna:run2 | 4 | 0.750 | 0.750 | 0.750 | 0.000 |
| semantic_distance | bm25:name_desc_server | 12 | 0.208 | 0.167 | 0.083 | 0.167 |
| semantic_distance | emb:text-embedding-3-small:name_desc_server | 12 | 0.500 | 0.333 | 0.458 | 0.167 |
| semantic_distance | full_catalog:gpt-6-luna | 12 | 0.662 | 0.500 | 0.792 | 0.167 |
| semantic_distance | full_catalog:gpt-6-luna:run2 | 12 | 0.579 | 0.417 | 0.625 | 0.167 |
| taxonomy_collision | bm25:name_desc_server | 10 | 0.450 | 0.300 | 0.225 | 0.300 |
| taxonomy_collision | emb:text-embedding-3-small:name_desc_server | 10 | 0.575 | 0.300 | 0.425 | 0.500 |
| taxonomy_collision | full_catalog:gpt-6-luna | 10 | 0.700 | 0.600 | 0.617 | 0.000 |
| taxonomy_collision | full_catalog:gpt-6-luna:run2 | 10 | 0.750 | 0.700 | 0.650 | 0.000 |

## 3. Per task family (mean over queries)

| Family | System | n | slot_recall@5 |
|---|---|---|---|
| academic_search | bm25:name_desc_server | 7 | 0.357 |
| academic_search | emb:text-embedding-3-small:name_desc_server | 7 | 0.524 |
| academic_search | full_catalog:gpt-6-luna | 7 | 0.595 |
| academic_search | full_catalog:gpt-6-luna:run2 | 7 | 0.690 |
| developer_tools | bm25:name_desc_server | 2 | 0.500 |
| developer_tools | emb:text-embedding-3-small:name_desc_server | 2 | 1.000 |
| developer_tools | full_catalog:gpt-6-luna | 2 | 1.000 |
| developer_tools | full_catalog:gpt-6-luna:run2 | 2 | 1.000 |
| document_authoring | bm25:name_desc_server | 4 | 0.208 |
| document_authoring | emb:text-embedding-3-small:name_desc_server | 4 | 0.271 |
| document_authoring | full_catalog:gpt-6-luna | 4 | 0.250 |
| document_authoring | full_catalog:gpt-6-luna:run2 | 4 | 0.375 |
| file_conversion | bm25:name_desc_server | 2 | 0.000 |
| file_conversion | emb:text-embedding-3-small:name_desc_server | 2 | 0.000 |
| file_conversion | full_catalog:gpt-6-luna | 2 | 1.000 |
| file_conversion | full_catalog:gpt-6-luna:run2 | 2 | 1.000 |
| finance_analysis | bm25:name_desc_server | 6 | 0.333 |
| finance_analysis | emb:text-embedding-3-small:name_desc_server | 6 | 0.403 |
| finance_analysis | full_catalog:gpt-6-luna | 6 | 0.403 |
| finance_analysis | full_catalog:gpt-6-luna:run2 | 6 | 0.486 |
| gaming | bm25:name_desc_server | 3 | 0.667 |
| gaming | emb:text-embedding-3-small:name_desc_server | 3 | 0.833 |
| gaming | full_catalog:gpt-6-luna | 3 | 0.667 |
| gaming | full_catalog:gpt-6-luna:run2 | 3 | 0.667 |
| geo_location | bm25:name_desc_server | 5 | 0.400 |
| geo_location | emb:text-embedding-3-small:name_desc_server | 5 | 0.500 |
| geo_location | full_catalog:gpt-6-luna | 5 | 0.900 |
| geo_location | full_catalog:gpt-6-luna:run2 | 5 | 0.900 |
| lifestyle_utilities | bm25:name_desc_server | 5 | 0.800 |
| lifestyle_utilities | emb:text-embedding-3-small:name_desc_server | 5 | 0.900 |
| lifestyle_utilities | full_catalog:gpt-6-luna | 5 | 0.800 |
| lifestyle_utilities | full_catalog:gpt-6-luna:run2 | 5 | 0.600 |
| local_files | bm25:name_desc_server | 7 | 0.738 |
| local_files | emb:text-embedding-3-small:name_desc_server | 7 | 0.643 |
| local_files | full_catalog:gpt-6-luna | 7 | 0.452 |
| local_files | full_catalog:gpt-6-luna:run2 | 7 | 0.643 |
| media_visual_audio | bm25:name_desc_server | 3 | 0.167 |
| media_visual_audio | emb:text-embedding-3-small:name_desc_server | 3 | 0.500 |
| media_visual_audio | full_catalog:gpt-6-luna | 3 | 0.833 |
| media_visual_audio | full_catalog:gpt-6-luna:run2 | 3 | 1.000 |
| news_and_trends | bm25:name_desc_server | 8 | 0.438 |
| news_and_trends | emb:text-embedding-3-small:name_desc_server | 8 | 0.531 |
| news_and_trends | full_catalog:gpt-6-luna | 8 | 0.438 |
| news_and_trends | full_catalog:gpt-6-luna:run2 | 8 | 0.500 |
| security_network | bm25:name_desc_server | 1 | 0.000 |
| security_network | emb:text-embedding-3-small:name_desc_server | 1 | 0.333 |
| security_network | full_catalog:gpt-6-luna | 1 | 0.333 |
| security_network | full_catalog:gpt-6-luna:run2 | 1 | 0.333 |
| shopping_research | bm25:name_desc_server | 2 | 0.000 |
| shopping_research | emb:text-embedding-3-small:name_desc_server | 2 | 0.000 |
| shopping_research | full_catalog:gpt-6-luna | 2 | 0.100 |
| shopping_research | full_catalog:gpt-6-luna:run2 | 2 | 0.100 |
| travel_planning | bm25:name_desc_server | 3 | 0.250 |
| travel_planning | emb:text-embedding-3-small:name_desc_server | 3 | 0.417 |
| travel_planning | full_catalog:gpt-6-luna | 3 | 0.833 |
| travel_planning | full_catalog:gpt-6-luna:run2 | 3 | 0.583 |
| web_research_writing | bm25:name_desc_server | 2 | 0.250 |
| web_research_writing | emb:text-embedding-3-small:name_desc_server | 2 | 0.250 |
| web_research_writing | full_catalog:gpt-6-luna | 2 | 0.833 |
| web_research_writing | full_catalog:gpt-6-luna:run2 | 2 | 0.833 |

## 4. Per split (mean over queries)

| Split | System | n | slot_recall@5 | full_coverage@5 |
|---|---|---|---|---|
| dev | bm25:name_desc_server | 18 | 0.435 | 0.333 |
| dev | emb:text-embedding-3-small:name_desc_server | 18 | 0.574 | 0.333 |
| dev | full_catalog:gpt-6-luna | 18 | 0.622 | 0.389 |
| dev | full_catalog:gpt-6-luna:run2 | 18 | 0.719 | 0.556 |
| test | bm25:name_desc_server | 42 | 0.403 | 0.214 |
| test | emb:text-embedding-3-small:name_desc_server | 42 | 0.492 | 0.262 |
| test | full_catalog:gpt-6-luna | 42 | 0.589 | 0.405 |
| test | full_catalog:gpt-6-luna:run2 | 42 | 0.601 | 0.429 |

## 5. Paired comparisons (A minus B, same queries)

### bm25:name_desc_server - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.104 | [-0.206, -0.007] | 5 | 16 | 39 | 60 |
| full_coverage@5 | -0.033 | [-0.133, 0.050] | 3 | 5 | 52 | 60 |
| r_precision | -0.153 | [-0.263, -0.044] | 8 | 22 | 30 | 60 |
| mrr | -0.161 | [-0.271, -0.053] | 10 | 28 | 22 | 60 |

### bm25:name_desc_server - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.187 | [-0.321, -0.044] | 9 | 31 | 20 | 60 |
| full_coverage@5 | -0.150 | [-0.300, 0.000] | 6 | 15 | 39 | 60 |
| r_precision | -0.427 | [-0.550, -0.297] | 6 | 40 | 12 | 58 |
| mrr | -0.273 | [-0.421, -0.115] | 11 | 34 | 15 | 60 |

### bm25:name_desc_server - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.224 | [-0.354, -0.089] | 7 | 31 | 22 | 60 |
| full_coverage@5 | -0.217 | [-0.367, -0.067] | 5 | 18 | 37 | 60 |
| r_precision | -0.406 | [-0.530, -0.284] | 6 | 37 | 16 | 59 |
| mrr | -0.251 | [-0.396, -0.103] | 13 | 33 | 14 | 60 |

### emb:text-embedding-3-small:name_desc_server - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.104 | [0.007, 0.206] | 16 | 5 | 39 | 60 |
| full_coverage@5 | 0.033 | [-0.050, 0.133] | 5 | 3 | 52 | 60 |
| r_precision | 0.153 | [0.044, 0.263] | 22 | 8 | 30 | 60 |
| mrr | 0.161 | [0.053, 0.271] | 28 | 10 | 22 | 60 |

### emb:text-embedding-3-small:name_desc_server - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.083 | [-0.203, 0.045] | 11 | 25 | 24 | 60 |
| full_coverage@5 | -0.117 | [-0.250, 0.017] | 6 | 13 | 41 | 60 |
| r_precision | -0.269 | [-0.395, -0.141] | 7 | 32 | 19 | 58 |
| mrr | -0.112 | [-0.250, 0.032] | 14 | 24 | 22 | 60 |

### emb:text-embedding-3-small:name_desc_server - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.120 | [-0.232, -0.005] | 8 | 24 | 28 | 60 |
| full_coverage@5 | -0.183 | [-0.317, -0.050] | 4 | 15 | 41 | 60 |
| r_precision | -0.251 | [-0.373, -0.125] | 8 | 31 | 20 | 59 |
| mrr | -0.090 | [-0.220, 0.042] | 14 | 23 | 23 | 60 |

### full_catalog:gpt-6-luna - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.187 | [0.044, 0.321] | 31 | 9 | 20 | 60 |
| full_coverage@5 | 0.150 | [0.000, 0.300] | 15 | 6 | 39 | 60 |
| r_precision | 0.427 | [0.297, 0.550] | 40 | 6 | 12 | 58 |
| mrr | 0.273 | [0.115, 0.421] | 34 | 11 | 15 | 60 |

### full_catalog:gpt-6-luna - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.083 | [-0.045, 0.203] | 25 | 11 | 24 | 60 |
| full_coverage@5 | 0.117 | [-0.017, 0.250] | 13 | 6 | 41 | 60 |
| r_precision | 0.269 | [0.141, 0.395] | 32 | 7 | 19 | 58 |
| mrr | 0.112 | [-0.032, 0.250] | 24 | 14 | 22 | 60 |

### full_catalog:gpt-6-luna - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.037 | [-0.114, 0.039] | 4 | 10 | 46 | 60 |
| full_coverage@5 | -0.067 | [-0.167, 0.033] | 3 | 7 | 50 | 60 |
| r_precision | 0.049 | [-0.016, 0.124] | 8 | 7 | 42 | 57 |
| mrr | 0.022 | [-0.060, 0.103] | 8 | 8 | 44 | 60 |

### full_catalog:gpt-6-luna:run2 - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.224 | [0.089, 0.354] | 31 | 7 | 22 | 60 |
| full_coverage@5 | 0.217 | [0.067, 0.367] | 18 | 5 | 37 | 60 |
| r_precision | 0.406 | [0.284, 0.530] | 37 | 6 | 16 | 59 |
| mrr | 0.251 | [0.103, 0.396] | 33 | 13 | 14 | 60 |

### full_catalog:gpt-6-luna:run2 - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.120 | [0.005, 0.232] | 24 | 8 | 28 | 60 |
| full_coverage@5 | 0.183 | [0.050, 0.317] | 15 | 4 | 41 | 60 |
| r_precision | 0.251 | [0.125, 0.373] | 31 | 8 | 20 | 59 |
| mrr | 0.090 | [-0.042, 0.220] | 23 | 14 | 23 | 60 |

### full_catalog:gpt-6-luna:run2 - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.037 | [-0.039, 0.114] | 10 | 4 | 46 | 60 |
| full_coverage@5 | 0.067 | [-0.033, 0.167] | 7 | 3 | 50 | 60 |
| r_precision | -0.049 | [-0.124, 0.016] | 7 | 8 | 42 | 57 |
| mrr | -0.022 | [-0.103, 0.060] | 8 | 8 | 44 | 60 |
