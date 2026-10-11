# ToolPrune: where the POC stands

Date: 2026-10-11. This is a summary of what was measured, what holds up, and what does not. It is not a claim of success. All numbers are from the frozen 60-query eval set unless stated, with one run per system (the full-catalog runs have two). Intervals are wide at n=60. Terms are in `glossary.md`.

## The question
Can an LLM-written tag per tool, plus a router that prunes by group, give an agent the few tools it needs with fewer tokens and fewer confusions than loading everything or using embedding search?

## What we built
- A frozen 60-query eval set (plus a 94-task natural set) with reviewed gold, a deterministic scorer, and bootstrap intervals.
- An enricher: one `gpt-6-luna` call per server writes a short tag per tool (summary, intents, effect, flags). 527 tools cost about 176k tokens in and 60k out.
- A grouper (draft 55-domain taxonomy) and a three-stage router: plan capabilities and groups, select tools from the chosen groups, widen to the rest only for uncovered capabilities.
- Baselines: BM25, embeddings, enriched embeddings, the full catalog in context (raw and as cards), and embedding plus LLM rerank.

## Results (frozen 60 queries)

| System | LLM input tokens | Latency p50 | Slot recall@5 | Full coverage@5 | R-precision | MRR | Confusion@5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BM25 | none | under 1 ms | 0.412 | 0.250 | 0.221 | 0.428 | 0.237 |
| Embeddings (raw) | none | under 1 ms, cached query | 0.517 | 0.283 | 0.374 | 0.589 | 0.288 |
| Embeddings (enriched tag) | none | under 1 ms, cached query | 0.529 | 0.317 | 0.457 | 0.666 | not computed here |
| Embedding + rerank (top 20, raw) | 4,800 | 3.7 s | 0.543 | 0.350 | 0.644 | 0.703 | 0.102 |
| Full catalog, raw definitions | 104,840 | 4.3 s | 0.599 and 0.637 (two runs) | 0.400 and 0.467 | 0.638 and 0.614 | 0.701 and 0.678 | 0.136 and 0.102 |
| Full catalog, enriched cards | 32,698 | 3.2 s | 0.635 and 0.657 | 0.450 and 0.433 | 0.651 and 0.664 | 0.758 and 0.758 | 0.085 and 0.119 |
| Router, server groups | 8,901 | 5.3 s | 0.638 | 0.400 | 0.612 | 0.713 | 0.119 |
| Router, domain groups | 8,502 | 6.1 s | 0.649 | 0.417 | 0.600 | 0.751 | 0.169 |

Natural set (94 tasks, bench reference tools as gold, 47 tasks overlap with the frozen set): BM25 0.361, embeddings 0.446, full catalog raw 0.596 slot recall@5. Same ordering as the frozen set. Cards and router were not run on it (credits ran out).

Noise scaling (random pools of 50 to 527 tools, gold kept): slot recall@5 falls from 0.60 to 0.41 for BM25 and from 0.78 to 0.52 for embeddings.

## What the data supports
1. **A cheap reasoning model with the whole catalog in context beats embedding search clearly** (R-precision 0.61 to 0.64 against 0.37), at about 105k tokens and 4 s per query. The 527-tool catalog fits in context.
2. **Enriched cards compress the catalog 3.2x (104,840 to 32,698 tokens) with no accuracy loss we can detect** (paired differences against raw all include zero), and about 1.1 s faster.
3. **The router reaches the same accuracy as the full-catalog baselines at about 8.5k to 8.9k tokens** (12x fewer than raw, 3.7x fewer than cards). It is slower, because it makes two or three LLM calls in a row.
4. **Flat enrichment alone gives a small gain for embeddings**, mainly in ordering (R-precision 0.374 to 0.457). No paired interval excludes zero except one MRR comparison, barely. Treat as a hint.
5. **Grouping by server does as well as grouping by our taxonomy** (paired differences include zero), so at this catalog size the taxonomy is not needed.
6. **Embedding plus rerank is a strong cheap competitor**: about half the router's tokens, faster, and equal on precision and confusions. It loses recall, because its embedding first stage contained an acceptable tool for only 64% of slots. The router's recall is higher (slot recall@5 0.638 against 0.543, 22 wins to 6 losses, interval [-0.204, 0.021] from the rerank side), most visibly on multi-capability and taxonomy-collision queries. Those bucket cells hold 10 to 15 queries each, so they are pointers.

## What we did not show
- That routing beats embedding plus rerank on confusion rate. The rates are close.
- That the hierarchy helps at the catalog sizes we tested. All of them fit in context, which is where pruning has least to prove.
- Anything about catalogs of thousands of tools, the regime registries face. That is the main open test.
- Stability beyond one run per system (the two full-catalog runs returned identical sets on only 45% and 63% of queries; averages agree).
- LLM-judge scores. Precision is a lower bound, because 30% to 73% of returned tools are neither acceptable nor listed confusers.

## Claims we can make, and ones we cannot
Can: enrichment is a cheap, one-time build step that compresses a tool catalog about 3x without a measurable accuracy loss at 527 tools; a group-based router keeps accuracy at under 9k tokens; embedding-only retrieval is clearly weaker than LLM reading at this size; flat enrichment helps embeddings a little.
Cannot: that ToolPrune is more accurate than loading everything, that it reduces confusions, that it beats embedding plus rerank overall, or that it works at registry scale.

## Limits
- Gold is a reviewed reference, not ground truth. A human reviewed only the 20 decisions that change gold. The bench's own reference lists look incomplete for about 27 tasks.
- Confusers are model-listed and not exhaustive. The confusion rate is narrow.
- `gpt-6-luna` rejects the `temperature` parameter, so calls are not strictly deterministic.
- Latency for embeddings excludes the query-embedding API call, which comes from the cache.
- n=60 (n=94 for the natural set), so differences under about 0.1 are within noise.

## To do
See `phase_plan.md`. The largest item is the scale test (MCP-Zero tools as distractors).
