"""Sanity check: BM25 on the original LiveMCPBench tasks, next to the self-reported 31.68 Recall@5.

Not a gate. Every document variant in toolprune.text.VARIANTS is reported, and no variant is
chosen or tuned. Two views are computed from the same top-k lists:

- name view: a returned tool counts for a gold name if tool.name equals that name (any server).
- id view: a gold name counts only if it is uniquely resolved, and then the returned tool id
  must equal the exact gold id from tasks_resolved.jsonl.

Gold names absent from the catalog (name view) or not uniquely resolved (id view) are dropped
from that task's denominator. Tasks left with no gold names are dropped. Query text is the
task question only.

Run with: .venv/bin/python -m toolprune.eval.sanity_bm25
"""

from toolprune.bm25 import BM25Retriever
from toolprune.models import PROC_DIR, ROOT, Tool, load_tools, read_jsonl
from toolprune.text import VARIANTS

TASKS_PATH = PROC_DIR / "tasks_resolved.jsonl"
REPORT_PATH = ROOT / "reports" / "sanity_bm25.md"
SELF_REPORTED_R5 = 31.68
KS = (5, 10)


def unique_gold_ids(task: dict) -> dict[str, str]:
    """Map each uniquely resolved gold name to its exact tool id."""
    ids = dict(zip(task["gold_names"], task["gold_ids"]))
    out: dict[str, str] = {}
    for entry in task["resolution"]:
        if entry["status"] == "unique" and len(entry["candidates"]) == 1:
            name = entry["name"]
            if name in ids and ids[name] != entry["candidates"][0]:
                raise ValueError(f"gold id mismatch for {name!r} in task {task['task_id']}")
            out[name] = entry["candidates"][0]
    return out


def score_variant(variant: str, tools: list[Tool], tasks: list[dict]) -> dict[str, dict[str, float | int]]:
    retriever = BM25Retriever(tools, variant)
    tool_by_id = {tool.id: tool for tool in tools}
    catalog_names = {tool.name for tool in tools}
    results: dict[str, dict[str, float | int]] = {}
    for view in ("name", "id"):
        recalls: dict[int, list[float]] = {k: [] for k in KS}
        dropped = 0
        for task in tasks:
            uniq = unique_gold_ids(task)
            if view == "name":
                gold = {n for n in task["gold_names"] if n in catalog_names}
                dropped += len(set(task["gold_names"])) - len(gold)
            else:
                gold = set(uniq)
                dropped += len(set(task["gold_names"])) - len(gold)
            if not gold:
                continue
            ranked = retriever.retrieve(task["question"], max(KS))
            for k in KS:
                top = [tool_by_id[hit.tool_id] for hit in ranked[:k]]
                if view == "name":
                    returned = {tool.name for tool in top}
                    hits = len(gold & returned)
                else:
                    returned_ids = {tool.id for tool in top}
                    hits = sum(1 for name in gold if uniq[name] in returned_ids)
                recalls[k].append(hits / len(gold))
        for k in KS:
            vals = recalls[k]
            results[f"{view}@{k}"] = {
                "recall": 100 * sum(vals) / len(vals) if vals else 0.0,
                "kept": len(vals),
                "dropped": dropped,
            }
    return results


def render(grid: dict[str, dict[str, dict[str, float | int]]]) -> str:
    lines = [
        "# BM25 sanity check on the original LiveMCPBench tasks",
        "",
        f"This is a sanity check against an unverified self-reported number: {SELF_REPORTED_R5} Recall@5 "
        "(toolrank README). It is not a gate. No variant was chosen or tuned to hit that number, "
        "and no winner is declared.",
        "",
        "## Protocol",
        "",
        f"- Tasks: `data/processed/tasks_resolved.jsonl`, {len(read_jsonl(TASKS_PATH))} original tasks. "
        "Query text is the task `question` only. Gold is the bench reference tool names (`gold_names`), no server.",
        "- Name view: a returned tool counts for a gold name if `tool.name` equals it, on any server. "
        "Gold names that appear nowhere in the catalog are dropped from that task's denominator.",
        "- Id view: a gold name counts only when uniquely resolved in the catalog, and then the returned tool id "
        "must equal the exact id from `gold_ids`. Ambiguous and missing names are skipped.",
        "- Per task Recall@k = distinct gold names matched in the top k / distinct gold names. "
        "Reported as the mean over kept tasks, in percent. Tasks with zero gold names are dropped.",
        "- Document variants: every entry of `toolprune.text.VARIANTS`, scored with `BM25Retriever(load_tools(), variant)` "
        "at k1=1.5, b=0.75.",
        "- Not known about the reference: its document text, its query set (the self-reported figure is over 94 "
        "queries, here 95 tasks), and its gold matching rule. The gap is documented, not tuned away.",
        "",
        "## Results (percent, mean Recall@k over kept tasks)",
        "",
        "| Variant | Name R@5 | Name R@10 | Id R@5 | Id R@10 | Name kept | Id kept | Name dropped gold | Id dropped gold |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for variant, res in grid.items():
        lines.append(
            f"| `{variant}` | {res['name@5']['recall']:.2f} | {res['name@10']['recall']:.2f} "
            f"| {res['id@5']['recall']:.2f} | {res['id@10']['recall']:.2f} "
            f"| {res['name@5']['kept']} | {res['id@5']['kept']} "
            f"| {res['name@5']['dropped']} | {res['id@5']['dropped']} |"
        )
    lines.append("")
    lines.append(f"Self-reported reference: {SELF_REPORTED_R5} Recall@5 (unverified).")
    return "\n".join(lines) + "\n"


def main() -> None:
    tools = load_tools()
    tasks = read_jsonl(TASKS_PATH)
    grid = {variant: score_variant(variant, tools, tasks) for variant in VARIANTS}
    report = render(grid)
    print(report)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
