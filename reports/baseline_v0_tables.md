# Baseline v0 tables

Scores are deterministic. Challenge bucket and task family are eval annotations. n=60 queries, so intervals are wide.

## 1. Overall (all 60 queries)
Cells are mean [95% bootstrap CI]. Latency p50 and p95 are point values.

| Metric | bm25:name_desc_server | emb:text-embedding-3-small:name_desc_server |
|---|---|---|
| slot_recall@1 | 0.172 [0.099, 0.254] | 0.242 [0.161, 0.328] |
| slot_recall@5 | 0.412 [0.312, 0.512] | 0.517 [0.425, 0.608] |
| slot_recall@10 | 0.467 [0.368, 0.568] | 0.625 [0.535, 0.714] |
| full_coverage@5 | 0.250 [0.150, 0.367] | 0.283 [0.167, 0.400] |
| precision@5 | 0.177 [0.137, 0.217] | 0.253 [0.207, 0.303] |
| r_precision | 0.221 [0.146, 0.301] | 0.374 [0.283, 0.467] |
| mrr | 0.428 [0.326, 0.533] | 0.589 [0.491, 0.685] |
| confusion@5 | 0.237 [0.136, 0.339] | 0.288 [0.169, 0.407] |
| confuser_first@5 | 0.186 [0.102, 0.288] | 0.153 [0.068, 0.254] |
| unjudged@5 | 0.733 [0.677, 0.790] | 0.623 [0.557, 0.690] |
| tokens@5 | 1153.383 [978.464, 1355.054] | 1028.367 [817.961, 1277.101] |
| latency_ms | 0.416 [0.285, 0.626] | 0.187 [0.179, 0.198] |
| latency p50 (ms) | 0.239 | 0.176 |
| latency p95 (ms) | 0.910 | 0.229 |

## 2. Per challenge bucket (mean over queries)

| Bucket | System | n | slot_recall@5 | full_coverage@5 | r_precision | confusion@5 |
|---|---|---|---|---|---|---|
| ambiguity | bm25:name_desc_server | 10 | 0.592 | 0.400 | 0.408 | 0.300 |
| ambiguity | emb:text-embedding-3-small:name_desc_server | 10 | 0.600 | 0.400 | 0.533 | 0.300 |
| multi_capability | bm25:name_desc_server | 15 | 0.211 | 0.000 | 0.194 | 0.333 |
| multi_capability | emb:text-embedding-3-small:name_desc_server | 15 | 0.383 | 0.067 | 0.222 | 0.267 |
| near_duplicate | bm25:name_desc_server | 9 | 0.519 | 0.222 | 0.333 | 0.125 |
| near_duplicate | emb:text-embedding-3-small:name_desc_server | 9 | 0.500 | 0.222 | 0.333 | 0.375 |
| none | bm25:name_desc_server | 4 | 1.000 | 1.000 | 0.000 | 0.000 |
| none | emb:text-embedding-3-small:name_desc_server | 4 | 0.750 | 0.750 | 0.250 | 0.000 |
| semantic_distance | bm25:name_desc_server | 12 | 0.208 | 0.167 | 0.083 | 0.167 |
| semantic_distance | emb:text-embedding-3-small:name_desc_server | 12 | 0.500 | 0.333 | 0.458 | 0.167 |
| taxonomy_collision | bm25:name_desc_server | 10 | 0.450 | 0.300 | 0.225 | 0.300 |
| taxonomy_collision | emb:text-embedding-3-small:name_desc_server | 10 | 0.575 | 0.300 | 0.425 | 0.500 |

## 3. Per task family (mean over queries)

| Family | System | n | slot_recall@5 |
|---|---|---|---|
| academic_search | bm25:name_desc_server | 7 | 0.357 |
| academic_search | emb:text-embedding-3-small:name_desc_server | 7 | 0.524 |
| developer_tools | bm25:name_desc_server | 2 | 0.500 |
| developer_tools | emb:text-embedding-3-small:name_desc_server | 2 | 1.000 |
| document_authoring | bm25:name_desc_server | 4 | 0.208 |
| document_authoring | emb:text-embedding-3-small:name_desc_server | 4 | 0.271 |
| file_conversion | bm25:name_desc_server | 2 | 0.000 |
| file_conversion | emb:text-embedding-3-small:name_desc_server | 2 | 0.000 |
| finance_analysis | bm25:name_desc_server | 6 | 0.333 |
| finance_analysis | emb:text-embedding-3-small:name_desc_server | 6 | 0.403 |
| gaming | bm25:name_desc_server | 3 | 0.667 |
| gaming | emb:text-embedding-3-small:name_desc_server | 3 | 0.833 |
| geo_location | bm25:name_desc_server | 5 | 0.400 |
| geo_location | emb:text-embedding-3-small:name_desc_server | 5 | 0.500 |
| lifestyle_utilities | bm25:name_desc_server | 5 | 0.800 |
| lifestyle_utilities | emb:text-embedding-3-small:name_desc_server | 5 | 0.900 |
| local_files | bm25:name_desc_server | 7 | 0.738 |
| local_files | emb:text-embedding-3-small:name_desc_server | 7 | 0.643 |
| media_visual_audio | bm25:name_desc_server | 3 | 0.167 |
| media_visual_audio | emb:text-embedding-3-small:name_desc_server | 3 | 0.500 |
| news_and_trends | bm25:name_desc_server | 8 | 0.438 |
| news_and_trends | emb:text-embedding-3-small:name_desc_server | 8 | 0.531 |
| security_network | bm25:name_desc_server | 1 | 0.000 |
| security_network | emb:text-embedding-3-small:name_desc_server | 1 | 0.333 |
| shopping_research | bm25:name_desc_server | 2 | 0.000 |
| shopping_research | emb:text-embedding-3-small:name_desc_server | 2 | 0.000 |
| travel_planning | bm25:name_desc_server | 3 | 0.250 |
| travel_planning | emb:text-embedding-3-small:name_desc_server | 3 | 0.417 |
| web_research_writing | bm25:name_desc_server | 2 | 0.250 |
| web_research_writing | emb:text-embedding-3-small:name_desc_server | 2 | 0.250 |

## 4. Per split (mean over queries)

| Split | System | n | slot_recall@5 | full_coverage@5 |
|---|---|---|---|---|
| dev | bm25:name_desc_server | 18 | 0.435 | 0.333 |
| dev | emb:text-embedding-3-small:name_desc_server | 18 | 0.574 | 0.333 |
| test | bm25:name_desc_server | 42 | 0.403 | 0.214 |
| test | emb:text-embedding-3-small:name_desc_server | 42 | 0.492 | 0.262 |

## 5. Paired comparisons (A minus B, same queries)

### bm25:name_desc_server - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.104 | [-0.206, -0.007] | 5 | 16 | 39 | 60 |
| full_coverage@5 | -0.033 | [-0.133, 0.050] | 3 | 5 | 52 | 60 |
| r_precision | -0.153 | [-0.263, -0.044] | 8 | 22 | 30 | 60 |
| mrr | -0.161 | [-0.271, -0.053] | 10 | 28 | 22 | 60 |

### emb:text-embedding-3-small:name_desc_server - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.104 | [0.007, 0.206] | 16 | 5 | 39 | 60 |
| full_coverage@5 | 0.033 | [-0.050, 0.133] | 5 | 3 | 52 | 60 |
| r_precision | 0.153 | [0.044, 0.263] | 22 | 8 | 30 | 60 |
| mrr | 0.161 | [0.053, 0.271] | 28 | 10 | 22 | 60 |
