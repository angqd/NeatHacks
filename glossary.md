# ToolPrune glossary

One name per thing. Use these terms in code, reports, commits, and the README. If a term is missing, add it here first.

## 1. Source data (from LiveMCPBench, raw)

| Term | Meaning | Count |
| --- | --- | --- |
| **Server** | An MCP server, for example `MCP Music Analysis`. Published by a third party, not by us. | 70 |
| **Tool** | One callable on a server. Its id is `<server>::<tool name>`, for example `MCP Music Analysis::mfcc`. | 527 |
| **Catalog** | All 70 servers and 527 tools together. The retrieval universe. | 1 |
| **Raw tool document** | The text of a tool as the source gives it: tool name, description, server name, and input schema. Nothing of ours. | per tool |
| **Server category** | The bench's coarse label for a server (`Discovery`, `Finance`, `Code`, ...). Raw source metadata. Not shown to any system. | 8 values |
| **Task** | A bench task: question, answer, task category, annotator steps, reference tool list. | 95 |
| **Task category** | The bench's label for a task (`Office`, `Travel`, ...). Not shown to any system. | 6 values |
| **Reference tool list** | The tool names the bench annotator used in their solution. A hint for gold, not exact gold. | per task |

## 2. Eval annotations (ours, used only for scoring)

No system under test ever sees these.

| Term | Meaning |
| --- | --- |
| **Eval set** | The frozen 60 queries in `data/processed/eval_set.jsonl`. |
| **Query** | One natural-language request in the eval set. Field `question`. |
| **Gold slot** | One capability the query requires. Fields `slots`. A query has 1 or more. |
| **Pick** | The one tool chosen as the answer for a slot. |
| **Alternate** | Another tool that would also satisfy the slot. |
| **Acceptable tools** | A slot's pick plus its alternates. Recall and precision are scored against this. |
| **Confuser** | A plausible tool that is wrong for the query, with a reason. Tracked separately. |
| **Challenge bucket** | Why the query is hard: `semantic_distance`, `taxonomy_collision`, `multi_capability`, `near_duplicate`, `ambiguity`, or `none`. Field `bucket`. |
| **Task family** | What kind of job the query is about (`academic_search`, `geo_location`, ...). 15 values. Field `family`. Assigned by the labeler from the query alone. It is not the enricher's taxonomy. |
| **Derived query** | A rewrite of a bench task made to fill a thin challenge bucket. Field `derived`. |
| **Split** | `dev` (18) or `test` (42). Never tune on test. |

## 3. ToolPrune internals (ours, used only by the enricher and the router)

| Term | Meaning |
| --- | --- |
| **Enricher** | The offline LLM pass that annotates tools and servers. Reads raw tool documents only. Never sees queries. |
| **Facets** | The enricher's per-tool fields: function group, domain, effect (`read`, `write`, `destructive`), inputs and outputs, a "not for" line, a summary. |
| **Server card** | The enricher's per-server annotation: summary, what it is for and not for, sub-groups. |
| **Taxonomy** | The fixed, versioned label set the enricher assigns from (`taxonomy_v1.json`). |
| **Function group (L0)** | Top level of the taxonomy. Optional. Added only if domain clusters are too large. |
| **Domain (L1)** | Second level of the taxonomy, for example `image`, `contact info`. |
| **Enriched tool document** | The raw tool document plus its facets. |
| **Router** | The online component that prunes the catalog using the taxonomy and enriched documents. |

## 4. Systems and outputs

| Term | Meaning |
| --- | --- |
| **System** | Anything that takes a query and returns tools: a baseline or the router. |
| **Baseline** | A system without our taxonomy: full catalog in context, BM25, embedding top-k, embedding plus rerank. |
| **Returned set** | The ranked tool ids a system returns for one query. Field type `RetrievedSet`. |
| **Hit** | A gold slot is hit when the returned set contains any of its acceptable tools. |
| **Unjudged tool** | A returned tool that is not acceptable and not a listed confuser. |
| **Judge** | An LLM that rates a returned set (sufficiency) and labels unjudged tools. |

## Who may see what

| | Raw tool documents | Server category, task category | Taxonomy, facets, server cards | Eval annotations (gold, bucket, family, confuser) |
| --- | --- | --- | --- | --- |
| Baselines | yes | no | no | no |
| Enricher | yes | no | writes them | no |
| Router | yes | no | yes | no |
| Scorer | yes | yes | no | yes |
| Judges | yes | no | no | no gold, no system identity |

Two rules follow:

1. Only the enricher and the router touch our taxonomy. Baselines run on raw tool documents, as an ordinary MCP client would.
2. Eval annotations never reach a system. The task family and challenge bucket exist for reporting only.

## Writing rule for reports

Say what the thing is. Write "the returned set held three tools from the server `MCP Music Analysis`", not "BM25 sent the query to a bucket" or "to music tools". A server is a server, a challenge bucket is a challenge bucket, and a domain is a domain.
