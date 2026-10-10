# ToolPrune benchmark plan

Two separate pipelines share the raw data and nothing else.

| | Dataset labeler (builds the test) | Enricher (the product) |
| --- | --- | --- |
| Purpose | Turn LiveMCPBench into a labeled eval set | Add facets to each tool |
| Input | `tasks.json` plus the gold tools' docs | `tools.json` only |
| Sees queries? | Yes | Never |
| Output | `eval_set.jsonl` | `annotations.jsonl` |
| Model | Strong model, low volume (about 95 calls) | Cheapest model that passes a quality check |

The labeler and the enricher use different model families, so labels do not favour the enricher's style.

The five bucket types belong only to the labeler. L0 and L1 belong only to the enricher.

## Stages

1. **Normalize** (no LLM). Output: `data/processed/tools.jsonl`, `data/processed/tasks_resolved.jsonl`.
2. **Label tasks** (LLM plus script features). Output: `data/processed/tasks_tagged.jsonl`, `data/processed/review_queue.jsonl`.
3. **Review and select** (human). Review low-confidence tasks and a 10% sample of the rest. Select 60 with quotas per bucket, add about 6 derived rewrites, freeze the 30/70 dev/test split. Output: `data/processed/eval_set.jsonl`.
4. **Induce the taxonomy** (LLM, then human). Input is `tools.jsonl` only.
   - Pass 1: free-form function and domain labels per tool.
   - Pass 2: consolidate into 30 to 60 labels plus "other". Report cluster sizes to decide whether L1 alone is enough or L0 is needed.
   - Pass 3: human approves. Freeze as `taxonomy_v1.json`.
5. **Enrich** (LLM, one call per tool, constrained to the taxonomy). Cache by content hash. Output: `annotations.jsonl`.
6. **Retrieve and evaluate.** Router, baselines, scoring against `eval_set.jsonl`.

Build order: stages 1 to 3 first (subset), then 4 and 5.

## Baselines (stage 6)

1. Full catalog in context (LLM picks from all 527 definitions; exact token count).
2. Embedding top-k, raw text.
3. BM25, raw text.
4. Embedding shortlist plus LLM rerank.
5. Ablation: enriched embeddings, no hierarchy.

Compare at fixed k, at the agent's set size, and at matched tokens. Report per-bucket recall, full coverage of gold slots, confusion rate, tokens, p50 latency, cost per query, with paired win/loss counts and bootstrap intervals.

## Stage 1 spec: normalize

Script: `src/toolprune/normalize.py`. Deterministic, no LLM.

Input: `data/raw/tools.json`, `data/raw/tasks.json`. The tools file is a list of servers. Each server has `name`, `description`, `category`, `web`, `config`, and `tools`. `tools` is a dict keyed by config name, whose values contain a `tools` list of `{name, description, inputSchema, annotations}`.

Output `tools.jsonl`, one line per tool:

- `id`: `"<server>::<tool_name>"`
- `server`, `server_category`, `server_description`
- `name`, `description`, `input_schema`, `annotations`
- `name_collision_count`: number of tools in the catalog with the same `name`

Output `tasks_resolved.jsonl`, one line per task:

- `task_id`, `question`, `category`, `file_name`, `steps`
- `gold_names`: tool names parsed from `Annotator Metadata.Tools` (strip numbering, one per line)
- `gold_ids`: resolved tool ids, `null` where unresolved
- `resolution`: per gold name, one of `unique`, `ambiguous`, `missing`, with the candidate ids
- For `ambiguous`, try to disambiguate by checking whether a candidate's server name appears in `steps`. Record `resolved_by: "steps_server_match"` if it works, otherwise leave unresolved.
- `n_gold`, `fully_resolved`: boolean

Also print a summary: counts of unique, ambiguous, and missing, and how many tasks are fully resolved.

## Stage 2 spec: label tasks

Two parts.

### Part A: deterministic features

Script: `src/toolprune/task_features.py`. Writes features into `tasks_tagged.jsonl`.

- `overlap_ratio`: lowercase, drop stopwords, light stemming. Take content tokens of the question. Count those that also appear in the gold tools' name, description, and server name tokens. Ratio is overlap count divided by question content tokens. Flag `low_overlap` if the ratio is at most 0.10. This threshold is fixed before any system is scored. Do not choose it by looking at baseline results.
- `n_gold`: flag `multi_capability` if 3 or more.
- `shared_name`: true if any gold tool has `name_collision_count` above 1.
- `schema_neighbors`: for each gold tool, other tools on a different server with the same name, plus tools whose name tokens overlap strongly. No embeddings.
- `read_only_hint` and `destructive_hint` pulled from tool annotations where present.

### Part B: LLM judgment per task

One judgment per task, structured output. Input: the question, the steps, the gold tools' docs, and the neighbour tools' docs.

Output record, one JSON line per task:

- `task_id`
- `buckets`: list from `semantic_distance`, `taxonomy_collision`, `multi_capability`, `near_duplicate`, `ambiguity`, `none`
- `primary_bucket`: one value from the same list
- `evidence`: one or two sentences per bucket assigned, quoting the doc text or question words
- `confusers`: list of `{tool_id, reason}` with reason in `wrong_domain`, `wrong_output`, `current_not_historical`, `destructive`, `missing_capability`, `other`
- `needs_clarification`: boolean
- `confidence`: `high`, `medium`, `low`
- `review_reason`: required when confidence is not `high`

Bucket definitions to apply:

1. **semantic_distance**: the question states the outcome without words from the gold tools' docs. `low_overlap` is a strong signal, but judge it. A question can have high overlap through shared common words and still be semantically distant.
2. **taxonomy_collision**: other tools in the catalog have similar names or descriptions but belong to a different functional category or produce a different output.
3. **multi_capability**: one stated outcome requires several tools.
4. **near_duplicate**: two or more tools look equally relevant, but only some satisfy a constraint in the question (current versus historical, read versus write, file versus URL, free versus authenticated). The constraint must be checkable from the schema or description.
5. **ambiguity**: several interpretations are plausible, or an essential parameter is missing.
6. **none**: an ordinary, clear task.

Rules for the labeler:

- Judge from the question and tool docs. Do not use embeddings or any retriever output.
- A task can carry several buckets. Pick one `primary_bucket`, the one that makes the task hardest for a retriever.
- When unsure, set confidence to `low` and say why. Do not guess.
- Never change the gold tool list. It comes from the bench.

### Selection helper

After tagging, print counts per bucket and per primary bucket. Write `review_queue.jsonl` containing every task with confidence not `high`, every task that is not `fully_resolved`, and a random 10% sample (seed 0) of the rest.

## Pre-registered rules

- Overlap threshold: 0.10, fixed above.
- Bucket quotas for the 60: set in stage 3 after seeing the tag counts, but before any retriever runs.
- Dev/test split 30/70, frozen before the enricher exists.
- Derived rewrites (ambiguity and semantic distance) keep the original bench gold and are labeled `derived`.

## Stage 6 spec: deterministic metrics

Scored per system, per query, from the returned set. The scorer is plain code. No LLM computes any number.

Definitions (acceptable tools = a slot's pick plus its alternates; listed confusers are in the eval set):

- **Slot recall@k:** for one query, the share of its slots with at least one acceptable tool in the top k. A slot counts once however many of its acceptable tools are returned. Averaged over queries.
- **Full coverage@k:** share of queries where every slot is hit.
- **Precision@k:** returned tools in the top k that are acceptable for any slot, divided by the returned tools (up to k).
- **R-precision:** precision at k equal to the query's number of slots. The fair fixed-size precision.
- **MRR:** reciprocal rank of the first acceptable tool, averaged over queries (0 if none in the list).
- **Confusion rate@k:** queries with at least one missed slot and at least one listed confuser in the top k, divided by queries that list a confuser.
- **Confuser-first rate@k:** queries where a listed confuser ranks above the first acceptable tool (or an acceptable tool is absent and a confuser is present), divided by queries that list a confuser. A looser companion to the confusion rate.
- **Unjudged rate:** returned tools that are neither acceptable nor a listed confuser, divided by returned tools.
- **Tokens:** tokens in the returned tools' definitions (name, description, input schema), counted with tiktoken `o200k_base`. This is a proxy for the model's own tokenizer.
- **Latency:** wall-clock time of one retrieve call for one query, reported as p50 and p95 in milliseconds. For embedding systems it includes the query-embedding API call.

Reporting: per challenge bucket and per task family, macro average (mean of group means) and micro average (mean over queries). Intervals by 10,000 bootstrap resamples of queries, seed 0, 95% percentile. Paired differences between systems with win, loss, and tie counts.

Sanity check, not a gate: BM25 on the original LiveMCPBench tasks, using the bench reference tool names as gold matched by tool name, reported across a grid of document-text variants next to the self-reported 31.68. No variant is tuned to hit it.

LLM-judge scores (sufficiency, labels for unjudged tools) are a separate, later step (Phase D) and are reported next to these numbers, never mixed into them.

