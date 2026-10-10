# Baseline v0 tables

Scores are deterministic. Challenge bucket and task family are eval annotations. n=60 queries, so intervals are wide.

## 1. Overall (all 60 queries)
Cells are mean [95% bootstrap CI]. Latency p50 and p95 are point values.

| Metric | bm25:enriched_raw_tag | bm25:enriched_tag | bm25:name_desc_server | emb:text-embedding-3-small:enriched_raw_tag | emb:text-embedding-3-small:enriched_tag | emb:text-embedding-3-small:enriched_tag_topic | emb:text-embedding-3-small:name_desc_server | emb_rerank:gpt-6-luna:raw:n20 | full_catalog:gpt-6-luna | full_catalog:gpt-6-luna:run2 | full_catalog_cards:gpt-6-luna | full_catalog_cards:gpt-6-luna:run2 | router:domain | router:server |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| slot_recall@1 | 0.189 [0.117, 0.267] | 0.203 [0.126, 0.285] | 0.172 [0.099, 0.254] | 0.319 [0.228, 0.414] | 0.354 [0.258, 0.450] | 0.335 [0.240, 0.429] | 0.242 [0.161, 0.328] | 0.351 [0.264, 0.442] | 0.348 [0.264, 0.435] | 0.328 [0.239, 0.421] | 0.371 [0.287, 0.459] | 0.381 [0.293, 0.472] | 0.349 [0.265, 0.436] | 0.324 [0.241, 0.414] |
| slot_recall@5 | 0.453 [0.351, 0.554] | 0.414 [0.318, 0.512] | 0.412 [0.312, 0.512] | 0.524 [0.429, 0.619] | 0.529 [0.436, 0.625] | 0.526 [0.435, 0.619] | 0.517 [0.425, 0.608] | 0.543 [0.446, 0.640] | 0.599 [0.498, 0.694] | 0.637 [0.534, 0.734] | 0.635 [0.537, 0.728] | 0.657 [0.562, 0.747] | 0.649 [0.560, 0.736] | 0.638 [0.548, 0.728] |
| slot_recall@10 | 0.539 [0.440, 0.639] | 0.511 [0.408, 0.614] | 0.467 [0.368, 0.568] | 0.637 [0.544, 0.729] | 0.632 [0.539, 0.724] | 0.642 [0.551, 0.732] | 0.625 [0.535, 0.714] | 0.547 [0.449, 0.644] | 0.634 [0.532, 0.731] | 0.662 [0.557, 0.760] | 0.689 [0.594, 0.781] | 0.691 [0.594, 0.779] | 0.681 [0.593, 0.765] | 0.671 [0.577, 0.764] |
| full_coverage@5 | 0.283 [0.167, 0.400] | 0.233 [0.133, 0.350] | 0.250 [0.150, 0.367] | 0.317 [0.200, 0.433] | 0.317 [0.200, 0.433] | 0.300 [0.183, 0.417] | 0.283 [0.167, 0.400] | 0.350 [0.233, 0.467] | 0.400 [0.283, 0.517] | 0.467 [0.333, 0.600] | 0.450 [0.317, 0.583] | 0.433 [0.300, 0.567] | 0.417 [0.300, 0.550] | 0.400 [0.283, 0.533] |
| precision@5 | 0.203 [0.157, 0.253] | 0.193 [0.150, 0.240] | 0.177 [0.137, 0.217] | 0.247 [0.203, 0.293] | 0.257 [0.210, 0.303] | 0.260 [0.217, 0.307] | 0.253 [0.207, 0.303] | 0.622 [0.524, 0.718] | 0.618 [0.516, 0.714] | 0.610 [0.514, 0.705] | 0.645 [0.550, 0.738] | 0.656 [0.562, 0.746] | 0.590 [0.505, 0.675] | 0.594 [0.507, 0.680] |
| r_precision | 0.268 [0.188, 0.354] | 0.286 [0.200, 0.376] | 0.221 [0.146, 0.301] | 0.431 [0.335, 0.528] | 0.457 [0.361, 0.551] | 0.451 [0.357, 0.546] | 0.374 [0.283, 0.467] | 0.644 [0.543, 0.741] | 0.638 [0.533, 0.737] | 0.614 [0.510, 0.715] | 0.651 [0.551, 0.745] | 0.664 [0.564, 0.758] | 0.600 [0.501, 0.694] | 0.612 [0.518, 0.703] |
| mrr | 0.488 [0.383, 0.592] | 0.475 [0.365, 0.585] | 0.428 [0.326, 0.533] | 0.634 [0.528, 0.737] | 0.666 [0.561, 0.766] | 0.663 [0.561, 0.761] | 0.589 [0.491, 0.685] | 0.703 [0.597, 0.806] | 0.701 [0.592, 0.801] | 0.678 [0.574, 0.778] | 0.758 [0.658, 0.849] | 0.758 [0.657, 0.849] | 0.751 [0.657, 0.839] | 0.713 [0.614, 0.806] |
| confusion@5 | 0.169 [0.085, 0.271] | 0.203 [0.102, 0.305] | 0.237 [0.136, 0.339] | 0.305 [0.186, 0.424] | 0.305 [0.186, 0.424] | 0.373 [0.254, 0.492] | 0.288 [0.169, 0.407] | 0.102 [0.034, 0.186] | 0.136 [0.051, 0.220] | 0.102 [0.034, 0.186] | 0.085 [0.017, 0.169] | 0.119 [0.051, 0.203] | 0.169 [0.085, 0.271] | 0.119 [0.051, 0.203] |
| confuser_first@5 | 0.085 [0.017, 0.169] | 0.085 [0.017, 0.169] | 0.186 [0.102, 0.288] | 0.119 [0.051, 0.203] | 0.102 [0.034, 0.186] | 0.153 [0.068, 0.254] | 0.153 [0.068, 0.254] | 0.068 [0.017, 0.136] | 0.068 [0.017, 0.136] | 0.068 [0.017, 0.136] | 0.051 [0.000, 0.119] | 0.068 [0.017, 0.136] | 0.051 [0.000, 0.119] | 0.068 [0.017, 0.136] |
| unjudged@5 | 0.707 [0.637, 0.773] | 0.727 [0.660, 0.790] | 0.733 [0.677, 0.790] | 0.630 [0.563, 0.697] | 0.617 [0.550, 0.680] | 0.600 [0.540, 0.660] | 0.623 [0.557, 0.690] | 0.343 [0.255, 0.436] | 0.331 [0.241, 0.426] | 0.328 [0.239, 0.420] | 0.297 [0.210, 0.392] | 0.291 [0.206, 0.384] | 0.351 [0.271, 0.435] | 0.360 [0.281, 0.443] |
| tokens@5 | 1049.183 [882.165, 1250.006] | 909.183 [778.043, 1053.817] | 1153.383 [978.464, 1355.054] | 1009.933 [810.220, 1250.784] | 958.150 [772.663, 1177.390] | 1020.883 [821.011, 1249.706] | 1028.367 [817.961, 1277.101] | 409.586 [317.634, 518.794] | 575.966 [434.964, 752.063] | 569.390 [414.553, 772.289] | 521.917 [414.810, 641.068] | 540.000 [417.765, 689.283] | 728.850 [592.125, 897.535] | 606.667 [492.115, 731.333] |
| latency_ms | 0.493 [0.350, 0.719] | 0.438 [0.308, 0.636] | 0.416 [0.285, 0.626] | 0.182 [0.179, 0.186] | 0.245 [0.210, 0.294] | 0.199 [0.188, 0.213] | 0.187 [0.179, 0.198] | 3759.515 [3408.732, 4126.769] | 4488.554 [4083.077, 4892.737] | 4457.276 [3996.070, 4962.172] | 3362.240 [3046.885, 3725.300] | 3208.311 [2938.732, 3490.415] | 6621.788 [6028.437, 7276.000] | 5829.184 [5134.031, 6536.023] |
| latency p50 (ms) | 0.321 | 0.287 | 0.239 | 0.177 | 0.203 | 0.181 | 0.176 | 3686.652 | 4262.340 | 4113.480 | 3151.514 | 3031.347 | 6125.044 | 5282.288 |
| latency p95 (ms) | 0.966 | 0.825 | 0.910 | 0.201 | 0.327 | 0.278 | 0.229 | 6341.651 | 7349.983 | 8166.312 | 5791.985 | 5066.935 | 11949.131 | 11342.424 |

## 2. Per challenge bucket (mean over queries)

| Bucket | System | n | slot_recall@5 | full_coverage@5 | r_precision | confusion@5 |
|---|---|---|---|---|---|---|
| ambiguity | bm25:enriched_raw_tag | 10 | 0.492 | 0.300 | 0.417 | 0.200 |
| ambiguity | bm25:enriched_tag | 10 | 0.308 | 0.200 | 0.267 | 0.300 |
| ambiguity | bm25:name_desc_server | 10 | 0.592 | 0.400 | 0.408 | 0.300 |
| ambiguity | emb:text-embedding-3-small:enriched_raw_tag | 10 | 0.625 | 0.400 | 0.533 | 0.300 |
| ambiguity | emb:text-embedding-3-small:enriched_tag | 10 | 0.550 | 0.300 | 0.517 | 0.400 |
| ambiguity | emb:text-embedding-3-small:enriched_tag_topic | 10 | 0.575 | 0.300 | 0.583 | 0.400 |
| ambiguity | emb:text-embedding-3-small:name_desc_server | 10 | 0.600 | 0.400 | 0.533 | 0.300 |
| ambiguity | emb_rerank:gpt-6-luna:raw:n20 | 10 | 0.525 | 0.300 | 0.667 | 0.100 |
| ambiguity | full_catalog:gpt-6-luna | 10 | 0.225 | 0.000 | 0.500 | 0.300 |
| ambiguity | full_catalog:gpt-6-luna:run2 | 10 | 0.475 | 0.300 | 0.528 | 0.300 |
| ambiguity | full_catalog_cards:gpt-6-luna | 10 | 0.508 | 0.300 | 0.700 | 0.100 |
| ambiguity | full_catalog_cards:gpt-6-luna:run2 | 10 | 0.475 | 0.200 | 0.675 | 0.200 |
| ambiguity | router:domain | 10 | 0.667 | 0.300 | 0.733 | 0.400 |
| ambiguity | router:server | 10 | 0.533 | 0.300 | 0.725 | 0.300 |
| multi_capability | bm25:enriched_raw_tag | 15 | 0.261 | 0.067 | 0.244 | 0.067 |
| multi_capability | bm25:enriched_tag | 15 | 0.250 | 0.000 | 0.217 | 0.067 |
| multi_capability | bm25:name_desc_server | 15 | 0.211 | 0.000 | 0.194 | 0.333 |
| multi_capability | emb:text-embedding-3-small:enriched_raw_tag | 15 | 0.333 | 0.067 | 0.256 | 0.333 |
| multi_capability | emb:text-embedding-3-small:enriched_tag | 15 | 0.294 | 0.067 | 0.261 | 0.267 |
| multi_capability | emb:text-embedding-3-small:enriched_tag_topic | 15 | 0.317 | 0.067 | 0.261 | 0.533 |
| multi_capability | emb:text-embedding-3-small:name_desc_server | 15 | 0.383 | 0.067 | 0.222 | 0.267 |
| multi_capability | emb_rerank:gpt-6-luna:raw:n20 | 15 | 0.400 | 0.067 | 0.511 | 0.200 |
| multi_capability | full_catalog:gpt-6-luna | 15 | 0.572 | 0.267 | 0.478 | 0.200 |
| multi_capability | full_catalog:gpt-6-luna:run2 | 15 | 0.633 | 0.333 | 0.530 | 0.067 |
| multi_capability | full_catalog_cards:gpt-6-luna | 15 | 0.606 | 0.267 | 0.569 | 0.067 |
| multi_capability | full_catalog_cards:gpt-6-luna:run2 | 15 | 0.683 | 0.267 | 0.650 | 0.133 |
| multi_capability | router:domain | 15 | 0.572 | 0.267 | 0.550 | 0.200 |
| multi_capability | router:server | 15 | 0.667 | 0.200 | 0.636 | 0.133 |
| near_duplicate | bm25:enriched_raw_tag | 9 | 0.593 | 0.444 | 0.389 | 0.125 |
| near_duplicate | bm25:enriched_tag | 9 | 0.556 | 0.444 | 0.444 | 0.125 |
| near_duplicate | bm25:name_desc_server | 9 | 0.519 | 0.222 | 0.333 | 0.125 |
| near_duplicate | emb:text-embedding-3-small:enriched_raw_tag | 9 | 0.611 | 0.444 | 0.444 | 0.250 |
| near_duplicate | emb:text-embedding-3-small:enriched_tag | 9 | 0.611 | 0.444 | 0.500 | 0.250 |
| near_duplicate | emb:text-embedding-3-small:enriched_tag_topic | 9 | 0.611 | 0.444 | 0.444 | 0.250 |
| near_duplicate | emb:text-embedding-3-small:name_desc_server | 9 | 0.500 | 0.222 | 0.333 | 0.375 |
| near_duplicate | emb_rerank:gpt-6-luna:raw:n20 | 9 | 0.704 | 0.556 | 0.688 | 0.000 |
| near_duplicate | full_catalog:gpt-6-luna | 9 | 0.685 | 0.444 | 0.685 | 0.000 |
| near_duplicate | full_catalog:gpt-6-luna:run2 | 9 | 0.722 | 0.556 | 0.722 | 0.000 |
| near_duplicate | full_catalog_cards:gpt-6-luna | 9 | 0.722 | 0.556 | 0.667 | 0.000 |
| near_duplicate | full_catalog_cards:gpt-6-luna:run2 | 9 | 0.648 | 0.444 | 0.593 | 0.000 |
| near_duplicate | router:domain | 9 | 0.778 | 0.556 | 0.685 | 0.000 |
| near_duplicate | router:server | 9 | 0.778 | 0.667 | 0.630 | 0.000 |
| none | bm25:enriched_raw_tag | 4 | 1.000 | 1.000 | 0.000 | 0.000 |
| none | bm25:enriched_tag | 4 | 0.750 | 0.750 | 0.250 | 0.000 |
| none | bm25:name_desc_server | 4 | 1.000 | 1.000 | 0.000 | 0.000 |
| none | emb:text-embedding-3-small:enriched_raw_tag | 4 | 0.750 | 0.750 | 0.750 | 0.000 |
| none | emb:text-embedding-3-small:enriched_tag | 4 | 0.750 | 0.750 | 0.750 | 0.000 |
| none | emb:text-embedding-3-small:enriched_tag_topic | 4 | 0.750 | 0.750 | 0.750 | 0.000 |
| none | emb:text-embedding-3-small:name_desc_server | 4 | 0.750 | 0.750 | 0.250 | 0.000 |
| none | emb_rerank:gpt-6-luna:raw:n20 | 4 | 0.750 | 0.750 | 0.750 | 0.000 |
| none | full_catalog:gpt-6-luna | 4 | 1.000 | 1.000 | 1.000 | 0.000 |
| none | full_catalog:gpt-6-luna:run2 | 4 | 0.750 | 0.750 | 0.750 | 0.000 |
| none | full_catalog_cards:gpt-6-luna | 4 | 0.750 | 0.750 | 0.750 | 0.000 |
| none | full_catalog_cards:gpt-6-luna:run2 | 4 | 1.000 | 1.000 | 1.000 | 0.000 |
| none | router:domain | 4 | 0.750 | 0.750 | 0.750 | 0.000 |
| none | router:server | 4 | 0.500 | 0.500 | 0.500 | 0.000 |
| semantic_distance | bm25:enriched_raw_tag | 12 | 0.333 | 0.167 | 0.167 | 0.167 |
| semantic_distance | bm25:enriched_tag | 12 | 0.417 | 0.250 | 0.208 | 0.250 |
| semantic_distance | bm25:name_desc_server | 12 | 0.208 | 0.167 | 0.083 | 0.167 |
| semantic_distance | emb:text-embedding-3-small:enriched_raw_tag | 12 | 0.431 | 0.250 | 0.389 | 0.333 |
| semantic_distance | emb:text-embedding-3-small:enriched_tag | 12 | 0.486 | 0.250 | 0.403 | 0.250 |
| semantic_distance | emb:text-embedding-3-small:enriched_tag_topic | 12 | 0.465 | 0.250 | 0.424 | 0.250 |
| semantic_distance | emb:text-embedding-3-small:name_desc_server | 12 | 0.500 | 0.333 | 0.458 | 0.167 |
| semantic_distance | emb_rerank:gpt-6-luna:raw:n20 | 12 | 0.542 | 0.417 | 0.727 | 0.083 |
| semantic_distance | full_catalog:gpt-6-luna | 12 | 0.662 | 0.500 | 0.792 | 0.167 |
| semantic_distance | full_catalog:gpt-6-luna:run2 | 12 | 0.579 | 0.417 | 0.625 | 0.167 |
| semantic_distance | full_catalog_cards:gpt-6-luna | 12 | 0.579 | 0.417 | 0.667 | 0.167 |
| semantic_distance | full_catalog_cards:gpt-6-luna:run2 | 12 | 0.593 | 0.417 | 0.625 | 0.167 |
| semantic_distance | router:domain | 12 | 0.496 | 0.333 | 0.458 | 0.083 |
| semantic_distance | router:server | 12 | 0.454 | 0.250 | 0.479 | 0.083 |
| taxonomy_collision | bm25:enriched_raw_tag | 10 | 0.500 | 0.300 | 0.275 | 0.400 |
| taxonomy_collision | bm25:enriched_tag | 10 | 0.500 | 0.200 | 0.375 | 0.400 |
| taxonomy_collision | bm25:name_desc_server | 10 | 0.450 | 0.300 | 0.225 | 0.300 |
| taxonomy_collision | emb:text-embedding-3-small:enriched_raw_tag | 10 | 0.650 | 0.400 | 0.500 | 0.400 |
| taxonomy_collision | emb:text-embedding-3-small:enriched_tag | 10 | 0.750 | 0.500 | 0.600 | 0.500 |
| taxonomy_collision | emb:text-embedding-3-small:enriched_tag_topic | 10 | 0.700 | 0.400 | 0.525 | 0.500 |
| taxonomy_collision | emb:text-embedding-3-small:name_desc_server | 10 | 0.575 | 0.300 | 0.425 | 0.500 |
| taxonomy_collision | emb_rerank:gpt-6-luna:raw:n20 | 10 | 0.550 | 0.400 | 0.650 | 0.100 |
| taxonomy_collision | full_catalog:gpt-6-luna | 10 | 0.700 | 0.600 | 0.617 | 0.000 |
| taxonomy_collision | full_catalog:gpt-6-luna:run2 | 10 | 0.750 | 0.700 | 0.650 | 0.000 |
| taxonomy_collision | full_catalog_cards:gpt-6-luna | 10 | 0.750 | 0.700 | 0.650 | 0.100 |
| taxonomy_collision | full_catalog_cards:gpt-6-luna:run2 | 10 | 0.750 | 0.700 | 0.650 | 0.100 |
| taxonomy_collision | router:domain | 10 | 0.775 | 0.600 | 0.575 | 0.200 |
| taxonomy_collision | router:server | 10 | 0.850 | 0.700 | 0.650 | 0.100 |

## 3. Per task family (mean over queries)

| Family | System | n | slot_recall@5 |
|---|---|---|---|
| academic_search | bm25:enriched_raw_tag | 7 | 0.405 |
| academic_search | bm25:enriched_tag | 7 | 0.357 |
| academic_search | bm25:name_desc_server | 7 | 0.357 |
| academic_search | emb:text-embedding-3-small:enriched_raw_tag | 7 | 0.524 |
| academic_search | emb:text-embedding-3-small:enriched_tag | 7 | 0.548 |
| academic_search | emb:text-embedding-3-small:enriched_tag_topic | 7 | 0.595 |
| academic_search | emb:text-embedding-3-small:name_desc_server | 7 | 0.524 |
| academic_search | emb_rerank:gpt-6-luna:raw:n20 | 7 | 0.524 |
| academic_search | full_catalog:gpt-6-luna | 7 | 0.595 |
| academic_search | full_catalog:gpt-6-luna:run2 | 7 | 0.690 |
| academic_search | full_catalog_cards:gpt-6-luna | 7 | 0.786 |
| academic_search | full_catalog_cards:gpt-6-luna:run2 | 7 | 0.690 |
| academic_search | router:domain | 7 | 0.738 |
| academic_search | router:server | 7 | 0.810 |
| developer_tools | bm25:enriched_raw_tag | 2 | 1.000 |
| developer_tools | bm25:enriched_tag | 2 | 0.750 |
| developer_tools | bm25:name_desc_server | 2 | 0.500 |
| developer_tools | emb:text-embedding-3-small:enriched_raw_tag | 2 | 1.000 |
| developer_tools | emb:text-embedding-3-small:enriched_tag | 2 | 1.000 |
| developer_tools | emb:text-embedding-3-small:enriched_tag_topic | 2 | 1.000 |
| developer_tools | emb:text-embedding-3-small:name_desc_server | 2 | 1.000 |
| developer_tools | emb_rerank:gpt-6-luna:raw:n20 | 2 | 1.000 |
| developer_tools | full_catalog:gpt-6-luna | 2 | 1.000 |
| developer_tools | full_catalog:gpt-6-luna:run2 | 2 | 1.000 |
| developer_tools | full_catalog_cards:gpt-6-luna | 2 | 1.000 |
| developer_tools | full_catalog_cards:gpt-6-luna:run2 | 2 | 1.000 |
| developer_tools | router:domain | 2 | 1.000 |
| developer_tools | router:server | 2 | 1.000 |
| document_authoring | bm25:enriched_raw_tag | 4 | 0.188 |
| document_authoring | bm25:enriched_tag | 4 | 0.208 |
| document_authoring | bm25:name_desc_server | 4 | 0.208 |
| document_authoring | emb:text-embedding-3-small:enriched_raw_tag | 4 | 0.333 |
| document_authoring | emb:text-embedding-3-small:enriched_tag | 4 | 0.271 |
| document_authoring | emb:text-embedding-3-small:enriched_tag_topic | 4 | 0.333 |
| document_authoring | emb:text-embedding-3-small:name_desc_server | 4 | 0.271 |
| document_authoring | emb_rerank:gpt-6-luna:raw:n20 | 4 | 0.396 |
| document_authoring | full_catalog:gpt-6-luna | 4 | 0.250 |
| document_authoring | full_catalog:gpt-6-luna:run2 | 4 | 0.375 |
| document_authoring | full_catalog_cards:gpt-6-luna | 4 | 0.312 |
| document_authoring | full_catalog_cards:gpt-6-luna:run2 | 4 | 0.375 |
| document_authoring | router:domain | 4 | 0.333 |
| document_authoring | router:server | 4 | 0.562 |
| file_conversion | bm25:enriched_raw_tag | 2 | 0.250 |
| file_conversion | bm25:enriched_tag | 2 | 0.250 |
| file_conversion | bm25:name_desc_server | 2 | 0.000 |
| file_conversion | emb:text-embedding-3-small:enriched_raw_tag | 2 | 0.000 |
| file_conversion | emb:text-embedding-3-small:enriched_tag | 2 | 0.000 |
| file_conversion | emb:text-embedding-3-small:enriched_tag_topic | 2 | 0.000 |
| file_conversion | emb:text-embedding-3-small:name_desc_server | 2 | 0.000 |
| file_conversion | emb_rerank:gpt-6-luna:raw:n20 | 2 | 0.125 |
| file_conversion | full_catalog:gpt-6-luna | 2 | 1.000 |
| file_conversion | full_catalog:gpt-6-luna:run2 | 2 | 1.000 |
| file_conversion | full_catalog_cards:gpt-6-luna | 2 | 0.625 |
| file_conversion | full_catalog_cards:gpt-6-luna:run2 | 2 | 1.000 |
| file_conversion | router:domain | 2 | 1.000 |
| file_conversion | router:server | 2 | 0.750 |
| finance_analysis | bm25:enriched_raw_tag | 6 | 0.208 |
| finance_analysis | bm25:enriched_tag | 6 | 0.250 |
| finance_analysis | bm25:name_desc_server | 6 | 0.333 |
| finance_analysis | emb:text-embedding-3-small:enriched_raw_tag | 6 | 0.361 |
| finance_analysis | emb:text-embedding-3-small:enriched_tag | 6 | 0.444 |
| finance_analysis | emb:text-embedding-3-small:enriched_tag_topic | 6 | 0.444 |
| finance_analysis | emb:text-embedding-3-small:name_desc_server | 6 | 0.403 |
| finance_analysis | emb_rerank:gpt-6-luna:raw:n20 | 6 | 0.694 |
| finance_analysis | full_catalog:gpt-6-luna | 6 | 0.403 |
| finance_analysis | full_catalog:gpt-6-luna:run2 | 6 | 0.486 |
| finance_analysis | full_catalog_cards:gpt-6-luna | 6 | 0.569 |
| finance_analysis | full_catalog_cards:gpt-6-luna:run2 | 6 | 0.611 |
| finance_analysis | router:domain | 6 | 0.764 |
| finance_analysis | router:server | 6 | 0.611 |
| gaming | bm25:enriched_raw_tag | 3 | 0.667 |
| gaming | bm25:enriched_tag | 3 | 0.667 |
| gaming | bm25:name_desc_server | 3 | 0.667 |
| gaming | emb:text-embedding-3-small:enriched_raw_tag | 3 | 0.833 |
| gaming | emb:text-embedding-3-small:enriched_tag | 3 | 1.000 |
| gaming | emb:text-embedding-3-small:enriched_tag_topic | 3 | 0.833 |
| gaming | emb:text-embedding-3-small:name_desc_server | 3 | 0.833 |
| gaming | emb_rerank:gpt-6-luna:raw:n20 | 3 | 0.500 |
| gaming | full_catalog:gpt-6-luna | 3 | 0.667 |
| gaming | full_catalog:gpt-6-luna:run2 | 3 | 0.667 |
| gaming | full_catalog_cards:gpt-6-luna | 3 | 0.667 |
| gaming | full_catalog_cards:gpt-6-luna:run2 | 3 | 0.667 |
| gaming | router:domain | 3 | 0.667 |
| gaming | router:server | 3 | 0.667 |
| geo_location | bm25:enriched_raw_tag | 5 | 0.350 |
| geo_location | bm25:enriched_tag | 5 | 0.350 |
| geo_location | bm25:name_desc_server | 5 | 0.400 |
| geo_location | emb:text-embedding-3-small:enriched_raw_tag | 5 | 0.350 |
| geo_location | emb:text-embedding-3-small:enriched_tag | 5 | 0.450 |
| geo_location | emb:text-embedding-3-small:enriched_tag_topic | 5 | 0.450 |
| geo_location | emb:text-embedding-3-small:name_desc_server | 5 | 0.500 |
| geo_location | emb_rerank:gpt-6-luna:raw:n20 | 5 | 0.600 |
| geo_location | full_catalog:gpt-6-luna | 5 | 0.900 |
| geo_location | full_catalog:gpt-6-luna:run2 | 5 | 0.900 |
| geo_location | full_catalog_cards:gpt-6-luna | 5 | 0.900 |
| geo_location | full_catalog_cards:gpt-6-luna:run2 | 5 | 0.900 |
| geo_location | router:domain | 5 | 0.650 |
| geo_location | router:server | 5 | 0.650 |
| lifestyle_utilities | bm25:enriched_raw_tag | 5 | 0.800 |
| lifestyle_utilities | bm25:enriched_tag | 5 | 0.500 |
| lifestyle_utilities | bm25:name_desc_server | 5 | 0.800 |
| lifestyle_utilities | emb:text-embedding-3-small:enriched_raw_tag | 5 | 0.900 |
| lifestyle_utilities | emb:text-embedding-3-small:enriched_tag | 5 | 0.800 |
| lifestyle_utilities | emb:text-embedding-3-small:enriched_tag_topic | 5 | 0.800 |
| lifestyle_utilities | emb:text-embedding-3-small:name_desc_server | 5 | 0.900 |
| lifestyle_utilities | emb_rerank:gpt-6-luna:raw:n20 | 5 | 0.900 |
| lifestyle_utilities | full_catalog:gpt-6-luna | 5 | 0.800 |
| lifestyle_utilities | full_catalog:gpt-6-luna:run2 | 5 | 0.600 |
| lifestyle_utilities | full_catalog_cards:gpt-6-luna | 5 | 0.700 |
| lifestyle_utilities | full_catalog_cards:gpt-6-luna:run2 | 5 | 0.700 |
| lifestyle_utilities | router:domain | 5 | 0.700 |
| lifestyle_utilities | router:server | 5 | 0.700 |
| local_files | bm25:enriched_raw_tag | 7 | 0.690 |
| local_files | bm25:enriched_tag | 7 | 0.643 |
| local_files | bm25:name_desc_server | 7 | 0.738 |
| local_files | emb:text-embedding-3-small:enriched_raw_tag | 7 | 0.643 |
| local_files | emb:text-embedding-3-small:enriched_tag | 7 | 0.643 |
| local_files | emb:text-embedding-3-small:enriched_tag_topic | 7 | 0.643 |
| local_files | emb:text-embedding-3-small:name_desc_server | 7 | 0.643 |
| local_files | emb_rerank:gpt-6-luna:raw:n20 | 7 | 0.548 |
| local_files | full_catalog:gpt-6-luna | 7 | 0.452 |
| local_files | full_catalog:gpt-6-luna:run2 | 7 | 0.643 |
| local_files | full_catalog_cards:gpt-6-luna | 7 | 0.643 |
| local_files | full_catalog_cards:gpt-6-luna:run2 | 7 | 0.690 |
| local_files | router:domain | 7 | 0.786 |
| local_files | router:server | 7 | 0.786 |
| media_visual_audio | bm25:enriched_raw_tag | 3 | 0.167 |
| media_visual_audio | bm25:enriched_tag | 3 | 0.000 |
| media_visual_audio | bm25:name_desc_server | 3 | 0.167 |
| media_visual_audio | emb:text-embedding-3-small:enriched_raw_tag | 3 | 0.389 |
| media_visual_audio | emb:text-embedding-3-small:enriched_tag | 3 | 0.278 |
| media_visual_audio | emb:text-embedding-3-small:enriched_tag_topic | 3 | 0.278 |
| media_visual_audio | emb:text-embedding-3-small:name_desc_server | 3 | 0.500 |
| media_visual_audio | emb_rerank:gpt-6-luna:raw:n20 | 3 | 0.333 |
| media_visual_audio | full_catalog:gpt-6-luna | 3 | 0.833 |
| media_visual_audio | full_catalog:gpt-6-luna:run2 | 3 | 1.000 |
| media_visual_audio | full_catalog_cards:gpt-6-luna | 3 | 0.833 |
| media_visual_audio | full_catalog_cards:gpt-6-luna:run2 | 3 | 0.722 |
| media_visual_audio | router:domain | 3 | 0.500 |
| media_visual_audio | router:server | 3 | 0.500 |
| news_and_trends | bm25:enriched_raw_tag | 8 | 0.562 |
| news_and_trends | bm25:enriched_tag | 8 | 0.625 |
| news_and_trends | bm25:name_desc_server | 8 | 0.438 |
| news_and_trends | emb:text-embedding-3-small:enriched_raw_tag | 8 | 0.688 |
| news_and_trends | emb:text-embedding-3-small:enriched_tag | 8 | 0.688 |
| news_and_trends | emb:text-embedding-3-small:enriched_tag_topic | 8 | 0.688 |
| news_and_trends | emb:text-embedding-3-small:name_desc_server | 8 | 0.531 |
| news_and_trends | emb_rerank:gpt-6-luna:raw:n20 | 8 | 0.625 |
| news_and_trends | full_catalog:gpt-6-luna | 8 | 0.438 |
| news_and_trends | full_catalog:gpt-6-luna:run2 | 8 | 0.500 |
| news_and_trends | full_catalog_cards:gpt-6-luna | 8 | 0.500 |
| news_and_trends | full_catalog_cards:gpt-6-luna:run2 | 8 | 0.500 |
| news_and_trends | router:domain | 8 | 0.615 |
| news_and_trends | router:server | 8 | 0.438 |
| security_network | bm25:enriched_raw_tag | 1 | 0.000 |
| security_network | bm25:enriched_tag | 1 | 0.000 |
| security_network | bm25:name_desc_server | 1 | 0.000 |
| security_network | emb:text-embedding-3-small:enriched_raw_tag | 1 | 0.333 |
| security_network | emb:text-embedding-3-small:enriched_tag | 1 | 0.333 |
| security_network | emb:text-embedding-3-small:enriched_tag_topic | 1 | 0.333 |
| security_network | emb:text-embedding-3-small:name_desc_server | 1 | 0.333 |
| security_network | emb_rerank:gpt-6-luna:raw:n20 | 1 | 0.333 |
| security_network | full_catalog:gpt-6-luna | 1 | 0.333 |
| security_network | full_catalog:gpt-6-luna:run2 | 1 | 0.333 |
| security_network | full_catalog_cards:gpt-6-luna | 1 | 0.333 |
| security_network | full_catalog_cards:gpt-6-luna:run2 | 1 | 0.333 |
| security_network | router:domain | 1 | 0.333 |
| security_network | router:server | 1 | 0.333 |
| shopping_research | bm25:enriched_raw_tag | 2 | 0.000 |
| shopping_research | bm25:enriched_tag | 2 | 0.000 |
| shopping_research | bm25:name_desc_server | 2 | 0.000 |
| shopping_research | emb:text-embedding-3-small:enriched_raw_tag | 2 | 0.000 |
| shopping_research | emb:text-embedding-3-small:enriched_tag | 2 | 0.125 |
| shopping_research | emb:text-embedding-3-small:enriched_tag_topic | 2 | 0.000 |
| shopping_research | emb:text-embedding-3-small:name_desc_server | 2 | 0.000 |
| shopping_research | emb_rerank:gpt-6-luna:raw:n20 | 2 | 0.000 |
| shopping_research | full_catalog:gpt-6-luna | 2 | 0.100 |
| shopping_research | full_catalog:gpt-6-luna:run2 | 2 | 0.100 |
| shopping_research | full_catalog_cards:gpt-6-luna | 2 | 0.100 |
| shopping_research | full_catalog_cards:gpt-6-luna:run2 | 2 | 0.100 |
| shopping_research | router:domain | 2 | 0.100 |
| shopping_research | router:server | 2 | 0.100 |
| travel_planning | bm25:enriched_raw_tag | 3 | 0.583 |
| travel_planning | bm25:enriched_tag | 3 | 0.583 |
| travel_planning | bm25:name_desc_server | 3 | 0.250 |
| travel_planning | emb:text-embedding-3-small:enriched_raw_tag | 3 | 0.500 |
| travel_planning | emb:text-embedding-3-small:enriched_tag | 3 | 0.500 |
| travel_planning | emb:text-embedding-3-small:enriched_tag_topic | 3 | 0.500 |
| travel_planning | emb:text-embedding-3-small:name_desc_server | 3 | 0.417 |
| travel_planning | emb_rerank:gpt-6-luna:raw:n20 | 3 | 0.583 |
| travel_planning | full_catalog:gpt-6-luna | 3 | 0.833 |
| travel_planning | full_catalog:gpt-6-luna:run2 | 3 | 0.583 |
| travel_planning | full_catalog_cards:gpt-6-luna | 3 | 0.667 |
| travel_planning | full_catalog_cards:gpt-6-luna:run2 | 3 | 0.917 |
| travel_planning | router:domain | 3 | 0.667 |
| travel_planning | router:server | 3 | 0.750 |
| web_research_writing | bm25:enriched_raw_tag | 2 | 0.250 |
| web_research_writing | bm25:enriched_tag | 2 | 0.250 |
| web_research_writing | bm25:name_desc_server | 2 | 0.250 |
| web_research_writing | emb:text-embedding-3-small:enriched_raw_tag | 2 | 0.250 |
| web_research_writing | emb:text-embedding-3-small:enriched_tag | 2 | 0.000 |
| web_research_writing | emb:text-embedding-3-small:enriched_tag_topic | 2 | 0.000 |
| web_research_writing | emb:text-embedding-3-small:name_desc_server | 2 | 0.250 |
| web_research_writing | emb_rerank:gpt-6-luna:raw:n20 | 2 | 0.000 |
| web_research_writing | full_catalog:gpt-6-luna | 2 | 0.833 |
| web_research_writing | full_catalog:gpt-6-luna:run2 | 2 | 0.833 |
| web_research_writing | full_catalog_cards:gpt-6-luna | 2 | 0.583 |
| web_research_writing | full_catalog_cards:gpt-6-luna:run2 | 2 | 0.583 |
| web_research_writing | router:domain | 2 | 0.333 |
| web_research_writing | router:server | 2 | 0.583 |

## 4. Per split (mean over queries)

| Split | System | n | slot_recall@5 | full_coverage@5 |
|---|---|---|---|---|
| dev | bm25:enriched_raw_tag | 18 | 0.486 | 0.333 |
| dev | bm25:enriched_tag | 18 | 0.366 | 0.167 |
| dev | bm25:name_desc_server | 18 | 0.435 | 0.333 |
| dev | emb:text-embedding-3-small:enriched_raw_tag | 18 | 0.472 | 0.278 |
| dev | emb:text-embedding-3-small:enriched_tag | 18 | 0.468 | 0.278 |
| dev | emb:text-embedding-3-small:enriched_tag_topic | 18 | 0.440 | 0.222 |
| dev | emb:text-embedding-3-small:name_desc_server | 18 | 0.574 | 0.333 |
| dev | emb_rerank:gpt-6-luna:raw:n20 | 18 | 0.602 | 0.389 |
| dev | full_catalog:gpt-6-luna | 18 | 0.622 | 0.389 |
| dev | full_catalog:gpt-6-luna:run2 | 18 | 0.719 | 0.556 |
| dev | full_catalog_cards:gpt-6-luna | 18 | 0.733 | 0.500 |
| dev | full_catalog_cards:gpt-6-luna:run2 | 18 | 0.729 | 0.444 |
| dev | router:domain | 18 | 0.622 | 0.333 |
| dev | router:server | 18 | 0.692 | 0.444 |
| test | bm25:enriched_raw_tag | 42 | 0.438 | 0.262 |
| test | bm25:enriched_tag | 42 | 0.435 | 0.262 |
| test | bm25:name_desc_server | 42 | 0.403 | 0.214 |
| test | emb:text-embedding-3-small:enriched_raw_tag | 42 | 0.546 | 0.333 |
| test | emb:text-embedding-3-small:enriched_tag | 42 | 0.556 | 0.333 |
| test | emb:text-embedding-3-small:enriched_tag_topic | 42 | 0.563 | 0.333 |
| test | emb:text-embedding-3-small:name_desc_server | 42 | 0.492 | 0.262 |
| test | emb_rerank:gpt-6-luna:raw:n20 | 42 | 0.518 | 0.333 |
| test | full_catalog:gpt-6-luna | 42 | 0.589 | 0.405 |
| test | full_catalog:gpt-6-luna:run2 | 42 | 0.601 | 0.429 |
| test | full_catalog_cards:gpt-6-luna | 42 | 0.593 | 0.429 |
| test | full_catalog_cards:gpt-6-luna:run2 | 42 | 0.627 | 0.429 |
| test | router:domain | 42 | 0.661 | 0.452 |
| test | router:server | 42 | 0.615 | 0.381 |

## 5. Paired comparisons (A minus B, same queries)

### bm25:enriched_raw_tag - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.039 | [-0.025, 0.101] | 9 | 4 | 47 | 60 |
| full_coverage@5 | 0.050 | [-0.017, 0.133] | 4 | 1 | 55 | 60 |
| r_precision | -0.018 | [-0.093, 0.053] | 7 | 7 | 46 | 60 |
| mrr | 0.014 | [-0.049, 0.082] | 11 | 14 | 35 | 60 |

### bm25:enriched_raw_tag - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.040 | [-0.024, 0.107] | 9 | 5 | 46 | 60 |
| full_coverage@5 | 0.033 | [-0.033, 0.100] | 3 | 1 | 56 | 60 |
| r_precision | 0.047 | [-0.013, 0.104] | 11 | 4 | 45 | 60 |
| mrr | 0.060 | [-0.017, 0.138] | 17 | 9 | 34 | 60 |

### bm25:enriched_raw_tag - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.071 | [-0.158, 0.015] | 7 | 13 | 40 | 60 |
| full_coverage@5 | -0.033 | [-0.117, 0.050] | 2 | 4 | 54 | 60 |
| r_precision | -0.163 | [-0.268, -0.064] | 8 | 20 | 32 | 60 |
| mrr | -0.146 | [-0.250, -0.046] | 10 | 25 | 25 | 60 |

### bm25:enriched_raw_tag - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.076 | [-0.168, 0.010] | 9 | 17 | 34 | 60 |
| full_coverage@5 | -0.033 | [-0.117, 0.050] | 2 | 4 | 54 | 60 |
| r_precision | -0.189 | [-0.293, -0.089] | 7 | 25 | 28 | 60 |
| mrr | -0.178 | [-0.291, -0.067] | 9 | 28 | 23 | 60 |

### bm25:enriched_raw_tag - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.074 | [-0.164, 0.014] | 8 | 16 | 36 | 60 |
| full_coverage@5 | -0.017 | [-0.100, 0.067] | 3 | 4 | 53 | 60 |
| r_precision | -0.183 | [-0.289, -0.085] | 7 | 23 | 30 | 60 |
| mrr | -0.175 | [-0.290, -0.065] | 10 | 26 | 24 | 60 |

### bm25:enriched_raw_tag - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.064 | [-0.168, 0.035] | 10 | 16 | 34 | 60 |
| full_coverage@5 | 0.000 | [-0.100, 0.100] | 5 | 5 | 50 | 60 |
| r_precision | -0.106 | [-0.219, 0.008] | 11 | 20 | 29 | 60 |
| mrr | -0.101 | [-0.218, 0.012] | 15 | 24 | 21 | 60 |

### bm25:enriched_raw_tag - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.090 | [-0.201, 0.018] | 9 | 19 | 32 | 60 |
| full_coverage@5 | -0.067 | [-0.183, 0.050] | 5 | 9 | 46 | 60 |
| r_precision | -0.366 | [-0.480, -0.253] | 5 | 36 | 17 | 58 |
| mrr | -0.215 | [-0.342, -0.087] | 9 | 27 | 24 | 60 |

### bm25:enriched_raw_tag - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.146 | [-0.271, -0.016] | 7 | 26 | 27 | 60 |
| full_coverage@5 | -0.117 | [-0.250, 0.017] | 6 | 13 | 41 | 60 |
| r_precision | -0.378 | [-0.497, -0.259] | 5 | 36 | 17 | 58 |
| mrr | -0.212 | [-0.350, -0.071] | 11 | 29 | 20 | 60 |

### bm25:enriched_raw_tag - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.184 | [-0.304, -0.058] | 6 | 28 | 26 | 60 |
| full_coverage@5 | -0.183 | [-0.317, -0.050] | 5 | 16 | 39 | 60 |
| r_precision | -0.341 | [-0.469, -0.215] | 8 | 34 | 17 | 59 |
| mrr | -0.190 | [-0.331, -0.049] | 14 | 28 | 18 | 60 |

### bm25:enriched_raw_tag - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.182 | [-0.292, -0.066] | 5 | 29 | 26 | 60 |
| full_coverage@5 | -0.167 | [-0.300, -0.033] | 5 | 15 | 40 | 60 |
| r_precision | -0.383 | [-0.496, -0.271] | 5 | 38 | 17 | 60 |
| mrr | -0.269 | [-0.399, -0.140] | 9 | 32 | 19 | 60 |

### bm25:enriched_raw_tag - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.205 | [-0.310, -0.094] | 4 | 28 | 28 | 60 |
| full_coverage@5 | -0.150 | [-0.283, -0.017] | 4 | 13 | 43 | 60 |
| r_precision | -0.396 | [-0.510, -0.282] | 6 | 39 | 15 | 60 |
| mrr | -0.269 | [-0.395, -0.142] | 8 | 32 | 20 | 60 |

### bm25:enriched_raw_tag - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.196 | [-0.313, -0.080] | 7 | 29 | 24 | 60 |
| full_coverage@5 | -0.133 | [-0.267, 0.000] | 5 | 13 | 42 | 60 |
| r_precision | -0.332 | [-0.439, -0.229] | 4 | 35 | 21 | 60 |
| mrr | -0.263 | [-0.388, -0.138] | 7 | 31 | 22 | 60 |

### bm25:enriched_raw_tag - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.185 | [-0.303, -0.068] | 6 | 26 | 28 | 60 |
| full_coverage@5 | -0.117 | [-0.250, 0.017] | 5 | 12 | 43 | 60 |
| r_precision | -0.344 | [-0.443, -0.247] | 2 | 37 | 21 | 60 |
| mrr | -0.225 | [-0.354, -0.100] | 11 | 28 | 21 | 60 |

### bm25:enriched_tag - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.039 | [-0.101, 0.025] | 4 | 9 | 47 | 60 |
| full_coverage@5 | -0.050 | [-0.133, 0.017] | 1 | 4 | 55 | 60 |
| r_precision | 0.018 | [-0.053, 0.093] | 7 | 7 | 46 | 60 |
| mrr | -0.014 | [-0.082, 0.049] | 14 | 11 | 35 | 60 |

### bm25:enriched_tag - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.001 | [-0.086, 0.086] | 12 | 11 | 37 | 60 |
| full_coverage@5 | -0.017 | [-0.100, 0.067] | 3 | 4 | 53 | 60 |
| r_precision | 0.065 | [-0.025, 0.156] | 16 | 8 | 36 | 60 |
| mrr | 0.047 | [-0.051, 0.148] | 21 | 14 | 25 | 60 |

### bm25:enriched_tag - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.110 | [-0.194, -0.028] | 4 | 16 | 40 | 60 |
| full_coverage@5 | -0.083 | [-0.167, 0.000] | 1 | 6 | 53 | 60 |
| r_precision | -0.144 | [-0.249, -0.046] | 9 | 20 | 31 | 60 |
| mrr | -0.160 | [-0.272, -0.050] | 10 | 28 | 22 | 60 |

### bm25:enriched_tag - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.115 | [-0.201, -0.033] | 6 | 20 | 34 | 60 |
| full_coverage@5 | -0.083 | [-0.167, 0.000] | 1 | 6 | 53 | 60 |
| r_precision | -0.171 | [-0.274, -0.074] | 8 | 23 | 29 | 60 |
| mrr | -0.191 | [-0.309, -0.074] | 9 | 29 | 22 | 60 |

### bm25:enriched_tag - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.112 | [-0.196, -0.032] | 4 | 18 | 38 | 60 |
| full_coverage@5 | -0.067 | [-0.150, 0.000] | 1 | 5 | 54 | 60 |
| r_precision | -0.165 | [-0.268, -0.068] | 7 | 21 | 32 | 60 |
| mrr | -0.189 | [-0.305, -0.073] | 9 | 27 | 24 | 60 |

### bm25:enriched_tag - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.103 | [-0.204, -0.006] | 8 | 20 | 32 | 60 |
| full_coverage@5 | -0.050 | [-0.150, 0.050] | 4 | 7 | 49 | 60 |
| r_precision | -0.087 | [-0.194, 0.019] | 12 | 21 | 27 | 60 |
| mrr | -0.114 | [-0.238, 0.010] | 14 | 26 | 20 | 60 |

### bm25:enriched_tag - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.129 | [-0.235, -0.025] | 6 | 23 | 31 | 60 |
| full_coverage@5 | -0.117 | [-0.233, 0.000] | 3 | 10 | 47 | 60 |
| r_precision | -0.348 | [-0.458, -0.234] | 5 | 35 | 18 | 58 |
| mrr | -0.228 | [-0.363, -0.092] | 11 | 28 | 21 | 60 |

### bm25:enriched_tag - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.185 | [-0.305, -0.057] | 7 | 31 | 22 | 60 |
| full_coverage@5 | -0.167 | [-0.300, -0.033] | 5 | 15 | 40 | 60 |
| r_precision | -0.359 | [-0.483, -0.233] | 5 | 36 | 17 | 58 |
| mrr | -0.226 | [-0.372, -0.076] | 10 | 30 | 20 | 60 |

### bm25:enriched_tag - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.223 | [-0.343, -0.101] | 6 | 33 | 21 | 60 |
| full_coverage@5 | -0.233 | [-0.367, -0.100] | 4 | 18 | 38 | 60 |
| r_precision | -0.323 | [-0.451, -0.195] | 7 | 33 | 19 | 59 |
| mrr | -0.204 | [-0.349, -0.058] | 12 | 28 | 20 | 60 |

### bm25:enriched_tag - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.221 | [-0.331, -0.104] | 4 | 32 | 24 | 60 |
| full_coverage@5 | -0.217 | [-0.350, -0.083] | 4 | 17 | 39 | 60 |
| r_precision | -0.364 | [-0.487, -0.242] | 5 | 38 | 17 | 60 |
| mrr | -0.283 | [-0.418, -0.145] | 9 | 32 | 19 | 60 |

### bm25:enriched_tag - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.244 | [-0.342, -0.135] | 3 | 35 | 22 | 60 |
| full_coverage@5 | -0.200 | [-0.333, -0.067] | 3 | 15 | 42 | 60 |
| r_precision | -0.378 | [-0.499, -0.253] | 6 | 39 | 15 | 60 |
| mrr | -0.283 | [-0.413, -0.149] | 8 | 32 | 20 | 60 |

### bm25:enriched_tag - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.235 | [-0.346, -0.119] | 5 | 33 | 22 | 60 |
| full_coverage@5 | -0.183 | [-0.317, -0.050] | 4 | 15 | 41 | 60 |
| r_precision | -0.314 | [-0.425, -0.201] | 4 | 36 | 20 | 60 |
| mrr | -0.277 | [-0.412, -0.141] | 9 | 32 | 19 | 60 |

### bm25:enriched_tag - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.224 | [-0.338, -0.108] | 5 | 31 | 24 | 60 |
| full_coverage@5 | -0.167 | [-0.300, -0.033] | 4 | 14 | 42 | 60 |
| r_precision | -0.326 | [-0.437, -0.212] | 5 | 37 | 18 | 60 |
| mrr | -0.238 | [-0.379, -0.097] | 12 | 29 | 19 | 60 |

### bm25:name_desc_server - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.040 | [-0.107, 0.024] | 5 | 9 | 46 | 60 |
| full_coverage@5 | -0.033 | [-0.100, 0.033] | 1 | 3 | 56 | 60 |
| r_precision | -0.047 | [-0.104, 0.013] | 4 | 11 | 45 | 60 |
| mrr | -0.060 | [-0.138, 0.017] | 9 | 17 | 34 | 60 |

### bm25:name_desc_server - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.001 | [-0.086, 0.086] | 11 | 12 | 37 | 60 |
| full_coverage@5 | 0.017 | [-0.067, 0.100] | 4 | 3 | 53 | 60 |
| r_precision | -0.065 | [-0.156, 0.025] | 8 | 16 | 36 | 60 |
| mrr | -0.047 | [-0.148, 0.051] | 14 | 21 | 25 | 60 |

### bm25:name_desc_server - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.111 | [-0.203, -0.021] | 6 | 17 | 37 | 60 |
| full_coverage@5 | -0.067 | [-0.167, 0.017] | 2 | 6 | 52 | 60 |
| r_precision | -0.210 | [-0.319, -0.107] | 7 | 26 | 27 | 60 |
| mrr | -0.207 | [-0.322, -0.095] | 9 | 30 | 21 | 60 |

### bm25:name_desc_server - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.117 | [-0.212, -0.025] | 8 | 21 | 31 | 60 |
| full_coverage@5 | -0.067 | [-0.167, 0.017] | 2 | 6 | 52 | 60 |
| r_precision | -0.236 | [-0.333, -0.142] | 6 | 30 | 24 | 60 |
| mrr | -0.238 | [-0.352, -0.129] | 8 | 31 | 21 | 60 |

### bm25:name_desc_server - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.114 | [-0.210, -0.021] | 7 | 20 | 33 | 60 |
| full_coverage@5 | -0.050 | [-0.150, 0.050] | 3 | 6 | 51 | 60 |
| r_precision | -0.231 | [-0.333, -0.135] | 6 | 28 | 26 | 60 |
| mrr | -0.235 | [-0.348, -0.126] | 9 | 30 | 21 | 60 |

### bm25:name_desc_server - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.104 | [-0.206, -0.007] | 5 | 16 | 39 | 60 |
| full_coverage@5 | -0.033 | [-0.133, 0.050] | 3 | 5 | 52 | 60 |
| r_precision | -0.153 | [-0.263, -0.044] | 8 | 22 | 30 | 60 |
| mrr | -0.161 | [-0.271, -0.053] | 10 | 28 | 22 | 60 |

### bm25:name_desc_server - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.131 | [-0.246, -0.015] | 8 | 22 | 30 | 60 |
| full_coverage@5 | -0.100 | [-0.233, 0.033] | 5 | 11 | 44 | 60 |
| r_precision | -0.415 | [-0.526, -0.305] | 3 | 38 | 17 | 58 |
| mrr | -0.275 | [-0.402, -0.145] | 8 | 30 | 22 | 60 |

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

### bm25:name_desc_server - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.223 | [-0.346, -0.094] | 6 | 32 | 22 | 60 |
| full_coverage@5 | -0.200 | [-0.350, -0.050] | 5 | 17 | 38 | 60 |
| r_precision | -0.430 | [-0.553, -0.306] | 5 | 41 | 14 | 60 |
| mrr | -0.330 | [-0.475, -0.184] | 10 | 36 | 14 | 60 |

### bm25:name_desc_server - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.245 | [-0.365, -0.117] | 6 | 30 | 24 | 60 |
| full_coverage@5 | -0.183 | [-0.317, -0.050] | 4 | 15 | 41 | 60 |
| r_precision | -0.443 | [-0.565, -0.317] | 5 | 41 | 14 | 60 |
| mrr | -0.330 | [-0.471, -0.184] | 9 | 36 | 15 | 60 |

### bm25:name_desc_server - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.237 | [-0.359, -0.114] | 5 | 29 | 26 | 60 |
| full_coverage@5 | -0.167 | [-0.300, -0.033] | 4 | 14 | 42 | 60 |
| r_precision | -0.379 | [-0.494, -0.261] | 5 | 39 | 16 | 60 |
| mrr | -0.324 | [-0.449, -0.196] | 7 | 36 | 17 | 60 |

### bm25:name_desc_server - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.226 | [-0.353, -0.095] | 6 | 31 | 23 | 60 |
| full_coverage@5 | -0.150 | [-0.283, -0.017] | 5 | 14 | 41 | 60 |
| r_precision | -0.391 | [-0.499, -0.281] | 3 | 41 | 16 | 60 |
| mrr | -0.285 | [-0.418, -0.154] | 10 | 34 | 16 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.071 | [-0.015, 0.158] | 13 | 7 | 40 | 60 |
| full_coverage@5 | 0.033 | [-0.050, 0.117] | 4 | 2 | 54 | 60 |
| r_precision | 0.163 | [0.064, 0.268] | 20 | 8 | 32 | 60 |
| mrr | 0.146 | [0.046, 0.250] | 25 | 10 | 25 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.110 | [0.028, 0.194] | 16 | 4 | 40 | 60 |
| full_coverage@5 | 0.083 | [0.000, 0.167] | 6 | 1 | 53 | 60 |
| r_precision | 0.144 | [0.046, 0.249] | 20 | 9 | 31 | 60 |
| mrr | 0.160 | [0.050, 0.272] | 28 | 10 | 22 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.111 | [0.021, 0.203] | 17 | 6 | 37 | 60 |
| full_coverage@5 | 0.067 | [-0.017, 0.167] | 6 | 2 | 52 | 60 |
| r_precision | 0.210 | [0.107, 0.319] | 26 | 7 | 27 | 60 |
| mrr | 0.207 | [0.095, 0.322] | 30 | 9 | 21 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.006 | [-0.049, 0.037] | 5 | 6 | 49 | 60 |
| full_coverage@5 | 0.000 | [-0.050, 0.050] | 1 | 1 | 58 | 60 |
| r_precision | -0.026 | [-0.089, 0.033] | 5 | 10 | 45 | 60 |
| mrr | -0.031 | [-0.098, 0.034] | 11 | 12 | 37 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.003 | [-0.040, 0.035] | 3 | 4 | 53 | 60 |
| full_coverage@5 | 0.017 | [0.000, 0.050] | 1 | 0 | 59 | 60 |
| r_precision | -0.021 | [-0.076, 0.031] | 4 | 7 | 49 | 60 |
| mrr | -0.029 | [-0.087, 0.026] | 8 | 12 | 40 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.007 | [-0.040, 0.062] | 5 | 6 | 49 | 60 |
| full_coverage@5 | 0.033 | [-0.033, 0.100] | 3 | 1 | 56 | 60 |
| r_precision | 0.057 | [-0.025, 0.144] | 11 | 7 | 42 | 60 |
| mrr | 0.046 | [-0.033, 0.124] | 15 | 12 | 33 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.019 | [-0.104, 0.071] | 7 | 13 | 40 | 60 |
| full_coverage@5 | -0.033 | [-0.133, 0.067] | 4 | 6 | 50 | 60 |
| r_precision | -0.198 | [-0.290, -0.105] | 4 | 26 | 28 | 58 |
| mrr | -0.068 | [-0.165, 0.030] | 9 | 15 | 36 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.076 | [-0.208, 0.065] | 11 | 24 | 25 | 60 |
| full_coverage@5 | -0.083 | [-0.233, 0.067] | 8 | 13 | 39 | 60 |
| r_precision | -0.227 | [-0.349, -0.101] | 8 | 31 | 19 | 58 |
| mrr | -0.066 | [-0.212, 0.081] | 16 | 20 | 24 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.113 | [-0.240, 0.018] | 9 | 24 | 27 | 60 |
| full_coverage@5 | -0.150 | [-0.300, 0.000] | 6 | 15 | 39 | 60 |
| r_precision | -0.176 | [-0.302, -0.048] | 11 | 28 | 20 | 59 |
| mrr | -0.044 | [-0.181, 0.092] | 18 | 18 | 24 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.112 | [-0.228, 0.010] | 8 | 23 | 29 | 60 |
| full_coverage@5 | -0.133 | [-0.283, 0.000] | 6 | 14 | 40 | 60 |
| r_precision | -0.220 | [-0.331, -0.107] | 6 | 30 | 24 | 60 |
| mrr | -0.123 | [-0.248, 0.001] | 13 | 19 | 28 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.134 | [-0.256, -0.005] | 8 | 24 | 28 | 60 |
| full_coverage@5 | -0.117 | [-0.250, 0.017] | 6 | 13 | 41 | 60 |
| r_precision | -0.233 | [-0.342, -0.119] | 5 | 30 | 25 | 60 |
| mrr | -0.123 | [-0.246, 0.000] | 12 | 19 | 29 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.126 | [-0.235, -0.016] | 8 | 22 | 30 | 60 |
| full_coverage@5 | -0.100 | [-0.217, 0.017] | 4 | 10 | 46 | 60 |
| r_precision | -0.169 | [-0.279, -0.053] | 9 | 31 | 20 | 60 |
| mrr | -0.117 | [-0.239, 0.002] | 12 | 21 | 27 | 60 |

### emb:text-embedding-3-small:enriched_raw_tag - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.114 | [-0.226, -0.002] | 8 | 23 | 29 | 60 |
| full_coverage@5 | -0.083 | [-0.217, 0.033] | 5 | 10 | 45 | 60 |
| r_precision | -0.181 | [-0.287, -0.071] | 8 | 32 | 20 | 60 |
| mrr | -0.079 | [-0.205, 0.047] | 16 | 19 | 25 | 60 |

### emb:text-embedding-3-small:enriched_tag - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.076 | [-0.010, 0.168] | 17 | 9 | 34 | 60 |
| full_coverage@5 | 0.033 | [-0.050, 0.117] | 4 | 2 | 54 | 60 |
| r_precision | 0.189 | [0.089, 0.293] | 25 | 7 | 28 | 60 |
| mrr | 0.178 | [0.067, 0.291] | 28 | 9 | 23 | 60 |

### emb:text-embedding-3-small:enriched_tag - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.115 | [0.033, 0.201] | 20 | 6 | 34 | 60 |
| full_coverage@5 | 0.083 | [0.000, 0.167] | 6 | 1 | 53 | 60 |
| r_precision | 0.171 | [0.074, 0.274] | 23 | 8 | 29 | 60 |
| mrr | 0.191 | [0.074, 0.309] | 29 | 9 | 22 | 60 |

### emb:text-embedding-3-small:enriched_tag - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.117 | [0.025, 0.212] | 21 | 8 | 31 | 60 |
| full_coverage@5 | 0.067 | [-0.017, 0.167] | 6 | 2 | 52 | 60 |
| r_precision | 0.236 | [0.142, 0.333] | 30 | 6 | 24 | 60 |
| mrr | 0.238 | [0.129, 0.352] | 31 | 8 | 21 | 60 |

### emb:text-embedding-3-small:enriched_tag - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.006 | [-0.037, 0.049] | 6 | 5 | 49 | 60 |
| full_coverage@5 | 0.000 | [-0.050, 0.050] | 1 | 1 | 58 | 60 |
| r_precision | 0.026 | [-0.033, 0.089] | 10 | 5 | 45 | 60 |
| mrr | 0.031 | [-0.034, 0.098] | 12 | 11 | 37 | 60 |

### emb:text-embedding-3-small:enriched_tag - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.003 | [-0.019, 0.026] | 2 | 2 | 56 | 60 |
| full_coverage@5 | 0.017 | [0.000, 0.050] | 1 | 0 | 59 | 60 |
| r_precision | 0.006 | [-0.033, 0.042] | 4 | 2 | 54 | 60 |
| mrr | 0.003 | [-0.037, 0.040] | 8 | 8 | 44 | 60 |

### emb:text-embedding-3-small:enriched_tag - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.013 | [-0.050, 0.079] | 8 | 8 | 44 | 60 |
| full_coverage@5 | 0.033 | [-0.050, 0.117] | 4 | 2 | 54 | 60 |
| r_precision | 0.083 | [-0.003, 0.174] | 12 | 8 | 40 | 60 |
| mrr | 0.077 | [-0.013, 0.165] | 18 | 13 | 29 | 60 |

### emb:text-embedding-3-small:enriched_tag - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.014 | [-0.094, 0.074] | 8 | 14 | 38 | 60 |
| full_coverage@5 | -0.033 | [-0.133, 0.067] | 4 | 6 | 50 | 60 |
| r_precision | -0.171 | [-0.266, -0.073] | 7 | 27 | 24 | 58 |
| mrr | -0.037 | [-0.130, 0.059] | 12 | 14 | 34 | 60 |

### emb:text-embedding-3-small:enriched_tag - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.070 | [-0.203, 0.068] | 12 | 22 | 26 | 60 |
| full_coverage@5 | -0.083 | [-0.217, 0.050] | 7 | 12 | 41 | 60 |
| r_precision | -0.200 | [-0.335, -0.063] | 11 | 30 | 17 | 58 |
| mrr | -0.035 | [-0.189, 0.122] | 18 | 19 | 23 | 60 |

### emb:text-embedding-3-small:enriched_tag - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.107 | [-0.233, 0.021] | 10 | 23 | 27 | 60 |
| full_coverage@5 | -0.150 | [-0.283, -0.017] | 5 | 14 | 41 | 60 |
| r_precision | -0.166 | [-0.293, -0.039] | 12 | 27 | 20 | 59 |
| mrr | -0.013 | [-0.156, 0.134] | 19 | 18 | 23 | 60 |

### emb:text-embedding-3-small:enriched_tag - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.106 | [-0.220, 0.013] | 8 | 23 | 29 | 60 |
| full_coverage@5 | -0.133 | [-0.267, 0.000] | 5 | 13 | 42 | 60 |
| r_precision | -0.194 | [-0.317, -0.068] | 10 | 29 | 21 | 60 |
| mrr | -0.092 | [-0.230, 0.049] | 15 | 20 | 25 | 60 |

### emb:text-embedding-3-small:enriched_tag - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.128 | [-0.246, -0.003] | 8 | 25 | 27 | 60 |
| full_coverage@5 | -0.117 | [-0.250, 0.017] | 5 | 12 | 43 | 60 |
| r_precision | -0.207 | [-0.331, -0.079] | 11 | 31 | 18 | 60 |
| mrr | -0.092 | [-0.229, 0.049] | 14 | 20 | 26 | 60 |

### emb:text-embedding-3-small:enriched_tag - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.120 | [-0.222, -0.019] | 7 | 19 | 34 | 60 |
| full_coverage@5 | -0.100 | [-0.217, 0.000] | 3 | 9 | 48 | 60 |
| r_precision | -0.143 | [-0.258, -0.024] | 11 | 28 | 21 | 60 |
| mrr | -0.086 | [-0.217, 0.042] | 16 | 19 | 25 | 60 |

### emb:text-embedding-3-small:enriched_tag - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.109 | [-0.215, -0.001] | 8 | 21 | 31 | 60 |
| full_coverage@5 | -0.083 | [-0.200, 0.033] | 4 | 9 | 47 | 60 |
| r_precision | -0.155 | [-0.270, -0.035] | 11 | 29 | 20 | 60 |
| mrr | -0.047 | [-0.184, 0.090] | 18 | 19 | 23 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.074 | [-0.014, 0.164] | 16 | 8 | 36 | 60 |
| full_coverage@5 | 0.017 | [-0.067, 0.100] | 4 | 3 | 53 | 60 |
| r_precision | 0.183 | [0.085, 0.289] | 23 | 7 | 30 | 60 |
| mrr | 0.175 | [0.065, 0.290] | 26 | 10 | 24 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.112 | [0.032, 0.196] | 18 | 4 | 38 | 60 |
| full_coverage@5 | 0.067 | [0.000, 0.150] | 5 | 1 | 54 | 60 |
| r_precision | 0.165 | [0.068, 0.268] | 21 | 7 | 32 | 60 |
| mrr | 0.189 | [0.073, 0.305] | 27 | 9 | 24 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.114 | [0.021, 0.210] | 20 | 7 | 33 | 60 |
| full_coverage@5 | 0.050 | [-0.050, 0.150] | 6 | 3 | 51 | 60 |
| r_precision | 0.231 | [0.135, 0.333] | 28 | 6 | 26 | 60 |
| mrr | 0.235 | [0.126, 0.348] | 30 | 9 | 21 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.003 | [-0.035, 0.040] | 4 | 3 | 53 | 60 |
| full_coverage@5 | -0.017 | [-0.050, 0.000] | 0 | 1 | 59 | 60 |
| r_precision | 0.021 | [-0.031, 0.076] | 7 | 4 | 49 | 60 |
| mrr | 0.029 | [-0.026, 0.087] | 12 | 8 | 40 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.003 | [-0.026, 0.019] | 2 | 2 | 56 | 60 |
| full_coverage@5 | -0.017 | [-0.050, 0.000] | 0 | 1 | 59 | 60 |
| r_precision | -0.006 | [-0.042, 0.033] | 2 | 4 | 54 | 60 |
| mrr | -0.003 | [-0.040, 0.037] | 8 | 8 | 44 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.010 | [-0.050, 0.075] | 7 | 7 | 46 | 60 |
| full_coverage@5 | 0.017 | [-0.050, 0.083] | 3 | 2 | 55 | 60 |
| r_precision | 0.078 | [-0.001, 0.161] | 12 | 7 | 41 | 60 |
| mrr | 0.074 | [0.001, 0.148] | 18 | 10 | 32 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.017 | [-0.093, 0.068] | 6 | 12 | 42 | 60 |
| full_coverage@5 | -0.050 | [-0.150, 0.050] | 3 | 6 | 51 | 60 |
| r_precision | -0.177 | [-0.259, -0.093] | 4 | 26 | 28 | 58 |
| mrr | -0.040 | [-0.124, 0.046] | 12 | 14 | 34 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.073 | [-0.203, 0.065] | 11 | 22 | 27 | 60 |
| full_coverage@5 | -0.100 | [-0.233, 0.050] | 7 | 13 | 40 | 60 |
| r_precision | -0.205 | [-0.332, -0.079] | 8 | 29 | 21 | 58 |
| mrr | -0.037 | [-0.180, 0.109] | 16 | 18 | 26 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.110 | [-0.234, 0.015] | 9 | 23 | 28 | 60 |
| full_coverage@5 | -0.167 | [-0.300, -0.033] | 5 | 15 | 40 | 60 |
| r_precision | -0.171 | [-0.290, -0.055] | 9 | 26 | 24 | 59 |
| mrr | -0.015 | [-0.151, 0.121] | 19 | 17 | 24 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.109 | [-0.221, 0.008] | 7 | 23 | 30 | 60 |
| full_coverage@5 | -0.150 | [-0.283, -0.017] | 5 | 14 | 41 | 60 |
| r_precision | -0.199 | [-0.314, -0.086] | 7 | 28 | 25 | 60 |
| mrr | -0.094 | [-0.225, 0.036] | 16 | 20 | 24 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.131 | [-0.246, -0.007] | 7 | 25 | 28 | 60 |
| full_coverage@5 | -0.133 | [-0.267, 0.000] | 5 | 13 | 42 | 60 |
| r_precision | -0.212 | [-0.326, -0.096] | 8 | 30 | 22 | 60 |
| mrr | -0.094 | [-0.221, 0.034] | 13 | 20 | 27 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.123 | [-0.220, -0.025] | 6 | 20 | 34 | 60 |
| full_coverage@5 | -0.117 | [-0.233, 0.000] | 3 | 10 | 47 | 60 |
| r_precision | -0.149 | [-0.257, -0.036] | 9 | 28 | 23 | 60 |
| mrr | -0.088 | [-0.208, 0.029] | 16 | 19 | 25 | 60 |

### emb:text-embedding-3-small:enriched_tag_topic - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.112 | [-0.216, -0.006] | 7 | 22 | 31 | 60 |
| full_coverage@5 | -0.100 | [-0.217, 0.017] | 4 | 10 | 46 | 60 |
| r_precision | -0.160 | [-0.266, -0.050] | 7 | 29 | 24 | 60 |
| mrr | -0.050 | [-0.180, 0.078] | 18 | 17 | 25 | 60 |

### emb:text-embedding-3-small:name_desc_server - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.064 | [-0.035, 0.168] | 16 | 10 | 34 | 60 |
| full_coverage@5 | 0.000 | [-0.100, 0.100] | 5 | 5 | 50 | 60 |
| r_precision | 0.106 | [-0.008, 0.219] | 20 | 11 | 29 | 60 |
| mrr | 0.101 | [-0.012, 0.218] | 24 | 15 | 21 | 60 |

### emb:text-embedding-3-small:name_desc_server - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.103 | [0.006, 0.204] | 20 | 8 | 32 | 60 |
| full_coverage@5 | 0.050 | [-0.050, 0.150] | 7 | 4 | 49 | 60 |
| r_precision | 0.087 | [-0.019, 0.194] | 21 | 12 | 27 | 60 |
| mrr | 0.114 | [-0.010, 0.238] | 26 | 14 | 20 | 60 |

### emb:text-embedding-3-small:name_desc_server - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.104 | [0.007, 0.206] | 16 | 5 | 39 | 60 |
| full_coverage@5 | 0.033 | [-0.050, 0.133] | 5 | 3 | 52 | 60 |
| r_precision | 0.153 | [0.044, 0.263] | 22 | 8 | 30 | 60 |
| mrr | 0.161 | [0.053, 0.271] | 28 | 10 | 22 | 60 |

### emb:text-embedding-3-small:name_desc_server - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.007 | [-0.062, 0.040] | 6 | 5 | 49 | 60 |
| full_coverage@5 | -0.033 | [-0.100, 0.033] | 1 | 3 | 56 | 60 |
| r_precision | -0.057 | [-0.144, 0.025] | 7 | 11 | 42 | 60 |
| mrr | -0.046 | [-0.124, 0.033] | 12 | 15 | 33 | 60 |

### emb:text-embedding-3-small:name_desc_server - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.013 | [-0.079, 0.050] | 8 | 8 | 44 | 60 |
| full_coverage@5 | -0.033 | [-0.117, 0.050] | 2 | 4 | 54 | 60 |
| r_precision | -0.083 | [-0.174, 0.003] | 8 | 12 | 40 | 60 |
| mrr | -0.077 | [-0.165, 0.013] | 13 | 18 | 29 | 60 |

### emb:text-embedding-3-small:name_desc_server - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.010 | [-0.075, 0.050] | 7 | 7 | 46 | 60 |
| full_coverage@5 | -0.017 | [-0.083, 0.050] | 2 | 3 | 55 | 60 |
| r_precision | -0.078 | [-0.161, 0.001] | 7 | 12 | 41 | 60 |
| mrr | -0.074 | [-0.148, -0.001] | 10 | 18 | 32 | 60 |

### emb:text-embedding-3-small:name_desc_server - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.026 | [-0.103, 0.054] | 6 | 12 | 42 | 60 |
| full_coverage@5 | -0.067 | [-0.167, 0.033] | 3 | 7 | 50 | 60 |
| r_precision | -0.257 | [-0.353, -0.159] | 2 | 31 | 25 | 58 |
| mrr | -0.114 | [-0.213, -0.013] | 10 | 22 | 28 | 60 |

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

### emb:text-embedding-3-small:name_desc_server - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.119 | [-0.222, -0.014] | 7 | 25 | 28 | 60 |
| full_coverage@5 | -0.167 | [-0.300, -0.033] | 4 | 14 | 42 | 60 |
| r_precision | -0.277 | [-0.394, -0.158] | 5 | 33 | 22 | 60 |
| mrr | -0.169 | [-0.294, -0.043] | 11 | 25 | 24 | 60 |

### emb:text-embedding-3-small:name_desc_server - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.141 | [-0.251, -0.029] | 8 | 26 | 26 | 60 |
| full_coverage@5 | -0.150 | [-0.283, -0.017] | 5 | 14 | 41 | 60 |
| r_precision | -0.290 | [-0.408, -0.174] | 5 | 35 | 20 | 60 |
| mrr | -0.169 | [-0.293, -0.042] | 11 | 27 | 22 | 60 |

### emb:text-embedding-3-small:name_desc_server - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.132 | [-0.236, -0.031] | 6 | 20 | 34 | 60 |
| full_coverage@5 | -0.133 | [-0.250, -0.017] | 3 | 11 | 46 | 60 |
| r_precision | -0.226 | [-0.349, -0.097] | 8 | 33 | 19 | 60 |
| mrr | -0.163 | [-0.286, -0.044] | 12 | 26 | 22 | 60 |

### emb:text-embedding-3-small:name_desc_server - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.121 | [-0.237, -0.007] | 8 | 24 | 28 | 60 |
| full_coverage@5 | -0.117 | [-0.250, 0.017] | 5 | 12 | 43 | 60 |
| r_precision | -0.238 | [-0.359, -0.112] | 8 | 35 | 17 | 60 |
| mrr | -0.124 | [-0.252, 0.001] | 12 | 26 | 22 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.090 | [-0.018, 0.201] | 19 | 9 | 32 | 60 |
| full_coverage@5 | 0.067 | [-0.050, 0.183] | 9 | 5 | 46 | 60 |
| r_precision | 0.366 | [0.253, 0.480] | 36 | 5 | 17 | 58 |
| mrr | 0.215 | [0.087, 0.342] | 27 | 9 | 24 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.129 | [0.025, 0.235] | 23 | 6 | 31 | 60 |
| full_coverage@5 | 0.117 | [0.000, 0.233] | 10 | 3 | 47 | 60 |
| r_precision | 0.348 | [0.234, 0.458] | 35 | 5 | 18 | 58 |
| mrr | 0.228 | [0.092, 0.363] | 28 | 11 | 21 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.131 | [0.015, 0.246] | 22 | 8 | 30 | 60 |
| full_coverage@5 | 0.100 | [-0.033, 0.233] | 11 | 5 | 44 | 60 |
| r_precision | 0.415 | [0.305, 0.526] | 38 | 3 | 17 | 58 |
| mrr | 0.275 | [0.145, 0.402] | 30 | 8 | 22 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.019 | [-0.071, 0.104] | 13 | 7 | 40 | 60 |
| full_coverage@5 | 0.033 | [-0.067, 0.133] | 6 | 4 | 50 | 60 |
| r_precision | 0.198 | [0.105, 0.290] | 26 | 4 | 28 | 58 |
| mrr | 0.068 | [-0.030, 0.165] | 15 | 9 | 36 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.014 | [-0.074, 0.094] | 14 | 8 | 38 | 60 |
| full_coverage@5 | 0.033 | [-0.067, 0.133] | 6 | 4 | 50 | 60 |
| r_precision | 0.171 | [0.073, 0.266] | 27 | 7 | 24 | 58 |
| mrr | 0.037 | [-0.059, 0.130] | 14 | 12 | 34 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.017 | [-0.068, 0.093] | 12 | 6 | 42 | 60 |
| full_coverage@5 | 0.050 | [-0.050, 0.150] | 6 | 3 | 51 | 60 |
| r_precision | 0.177 | [0.093, 0.259] | 26 | 4 | 28 | 58 |
| mrr | 0.040 | [-0.046, 0.124] | 14 | 12 | 34 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.026 | [-0.054, 0.103] | 12 | 6 | 42 | 60 |
| full_coverage@5 | 0.067 | [-0.033, 0.167] | 7 | 3 | 50 | 60 |
| r_precision | 0.257 | [0.159, 0.353] | 31 | 2 | 25 | 58 |
| mrr | 0.114 | [0.013, 0.213] | 22 | 10 | 28 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.056 | [-0.166, 0.058] | 11 | 19 | 30 | 60 |
| full_coverage@5 | -0.050 | [-0.167, 0.083] | 6 | 9 | 45 | 60 |
| r_precision | 0.006 | [-0.109, 0.121] | 14 | 13 | 29 | 56 |
| mrr | 0.002 | [-0.126, 0.129] | 13 | 11 | 36 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.094 | [-0.200, 0.012] | 7 | 17 | 36 | 60 |
| full_coverage@5 | -0.117 | [-0.250, 0.000] | 4 | 11 | 45 | 60 |
| r_precision | 0.037 | [-0.057, 0.132] | 13 | 11 | 33 | 57 |
| mrr | 0.024 | [-0.090, 0.139] | 13 | 11 | 36 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.092 | [-0.185, 0.002] | 6 | 20 | 34 | 60 |
| full_coverage@5 | -0.100 | [-0.217, 0.017] | 4 | 10 | 46 | 60 |
| r_precision | 0.005 | [-0.087, 0.097] | 10 | 10 | 38 | 58 |
| mrr | -0.055 | [-0.162, 0.050] | 7 | 13 | 40 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.114 | [-0.215, -0.010] | 6 | 20 | 34 | 60 |
| full_coverage@5 | -0.083 | [-0.217, 0.033] | 5 | 10 | 45 | 60 |
| r_precision | -0.017 | [-0.115, 0.082] | 11 | 12 | 35 | 58 |
| mrr | -0.055 | [-0.169, 0.056] | 9 | 12 | 39 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.106 | [-0.205, -0.007] | 8 | 20 | 32 | 60 |
| full_coverage@5 | -0.067 | [-0.183, 0.050] | 5 | 9 | 46 | 60 |
| r_precision | 0.049 | [-0.056, 0.158] | 12 | 14 | 32 | 58 |
| mrr | -0.049 | [-0.153, 0.054] | 9 | 15 | 36 | 60 |

### emb_rerank:gpt-6-luna:raw:n20 - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.095 | [-0.204, 0.021] | 6 | 22 | 32 | 60 |
| full_coverage@5 | -0.050 | [-0.183, 0.067] | 6 | 9 | 45 | 60 |
| r_precision | 0.037 | [-0.064, 0.141] | 14 | 15 | 29 | 58 |
| mrr | -0.010 | [-0.130, 0.111] | 11 | 15 | 34 | 60 |

### full_catalog:gpt-6-luna - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.146 | [0.016, 0.271] | 26 | 7 | 27 | 60 |
| full_coverage@5 | 0.117 | [-0.017, 0.250] | 13 | 6 | 41 | 60 |
| r_precision | 0.378 | [0.259, 0.497] | 36 | 5 | 17 | 58 |
| mrr | 0.212 | [0.071, 0.350] | 29 | 11 | 20 | 60 |

### full_catalog:gpt-6-luna - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.185 | [0.057, 0.305] | 31 | 7 | 22 | 60 |
| full_coverage@5 | 0.167 | [0.033, 0.300] | 15 | 5 | 40 | 60 |
| r_precision | 0.359 | [0.233, 0.483] | 36 | 5 | 17 | 58 |
| mrr | 0.226 | [0.076, 0.372] | 30 | 10 | 20 | 60 |

### full_catalog:gpt-6-luna - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.187 | [0.044, 0.321] | 31 | 9 | 20 | 60 |
| full_coverage@5 | 0.150 | [0.000, 0.300] | 15 | 6 | 39 | 60 |
| r_precision | 0.427 | [0.297, 0.550] | 40 | 6 | 12 | 58 |
| mrr | 0.273 | [0.115, 0.421] | 34 | 11 | 15 | 60 |

### full_catalog:gpt-6-luna - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.076 | [-0.065, 0.208] | 24 | 11 | 25 | 60 |
| full_coverage@5 | 0.083 | [-0.067, 0.233] | 13 | 8 | 39 | 60 |
| r_precision | 0.227 | [0.101, 0.349] | 31 | 8 | 19 | 58 |
| mrr | 0.066 | [-0.081, 0.212] | 20 | 16 | 24 | 60 |

### full_catalog:gpt-6-luna - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.070 | [-0.068, 0.203] | 22 | 12 | 26 | 60 |
| full_coverage@5 | 0.083 | [-0.050, 0.217] | 12 | 7 | 41 | 60 |
| r_precision | 0.200 | [0.063, 0.335] | 30 | 11 | 17 | 58 |
| mrr | 0.035 | [-0.122, 0.189] | 19 | 18 | 23 | 60 |

### full_catalog:gpt-6-luna - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.073 | [-0.065, 0.203] | 22 | 11 | 27 | 60 |
| full_coverage@5 | 0.100 | [-0.050, 0.233] | 13 | 7 | 40 | 60 |
| r_precision | 0.205 | [0.079, 0.332] | 29 | 8 | 21 | 58 |
| mrr | 0.037 | [-0.109, 0.180] | 18 | 16 | 26 | 60 |

### full_catalog:gpt-6-luna - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.083 | [-0.045, 0.203] | 25 | 11 | 24 | 60 |
| full_coverage@5 | 0.117 | [-0.017, 0.250] | 13 | 6 | 41 | 60 |
| r_precision | 0.269 | [0.141, 0.395] | 32 | 7 | 19 | 58 |
| mrr | 0.112 | [-0.032, 0.250] | 24 | 14 | 22 | 60 |

### full_catalog:gpt-6-luna - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.056 | [-0.058, 0.166] | 19 | 11 | 30 | 60 |
| full_coverage@5 | 0.050 | [-0.083, 0.167] | 9 | 6 | 45 | 60 |
| r_precision | -0.006 | [-0.121, 0.109] | 13 | 14 | 29 | 56 |
| mrr | -0.002 | [-0.129, 0.126] | 11 | 13 | 36 | 60 |

### full_catalog:gpt-6-luna - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.037 | [-0.114, 0.039] | 4 | 10 | 46 | 60 |
| full_coverage@5 | -0.067 | [-0.167, 0.033] | 3 | 7 | 50 | 60 |
| r_precision | 0.049 | [-0.016, 0.124] | 8 | 7 | 42 | 57 |
| mrr | 0.022 | [-0.060, 0.103] | 8 | 8 | 44 | 60 |

### full_catalog:gpt-6-luna - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.036 | [-0.121, 0.049] | 5 | 11 | 44 | 60 |
| full_coverage@5 | -0.050 | [-0.167, 0.067] | 5 | 8 | 47 | 60 |
| r_precision | -0.001 | [-0.084, 0.086] | 7 | 10 | 41 | 58 |
| mrr | -0.057 | [-0.145, 0.026] | 5 | 10 | 45 | 60 |

### full_catalog:gpt-6-luna - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.058 | [-0.132, 0.014] | 4 | 11 | 45 | 60 |
| full_coverage@5 | -0.033 | [-0.133, 0.050] | 3 | 5 | 52 | 60 |
| r_precision | -0.014 | [-0.096, 0.068] | 7 | 10 | 41 | 58 |
| mrr | -0.057 | [-0.142, 0.022] | 5 | 8 | 47 | 60 |

### full_catalog:gpt-6-luna - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.050 | [-0.162, 0.057] | 10 | 16 | 34 | 60 |
| full_coverage@5 | -0.017 | [-0.150, 0.100] | 7 | 8 | 45 | 60 |
| r_precision | 0.052 | [-0.046, 0.154] | 11 | 10 | 37 | 58 |
| mrr | -0.051 | [-0.157, 0.056] | 8 | 15 | 37 | 60 |

### full_catalog:gpt-6-luna - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.039 | [-0.154, 0.074] | 11 | 16 | 33 | 60 |
| full_coverage@5 | 0.000 | [-0.133, 0.133] | 9 | 9 | 42 | 60 |
| r_precision | 0.040 | [-0.057, 0.140] | 12 | 11 | 35 | 58 |
| mrr | -0.012 | [-0.123, 0.097] | 11 | 12 | 37 | 60 |

### full_catalog:gpt-6-luna:run2 - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.184 | [0.058, 0.304] | 28 | 6 | 26 | 60 |
| full_coverage@5 | 0.183 | [0.050, 0.317] | 16 | 5 | 39 | 60 |
| r_precision | 0.341 | [0.215, 0.469] | 34 | 8 | 17 | 59 |
| mrr | 0.190 | [0.049, 0.331] | 28 | 14 | 18 | 60 |

### full_catalog:gpt-6-luna:run2 - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.223 | [0.101, 0.343] | 33 | 6 | 21 | 60 |
| full_coverage@5 | 0.233 | [0.100, 0.367] | 18 | 4 | 38 | 60 |
| r_precision | 0.323 | [0.195, 0.451] | 33 | 7 | 19 | 59 |
| mrr | 0.204 | [0.058, 0.349] | 28 | 12 | 20 | 60 |

### full_catalog:gpt-6-luna:run2 - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.224 | [0.089, 0.354] | 31 | 7 | 22 | 60 |
| full_coverage@5 | 0.217 | [0.067, 0.367] | 18 | 5 | 37 | 60 |
| r_precision | 0.406 | [0.284, 0.530] | 37 | 6 | 16 | 59 |
| mrr | 0.251 | [0.103, 0.396] | 33 | 13 | 14 | 60 |

### full_catalog:gpt-6-luna:run2 - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.113 | [-0.018, 0.240] | 24 | 9 | 27 | 60 |
| full_coverage@5 | 0.150 | [0.000, 0.300] | 15 | 6 | 39 | 60 |
| r_precision | 0.176 | [0.048, 0.302] | 28 | 11 | 20 | 59 |
| mrr | 0.044 | [-0.092, 0.181] | 18 | 18 | 24 | 60 |

### full_catalog:gpt-6-luna:run2 - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.107 | [-0.021, 0.233] | 23 | 10 | 27 | 60 |
| full_coverage@5 | 0.150 | [0.017, 0.283] | 14 | 5 | 41 | 60 |
| r_precision | 0.166 | [0.039, 0.293] | 27 | 12 | 20 | 59 |
| mrr | 0.013 | [-0.134, 0.156] | 18 | 19 | 23 | 60 |

### full_catalog:gpt-6-luna:run2 - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.110 | [-0.015, 0.234] | 23 | 9 | 28 | 60 |
| full_coverage@5 | 0.167 | [0.033, 0.300] | 15 | 5 | 40 | 60 |
| r_precision | 0.171 | [0.055, 0.290] | 26 | 9 | 24 | 59 |
| mrr | 0.015 | [-0.121, 0.151] | 17 | 19 | 24 | 60 |

### full_catalog:gpt-6-luna:run2 - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.120 | [0.005, 0.232] | 24 | 8 | 28 | 60 |
| full_coverage@5 | 0.183 | [0.050, 0.317] | 15 | 4 | 41 | 60 |
| r_precision | 0.251 | [0.125, 0.373] | 31 | 8 | 20 | 59 |
| mrr | 0.090 | [-0.042, 0.220] | 23 | 14 | 23 | 60 |

### full_catalog:gpt-6-luna:run2 - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.094 | [-0.012, 0.200] | 17 | 7 | 36 | 60 |
| full_coverage@5 | 0.117 | [0.000, 0.250] | 11 | 4 | 45 | 60 |
| r_precision | -0.037 | [-0.132, 0.057] | 11 | 13 | 33 | 57 |
| mrr | -0.024 | [-0.139, 0.090] | 11 | 13 | 36 | 60 |

### full_catalog:gpt-6-luna:run2 - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.037 | [-0.039, 0.114] | 10 | 4 | 46 | 60 |
| full_coverage@5 | 0.067 | [-0.033, 0.167] | 7 | 3 | 50 | 60 |
| r_precision | -0.049 | [-0.124, 0.016] | 7 | 8 | 42 | 57 |
| mrr | -0.022 | [-0.103, 0.060] | 8 | 8 | 44 | 60 |

### full_catalog:gpt-6-luna:run2 - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.001 | [-0.043, 0.049] | 4 | 5 | 51 | 60 |
| full_coverage@5 | 0.017 | [-0.050, 0.083] | 3 | 2 | 55 | 60 |
| r_precision | -0.048 | [-0.114, 0.013] | 3 | 7 | 49 | 59 |
| mrr | -0.079 | [-0.142, -0.028] | 2 | 9 | 49 | 60 |

### full_catalog:gpt-6-luna:run2 - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.021 | [-0.083, 0.037] | 4 | 5 | 51 | 60 |
| full_coverage@5 | 0.033 | [-0.050, 0.117] | 4 | 2 | 54 | 60 |
| r_precision | -0.062 | [-0.144, 0.015] | 4 | 10 | 45 | 59 |
| mrr | -0.079 | [-0.155, -0.011] | 4 | 10 | 46 | 60 |

### full_catalog:gpt-6-luna:run2 - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.013 | [-0.101, 0.072] | 10 | 10 | 40 | 60 |
| full_coverage@5 | 0.050 | [-0.050, 0.150] | 6 | 3 | 51 | 60 |
| r_precision | 0.003 | [-0.090, 0.097] | 12 | 10 | 37 | 59 |
| mrr | -0.073 | [-0.157, 0.009] | 7 | 14 | 39 | 60 |

### full_catalog:gpt-6-luna:run2 - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.001 | [-0.094, 0.087] | 11 | 12 | 37 | 60 |
| full_coverage@5 | 0.067 | [-0.050, 0.183] | 9 | 5 | 46 | 60 |
| r_precision | -0.008 | [-0.097, 0.082] | 10 | 10 | 39 | 59 |
| mrr | -0.035 | [-0.124, 0.053] | 7 | 10 | 43 | 60 |

### full_catalog_cards:gpt-6-luna - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.182 | [0.066, 0.292] | 29 | 5 | 26 | 60 |
| full_coverage@5 | 0.167 | [0.033, 0.300] | 15 | 5 | 40 | 60 |
| r_precision | 0.383 | [0.271, 0.496] | 38 | 5 | 17 | 60 |
| mrr | 0.269 | [0.140, 0.399] | 32 | 9 | 19 | 60 |

### full_catalog_cards:gpt-6-luna - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.221 | [0.104, 0.331] | 32 | 4 | 24 | 60 |
| full_coverage@5 | 0.217 | [0.083, 0.350] | 17 | 4 | 39 | 60 |
| r_precision | 0.364 | [0.242, 0.487] | 38 | 5 | 17 | 60 |
| mrr | 0.283 | [0.145, 0.418] | 32 | 9 | 19 | 60 |

### full_catalog_cards:gpt-6-luna - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.223 | [0.094, 0.346] | 32 | 6 | 22 | 60 |
| full_coverage@5 | 0.200 | [0.050, 0.350] | 17 | 5 | 38 | 60 |
| r_precision | 0.430 | [0.306, 0.553] | 41 | 5 | 14 | 60 |
| mrr | 0.330 | [0.184, 0.475] | 36 | 10 | 14 | 60 |

### full_catalog_cards:gpt-6-luna - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.112 | [-0.010, 0.228] | 23 | 8 | 29 | 60 |
| full_coverage@5 | 0.133 | [0.000, 0.283] | 14 | 6 | 40 | 60 |
| r_precision | 0.220 | [0.107, 0.331] | 30 | 6 | 24 | 60 |
| mrr | 0.123 | [-0.001, 0.248] | 19 | 13 | 28 | 60 |

### full_catalog_cards:gpt-6-luna - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.106 | [-0.013, 0.220] | 23 | 8 | 29 | 60 |
| full_coverage@5 | 0.133 | [0.000, 0.267] | 13 | 5 | 42 | 60 |
| r_precision | 0.194 | [0.068, 0.317] | 29 | 10 | 21 | 60 |
| mrr | 0.092 | [-0.049, 0.230] | 20 | 15 | 25 | 60 |

### full_catalog_cards:gpt-6-luna - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.109 | [-0.008, 0.221] | 23 | 7 | 30 | 60 |
| full_coverage@5 | 0.150 | [0.017, 0.283] | 14 | 5 | 41 | 60 |
| r_precision | 0.199 | [0.086, 0.314] | 28 | 7 | 25 | 60 |
| mrr | 0.094 | [-0.036, 0.225] | 20 | 16 | 24 | 60 |

### full_catalog_cards:gpt-6-luna - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.119 | [0.014, 0.222] | 25 | 7 | 28 | 60 |
| full_coverage@5 | 0.167 | [0.033, 0.300] | 14 | 4 | 42 | 60 |
| r_precision | 0.277 | [0.158, 0.394] | 33 | 5 | 22 | 60 |
| mrr | 0.169 | [0.043, 0.294] | 25 | 11 | 24 | 60 |

### full_catalog_cards:gpt-6-luna - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.092 | [-0.002, 0.185] | 20 | 6 | 34 | 60 |
| full_coverage@5 | 0.100 | [-0.017, 0.217] | 10 | 4 | 46 | 60 |
| r_precision | -0.005 | [-0.097, 0.087] | 10 | 10 | 38 | 58 |
| mrr | 0.055 | [-0.050, 0.162] | 13 | 7 | 40 | 60 |

### full_catalog_cards:gpt-6-luna - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.036 | [-0.049, 0.121] | 11 | 5 | 44 | 60 |
| full_coverage@5 | 0.050 | [-0.067, 0.167] | 8 | 5 | 47 | 60 |
| r_precision | 0.001 | [-0.086, 0.084] | 10 | 7 | 41 | 58 |
| mrr | 0.057 | [-0.026, 0.145] | 10 | 5 | 45 | 60 |

### full_catalog_cards:gpt-6-luna - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.001 | [-0.049, 0.043] | 5 | 4 | 51 | 60 |
| full_coverage@5 | -0.017 | [-0.083, 0.050] | 2 | 3 | 55 | 60 |
| r_precision | 0.048 | [-0.013, 0.114] | 7 | 3 | 49 | 59 |
| mrr | 0.079 | [0.028, 0.142] | 9 | 2 | 49 | 60 |

### full_catalog_cards:gpt-6-luna - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.022 | [-0.078, 0.032] | 4 | 6 | 50 | 60 |
| full_coverage@5 | 0.017 | [-0.067, 0.100] | 4 | 3 | 53 | 60 |
| r_precision | -0.013 | [-0.068, 0.036] | 4 | 6 | 50 | 60 |
| mrr | 0.000 | [-0.050, 0.044] | 5 | 3 | 52 | 60 |

### full_catalog_cards:gpt-6-luna - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.014 | [-0.094, 0.060] | 9 | 8 | 43 | 60 |
| full_coverage@5 | 0.033 | [-0.067, 0.133] | 5 | 3 | 52 | 60 |
| r_precision | 0.051 | [-0.017, 0.123] | 11 | 7 | 42 | 60 |
| mrr | 0.006 | [-0.055, 0.070] | 8 | 8 | 44 | 60 |

### full_catalog_cards:gpt-6-luna - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.003 | [-0.090, 0.082] | 9 | 10 | 41 | 60 |
| full_coverage@5 | 0.050 | [-0.067, 0.167] | 7 | 4 | 49 | 60 |
| r_precision | 0.039 | [-0.026, 0.110] | 10 | 8 | 42 | 60 |
| mrr | 0.044 | [-0.017, 0.111] | 8 | 5 | 47 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.205 | [0.094, 0.310] | 28 | 4 | 28 | 60 |
| full_coverage@5 | 0.150 | [0.017, 0.283] | 13 | 4 | 43 | 60 |
| r_precision | 0.396 | [0.282, 0.510] | 39 | 6 | 15 | 60 |
| mrr | 0.269 | [0.142, 0.395] | 32 | 8 | 20 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.244 | [0.135, 0.342] | 35 | 3 | 22 | 60 |
| full_coverage@5 | 0.200 | [0.067, 0.333] | 15 | 3 | 42 | 60 |
| r_precision | 0.378 | [0.253, 0.499] | 39 | 6 | 15 | 60 |
| mrr | 0.283 | [0.149, 0.413] | 32 | 8 | 20 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.245 | [0.117, 0.365] | 30 | 6 | 24 | 60 |
| full_coverage@5 | 0.183 | [0.050, 0.317] | 15 | 4 | 41 | 60 |
| r_precision | 0.443 | [0.317, 0.565] | 41 | 5 | 14 | 60 |
| mrr | 0.330 | [0.184, 0.471] | 36 | 9 | 15 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.134 | [0.005, 0.256] | 24 | 8 | 28 | 60 |
| full_coverage@5 | 0.117 | [-0.017, 0.250] | 13 | 6 | 41 | 60 |
| r_precision | 0.233 | [0.119, 0.342] | 30 | 5 | 25 | 60 |
| mrr | 0.123 | [-0.000, 0.246] | 19 | 12 | 29 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.128 | [0.003, 0.246] | 25 | 8 | 27 | 60 |
| full_coverage@5 | 0.117 | [-0.017, 0.250] | 12 | 5 | 43 | 60 |
| r_precision | 0.207 | [0.079, 0.331] | 31 | 11 | 18 | 60 |
| mrr | 0.092 | [-0.049, 0.229] | 20 | 14 | 26 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.131 | [0.007, 0.246] | 25 | 7 | 28 | 60 |
| full_coverage@5 | 0.133 | [0.000, 0.267] | 13 | 5 | 42 | 60 |
| r_precision | 0.212 | [0.096, 0.326] | 30 | 8 | 22 | 60 |
| mrr | 0.094 | [-0.034, 0.221] | 20 | 13 | 27 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.141 | [0.029, 0.251] | 26 | 8 | 26 | 60 |
| full_coverage@5 | 0.150 | [0.017, 0.283] | 14 | 5 | 41 | 60 |
| r_precision | 0.290 | [0.174, 0.408] | 35 | 5 | 20 | 60 |
| mrr | 0.169 | [0.042, 0.293] | 27 | 11 | 22 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.114 | [0.010, 0.215] | 20 | 6 | 34 | 60 |
| full_coverage@5 | 0.083 | [-0.033, 0.217] | 10 | 5 | 45 | 60 |
| r_precision | 0.017 | [-0.082, 0.115] | 12 | 11 | 35 | 58 |
| mrr | 0.055 | [-0.056, 0.169] | 12 | 9 | 39 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.058 | [-0.014, 0.132] | 11 | 4 | 45 | 60 |
| full_coverage@5 | 0.033 | [-0.050, 0.133] | 5 | 3 | 52 | 60 |
| r_precision | 0.014 | [-0.068, 0.096] | 10 | 7 | 41 | 58 |
| mrr | 0.057 | [-0.022, 0.142] | 8 | 5 | 47 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.021 | [-0.037, 0.083] | 5 | 4 | 51 | 60 |
| full_coverage@5 | -0.033 | [-0.117, 0.050] | 2 | 4 | 54 | 60 |
| r_precision | 0.062 | [-0.015, 0.144] | 10 | 4 | 45 | 59 |
| mrr | 0.079 | [0.011, 0.155] | 10 | 4 | 46 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.022 | [-0.032, 0.078] | 6 | 4 | 50 | 60 |
| full_coverage@5 | -0.017 | [-0.100, 0.067] | 3 | 4 | 53 | 60 |
| r_precision | 0.013 | [-0.036, 0.068] | 6 | 4 | 50 | 60 |
| mrr | 0.000 | [-0.044, 0.050] | 3 | 5 | 52 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.008 | [-0.076, 0.087] | 12 | 8 | 40 | 60 |
| full_coverage@5 | 0.017 | [-0.083, 0.117] | 5 | 4 | 51 | 60 |
| r_precision | 0.064 | [-0.011, 0.143] | 13 | 8 | 39 | 60 |
| mrr | 0.006 | [-0.069, 0.085] | 9 | 12 | 39 | 60 |

### full_catalog_cards:gpt-6-luna:run2 - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.019 | [-0.069, 0.107] | 11 | 10 | 39 | 60 |
| full_coverage@5 | 0.033 | [-0.083, 0.150] | 8 | 6 | 46 | 60 |
| r_precision | 0.052 | [-0.022, 0.131] | 12 | 7 | 41 | 60 |
| mrr | 0.044 | [-0.034, 0.127] | 10 | 9 | 41 | 60 |

### router:domain - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.196 | [0.080, 0.313] | 29 | 7 | 24 | 60 |
| full_coverage@5 | 0.133 | [0.000, 0.267] | 13 | 5 | 42 | 60 |
| r_precision | 0.332 | [0.229, 0.439] | 35 | 4 | 21 | 60 |
| mrr | 0.263 | [0.138, 0.388] | 31 | 7 | 22 | 60 |

### router:domain - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.235 | [0.119, 0.346] | 33 | 5 | 22 | 60 |
| full_coverage@5 | 0.183 | [0.050, 0.317] | 15 | 4 | 41 | 60 |
| r_precision | 0.314 | [0.201, 0.425] | 36 | 4 | 20 | 60 |
| mrr | 0.277 | [0.141, 0.412] | 32 | 9 | 19 | 60 |

### router:domain - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.237 | [0.114, 0.359] | 29 | 5 | 26 | 60 |
| full_coverage@5 | 0.167 | [0.033, 0.300] | 14 | 4 | 42 | 60 |
| r_precision | 0.379 | [0.261, 0.494] | 39 | 5 | 16 | 60 |
| mrr | 0.324 | [0.196, 0.449] | 36 | 7 | 17 | 60 |

### router:domain - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.126 | [0.016, 0.235] | 22 | 8 | 30 | 60 |
| full_coverage@5 | 0.100 | [-0.017, 0.217] | 10 | 4 | 46 | 60 |
| r_precision | 0.169 | [0.053, 0.279] | 31 | 9 | 20 | 60 |
| mrr | 0.117 | [-0.002, 0.239] | 21 | 12 | 27 | 60 |

### router:domain - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.120 | [0.019, 0.222] | 19 | 7 | 34 | 60 |
| full_coverage@5 | 0.100 | [-0.000, 0.217] | 9 | 3 | 48 | 60 |
| r_precision | 0.143 | [0.024, 0.258] | 28 | 11 | 21 | 60 |
| mrr | 0.086 | [-0.042, 0.217] | 19 | 16 | 25 | 60 |

### router:domain - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.123 | [0.025, 0.220] | 20 | 6 | 34 | 60 |
| full_coverage@5 | 0.117 | [0.000, 0.233] | 10 | 3 | 47 | 60 |
| r_precision | 0.149 | [0.036, 0.257] | 28 | 9 | 23 | 60 |
| mrr | 0.088 | [-0.029, 0.208] | 19 | 16 | 25 | 60 |

### router:domain - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.132 | [0.031, 0.236] | 20 | 6 | 34 | 60 |
| full_coverage@5 | 0.133 | [0.017, 0.250] | 11 | 3 | 46 | 60 |
| r_precision | 0.226 | [0.097, 0.349] | 33 | 8 | 19 | 60 |
| mrr | 0.163 | [0.044, 0.286] | 26 | 12 | 22 | 60 |

### router:domain - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.106 | [0.007, 0.205] | 20 | 8 | 32 | 60 |
| full_coverage@5 | 0.067 | [-0.050, 0.183] | 9 | 5 | 46 | 60 |
| r_precision | -0.049 | [-0.158, 0.056] | 14 | 12 | 32 | 58 |
| mrr | 0.049 | [-0.054, 0.153] | 15 | 9 | 36 | 60 |

### router:domain - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.050 | [-0.057, 0.162] | 16 | 10 | 34 | 60 |
| full_coverage@5 | 0.017 | [-0.100, 0.150] | 8 | 7 | 45 | 60 |
| r_precision | -0.052 | [-0.154, 0.046] | 10 | 11 | 37 | 58 |
| mrr | 0.051 | [-0.056, 0.157] | 15 | 8 | 37 | 60 |

### router:domain - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.013 | [-0.072, 0.101] | 10 | 10 | 40 | 60 |
| full_coverage@5 | -0.050 | [-0.150, 0.050] | 3 | 6 | 51 | 60 |
| r_precision | -0.003 | [-0.097, 0.090] | 10 | 12 | 37 | 59 |
| mrr | 0.073 | [-0.009, 0.157] | 14 | 7 | 39 | 60 |

### router:domain - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.014 | [-0.060, 0.094] | 8 | 9 | 43 | 60 |
| full_coverage@5 | -0.033 | [-0.133, 0.067] | 3 | 5 | 52 | 60 |
| r_precision | -0.051 | [-0.123, 0.017] | 7 | 11 | 42 | 60 |
| mrr | -0.006 | [-0.070, 0.055] | 8 | 8 | 44 | 60 |

### router:domain - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.008 | [-0.087, 0.076] | 8 | 12 | 40 | 60 |
| full_coverage@5 | -0.017 | [-0.117, 0.083] | 4 | 5 | 51 | 60 |
| r_precision | -0.064 | [-0.143, 0.011] | 8 | 13 | 39 | 60 |
| mrr | -0.006 | [-0.085, 0.069] | 12 | 9 | 39 | 60 |

### router:domain - router:server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.011 | [-0.067, 0.092] | 9 | 10 | 41 | 60 |
| full_coverage@5 | 0.017 | [-0.083, 0.117] | 5 | 4 | 51 | 60 |
| r_precision | -0.012 | [-0.079, 0.056] | 8 | 10 | 42 | 60 |
| mrr | 0.038 | [-0.014, 0.099] | 8 | 5 | 47 | 60 |

### router:server - bm25:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.185 | [0.068, 0.303] | 26 | 6 | 28 | 60 |
| full_coverage@5 | 0.117 | [-0.017, 0.250] | 12 | 5 | 43 | 60 |
| r_precision | 0.344 | [0.247, 0.443] | 37 | 2 | 21 | 60 |
| mrr | 0.225 | [0.100, 0.354] | 28 | 11 | 21 | 60 |

### router:server - bm25:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.224 | [0.108, 0.338] | 31 | 5 | 24 | 60 |
| full_coverage@5 | 0.167 | [0.033, 0.300] | 14 | 4 | 42 | 60 |
| r_precision | 0.326 | [0.212, 0.437] | 37 | 5 | 18 | 60 |
| mrr | 0.238 | [0.097, 0.379] | 29 | 12 | 19 | 60 |

### router:server - bm25:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.226 | [0.095, 0.353] | 31 | 6 | 23 | 60 |
| full_coverage@5 | 0.150 | [0.017, 0.283] | 14 | 5 | 41 | 60 |
| r_precision | 0.391 | [0.281, 0.499] | 41 | 3 | 16 | 60 |
| mrr | 0.285 | [0.154, 0.418] | 34 | 10 | 16 | 60 |

### router:server - emb:text-embedding-3-small:enriched_raw_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.114 | [0.002, 0.226] | 23 | 8 | 29 | 60 |
| full_coverage@5 | 0.083 | [-0.033, 0.217] | 10 | 5 | 45 | 60 |
| r_precision | 0.181 | [0.071, 0.287] | 32 | 8 | 20 | 60 |
| mrr | 0.079 | [-0.047, 0.205] | 19 | 16 | 25 | 60 |

### router:server - emb:text-embedding-3-small:enriched_tag

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.109 | [0.001, 0.215] | 21 | 8 | 31 | 60 |
| full_coverage@5 | 0.083 | [-0.033, 0.200] | 9 | 4 | 47 | 60 |
| r_precision | 0.155 | [0.035, 0.270] | 29 | 11 | 20 | 60 |
| mrr | 0.047 | [-0.090, 0.184] | 19 | 18 | 23 | 60 |

### router:server - emb:text-embedding-3-small:enriched_tag_topic

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.112 | [0.006, 0.216] | 22 | 7 | 31 | 60 |
| full_coverage@5 | 0.100 | [-0.017, 0.217] | 10 | 4 | 46 | 60 |
| r_precision | 0.160 | [0.050, 0.266] | 29 | 7 | 24 | 60 |
| mrr | 0.050 | [-0.078, 0.180] | 17 | 18 | 25 | 60 |

### router:server - emb:text-embedding-3-small:name_desc_server

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.121 | [0.007, 0.237] | 24 | 8 | 28 | 60 |
| full_coverage@5 | 0.117 | [-0.017, 0.250] | 12 | 5 | 43 | 60 |
| r_precision | 0.238 | [0.112, 0.359] | 35 | 8 | 17 | 60 |
| mrr | 0.124 | [-0.001, 0.252] | 26 | 12 | 22 | 60 |

### router:server - emb_rerank:gpt-6-luna:raw:n20

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.095 | [-0.021, 0.204] | 22 | 6 | 32 | 60 |
| full_coverage@5 | 0.050 | [-0.067, 0.183] | 9 | 6 | 45 | 60 |
| r_precision | -0.037 | [-0.141, 0.064] | 15 | 14 | 29 | 58 |
| mrr | 0.010 | [-0.111, 0.130] | 15 | 11 | 34 | 60 |

### router:server - full_catalog:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.039 | [-0.074, 0.154] | 16 | 11 | 33 | 60 |
| full_coverage@5 | 0.000 | [-0.133, 0.133] | 9 | 9 | 42 | 60 |
| r_precision | -0.040 | [-0.140, 0.057] | 11 | 12 | 35 | 58 |
| mrr | 0.012 | [-0.097, 0.123] | 12 | 11 | 37 | 60 |

### router:server - full_catalog:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.001 | [-0.087, 0.094] | 12 | 11 | 37 | 60 |
| full_coverage@5 | -0.067 | [-0.183, 0.050] | 5 | 9 | 46 | 60 |
| r_precision | 0.008 | [-0.082, 0.097] | 10 | 10 | 39 | 59 |
| mrr | 0.035 | [-0.053, 0.124] | 10 | 7 | 43 | 60 |

### router:server - full_catalog_cards:gpt-6-luna

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | 0.003 | [-0.082, 0.090] | 10 | 9 | 41 | 60 |
| full_coverage@5 | -0.050 | [-0.167, 0.067] | 4 | 7 | 49 | 60 |
| r_precision | -0.039 | [-0.110, 0.026] | 8 | 10 | 42 | 60 |
| mrr | -0.044 | [-0.111, 0.017] | 5 | 8 | 47 | 60 |

### router:server - full_catalog_cards:gpt-6-luna:run2

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.019 | [-0.107, 0.069] | 10 | 11 | 39 | 60 |
| full_coverage@5 | -0.033 | [-0.150, 0.083] | 6 | 8 | 46 | 60 |
| r_precision | -0.052 | [-0.131, 0.022] | 7 | 12 | 41 | 60 |
| mrr | -0.044 | [-0.127, 0.034] | 9 | 10 | 41 | 60 |

### router:server - router:domain

| Metric | Mean diff | CI95 | Wins | Losses | Ties | n |
|---|---|---|---|---|---|---|
| slot_recall@5 | -0.011 | [-0.092, 0.067] | 10 | 9 | 41 | 60 |
| full_coverage@5 | -0.017 | [-0.117, 0.083] | 4 | 5 | 51 | 60 |
| r_precision | 0.012 | [-0.056, 0.079] | 10 | 8 | 42 | 60 |
| mrr | -0.038 | [-0.099, 0.014] | 5 | 8 | 47 | 60 |
