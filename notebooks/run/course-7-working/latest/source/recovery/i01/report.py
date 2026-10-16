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
from .store import connection, Store, validate_call_slots, usage
from .policy import (qualification, AUTOMATIC_POLICIES, validation_detail,
                     runtime_safe, admission_blocks)


def read_run(run):
    run = Path(run)
    manifest = json.loads((run/"run.json").read_text())
    tables = {name: [] for name in ("episodes", "calls", "attempts", "sessions", "annotations")}
    metadata = {}
    for slot in range(2):
        Store.validate(run/f'worker-{slot}.sqlite', {'manifest':manifest},allow_legacy=True)
        db = connection(run/f"worker-{slot}.sqlite", True)
        try:
            db.execute('BEGIN')
            for name in tables:
                tables[name] += [dict(r, slot=slot) for r in db.execute("SELECT * FROM " + name)]
            if slot == 0:
                metadata = {r["key"]:json.loads(r["value"]) for r in db.execute("SELECT * FROM meta")}
            else:
                metadata.update({r['key']:json.loads(r['value']) for r in db.execute("SELECT * FROM meta WHERE key LIKE 'timeout_termination/%'")})
        finally:
            db.close()
    validate_call_slots(manifest, tables['calls'])
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
                             dispatch_seconds=outcome.get("dispatch_seconds"),observed_seconds=outcome.get("observed_seconds",outcome.get("dispatch_seconds",outcome.get("ready_seconds"))),
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
                     observed_seconds=sum(v["observed_seconds"] or 0 for v in a),
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
    budget = usage(tables['attempts'], meta)
    summary.update(campaign_attempts=budget['campaign_attempts'], prior_attempts=budget['prior_attempts'],
                   attempt_scope=budget['attempt_scope'],
                   missing_prior_studies=budget['missing_prior_studies'],
                   contingency=budget['contingency'], local_contingency=budget['local_contingency'],
                   remaining_attempt_allowance=budget['remaining'], prior_spending=meta.get('prior_spending', []))
    policy_costs=[]
    by_cost={(r["world"],r["phase"]):r for r in cost_rows}
    for w in world_rows:
        for phase in ("retain","clear"):
            prefix, recovery=by_cost[(w["id"],"prefix")],by_cost[(w["id"],phase)]
            policy_costs.append(dict(world=w["id"],group=w["group"],policy=phase,success=w[phase],
                physical_prefix_shared_once=True,logical_prefix_calls=prefix["calls"] if prefix['complete'] else None,
                recovery_calls=recovery["calls"] if recovery['complete'] else None,
                logical_end_to_end_calls=prefix["calls"]+recovery["calls"] if prefix['complete'] and recovery['complete'] else None,
                observed_prefix_calls=prefix['calls'],observed_recovery_calls=recovery['calls'],
                observed_end_to_end_calls=prefix['calls']+recovery['calls'],
                complete=prefix["complete"] and recovery["complete"],
                post_revision_ready_seconds=recovery["ready_seconds"] if recovery["complete"] else None,
                observed_post_revision_seconds=recovery["observed_seconds"],
                generated_tokens=recovery["generated_tokens"] if recovery["complete"] else None,
                paired_category=("unknown" if w["retain"] is None or w["clear"] is None else "both" if w["retain"] and w["clear"] else "retain_only" if w["retain"] else "clear_only" if w["clear"] else "neither")))
    summary["physical_ready_seconds_observed"]=sum(a["ready_seconds"] or 0 for a in attempts)
    summary["physical_dispatch_seconds_observed"]=sum(a["observed_seconds"] or 0 for a in attempts)
    summary["attempts_unknown_ready_seconds"]=sum(a["ready_seconds"] is None for a in attempts)
    summary["generated_tokens_observed"]=sum(a["generated_tokens"] or 0 for a in attempts)
    summary['campaign_ready_seconds_observed']=summary['physical_ready_seconds_observed']+sum(p.get('ready_seconds_observed',0) for p in meta.get('prior_spending',[]))
    summary['campaign_generated_tokens_observed']=summary['generated_tokens_observed']+sum(p.get('generated_tokens_observed',0) for p in meta.get('prior_spending',[]))
    summary['campaign_attempts_unknown_ready_seconds']=sum(a['ready_seconds'] is None for a in attempts)+sum(p.get('attempts_unknown_ready_seconds',0) for p in meta.get('prior_spending',[]))
    summary["attempts_unknown_generated_tokens"]=sum(a["generated_tokens"] is None for a in attempts)
    summary["model_load_seconds_observed"]=sum(json.loads(s["evidence"]).get("load",{}).get("load_seconds",0) for s in tables["sessions"])
    summary["failed_model_load_seconds_observed"]=sum(json.loads(s["evidence"]).get("load_seconds") or 0 for s in tables["sessions"] if json.loads(s["evidence"]).get("load_failure"))
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
        if phase=='prefix' or phase in ('control-original-direct','control-original-thinking'):
            truth=world['original_truth']
        elif phase in ('retain','clear','control-revised-direct','control-revised-thinking'):
            truth=world['revised_truth']
        else: raise ValueError('Unknown saved episode type: '+ep['id'])
        labels=[]
        if state.get("terminal") in ("waiting_deadlock","horizon_exhausted"): labels.append(state["terminal"])
        if any(v is not None and v!=truth for v in state.get("submissions",[])): labels.append("wrong_submission")
        if state.get('error'):
            error=state['error']
            labels.append(error if error in manifest['config']['rubric'] else 'provider_failure')
        for event in state.get("events",[]):
            if event.get("error"):
                labels.append(event["error"] if event["error"] in manifest["config"]["rubric"] else "provider_failure")
            if phase in ("retain","clear") and event.get("action") and event["action"].get("submit")==world["before"]:
                labels.append("obsolete_value_repeated")
        for label in sorted(set(labels)):
            refs=[e['call'] for e in state.get('events',[])] or [r['id'] for r in tables['calls'] if r['episode']==ep['id']]
            scope='episode_context'
            if label in ('malformed_action','truncated_action','provider_failure'):
                refs=[e['call'] for e in state.get('events',[]) if e.get('error') and (e['error']==label or label=='provider_failure' and e['error'] not in manifest['config']['rubric'])] or refs
                scope='exact_offending_calls'
            elif label in ('wrong_submission','obsolete_value_repeated') and state.get('events'):
                refs=[e['call'] for e in state['events'] if e.get('action') and e['action']['submit'] is not None and
                      (e['action']['submit']!=truth if label=='wrong_submission' else e['action']['submit']==world['before'])]
                scope='exact_offending_calls'
            failure_rows.append(dict(episode=ep["id"],label=label,calls=refs,
                                     call_scope=scope,basis="Observable record; internal explanation remains ambiguous"))
    screens=qualification(manifest,tables,meta)
    summary['qualification']={mode:{k:v for k,v in q.items() if k!='controls'} for mode,q in screens.items()}
    plan=meta.get('execution_plan',{})
    summary.update(execution_policy=plan.get('policy','individual-stages'),
                   human_review_status='retrospective_pending' if plan.get('policy') in AUTOMATIC_POLICIES else 'see_recorded_reviews')
    validation=[]
    world_map={w['id']:w for w in manifest['worlds']}
    for call in tables['calls']:
        world=world_map.get(call['episode'].split('/')[0])
        if world is None:continue  # Forced hardware probes are not scientific JSON trials.
        req=json.loads(call['request'])
        outcome=json.loads(call['outcome']) if call['outcome'] else None
        phase=call['episode'].split('/')[1]
        detail=validation_detail(outcome,control='/control-' in call['episode']) if outcome else dict(json_valid=None,schema_valid=None,legal_action=None,error=None,reason=None)
        safe=runtime_safe(outcome,meta.get('timeout_termination/'+call['id'])) if outcome else None
        validation.append(dict(call=call['id'],world=world['id'],group=world['group'],phase=phase,
            agent=req['view'].get('agent'),recorded=outcome is not None,committed=bool(call['effect_committed']),
            policy=plan.get('policy','individual-stages'),**detail,runtime_safe=safe,
            admission_blocking=admission_blocks(plan.get('policy'),world['group'],phase,detail,safe=safe) if outcome else None))
    compliance=[]
    for group,phase in sorted({(r['group'],r['phase']) for r in validation}):
        rows=[r for r in validation if r['group']==group and r['phase']==phase]
        recorded=[r for r in rows if r['recorded']]
        compliance.append(dict(group=group,phase=phase,registered_calls=len(rows),recorded_calls=len(recorded),
            unknown_calls=len(rows)-len(recorded),committed_calls=sum(r['committed'] for r in rows),
            json_valid=sum(r['json_valid'] for r in recorded),schema_valid=sum(r['schema_valid'] for r in recorded),
            legal_actions=sum(r['legal_action'] for r in recorded),admission_blocking=sum(r['admission_blocking'] for r in recorded)))
    blocked=[key for key,value in meta.items() if key.startswith('automatic/pilot-') and value.get('passed') is False]
    stage_path=Path(run)/'receipts/stage-error.json'
    stage=json.loads(stage_path.read_text(encoding='utf-8')) if stage_path.is_file() else {}
    if stage and not stage.get('resolved'):blocked.append(stage['action']+': '+stage['error'])
    if meta.get('model_defect'):blocked.append('model/runtime defect')
    if budget['remaining'] is None or budget['in_flight']:blocked.append('unresolved spending')
    summary.update(scientific_gate_status='blocked' if blocked else 'complete' if complete else 'pending',
                   blocking_reasons=blocked,session_window=meta.get('window'),failure_cleanup=meta.get('failure_cleanup'))
    pilot_checks=[dict(pilot=n,world=f'pilot-{n-1:02d}',passed=meta.get(f'automatic/pilot-{n}',{}).get('passed'),
                       checks=meta.get(f'automatic/pilot-{n}',{}).get('checks'),
                       policy=meta.get(f'automatic/pilot-{n}',{}).get('policy'),
                       protocol_errors=meta.get(f'automatic/pilot-{n}',{}).get('protocol_errors'),
                       recovery_protocol_errors=meta.get(f'automatic/pilot-{n}',{}).get('recovery_protocol_errors'),
                       prefix_protocol_errors=meta.get(f'automatic/pilot-{n}',{}).get('prefix_protocol_errors'),
                       control_protocol_errors=meta.get(f'automatic/pilot-{n}',{}).get('control_protocol_errors'),
                       original_team_completed=meta.get(f'automatic/pilot-{n}',{}).get('original_team_completed'),
                       original_messages=meta.get(f'automatic/pilot-{n}',{}).get('original_messages'),
                       useful_communication=meta.get(f'review/pilot-{n}',{}).get('useful_communication'),
                       human_review=meta.get(f'automatic/pilot-{n}',{}).get('human_review','not_recorded')) for n in (1,2,3)]
    return dict(summary=summary, worlds=world_rows, costs=cost_rows, policy_costs=policy_costs, attempts=attempts,
                pilot_checks=pilot_checks,validation_details=validation,protocol_compliance=compliance,
                qualification=screens,qualification_controls=[r for mode in screens.values() for r in mode['controls']],
                prior_spending=meta.get('prior_spending',[]),
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
    from matplotlib.ticker import MaxNLocator
    out = Path(out)
    out.mkdir(exist_ok=True)
    main = [w for w in result["worlds"] if w["group"] == "main"]
    costs = {(r["world"], r["phase"]):r for r in result["costs"]}
    plots = []
    fig, ax = plt.subplots(figsize=(8,3.8),layout='constrained')
    modes=list(result['qualification']);bottom=[0,0]
    for label,key,color in (('Correct final','correct','#297c71'),('Wrong scalar','wrong_scalar','#a26635'),('Invalid output','protocol_errors','#b84b50'),('Pending / unexecuted',None,'#999999')):
        values=[q[key] if key else 12-q['correct']-q['wrong_scalar']-q['protocol_errors'] for q in result['qualification'].values()]
        ax.bar(modes,values,bottom=bottom,label=label,color=color)
        bottom=[a+b for a,b in zip(bottom,values)]
    ax.set(ylabel='Fixed planned controls per mode',title='Qualification coverage and exact outputs; not a main result',ylim=(0,15))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True));ax.legend(fontsize=8,ncol=2,loc='upper center')
    plots.append(('qualification-outcomes',fig))
    fig,axes=plt.subplots(1,2,figsize=(9,3.8),layout='constrained')
    labels=[f"{mode}\n{q['recorded']}/12 raw outcomes" for mode,q in result['qualification'].items()]
    for axis,key,label in zip(axes,('ready_seconds_observed','generated_tokens_observed'),('Ready-model seconds','Generated tokens')):
        axis.bar(labels,[q[key] for q in result['qualification'].values()],color=['#297c71','#596dce'])
        axis.set(ylabel=label)
    fig.suptitle('Observed qualification effort; mode scopes may differ, invalid outputs included',fontsize=10)
    plots.append(('qualification-effort',fig))
    fig, ax = plt.subplots(figsize=(7, 3.6), layout="constrained")
    cats = ["both", "retain_only", "clear_only", "neither", "unknown"]
    ax.bar(["Both correct","Retain only","Clear only","Neither","Unknown"], [result["summary"]["paired_counts"].get(c,0) for c in cats], color=["#297c71", "#a26635", "#596dce", "#b84b50", "#999999"])
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set(ylabel="Worlds (intended n=20)", title="Paired exact recovery success")
    plots.append(("paired-outcomes", fig))
    for metric in ("ready_seconds", "calls", "generated_tokens"):
        fig, ax = plt.subplots(figsize=(9,4), layout="constrained")
        for phase, color in (("retain", "#a26635"), ("clear", "#596dce")):
            labeled=False
            for i, w in enumerate(main):
                c = costs[(w["id"],phase)]
                value = c[metric] if c["complete"] else None
                if value is not None:
                    ax.scatter(i+1, value, c=color, marker="o" if w[phase] == 1 else "x", label=phase if not labeled else None)
                    labeled=True
        for i,w in enumerate(main):
            r,c=costs[(w["id"],"retain")],costs[(w["id"],"clear")]
            if r["complete"] and c["complete"] and r[metric] is not None and c[metric] is not None:
                ax.plot([i+1,i+1],[r[metric],c[metric]],color="#c5c5c5",linewidth=1,zorder=0)
        ax.set(xlabel="Fixed main world index", ylabel=metric.replace("_", " "), title="Recovery cost; circles success, crosses unsuccessful; unknown omitted")
        ax.set_xlim(.5,20.5); ax.set_xticks(range(1,21)); ax.tick_params(axis="x",labelsize=9)
        if not any(costs[(w['id'],p)]['complete'] for w in main for p in ('retain','clear')):
            ax.text(.5,.5,'No main recovery data recorded.\nPilot results are reported separately.',
                    transform=ax.transAxes,ha='center',va='center',color='#566d80')
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend()
        plots.append(("recovery-"+metric,fig))
    fig, ax = plt.subplots(figsize=(7,3.6), layout="constrained")
    reasons = result["summary"]["terminal_reasons"] or {"no recorded terminal episodes":0}
    ax.barh(list(reasons), list(reasons.values()), color="#566d80")
    ax.set(xlabel="Episodes", title="Procedural termination / coverage")
    plots.append(("termination-coverage", fig))
    fig,ax=plt.subplots(figsize=(8,3.6),layout="constrained")
    failures=Counter(r["label"] for r in result["failure_analysis"]) or {"no recorded failure labels":0}
    ax.barh(list(failures),list(failures.values()),color="#aa5f59")
    ax.set(xlabel="Episodes with observable label (labels can overlap)",title="Observable failure audit; no inferred internal mechanism")
    plots.append(("failure-labels",fig))
    for name, fig in plots:
        for ext in ("svg", "png"):
            fig.savefig(out/f"{name}.{ext}", dpi=180)
        plt.close(fig)


def write_report(run, out, *, plot=True):
    result = analysis(run)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out/"analysis.json").write_text(json.dumps(result, indent=2, ensure_ascii=True), encoding="utf-8")
    for name in ("worlds", "costs", "policy_costs", "paired_costs", "failure_analysis", "attempts", "annotations", "sessions", "qualification_controls", "prior_spending", "pilot_checks", "validation_details", "protocol_compliance"):
        csv_file(out/(name+".csv"), result[name])
    csv_file(out/"plotting-data.csv", result["costs"])
    csv_file(out/"plotting-outcomes.csv", result["worlds"])
    (out/"paired-results.csv").write_text("category,worlds\n" + "".join(f"{k},{v}\n" for k,v in result["summary"]["paired_counts"].items()), encoding="utf-8")
    traces = result["traces"]
    (out/"conversations.jsonl").write_text("".join(canonical(dict(record_type="episode_checkpoint",**e))+"\n" for e in result["episodes"])+"".join(canonical(dict(record_type="call",**t))+"\n" for t in traces), encoding="utf-8")
    body = ['<!doctype html><meta charset="utf-8"><title>I-01 conversations</title><style>body{font:16px system-ui;max-width:1100px;margin:2rem auto}pre{white-space:pre-wrap;overflow-wrap:anywhere}.audit{background:#fff3db;padding:1rem}details{border-bottom:1px solid #ccc;padding:1rem}</style>',
            '<h1>Complete I-01 trace audit</h1><p>Private submissions, truth and thinking are evaluator audit material. They never enter partner views. Every registered request/outcome is listed.</p>']
    text = [f"I-01 saved conversation audit\nStudy: {result['manifest']['study_id']}\nRecorded calls: {len(traces)}\nKnown main pairs: {result['summary']['known_pairs']}/20\n"+
            ('No model calls or conversations are recorded; unexecuted outcomes remain unknown.' if not traces else 'Private evaluator audit follows; no hidden reasoning enters peer histories.')]
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
    progress=[('Scalar interface qualification',str(result['qualification']['direct']['committed'])+'/12 committed; eligible '+str(result['qualification']['direct']['passed'])),
              *[(f"Pilot {p['pilot']} admission",'Pending' if p['passed'] is None else 'Admitted recorded outcomes' if p['passed'] else 'Blocked') for p in result['pilot_checks']],
              ('Main paired coverage',str(s['known_pairs'])+'/20'),
              ('Failure worker closure',str((s['failure_cleanup'] or {}).get('termination_confirmed','No failure cleanup recorded'))),
              ('Provider release','Unknown unless established separately')]
    diagnostics_html=['<h2>Admission and protocol diagnostics</h2><p>Scientific gate: <b>'+escape(s['scientific_gate_status'])+'</b>. '+escape('; '.join(s['blocking_reasons']))+'</p>',
        '<p>A successful snapshot preserves evidence; it does not clear a blocked gate. Policy: '+escape(s['execution_policy'])+'. Human review: '+escape(s['human_review_status'])+'.</p>',
        '<p><a href="validation_details.csv">Every scientific action</a> · <a href="protocol_compliance.csv">Phase denominators</a> · <a href="pilot_checks.csv">Pilot admission checks</a></p>',
        '<table><tr><th>Stage</th><th>Recorded state</th></tr>'+''.join('<tr><td>'+escape(k)+'</td><td>'+escape(v)+'</td></tr>' for k,v in progress)+'</table>',
        '<p>Admission preserves measured mistakes; it does not mean every action was legal, the original team completed, or recovery succeeded.</p>',
        '<table><tr><th>Call</th><th>Reason</th><th>Admission blocking</th></tr>']
    for row in validation_errors(result):
        diagnostics_html.append('<tr>'+''.join('<td>'+escape(str(row[key]))+'</td>' for key in ('call','reason','admission_blocking'))+'</tr>')
    diagnostics_html.append('</table>')
    qualification_text='## Qualification and protocol admission\n\nMathematical accuracy is reported separately from protocol eligibility. Historical decisions retain their original rule. Thinking completion is not inferred from a missing aggregate.\n\n'
    qualification_text+='| Mode | Committed / planned | Correct | Wrong scalar | Invalid | Unexecuted | Current eligible | Ready seconds | Tokens | Historical passed |\n|---|---:|---:|---:|---:|---:|---|---:|---:|---|\n'
    for mode,q in result['qualification'].items():
        qualification_text+=f"| {mode} | {q['committed']}/12 | {q['correct']} | {q['wrong_scalar']} | {q['protocol_errors']} | {q['unexecuted']} | {q['passed']} | {q['ready_seconds_observed']:.3f} | {q['generated_tokens_observed']} | {(q['historical_gate'] or {}).get('passed', 'not recorded')} |\n"
    qualification_text+='\nSee qualification_controls.csv and conversations.html for every planned control, exact answer/truth, validity, effort and call reference. Unresolved attempts and raw-but-uncommitted calls are pending, not unexecuted.\n\n'
    narrative = (f"# I-01 course recovery report — {s['status']}\n\n"
                 f"Execution policy: {s['execution_policy']}. Human communication/mechanism review: {s['human_review_status']}. "
                 "Automatic pilot checks establish protocol/evidence/resource eligibility, not useful communication or human approval. "
                 "See pilot_checks.csv and the complete conversations.\n\n"
                 f"Intended main population: 20 independent worlds; known paired outcomes: {s['known_pairs']}/20. "
                 f"Budget scope: {s['attempt_scope']}. Current-study physical attempts: {s['attempts']}; prior-study charges: {s['prior_attempts']}; campaign total: {s['campaign_attempts']}/500. "
                 f"Shared contingency used: {s['contingency']}/28; historical 45 recorded separately.\n\n"+qualification_text+
                 f"Known prior studies still requiring reconciliation: {s['missing_prior_studies']}. Remaining allowance: {s['remaining_attempt_allowance']} (unknown blocks admission).\n\n"+
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
    html=['<!doctype html><meta charset="utf-8"><title>I-01 research report</title><style>body{font:16px system-ui;line-height:1.5;max-width:1200px;margin:2rem auto;padding:0 1rem;color:#243345}header{border-bottom:3px solid #297c71;padding-bottom:1rem}.cards{display:flex;gap:1rem;flex-wrap:wrap}.card{background:#edf3f5;padding:1rem;border-radius:8px;min-width:180px}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:.5rem;border-bottom:1px solid #dae1e5;text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere}img{max-width:100%}</style>',
          f'<header><h1>I-01 distributed-team recovery</h1><p>Controlled recovery extension of SILO-BENCH I-01 · {escape(s["status"])} evidence</p><a href="conversations.html">Browse every prompt, action and raw audit outcome</a></header>',
          f'<div class="cards"><div class="card">Known pairs<br><b>{s["known_pairs"]}/20</b></div><div class="card">Campaign physical attempts<br><b>{s["campaign_attempts"]}/500</b> ({s["attempts"]} here)</div><div class="card">Correct-prefix stratum<br><b>{s["correct_prefix_denominator"]}</b></div><div class="card">Clear minus retain<br><b>{s["clear_minus_retain"]}</b></div></div>',
          '<h2>All intended worlds</h2><p>Unknown is distinct from a recorded unsuccessful outcome. Controls never select the population.</p><table><tr><th>World</th><th>Group</th><th>Old truth</th><th>New truth</th><th>Prefix</th><th>Retain</th><th>Clear</th></tr>']
    # Qualification leads the report while main is unknown; complete traces stay
    # in the existing escaped conversation audit, rather than another data store.
    from urllib.parse import quote
    qualification_html=['<h2>Qualification and partial progress</h2><p>Mathematical accuracy is a diagnostic. Current eligibility and original gate decisions remain distinct; physical completion alone does not establish valid output.</p><table><tr><th>Mode</th><th>Committed / planned</th><th>Correct</th><th>Wrong scalar</th><th>Invalid</th><th>Unexecuted</th><th>Current eligible</th><th>Historical passed</th></tr>']
    for mode,q in result['qualification'].items():
        values=(mode,str(q['committed'])+'/12',q['correct'],q['wrong_scalar'],q['protocol_errors'],q['unexecuted'],q['passed'],(q['historical_gate'] or {}).get('passed','not recorded'))
        qualification_html.append('<tr>'+''.join('<td>'+escape(str(v))+'</td>' for v in values)+'</tr>')
    qualification_html.append('</table><h3>Every planned control</h3><table><tr><th>Call / trace</th><th>Truth</th><th>Submission</th><th>Committed</th><th>Valid</th><th>Correct</th><th>Error</th><th>Tokens</th><th>Seconds</th></tr>')
    for r in result['qualification_controls']:
        label=escape(r['call'])
        if r['recorded']:
            label='<a href="conversations.html#'+escape(quote(r['call'],safe='/'),quote=True)+'">'+label+'</a>'
        qualification_html.append('<tr><td>'+label+'</td>'+''.join('<td>'+escape(str(r[k]) if r[k] is not None else 'unknown')+'</td>' for k in ('truth','submission','committed','valid','correct','error','generated_tokens','ready_seconds'))+'</tr>')
    qualification_html.append('</table><p><a href="qualification_controls.csv">Download qualification controls</a></p>')
    html.insert(-1, '\n'.join(diagnostics_html+qualification_html))
    for w in result["worlds"]:
        html.append('<tr>'+''.join('<td>'+escape(str(w[k]) if w[k] is not None else 'unknown')+'</td>' for k in ("id","group","original_truth","revised_truth","prefix","retain","clear"))+'</tr>')
    html.append('</table><h2>Paired results and costs</h2><p><a href="paired-results.csv">Paired outcomes</a> · <a href="paired_costs.csv">Paired costs</a> · <a href="attempts.csv">Local attempt ledger</a> · <a href="prior_spending.csv">Prior-study spending/proof</a> · <a href="failure_analysis.csv">Observable failure audit</a> · <a href="analysis.json">Complete reconstruction</a></p>')
    if plot:
        html.extend(f'<h3>{name}</h3><img src="figures/{name}.svg" alt="{name}">' for name in ('qualification-outcomes','qualification-effort',"paired-outcomes","recovery-ready_seconds","recovery-calls","recovery-generated_tokens","failure-labels","termination-coverage"))
    html.append('<h2>Interpretation, gates and limitations</h2><pre>'+escape(narrative)+'</pre>')
    (out/"overview.html").write_text('\n'.join(html),encoding="utf-8")
    if plot:
        figures(result, out/"figures")
    return dict(directory=str(out), summary=s, files=[p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()])


def validation_errors(result):
    return [row for row in result['validation_details'] if row['recorded'] and not row['legal_action']]
