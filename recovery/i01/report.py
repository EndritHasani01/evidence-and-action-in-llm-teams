"""Read-only exact episode scoring, intended populations, traces and figures.

This module does not import inference or create workers. Unknown outcomes remain
unknown; a terminal unsuccessful episode scores zero, unused turns are unused.
"""

from collections import Counter
import csv
from html import escape
import json
from pathlib import Path
import random
import sqlite3

from .core import canonical, success
from .store import connection


def read_run(run):
    run = Path(run)
    manifest = json.loads((run/"run.json").read_text())
    tables = {name: [] for name in ("episodes", "calls", "attempts", "sessions", "annotations")}
    metadata = {}
    for slot in range(2):
        db = connection(run/f"worker-{slot}.sqlite", True)
        try:
            for name in tables:
                tables[name] += [dict(r, slot=slot) for r in db.execute("SELECT * FROM " + name)]
            if slot == 0:
                metadata = {r["key"]:json.loads(r["value"]) for r in db.execute("SELECT * FROM meta")}
        finally:
            db.close()
    return manifest, tables, metadata


def bootstrap(rows, config):
    if not rows or any(r["retain"] is None or r["clear"] is None for r in rows):
        return None
    strata = {}
    for r in rows:
        strata.setdefault((r["owner"], r["first"]), []).append(r["clear"]-r["retain"])
    rng = random.Random(config["bootstrap_seed"])
    draws = sorted(sum(rng.choice(values) for values in strata.values() for _ in values)/len(rows)
                   for _ in range(config["bootstrap_draws"]))
    lo, hi = draws[int(len(draws)*.025)], draws[min(len(draws)-1, int(len(draws)*.975))]
    return dict(low=lo, high=hi, confidence=.95, draws=len(draws), strata="owner/first-speaker",
                caveat="Exploratory small-sample interval; zero width does not establish equivalence." if lo == hi else "Exploratory small-sample interval.")


def analysis(run):
    manifest, tables, meta = read_run(run)
    episodes = {r["id"]:json.loads(r["state"]) for r in tables["episodes"]}
    calls = {r["id"]:r for r in tables["calls"]}
    attempts = []
    for row in tables["attempts"]:
        req = json.loads(calls[row["call_id"]]["request"])
        outcome = json.loads(row["evidence"]) if row["evidence"] else {}
        attempts.append(dict(row, episode=calls[row["call_id"]]["episode"], seed=req["seed"],
                             settings=req["settings"], input_tokens=outcome.get("input_tokens", len(req.get("input_ids", []))),
                             generated_tokens=outcome.get("generated_tokens"), ready_seconds=outcome.get("ready_seconds"),
                             termination=outcome.get("termination"), device=outcome.get("backend", {}).get("device"),
                             pid=outcome.get("backend", {}).get("pid")))
    world_rows, cost_rows = [], []
    for w in manifest["worlds"]:
        r = {k:w[k] for k in ("id", "group", "owner", "first", "original_truth", "revised_truth")}
        for phase in ("prefix", "retain", "clear"):
            e = episodes.get(w["id"]+"/"+phase)
            r[phase] = success(e, w["original_truth"] if phase == "prefix" else w["revised_truth"])
            r[phase+"_terminal"] = e.get("terminal") if e else None
            r[phase+"_submissions"] = e.get("submissions") if e else None
            a = [v for v in attempts if v["episode"] == w["id"]+"/"+phase]
            c = dict(world=w["id"], phase=phase, complete=bool(e and e.get("terminal")), calls=len(a),
                     input_tokens=sum(v["input_tokens"] for v in a),
                     generated_tokens=None if any(v["generated_tokens"] is None for v in a) else sum(v["generated_tokens"] for v in a),
                     ready_seconds=None if any(v["ready_seconds"] is None for v in a) else sum(v["ready_seconds"] for v in a),
                     observed_seconds=sum(v["ready_seconds"] or 0 for v in a),
                     messages=sum(ev.get("action", {}).get("message") is not None for ev in (e or {}).get("events", []) if ev.get("action")))
            if e is None:
                c.update(ready_seconds=None, generated_tokens=None)
            cost_rows.append(c)
        for mode in ("direct", "thinking"):
            for input_phase in ("original", "revised"):
                cid = f"{w['id']}/control-{input_phase}-{mode}"
                row = calls.get(cid)
                o = json.loads(row["outcome"]) if row and row["outcome"] else None
                if o is not None:
                    from .core import validate_action
                    act, error = validate_action(o.get("visible_text", ""), truncated=o.get("truncated", False), control=True)
                    r[f"control_{input_phase}_{mode}"] = int(not error and not o.get("framing_error") and not o.get("failure") and act["submit"] == w[input_phase+"_truth"])
                else:
                    r[f"control_{input_phase}_{mode}"] = None
        world_rows.append(r)
    main = [r for r in world_rows if r["group"] == "main"]
    pairs = Counter("unknown" if r["retain"] is None or r["clear"] is None else
                    ("both" if r["retain"] and r["clear"] else "retain_only" if r["retain"] else "clear_only" if r["clear"] else "neither") for r in main)
    known = [r for r in main if r["retain"] is not None and r["clear"] is not None]
    lower = sum((r["clear"] if r["clear"] is not None else 0) - (r["retain"] if r["retain"] is not None else 1) for r in main)/20
    upper = sum((r["clear"] if r["clear"] is not None else 1) - (r["retain"] if r["retain"] is not None else 0) for r in main)/20
    correct_prefix = [r for r in main if r["prefix"] == 1]
    failures = Counter(e["terminal"] for e in episodes.values() if e.get("terminal"))
    contingency = sum(a["contingency"] for a in attempts)
    gap = meta.get("lost_spending", {"upper":0, "resolved":True})
    complete = bool(meta.get("freeze")) and len(known) == 20 and not any(a["status"]=="admitted" for a in attempts) and all(r["prefix"] is not None and r.get("control_revised_"+meta.get("selected_mode", "direct")) is not None for r in main)
    summary = dict(status="complete" if complete and not gap.get("upper") and gap.get("resolved") else "partial",
                   intended_worlds=20, known_pairs=len(known), paired_counts=dict(pairs),
                   clear_minus_retain=sum(r["clear"]-r["retain"] for r in known)/20 if len(known) == 20 else None,
                   complete_case_descriptive_mean=sum(r["clear"]-r["retain"] for r in known)/len(known) if known else None,
                   missingness_bounds=[lower, upper], interval=bootstrap(main, manifest["config"]),
                   correct_prefix_denominator=len(correct_prefix), unknown_prefixes=sum(r["prefix"] is None for r in main),
                   correct_prefix_interval=bootstrap(correct_prefix, manifest["config"]),
                   correct_prefix_mean=(sum(r["clear"]-r["retain"] for r in correct_prefix)/len(correct_prefix)
                       if correct_prefix and all(r["clear"] is not None and r["retain"] is not None for r in correct_prefix) else None),
                   attempts=len(attempts), contingency=contingency, hard_limit=500, historical_attempts_separate=45,
                   in_flight=sum(a["status"] == "admitted" for a in attempts), gates={k:v for k,v in meta.items() if k not in ("schema","binding")},
                   terminal_reasons=dict(failures), lost_spending=gap)
    policy_costs=[]
    by_cost={(r["world"],r["phase"]):r for r in cost_rows}
    for w in world_rows:
        for phase in ("retain","clear"):
            prefix, recovery=by_cost[(w["id"],"prefix")],by_cost[(w["id"],phase)]
            policy_costs.append(dict(world=w["id"],group=w["group"],policy=phase,success=w[phase],
                physical_prefix_shared_once=True,logical_prefix_calls=prefix["calls"],recovery_calls=recovery["calls"],
                logical_end_to_end_calls=prefix["calls"]+recovery["calls"],
                complete=prefix["complete"] and recovery["complete"],
                post_revision_ready_seconds=recovery["ready_seconds"] if recovery["complete"] else None,
                observed_post_revision_seconds=recovery["observed_seconds"],
                generated_tokens=recovery["generated_tokens"] if recovery["complete"] else None,
                paired_category=("unknown" if w["retain"] is None or w["clear"] is None else "both" if w["retain"] and w["clear"] else "retain_only" if w["retain"] else "clear_only" if w["clear"] else "neither")))
    summary["physical_ready_seconds_observed"]=sum(a["ready_seconds"] or 0 for a in attempts)
    summary["attempts_unknown_ready_seconds"]=sum(a["ready_seconds"] is None for a in attempts)
    summary["generated_tokens_observed"]=sum(a["generated_tokens"] or 0 for a in attempts)
    summary["attempts_unknown_generated_tokens"]=sum(a["generated_tokens"] is None for a in attempts)
    summary["model_load_seconds_observed"]=sum(json.loads(s["evidence"]).get("load",{}).get("load_seconds",0) for s in tables["sessions"])
    summary["provider_assignment_release"]= "unknown unless supplied separately; observation and process exit do not establish allocation boundaries"
    paired_costs=[]
    for w in main:
        r,c=by_cost[(w["id"],"retain")],by_cost[(w["id"],"clear")]
        row=dict(world=w["id"],owner=w["owner"],first=w["first"],retain_success=w["retain"],clear_success=w["clear"])
        for key in ("ready_seconds","calls","generated_tokens","input_tokens","messages"):
            rv=r[key] if r["complete"] else None
            cv=c[key] if c["complete"] else None
            row["retain_"+key]=rv; row["clear_"+key]=cv
            row["clear_minus_retain_"+key]=cv-rv if rv is not None and cv is not None else None
        paired_costs.append(row)
    timing=[dict(owner=r["owner"],first=r["first"],retain=r["retain_ready_seconds"],clear=r["clear_ready_seconds"]) for r in paired_costs]
    summary["principal_effort_clear_minus_retain_seconds"]=(sum(r["clear"]-r["retain"] for r in timing)/20 if all(r["retain"] is not None and r["clear"] is not None for r in timing) else None)
    summary["principal_effort_interval"]=bootstrap(timing,manifest["config"])
    summary["cost_complete_pairs"]=sum(r["retain"] is not None and r["clear"] is not None for r in timing)
    failure_rows=[]
    world_by_id={w["id"]:w for w in manifest["worlds"]}
    for ep in tables["episodes"]:
        state=json.loads(ep["state"])
        world=world_by_id.get(ep["id"].split("/")[0])
        if not world or not state.get("terminal"): continue
        phase=ep["id"].split("/")[-1]
        truth=world["original_truth"] if phase=="prefix" else world["revised_truth"]
        labels=[]
        if state.get("terminal") in ("waiting_deadlock","horizon_exhausted"): labels.append(state["terminal"])
        if any(v is not None and v!=truth for v in state.get("submissions",[])): labels.append("wrong_submission")
        for event in state.get("events",[]):
            if event.get("error"):
                labels.append(event["error"] if event["error"] in manifest["config"]["rubric"] else "provider_failure")
            if phase in ("retain","clear") and event.get("action") and event["action"].get("submit")==world["before"]:
                labels.append("obsolete_value_repeated")
        for label in sorted(set(labels)):
            failure_rows.append(dict(episode=ep["id"],label=label,calls=[e["call"] for e in state.get("events",[])],
                                     basis="Observable record; internal explanation remains ambiguous"))
    return dict(summary=summary, worlds=world_rows, costs=cost_rows, policy_costs=policy_costs, attempts=attempts,
                paired_costs=paired_costs,failure_analysis=failure_rows,
                episodes=tables["episodes"],traces=tables["calls"], annotations=tables["annotations"], sessions=tables["sessions"], manifest=manifest)


def csv_file(path, rows):
    keys = sorted({k for row in rows for k in row})
    with Path(path).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow({k:canonical(v) if isinstance(v, (dict, list)) else v for k,v in row.items()})


def figures(result, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out = Path(out)
    out.mkdir(exist_ok=True)
    main = [w for w in result["worlds"] if w["group"] == "main"]
    costs = {(r["world"], r["phase"]):r for r in result["costs"]}
    plots = []
    fig, ax = plt.subplots(figsize=(7, 3.6), layout="constrained")
    cats = ["both", "retain_only", "clear_only", "neither", "unknown"]
    ax.bar(cats, [result["summary"]["paired_counts"].get(c,0) for c in cats], color=["#297c71", "#a26635", "#596dce", "#b84b50", "#999999"])
    ax.set(ylabel="Worlds (intended n=20)", title="Paired exact recovery success")
    plots.append(("paired-outcomes", fig))
    for metric in ("ready_seconds", "calls", "generated_tokens"):
        fig, ax = plt.subplots(figsize=(9,4), layout="constrained")
        for phase, color in (("retain", "#a26635"), ("clear", "#596dce")):
            for i, w in enumerate(main):
                c = costs[(w["id"],phase)]
                value = c[metric] if c["complete"] else None
                if value is not None:
                    ax.scatter(i+1, value, c=color, marker="o" if w[phase] == 1 else "x", label=phase if i == 0 else None)
        ax.set(xlabel="Fixed main world index", ylabel=metric.replace("_", " "), title="Recovery cost; circles success, crosses unsuccessful; unknown omitted")
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend()
        plots.append(("recovery-"+metric,fig))
    fig, ax = plt.subplots(figsize=(7,3.6), layout="constrained")
    reasons = result["summary"]["terminal_reasons"] or {"no recorded terminal episodes":0}
    ax.barh(list(reasons), list(reasons.values()), color="#566d80")
    ax.set(xlabel="Episodes", title="Procedural termination / coverage")
    plots.append(("termination-coverage", fig))
    for name, fig in plots:
        for ext in ("svg", "png"):
            fig.savefig(out/f"{name}.{ext}", dpi=180)
        plt.close(fig)


def write_report(run, out, *, plot=True):
    result = analysis(run)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out/"analysis.json").write_text(json.dumps(result, indent=2, ensure_ascii=True), encoding="utf-8")
    for name in ("worlds", "costs", "policy_costs", "paired_costs", "failure_analysis", "attempts", "annotations", "sessions"):
        csv_file(out/(name+".csv"), result[name])
    csv_file(out/"plotting-data.csv", result["costs"])
    (out/"paired-results.csv").write_text("category,worlds\n" + "".join(f"{k},{v}\n" for k,v in result["summary"]["paired_counts"].items()), encoding="utf-8")
    traces = result["traces"]
    (out/"conversations.jsonl").write_text("".join(canonical(dict(record_type="episode_checkpoint",**e))+"\n" for e in result["episodes"])+"".join(canonical(dict(record_type="call",**t))+"\n" for t in traces), encoding="utf-8")
    body = ['<!doctype html><meta charset="utf-8"><title>I-01 conversations</title><style>body{font:16px system-ui;max-width:1100px;margin:2rem auto}pre{white-space:pre-wrap;overflow-wrap:anywhere}.audit{background:#fff3db;padding:1rem}details{border-bottom:1px solid #ccc;padding:1rem}</style>',
            '<h1>Complete I-01 trace audit</h1><p>Private submissions, truth and thinking are evaluator audit material. They never enter partner views. Every registered request/outcome is listed.</p>']
    text = []
    for ep in result["episodes"]:
        state=json.loads(ep["state"])
        phase_text=f"PHASE CHECKPOINT {ep['id']}\n{json.dumps(state,indent=2)}"
        body.append('<details><summary>Phase boundary / delivery timeline '+escape(ep["id"])+'</summary><pre>'+escape(phase_text)+'</pre></details>')
        text.append(phase_text)
    for t in traces:
        req = json.loads(t["request"])
        outcome = json.loads(t["outcome"]) if t["outcome"] else None
        entry = f"{t['id']}\nPERMITTED VIEW\n{json.dumps(req['view'],indent=2)}\nEXACT RENDERED PROMPT\n{req.get('rendered','')}\nRAW OUTCOME (including private thinking and tokens)\n{json.dumps(outcome,indent=2)}\nEffect committed: {t['effect_committed']}"
        body.append(f'<details id="{escape(t["id"],quote=True)}"><summary>{escape(t["id"])}</summary><pre>{escape(entry)}</pre></details>')
        text.append(entry)
    body.append('<h2 class="audit">Evaluator annotations, inputs and truth</h2><pre class="audit">'+escape(json.dumps(dict(worlds=result["worlds"], annotations=result["annotations"]),indent=2))+'</pre>')
    (out/"conversations.html").write_text("\n".join(body),encoding="utf-8")
    (out/"conversations.txt").write_text("\n\n".join(text),encoding="utf-8")
    s = result["summary"]
    narrative = (f"# I-01 course recovery report — {s['status']}\n\n"
                 f"Intended main population: 20 independent worlds; known paired outcomes: {s['known_pairs']}/20. "
                 f"Physical new attempts: {s['attempts']}/500; historical 45 recorded separately.\n\n"
                 f"Clear-minus-retain mean: {s['clear_minus_retain']}; unknown bounds: {s['missingness_bounds']}. "
                 f"Correct-prefix descriptive denominator: {s['correct_prefix_denominator']}; unknown prefixes: {s['unknown_prefixes']}.\n\n"
                 "This is a controlled recovery extension of SILO-BENCH I-01. Clearing removes remote information in prior messages. "
                 "Small sample and one seed/prefix per world limit inference; zero-width intervals do not establish equivalence. "
                 "Principal effort is ready-model recovery inference time. Costs of unsuccessful episodes are spending, not useful efficiency. "
                 "Loading, observed allocation and unknown provider time are separate. Shared prefix is physically charged once and logically to both policies. "
                 "No native benchmark, pure anchoring, correction-specific, broad generalization or superiority claim follows.\n\n"
                 "Review every trace using the frozen rubric; human labels require call references. Ambiguous mechanisms remain ambiguous. "
                 "Save the executed notebook separately and download the latest portable archive off session.\n\n"
                 "```json\n"+json.dumps(s,indent=2)+"\n```\n")
    (out/"overview.md").write_text(narrative,encoding="utf-8")
    (out/"overview.html").write_text('<!doctype html><meta charset="utf-8"><title>I-01 report</title><h1>I-01 report</h1><a href="conversations.html">All conversations</a><pre style="white-space:pre-wrap">'+escape(narrative)+'</pre>',encoding="utf-8")
    if plot:
        figures(result, out/"figures")
    return dict(directory=str(out), summary=s, files=[p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()])
