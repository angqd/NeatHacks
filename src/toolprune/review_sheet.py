"""Build a self-contained HTML review sheet from tagged tasks and second-opinion reviews.

Run: .venv/bin/python -m toolprune.review_sheet
Reads data/processed/{tasks_tagged,tools}.jsonl and review_sonnet_*.jsonl (optional).
Writes data/processed/review_sheet.html. Decisions are kept in the browser and exported as JSON.
"""

import glob
import json
import random
from pathlib import Path

PROC = Path(__file__).resolve().parents[2] / "data" / "processed"
DESC_CAP = 320
NEIGHBOR_CAP = 12


def read_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 1.0


def tool_card(tool: dict) -> dict:
    ann = tool.get("annotations") or {}
    return {
        "server": tool["server"],
        "name": tool["name"],
        "desc": (tool.get("description") or "")[:DESC_CAP],
        "read_only": ann.get("readOnlyHint"),
        "destructive": ann.get("destructiveHint"),
    }


def build_slots(task: dict, review: dict | None) -> list[dict]:
    proposals = {p["name"]: p for p in task.get("resolution_proposals") or []}
    sonnet_slots = {s["gold_name"]: s for s in (review or {}).get("slot_review", [])}
    neighbors = task["features"].get("neighbors", {})
    slots = []
    for res in task["resolution"]:
        name = res["name"]
        cands = res.get("candidates") or []
        prop = proposals.get(name, {})
        son = sonnet_slots.get(name, {})
        haiku_pick = cands[0] if res["status"] == "unique" and cands else prop.get("proposed_id")
        near: list[dict] = []
        seen = set(cands)
        for cid in cands or [haiku_pick]:
            for n in neighbors.get(cid, []):
                if n["tool_id"] not in seen:
                    seen.add(n["tool_id"])
                    near.append({"id": n["tool_id"], "reasons": n["reasons"]})
        slots.append({
            "name": name,
            "status": res["status"],
            "candidates": cands,
            "haiku_pick": haiku_pick,
            "haiku_conf": prop.get("confidence", "high" if res["status"] == "unique" else None),
            "haiku_reason": prop.get("reason"),
            "sonnet_pick": son.get("pick"),
            "sonnet_conf": son.get("pick_confidence"),
            "sonnet_reason": son.get("pick_reason"),
            "sonnet_keep": son.get("keep"),
            "sonnet_alts": son.get("alternates") or [],
            "neighbors": near[:NEIGHBOR_CAP],
        })
    return slots


def triage(task: dict, slots: list[dict], review: dict | None) -> tuple[str, list[str]]:
    """Return (level, reasons). `needs` = gold or confidence problem, `bucket` = only bucket labels differ."""
    gold: list[str] = []
    bucket: list[str] = []
    if not review:
        return "needs", ["no second opinion"]
    for s in slots:
        if s["status"] == "missing":
            gold.append(f"gold missing: {s['name']}")
        elif s["status"] == "ambiguous":
            if s["sonnet_pick"] != s["haiku_pick"]:
                gold.append(f"pick conflict: {s['name']}")
            elif "low" in (s["haiku_conf"], s["sonnet_conf"]):
                gold.append(f"low pick confidence: {s['name']}")
        if s["sonnet_keep"] is False:
            gold.append(f"Sonnet says drop slot: {s['name']}")
    if "low" in (task["confidence"], review.get("confidence")):
        gold.append("low label confidence")
    h_set, s_set = set(task["buckets"]), set(review.get("buckets", []))
    if not (task["primary_bucket"] in s_set and review.get("primary_bucket") in h_set):
        bucket.append("bucket labels differ")
    if gold:
        return "needs", gold + bucket
    return ("bucket" if bucket else "auto"), bucket


def build() -> dict:
    tasks = read_jsonl(PROC / "tasks_tagged.jsonl")
    tools = {t["id"]: t for t in read_jsonl(PROC / "tools.jsonl")}
    reviews: dict[str, dict] = {}
    for path in sorted(glob.glob(str(PROC / "review_sonnet_*.jsonl"))):
        for r in read_jsonl(Path(path)):
            reviews[r["task_id"]] = r

    rng = random.Random(0)
    out_tasks, needed_tools = [], set()
    for task in tasks:
        review = reviews.get(task["task_id"])
        slots = build_slots(task, review)
        level, reasons = triage(task, slots, review)
        if level == "auto" and rng.random() < 0.10:
            level, reasons = "bucket", ["random audit sample"]
        for s in slots:
            needed_tools.update(s["candidates"])
            needed_tools.update(x["id"] for x in s["neighbors"])
            for k in ("haiku_pick", "sonnet_pick"):
                if s[k]:
                    needed_tools.add(s[k])
            needed_tools.update(s["sonnet_alts"])
        for c in task.get("confusers") or []:
            needed_tools.add(c["tool_id"])
        out_tasks.append({
            "id": task["task_id"],
            "question": task["question"],
            "category": task["category"],
            "steps": task["steps"],
            "slots": slots,
            "triage": level,
            "reasons": reasons,
            "features": {
                "overlap_ratio": task["features"]["overlap_ratio"],
                "n_gold": task["n_gold"],
            },
            "haiku": {
                "buckets": task["buckets"],
                "primary": task["primary_bucket"],
                "confidence": task["confidence"],
                "evidence": task["evidence"],
                "confusers": task.get("confusers") or [],
                "needs_clarification": task["needs_clarification"],
                "review_reason": task.get("review_reason"),
            },
            "sonnet": None if not review else {
                "buckets": review.get("buckets", []),
                "primary": review.get("primary_bucket"),
                "confidence": review.get("confidence"),
                "evidence": review.get("evidence", {}),
                "confusers": review.get("confusers", []),
                "needs_clarification": review.get("needs_clarification"),
                "review_reason": review.get("review_reason"),
                "missing_capabilities": review.get("missing_capabilities", []),
            },
        })
    return {
        "tasks": out_tasks,
        "tools": {tid: tool_card(tools[tid]) for tid in needed_tools if tid in tools},
        "buckets": ["semantic_distance", "taxonomy_collision", "multi_capability",
                    "near_duplicate", "ambiguity", "none"],
    }


def main() -> None:
    data = build()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__DATA__", payload)
    path = PROC / "review_sheet.html"
    path.write_text(html, encoding="utf-8")
    counts = {k: sum(1 for t in data["tasks"] if t["triage"] == k) for k in ("needs", "bucket", "auto")}
    print(f"wrote {path}: {len(data['tasks'])} tasks, {counts}")


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ToolPrune review sheet</title>
<style>
:root{--bg:#fbfaf8;--panel:#fff;--ink:#1c1b19;--mute:#6b6a66;--line:#e4e1da;--accent:#2f5d8a;--ok:#2d7a4b;--warn:#a5671a;--bad:#b23a3a;--chip:#eef2f6}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#17181a;--panel:#1f2124;--ink:#ecebe8;--mute:#9a9892;--line:#33363a;--accent:#7fb0e0;--ok:#6cc08b;--warn:#e0a456;--bad:#e27b7b;--chip:#2a2f35}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header h1{font-size:15px;margin:0 8px 0 0}
.bar{flex:1;min-width:140px;height:8px;background:var(--chip);border-radius:4px;overflow:hidden}.bar i{display:block;height:100%;background:var(--ok)}
button,select{font:inherit;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:5px 10px;cursor:pointer}
button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}button:disabled{opacity:.5}
main{display:grid;grid-template-columns:300px 1fr;gap:16px;padding:16px;max-width:1400px;margin:0 auto}
@media(max-width:860px){main{grid-template-columns:1fr}}
#list{background:var(--panel);border:1px solid var(--line);border-radius:8px;max-height:calc(100vh - 90px);overflow:auto;position:sticky;top:60px}
.row{padding:8px 10px;border-bottom:1px solid var(--line);cursor:pointer;display:flex;gap:8px;align-items:flex-start}
.row.sel{background:var(--chip)}.dot{width:9px;height:9px;border-radius:50%;margin-top:5px;flex:none;background:var(--line)}
.dot.needs{background:var(--warn)}.dot.bucket{background:var(--accent)}.dot.done{background:var(--ok)}.dot.auto{background:var(--mute)}
.row small{color:var(--mute);display:block}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px;margin-bottom:16px}
.card h2{margin:0 0 6px;font-size:16px}.q{font-size:15px;margin:0 0 8px}
.chip{display:inline-block;background:var(--chip);border-radius:11px;padding:2px 9px;margin:2px 4px 2px 0;font-size:12px}
.chip.on{background:var(--accent);color:#fff}.chip.warn{background:transparent;border:1px solid var(--warn);color:var(--warn)}
.mute{color:var(--mute)}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:700px){.grid2{grid-template-columns:1fr}}
table{border-collapse:collapse;width:100%}td,th{border-top:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{color:var(--mute);font-weight:500;font-size:12px}
.agree{color:var(--ok)}.diff{color:var(--bad)}.tool{font-family:ui-monospace,monospace;font-size:12px}
details summary{cursor:pointer;color:var(--mute)}textarea{width:100%;min-height:52px;font:inherit;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:6px}
label.opt{display:block;padding:3px 0}.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.hint{font-size:12px;color:var(--mute)}
</style></head><body>
<header><h1>ToolPrune review</h1>
<select id="filter"><option value="needs">Gold or confidence issues</option><option value="bucket">Bucket labels only</option><option value="all">All tasks</option><option value="done">Reviewed</option><option value="auto">Auto-accepted</option></select>
<div class="bar" title="reviewed"><i id="prog" style="width:0"></i></div><span id="count" class="mute"></span>
<button id="export" class="primary">Export decisions</button><button id="import">Import</button>
<button id="acceptAuto">Accept all auto</button><input id="file" type="file" accept=".json" hidden>
<span class="hint">keys: j/k move, a accept as suggested, e edit</span></header>
<main><div id="list"></div><div id="detail"></div></main>
<script>
const DATA=__DATA__;
const KEY="toolprune-review-v1";
let dec={};try{dec=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
const persist=()=>{try{localStorage.setItem(KEY,JSON.stringify(dec))}catch(e){}};
const T=DATA.tasks;let cur=0;
const el=(t,p={},...k)=>{const e=document.createElement(t);for(const[a,v]of Object.entries(p)){if(a==="class")e.className=v;else if(a.startsWith("on"))e[a]=v;else e.setAttribute(a,v)}for(const c of k.flat())e.append(c&&c.nodeType?c:document.createTextNode(c??""));return e};
const tl=id=>{const t=DATA.tools[id];return t?`${t.server} :: ${t.name}`:(id||"(none)")};
const jac=(a,b)=>{const A=new Set(a),B=new Set(b),u=new Set([...A,...B]);return u.size?[...A].filter(x=>B.has(x)).length/u.size:1};
function suggestion(t){ // merged suggestion: prefer agreement, else Haiku
  const s=t.sonnet;
  return {primary:t.haiku.primary,buckets:[...t.haiku.buckets],
    needs_clarification:t.haiku.needs_clarification,
    slots:t.slots.map(x=>({name:x.name,keep:x.sonnet_keep!==false,pick:x.haiku_pick||x.sonnet_pick||null,alternates:[...x.sonnet_alts]}))};
}
function state(t){return dec[t.id]?"done":t.triage}
function visible(){const f=document.getElementById("filter").value;return T.map((t,i)=>i).filter(i=>f==="all"?true:state(T[i])===f)}
function renderList(){const L=document.getElementById("list");L.replaceChildren();
  const vis=visible();
  vis.forEach(i=>{const t=T[i];L.append(el("div",{class:"row"+(i===cur?" sel":""),onclick:()=>{cur=i;render()}},
    el("span",{class:"dot "+state(t)}),el("div",{},t.question.slice(0,70)+(t.question.length>70?"…":""),el("small",{},`${t.haiku.primary} · ${t.reasons.length?t.reasons.length+" flags":"clean"}`))))});
  const done=T.filter(t=>dec[t.id]).length;
  document.getElementById("prog").style.width=(100*done/T.length)+"%";
  document.getElementById("count").textContent=`${done}/${T.length} reviewed · ${vis.length} shown`;
}
function chips(list,cls){return list.map(b=>el("span",{class:"chip "+(cls||"")},b))}
function renderDetail(){
  const t=T[cur];const D=document.getElementById("detail");D.replaceChildren();if(!t)return;
  const d=dec[t.id]||{...suggestion(t),status:"pending",note:""};
  const draft=JSON.parse(JSON.stringify(d));
  const save=(status)=>{draft.status=status;dec[t.id]=draft;persist();const vis=visible();render()};
  const head=el("div",{class:"card"},el("h2",{},`${t.category} · ${t.id.slice(0,8)}`),
    el("p",{class:"q"},t.question),
    el("div",{},...t.reasons.map(r=>el("span",{class:"chip warn"},r))),
    el("details",{},el("summary",{},"Annotator steps"),el("pre",{style:"white-space:pre-wrap"},t.steps)),
    el("div",{class:"mute"},`overlap ratio ${t.features.overlap_ratio}`));
  // buckets
  const bk=el("div",{class:"card"},el("h2",{},"Buckets"));
  const g=el("div",{class:"grid2"});
  const col=(title,m)=>el("div",{},el("div",{class:"mute"},title+(m?` (confidence ${m.confidence})`:"")),
    m?[...chips(m.buckets),el("div",{class:"mute"},`primary: ${m.primary}`),
      el("details",{},el("summary",{},"evidence"),...Object.entries(m.evidence).map(([k,v])=>el("p",{},el("b",{},k+": "),v)))]:el("div",{class:"mute"},"no second opinion"));
  g.append(col("Haiku",t.haiku),col("Sonnet",t.sonnet));bk.append(g);
  const pick=el("div",{style:"margin-top:8px"},el("div",{class:"mute"},"Your buckets"));
  DATA.buckets.forEach(b=>{const on=draft.buckets.includes(b);
    pick.append(el("span",{class:"chip"+(on?" on":""),style:"cursor:pointer",onclick:()=>{draft.buckets=on?draft.buckets.filter(x=>x!==b):[...draft.buckets,b];if(!draft.buckets.includes(draft.primary))draft.primary=draft.buckets[0]||"none";dec[t.id]=draft;renderDetail()}},b))});
  const sel=el("select",{onchange:e=>{draft.primary=e.target.value;if(!draft.buckets.includes(draft.primary))draft.buckets.push(draft.primary)}},...DATA.buckets.map(b=>{const o=el("option",{value:b},b);if(b===draft.primary)o.selected=true;return o}));
  pick.append(el("div",{style:"margin-top:6px"},"Primary: ",sel));
  const nc=el("input",{type:"checkbox",onchange:e=>draft.needs_clarification=e.target.checked});nc.checked=!!draft.needs_clarification;
  pick.append(el("label",{class:"opt"},nc," needs clarification (intent underspecified)"));
  bk.append(pick);
  if(t.sonnet&&t.sonnet.missing_capabilities.length)bk.append(el("p",{class:"diff"},"Sonnet sees missing capability: "+t.sonnet.missing_capabilities.join("; ")));
  // slots
  const sl=el("div",{class:"card"},el("h2",{},"Gold slots"),el("div",{class:"hint"},"Required capabilities from the bench reference list. Pick the tool, drop a slot the intent does not need, tick acceptable alternates."));
  t.slots.forEach((s,i)=>{const ds=draft.slots[i];
    const cands=[...new Set([...s.candidates,s.haiku_pick,s.sonnet_pick].filter(Boolean))];
    const agree=s.sonnet_pick&&s.haiku_pick===s.sonnet_pick;
    const box=el("div",{style:"border-top:1px solid var(--line);padding:8px 0"});
    const keep=el("input",{type:"checkbox",onchange:e=>ds.keep=e.target.checked});keep.checked=ds.keep;
    box.append(el("div",{},el("b",{},s.name)," ",el("span",{class:"chip"},s.status)," ",el("label",{},keep," required")));
    if(s.status!=="unique"||cands.length>1){
      cands.forEach(c=>{const r=el("input",{type:"radio",name:`p${t.id}${i}`,onchange:()=>ds.pick=c});r.checked=ds.pick===c;
        const tag=[c===s.haiku_pick?"Haiku":"",c===s.sonnet_pick?"Sonnet":""].filter(Boolean).join("+");
        box.append(el("label",{class:"opt"},r," ",el("span",{class:"tool"},tl(c)),tag?el("span",{class:"chip"},tag):"",
          el("div",{class:"hint"},(DATA.tools[c]||{}).desc||"")))});
      const none=el("input",{type:"radio",name:`p${t.id}${i}`,onchange:()=>ds.pick=null});none.checked=!ds.pick;
      box.append(el("label",{class:"opt"},none," none fits / drop"));
      box.append(el("div",{class:agree?"agree":"diff"},agree?"Models agree":"Models differ"),
        el("div",{class:"hint"},`Haiku (${s.haiku_conf||"-"}): ${s.haiku_reason||"-"}`),
        el("div",{class:"hint"},`Sonnet (${s.sonnet_conf||"-"}): ${s.sonnet_reason||"-"}`));
    }else box.append(el("div",{class:"tool"},tl(s.candidates[0])),el("div",{class:"hint"},(DATA.tools[s.candidates[0]]||{}).desc||""));
    const nb=[...new Set([...s.sonnet_alts,...s.neighbors.map(n=>n.id)])];
    if(nb.length)box.append(el("details",{},el("summary",{},`Alternates (${nb.length} candidates)`),...nb.map(id=>{
      const c=el("input",{type:"checkbox",onchange:e=>{ds.alternates=e.target.checked?[...ds.alternates,id]:ds.alternates.filter(x=>x!==id)}});c.checked=ds.alternates.includes(id);
      const nr=s.neighbors.find(n=>n.id===id);
      return el("label",{class:"opt"},c," ",el("span",{class:"tool"},tl(id)),s.sonnet_alts.includes(id)?el("span",{class:"chip"},"Sonnet"):"",nr?el("span",{class:"hint"}," "+nr.reasons.join(", ")):"",el("div",{class:"hint"},(DATA.tools[id]||{}).desc||""))})));
    sl.append(box)});
  // confusers
  const conf=[...t.haiku.confusers,...(t.sonnet?t.sonnet.confusers:[])];
  const cf=el("div",{class:"card"},el("h2",{},"Confusers (not gold, plausible)"),
    conf.length?conf.map(c=>el("div",{},el("span",{class:"tool"},tl(c.tool_id))," ",el("span",{class:"chip"},c.reason))):el("div",{class:"mute"},"none listed"));
  const note=el("textarea",{placeholder:"note (optional)",oninput:e=>draft.note=e.target.value});note.value=draft.note||"";
  const act=el("div",{class:"actions"},
    el("button",{class:"primary",onclick:()=>{save("accepted_edited");next()}},"Save my choices"),
    el("button",{onclick:()=>{Object.assign(draft,suggestion(t));save("accepted_suggested");next()}},"Accept Haiku suggestion"),
    el("button",{onclick:()=>{save("skipped");next()}},"Skip"),
    dec[t.id]?el("button",{onclick:()=>{delete dec[t.id];persist();render()}},"Clear"):"");
  D.append(head,bk,sl,cf,el("div",{class:"card"},note,act));
  window._draft=draft;window._t=t;
}
function next(){const vis=visible();const k=vis.indexOf(cur);if(vis.length)cur=vis[Math.min(k+1,vis.length-1)]??vis[0]}
function render(){renderList();renderDetail()}
document.getElementById("filter").onchange=()=>{const v=visible();if(v.length&&!v.includes(cur))cur=v[0];render()};
document.addEventListener("keydown",e=>{if(/INPUT|TEXTAREA|SELECT/.test(e.target.tagName))return;
  const v=visible(),k=v.indexOf(cur);
  if(e.key==="j"&&k<v.length-1){cur=v[k+1];render()}
  if(e.key==="k"&&k>0){cur=v[k-1];render()}
  if(e.key==="a"){const t=T[cur];dec[t.id]={...suggestion(t),status:"accepted_suggested",note:""};persist();next();render()}});
document.getElementById("acceptAuto").onclick=()=>{const n=T.filter(t=>t.triage==="auto"&&!dec[t.id]);
  if(!confirm(`Accept ${n.length} auto-triaged tasks as suggested?`))return;
  n.forEach(t=>dec[t.id]={...suggestion(t),status:"accepted_auto",note:""});persist();render()};
document.getElementById("export").onclick=()=>{
  const out=T.map(t=>({task_id:t.id,review:dec[t.id]||null,triage:t.triage,reasons:t.reasons}));
  const a=el("a",{href:URL.createObjectURL(new Blob([JSON.stringify(out,null,2)],{type:"application/json"})),download:"review_decisions.json"});
  document.body.append(a);a.click();a.remove()};
document.getElementById("import").onclick=()=>document.getElementById("file").click();
document.getElementById("file").onchange=async e=>{const f=e.target.files[0];if(!f)return;
  try{for(const r of JSON.parse(await f.text()))if(r.review)dec[r.task_id]=r.review;persist();render()}catch(x){alert("bad file")}};
const v0=visible();if(v0.length)cur=v0[0];render();
</script></body></html>
"""


if __name__ == "__main__":
    main()
