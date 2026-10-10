"""Build the natural eval set: every original LiveMCPBench task, scored by the bench's own tool names.

No review, no adjudication, no alternates beyond same-name tools. Each task's distinct gold names
(from tasks_resolved.jsonl) are matched to catalog tools by exact name. The pick is the first
matching tool in catalog order, and the alternates are the other matching tools on any server.
A gold name with no catalog match is dropped, and a task left with no slots is dropped.

Run with: python -m toolprune.eval.build_natural
"""

import hashlib
import json

from toolprune.eval.sets import NATURAL_PATH
from toolprune.models import PROC_DIR, read_jsonl, load_tools

TASKS_PATH = PROC_DIR / "tasks_resolved.jsonl"
FROZEN_PATH = PROC_DIR / "eval_set.jsonl"


def main() -> None:
    tools_by_name: dict[str, list[str]] = {}
    for tool in load_tools():
        tools_by_name.setdefault(tool.name, []).append(tool.id)

    tasks = read_jsonl(TASKS_PATH)
    frozen_ids = {row["task_id"] for row in read_jsonl(FROZEN_PATH)}

    gold_total = 0
    gold_dropped = 0
    tasks_dropped = 0
    rows: list[dict] = []
    for task in tasks:
        distinct = list(dict.fromkeys(task["gold_names"]))
        gold_total += len(distinct)
        slots = []
        for name in distinct:
            candidates = tools_by_name.get(name, [])
            if not candidates:
                gold_dropped += 1
                continue
            slots.append({"gold_name": name, "pick": candidates[0], "alternates": candidates[1:]})
        if not slots:
            tasks_dropped += 1
            continue
        rows.append(
            {
                "task_id": task["task_id"],
                "question": task["question"],
                "category": task["category"],
                "bucket": "natural",
                "family": task["category"],
                "slots": slots,
                "confusers": [],
                "needs_clarification": False,
                "derived": False,
                "split": "test",
            }
        )

    NATURAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with NATURAL_PATH.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    digest = hashlib.sha256(NATURAL_PATH.read_bytes()).hexdigest()
    overlap = sum(1 for row in rows if row["task_id"] in frozen_ids)
    print(f"tasks read: {len(tasks)}")
    print(f"tasks kept: {len(rows)}  dropped (no slots): {tasks_dropped}")
    print(f"gold names: {gold_total}  dropped (no catalog match): {gold_dropped}")
    print(f"slots: {sum(len(row['slots']) for row in rows)}")
    print(f"overlap with frozen eval set (task_id): {overlap}")
    print(f"wrote {NATURAL_PATH}")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
