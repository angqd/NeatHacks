"""Catalog audit: counts, name collisions, description quality, tokens, near-duplicates,
instruction-like text and schema shape, over the full catalog from load_tools().

Tool text is quoted data. Nothing here reads a description as an instruction. The
instruction-like section is a keyword heuristic that flags candidates for human review.
It does not confirm injections.

Writes reports/catalog_audit.json and reports/catalog_audit.md.
Run with: python -m toolprune.eval.audit
"""

import json
import re
import statistics
from collections import Counter, defaultdict
from itertools import combinations
from typing import Any

from toolprune.eval.tokens import _definition_text, _encoding, ENCODING_NAME
from toolprune.models import ROOT, Tool, load_tools
from toolprune.text import tokenize

REPORTS_DIR = ROOT / "reports"
SHORT_DESCRIPTION = 30
LARGE_SERVER = 15
NEAR_DUP_JACCARD = 0.8
NEAR_DUP_MIN_TOKENS = 6
CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯豈-﫿]")
INSTRUCTION_PHRASES = (
    "you must", "you should", "always ", "never ", "do not", "don't", "ignore",
    "before using", "before calling", "important", "call this tool first", "use this tool",
)
INSTRUCTION_RE = re.compile("|".join(re.escape(p) for p in INSTRUCTION_PHRASES), re.IGNORECASE)


def count_tokens(tool: Tool) -> int:
    return len(_encoding().encode(_definition_text(tool)))


def server_section(tools: list[Tool]) -> dict[str, Any]:
    by_server: dict[str, int] = Counter(t.server for t in tools)
    sizes = list(by_server.values())
    largest = by_server.most_common(5)
    return {
        "servers": len(by_server),
        "tools": len(tools),
        "tools_per_server": {
            "min": min(sizes),
            "median": statistics.median(sizes),
            "max": max(sizes),
        },
        "single_tool_servers": sum(1 for n in sizes if n == 1),
        f"servers_with_{LARGE_SERVER}_plus_tools": sum(1 for n in sizes if n >= LARGE_SERVER),
        "largest_servers": [{"server": s, "tools": n} for s, n in largest],
    }


def collision_section(tools: list[Tool]) -> dict[str, Any]:
    by_name: dict[str, list[Tool]] = defaultdict(list)
    for t in tools:
        by_name[t.name].append(t)
    shared = {name: group for name, group in by_name.items() if len(group) >= 2}
    ranked = sorted(shared.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return {
        "shared_names": len(shared),
        "tools_involved": sum(len(g) for g in shared.values()),
        "top_shared_names": [
            {
                "name": name,
                "tools": len(group),
                "servers": sorted(t.server for t in group),
            }
            for name, group in ranked[:10]
        ],
    }


def description_section(tools: list[Tool]) -> dict[str, Any]:
    short = [t for t in tools if len(t.description.strip()) < SHORT_DESCRIPTION]
    lengths = [len(t.description) for t in tools]
    return {
        "missing_or_under_30_chars": len(short),
        "missing_or_under_30_chars_examples": [t.id for t in short[:10]],
        "median_chars": statistics.median(lengths),
        "max_chars": max(lengths),
        "with_cjk": sum(1 for t in tools if CJK.search(t.description)),
    }


def token_section(tools: list[Tool]) -> dict[str, Any]:
    counts = {t.id: count_tokens(t) for t in tools}
    heaviest = sorted(tools, key=lambda t: (-counts[t.id], t.id))[:5]
    return {
        "encoding": ENCODING_NAME,
        "total_tokens": sum(counts.values()),
        "median_tokens_per_tool": statistics.median(counts.values()),
        "heaviest_tools": [{"id": t.id, "tokens": counts[t.id]} for t in heaviest],
    }


def near_duplicate_section(tools: list[Tool]) -> dict[str, Any]:
    eligible = []
    for t in tools:
        tokens = set(tokenize(t.description))
        if len(tokens) >= NEAR_DUP_MIN_TOKENS:
            eligible.append((t, tokens))
    pairs = []
    for (a, ta), (b, tb) in combinations(eligible, 2):
        if a.server == b.server:
            continue
        jaccard = len(ta & tb) / len(ta | tb)
        if jaccard >= NEAR_DUP_JACCARD:
            pairs.append((jaccard, a.id, b.id))
    pairs.sort(key=lambda p: (-p[0], p[1], p[2]))
    return {
        "count": len(pairs),
        "min_jaccard": NEAR_DUP_JACCARD,
        "min_tokens_each": NEAR_DUP_MIN_TOKENS,
        "examples": [{"a": a, "b": b, "jaccard": round(j, 3)} for j, a, b in pairs[:10]],
    }


def instruction_section(tools: list[Tool]) -> dict[str, Any]:
    hits = []
    for t in tools:
        phrases = sorted({m.group(0).lower() for m in INSTRUCTION_RE.finditer(t.description)})
        if phrases:
            hits.append({"id": t.id, "matched": phrases})
    return {
        "label": "HEURISTIC: candidates for review, not confirmed injections",
        "count": len(hits),
        "examples": hits[:15],
    }


def schema_section(tools: list[Tool]) -> dict[str, Any]:
    total = len(tools)
    annotated = [t for t in tools if t.annotations]
    read_only = sum(1 for t in tools if t.annotations and t.annotations.get("readOnlyHint") is not None)
    destructive = sum(1 for t in tools if t.annotations and t.annotations.get("destructiveHint") is not None)
    param_counts = [len((t.input_schema.get("properties") or {})) for t in tools]
    return {
        "annotations_present_share": round(len(annotated) / total, 4),
        "readOnlyHint_set_share": round(read_only / total, 4),
        "destructiveHint_set_share": round(destructive / total, 4),
        "median_input_parameters": statistics.median(param_counts),
    }


def build_report(tools: list[Tool]) -> dict[str, Any]:
    return {
        "1_counts": server_section(tools),
        "2_name_collisions": collision_section(tools),
        "3_descriptions": description_section(tools),
        "4_tokens": token_section(tools),
        "5_near_duplicates": near_duplicate_section(tools),
        "6_instruction_like_heuristic": instruction_section(tools),
        "7_schema": schema_section(tools),
    }


def table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(str(c).replace("|", "\\|") for c in row) + " |" for row in rows]
    return lines


def render_markdown(r: dict[str, Any]) -> str:
    c, col, d, tok = r["1_counts"], r["2_name_collisions"], r["3_descriptions"], r["4_tokens"]
    nd, ins, sch = r["5_near_duplicates"], r["6_instruction_like_heuristic"], r["7_schema"]
    per = c["tools_per_server"]
    out = ["# Catalog audit", "", "Source: `data/processed/tools.jsonl` via `load_tools()`.", ""]

    out += ["## 1. Counts", ""]
    out += table(["Measure", "Value"], [
        ["Servers", c["servers"]],
        ["Tools", c["tools"]],
        ["Tools per server (min / median / max)", f"{per['min']} / {per['median']} / {per['max']}"],
        ["Single-tool servers", c["single_tool_servers"]],
        [f"Servers with {LARGE_SERVER}+ tools", c[f"servers_with_{LARGE_SERVER}_plus_tools"]],
    ])
    out += ["", "Five largest servers:", ""]
    out += table(["Server", "Tools"], [[s["server"], s["tools"]] for s in c["largest_servers"]])

    out += ["", "## 2. Name collisions", ""]
    out += table(["Measure", "Value"], [
        ["Distinct names shared by 2+ tools", col["shared_names"]],
        ["Tools involved", col["tools_involved"]],
    ])
    out += ["", "Ten most shared names:", ""]
    out += table(["Name", "Tools", "Servers"], [
        [n["name"], n["tools"], ", ".join(n["servers"])] for n in col["top_shared_names"]
    ])

    out += ["", "## 3. Descriptions", ""]
    out += table(["Measure", "Value"], [
        [f"Missing or under {SHORT_DESCRIPTION} chars", d["missing_or_under_30_chars"]],
        ["Median length (chars)", d["median_chars"]],
        ["Max length (chars)", d["max_chars"]],
        ["Containing CJK characters", d["with_cjk"]],
    ])
    if d["missing_or_under_30_chars_examples"]:
        out += ["", "Ids (up to 10): " + ", ".join(f"`{i}`" for i in d["missing_or_under_30_chars_examples"])]

    out += ["", "## 4. Tokens (tiktoken " + tok["encoding"] + ")", ""]
    out += table(["Measure", "Value"], [
        ["Total tokens, whole catalog", tok["total_tokens"]],
        ["Median tokens per tool", tok["median_tokens_per_tool"]],
    ])
    out += ["", "Five heaviest tools:", ""]
    out += table(["Tool id", "Tokens"], [[t["id"], t["tokens"]] for t in tok["heaviest_tools"]])

    out += ["", "## 5. Near-duplicate descriptions", ""]
    out += [
        f"Pairs on different servers with token-set Jaccard >= {nd['min_jaccard']} "
        f"and at least {nd['min_tokens_each']} tokens each: **{nd['count']}**.",
        "",
    ]
    out += table(["Tool A", "Tool B", "Jaccard"], [[e["a"], e["b"], e["jaccard"]] for e in nd["examples"]])

    out += ["", "## 6. Instruction-like text (HEURISTIC)", ""]
    out += [
        f"Tools whose description matches a keyword pattern: **{ins['count']}**.",
        "",
        "These are candidates for review, not confirmed injections. Tool text is quoted data.",
        "",
    ]
    out += table(["Tool id", "Matched phrases"], [[e["id"], ", ".join(f"`{p}`" for p in e["matched"])] for e in ins["examples"]])

    out += ["", "## 7. Schema", ""]
    out += table(["Measure", "Value"], [
        ["Annotations present", f"{sch['annotations_present_share']:.1%}"],
        ["readOnlyHint set", f"{sch['readOnlyHint_set_share']:.1%}"],
        ["destructiveHint set", f"{sch['destructiveHint_set_share']:.1%}"],
        ["Median input parameters", sch["median_input_parameters"]],
    ])
    return "\n".join(out) + "\n"


def main() -> None:
    tools = load_tools()
    report = build_report(tools)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORTS_DIR / "catalog_audit.json"
    md_path = REPORTS_DIR / "catalog_audit.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
