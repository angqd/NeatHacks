"""Stage 2 Part A: deterministic per-task features. No LLM, no embeddings.

Reads data/processed/tools.jsonl and tasks_resolved.jsonl and writes
data/processed/tasks_tagged.jsonl with feature fields. Judgment fields and
resolution proposals are added afterwards by the Part B labeler (merged by task_id).

Run: python -m toolprune.task_features
"""

import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROC_DIR = ROOT / "data" / "processed"

OVERLAP_THRESHOLD = 0.10  # fixed before any system is scored; do not tune
MULTI_CAPABILITY_MIN = 3
NAME_JACCARD_MIN = 0.5
NEIGHBOR_TFIDF_TOP = 8
NEIGHBOR_JACCARD_TOP = 3
NEIGHBOR_SAME_SERVER_CAP = 10

STOPWORDS = frozenset(
    """a an and are as at be but by can do does for from had has have how i in into is it
    its me my of on or our please that the their them then there these this to us was we
    what when where which who why will with would you your want need using use make
    get give show find tell let just also any all some each one two about over under
    should could may might must shall being been were am out up down off than too very
    s t""".split()
)


def stem(token: str) -> str:
    """Light suffix stripping. Deliberately simple and applied identically everywhere."""
    for suffix, minimum in (("ing", 5), ("ed", 4), ("es", 4), ("s", 4)):
        if token.endswith(suffix) and len(token) >= minimum:
            return token[: -len(suffix)]
    return token


CJK_RUN = re.compile(r"[一-鿿]+")
ASCII_TOKEN = re.compile(r"[a-z0-9]+")


def content_tokens(text: str) -> set[str]:
    """ASCII words (stemmed, stopwords dropped) plus CJK character bigrams.

    CJK text has no spaces, so each run is split into overlapping bigrams
    (a single-character run stays as one token). Without this, Chinese
    questions and docs would score zero overlap by construction.
    """
    lowered = text.lower()
    out = {stem(t) for t in ASCII_TOKEN.findall(lowered) if t not in STOPWORDS and len(t) > 1}
    for run in CJK_RUN.findall(text):
        if len(run) == 1:
            out.add(run)
        else:
            out.update(run[i:i + 2] for i in range(len(run) - 1))
    return out


def name_tokens(name: str) -> set[str]:
    """Split identifiers on _, -, spaces, dots and camelCase boundaries."""
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
    parts = re.findall(r"[a-z0-9]+", spaced.lower())
    return {stem(p) for p in parts if p not in STOPWORDS}


def overlap_ratio(question: str, gold_tools: list[dict]) -> tuple[float, int, int]:
    q = content_tokens(question)
    if not q:
        return 0.0, 0, 0
    doc_terms: set[str] = set()
    for tool in gold_tools:
        doc_terms |= name_tokens(tool["name"])
        doc_terms |= content_tokens(tool.get("description") or "")
        doc_terms |= name_tokens(tool["server"])
    hit = q & doc_terms
    return len(hit) / len(q), len(hit), len(q)


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class Index:
    """Lexical index over the full catalog: TF-IDF cosine on name+description, name-token Jaccard."""

    def __init__(self, tools: list[dict]):
        self.tools = tools
        self.by_id = {t["id"]: t for t in tools}
        self.by_name: dict[str, list[dict]] = {}
        self.by_server: dict[str, list[dict]] = {}
        self.doc_terms: dict[str, set[str]] = {}
        self.name_terms: dict[str, set[str]] = {}
        df: Counter = Counter()
        for t in tools:
            self.by_name.setdefault(t["name"], []).append(t)
            self.by_server.setdefault(t["server"], []).append(t)
            terms = name_tokens(t["name"]) | content_tokens(t.get("description") or "")
            self.doc_terms[t["id"]] = terms
            self.name_terms[t["id"]] = name_tokens(t["name"])
            df.update(terms)
        n = len(tools)
        self.idf = {term: math.log((1 + n) / (1 + c)) + 1.0 for term, c in df.items()}
        self.norm = {}
        for tid, terms in self.doc_terms.items():
            self.norm[tid] = math.sqrt(sum(self.idf[t] ** 2 for t in terms)) or 1.0

    def tfidf_cosine(self, a: str, b: str) -> float:
        shared = self.doc_terms[a] & self.doc_terms[b]
        num = sum(self.idf[t] ** 2 for t in shared)
        return num / (self.norm[a] * self.norm[b])

    def neighbors_of(self, gold: dict) -> list[dict]:
        gid = gold["id"]
        others = [t["id"] for t in self.tools if t["id"] != gid]

        reasons: dict[str, set[str]] = {}
        scores: dict[str, dict] = {}

        def add(tid: str, reason: str) -> None:
            reasons.setdefault(tid, set()).add(reason)

        # (a) every same-name tool
        for t in self.by_name.get(gold["name"], []):
            if t["id"] != gid:
                add(t["id"], "same_name")

        # (b) same-server tools, cap 10, ranked by TF-IDF cosine
        same = [t["id"] for t in self.by_server.get(gold["server"], []) if t["id"] != gid]
        same.sort(key=lambda x: -self.tfidf_cosine(gid, x))
        for tid in same[:NEIGHBOR_SAME_SERVER_CAP]:
            add(tid, "same_server")

        # (c) top 3 by name-token Jaccard
        g_name = self.name_terms[gid]
        jac = sorted(((jaccard(g_name, self.name_terms[t]), t) for t in others), reverse=True)
        for score, tid in jac[:NEIGHBOR_JACCARD_TOP]:
            if score > 0:
                add(tid, "name_overlap")
                scores.setdefault(tid, {})["name_jaccard"] = round(score, 3)

        # rest: top 8 by TF-IDF cosine over name+description
        tf = sorted(((self.tfidf_cosine(gid, t), t) for t in others), reverse=True)
        for score, tid in tf[:NEIGHBOR_TFIDF_TOP]:
            if score > 0:
                add(tid, "desc_overlap")
                scores.setdefault(tid, {})["tfidf"] = round(score, 4)

        order = {"same_name": 0, "name_overlap": 1, "same_server": 2, "desc_overlap": 3}
        out = []
        for tid, rs in reasons.items():
            entry = {"tool_id": tid, "reasons": sorted(rs, key=lambda r: order[r])}
            entry.update(scores.get(tid, {}))
            if "tfidf" not in entry:
                entry["tfidf"] = round(self.tfidf_cosine(gid, tid), 4)
            out.append(entry)
        out.sort(key=lambda e: (min(order[r] for r in e["reasons"]), -e["tfidf"]))
        return out


def hints(tool: dict) -> tuple[bool | None, bool | None]:
    ann = tool.get("annotations") or {}
    return ann.get("readOnlyHint"), ann.get("destructiveHint")


def main() -> None:
    tools = [json.loads(line) for line in (PROC_DIR / "tools.jsonl").read_text(encoding="utf-8").splitlines()]
    tasks = [json.loads(line) for line in (PROC_DIR / "tasks_resolved.jsonl").read_text(encoding="utf-8").splitlines()]
    index = Index(tools)

    rows = []
    n_low = n_multi = n_shared = 0
    for task in tasks:
        gold_resolved = [index.by_id[g] for g in task["gold_ids"] if g is not None]
        ratio, hit, qn = overlap_ratio(task["question"], gold_resolved)
        low = ratio <= OVERLAP_THRESHOLD
        multi = task["n_gold"] >= MULTI_CAPABILITY_MIN

        # shared_name: computed from gold names against the catalog, so ambiguous names count.
        shared_name_tools = {}
        for name in task["gold_names"]:
            shared_name_tools[name] = [t["id"] for t in index.by_name.get(name, [])]
        shared = any(len(ids) > 1 for ids in shared_name_tools.values())
        n_low += low
        n_multi += multi
        n_shared += shared

        # gold-side tools: unique resolutions plus every candidate of an ambiguous name
        gold_side: list[dict] = []
        seen = set()
        for entry in task["resolution"]:
            if entry["status"] == "unique":
                ids = entry["candidates"]
            elif entry["status"] == "ambiguous":
                ids = entry["candidates"]
            else:
                ids = []
            for tid in ids:
                if tid not in seen:
                    seen.add(tid)
                    gold_side.append(index.by_id[tid])

        gold_detail = []
        for g in gold_side:
            ro, de = hints(g)
            gold_detail.append({"tool_id": g["id"], "name_collision_count": len(index.by_name[g["name"]]),
                                "read_only_hint": ro, "destructive_hint": de})

        neighbors = {g["id"]: index.neighbors_of(g) for g in gold_side}

        rows.append({
            "task_id": task["task_id"],
            "question": task["question"],
            "category": task["category"],
            "steps": task["steps"],
            "gold_names": task["gold_names"],
            "gold_ids": task["gold_ids"],
            "resolution": task["resolution"],
            "n_gold": task["n_gold"],
            "fully_resolved": task["fully_resolved"],
            "features": {
                "overlap_ratio": round(ratio, 4),
                "overlap_count": hit,
                "question_content_tokens": qn,
                "low_overlap": low,
                "multi_capability": multi,
                "shared_name": shared,
                "shared_name_tools": shared_name_tools,
                "gold_tool_hints": gold_detail,
                "neighbors": neighbors,
                "n_gold_side_tools": len(gold_side),
            },
            "judgment": None,
        })

    out = PROC_DIR / "tasks_tagged.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rows to {out}")
    print(f"low_overlap (ratio <= {OVERLAP_THRESHOLD}): {n_low}")
    print(f"multi_capability (n_gold >= {MULTI_CAPABILITY_MIN}): {n_multi}")
    print(f"shared_name: {n_shared}")


if __name__ == "__main__":
    main()
