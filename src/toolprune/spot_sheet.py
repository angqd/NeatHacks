"""Build a short spot-check sheet for the decisions that change what gold means.

Items: bench tool names missing from the catalog (mapped by the models), slots the adjudicator
dropped, and tasks marked as needing clarification.

Run: .venv/bin/python -m toolprune.spot_sheet
Writes data/processed/spot_check.html. Export gives spot_decisions.json entries:
{task_id, gold_name, pick, keep, needs_clarification}.
"""

import glob
import json
from pathlib import Path

PROC = Path(__file__).resolve().parents[2] / "data" / "processed"
DESC_CAP = 360
SEARCH_CAP = 160


def read_jsonl(path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def build() -> dict:
    tools = {t["id"]: t for t in read_jsonl(PROC / "tools.jsonl")}
    tagged = {t["task_id"]: t for t in read_jsonl(PROC / "tasks_tagged.jsonl")}
    reviewed = read_jsonl(PROC / "tasks_reviewed.jsonl")
    sonnet: dict[str, dict] = {}
    for path in glob.glob(str(PROC / "review_sonnet_*.jsonl")):
        for r in read_jsonl(path):
            sonnet[r["task_id"]] = r

    items: list[dict] = []
    shown: set[str] = set()

    def card(tid):
        if not tid or tid not in tools:
            return None
        shown.add(tid)
        t = tools[tid]
        return {"id": tid, "server": t["server"], "name": t["name"],
                "desc": (t.get("description") or "")[:DESC_CAP]}

    for r in reviewed:
        task = tagged[r["task_id"]]
        props = {p["name"]: p for p in task.get("resolution_proposals") or []}
        son = {s["gold_name"]: s for s in sonnet[r["task_id"]]["slot_review"]}
        ctx = {
            "task_id": r["task_id"],
            "question": r["question"],
            "steps": task["steps"],
            "final_slots": [{"name": s["gold_name"], "keep": s["keep"], "pick": s["pick"]} for s in r["slots"]],
            "decisions": r["decisions"],
        }
        for slot, res in zip(r["slots"], task["resolution"]):
            name = slot["gold_name"]
            if res["status"] == "missing":
                kind = "mapping"
            elif not slot["keep"]:
                kind = "drop"
            else:
                continue
            prop, sl = props.get(name, {}), son.get(name, {})
            opts = [slot["pick"], prop.get("proposed_id"), sl.get("pick"), *res.get("candidates", [])]
            options = [c for c in dict.fromkeys(o for o in opts if o) if c in tools]
            items.append({
                **ctx, "kind": kind, "gold_name": name,
                "adjudicator": {"keep": slot["keep"], "pick": slot["pick"]},
                "haiku": {"pick": prop.get("proposed_id"), "reason": prop.get("reason")},
                "sonnet": {"pick": sl.get("pick"), "keep": sl.get("keep"), "reason": sl.get("pick_reason")},
                "options": [card(o) for o in options],
                "original_status": res["status"],
            })
        if r["needs_clarification"]:
            items.append({**ctx, "kind": "clarify", "gold_name": None,
                          "adjudicator": {"needs_clarification": True},
                          "haiku": {"needs_clarification": task["needs_clarification"]},
                          "sonnet": {"needs_clarification": sonnet[r["task_id"]].get("needs_clarification")},
                          "options": []})
    catalog = [{"id": tid, "server": t["server"], "name": t["name"],
                "desc": (t.get("description") or "")[:SEARCH_CAP]} for tid, t in tools.items()]
    return {"items": items, "catalog": catalog}


def main() -> None:
    data = build()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    path = PROC / "spot_check.html"
    path.write_text(TEMPLATE.replace("__DATA__", payload), encoding="utf-8")
    kinds = {k: sum(1 for i in data["items"] if i["kind"] == k) for k in ("mapping", "drop", "clarify")}
    print(f"wrote {path}: {len(data['items'])} items {kinds}")


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ToolPrune spot check</title>
<style>
:root{--bg:#fbfaf8;--panel:#fff;--ink:#1c1b19;--mute:#6b6a66;--line:#e4e1da;--accent:#2f5d8a;--ok:#2d7a4b;--warn:#a5671a;--chip:#eef2f6}
@media (prefers-color-scheme:dark){:root{--bg:#17181a;--panel:#1f2124;--ink:#ecebe8;--mute:#9a9892;--line:#33363a;--accent:#7fb0e0;--ok:#6cc08b;--warn:#e0a456;--chip:#2a2f35}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header h1{font-size:15px;margin:0}.bar{flex:1;min-width:120px;height:8px;background:var(--chip);border-radius:4px;overflow:hidden}.bar i{display:block;height:100%;background:var(--ok)}
main{max-width:900px;margin:0 auto;padding:16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px;margin-bottom:16px}.card.done{border-left:4px solid var(--ok)}
button{font:inherit;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:5px 10px;cursor:pointer}
button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}button.sel{outline:2px solid var(--accent)}
.chip{display:inline-block;background:var(--chip);border-radius:11px;padding:2px 9px;margin:2px 4px 2px 0;font-size:12px}.chip.warn{background:transparent;border:1px solid var(--warn);color:var(--warn)}
.mute{color:var(--mute)}.tool{font-family:ui-monospace,monospace;font-size:12px}.hint{font-size:12px;color:var(--mute)}
label.opt{display:block;padding:4px 0}details summary{cursor:pointer;color:var(--mute)}
input[type=search]{width:100%;font:inherit;padding:6px;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:6px}
.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.res{max-height:180px;overflow:auto;border:1px solid var(--line);border-radius:6px;margin-top:4px}
.res div{padding:5px 8px;border-bottom:1px solid var(--line);cursor:pointer}.res div:hover{background:var(--chip)}
</style></head><body>
<header><h1>Spot check</h1><div class="bar"><i id="prog" style="width:0"></i></div><span id="count" class="mute"></span>
<button id="export" class="primary">Export decisions</button></header>
<main id="main"></main>
<script>
const D=__DATA__;const KEY="toolprune-spot-v1";
let dec={};try{dec=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(dec))}catch(e){}};
const k=i=>i.task_id+"|"+(i.gold_name||"");
const el=(t,p={},...c)=>{const e=document.createElement(t);for(const[a,v]of Object.entries(p)){if(a==="class")e.className=v;else if(a.startsWith("on"))e[a]=v;else e.setAttribute(a,v)}for(const x of c.flat())e.append(x&&x.nodeType?x:document.createTextNode(x??""));return e};
const label=id=>{const c=D.catalog.find(x=>x.id===id);return c?c.server+" :: "+c.name:(id||"(none)")};
function render(){const m=document.getElementById("main");m.replaceChildren();
  D.items.forEach((it,n)=>{const key=k(it),d=dec[key],done=!!d;
    const card=el("div",{class:"card"+(done?" done":"")});
    const title={mapping:"Bench tool missing from catalog",drop:"Slot dropped by adjudicator",clarify:"Marked as needing clarification"}[it.kind];
    card.append(el("div",{},el("span",{class:"chip warn"},title)," ",it.gold_name?el("b",{},it.gold_name):""),
      el("p",{style:"font-size:15px"},it.question),
      el("details",{},el("summary",{},"Annotator steps"),el("pre",{style:"white-space:pre-wrap"},it.steps)),
      el("div",{class:"hint"},"All slots: "+it.final_slots.map(s=>`${s.name} → ${s.keep?label(s.pick):"DROPPED"}`).join("  |  ")));
    if(it.decisions.length)card.append(el("details",{},el("summary",{},"Adjudicator notes"),...it.decisions.map(x=>el("div",{class:"hint"},x))));
    if(it.kind==="clarify"){
      card.append(el("div",{class:"hint"},`Haiku: ${it.haiku.needs_clarification} · Sonnet: ${it.sonnet.needs_clarification} · Adjudicator: true`),
        el("div",{class:"actions"},
          el("button",{class:d&&d.needs_clarification===true?"sel":"",onclick:()=>{dec[key]={task_id:it.task_id,gold_name:null,needs_clarification:true};save();render()}},"Yes, underspecified"),
          el("button",{class:d&&d.needs_clarification===false?"sel":"",onclick:()=>{dec[key]={task_id:it.task_id,gold_name:null,needs_clarification:false};save();render()}},"No, it is clear")));
    }else{
      const cur=d?d:{pick:it.adjudicator.pick,keep:it.adjudicator.keep};
      card.append(el("div",{class:"hint"},`Haiku (${it.haiku.pick?label(it.haiku.pick):"none"}): ${it.haiku.reason||"-"}`),
        el("div",{class:"hint"},`Sonnet (${it.sonnet.pick?label(it.sonnet.pick):"none"}, keep=${it.sonnet.keep}): ${it.sonnet.reason||"-"}`),
        el("div",{class:"hint"},`Adjudicator: keep=${it.adjudicator.keep}, pick=${it.adjudicator.pick?label(it.adjudicator.pick):"none"}`));
      it.options.forEach(o=>{const r=el("input",{type:"radio",name:"p"+n,onchange:()=>{dec[key]={task_id:it.task_id,gold_name:it.gold_name,pick:o.id,keep:true};save();render()}});
        r.checked=d&&d.keep&&d.pick===o.id;
        card.append(el("label",{class:"opt"},r," ",el("span",{class:"tool"},o.server+" :: "+o.name),el("div",{class:"hint"},o.desc)))});
      const s=el("input",{type:"search",placeholder:"search the full catalog to pick another tool"});const res=el("div",{class:"res"});res.style.display="none";
      s.oninput=()=>{const q=s.value.toLowerCase().trim();res.replaceChildren();if(q.length<2){res.style.display="none";return}
        const hits=D.catalog.filter(c=>(c.name+" "+c.server+" "+c.desc).toLowerCase().includes(q)).slice(0,25);res.style.display="block";
        hits.forEach(c=>res.append(el("div",{onclick:()=>{dec[key]={task_id:it.task_id,gold_name:it.gold_name,pick:c.id,keep:true};save();render()}},el("span",{class:"tool"},c.server+" :: "+c.name),el("div",{class:"hint"},c.desc))))};
      card.append(el("details",{},el("summary",{},"Pick a different tool"),s,res),
        el("div",{class:"actions"},
          el("button",{class:d&&d.keep&&d.pick===it.adjudicator.pick&&it.adjudicator.keep?"sel":"",disabled:!it.adjudicator.keep,onclick:()=>{dec[key]={task_id:it.task_id,gold_name:it.gold_name,pick:it.adjudicator.pick,keep:true};save();render()}},"Accept adjudicator pick"),
          el("button",{class:d&&d.keep===false?"sel":"",onclick:()=>{dec[key]={task_id:it.task_id,gold_name:it.gold_name,pick:null,keep:false};save();render()}},"Drop this slot (not required)"),
          it.kind==="drop"?el("button",{onclick:()=>{dec[key]={task_id:it.task_id,gold_name:it.gold_name,pick:it.options[0]?it.options[0].id:null,keep:!!it.options[0]};save();render()}},"Restore slot"):""));
      if(d)card.append(el("div",{class:"hint"},"Saved: "+(d.keep===false?"slot dropped":d.keep?`pick ${label(d.pick)}`:`needs_clarification=${d.needs_clarification}`)));
    }
    if(done)card.append(el("div",{class:"actions"},el("button",{onclick:()=>{delete dec[key];save();render()}},"Clear")));
    m.append(card)});
  const n=D.items.filter(i=>dec[k(i)]).length;
  document.getElementById("prog").style.width=(100*n/D.items.length)+"%";
  document.getElementById("count").textContent=`${n}/${D.items.length} decided`;
}
document.getElementById("export").onclick=()=>{
  const out=D.items.filter(i=>dec[k(i)]).map(i=>dec[k(i)]);
  const a=el("a",{href:URL.createObjectURL(new Blob([JSON.stringify(out,null,2)],{type:"application/json"})),download:"spot_decisions.json"});
  document.body.append(a);a.click();a.remove()};
render();
</script></body></html>
"""


if __name__ == "__main__":
    main()
