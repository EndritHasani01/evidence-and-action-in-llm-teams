"""Estimands, uncertainty, diagnostics and reports from the canonical store only.

Specification sections 3.9-3.11. Every number is recomputed from the run's
SQLite store and its saved inputs; nothing is taken from progress output.
Estimates are withheld until main is complete for a model or the campaign is
explicitly declared stopped (no interim analysis).
"""

from contextlib import closing
import csv
import json
import math
from pathlib import Path
from random import Random
import sqlite3

from . import CELLS, MODELS
from . import protocol

LINEAR = {
    # name: (coefficients over cells, label)
    "delta_E": ({"RN": .5, "RV": -.5, "CN": .5, "CV": -.5}, "revision cost: success(no change) - success(revision), mean over retain/clear"),
    "delta_H": ({"CV": 1, "RV": -1}, "history effect after revision: clear - retain"),
    "theta": ({"CV": 1, "RV": -1, "CN": -1, "RN": 1}, "interaction: (CV-RV) - (CN-RN)"),
    "delta_E_retain": ({"RN": 1, "RV": -1}, "revision cost under retain"),
    "delta_E_clear": ({"CN": 1, "CV": -1}, "revision cost under clear"),
    "delta_H_no_change": ({"CN": 1, "RN": -1}, "history effect under no change: CN - RN"),
    "rate_prefix": ({"prefix": 1}, "original-phase success"),
    "rate_RV": ({"RV": 1}, "success retain/revision"),
    "rate_CV": ({"CV": 1}, "success clear/revision"),
    "rate_RN": ({"RN": 1}, "success retain/no change"),
    "rate_CN": ({"CN": 1}, "success clear/no change"),
}
PRIMARY = ("delta_E", "delta_H")


def interval_indices(draws, confidence):
    alpha = 1 - confidence
    return math.floor(draws * alpha / 2), math.ceil(draws * (1 - alpha / 2)) - 1


def value_range(coefficients):
    return (sum(min(0, c) for c in coefficients.values()), sum(max(0, c) for c in coefficients.values()))


def world_value(coefficients, ys, fill=None):
    """Linear world contrast; fill='min'|'max' bounds unknown outcomes by coefficient sign."""
    total = 0.0
    for cell, c in coefficients.items():
        y = ys.get(cell)
        if y is None:
            if fill is None:
                return None
            y = (0 if c > 0 else 1) if fill == "min" else (1 if c > 0 else 0)
        total += c * y
    return total


def stratified_mean(values, strata):
    groups = {}
    for v, s in zip(values, strata):
        groups.setdefault(s, []).append(v)
    return sum(sum(g) / len(g) for g in groups.values()) / len(groups)


def hoeffding(strata, value_span, alpha):
    groups = {}
    for s in strata:
        groups[s] = groups.get(s, 0) + 1
    count = len(groups)
    weights = sum(1 / (count ** 2 * n) for n in groups.values())
    return value_span * math.sqrt(0.5 * math.log(2 / alpha) * weights)


class Bootstrap:
    """Shared stratified resamples (Python Random(seed)); worlds in index order within strata."""

    def __init__(self, strata, draws, seed):
        import numpy as np
        self.np = np
        order = sorted(range(len(strata)), key=lambda i: (strata[i], i))
        self.blocks = []
        for s in sorted(set(strata)):
            members = [i for i in order if strata[i] == s]
            self.blocks.append(members)
        rng = Random(seed)
        self.index = np.empty((draws, len(strata)), dtype=np.int64)
        for b in range(draws):
            col = 0
            for members in self.blocks:
                n = len(members)
                for _ in range(n):
                    self.index[b, col] = members[rng.randrange(n)]
                    col += 1
        self.draws = draws

    def distribution(self, values):
        np = self.np
        v = np.asarray(values, dtype=float)[self.index]
        means, col = [], 0
        for members in self.blocks:
            n = len(members)
            means.append(v[:, col:col + n].mean(axis=1))
            col += n
        return np.sort(np.mean(means, axis=0))


def summarize(values, strata, boot, confidence, value_bounds):
    """Point estimate, percentile interval and the degenerate-case Hoeffding companion."""
    lo_i, hi_i = interval_indices(boot.draws, confidence)
    dist = boot.distribution(values)
    estimate = stratified_mean(values, strata)
    low, high = float(dist[lo_i]), float(dist[hi_i])
    L, U = value_bounds
    constant = all(len({values[i] for i in block}) == 1 for block in boot.blocks)
    result = dict(estimate=round(estimate, 6), interval=[round(low, 6), round(high, 6)], confidence=confidence,
                  n=len(values), degenerate=bool(low == high or constant))
    excludes = low > 0 or high < 0
    if result["degenerate"]:
        h = hoeffding(strata, U - L, 1 - confidence)
        result["hoeffding"] = [round(max(L, estimate - h), 6), round(min(U, estimate + h), 6)]
        excludes = excludes and (result["hoeffding"][0] > 0 or result["hoeffding"][1] < 0)
    result["direction"] = ("positive" if excludes and estimate > 0 else
                           "negative" if excludes and estimate < 0 else "inconclusive")
    return result


def paired_categories(ys_list, a, b):
    """For a contrast b - a: both / only b / only a / neither (known pairs only)."""
    counts = dict(both=0, only_first=0, only_second=0, neither=0, unknown=0)
    for ys in ys_list:
        x, y = ys.get(a), ys.get(b)
        if x is None or y is None:
            counts["unknown"] += 1
        elif x and y:
            counts["both"] += 1
        elif y:
            counts["only_second"] += 1
        elif x:
            counts["only_first"] += 1
        else:
            counts["neither"] += 1
    return counts


# ---------------------------------------------------------------- loading
def read(run):
    run = Path(run)
    config = json.loads((run / "inputs/thesis.json").read_text(encoding="utf-8"))
    manifest = json.loads((run / "inputs/thesis-worlds.json").read_text(encoding="utf-8"))
    uri = (run / "study.sqlite").resolve().as_uri() + "?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as db:
        meta = {k: json.loads(v) for k, v in db.execute("SELECT key, value FROM meta")}
        states = {i: json.loads(s) for i, s in db.execute("SELECT id, state FROM episodes")}
        calls = {i: dict(episode=e, outcome=json.loads(o) if o else None, request=json.loads(r))
                 for i, e, o, r in db.execute("SELECT id, episode, outcome, request FROM calls")}
        attempts = [dict(zip(("id", "call_id", "number", "stage", "contingency", "admitted_at", "finished_at", "status"), row))
                    for row in db.execute("SELECT id, call_id, number, stage, contingency, admitted_at, finished_at, status FROM attempts")]
        sessions = {i: json.loads(e) for i, e in db.execute("SELECT id, evidence FROM sessions")}
    return dict(run=run, config=config, manifest=manifest, worlds={w["id"]: w for w in manifest["worlds"]},
                meta=meta, states=states, calls=calls, attempts=attempts, sessions=sessions)


def outcomes(data, model, ids):
    table = []
    for wid in ids:
        w = data["worlds"][wid]
        ys = {cell: protocol.score(w, data["states"].get(f"{model}/{wid}/{cell}")) for cell in ("prefix",) + CELLS}
        table.append(ys)
    return table


def episode_cost(data, eid):
    calls = [c for c in data["calls"].values() if c["episode"] == eid and c["outcome"]]
    return dict(calls=len(calls), input_tokens=sum(c["outcome"].get("input_tokens") or 0 for c in calls),
                generated_tokens=sum(c["outcome"].get("generated_tokens") or 0 for c in calls),
                ready_seconds=round(sum(c["outcome"].get("ready_seconds") or 0 for c in calls), 3))


# ---------------------------------------------------------------- analysis
def analyse(run, *, draws=None):
    data = read(run)
    config, meta = data["config"], data["meta"]
    draws = draws or config["bootstrap_draws"]
    freeze = meta.get("freeze")
    stopped = meta.get("declared_stopped")
    result = dict(regime=config["regime"], study=meta["binding"]["study"], profile=meta["binding"]["profile"],
                  binding=meta["binding"], gate_report=meta.get("gate_report"), freeze=freeze,
                  declared_stopped=stopped, coverage={}, models={}, model_differences={},
                  attempts=attempt_summary(data), sessions=session_summary(data),
                  notes=["Scripted rehearsal data are pipeline evidence, never model results."]
                  if meta["binding"]["profile"] == "rehearsal" else [])
    result["development"] = development_summary(data)
    if not freeze:
        result["status"] = "development" if not meta.get("gate_report") else "awaiting main authorization"
        return result
    ids = freeze["worlds"]
    strata = [data["worlds"][i]["stratum"] for i in ids]
    boot = None
    per_model_values = {}
    for model in freeze["models"]:
        table = outcomes(data, model, ids)
        unknown = sum(table[i][c] is None for i in range(len(ids)) for c in ("prefix",) + CELLS)
        complete = unknown == 0
        result["coverage"][model] = dict(intended_worlds=len(ids), unknown_episode_outcomes=unknown,
                                         complete=complete)
        if not complete and not stopped:
            result["models"][model] = dict(withheld="main incomplete; estimates are computed only when every intended "
                                                    "episode is terminal or the campaign is declared stopped")
            continue
        if boot is None:
            boot = Bootstrap(strata, draws, config["bootstrap_seed"])
        result["models"][model] = model_result(data, model, ids, strata, table, boot, config, complete)
        per_model_values[model] = table
    if len(per_model_values) == 2 and all(result["coverage"][m]["complete"] for m in per_model_values):
        q, g = (per_model_values[m] for m in MODELS)
        for name in PRIMARY:
            coefficients = LINEAR[name][0]
            diff = [world_value(coefficients, a) - world_value(coefficients, b) for a, b in zip(q, g)]
            low, high = value_range(coefficients)
            result["model_differences"][name] = summarize(diff, strata, boot, config["secondary_confidence"],
                                                          (low - high, high - low))
    result["status"] = ("complete" if all(c["complete"] for c in result["coverage"].values()) else
                        "declared stopped" if stopped else "main in progress")
    return result


def model_result(data, model, ids, strata, table, boot, config, complete):
    out = dict(cells={}, estimands={}, edit_types={}, paired={}, funnel={}, controls={}, costs={},
               prefix_strata={}, bounds=None)
    fills = [None] if complete else ["min", "max"]
    for name, (coefficients, label) in LINEAR.items():
        confidence = config["primary_confidence"] if name in PRIMARY else config["secondary_confidence"]
        entries = {}
        for fill in fills:
            values = [world_value(coefficients, ys, fill) for ys in table]
            entries[fill or "observed"] = summarize(values, strata, boot, confidence, value_range(coefficients))
        if complete:
            entry = entries["observed"]
        else:
            lo, hi = entries["min"], entries["max"]
            agree = lo["direction"] == hi["direction"]
            entry = dict(bounds=dict(lower=lo, upper=hi), direction=lo["direction"] if agree else "inconclusive",
                         estimate_range=[lo["estimate"], hi["estimate"]])
        entry["label"] = label
        entry["primary"] = name in PRIMARY
        target = out["cells"] if name.startswith("rate_") else out["estimands"]
        target[name] = entry
    for edit in ("demote", "keep"):
        keep = [i for i, wid in enumerate(ids) if data["worlds"][wid]["edit"] == edit]
        sub_strata = [strata[i] for i in keep]
        if not keep or not complete:
            continue
        sub_boot = Bootstrap(sub_strata, boot.draws, config["bootstrap_seed"])
        out["edit_types"][edit] = {name: summarize([world_value(LINEAR[name][0], table[i]) for i in keep],
                                                   sub_strata, sub_boot, config["secondary_confidence"],
                                                   value_range(LINEAR[name][0]))
                                   for name in PRIMARY + ("theta",)}
    out["paired"] = {"delta_H (RV vs CV)": paired_categories(table, "RV", "CV"),
                     "delta_E retain (RV vs RN)": paired_categories(table, "RV", "RN"),
                     "delta_E clear (CV vs CN)": paired_categories(table, "CV", "CN"),
                     "no change (RN vs CN)": paired_categories(table, "RN", "CN")}
    for cell in ("prefix",) + CELLS:
        rows = [protocol.funnel(data["worlds"][wid], data["states"].get(f"{model}/{wid}/{cell}")) for wid in ids]
        rows = [r for r in rows if r]
        classes = {}
        for r in rows:
            for c in r["classes"]:
                classes[c] = classes.get(c, 0) + 1
        needers = [r for r in rows if r["needers"]]
        out["funnel"][cell] = dict(
            episodes=len(rows), success=sum(r["success"] for r in rows), completed=sum(r["completed"] for r in rows),
            wrong_agreement=sum(r["wrong_agreement"] for r in rows), wrong_disagreement=sum(r["wrong_disagreement"] for r in rows),
            terminal={t: sum(r["terminal"] == t for r in rows) for t in ("both_submitted", "horizon_exhausted", "waiting_deadlock")},
            answer_visible_to_needer=sum(all(r["delivered_to_needer"].values()) for r in needers),
            needer_episodes=len(needers),
            holder_correct=sum(all(r["holder_correct"]) for r in rows),
            needer_correct=sum(all(r["needer_correct"]) for r in needers),
            submission_classes=classes)
    for phase in ("original", "revised"):
        states = [data["states"].get(f"{model}/{wid}/control-{phase}") for wid in ids]
        out["controls"][phase] = dict(correct=sum(bool(s and s.get("correct")) for s in states), total=len(ids))
    for cell in ("prefix",) + CELLS:
        costs = [episode_cost(data, f"{model}/{wid}/{cell}") for wid in ids]
        out["costs"][cell] = {k: round(sum(c[k] for c in costs) / len(ids), 3) for k in costs[0]}
    out["costs"]["logical_per_policy"] = {cell: {k: round(out["costs"]["prefix"][k] + out["costs"][cell][k], 3)
                                                 for k in out["costs"][cell]} for cell in CELLS}
    for label, wanted in (("correct_prefix", 1), ("incorrect_prefix", 0)):
        chosen = [ys for ys in table if ys["prefix"] == wanted]
        out["prefix_strata"][label] = dict(worlds=len(chosen), **{cell: sum(ys[cell] == 1 for ys in chosen) for cell in CELLS})
    if not complete:
        out["bounds"] = "Unknown outcomes are bounded at 0 and 1 by coefficient sign; claim only if both bounded intervals agree."
    return out


def attempt_summary(data):
    summary = {}
    for a in data["attempts"]:
        key = f"{a['stage']}/{'contingency' if a['contingency'] else 'first'}/{a['status']}"
        summary[key] = summary.get(key, 0) + 1
    return dict(total=len(data["attempts"]), by_stage_and_status=summary)


def session_summary(data):
    rows = [e for k, e in data["sessions"].items() if k.startswith("session/")]
    return [dict(session=e["session"], start=e["start"], last_seen=e.get("last_seen"), scope=e.get("scope"),
                 gpu=e.get("gpu"), closed=e.get("closed")) for e in rows]


def development_summary(data):
    meta = data["meta"]
    result = {}
    for model in MODELS:
        record = meta.get(f"gates/{model}")
        if record:
            result[model] = record
    return result


# ---------------------------------------------------------------- reports
def pct(x):
    return "n/a" if x is None else f"{100 * x:+.1f} pp" if abs(x) <= 2 else str(x)


def fmt_interval(entry):
    if "bounds" in entry:
        lo, hi = entry["bounds"]["lower"], entry["bounds"]["upper"]
        return (f"bounded {pct(lo['estimate'])} to {pct(hi['estimate'])}; intervals "
                f"[{pct(lo['interval'][0])}, {pct(lo['interval'][1])}] and [{pct(hi['interval'][0])}, {pct(hi['interval'][1])}]")
    text = f"{pct(entry['estimate'])} [{pct(entry['interval'][0])}, {pct(entry['interval'][1])}]"
    if entry.get("hoeffding"):
        text += f" (degenerate; Hoeffding [{pct(entry['hoeffding'][0])}, {pct(entry['hoeffding'][1])}])"
    return text


def fmt_rate(entry):
    if "bounds" in entry:
        lo, hi = entry["bounds"]["lower"], entry["bounds"]["upper"]
        return f"bounded {100 * lo['estimate']:.1f}% to {100 * hi['estimate']:.1f}%"
    return f"{100 * entry['estimate']:.1f}% [{100 * entry['interval'][0]:.1f}%, {100 * entry['interval'][1]:.1f}%]"


def write_report(run, out=None, *, draws=None, plots=True):
    run = Path(run)
    out = Path(out or run / "reports")
    out.mkdir(parents=True, exist_ok=True)
    result = analyse(run, draws=draws)
    data = read(run)
    (out / "analysis.json").write_text(json.dumps(result, indent=1, sort_keys=True, default=str) + "\n", encoding="utf-8")
    lines = [f"# Thesis study report: {result['study']}", "",
             f"Status: **{result['status']}** · profile `{result['profile']}` · source `{result['binding']['source_commit']}`", ""]
    lines += result["notes"]
    gate = result.get("gate_report")
    if gate:
        lines += ["", f"## Development gates (report `{gate['id']}`)", "",
                  "| Model | G1 | G2 controls | G3 legal prefix calls | G4 original teams | Admitted | g (s/call) |",
                  "|---|---|---|---|---|---|---:|"]
        for m, r in gate["models"].items():
            if not r.get("complete"):
                lines.append(f"| {m} | fail | — | — | — | no | — |")
                continue
            lines.append(f"| {m} | {'pass' if r['G1']['passed'] else 'fail'} | {r['G2']['correct']}/{r['G2']['total']} | "
                         f"{r['G3']['fraction']:.1%} | {r['G4']['correct']}/{r['G4']['total']} | "
                         f"{'yes' if r['admitted'] else 'no'} | {r['g_seconds']} |")
        lines += ["", "Development outcomes are descriptive and never gated."]
    if result["freeze"]:
        f = result["freeze"]
        lines += ["", "## Main", "", f"Frozen: {f['n']} worlds for {', '.join(f['models'])} "
                  f"(authorization `{f['authorization']}`, input limit {f['input_limit']})."]
        for model, cov in result["coverage"].items():
            lines.append(f"- {model}: unknown episode outcomes {cov['unknown_episode_outcomes']}; complete={cov['complete']}")
    for model, r in result["models"].items():
        lines += ["", f"## {model}", ""]
        if "withheld" in r:
            lines.append(r["withheld"])
            continue
        lines += ["| Estimand | Estimate and interval | Direction |", "|---|---|---|"]
        for name in ("delta_E", "delta_H", "theta", "delta_E_retain", "delta_E_clear", "delta_H_no_change"):
            e = r["estimands"][name]
            tag = " (primary, 97.5%)" if e["primary"] else " (95%)"
            lines.append(f"| {name}{tag}: {e['label']} | {fmt_interval(e)} | {e['direction']} |")
        lines += ["", "| Cell | Success rate |", "|---|---|"]
        for name, e in r["cells"].items():
            lines.append(f"| {name.removeprefix('rate_')} | {fmt_rate(e)} |")
        lines += ["", "Paired categories (first, second): " + json.dumps(r["paired"]), "",
                  "Controls: " + json.dumps(r["controls"]), "", "Funnel by cell:", ""]
        for cell, fn in r["funnel"].items():
            lines.append(f"- {cell}: success {fn['success']}/{fn['episodes']}, completed {fn['completed']}, "
                         f"answer visible to needer {fn['answer_visible_to_needer']}/{fn['needer_episodes']}, "
                         f"holder correct {fn['holder_correct']}, needer correct {fn['needer_correct']}, "
                         f"terminal {fn['terminal']}, classes {fn['submission_classes']}")
        lines += ["", "Mean cost per world: " + json.dumps(r["costs"])]
    if result["model_differences"]:
        lines += ["", "## Model differences (Qwen - Granite, descriptive 95%)", ""]
        for name, e in result["model_differences"].items():
            lines.append(f"- {name}: {fmt_interval(e)} ({e['direction']})")
    lines += ["", "## Attempts", "", "```", json.dumps(result["attempts"], indent=1), "```"]
    (out / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    withheld = {m for m, r in result["models"].items() if "withheld" in r}
    write_tables(data, out, withheld)
    write_casebook(data, result, out, withheld)
    if plots and result["models"]:
        try:
            write_figures(result, out)
        except ImportError:
            pass
    return result


def write_tables(data, out, withheld=frozenset()):
    """Episode and call tables; main outcomes of a model with withheld estimates stay blank."""
    with (out / "episodes.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["model", "world", "group", "stratum", "edit", "owner", "first", "cell", "terminal",
                         "submission_0", "submission_1", "success"])
        for eid, state in sorted(data["states"].items()):
            parts = eid.split("/")
            if len(parts) != 3 or parts[0] not in MODELS:
                continue
            model, wid, cell = parts
            w = data["worlds"].get(wid)
            if not w:
                continue
            subs = state.get("submissions") or [state.get("submission"), None]
            success = protocol.score(w, state) if cell in ("prefix",) + CELLS else state.get("correct")
            if model in withheld and w["group"] == "main":
                subs, success = ["withheld", "withheld"], "withheld"  # no interim analysis
            writer.writerow([model, wid, w["group"], w["stratum"], w["edit"], w["owner"], w["first"], cell,
                             state.get("terminal"), subs[0], subs[1], success])
    with (out / "calls.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["call", "episode", "failure", "termination", "input_tokens", "generated_tokens",
                         "ready_seconds", "stage", "session"])
        for cid, c in sorted(data["calls"].items()):
            o = c["outcome"] or {}
            d = o.get("dispatch") or {}
            writer.writerow([cid, c["episode"], o.get("failure"), o.get("termination"), o.get("input_tokens"),
                             o.get("generated_tokens"), o.get("ready_seconds"), d.get("stage"), d.get("session")])


def casebook_worlds(data, ids):
    chosen, seen = [], set()
    for wid in ids:
        s = data["worlds"][wid]["stratum"]
        if s not in seen:
            seen.add(s)
            chosen.append(wid)
    return chosen


def trace(data, model, wid, cell):
    """Exact requests and replies in the order the calls were made."""
    eid = f"{model}/{wid}/{cell}"
    state = data["states"].get(eid) or {}
    ordered = [e["call"] for e in state.get("events", [])]
    calls = ordered + sorted(cid for cid, c in data["calls"].items() if c["episode"] == eid and cid not in ordered)
    lines = [f"### {eid}", ""]
    for cid in calls:
        if cid not in data["calls"]:
            continue
        c = data["calls"][cid]
        user = c["request"]["messages"][-1]["content"]
        reply = (c["outcome"] or {}).get("visible_text")
        lines += [f"**{cid}**", "", "Request (user message):", "```text", user, "```", "Reply:", "```text",
                  str(reply), "```", ""]
    state = data["states"].get(eid)
    if state:
        lines += [f"Terminal: {state.get('terminal')}; submissions: {state.get('submissions')}", ""]
    return lines


def write_casebook(data, result, out, withheld=frozenset()):
    freeze = data["meta"].get("freeze")
    if not freeze:
        return
    lines = ["# Casebook (fixed rule: lowest-index main world per stratum)", ""]
    for model in freeze["models"]:
        if model in withheld:
            lines += [f"{model}: withheld until main is complete or the campaign is declared stopped.", ""]
            continue
        for wid in casebook_worlds(data, freeze["worlds"]):
            for cell in ("prefix",) + CELLS:
                lines += trace(data, model, wid, cell)
    (out / "casebook.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_figures(result, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    models = [m for m, r in result["models"].items() if "estimands" in r and "estimate" in r["estimands"]["delta_E"]]
    if not models:
        return
    fig, ax = plt.subplots(figsize=(7, 3.5))
    names = ["delta_E", "delta_H", "theta"]
    for k, model in enumerate(models):
        for j, name in enumerate(names):
            e = result["models"][model]["estimands"][name]
            x = j + (k - (len(models) - 1) / 2) * 0.2
            ax.errorbar([x], [e["estimate"]], yerr=[[e["estimate"] - e["interval"][0]], [e["interval"][1] - e["estimate"]]],
                        fmt="o", capsize=4, label=model if j == 0 else None)
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(["revision cost", "history effect", "interaction"])
    ax.set_ylabel("difference in team success")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "estimands.png", dpi=150)
    plt.close(fig)


def show(run, model, world, cell):
    data = read(run)
    return "\n".join(trace(data, model, world, cell))
