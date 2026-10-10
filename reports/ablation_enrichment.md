# Ablation: does enrichment alone help? (flat retrieval, no hierarchy)

Date: 2026-10-11. Frozen eval set, 60 queries. Retrieval is flat top-k over the 527 tools, exactly as in the baselines. Only the text being searched changes. The enrichment comes from `data/enriched/pass1_annotations.jsonl` (summary and intents written by `gpt-6-luna` from the tool documents, never from queries). Cells: mean [95% bootstrap interval]. Scores are deterministic and come from `toolprune.eval.score`.

Variants: *tag* is the summary plus the intents only. *raw + tag* is the raw document (name, description, server) followed by the tag. *tag + topic* adds the pass-1 topic label. No variant uses the effect or flags.

## Results

| System | Slot recall@5 | Full coverage@5 | R-precision | MRR |
|---|---|---|---|---|
| BM25, raw text | 0.412 [0.312, 0.512] | 0.250 [0.150, 0.367] | 0.221 [0.146, 0.301] | 0.428 [0.326, 0.533] |
| BM25, enriched tag + raw text | 0.453 [0.351, 0.554] | 0.283 [0.167, 0.400] | 0.268 [0.188, 0.354] | 0.488 [0.383, 0.592] |
| BM25, enriched tag only | 0.414 [0.318, 0.512] | 0.233 [0.133, 0.350] | 0.286 [0.200, 0.376] | 0.475 [0.365, 0.585] |
| Embeddings, raw text (baseline) | 0.517 [0.425, 0.608] | 0.283 [0.167, 0.400] | 0.374 [0.283, 0.467] | 0.589 [0.491, 0.685] |
| Embeddings, enriched tag (summary + intents) | 0.529 [0.436, 0.625] | 0.317 [0.200, 0.433] | 0.457 [0.361, 0.551] | 0.666 [0.561, 0.766] |
| Embeddings, raw text + enriched tag | 0.524 [0.429, 0.619] | 0.317 [0.200, 0.433] | 0.431 [0.335, 0.528] | 0.634 [0.528, 0.737] |
| Embeddings, enriched tag + topic | 0.526 [0.435, 0.619] | 0.300 [0.183, 0.417] | 0.451 [0.357, 0.546] | 0.663 [0.561, 0.761] |

## Paired differences against raw-text embeddings (same 60 queries)

| System | Metric | Mean diff | CI95 | Wins | Losses | Ties |
|---|---|---|---|---|---|---|
| Embeddings, enriched tag (summary + intents) | Slot recall@5 | +0.013 | [-0.050, 0.079] | 8 | 8 | 44 |
| Embeddings, enriched tag (summary + intents) | Full coverage@5 | +0.033 | [-0.050, 0.117] | 4 | 2 | 54 |
| Embeddings, enriched tag (summary + intents) | R-precision | +0.083 | [-0.003, 0.174] | 12 | 8 | 40 |
| Embeddings, enriched tag (summary + intents) | MRR | +0.077 | [-0.013, 0.165] | 18 | 13 | 29 |
| Embeddings, raw text + enriched tag | Slot recall@5 | +0.007 | [-0.040, 0.062] | 5 | 6 | 49 |
| Embeddings, raw text + enriched tag | Full coverage@5 | +0.033 | [-0.033, 0.100] | 3 | 1 | 56 |
| Embeddings, raw text + enriched tag | R-precision | +0.057 | [-0.025, 0.144] | 11 | 7 | 42 |
| Embeddings, raw text + enriched tag | MRR | +0.046 | [-0.033, 0.124] | 15 | 12 | 33 |
| Embeddings, enriched tag + topic | Slot recall@5 | +0.010 | [-0.050, 0.075] | 7 | 7 | 46 |
| Embeddings, enriched tag + topic | Full coverage@5 | +0.017 | [-0.050, 0.083] | 3 | 2 | 55 |
| Embeddings, enriched tag + topic | R-precision | +0.078 | [-0.001, 0.161] | 12 | 7 | 41 |
| Embeddings, enriched tag + topic | MRR | +0.074 | [0.001, 0.148] | 18 | 10 | 32 |

## Paired differences against raw-text BM25

| System | Metric | Mean diff | CI95 | Wins | Losses | Ties |
|---|---|---|---|---|---|---|
| BM25, enriched tag + raw text | Slot recall@5 | +0.040 | [-0.024, 0.107] | 9 | 5 | 46 |
| BM25, enriched tag + raw text | Full coverage@5 | +0.033 | [-0.033, 0.100] | 3 | 1 | 56 |
| BM25, enriched tag + raw text | R-precision | +0.047 | [-0.013, 0.104] | 11 | 4 | 45 |
| BM25, enriched tag + raw text | MRR | +0.060 | [-0.017, 0.138] | 17 | 9 | 34 |
| BM25, enriched tag only | Slot recall@5 | +0.001 | [-0.086, 0.086] | 12 | 11 | 37 |
| BM25, enriched tag only | Full coverage@5 | -0.017 | [-0.100, 0.067] | 3 | 4 | 53 |
| BM25, enriched tag only | R-precision | +0.065 | [-0.025, 0.156] | 16 | 8 | 36 |
| BM25, enriched tag only | MRR | +0.047 | [-0.051, 0.148] | 21 | 14 | 25 |

## Reading the table

- Enrichment alone gives a small gain for embeddings, mostly in how results are ordered (R-precision and MRR), not in how many slots are reached. Every paired interval includes zero except tag + topic on MRR, which only just excludes it (+0.074, [0.001, 0.148]). With 60 queries, treat this as a hint.
- The three embedding variants are within noise of each other. The tag alone does as well as raw text plus tag, so the raw definition adds nothing to the vector.
- Enriched BM25 gains a little when the raw text is kept (slot recall@5 0.412 to 0.453), and does not gain from the tag alone.
- Flat enriched embeddings stay well below the LLM-based systems (slot recall@5 about 0.60 to 0.64, R-precision about 0.61 to 0.66). So enrichment as embedding text does not close the gap. The gap is reasoning over the candidates, which is what the router adds. See `ladder` results for the LLM systems.
- This ablation answers the draft's rung 3 (enriched embeddings, no hierarchy). Cost: about 82k embedding tokens for the three variants.

