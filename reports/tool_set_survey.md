# Tool set survey: large catalogs for a retrieval scale test

Date: 2026-10-11. Scope: public tool sets and MCP registries that could serve as a large distractor catalog (thousands to tens of thousands of tools). Method: web search plus WebFetch on the pages listed. No files were downloaded. Where a figure was not found, it is marked "not found". Figures taken from search snippets or third-party listings are marked as such.

## Comparison table

| # | Candidate | Size (as stated) | Bulk tool-level data (name, description, schema) | How to get it | License / terms | Ships queries and gold tools | Verified |
|---|---|---|---|---|---|---|---|
| 1 | MCP-Zero "MCP-tools" | 308 servers, 2,797 tools | Yes in the file, but param is a simplified map, not a full JSON Schema. Each tool has name, description, parameter, plus 3072-d embeddings | Google Drive link (`mcp_tools_with_embedding.json`). HF link "coming soon" | Repo MIT. No separate dataset license stated | No query set described. Only `test_cases.jsonl` for a matcher unit test | Repo README via WebFetch. Drive file not downloaded |
| 2 | MCP-Flow | 1,166 servers, 11,536 tools; 68,733 instruction-function call pairs; 6,439 trajectories (arXiv abstract) | Repo lists `data/tools/` ("tool descriptions and schema definitions"). Field layout not seen | HF `wwh0411/MCP-Flow` (per news item and repo), plus `server_info_with_description_v3.json` in repo | Not stated (no LICENSE in repo view) | Yes: instruction-function call pairs and test sets on HF (`test_data`). Gold structure not seen | Abstract and repo via WebFetch. HF page not fetched |
| 3 | ToolBench / StableToolBench | ToolBench: 16,464 REST APIs (RapidAPI), statistics table also says 3,451 tools. StableToolBench: third-party listing says 7,437 APIs, 49 categories (not verified against paper) | Yes: `toolenv/` has API JSONs with tool name, description, URL, method, parameters | data.zip on Google Drive or Tsinghua Cloud. RapidAPI backend needs a form. StableToolBench data on HF (`stabletoolbench/*`) | ToolBench repo Apache-2.0; data "for research and educational purposes" only; RapidAPI API terms not addressed | Yes: instructions and queries with solution paths (exact format not checked) | ToolBench repo via WebFetch. HF pages via search only |
| 4 | Official MCP registry | Server list only (`/v0/servers`). Total count not found | No. List entries have name, description, remotes, status. No tools or schemas | Public REST, no key seen. Paginated with `metadata.nextCursor` | Not checked | No | Live `/v0/servers?limit=5` fetched |
| 5 | Smithery | Count not found | Per-server tool data at `api.smithery.ai/servers/{qualifiedName}` (per docs, schema not seen) | Registry list needs bearer token (`registry.smithery.ai/servers`) | Not checked | No | Docs via search only |
| 6 | Glama | Count not found | Not found in API docs seen | API key required; 100 req/s; cursor pagination | API Data License: must credit Glama, link each listing | No | Search snippets only |
| 7 | PulseMCP | Count not found | Not bulk. Per-query API (`list_servers`, up to 5,000 per page per a third-party wrapper) | API key and tenant ID by contacting PulseMCP | Not checked | No | Search snippets only |
| 8 | mcp.so | Not checked | Not checked | Not checked | Not checked | No | Not verified |
| 9 | LiveMCPBench (our current source) | 70 servers, 527 tools, 95 tasks (HF page) | Yes in `tools/tools.json` (already in repo) | HF `ICIP/LiveMCPBench` | Apache-2.0 (HF tag). Repo still lists terms check as open | Yes: 95 tasks with answers and reference tools | HF page via WebFetch |
| 10 | TheMCPCompany (arXiv 2510.19286) | 18,505 tools per third-party AlphaXiv listing; 192 tasks. Azure is 16,837 of those | Not found | No GitHub or HF link found | Not found | Yes (192 tasks) per listing; gold labels not verified | Paper abstract via search only |
| 11 | HumanMCP (arXiv 2602.23367) | 2,800 tools, 308 servers (abstract) | Not found | Not found | Not found | Queries built from user personas. Count not found | Abstract via WebFetch |
| 12 | MCPVerse (arXiv 2508.16260) | 550+ executable tools; server count not found | Not found | Not found | Not found | Not found | Abstract via WebFetch |

## Notes per candidate

**1. MCP-Zero (github.com/xfey/MCP-Zero).** The README states 308 servers and 2,797 tools from the official MCP repo. This is the only candidate whose tool format is already close to ours (name, description, parameters per tool, grouped by server). Blocker: the JSON sits on Google Drive, not HF, and the HF link is "coming soon". The `parameter` field is a simplified dict, so input schemas may need reconstruction. Its embeddings were built with text-embedding-3-large, which we would need to drop or recompute. Tool descriptions and quality were not inspected. Duplicate names and missing descriptions are unknown.

**2. MCP-Flow (github.com/wwh0411/MCP-Flow).** The largest MCP-specific corpus with a stated count (1,166 servers, 11,536 tools) and a query-side resource (68k+ instruction-function call pairs, test sets). Data is said to be on HF. The license is not stated anywhere I could see, which is a blocker for anything redistributed. Tool-level field layout was not confirmed. The arXiv page's CC BY 4.0 label covers the paper, not the data.

**3. ToolBench / StableToolBench.** Apache-2.0 for the repo, and tool JSON with parameters is included. The count is inconsistent across sources: 16,464 APIs versus 3,451 tools in the same README, so "tools" must be defined before use. These are RapidAPI REST APIs, not MCP tools, so each would need converting to our `{server, name, description, input_schema}` shape. The RapidAPI backend needs a request form for live calls, but offline tool JSON does not. Data is distributed via Google Drive, which is a manual download step. Terms say research and education only.

**4. Official MCP registry.** Useful for finding servers, not for tools. The list endpoint returns no tool definitions. Building a tool catalog would mean running each server and calling `tools/list`, which many servers cannot do without credentials. Not a bulk source.

**5-7. Smithery, Glama, PulseMCP.** All are directories with per-server APIs. Smithery and Glama need keys. Glama's API license requires attribution on every data page. None gives a bulk dump I could verify. Treat them as sources of server names to cross-check, not as tool catalogs.

**8. mcp.so.** Not checked.

**10-12. TheMCPCompany, HumanMCP, MCPVerse.** Large tool counts are claimed (18k, 2.8k, 550+). I did not find a released tool dump for any of them. TheMCPCompany is 91% Azure tools, so it is skewed. Treat as unavailable until a repo is found.

## Ranked recommendation (for a retrieval scale test that keeps our 60 queries and adds distractors)

**1. MCP-Zero MCP-tools (2,797 tools, 308 servers).** Best format fit: real MCP servers and tools, names and descriptions per tool, MIT repo. The 60 queries stay as the gold set; the 527 LiveMCPBench tools remain the gold pool, and MCP-Zero tools are added as distractors.
- Blocker: the JSON is on Google Drive. Not downloaded, so content, duplicates, and missing descriptions are unverified.
- Steps: (1) download the Drive file by hand into a scratch dir and check its size (over 5 MB rules out a direct fetch); (2) write a script (kept outside the repo) that reads it with `python -I`, flattens to `{server, name, description, input_schema}`, and reconstructs schemas from `parameter`; (3) dedupe by (server, name); drop tools whose name collides with a gold tool so the gold set is unchanged; (4) emit jsonl; (5) recompute embeddings only if our retriever needs them. Rough time: 0.5 to 1 day, most of it on schema reconstruction and the license check.

**2. MCP-Flow (1,166 servers, 11,536 tools).** Larger scale, MCP-specific, and HF-hosted, so the download is straightforward.
- Blocker: no license stated, so it cannot be redistributed. Internal testing may still be acceptable, but this needs confirmation. The tool field layout is also unverified.
- Steps: (1) open the HF dataset card and file tree for `wwh0411/MCP-Flow` and find the tools file (`data/tools/` or `server_info_with_description_v3.json`); (2) download if under 5 MB, else sample with a streaming read; (3) inspect 20 records against the schema we need; (4) convert as above and dedupe; (5) keep only tools whose server is not already in our 70. Rough time: 1 to 2 days, most of it on the license question and format mapping.

Fallback if MCP-Flow's license fails: ToolBench (Apache-2.0 code, tool JSON included), with the caveat that its tools are RapidAPI APIs and the count needs defining.

## Verified vs not verified

Verified by fetch or search: MCP-Zero counts and file layout (README, via WebFetch); MCP-Flow counts (arXiv abstract); LiveMCPBench counts, license, and file list (HF page); ToolBench license and data source (GitHub README); official registry list response shape (live fetch of a 5-item page); Glama API terms (search snippet from docs); PulseMCP access (search snippet only).

Not verified: contents of any downloaded file (nothing was downloaded); the MCP-Zero Drive file; the MCP-Flow HF files and their license (repo view does not show a LICENSE); the StableToolBench HF file list; the HF page for `xfey/MCP-tools` (returned HTTP 401, so it may be gated or absent); TheMCPCompany, HumanMCP, and MCPVerse data releases (none found); Smithery, Glama, PulseMCP, and mcp.so counts and tool schemas; whether any candidate's tools duplicate LiveMCPBench servers.
