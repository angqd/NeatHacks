"""Stage 3 DRAFT: deterministic selection of the 60-task eval set (seed 0).

Reads tasks_reviewed.jsonl, task_families.jsonl, derived_candidates.jsonl and the
optional spot_decisions.json; writes eval_set_draft.jsonl and selection_report.md.
Nothing here is frozen.

Run: python -m toolprune.select_subset
"""

import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
SEED = 0
FAMILY_CAP = 8
DEV_TOTAL = 18  # 30 of 60
QUOTAS = {"multi_capability": 12, "semantic_distance": 12, "near_duplicate": 12,
          "taxonomy_collision": 10, "ambiguity": 10, "none": 4}
FILL_ORDER = ["ambiguity", "none", "semantic_distance", "near_duplicate", "taxonomy_collision", "multi_capability"]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def apply_overrides(tasks: list[dict], overrides: list[dict]) -> list[str]:
    """Apply spot decisions in place. Returns notes about what changed."""
    notes = []
    by_id = {t["task_id"]: t for t in tasks}
    for o in overrides:
        t = by_id.get(o["task_id"])
        if t is None:
            notes.append(f"override for unknown task {o['task_id']} ignored")
            continue
        if o.get("needs_clarification") is not None:
            t["needs_clarification"] = o["needs_clarification"]
        if o.get("gold_name"):
            for s in t["slots"]:
                if s["gold_name"] == o["gold_name"]:
                    if "pick" in o and o["pick"] is not None:
                        s["pick"] = o["pick"]
                    if o.get("keep") is not None:
                        s["keep"] = o["keep"]
        notes.append(f"override applied: {o['task_id'][:8]} {o.get('gold_name')}")
    return notes


def kept(t: dict) -> list[dict]:
    return [s for s in t["slots"] if s.get("keep", True)]


def eligible(t: dict) -> bool:
    ks = kept(t)
    return bool(ks) and all(s.get("pick") for s in ks)


def pick_set(t: dict) -> frozenset:
    return frozenset(s["pick"] for s in kept(t))


def main() -> None:
    reviewed = read_jsonl(PROC / "tasks_reviewed.jsonl")
    fam = {r["task_id"]: r["family"] for r in read_jsonl(PROC / "task_families.jsonl")}
    derived = read_jsonl(PROC / "derived_candidates.jsonl")
    spot = PROC / "spot_decisions.json"
    overrides = json.loads(spot.read_text(encoding="utf-8")) if spot.exists() else []

    for t in reviewed:
        t["bucket"] = t["primary_bucket"]
        t["family"] = fam[t["task_id"]]
        t["derived"] = False
    notes = apply_overrides(reviewed + derived, overrides)

    derived_from = {d["derived_from"] for d in derived}
    pool = defaultdict(list)
    n_ineligible = 0
    for t in reviewed:
        if t["task_id"] in derived_from:
            continue
        if not eligible(t):
            n_ineligible += 1
            continue
        pool[t["bucket"]].append(t)
    for d in derived:
        if eligible(d):
            pool[d["bucket"]].append(d)
    rng = random.Random(SEED)
    for b in sorted(pool):
        pool[b].sort(key=lambda t: t["task_id"])
        # derived first (they exist to fill thin buckets), natural shuffled
        nat = [t for t in pool[b] if not t["derived"]]
        der = [t for t in pool[b] if t["derived"]]
        rng.shuffle(nat)
        # natural ambiguity tasks are rarer than derived ones, keep them first
        pool[b] = (nat + der) if b == "ambiguity" else (der + nat)

    chosen: list[dict] = []
    fam_count: Counter = Counter()
    seen_sets: set = set()
    skipped = Counter()

    def take(bucket: str, n: int) -> int:
        got = 0
        for t in pool[bucket]:
            if got >= n:
                break
            if any(t is c for c in chosen):
                continue
            if fam_count[t["family"]] >= FAMILY_CAP:
                skipped["family_cap"] += 1
                continue
            if pick_set(t) in seen_sets:
                skipped["duplicate_gold_set"] += 1
                continue
            chosen.append(t)
            fam_count[t["family"]] += 1
            seen_sets.add(pick_set(t))
            got += 1
        return got

    got = {b: take(b, QUOTAS[b]) for b in FILL_ORDER}
    shortfall = {b: QUOTAS[b] - got[b] for b in FILL_ORDER if got[b] < QUOTAS[b]}
    extra = sum(shortfall.values())
    filled = take("multi_capability", extra) if extra else 0
    total_short = extra - filled

    # stratified dev/test split by bucket (largest remainder to hit 18 dev)
    by_bucket = defaultdict(list)
    for t in chosen:
        by_bucket[t["bucket"]].append(t)
    ideal = {b: len(v) * DEV_TOTAL / len(chosen) for b, v in by_bucket.items()}
    dev_n = {b: int(x) for b, x in ideal.items()}
    for b in sorted(ideal, key=lambda b: (-(ideal[b] - dev_n[b]), b))[: DEV_TOTAL - sum(dev_n.values())]:
        dev_n[b] += 1
    split = {}
    for b in sorted(by_bucket):
        ids = sorted(t["task_id"] for t in by_bucket[b])
        random.Random(f"{SEED}-{b}").shuffle(ids)
        for i, tid in enumerate(ids):
            split[tid] = "dev" if i < dev_n[b] else "test"

    records = []
    for t in sorted(chosen, key=lambda t: (t["bucket"], t["task_id"])):
        records.append({
            "task_id": t["task_id"],
            "question": t["question"],
            "category": t.get("category"),
            "bucket": t["bucket"],
            "family": t["family"],
            "slots": [{"gold_name": s["gold_name"], "pick": s["pick"], "alternates": s.get("alternates", [])} for s in kept(t)],
            "confusers": t.get("confusers", []),
            "needs_clarification": bool(t.get("needs_clarification")),
            "derived": bool(t["derived"]),
            "split": split[t["task_id"]],
        })
    (PROC / "eval_set_draft.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")

    def table(counter: Counter, head: str) -> str:
        return f"| {head} | n |\n| --- | --- |\n" + "".join(f"| {k} | {v} |\n" for k, v in sorted(counter.items()))

    cb = Counter(r["bucket"] for r in records)
    lines = [
        "# Eval set selection report (DRAFT, not frozen)", "",
        f"Seed {SEED}. Tasks selected: {len(records)}. Derived: {sum(r['derived'] for r in records)}. "
        f"Overrides applied: {len(overrides)} (spot_decisions.json {'found' if spot.exists() else 'absent'}). "
        f"Natural tasks ineligible (null pick on a kept slot): {n_ineligible}.", "",
        "## Per bucket (quota -> selected)", "| bucket | quota | selected |", "| --- | --- | --- |",
        *[f"| {b} | {QUOTAS[b]} | {cb.get(b, 0)} |" for b in QUOTAS], "",
        "## Per family", table(Counter(r["family"] for r in records), "family"),
        "## Per split", table(Counter(r["split"] for r in records), "split"),
        "## Split by bucket", table(Counter(f"{r['bucket']}/{r['split']}" for r in records), "bucket/split"),
        "## Shortfalls",
    ]
    if shortfall:
        lines += [f"- {b}: short by {n}" for b, n in shortfall.items()]
        lines.append(f"- Filled {filled} of {extra} missing slots from multi_capability."
                     + (f" Still short by {total_short}." if total_short else ""))
    else:
        lines.append("- none")
    lines += ["", f"Skips while selecting: {dict(skipped)}"]
    if notes:
        lines += ["", "## Override notes", *[f"- {n}" for n in notes]]
    (PROC / "selection_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
