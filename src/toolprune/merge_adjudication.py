"""Merge adjudicated_*.jsonl with tagged tasks into data/processed/tasks_reviewed.jsonl and validate ids.

Run: .venv/bin/python -m toolprune.merge_adjudication
"""

import collections
import glob
import json
from pathlib import Path

PROC = Path(__file__).resolve().parents[2] / "data" / "processed"


def read_jsonl(path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main() -> None:
    tools = {t["id"] for t in read_jsonl(PROC / "tools.jsonl")}
    tagged = {t["task_id"]: t for t in read_jsonl(PROC / "tasks_tagged.jsonl")}
    adj = {}
    for path in sorted(glob.glob(str(PROC / "adjudicated_*.jsonl"))):
        for r in read_jsonl(path):
            adj[r["task_id"]] = r
    problems: list[str] = []
    out = []
    for tid, task in tagged.items():
        a = adj.get(tid)
        if not a:
            problems.append(f"{tid}: not adjudicated")
            continue
        names = [s["gold_name"] for s in a["slots"]]
        if names != task["gold_names"]:
            problems.append(f"{tid}: slot names differ")
        for s in a["slots"]:
            for i in [s["pick"], *s["alternates"]]:
                if i and i not in tools:
                    problems.append(f"{tid}: unknown tool id {i}")
        for c in a["confusers"]:
            if c["tool_id"] not in tools:
                problems.append(f"{tid}: unknown confuser {c['tool_id']}")
        out.append({**a, "question": task["question"], "category": task["category"],
                    "original_gold_ids": task["gold_ids"]})
    with open(PROC / "tasks_reviewed.jsonl", "w", encoding="utf-8") as fh:
        for r in out:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"merged {len(out)} tasks, {len(problems)} problems")
    for p in problems[:20]:
        print(" ", p)
    print("confidence", dict(collections.Counter(r["confidence"] for r in out)))
    print("escalate", sum(r["escalate"] for r in out), "divergent", sum(r["divergent"] for r in out))
    print("primary", dict(collections.Counter(r["primary_bucket"] for r in out)))
    fam = collections.Counter(r["task_family"] for r in out)
    print(len(fam), "families", fam.most_common(15))


if __name__ == "__main__":
    main()
