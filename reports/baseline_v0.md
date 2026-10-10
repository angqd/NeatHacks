# Baseline v0: BM25 and embeddings on the frozen eval set

Date: 2026-10-11. Systems: BM25 (`name_desc_server`, k1=1.5, b=0.75) and OpenAI `text-embedding-3-small` over the same raw tool document. Both see raw tool documents only. Eval set: 60 queries, sha256 `305447a1...bf4afc`. All numbers come from `toolprune.eval.score` and are tabulated in `baseline_v0_tables.md` and `results.json`. Terms are defined in `glossary.md`.

Read with care: n is 60, so intervals are wide, and the per-bucket and per-family cells hold 1 to 15 queries each. These cells carry no intervals. Treat them as pointers, not findings.

## What the numbers say

**Embeddings beat BM25 overall, but both miss a lot.**

| Metric (k=5 unless noted) | BM25 | Embeddings |
| --- | --- | --- |
| Slot recall@5 | 0.412 [0.312, 0.512] | 0.517 [0.425, 0.608] |
| Slot recall@10 | 0.467 [0.368, 0.568] | 0.625 [0.535, 0.714] |
| Full coverage@5 | 0.250 [0.150, 0.367] | 0.283 [0.167, 0.400] |
| R-precision | 0.221 [0.146, 0.301] | 0.374 [0.283, 0.467] |
| MRR | 0.428 [0.326, 0.533] | 0.589 [0.491, 0.685] |

- The paired difference on slot recall@5 is +0.104 for embeddings, interval [0.007, 0.206], with 16 wins, 5 losses, and 39 ties. R-precision (+0.153) and MRR (+0.161) also exclude zero.
- Full coverage@5 does not separate the two systems: the paired difference is +0.033 with an interval of [-0.050, 0.133].
- Even the better system covers every slot on only 28% of queries at k=5. Phase 1's Gate 1 asked whether baselines "miss a meaningful share". They do. Gate 1 also asks whether the misses come from collisions. This run does not show that. It has not yet analysed why queries miss.

**Where the gaps are (small n, no intervals).**
- `semantic_distance` (12 queries): slot recall@5 is 0.208 for BM25 and 0.500 for embeddings. This matches the expectation that keyword matching fails when the query avoids tool vocabulary. Embeddings still miss half of the slots.
- `multi_capability` (15 queries): slot recall@5 of 0.211 and 0.383, and full coverage of 0.000 and 0.067. Part of this is a ceiling effect. Some queries have 4 to 6 slots, and a top-5 list cannot cover 6. Read the recall@10 column and the later size-matched comparison, not this cell alone.
- `taxonomy_collision` (10) and `near_duplicate` (9): embeddings do not clearly gain in recall, and their confusion rate is higher (0.500 against 0.300, and 0.375 against 0.125). These are the buckets the router is meant to help with. At 9 and 10 queries, a difference of one or two queries moves these numbers a lot.
- `none` (4 queries, ordinary tasks): BM25 gets all slots into the top 5.
- Two task families (`file_conversion`, `shopping_research`, 2 queries each) score 0.0 for both systems. Two queries cannot support a conclusion.

**Precision is a lower bound.** 62% to 73% of the top-5 tools are neither acceptable nor a listed confuser. Many of these may be valid alternatives that nobody labeled. The LLM-judge pass (Phase D) is meant to label them. Until then, precision@5 (0.177 for BM25, 0.253 for embeddings) understates quality.

**Tokens are not where the contest is.** A top-5 list is about 1,000 to 1,150 tokens. The whole catalog is 100,496 tokens (`catalog_audit.md`). So any retriever that returns 5 tools saves about 99% of the context against loading everything. That comparison is easy to win. The real question is accuracy at small k.

**Latency is not comparable yet.** Both systems return in well under a millisecond because the embedding vectors for the queries come from the on-disk cache, so the embedding figure excludes the OpenAI call. A cold timing pass is still to do.

## Sanity check against the self-reported BM25 number

On the original 95 bench tasks, with the bench reference tool names as gold matched by name, our BM25 scores 36.06 Recall@5 for the `name_desc_server` document (range 27.04 to 37.83 across the five document variants). The self-reported reference is 31.68. The reference is unverified, and its document text, query set (94 queries), and gold matching are unknown to us. Our number is in the same range, which is all this check is for. No variant was tuned. Details are in `sanity_bm25.md`.

## What the catalog audit adds (`catalog_audit.md`)

- 70 servers, 527 tools, 100,496 tokens in total.
- 13 tool names shared across 30 tools, and the most shared name (`search`) appears 4 times.
- 66 tools have a missing or very short description, and 62 descriptions contain CJK text.
- Only 1 pair of tools on different servers has near-identical descriptions (Jaccard of 0.8 or more). So the `near_duplicate` challenge is mostly about tools that differ by a constraint (current or historical, read or write), not about copied text.
- 38 tools match instruction-like phrases by a keyword heuristic. These are candidates for review, not confirmed injections.

## Limits of this run

- Only two raw-text baselines. The full-catalog and embedding-plus-rerank baselines are not run yet.
- The scorer uses the reviewed gold. Human review covered only the 20 decisions that change gold, so label errors remain possible.
- Confusers are model-listed and not exhaustive. The confusion rate is a narrow measure.
- No LLM-judge scores exist yet.

## Next

1. Cold-latency pass for the embedding system.
2. Noise-scaling curve (pool sizes 50 to 527).
3. Analyse why the misses happen, split by cause (collision, vocabulary gap, slot count above k).
4. LLM baselines with `gpt-6-luna`: full catalog, and embedding shortlist plus rerank.
