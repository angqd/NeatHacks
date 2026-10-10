# ToolPrune: UI and brand brief

For the model or designer who builds the logo and, later, the UI. Read `README.md`, `Idea_Draft.md`, and `product_focus.md` for the full context.

**Scope right now: the logo only.** The UI waits until the benchmark is complete, because it depends on results that do not exist yet. The UI sections below are parked here so nothing is lost.

## What ToolPrune is

A retrieval layer for AI agents with many tools. An LLM annotates each MCP tool once with facets (function, domain, effect, a "not for" line). At query time a router prunes the catalog so the agent sees about 5 tools, not 500.

One-line pitch: **Your agent sees the 5 tools it needs, not the 500 it doesn't.**

Why it matters:
- Fewer tokens per agent turn than loading every tool definition.
- Fewer wrong picks where tool names or descriptions collide (`search`, `fetch`, `read_file` across servers).
- The agent never reads raw third-party tool descriptions, which can contain injected instructions.
- Optional least-privilege filter: destructive tools stay hidden unless the task needs them.

Audience: hackathon judges first, then MCP and agent developers running large tool catalogs.

Tone: precise, technical, a little dry. Engineering tool, not a consumer app. Confident without hype. No claim of "state of the art."

## Logo (the only deliverable now)

Name: **ToolPrune**. The idea to express: pruning a tree of tools down to the few that matter.

Ideas to explore, pick the strongest or combine:
- A branching tree or hierarchy (L0, L1, tool) with most branches cut and a few kept.
- Pruning shears or a clean cut line across a branch.
- A funnel or filter shape made of tool-like nodes.
- A wordmark where one letter carries the cut or the branch.

Requirements:
- **SVG**, hand-written, no raster, no external fonts required. Convert text to paths, or use a font stack that falls back safely.
- Delivered as: full logo (mark plus wordmark), mark only, and a monochrome version.
- Works on both light and dark backgrounds. Provide both colour variants, or use `currentColor` for the monochrome one.
- Legible at 16 px (favicon) and at 512 px (social avatar).
- Square avatar crop for the X post, and a wide banner crop.
- Restrained palette: one accent colour plus neutrals. Avoid generic AI gradients, robots, brains, circuit boards, and sparkles.
- Do not imitate any existing brand, and do not use a trademarked shape.

Output location: `assets/brand/` in the repo.
- `logo.svg`, `logo-mark.svg`, `logo-mono.svg`
- `logo-dark.svg` if the colour version differs on dark
- a short `assets/brand/README.md` stating the palette (hex values) and clear-space rule

Process: produce 3 distinct directions first as separate SVGs, with one line of rationale each. Then refine the chosen one. Do not ship a single option without alternatives.

## Constraints from the hackathon

- neatHack, Oct 10 to 12, 2026 (IST). All code and assets are written during the event, in a public repo with commits dated in that window.
- Never commit secrets or keys.
- The demo video is 3 minutes at most. Any UI must serve that demo.
- Building in public: small commits, clear messages.

## UI (parked until the benchmark is complete)

Stack decision from the draft: **Streamlit**. Python 3.12. Confirm before building.

Planned views, in priority order:

1. **Live router demo.** Type a task. Show the full catalog size, the pruned set, tokens before and after, and the route (L1 domain, then tools). Side by side with embedding top-k and BM25 for the same query. This is the demo centrepiece.
2. **Results ladder.** Table and chart of BM25, embeddings, enriched embeddings, embedding plus rerank, and the router. Per-bucket recall, full-coverage, confusion rate, tokens, p50 latency, cost per query, with confidence intervals and paired win/loss counts.
3. **Failure explorer.** Pick a query where a baseline failed. Show the gold tools, what each system returned, and the confuser that won.
4. **Tool-universe treemap.** Category, then server, then tool (data exists today in `data/processed/tools.jsonl`). Later add L1 domain once the taxonomy exists.
5. **Catalog audit.** Groups of tools with colliding names or descriptions, and tools whose descriptions contain instruction-like text.
6. **Injection demo.** A planted instruction in a tool description. Show full-context loading exposed to it versus the router, which never passes raw descriptions on.

Data contracts the UI will read (so UI and evaluation stay decoupled):
- `data/processed/tools.jsonl`: `id, server, server_category, name, description, input_schema, annotations, name_collision_count`.
- `data/processed/eval_set.jsonl` (frozen after review): query text, bucket, gold slots (with alternates), confusers, split.
- `data/processed/annotations.jsonl` (enricher output): L0, L1, effect, inputs and outputs, "not for", summary, `contains_instructions`.
- `reports/results.json` (to be defined by the evaluation step): per system, per query, the returned tool ids, token counts, latency, cost, and per-bucket aggregates.

UI principles:
- Show numbers, not claims. Every headline figure links to the underlying table.
- Label synthetic or derived queries wherever they appear.
- Report the full comparison, including bucket where the router loses.
- Light and dark themes. Legible on a projector.

## Open items

- Confirm Streamlit versus a custom web page.
- Brand direction approval: pick the logo direction before any UI colours are fixed.
- Final accent colour, taken from the chosen logo.
- Demo script (3 minutes), which decides which UI views make the cut.
