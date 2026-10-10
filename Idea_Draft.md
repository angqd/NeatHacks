# ToolPrune: hierarchical tool retrieval

Context brief for coding agents. Read this first. Detailed planning happens in follow-up tasks.

## What we are building

A training-free tool retriever. An LLM enriches each MCP/API tool with facet annotations, then queries are routed by pruning hierarchically (L0 function family, then L1 domain, then tool), so the agent sees only the few tools it needs.

Example: `search_1` (image search) sits under L1 `image` and `search_2` (contact lookup) under L1 `contact info`, both under L0 `search_tools`. A query about photos never reaches `search_2`.

**Hypothesis (unproven):** on queries where tool names or descriptions collide, hierarchical routing over enriched annotations makes fewer confusion errors than embedding search, and uses far fewer context tokens. We must measure this, not assume it. Most of the gain may come from the enrichment alone, not the hierarchy.

## Hackathon constraints (neatHack, Oct 10 to 12, 2026, IST)

- All code is written during the event. Public repo, commits dated Oct 10 to 12.
- Must use neatlogs and Entire while building, and cfo.ai for the business plan (not code). The demo video (3 min max) covers all three.
- Submit Oct 12, 7:00 to 11:55 PM IST, as a quote post on X.
- Score weights: agent 30, sponsor use 25, demo 20, building in public 15, usefulness and originality 10. A thin end-to-end agent proof (stretch) strengthens the agent score.
- Evidence we must keep: two neatlogs traces before and after a change with numbers, one run where something failed and the system recovered, Entire checkpoints.
- Never commit secrets. Checkpoints in a public repo are public.

## Benchmarks and baselines

BM25 is our floor, not the state of the art. Dense embeddings beat it. Numbers below are self-reported in the toolrank README (alpha release, Sep 30, 2026) and not independently verified.

| Retriever | ToolRet NDCG@10 | LiveMCPBench Recall@5 |
| --- | --- | --- |
| BM25, no instruction | 29.01 | 31.68 |
| Qwen3-Embedding-8B | 51.11 | 50.82 |
| Qwen3-Embedding-8B + learned heads | 54.03 | 53.03 |

- **LiveMCPBench:** 95 tasks, 70 servers, 527 tools. toolrank used 94 queries and 525 tools; one query is about one point, so report confidence intervals and never claim SOTA from it.
- **ToolRet:** 7.6k tasks, 43k tools. Too large to annotate fully; use a sampled subset and say so.
- **MTRB:** RestBench, MetaTool and ToolBench subsets (54 to 2,645 tools), adds Sufficiency@k for multi-tool tasks.
- **MCP-Zero tool set:** about 2,800 tools but no queries; any queries we write are synthetic and must be labeled as such.
- **Gate:** our BM25 harness must reproduce about 31.7 Recall@5 on LiveMCPBench within about 2 points before any other number is trusted.

## Phase 1: BM25 baseline and collision set (first)

Goal: a small set where confusion is guaranteed, so any win is attributable to the method.

**Tools (about 250, from LiveMCPBench):** about 120 in roughly 30 collision groups of 3 to 5 tools (same or near-same names across domains such as search, get, list, read, query; or near-identical descriptions on different servers), plus about 130 ordinary distractors. Mine candidate groups automatically, then verify by hand.

**Queries (about 120), written as tasks that do not reuse tool wording:**
- about 70 domain-disambiguation
- about 15 multi-tool
- about 20 constrained (read-only vs destructive)
- about 15 out-of-scope (correct answer: no tool)

**Rules:**
- Dev/test split 30/70, frozen before the enricher exists.
- Annotations are generated from tool docs only, never from queries.
- An LLM may draft queries; a human checks every one.

**Schemas:**
- Tool: `id, server, name, description, input_schema`
- Query: `id, text, type (domain | multi_tool | constrained | out_of_scope), gold_tools, confusers, split`

**Metrics:** Recall@1 and @5, MRR, confusion rate (gold tool missed while a labeled confuser ranks in the top 5), out-of-scope false-positive rate, tokens, latency, cost.

**Steps:**
1. Ingest and normalize LiveMCPBench tools and queries.
2. Run BM25 on raw text (name, description, server name) and pass the reproduction gate.
3. Mine and select the collision groups.
4. Draft and verify queries; run a 20-query pilot.
5. Write down what counts as "enough confusion" before the real run.
6. Run BM25 and raw-embedding baselines on the collision set, with every query traced in neatlogs.

**Gate 1:** baselines miss a meaningful share, and the misses are caused by collisions. If baselines are near-perfect, add harder collisions or shift the story to cost and scale.

## Phase 2: enricher and hierarchy (small scale)

- **Facets per tool:** function (L0), domain (L1), effect (read, write or destructive), auth, inputs and outputs, a "not for" line.
- **Taxonomy:** fixed seed of 30 to 60 domains plus "other", versioned. Annotate at temperature 0, cache by content hash, re-annotate only changed tools.
- **The ladder, all on the frozen test set:**
  1. BM25, raw text
  2. embeddings, raw text
  3. embeddings, enriched text
  4. enriched embeddings plus LLM rerank of the top 50
  5. hierarchical pruning (beam of 2 to 3 branches per level; low confidence widens the beam or falls back to flat search)
- **Report:** per-level accuracy (L0, L1, tool), confusion rate, Recall@k, tokens, latency, cost.

**Gate 2:** hierarchy matches or beats rung 4 on confusion rate, or ties it at lower tokens. If not, the enricher is the product.

## Phase 3: scale (only if Gate 2 passes)

- Full LiveMCPBench for the headline number, then MTRB-ToolBench (2,391 tools), then the MCP-Zero set (synthetic queries, labeled).
- Ship an MCP `find_tools` server and a CLI, plus the least-privilege filter (hide destructive tools unless the task needs them).
- Streamlit visuals: tool-universe treemap (category, server, tool) and a failure explorer.
- Stretch: a thin agent completing 10 to 20 real tasks with and without the router; a description audit post (how many tools have colliding descriptions).

## Engineering conventions

- Python 3.12, uv, Pydantic, httpx, SQLite, Streamlit. Plain code, no agent framework.
- Every step is a neatlogs span. Workflow names: `tool-retrieval-eval`, `tool-enrich`, `tool-route`.
- Deterministic where possible: temperature 0, cache all LLM and embedding calls, log the model used.
- `make eval` runs the full ladder and writes a results table to `reports/`.
- Keep dev and test strictly separate. Never tune on test.
- Small commits with clear messages so Entire checkpoints capture decisions.
- Secrets in `.env` only, never in code, logs or agent sessions.

Suggested layout: `src/ingest`, `src/baselines`, `src/enrich`, `src/route`, `src/eval`, `data/` (fetched by script), `reports/`.

## Claims policy

- Do not claim state of the art. Report the full ladder with intervals.
- Label synthetic data and sampled subsets.
- Fix the definition of confusion rate before running experiments.

## Open items

- Name: ToolPrune (chosen). Still check GitHub repo, X handle and domain availability.
- Confirm LiveMCPBench data terms and download method.
- Choose the embedding model (hosted API) and the LLM per step.
- Decide whether to include the thin agent proof.
