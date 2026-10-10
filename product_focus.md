# ToolPrune: product focus

Parked here to revisit after the POC is complete. The POC results decide which parts of this stay true.

## Who pays for enrichment

- Enrichment is a one-time, cacheable cost. About 527 tools times one small-model call is a few dollars, cached by content hash and re-run only when a tool's docs change.
- Cost scales with catalog size, not with traffic. It is amortized over every query afterwards, while loading a large catalog into context costs tokens on every agent turn.
- The catalog owner pays.
  - Self-host: the team running the agent, as a build step like indexing.
  - Hosted registry or gateway: the operator pays once and serves many tenants. Public MCP tools are shared across tenants, so the cost is amortized again.
- Private and internal tools are enriched on the customer's side, so their docs never leave.
- The hard sell is not the cost. It is proving that enrichment beats plain embeddings. The ablation (enriched embeddings, no hierarchy) tests this.

## Fit

A retrieval layer for agents with many tools, in three tiers:

1. MCP `find_tools` server or gateway. The agent asks for tools by task and sees about 5 tools, not 500. This is the core product (Phase 3 in `Idea_Draft.md`).
2. Least-privilege filter. The effect facet (read, write, destructive) lets a gateway hide destructive tools unless the task needs them. Plain embedding search cannot offer this.
3. Catalog audit. A report on colliding descriptions, such as "these 12 of your tools are indistinguishable." Cheap to produce, shareable, and good for building in public.

Not the lead: a public catalog of MCPs. Directories already exist and are commodity. A catalog is a feature, not the product.

## When the pitch is true

- Small catalogs (10 to 30 tools) do not need this. Loading everything is fine. Say so.
- The wedge is noisy catalogs: past roughly 100 tools, especially where names collide (`search`, `fetch`, `read_file` across servers) or where third-party MCPs are outside your control.
- Who feels it: agent platforms, MCP gateways and registries, and enterprises wiring many internal tools into one agent.

## Promotion

- Lead with numbers: tokens per query and confusion rate versus loading everything and versus plain embeddings.
- Demo one failure case: embedding search returns the wrong `search` tool, ours returns the right one, with the neatlogs trace.
- Publish the catalog audit as a concrete finding about real MCP servers.
- State the enrichment cost openly, for example "one-time, about $X per 500 tools."

## What could sink the pitch

- If plain enriched embeddings match the hierarchy, the router is not the product. Enrichment is, and the product narrows to a build-time step.
- If baselines already score above 90% on the hard buckets, the "extremely noisy" claim does not hold on this data, and the case rests on cost alone.
- Enrichment goes stale. The cache-by-hash and re-annotate-on-change story has to work in practice.

## Comparisons the POC must answer

| Baseline | What we measure | What counts as a win |
| --- | --- | --- |
| Full catalog in context | LLM picks tools from all 527 definitions; exact token count | Context 10x smaller or more, lower latency, recall within a few points |
| Embedding top-k | Raw-text embeddings | Better recall and fewer confusers on collision, near-duplicate, and multi-tool tags; latency loss accepted |
| BM25 | Name, description, server text | Better on semantic-distance and collision tags; latency loss accepted |
| Embedding shortlist plus LLM rerank | Draft rung 4 | Parity or better on confusion rate at equal or lower tokens |

Ablation: enriched embeddings with no hierarchy (draft rung 3).

Minimal viable proof: beat the full catalog on tokens and speed, beat BM25 and embedding on at least 2 or 3 hard buckets, reach parity with embedding plus rerank at lower tokens. If the last fails, enrichment is the product and the router is optional.
