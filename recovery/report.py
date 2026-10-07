"""Derived offline report and frozen §7.4 cases; never imported by execution.

Original schedules, workers and checkpoints remain authoritative. Case cards
illustrate recorded behavior; selection never changes analysis populations.
"""

from collections import defaultdict
from dataclasses import asdict
from fractions import Fraction
import csv
import gzip
from html import escape
import json
from pathlib import Path
from urllib.parse import quote


LABEL = "Synthetic CPU validation; not model capability or empirical findings"
CASE_CONTRASTS = (
    ("C-B", "revision", "auc", None),
    ("E_keep", "revision", "collaborator_accuracy", None),
    ("K_delta-K", "revision", "accuracy", 1),
)
CASE_RULE = {
    "contrasts": [list(key) for key in CASE_CONTRASTS],
    "replicate": 0,
    "complete_world": "Every scheduled outcome in the supplied world scope is recorded, including failures, controls and scheduled repeats.",
    "selection": "Within each strict sign sort by exact rational effect then immutable world ID; take index (n-1)//2, the lower observed median.",
    "duplicates": "Merge worlds, retaining every selecting contrast and sign; at most six cards.",
    "fallback": "Only if every eligible observed contrast is zero: smallest-ID regression world, else smallest-ID complete world. No eligible complete world means unavailable.",
    "excerpts": "For each selecting contrast use the earliest differing paired focal peer/round; ties use the edited owner at the first endpoint round. Include its actual prefix round-four reply, component replies and incoming prose first usable at that boundary, without alteration. A zero-effect regression fallback also shows the smallest-ID regressing continuation and its earliest regressing peer/round.",
    "interpretation": "Cases illustrate behavior; full nonexclusive annotations establish prevalence. Prose and delivery paths do not establish semantic causation.",
}


def _case_key(row):
    return tuple(row[k] for k in ("estimand", "event", "endpoint", "round"))


def _fraction(row):
    value = row["exact"]
    return Fraction(value["numerator"], value["denominator"])


def select_cases(contrasts, outcomes, trajectories):
    """Exact sign medians on complete worlds, independently of report rendering."""
    by_world = defaultdict(list)
    for row in outcomes:
        by_world[row["world_id"]].append(row)
    complete = {wid for wid, rows in by_world.items() if all(r["correct"] is not None for r in rows)}
    eligible = defaultdict(list)
    seen = set()
    for row in contrasts:
        key = _case_key(row)
        if row["replicate"] != 0 or key not in CASE_CONTRASTS:
            continue
        identity = (key, row["world_id"])
        if identity in seen:
            raise ValueError("duplicate case-selection world contrast")
        seen.add(identity)
        if row["world_id"] in complete and row["exact"] is not None and row["eligibility"] == "eligible":
            eligible[key].append(row)
    signs, chosen = [], defaultdict(list)
    for key in CASE_CONTRASTS:
        for sign, positive in (("positive", True), ("negative", False)):
            rows = sorted((r for r in eligible[key] if (_fraction(r) > 0 if positive else _fraction(r) < 0)),
                          key=lambda r: (_fraction(r), r["world_id"]))
            row = rows[(len(rows)-1)//2] if rows else None
            category = dict(contrast=list(key), sign=sign, eligible_complete_worlds=len(eligible[key]),
                sign_worlds=len(rows), selected_world_id=row["world_id"] if row else None,
                status="selected" if row else "sign_absent")
            signs.append(category)
            if row:
                chosen[row["world_id"]].append(dict(contrast=list(key), sign=sign, exact=row["exact"], value=row["value"]))
    available = {r["world_id"] for rows in eligible.values() for r in rows}
    all_zero = bool(available) and all(_fraction(r) == 0 for rows in eligible.values() for r in rows)
    fallback = None
    if all_zero:
        regressions = {r["world_id"] for r in trajectories if r["world_id"] in available
            and r["phase"] == "continuation" and r["replicate"] == 0 and r["regression"] is True}
        wid = min(regressions or available)
        fallback = dict(world_id=wid, reason="all_zero_regression" if regressions else "all_zero_smallest_complete")
        chosen[wid].append(dict(contrast=None, sign="all_zero", reason=fallback["reason"]))
    return dict(rule=CASE_RULE, status="available" if chosen else "unavailable",
        reason=None if chosen else "no_eligible_complete_world", complete_world_ids=sorted(complete),
        eligible_complete_world_ids=sorted(available), signs=signs, all_zero=all_zero, fallback=fallback,
        selected=[dict(world_id=wid, reasons=chosen[wid]) for wid in sorted(chosen)])


def trace_records(tables, records, inputs):
    """Unaltered rendered/raw text with original logical/physical/message IDs."""
    calls = []
    for outcome in tables["outcomes"]:
        logical = records.get(outcome["call_id"])
        original = records.get(outcome["generation_id"]) if logical else None
        raw = json.loads(original["raw_json"]) if original and original.get("raw_json") else None
        saved = inputs.get((outcome["branch_id"], outcome["round"]))
        request = None
        if saved:
            peer = outcome["peer"]
            rendered = saved["requests"]["rendered"]
            request = (rendered if peer is None else rendered[peer])["content"]
        calls.append({k: outcome[k] for k in ("call_id", "generation_id", "replay_parent", "world_id",
            "branch_id", "peer", "round", "protocol_outcome", "worker_file")} |
            dict(request_text=request, raw_reply=raw, failure=json.loads(original["failure_json"])
                if original and original.get("failure_json") else None))
    by_call = {r["call_id"]: r for r in calls}
    deliveries = []
    for row in tables["costs"]["validated_deliveries"]:
        if row["text"] is not None:
            call_id = row["message_id"].rsplit("/to", 1)[0]
            if call_id not in by_call:
                raise ValueError("prose delivery lacks its original scheduled sender call")
            row = dict(row, call_id=call_id, branch_id=by_call[call_id]["branch_id"])
        deliveries.append(row)
    return dict(kind=LABEL, calls=calls, deliveries=deliveries)


def case_cards(worlds, tables, traces, selection):
    """Link fixed cards to actual replies, deliveries and diagnostic denominators."""
    by_world = {w.world_id: w for w in worlds}
    by_call = {r["call_id"]: r for r in tables["outcomes"]}
    trace = {r["call_id"]: r for r in traces["calls"]}
    contrasts = {(r["world_id"], _case_key(r)): r for r in tables["estimands"]["world_contrasts"]
                 if r["replicate"] == 0}
    result = []
    for chosen in selection["selected"]:
        wid, reasons = chosen["world_id"], chosen["reasons"]
        prepared = by_world[wid]
        owner = next(r.owner for r in prepared.world.records if r.record_id == prepared.main_edit.record_id)
        keys = [tuple(r["contrast"]) for r in reasons if r["contrast"] is not None]
        if not keys:
            keys = [key for key in CASE_CONTRASTS if (wid, key) in contrasts
                    and contrasts[wid, key]["exact"] is not None]
        bids, excerpts, excerpt_boundaries = set(), set(), set()
        for key in keys:
            contrast = contrasts[wid, key]
            components = contrast["components"]
            bids.update(c["branch_id"] for c in components)
            rounds = sorted({a["round"] for c in components for a in c["atoms"]})
            # Compare within focal peers: E_keep holds each focal group's state
            # fixed; its two terms can cancel without erasing either subgroup.
            differences = []
            for number in rounds:
                for peer in range(4):
                    values = [a["correct"] for c in components for a in c["atoms"]
                              if a["round"] == number and a["peer"] == peer]
                    if values and len(set(values)) > 1:
                        differences.append((number, peer))
            number, peer = min(differences) if differences else (min(rounds), owner)
            for component in components:
                row = next((a for a in component["atoms"] if a["round"] == number and a["peer"] == peer), None)
                if row:
                    excerpts.add(row["call_id"])
                    excerpt_boundaries.add((component["branch_id"], number, peer))
                    prefix = by_call[row["call_id"]]["prefix_call_id"]
                    if prefix:
                        excerpts.add(prefix)
        if any(r.get("reason") == "all_zero_regression" for r in reasons):
            regressed = min((r for r in tables["trajectories"] if r["world_id"] == wid
                and r["phase"] == "continuation" and r["replicate"] == 0 and r["regression"] is True), key=lambda r: r["branch_id"])
            bid = regressed["branch_id"]
            bids.add(bid)
            rows = [r for r in tables["outcomes"] if r["branch_id"] == bid]
            row = min((r for r in rows if r["correct"] == 0 and any(p["peer"] == r["peer"]
                and p["round"] < r["round"] and p["correct"] == 1 for p in rows)), key=lambda r: (r["round"], r["peer"]))
            excerpts.update((row["call_id"], row["prefix_call_id"]))
            excerpt_boundaries.add((bid, row["round"], row["peer"]))
        incoming = [d for d in traces["deliveries"] if d["text"] is not None and d["first_usable"] is not None
            and d["first_usable"]["phase"] == "recovery"
            and (d["branch_id"], d["first_usable"]["round_number"], d["recipient"]) in excerpt_boundaries]
        result.append(dict(world_id=wid, family=prepared.world.task.value, size=prepared.world.size.value,
            reasons=reasons, edit=dict(chosen=asdict(prepared.main_edit),
                before=asdict(next(r for r in prepared.world.records if r.record_id == prepared.main_edit.record_id)),
                after=asdict(next(r for r in prepared.event_world("revision").records if r.record_id == prepared.main_edit.record_id))),
            partition=[list(g) for g in prepared.partition],
            trajectories=[r for r in tables["trajectories"] if r["branch_id"] in bids],
            availability=[{k: r[k] for k in ("call_id", "branch_id", "round", "peer", "correct",
                "v2_available", "v2_reason", "v2_delivery_ids")} for r in tables["outcomes"] if r["branch_id"] in bids],
            preservation=[r for r in tables["diagnostic_summaries"] if r["branch_id"] in bids
                          and r["level"] == "world" and r["metric"] in ("preservation", "collateral_damage")],
            excerpts=[trace[cid] for cid in sorted(excerpts)], incoming_prose=incoming,
            interpretation=CASE_RULE["interpretation"]))
    return result


INTERPRETATIONS = (
    "Equal revision and sham reset effects indicate generic cleanup; theta alone does not establish a practical reset benefit.",
    "Subgroup effects can cancel in phi; a shared revision/sham collaborator effect remains operational even when phi_corr is zero.",
    "Receipts may benefit every representation equally with eta zero; positive eta can also reflect harm to evidence-only reset.",
    "Prose delay can lose useful coordination time; inactive Q treatments stay included and delivery paths do not establish semantic causation.",
    "Ceiling quality can coexist with cost or temporary damage; common failure with poor full-information controls is capability-limited.",
    "Broad intervals or unstable conditional repeats support an inconclusive account, not equivalence or a universal policy recommendation.",
    "Evidence inventory, preserved correct output and measured computation are separate: retained records may be unused and unchanged output may be recomputed.",
    "Prompt length and scripted CPU attempt durations do not establish GPU runtime penalties. Policy computation, actual allocation and provider billing remain separate.",
    "Failures score zero; unexecuted calls stay unknown. Complete-case descriptions and missingness sensitivity never replace the frozen population.",
    "Four rounds define observed stability. No fifth failure round, successful-only time average, best-answer splicing or early-stop saving is used.",
    "These five fixed families, four synchronous peers, one announced edit and one future accepted model do not establish generality to other tasks, teams or models.",
)
PRIOR_WORK = (
    ("SILO-BENCH", "https://aclanthology.org/2026.acl-long.1354/", "Task mathematics; modified sizes, lifecycle, rendering and source dynamics."),
    ("CIR", "https://arxiv.org/html/2610.00372v1", "Matched recovery and rescue versus harm."),
    ("ICR", "https://arxiv.org/html/2610.01042v1", "Correction/preservation with independent solutions; this design instead follows private-information collaboration."),
    ("StateAuditor", "https://arxiv.org/html/2608.01619v1", "Previous/current transitions in repair."),
    ("DBSP", "https://arxiv.org/abs/2203.16684", "Incremental computation foundation."),
    ("REVISE", "https://arxiv.org/html/2609.00643v1", "Structured dependency recovery; no correct semantic dependency graph is assumed here."),
)


def _interval_row(row):
    intended, cc = row["intended_population"], row["complete_case_description"]
    return {k: row[k] for k in ("population", "estimand", "event", "endpoint", "round", "family",
        "eligible_worlds", "observed_worlds", "unknown_worlds", "family_denominators", "world_ids", "range")} | dict(
        estimate=intended["estimate"], interval=intended["interval"], primary=row["primary_interval"],
        probabilities=intended["probabilities"], hoeffding=intended["hoeffding"],
        complete_case_estimate=cc["estimate"], complete_case_interval=cc["interval"],
        complete_case_hoeffding=cc["hoeffding"], sensitivity=row["sensitivity"], paired_coverage=row["paired_coverage"])


def _prefix_summary(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["family"], row["round"]].append(row)
    result = []
    for (family, number), group in sorted(grouped.items()):
        worlds = sorted({r["world_id"] for r in group})
        values = [r["old_gold_correct"] for r in group]
        inventories = [r["inventory"] for r in group]
        tokens = [r["history_content_tokens"] for r in group]
        result.append(dict(family=family, round=number, world_ids=worlds, scheduled_worlds=len(worlds),
            scheduled_peers=len(group), recorded_peers=sum(v is not None for v in values),
            old_gold_correctness=sum(values)/len(values) if None not in values else None,
            remote_record_coverage=sum(i["remote_coverage"] for i in inventories)/len(group)
                if all(i is not None and i["remote_coverage"] is not None for i in inventories) else None,
            history_content_tokens=sum(tokens)/len(tokens) if None not in tokens else None,
            history_unknown_peers=sum(v is None for v in tokens)))
    return result


def _quality_plot_rows(rows):
    result = []
    def bounds(value):
        pair = [value["lower"]["estimate"], value["upper"]["estimate"]]
        return pair if None not in pair else None
    for row in rows:
        if (row["level"] != "all_families" or row["population"] != "main" or row["event"] != "revision"
                or row["metric"] not in ("auc", "final_preservation")
                or not (row["display"].startswith("policy_") or row["display"] == "boundary_rule")):
            continue
        cost = row["paired_cost"]
        result.append({k: row[k] for k in ("display", "metric", "eligible_worlds", "paired_observed_worlds", "unknown_worlds", "family_denominators", "world_ids")} | dict(
            estimate=bounds(row["intended_population"]), interval=row["intended_population"]["interval"],
            cost_estimate=bounds(cost["intended_population"]), cost_interval=cost["intended_population"]["interval"],
            complete_case_estimate=bounds(row["complete_case_description"]),
            complete_case_interval=row["complete_case_description"]["interval"],
            complete_case_cost_estimate=bounds(cost["complete_case_description"]),
            complete_case_cost_interval=cost["complete_case_description"]["interval"], sensitivity=row["sensitivity"],
            cost_axis="Original prefix plus all 16 logical continuation calls; same eligible/observed worlds and draws as this endpoint."))
    return result


def assemble_report(worlds, branches, tables, traces, *, provenance=None):
    """Seven explicit grouped exhibits, retaining all supporting M4 tables."""
    from .evaluate import ANNOTATIONS
    worlds, branches = tuple(worlds), tuple(branches)
    uncertainty, information, estimands, costs = (tables[k] for k in ("uncertainty", "information", "estimands", "costs"))
    pooled = [_interval_row(r) for r in uncertainty["summaries"] if r["level"] == "all_families"]
    effects = [r for r in pooled if r["population"] == "main" and r["round"] is None and (
        r["estimand"] == "theta" and r["endpoint"] == "auc" or
        r["estimand"] == "E_keep" and r["event"] == "revision" and r["endpoint"] == "collaborator_accuracy" or
        r["estimand"] in ("C-B", "K-C", "K-B", "B-L", "C-F") and r["event"] == "revision" and r["endpoint"] in ("auc", "final_joint"))]
    repair = [r for r in tables["diagnostic_summaries"] if r["level"] == "all_families"
              and r["replicate"] == 0 and r["event"] == "revision"]
    receipts = [r for r in pooled if r["population"] == "receipts" and r["endpoint"] == "accuracy" and r["round"] == 1]
    collaborators = [r for r in pooled if r["population"] == "main" and r["endpoint"] in ("accuracy", "collaborator_accuracy")
                    and (r["estimand"] in ("E_keep", "E_clear", "phi_corr", "own_reset_other_retained", "own_reset_other_cleared") or r["estimand"].startswith(("M_G_", "M_H_")))]
    prose = [r for r in pooled if r["population"] == "prose_delay" and r["endpoint"] == "accuracy"]
    context = _prefix_summary(information["prefix"])
    controls = [r for r in tables["outcomes"] if r["phase"] == "control"]
    selection = select_cases(estimands["world_contrasts"], tables["outcomes"], tables["trajectories"])
    cards = case_cards(worlds, tables, traces, selection)
    plots = dict(context=context, controls=controls, effects=effects, repair=repair, receipts=receipts,
        collaborators=collaborators, prose=prose, synchronization=uncertainty["family_completion"],
        quality_cost=_quality_plot_rows(uncertainty["policy_display_summaries"]),
        world_effects=[{k: r[k] for k in ("world_id", "family", "estimand", "event", "endpoint", "value", "exact")}
            for r in estimands["world_contrasts"] if r["primary"]],
        family_effects=[_interval_row(r) for r in uncertainty["summaries"] if r["level"] == "family"
            and (r["estimand"] == "theta" and r["endpoint"] == "auc" or r["estimand"] == "E_keep"
                 and r["event"] == "revision" and r["endpoint"] == "collaborator_accuracy")])
    exhibits = [
        dict(id="context", title="Prior work and task information", rows=len(context),
            supports=["information.prefix", "information.owner_exposure", "information.atlas", "outcomes"],
            note="Four prefix rounds include unsuccessful worlds. Full-information original/revised controls are shown separately; rendered exposure does not prove model use."),
        dict(id="effects", title="Recovery policy effects", rows=len(effects),
            supports=["estimands.world_contrasts", "estimands.summaries", "uncertainty.summaries", "uncertainty.world_bounds"],
            note="Theta is correction-specific; phi is the direct revised-world effect on retained collaborators. Filled markers show population intervals; hollow markers show complete cases. Dashed bounded-mean companions use that displayed cohort; sensitivity is separate from confidence. All prespecified AUC/final companions remain in the supporting tables."),
        dict(id="repair", title="Repair and preservation", rows=len(repair),
            supports=["coordinates", "peer_diagnostics", "diagnostic_summaries", "annotations", "annotation_counts"],
            note="Changed-coordinate repair, old-value persistence, preservation of previously correct U, collateral damage and repair of old U errors have distinct eligibility and denominators. Labels overlap."),
        dict(id="receipts", title="Representation and historical receipts", rows=len(receipts),
            supports=["information.receipt_information", "information.receipt_strata", "information.transport_references", "information.boundary_acquisition", "estimands.world_contrasts"],
            note="All six first-response cells and direct receipt effects accompany eta. Four-round/preservation companions, correctness assumptions and unresolved source associations remain explicit."),
        dict(id="collaborators", title="Effects on collaborators", rows=len(collaborators),
            supports=["estimands.world_contrasts", "uncertainty.summaries", "rounds"],
            note="Both subgroups and all four masks are retained. Round one is an exact-replay construction reference; the primary uses rounds 2–4. Cancellation does not show absence of subgroup effects."),
        dict(id="prose", title="Prose timing and synchronized completion", rows=len(prose),
            supports=["estimands.prose_activity", "information.receipt_timing", "information.receipt_timing_counts", "trajectories", "uncertainty.family_completion", "uncertainty.trajectory_summaries"],
            note="Q retains inactive and unobserved treatments. Sources are fixed through the round-two boundary; later differences are total scheduling effects. Fragmentation never becomes a spliced team answer."),
        dict(id="quality_cost", title="Quality, cost, repeatability and limits", rows=len(plots["quality_cost"]),
            supports=["costs.physical", "costs.resources", "costs.policy_costs", "costs.selection_frequencies", "uncertainty.policy_world_displays", "uncertainty.policy_display_summaries", "estimands.repeatability", "estimands.trajectory_changes"],
            note="Policy cost includes the abandoned/shared prefix and every continuation use. Paired quality and preservation use their own cost cohorts; allocation and billing are separate. Repeats are conditional on the original prefix."),
    ]
    return dict(kind=LABEL, coverage=tables["coverage"], provenance=provenance or {},
        scope=dict(size=worlds[0].world.size.value, world_ids=sorted(w.world_id for w in worlds),
            scheduled_worlds=len(worlds), scheduled_branches=len(branches),
            domain="development" if worlds[0].development else "supplied main manifest",
            populations=estimands["populations"]),
        settings=dict(uncertainty=uncertainty["settings"], accounting_as_of=costs["at"], case_rule=CASE_RULE,
            annotation_labels=list(ANNOTATIONS), annotation_interpretation="Six nonexclusive observable labels, with intersections and unknown/not-applicable counts.",
            source_association="Only the genuine receipt or exact edited-ID/v1=integer syntax with original spans/IDs qualifies. Numeric coincidence and unmatched wording remain unresolved; derived assertions remain untrusted.",
            source_association_rubric="docs/implementation-research/information-diagnostics.md",
            references="Specified-view CPU sufficiency/ambiguity; correct-summary assumptions never certify actual candidates; actual-candidate transport preserves residual errors."),
        prior_work=[dict(name=n, url=u, role=r, attribution="Context attributed by PROJECT_SPECIFICATION.md §10; verify precise versions before publication.") for n, u, r in PRIOR_WORK],
        interpretations=list(INTERPRETATIONS), reporting_references=uncertainty["reporting_references"],
        selection=selection, cases=cards, exhibits=exhibits, plotting_data=plots,
        boundary_rule=costs["selection_frequencies"], repeatability=estimands["repeatability"],
        trajectory_changes=estimands["trajectory_changes"], prose_activity=estimands["prose_activity"],
        history_tokenizer=information["history_tokenizer"],
        cpu_gate="A report is derived evidence, not a gate decision. The named repository M1–M4 audit must pass; M5 hardware/capability/resource gates and execution authorization remain separate.")


def report_run(worlds, branches, paths, *, now, seed=20261006, tokenizer=None, provenance=None):
    """One read-only worker snapshot feeds every table and unaltered excerpt."""
    from .analysis import analyze_estimands, prose_activity
    from .costs import cost_records, timestamp
    from .evaluate import evaluate_records, read_records
    from .information import information_records
    from .uncertainty import uncertainty_records
    # An explicit clock is necessary for reproducible uncertain attempt costs.
    if now is None:
        raise ValueError("report requires an explicit zoned accounting --as-of")
    timestamp(now)
    if type(seed) is not int or seed < 0:
        raise ValueError("resampling seed must be a nonnegative integer")
    worlds, branches = tuple(worlds), tuple(branches)
    records, inputs, attempts, committed, resources = read_records(worlds, branches, paths,
        include_committed=True, include_resources=True)
    tables = evaluate_records(worlds, branches, records, inputs, attempts)
    tables["costs"] = cost_records(worlds, branches, records, inputs, attempts, committed=committed,
        allocations=resources["allocations"], processes=resources["processes"], budgets=resources["budgets"], now=now, tables=tables)
    tables["information"] = information_records(worlds, branches, records, inputs, attempts,
        committed=committed, tokenizer=tokenizer, tables=tables)
    tables["estimands"] = analyze_estimands(worlds, branches, tables)
    tables["estimands"]["prose_activity"] = prose_activity(worlds, branches, inputs)
    tables["uncertainty"] = uncertainty_records(worlds, branches, tables, seed=seed)
    traces = trace_records(tables, records, inputs)
    report = assemble_report(worlds, branches, tables, traces, provenance=provenance)
    report["settings"]["generation_settings"] = sorted({r["settings_json"] for r in inputs.values()})
    return dict(tables=tables, report=report, traces=traces,
        inputs=dict(worlds=[asdict(w) for w in worlds], branches=[asdict(b) for b in branches]))


def _dump(path, value):
    # Stable compressed bytes as well as stable tables: omit gzip filename/time.
    data = (json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(",", ":"))+"\n").encode("utf-8")
    with path.open("xb") as target:
        if path.suffix == ".gz":
            with gzip.GzipFile(filename="", mode="wb", fileobj=target, mtime=0) as compressed:
                compressed.write(data)
        else:
            target.write(data)


def _table(rows, fields):
    def cell(value):
        if value is None:
            return "N/A"
        if isinstance(value, (dict, list)):
            return escape(json.dumps(value, sort_keys=True, ensure_ascii=True))
        return escape(str(value))
    return "<div class='scroll'><table><thead><tr>"+"".join("<th>"+escape(f)+"</th>" for f in fields)+"</tr></thead><tbody>"+"".join(
        "<tr>"+"".join("<td>"+cell(r.get(f))+"</td>" for f in fields)+"</tr>" for r in rows)+"</tbody></table></div>"


def _page(title, body):
    return "<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"+f"<title>{escape(title)}</title>"+"""<style>
body{max-width:1160px;margin:40px auto;padding:0 24px;color:#182a39;background:#fff;font:16px/1.6 system-ui,sans-serif}
h1,h2,h3{line-height:1.2}h2{margin-top:48px}a{color:#165e86}aside{padding:12px 18px;background:#edf3f7;border-left:4px solid #165e86}
img{width:100%;height:auto}.scroll{overflow:auto}table{border-collapse:collapse;font-size:13px;width:100%;margin:18px 0}th,td{border-bottom:1px solid #ccd5dd;padding:8px;text-align:left;vertical-align:top}th{background:#edf3f7}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f8;padding:16px;font-size:12px}code{overflow-wrap:anywhere}details{margin:16px 0}nav a{margin-right:16px}.muted{color:#546575}
</style>"""+"<body><h1>"+escape(title)+"</h1><aside>"+escape(LABEL)+"</aside>"+body+"</body></html>\n"


def _literal_html(text):
    # JSON string notation is reversible even for invalid Unicode. Never repair
    # the original raw reply or its protocol outcome to make a page encodable.
    if any(0xD800 <= ord(char) <= 0xDFFF for char in text):
        return "<p class='muted'>Non-scalar Unicode: this exact JSON string literal preserves the original text. The trace export retains the unaltered string.</p><pre>"+escape(json.dumps(text, ensure_ascii=True))+"</pre>"
    return "<pre>"+escape(text)+"</pre>"


def _cases_html(report):
    body = "<p><a href='report.html'>Report</a> · <a href='traces.json.gz'>Unaltered trace export</a></p>"
    body += "<p>"+escape(CASE_RULE["selection"]+" "+CASE_RULE["complete_world"])+"</p>"
    body += _table(report["selection"]["signs"], ("contrast", "sign", "eligible_complete_worlds", "sign_worlds", "selected_world_id", "status"))
    if not report["cases"]:
        body += "<p>Cases unavailable: no eligible complete world.</p>"
    for card in report["cases"]:
        body += "<h2 id='"+escape(card["world_id"], quote=True)+"'>"+escape(card["world_id"])+"</h2>"
        body += "<p>"+escape(card["interpretation"])+"</p>"+_table([card], ("family", "reasons", "edit", "partition"))
        body += _table(card["trajectories"], ("policy", "event", "mean_peer_correctness", "joint", "category", "first_joint_round", "first_stable_joint_round", "regression", "fragmented"))
        body += "<details><summary>All selected-branch availability and preservation denominators</summary>"+_table(card["availability"], ("call_id", "correct", "v2_available", "v2_reason", "v2_delivery_ids"))
        body += _table(card["preservation"], ("policy", "round", "metric", "rate", "denominator", "unique_coordinate_count", "peer_copy_count", "reason"))+"</details>"
        for row in card["excerpts"]:
            body += "<h3><a href='calls.html#"+quote(row["call_id"], safe="")+"'>"+escape(row["call_id"])+"</a></h3>"
            body += "<p>Original generation: <code>"+escape(row["generation_id"])+"</code>; "+escape(row["protocol_outcome"])+".</p>"
            body += _literal_html(row["raw_reply"]["text"] if row["raw_reply"] else "No recorded raw reply; see the linked failure/unknown trace.")
        for row in card["incoming_prose"]:
            body += "<p>Incoming message <a href='calls.html#"+quote(row["message_id"], safe="")+"'>"+escape(row["message_id"])+"</a>; delivery <code>"+escape(row["delivery_id"])+"</code>.</p>"+_literal_html(row["text"])
    return _page("Matched case cards", body)


def _calls_html(traces):
    body = "<p><a href='report.html'>Report</a> · <a href='cases.html'>Cases</a> · <a href='traces.json.gz'>Exact strings, generated tokens and delivery metadata</a></p>"
    for row in traces["calls"]:
        body += "<details id='"+escape(row["call_id"], quote=True)+"'><summary>"+escape(row["call_id"])+" — "+escape(row["protocol_outcome"])+"</summary>"
        body += _table([row], ("generation_id", "replay_parent", "worker_file", "failure"))
        body += "<h3>Rendered request</h3>"+_literal_html(row["request_text"] if row["request_text"] is not None else "Unavailable")+"<h3>Literal raw reply</h3>"
        body += _literal_html(row["raw_reply"]["text"] if row["raw_reply"] else "Unavailable")+"</details>"
    seen_messages = set()
    for row in traces["deliveries"]:
        if row["text"] is not None:
            # Replay can give one original message several branch-local deliveries.
            message_anchor = " id='"+escape(row["message_id"], quote=True)+"'" if row["message_id"] not in seen_messages else ""
            seen_messages.add(row["message_id"])
            body += "<details id='"+escape(row["delivery_id"], quote=True)+"'><summary"+message_anchor+">"+escape(row["message_id"])+"</summary>"
            body += _table([row], ("branch_id", "delivery_id", "first_usable", "recipient"))+_literal_html(row["text"])+"</details>"
    return _page("Original call and message traces", body)


def _report_html(report, figures):
    body = "<p>"+escape(report["cpu_gate"])+"</p><nav><a href='cases.html'>Matched cases</a><a href='tables.json.gz'>All scientific tables</a><a href='world_contrasts.csv'>World contrasts</a><a href='intervals.csv'>Family and pooled intervals</a><a href='plotting.json'>Deterministic plotting inputs</a><a href='inputs.json.gz'>Original input selection</a><a href='report.json'>Settings and provenance</a></nav>"
    body += "<h2>Coverage and interpretation</h2>"+_table([report["coverage"]], ("scheduled", "recorded", "unknown", "protocol_outcomes"))
    body += "<p>"+escape(report["history_tokenizer"])+". N/A is unavailable or structurally inapplicable, with the reason and denominator retained in the scientific tables.</p>"
    body += "<p>"+escape(report["settings"]["uncertainty"]["cluster"])+"</p>"
    for exhibit in report["exhibits"]:
        eid = exhibit["id"]
        body += "<h2 id='"+eid+"'>"+escape(exhibit["title"])+"</h2><p>"+escape(exhibit["note"])+"</p>"
        if figures:
            body += "<img src='figures/"+eid+".svg' alt='"+escape(exhibit["title"], quote=True)+"'>"
        else:
            body += "<p class='muted'>Figure inputs are in plotting.json. Render with <code>python -m recovery.figures --report THIS_DIRECTORY</code>.</p>"
        body += "<p>Supporting paths in <a href='tables.json.gz'>tables.json.gz</a>: "+", ".join("<code>"+escape(p)+"</code>" for p in exhibit["supports"])+".</p>"
        if eid == "context":
            body += _table(report["prior_work"], ("name", "role", "attribution"))
            body += "<p>"+" · ".join("<a href='"+escape(r["url"], quote=True)+"'>"+escape(r["name"])+"</a>" for r in report["prior_work"])+"</p>"
            body += _table(report["plotting_data"]["controls"], ("world_id", "event", "correct", "protocol_outcome", "call_id"))
        elif eid == "effects":
            body += _table(report["plotting_data"][eid], ("estimand", "event", "endpoint", "estimate", "interval", "hoeffding", "observed_worlds", "eligible_worlds", "family_denominators", "sensitivity"))
            body += "<details><summary>Raw primary world contrasts and descriptive family intervals</summary>"
            body += _table(report["plotting_data"]["world_effects"], ("world_id", "family", "estimand", "value", "exact"))
            body += _table(report["plotting_data"]["family_effects"], ("family", "estimand", "estimate", "interval", "observed_worlds", "eligible_worlds", "hoeffding"))+"</details>"
        elif eid == "prose":
            body += _table(report["prose_activity"], ("world_id", "event", "policy", "observed", "active", "nonempty_texts", "reason"))
        elif eid == "quality_cost":
            body += "<h3>Frozen source-coverage rule</h3>"+_table(report["boundary_rule"], ("level", "family", "event", "replicate", "counts", "unknown_selections", "frequency_denominator", "constant_policy", "statement"))
            body += "<details><summary>Conditional repeats and trajectory changes</summary>"+_table(report["repeatability"], ("world_id", "estimand", "event", "endpoint", "classification", "replicate_zero", "replicate_one"))
            body += _table(report["trajectory_changes"], ("world_id", "event", "policy", "replicate_zero_category", "replicate_one_category", "complete_pair"))+"</details>"
    body += "<h2>Limitations and unfavorable-outcome interpretation</h2><ul>"+"".join("<li>"+escape(s)+"</li>" for s in report["interpretations"])+"</ul>"
    body += "<p>Case status: "+escape(report["selection"]["status"])+"; selected IDs: "+escape(", ".join(r["world_id"] for r in report["cases"]) or "none")+". Absent signs are reported on the <a href='cases.html'>case-selection page</a>.</p>"
    return _page("Recovery report — synthetic validation", body)


def write_report(directory, result, *, figures=False):
    """Exclusively create a portable derived report; never replace existing work."""
    directory = Path(directory)
    if directory.exists():
        raise FileExistsError(f"report output already exists: {directory}")
    # Check the optional renderer before creating any output.
    if figures:
        from .figures import render_figures
        import matplotlib  # noqa: F401
    directory.mkdir()
    report, tables = result["report"], result["tables"]
    for name, value in (("report.json", report), ("plotting.json", report["plotting_data"]),
                        ("tables.json.gz", tables), ("traces.json.gz", result["traces"]), ("inputs.json.gz", result["inputs"])):
        _dump(directory/name, value)
    for name, rows, fields in (
        ("world_contrasts.csv", tables["estimands"]["world_contrasts"],
         ("world_id", "family", "population", "estimand", "event", "endpoint", "round", "replicate", "value", "exact", "eligibility", "reason")),
        ("intervals.csv", tables["uncertainty"]["summaries"],
         ("population", "estimand", "event", "endpoint", "round", "level", "family", "eligible_worlds", "observed_worlds", "unknown_worlds", "family_denominators", "intended_population", "complete_case_description", "sensitivity"))):
        with (directory/name).open("x", encoding="utf-8", newline="") as target:
            writer = csv.DictWriter(target, fields, lineterminator="\n")
            writer.writeheader()
            for row in rows:
                writer.writerow({k: json.dumps(row[k], sort_keys=True, ensure_ascii=True) if isinstance(row[k], (dict, list)) else row[k] for k in fields})
    for name, body in (("report.html", _report_html(report, figures)), ("cases.html", _cases_html(report)), ("calls.html", _calls_html(result["traces"]))):
        (directory/name).write_text(body, encoding="utf-8", newline="\n")
    if figures:
        render_figures(directory)
    return directory
