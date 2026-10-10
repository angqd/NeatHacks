# ToolPrune phase plan

Working plan for the build, phase by phase. `benchmark_plan.md` holds the dataset stage specs. `Idea_Draft.md` holds the original idea and hypothesis. This file holds the order of work, decisions, and acceptance criteria.

Last updated: 2026-10-11 (hackathon day 2).

## Decisions in force

| Topic | Decision |
| --- | --- |
| Model for baselines, retriever, and enricher | `gpt-6-luna`, one model across the whole ladder so systems stay comparable. Pivot to a stronger model only if a 10-query sample shows the system ranking flips. |
| Embeddings | OpenAI `text-embedding-3-small`, vectors cached on disk by content hash. |
| OpenAI calls | Only through OpenAI SDKs. The embedding script uses the `openai` SDK. The enricher and retriever, later, use the OpenAI Agents SDK. |
| Judges | Two families, blind and shuffled. Start with `claude-haiku` 5.5 via LiteLLM, then add `claude-sonnet-4.6` via LiteLLM, then an OpenAI-family judge. Judges are never systems under test. |
| Tracing | neatlogs, initialised once in a shared module. Workflow names: `tool-retrieval-eval`, `tool-enrich`, `tool-route`. |
| Tests | No unit tests at this scale. Keep the existing smoke test. Add an end-to-end check only where a stage needs one. |
| Eval set | Frozen: `data/processed/eval_set.jsonl`, sha256 `305447a13c3359e40b0193a2857c69d99430414bed2f337976db9d53ff0f4afc`. Do not edit. A change means a new versioned file. |
| Out-of-scope queries | Known gap. Add synthetic non-matching queries later, in a separate labeled file. |
| Gold | Candidate set per slot: the pick plus its alternates. Precision and recall are scored against it. Confusers are tracked separately. |

Terms are defined in `glossary.md`. Use them exactly.

## Working method

The orchestrator (the main Claude Code session) plans, decides, and reviews. Menial scripting, collection, and exploration go to Haiku subagents, one small task each, with an exact file path and function signature. The orchestrator reviews every deliverable by running it and checking its output before moving on. Commit per phase.

## Module layout (target)

- `src/toolprune/models.py`: Pydantic types (`Tool`, `Slot`, `EvalQuery`, `RetrievedSet`, `RunRecord`), file paths, loaders for `tools.jsonl` and `eval_set.jsonl`.
- `src/toolprune/text.py`: tokenizer and tool-document builders (raw text variants).
- `src/toolprune/bm25.py`: deterministic BM25.
- `src/toolprune/embeddings.py`: OpenAI embedding generation with an on-disk cache, plus the embedding retriever.
- `src/toolprune/tracing.py`: neatlogs initialisation shared by all workflows.
- `src/toolprune/eval/`: scorer, runner, reports (Phase B).
- later: enricher, router, judges.

Retriever interface: a retriever takes a query string and returns ranked tool ids with scores. All systems, baselines and ours, go through it.

## Phase A: foundations (no scoring yet)

Goal: BM25 and embedding retrievers that run on the frozen eval set.

1. Models, paths, loaders, and the retriever interface (`models.py`).
2. Tokenizer and tool-document builders (`text.py`). Reuse the CJK-aware tokenizer from `task_features.py`.
3. BM25 retriever (`bm25.py`): k1=1.5, b=0.75, fixed tokenization, stable tie order.
4. Embedding generator and retriever (`embeddings.py`): `text-embedding-3-small` through the `openai` SDK, cache keyed by content hash, model name and token count logged.
5. neatlogs initialisation (`tracing.py`) with the OpenAI instrumentation, so the embedding calls show up as spans.

Acceptance: `python -m toolprune.embeddings` builds the cache for all 527 tools and the 60 queries. Both retrievers return a ranked list for a sample query. Running twice makes no new API calls.

## Phase B: harness and first numbers

6. Scorer: slot recall@k with alternates, full coverage@k, precision@k and size-matched precision, set-F1, MRR, confusion rate, unjudged rate, tokens, latency, bootstrap intervals, paired win/loss per bucket.
7. Sanity check: BM25 on the original LiveMCPBench queries, reported next to the self-reported 31.68 Recall@5. Report a grid of document-text variants. Never tune a variant to hit the number. Investigate only a gross mismatch (more than 15 points either way), which would suggest a bug.
8. Write the confusion-rate definition into `benchmark_plan.md` before any run on the eval set.
9. Run BM25 and embeddings on the frozen 60 at k=1, 5, 10. Add the catalog audit stats and the noise-scaling curve (pool sizes 50, 100, 250, 527, gold always kept).

Acceptance: a `reports/` table with per-bucket numbers for both retrievers, with intervals.

## Phase C: LLM baselines (`gpt-6-luna`)

10. Full-catalog baseline: all tool definitions in one prompt, exact token count. Dev queries first.
11. Embedding shortlist plus LLM rerank.
12. Neatlogs before and after trace pair, with the numbers compared.

## Phase D: judges

13. Two-judge pipeline, blind and shuffled, each run twice. Report agreement. Judges label unjudged returned tools as alternate, confuser, or irrelevant, and give a sufficiency verdict per returned set. A small human sample checks disagreements.

## Phase E: enricher and router

14. Per-server annotation (server cards, sub-groups, sibling-aware "not for" lines), then taxonomy induction across servers, then tool-level facets. The prompt wraps tool docs as quoted data, constrains output to the taxonomy, and flags instruction-like text.
15. Router: one routing call over taxonomy labels, non-LLM scoring inside the chosen branches, one final selection call.
16. Ablation: enriched embeddings with no hierarchy.
17. Full ladder on the frozen set, with intervals.

## Gates

- Sanity check 0: our BM25 on the original bench is in the same range as the self-reported reference. The reference is unverified and the protocol differs, so a gap is documented, not tuned away.
- Gate 1: baselines miss a meaningful share on the hard buckets, and the misses come from collisions. If baselines are near-perfect, harden the buckets or shift the story to cost and scale.
- Gate 2: the router matches or beats embedding plus rerank on confusion rate, or ties it at lower tokens. If not, the enricher is the product.

## Evidence to keep (hackathon)

- Two neatlogs traces, before and after a change, with the numbers compared.
- One run where something failed and the system recovered.
- Entire checkpoints and small, dated commits.
- Never commit secrets.

## Status

- Done: eval set built, reviewed, frozen, committed, and pushed.
- Done: Phase A. BM25 and embedding retrievers run on the frozen set, embeddings are cached (588 texts, about 39k tokens), neatlogs initialises. Neatlogs span arrival in the dashboard is not yet confirmed by eye.
- Done: Phase B first numbers. Scorer, runner, report script, BM25 sanity check, catalog audit, and `reports/baseline_v0.md` are in. Still to do from Phase B: noise-scaling curve, cold-latency pass, miss-cause analysis.
- Post-todo (run in parallel with the enricher build): cold-latency pass for the embedding system.
- Done: noise-scaling curve and the full-catalog drop-in run (Phase C item 10). See reports/full_catalog_v0.md.
- Next: embedding plus rerank baseline (Phase C item 11), miss-cause analysis, then the enricher.
