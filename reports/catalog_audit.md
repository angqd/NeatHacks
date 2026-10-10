# Catalog audit

Source: `data/processed/tools.jsonl` via `load_tools()`.

## 1. Counts

| Measure | Value |
|---|---|
| Servers | 70 |
| Tools | 527 |
| Tools per server (min / median / max) | 1 / 4.0 / 35 |
| Single-tool servers | 12 |
| Servers with 15+ tools | 10 |

Five largest servers:

| Server | Tools |
|---|---|
| Office-PowerPoint-MCP-Server | 35 |
| Playwright MCP Server | 32 |
| MCP Server Chart | 25 |
| Office-Word-MCP-Server | 24 |
| OP.GG MCP Server | 22 |

## 2. Name collisions

| Measure | Value |
|---|---|
| Distinct names shared by 2+ tools | 13 |
| Tools involved | 30 |

Ten most shared names:

| Name | Tools | Servers |
|---|---|---|
| search | 4 | BioMCP: Biomedical Model Context Protocol, Hacker News MCP Server, Web3 Research MCP, Yahoo Finance MCP Server |
| get_file_info | 3 | Desktop Commander MCP, Filesystem MCP Server, MCP OKPPT Server |
| list_directory | 3 | Basic Memory, Desktop Commander MCP, Filesystem MCP Server |
| add_table | 2 | Office-PowerPoint-MCP-Server, Office-Word-MCP-Server |
| create_directory | 2 | Desktop Commander MCP, Filesystem MCP Server |
| fetch | 2 | BioMCP: Biomedical Model Context Protocol, Fetch MCP Server |
| get_price_history | 2 | Yahoo Finance MCP Server, investor-agent: A Financial Analysis MCP Server |
| move_file | 2 | Desktop Commander MCP, Filesystem MCP Server |
| read_file | 2 | Desktop Commander MCP, Filesystem MCP Server |
| read_multiple_files | 2 | Desktop Commander MCP, Filesystem MCP Server |

## 3. Descriptions

| Measure | Value |
|---|---|
| Missing or under 30 chars | 66 |
| Median length (chars) | 61 |
| Max length (chars) | 3866 |
| Containing CJK characters | 62 |

Ids (up to 10): `Bing_CN_MCP::fetch_webpage`, `MCP Yahoo Finance::get_earning_dates`, `OP.GG MCP Server::valorant-meta-maps`, `OP.GG MCP Server::valorant-meta-characters`, `HowToCook-MCP Server::mcp_howtocook_getAllRecipes`, `HowToCook-MCP Server::mcp_howtocook_whatToEat`, `HowToCook-MCP Server::mcp_howtocook_getRecipeById`, `Baige (ygocdb.com) MCP Server::search_cards`, `Baige (ygocdb.com) MCP Server::get_card_by_id`, `Baige (ygocdb.com) MCP Server::get_card_image`

## 4. Tokens (tiktoken o200k_base)

| Measure | Value |
|---|---|
| Total tokens, whole catalog | 100496 |
| Median tokens per tool | 118 |

Five heaviest tools:

| Tool id | Tokens |
|---|---|
| OP.GG MCP Server::tft-recommend-champion-for-item | 1932 |
| BioMCP: Biomedical Model Context Protocol::search | 1742 |
| OP.GG MCP Server::lol-champion-analysis | 1296 |
| MCP Server Chart::generate_district_map | 1239 |
| BioMCP: Biomedical Model Context Protocol::trial_searcher | 1061 |

## 5. Near-duplicate descriptions

Pairs on different servers with token-set Jaccard >= 0.8 and at least 6 tokens each: **1**.

| Tool A | Tool B | Jaccard |
|---|---|---|
| Playwright MCP Server::playwright_screenshot | Puppeteer::puppeteer_screenshot | 1.0 |

## 6. Instruction-like text (HEURISTIC)

Tools whose description matches a keyword pattern: **38**.

These are candidates for review, not confirmed injections. Tool text is quoted data.

| Tool id | Matched phrases |
|---|---|
| OP.GG MCP Server::lol-champion-analysis | `always `, `you must`, `you should` |
| OP.GG MCP Server::lol-summoner-search | `always ` |
| OP.GG MCP Server::lol-summoner-game-history | `always ` |
| OP.GG MCP Server::lol-summoner-renewal | `always ` |
| BioMCP: Biomedical Model Context Protocol::search | `do not`, `important` |
| BioMCP: Biomedical Model Context Protocol::fetch | `always `, `ignore` |
| BioMCP: Biomedical Model Context Protocol::think | `important`, `use this tool`, `you must` |
| BioMCP: Biomedical Model Context Protocol::article_searcher | `important`, `use this tool` |
| BioMCP: Biomedical Model Context Protocol::variant_searcher | `important` |
| Sequential Thinking MCP Server::sequentialthinking | `don't`, `ignore`, `use this tool`, `you should` |
| Context7 MCP - Up-to-date Code Docs For Any Prompt::resolve-library-id | `you must` |
| Context7 MCP - Up-to-date Code Docs For Any Prompt::get-library-docs | `use this tool`, `you must` |
| MCP Text Editor Server::edit_text_file_contents | `before using`, `don't`, `important`, `you must` |
| MCP TaskManager::request_planning | `always `, `do not`, `important`, `you must` |
| MCP TaskManager::get_next_task | `before calling`, `do not`, `you must` |

## 7. Schema

| Measure | Value |
|---|---|
| Annotations present | 8.3% |
| readOnlyHint set | 8.3% |
| destructiveHint set | 4.2% |
| Median input parameters | 2 |
