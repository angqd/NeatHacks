# ToolPrune

Hierarchical tool retrieval for MCP and API tools. An LLM annotates each tool once with facets (function, domain, effect, a "not for" line). At query time a router prunes the catalog so an agent sees a few tools, not hundreds.

Hypothesis (unproven): on queries where tool names or descriptions collide, routing over enriched annotations makes fewer confusion errors than plain embedding search, and passes far fewer tokens to the agent than loading every tool definition. Most of any gain may come from the enrichment alone, not the hierarchy. The benchmark is built to tell these apart.

Built for neatHack (Oct 10 to 12, 2026).

## Status

The Phase 1 POC is concluded for now. `reports/conclusion.md` has the full summary. In short:

- A frozen 60-query eval set and a 94-task natural set, a deterministic scorer, and the baselines (BM25, embeddings, enriched embeddings, full catalog raw and as cards, embedding plus rerank) are built and scored.
- The enricher (one tag per tool), a draft taxonomy, and a three-stage router are built and scored.
- Findings: enriched cards cut the catalog from 104,840 to 32,698 tokens with no accuracy loss we can detect. The router matches the full-catalog baselines at about 8.5k to 8.9k tokens, but is slower (5 to 6 s). Embedding plus rerank is a strong, cheaper competitor with lower recall. Grouping by server does as well as the taxonomy. At 527 tools everything fits in context, so the case for pruning at scale is untested.
- Not shown: a confusion-rate win, an accuracy win over the full catalog, anything at registry scale. All numbers have wide intervals (n=60).

See `phase_plan.md` for the to-do list and `reports/` for every result.

## Decisions in force

- **Model:** `gpt-6-luna` for every baseline, the enricher, and the retriever, so systems stay comparable. It rejects the `temperature` parameter, so its calls are not strictly deterministic. Calls are cached by content hash, and runs are repeated to measure stability.
- **Embeddings:** OpenAI `text-embedding-3-small`, cached on disk by content hash.
- **OpenAI calls:** only through OpenAI SDKs. The enricher and retriever will use the OpenAI Agents SDK (`openai-agents`).
- **Judges:** two model families, blind and shuffled. Start with Claude Haiku 5.5 via LiteLLM, then add Claude Sonnet 4.6, then an OpenAI-family judge.
- **Tracing:** neatlogs. Workflow names: `tool-retrieval-eval`, `tool-enrich`, `tool-route`.
- **Data contracts:** Pydantic models for tools, queries, annotations, and outputs.
- **Determinism:** temperature 0, cache every LLM and embedding call, log the model per call.
- **Tests:** no unit tests at this scale. One smoke test only.

## Terminology

`glossary.md` defines every term (server, tool, catalog, gold slot, acceptable tools, challenge bucket, task family, facets, taxonomy, domain, returned set, and more). Use those words in code, reports, and commits.

Visibility rule: baselines run on raw tool documents only, as an ordinary MCP client would. Only the enricher and the router touch our taxonomy, facets, and server cards. No system ever sees the eval annotations (gold, challenge bucket, task family, confusers).

## Data

Source: LiveMCPBench (`ICIP/LiveMCPBench` on Hugging Face). Raw files are fetched by script into `data/raw/` (gitignored) with URL, size, sha256, and fetch time in `data/raw/manifest.json`.

| File | Contents |
| --- | --- |
| `tools/tools.json` | 70 servers, 527 tools: name, description, inputSchema, annotations |
| `tasks/tasks.json` | 95 tasks: question, answer, category, annotator steps, reference tool list |
| `tools/all_config.json` | Server configs (not used) |

Catalog facts: tool names repeat across servers for 30 tools, 66 tools have a missing or very short description, 12 servers have one tool and 10 have 15 or more, and the full catalog is roughly 97k tokens (estimate).

Fetch with:

```bash
.venv/bin/python -m toolprune.pipeline          # keeps existing files
.venv/bin/python -m toolprune.pipeline --force  # re-download
```

Check the LiveMCPBench data terms before publishing derived data. This is still an open item.

## Eval set

`data/processed/eval_set.jsonl` is frozen: 60 queries, sha256 `305447a13c3359e40b0193a2857c69d99430414bed2f337976db9d53ff0f4afc`. Do not edit it. A change means a new versioned file.

- **Buckets:** multi_capability 15, semantic_distance 12, ambiguity 10, taxonomy_collision 10, near_duplicate 9, none 4.
- **Split:** 18 dev, 42 test. Never tune on test.
- **Derived:** 12 queries are rewrites of bench tasks (ambiguity and semantic distance) and are marked `derived`. They keep the bench gold.
- **Families:** 15 task families (for example `finance_analysis`, `academic_search`, `geo_location`), capped at 8 queries each. The families are independent of any enricher taxonomy. `data/processed/families_review.md` lists them.
- **Gold:** each query has slots. A slot has one picked tool and its acceptable alternates. Precision and recall are scored against that candidate set. Confusers (plausible but wrong tools) are tracked separately.
- **Known gap:** there are no out-of-scope queries (correct answer: no tool). Synthetic ones will be added later in a separate, labeled file.

How the set was built, in order:

| Step | Script or run | Output |
| --- | --- | --- |
| Normalize the catalog, resolve bench gold names | `toolprune.normalize` | `tools.jsonl`, `tasks_resolved.jsonl` (regenerable, not committed) |
| Deterministic task features | `toolprune.task_features` | features in `tasks_tagged.jsonl` |
| First-pass labels | Haiku subagent | `tasks_tagged.jsonl` |
| Blind second opinion | Sonnet subagents | `review_sonnet_*.jsonl` |
| Adjudication of every point | Sonnet subagents | `adjudicated_*.jsonl` |
| Review sheets | `toolprune.review_sheet`, `toolprune.spot_sheet` | HTML sheets (regenerable) |
| Human spot check of 20 gold-changing decisions | review sheet | `spot_decisions.json` |
| Merge and validate | `toolprune.merge_adjudication` | `tasks_reviewed.jsonl` |
| Families and derived rewrites | Sonnet subagent | `families.json`, `task_families.jsonl`, `derived_candidates.jsonl` |
| Select 60, split 30/70 | `toolprune.select_subset` | `eval_set.jsonl`, `selection_report.md` |

Label quality: the labels are LLM-written and model-reviewed. A human checked only the 20 decisions that change what gold means, and restored 8 slots the adjudicator had dropped. The other labels have no human check. Treat gold as a reviewed reference, not ground truth. The blind reviewer flagged 27 tasks whose bench reference tool list misses a needed capability, so the lists are probably incomplete.

## Benchmark method

Systems compared on the frozen set:

1. Full catalog in context: all tool definitions in one prompt, exact token count.
2. BM25 over tool name, description, and server name (k1=1.5, b=0.75, deterministic).
3. Embedding top-k, raw text.
4. Embedding shortlist plus LLM rerank.
5. Ablation: enriched embeddings, no hierarchy.
6. The router over enriched annotations.

Metrics:

- Deterministic: slot recall@k (a slot is hit by its pick or any alternate), full coverage@k, precision@k and size-matched precision, set-F1, MRR, confusion rate (a gold slot missed while a labeled confuser is returned), unjudged rate, returned tokens, p50 latency, cost per query. Bootstrap intervals and paired win/loss per bucket.
- LLM judges (secondary): sufficiency of the returned set, and labels for unjudged returned tools. Two families, blind, run twice, with agreement reported.
- Also planned: a catalog audit and a noise-scaling curve (pool sizes 50, 100, 250, 527, gold kept).

Gates:

- Sanity check 0: our BM25 on the original bench queries is reported next to the self-reported 31.7 Recall@5. The reference is unverified and its protocol differs, so the gap is documented and never tuned away. Only a gross mismatch (over 15 points) triggers a bug hunt.
- Gate 1: baselines miss a meaningful share on the hard buckets.
- Gate 2: the router matches or beats embedding plus rerank on confusion rate, or ties at lower tokens. If not, the enricher is the product.

At 60 queries, one query is about 1.7 points. Report intervals and never claim state of the art.

## Repo layout

```
Idea_Draft.md        original idea and hypothesis
benchmark_plan.md    dataset stage specs and rules
phase_plan.md        build order, decisions, acceptance criteria
product_focus.md     product thinking, parked for after the POC
ui_brief.md          logo and UI brief (logo first)
src/toolprune/       package: fetch, normalize, features, review tools, selection, models, text, bm25, embeddings, tracing
data/raw/            fetched bench files (gitignored)
data/processed/      labeled data, adjudications, families, frozen eval set
tests/               smoke test only
```

## Setup

Python 3.12 and a virtual environment. Install with `pip install -e .`. Put keys in `.env` (gitignored, never committed): `OPENAI_API_KEY`, `NEATLOGS_API_KEY`, `LITELLM_API_KEY`.

## To do

1. **Scale test.** Add MCP-Zero tools (about 2,800, 318 MB download, mostly embeddings) as distractors to the 527-tool catalog and run embeddings, rerank, and the router (server and domain groups) at about 527, 1.5k, and 3.3k tools. Needs the Drive file, schema reconstruction, bulk enrichment, and OpenAI credits. See `reports/tool_set_survey.md`.
2. **OpenAI credits.** The key ran out of quota. Blocked: cards and router on the natural set, the rerank tag variant, a router stability rerun.
3. **Cold latency** for the embedding system (query-embedding API call not cached).
4. **LLM judges** (two families): sufficiency and labels for unjudged tools. Needs the LiteLLM base URL.
5. **Out-of-scope queries** (correct answer: no tool), as a separate labeled file.
6. **Taxonomy decision.** Approve, merge the over-split domains, or drop domains in favour of server groups.
7. **Miss-cause analysis** (collision, vocabulary gap, slot count above k).
8. **Data terms.** Confirm LiveMCPBench terms before redistributing derived data.
9. **Hackathon evidence.** Confirm neatlogs spans in the dashboard, a before and after trace pair, and one failure-and-recovery run.
10. **Logo, UI, demo video, business plan, X post** (`ui_brief.md`, `product_focus.md`).
