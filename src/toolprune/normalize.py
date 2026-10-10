"""Stage 1: normalize raw LiveMCPBench files into per-tool and per-task JSONL. No LLM.

Run: python -m toolprune.normalize
"""

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"

NUMBERED = re.compile(r"^\s*\d+\.\s*(.+?)\s*$")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_tools(path: Path) -> list[dict]:
    """Flatten the server list into one dict per tool."""
    servers = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for server in servers:
        for config_name, block in server["tools"].items():
            for tool in block.get("tools", []):
                rows.append(
                    {
                        "id": f"{server['name']}::{tool['name']}",
                        "server": server["name"],
                        "server_category": server.get("category"),
                        "server_description": server.get("description"),
                        "config_name": config_name,
                        "name": tool["name"],
                        "description": tool.get("description") or "",
                        "input_schema": tool.get("inputSchema"),
                        "annotations": tool.get("annotations"),
                    }
                )
    counts = Counter(r["name"] for r in rows)
    for r in rows:
        r["name_collision_count"] = counts[r["name"]]
    return rows


def parse_gold_names(tools_field: str) -> list[str]:
    names = []
    for line in tools_field.splitlines():
        line = line.strip()
        if not line:
            continue
        m = NUMBERED.match(line)
        names.append(m.group(1).strip() if m else line)
    return names


def _server_in_steps(server: str, steps: str) -> bool:
    pattern = r"(?<![A-Za-z0-9])" + re.escape(server.lower()) + r"(?![A-Za-z0-9])"
    return re.search(pattern, steps.lower()) is not None


def resolve_task(task: dict, by_name: dict[str, list[dict]]) -> dict:
    meta = task["Annotator Metadata"]
    steps = meta.get("Steps", "") or ""
    gold_names = parse_gold_names(meta.get("Tools", "") or "")
    resolution, gold_ids = [], []
    for name in gold_names:
        candidates = by_name.get(name, [])
        cand_ids = [c["id"] for c in candidates]
        if len(candidates) == 1:
            entry = {"name": name, "status": "unique", "candidates": cand_ids}
            gold_ids.append(cand_ids[0])
        elif len(candidates) > 1:
            entry = {"name": name, "status": "ambiguous", "candidates": cand_ids}
            matched = [c for c in candidates if _server_in_steps(c["server"], steps)]
            if len(matched) == 1:
                entry["resolved_by"] = "steps_server_match"
                entry["chosen"] = matched[0]["id"]
                gold_ids.append(matched[0]["id"])
            else:
                gold_ids.append(None)
        else:
            entry = {"name": name, "status": "missing", "candidates": []}
            gold_ids.append(None)
        resolution.append(entry)
    return {
        "task_id": task["task_id"],
        "question": task["Question"],
        "category": task.get("category"),
        "file_name": task.get("file_name", ""),
        "steps": steps,
        "gold_names": gold_names,
        "gold_ids": gold_ids,
        "resolution": resolution,
        "n_gold": len(gold_names),
        "fully_resolved": len(gold_names) > 0 and all(g is not None for g in gold_ids),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tools = load_tools(RAW_DIR / "tools.json")
    tasks = json.loads((RAW_DIR / "tasks.json").read_text(encoding="utf-8"))

    by_name: dict[str, list[dict]] = {}
    for t in tools:
        by_name.setdefault(t["name"], []).append(t)
    resolved = [resolve_task(task, by_name) for task in tasks]

    _write_jsonl(OUT_DIR / "tools.jsonl", tools)
    _write_jsonl(OUT_DIR / "tasks_resolved.jsonl", resolved)

    status = Counter(e["status"] for r in resolved for e in r["resolution"])
    steps_resolved = sum(
        1 for r in resolved for e in r["resolution"] if e.get("resolved_by") == "steps_server_match"
    )
    full = sum(r["fully_resolved"] for r in resolved)
    print(f"tools: {len(tools)} rows, {len({t['name'] for t in tools})} distinct names, "
          f"{len({t['server'] for t in tools})} servers")
    print(f"tasks: {len(resolved)} rows")
    print(f"gold mentions: unique={status['unique']} ambiguous={status['ambiguous']} "
          f"missing={status['missing']} (total {sum(status.values())})")
    print(f"ambiguous resolved by steps_server_match: {steps_resolved}")
    print(f"tasks fully resolved: {full} / {len(resolved)}")
    for r in resolved:
        for e in r["resolution"]:
            if e["status"] == "missing":
                print(f"  missing: task {r['task_id']} gold '{e['name']}'")


if __name__ == "__main__":
    main()
