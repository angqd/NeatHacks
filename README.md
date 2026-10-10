# ToolPrune

Hierarchical tool retrieval for MCP/API tools. An LLM enriches each tool with facet annotations. Queries route through the hierarchy (L0 function family, then L1 domain, then tool), so the agent sees only the few tools it needs.

Status: Phase 1. Eval set built and frozen; baselines and enricher not yet built. Hypothesis unproven. See `Idea_Draft.md` for the full plan.

## Agent design

- **Agent framework:** OpenAI Agents SDK (`openai-agents`).
- **Data contracts:** Pydantic models for every tool, query, annotation, and agent output. No untyped dicts cross a module boundary.
- **Structured output:** agent outputs are Pydantic models validated by the SDK.
- **Tracing:** neatlogs via its OpenAI Agents processor. Workflow names: `tool-retrieval-eval`, `tool-enrich`, `tool-route`.
- **Model calls:** temperature 0, cached by content hash, model name logged per call.

Pending: `Idea_Draft.md` says "plain code, no agent framework." This README follows the OpenAI Agents SDK decision. Update the draft once confirmed.

## Dataset (as downloaded)

Source: LiveMCPBench (`ICIP/LiveMCPBench` on Hugging Face). Files are stored unmodified in `data/raw/`, with URL, size, sha256, and fetch time per file in `data/raw/manifest.json`.

| File | Records | Contents |
| --- | --- | --- |
| `tools/tools.json` | 70 servers, 527 tools | Per server: `name`, `category`, `web`, `tools` (tool name, description, inputSchema, annotations) |
| `tasks/tasks.json` | 95 tasks | `task_id`, `Question`, `answers`, `category`, `file_name`, `Annotator Metadata` (Steps, Tools, Number of tools) |
| `tools/all_config.json` | 70 entries | Server configs (not used yet) |

Tool categories: Discovery 25, Code 11, File Access 7, Visualization 7, Finance 6, Entertainment 5, Miscellaneous 8, Location 1 (per catalog entry).
Task categories: Office 31, Lifestyle 15, Leisure 14, Finance 14, Travel 12, Shopping 9.

Fetch with:

```bash
.venv/bin/python -m toolprune.pipeline          # keeps existing files
.venv/bin/python -m toolprune.pipeline --force  # re-download
```

## Eval set build (done)

The 60-query eval set is built and frozen: `data/processed/eval_set.jsonl` (sha256 `305447a1...bf4afc`). Method and stage specs are in `benchmark_plan.md`.

| Step | Script | Output |
| --- | --- | --- |
| Normalize catalog, resolve bench gold names | `toolprune.normalize` | `tools.jsonl`, `tasks_resolved.jsonl` (regenerable, not committed) |
| Deterministic task features | `toolprune.task_features` | features inside `tasks_tagged.jsonl` |
| LLM labeling, blind second opinion, adjudication | subagent runs (Haiku, Sonnet) | `tasks_tagged.jsonl`, `review_sonnet_*.jsonl`, `adjudicated_*.jsonl` |
| Review sheets | `toolprune.review_sheet`, `toolprune.spot_sheet` | HTML sheets (regenerable) |
| Merge and validate | `toolprune.merge_adjudication` | `tasks_reviewed.jsonl` |
| Families, derived rewrites | subagent run | `families.json`, `task_families.jsonl`, `derived_candidates.jsonl` |
| Select 60, split 30/70 | `toolprune.select_subset` | `eval_set.jsonl`, `selection_report.md` |

The LLM-written labels are checked by a blind second model and an adjudicator. A human reviewed the 20 decisions that change gold (`spot_decisions.json`). The other labels are model-reviewed only. 12 of the 60 queries are derived rewrites of bench tasks (ambiguity and semantic distance) and are marked `derived`. Gold comes from the bench's reference tool lists, adjusted by review.

## Benchmark method

- **Baseline:** BM25 (k1=1.5, b=0.75) over tool name, description, and server name. Deterministic: fixed tokenization, sorted query terms, stable tie order. Not yet implemented in this repo.
- **Gate:** BM25 must reproduce about 31.7 Recall@5 (toolrank, self-reported) within 2 points on the original LiveMCPBench queries before any other number is trusted. An earlier unversioned run gave 37.78, so the gate is not passed.
- **Confusion rate:** gold tool missed in top k while a labeled confuser ranks in top k. Definition is fixed in `benchmark_plan.md` before the real run.

## Neatlogs setup (order)

1. Create a neatlogs API key. Store it as `NEATLOGS_API_KEY` in `.env` (gitignored). Never in code.
2. Confirm the pipeline exports: run `python -m toolprune.pipeline` with the key set, check spans in the neatlogs dashboard.
3. Wire the OpenAI Agents processor into the agent code once the agent exists.
4. Record a before/after trace pair for each change, with the numbers compared.
5. Record one failing run where an action fails and the agent recovers.

## Open questions

1. **Gold for ambiguous names.** 29 tool names exist on several servers (e.g. `search`, `fetch`, `read_file`). Resolve by hand, by server named in task steps, or drop?
2. **Unresolved gold.** 5 gold names are absent from the catalog (e.g. `ddg-search`, `get_maven_latest_version`). Missing from the snapshot, or renamed?
3. **Gate failure.** BM25 scores 37.78 vs 31.68. Doc-text mismatch with toolrank, or different query text? Which variant matches?
4. **Confusers.** Currently 0 queries have confusers because ambiguous names are excluded from gold. Count ambiguous candidates as confusers?
5. **Human verification.** Who checks queries and gold labels, and how many?
6. **Agent framework.** Confirm OpenAI Agents SDK over the plain-code plan in `Idea_Draft.md`.
7. **LLM for enrichment.** Which model, and which API key? None set in the environment yet.
8. **Collision subset.** Build the ~250-tool collision set from the plan, or use all 527?
9. **Neatlogs key.** Do you have one for this project?
