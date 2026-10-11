"""Derive course diagnostics/costs from original M3 SQLite snapshots, without execution."""

import argparse
from collections import Counter, defaultdict
from contextlib import closing
from dataclasses import asdict
from datetime import datetime
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
from zipfile import ZipFile

from recovery.costs import costs_run
from recovery.evaluate import write_evaluation
from recovery.manifests import load_population, load_schedules
from recovery.state import PUBLIC_FEEDBACK
from recovery.tasks import Task
from tests.course_analysis_archive import RUN, WORKERS, extract, independent_checks as outcome_checks
from tests.information_examples import examples
from tests.outcome_fixture import ROOT
from tests.test_course_diagnostics import gold

FIXTURE = ROOT / "tests/fixtures/course_diagnostic_cost_tables.json.gz"
AS_OF = "2026-10-11T23:59:59+00:00"
FINAL = {"completed", "timeout", "infrastructure_failure", "replay"}


class ScriptedWordCounter:
    """Exact archived CPU counter; these are explicitly not native model tokens."""

    def encode(self, text, *, add_special_tokens=False):
        assert not add_special_tokens
        return list(range(len(text.split())))


def originals(paths):
    """Independent SQL join and public saved-byte decoder; no production reader."""
    from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
    calls, inputs, attempts, committed, allocations, processes = {}, {}, [], {}, [], []
    for worker, path in enumerate(paths):
        if not path.exists(): continue
        with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as con:
            con.row_factory = sqlite3.Row
            con.execute("PRAGMA query_only=ON")
            con.execute("BEGIN")
            for row in con.execute("SELECT * FROM calls"):
                assert row["call_id"] not in calls
                calls[row["call_id"]] = dict(row)
            for row in con.execute("SELECT * FROM round_inputs"):
                inputs[row["branch_id"], row["round_number"]] = json.loads(row["requests_json"])
            attempts.extend(dict(row, worker=worker) for row in con.execute("SELECT * FROM attempts"))
            tables = {row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "checkpoints" in tables:
                latest = {}
                for row in con.execute("SELECT * FROM checkpoints WHERE checkpoint_ns='' ORDER BY checkpoint_id"):
                    latest[row["thread_id"]] = row
                for branch_id, row in latest.items():
                    values = JsonPlusSerializer().loads_typed((row["type"], row["checkpoint"]))["channel_values"]
                    committed[branch_id] = json.loads(values["committed"])
            for table, target in (("allocations", allocations), ("provider_processes", processes)):
                if table in tables:
                    target.extend(dict(row, worker=worker) for row in con.execute(f"SELECT * FROM {table}"))
    return calls, inputs, attempts, committed, allocations, processes


def independent_diagnostics(worlds, branches, paths, actual, *, tokenizer=True):
    """Direct coordinate, inventory, receipt, original-attempt and whole-policy references."""
    calls, inputs, attempts, committed, allocations, processes = originals(paths)
    counts = outcome_checks(worlds, branches, paths, actual)
    by_world, by_branch = {w.world_id: w for w in worlds}, {b.branch_id: b for b in branches}
    scheduled = {c.call_id: (b, c) for b in branches for c in b.calls}
    outcomes = {r["call_id"]: r for r in actual["outcomes"]}

    def reply(cid):
        saved = calls.get(cid)
        if not saved or saved["status"] not in FINAL: return "unknown", None
        physical = calls[saved["generation_id"]]
        if physical["status"] in ("timeout", "infrastructure_failure"): return "failed", None
        validation = json.loads(saved["validation_json"])
        if validation["candidate"]["status"] != "valid": return "invalid", None
        return "valid", json.loads(json.loads(physical["raw_json"])["text"])["candidate"]

    def values(world, peer, candidate):
        if candidate is None: return {}
        if world.task is Task.BFS: return {int(k): v for k, v in candidate.items()}
        start = 6 * peer if world.task in (Task.PREFIX, Task.SORT) else 1 if world.task is Task.DIFFERENCE else 0
        return {start + j: value for j, value in enumerate(candidate)}

    coordinate_groups = defaultdict(list)
    for row in actual["coordinates"]:
        coordinate_groups[row["call_id"]].append(row)
    references = {}
    for cid, rows in coordinate_groups.items():
        branch, call = scheduled[cid]
        prepared = by_world[branch.world_id]
        current = prepared.event_world(branch.event)
        old, new = values(prepared.world, 0, gold(prepared.world)), values(current, 0, gold(current))
        # Independent full-array coordinates, not one local output slice.
        if current.task in (Task.PREFIX, Task.SORT):
            old, new = dict(enumerate(gold(prepared.world))), dict(enumerate(gold(current)))
        prefix_id = next(c.call_id for c in by_branch[branch.prefix_parent].calls if c.peer == call.peer and c.round_number == 4)
        status, candidate = reply(cid)
        prefix_status, prefix_candidate = reply(prefix_id)
        submitted, prefix = values(current, call.peer, candidate), values(prepared.world, call.peer, prefix_candidate)
        changed, eligible, errors = [], [], []
        category_counts = Counter()
        for row in rows:
            j = row["coordinate"]
            D = old[j] != new[j]
            old_correct = None if prefix_status == "unknown" else prefix_status == "valid" and prefix[j] == old[j]
            correct = None if status == "unknown" else int(status == "valid" and submitted[j] == new[j])
            category = ("unknown" if status == "unknown" else "malformed_or_missing" if status != "valid" else
                "new_gold" if correct else "old_gold" if submitted[j] == old[j] else "other_valid") if D else None
            assert (row["old_gold"], row["new_gold"], row["set"], row["value"], row["prefix_value"], row["new_correct"],
                row["prefix_correct"], row["changed_category"]) == (old[j], new[j], "D" if D else "U", submitted.get(j), prefix.get(j), correct, old_correct, category)
            if D:
                changed.append(j)
                category_counts[category] += 1
            elif old_correct: eligible.append(j)
            elif prefix_status == "valid": errors.append(j)
        references[cid] = dict(status=status, prefix_status=prefix_status, changed=changed, eligible=eligible, errors=errors,
            correct_changed=sum(submitted.get(j) == new[j] for j in changed) if status == "valid" else 0,
            preserved=sum(submitted.get(j) == new[j] for j in eligible) if status == "valid" else 0,
            repaired=sum(submitted.get(j) == new[j] for j in errors) if status == "valid" else 0,
            categories=category_counts, U=any(old[r["coordinate"]] == new[r["coordinate"]] for r in rows))
    for row in actual["peer_diagnostics"]:
        ref = references[row["call_id"]]
        metric = row["metric"]
        eligible = ref["eligible"] if metric in ("preservation", "collateral_damage") else ref["errors"] if metric == "old_error_repair" else ref["changed"]
        unknown_prefix = metric in ("preservation", "collateral_damage", "old_error_repair") and ref["prefix_status"] == "unknown" and ref["U"]
        denominator = None if unknown_prefix else len(eligible)
        count = {"changed_accuracy": ref["correct_changed"], "preservation": ref["preserved"],
            "collateral_damage": len(ref["eligible"]) - ref["preserved"], "old_error_repair": ref["repaired"],
            "old_value_persistence": ref["categories"]["old_gold"], "changed_other_valid": ref["categories"]["other_valid"],
            "changed_malformed_or_missing": ref["categories"]["malformed_or_missing"]}[metric]
        numerator = None if unknown_prefix or ref["status"] == "unknown" and eligible else count
        rate = numerator / denominator if denominator and numerator is not None else None
        assert (row["denominator"], row["numerator"], row["rate"], row["eligible_coordinates"]) == (denominator, numerator, rate, eligible)

    info, costs = actual["information"], actual["costs"]
    def state(bid, number):
        saved = inputs.get((bid, number))
        return json.loads(saved["before"]) if saved else None
    def check_inventory(current, sources, peer, result, excluded=None):
        if sources is None:
            assert result is None
            return
        known = [r for r in sources if "value" in r]
        pairs = sorted([r["record_id"], r["version"]] for r in known if r["owner"] != peer and r["record_id"] != excluded)
        denominator = sum(r.owner != peer and r.record_id != excluded for r in current.records)
        assert result["remote_pairs"] == pairs
        assert (result["remote_known"], result["remote_denominator"], result["pending_records"], result["known_tombstones"],
            result["complete_current_raw"]) == (len(pairs), denominator, len(sources) - len(known), sum(r["deleted"] for r in known), len(known) == len(current.records))
    for row in info["communication"]:
        status, _ = reply(row["call_id"])
        physical = calls.get(scheduled[row["call_id"]][1].generation_id)
        if status == "unknown":
            assert row["validated_messages"] is None and not row["observed"]
        elif status in ("invalid", "failed"):
            assert row["validated_messages"] == row["source_attempts"] == row["text_attempts"] == 0
        else:
            sends = json.loads(json.loads(physical["raw_json"])["text"])["send"]
            assert (row["validated_messages"], row["source_attempts"], row["text_attempts"]) == (
                len(sends), sum(len(send.get("source_refs", ())) for send in sends), sum(send.get("text") is not None for send in sends))
    for row in info["receipt_timing"]:
        receipt_rounds = []
        for number in range(1, 5):
            before = state(row["branch_id"], number)
            if before is None: continue
            edit = (by_world[row["world_id"]].main_edit if row["event"] == "revision" else by_world[row["world_id"]].preserving_edit)
            held = any(s["record_id"] == edit.record_id and s["version"] == 2 and "value" in s for s in before["peers"][row["peer"]]["sources"])
            if held: receipt_rounds.append(number)
        first = min(receipt_rounds) if receipt_rounds else None
        exact = first is not None and all(state(row["branch_id"], n) is not None for n in range(1, first))
        assert row["first_observed_receipt_round"] == first and row["first_receipt_round"] == (first if exact else None)
        if first:
            before = state(row["branch_id"], first)
            delivered = [d for d in before["deliveries"] if d["delivery_id"] in row["receipt_delivery_ids"]]
            assert sorted({d["origin"] for d in delivered}) == row["receipt_origins"]
            assert delivered and all(d["recipient"] == row["peer"] and d["first_usable"]["round_number"] <= first for d in delivered)
        if all(state(row["branch_id"], n) is not None for n in range(1, 5)) and not first:
            assert row["category"] == "no_receipt"
    for row in info["receipt_information"]:
        prepared = by_world[row["world_id"]]
        source = next(r for r in prepared.world.records if r.record_id == prepared.main_edit.record_id)
        for evidence in row["visibility"]["evidence"]:
            assert evidence["record_id"] == source.record_id and evidence["value"] == source.value
            if evidence["origin"] == "literal_derived_assertion":
                if "delivery_id" in evidence:
                    before = state(row["branch_id"], row["round"])
                    text = next(d["text"] for d in before["deliveries"] if d["delivery_id"] == evidence["delivery_id"])
                else:
                    saved = calls[evidence["call_id"]]
                    text = json.loads(calls[saved["generation_id"]]["raw_json"])["text"]
                assert text[slice(*evidence["span"])] == evidence["excerpt"] == f"{source.record_id}/v1={source.value}"
    for row in info["prefix"]:
        before = state(row["branch_id"], row["round"])
        sources = before["peers"][row["peer"]]["sources"] if before else None
        check_inventory(by_world[row["world_id"]].world, sources, row["peer"], row["inventory"])
        if before:
            saved = inputs[row["branch_id"], row["round"]]
            peer = before["peers"][row["peer"]]
            components = [entry["text"] if "text" in entry else "compact candidate" for entry in peer["history"]]
            # A compact JSON candidate encodes as one scripted word, regardless
            # of its keys; it is separate from literal own reply/prose content.
            count = sum(len(part.split()) if part != "compact candidate" else 1 for part in components)
            if peer["candidate"].get("historical"): count += 1
            count += sum(len(PUBLIC_FEEDBACK[entry["code"]].split()) for entry in peer["feedback"])
            assert row["input_tokens"] == len(saved["tokenized"][row["peer"]]["input_ids"])
            assert row["history_content_tokens"] == (count if tokenizer or count == 0 else None)
    for row in info["boundary_acquisition"]:
        branch = by_branch[row["branch_id"]]
        prepared = by_world[branch.world_id]
        before = state(branch.branch_id, 1)
        terminal = committed.get(branch.branch_id)
        if before is None and terminal and (not terminal["last_slot"] or terminal["last_slot"]["phase"] == "prefix"): before = terminal
        edit = prepared.main_edit if branch.event == "revision" else prepared.preserving_edit if branch.event == "preserving" else None
        check_inventory(prepared.event_world(branch.event), before["peers"][row["peer"]]["sources"] if before else None,
            row["peer"], row["boundary"], edit.record_id if edit else None)
        deliveries = {}
        for number in range(1, 5):
            observed = state(branch.branch_id, number)
            if observed: deliveries.update((d["delivery_id"], d) for d in observed["deliveries"])
        if terminal: deliveries.update((d["delivery_id"], d) for d in terminal["deliveries"])
        authority = {(r.record_id, r.version): r for r in (*prepared.world.records, *prepared.event_world(branch.event).records)}
        for delivery in deliveries.values():
            if delivery.get("source"):
                payload = delivery["source"]
                assert payload == json.loads(json.dumps(asdict(authority[payload["record_id"], payload["version"]])))
        attempt_ids = set()
        all_known = True
        for call in branch.calls:
            status, _ = reply(call.call_id)
            all_known = all_known and status != "unknown"
            if status != "valid": continue
            sends = json.loads(json.loads(calls[call.generation_id]["raw_json"])["text"])["send"]
            for send in sends:
                if send["to"] == row["peer"]:
                    attempt_ids.update(f"{call.call_id}/to{row['peer']}/source{n}" for n in range(len(send.get("source_refs", ()))))
        assert set(row["validated_attempt_delivery_ids"]) == attempt_ids
        assert row["all_validated_delivery_attempts"] == (len(attempt_ids) if all_known else None)
        assert row["observed_delivery_attempts"] == len(attempt_ids & deliveries.keys())
        acquired = sorted({(d["source"]["record_id"], d["source"]["version"]) for d in deliveries.values()
            if d["recipient"] == row["peer"] and d.get("source") and d.get("acquired") is True
            and d["delivery_id"] in attempt_ids})
        assert row["observed_unique_acquired_pairs"] == [list(pair) for pair in acquired]
        complete = bool(terminal and terminal["last_slot"] and terminal["last_slot"]["phase"] == "recovery" and terminal["last_slot"]["round_number"] == 4)
        assert row["unique_acquired_count"] == (len(acquired) if complete else None)
    for row in info["transport_references"]:
        status, candidate = reply(row["prefix_call_id"])
        applicable = by_branch[row["branch_id"]].task in (Task.PREFIX, Task.DIFFERENCE) and row["event"] == "revision"
        assert row["available"] == (status == "valid" and applicable)
        if row["available"]:
            prepared = by_world[row["world_id"]]
            old = gold(prepared.world)
            new = gold(prepared.event_world("revision"))
            if prepared.world.task is Task.PREFIX:
                old, new = old[6 * row["peer"]:6 * (row["peer"] + 1)], new[6 * row["peer"]:6 * (row["peer"] + 1)]
            expected = [value + b - a for value, a, b in zip(candidate, old, new)]
            assert row["candidate"] == expected and row["actual_old_candidate"] == candidate
            assert row["residual_old"] == row["residual_new"] == [value - a for value, a in zip(candidate, old)]

    def moment(value): return datetime.fromisoformat(value).timestamp()
    duration = {}
    for attempt in attempts:
        low = attempt["elapsed_seconds"] if attempt["elapsed_seconds"] is not None else attempt["observed_seconds"]
        high = low if attempt["elapsed_seconds"] is not None else max(low, moment(attempt.get("recovered_at") or AS_OF) - moment(attempt["started_at"]))
        duration.setdefault(attempt["call_id"], []).append((low, high))
    physical = [sum(pair[j] for ranges in duration.values() for pair in ranges) for j in (0, 1)]
    assert all(abs(a - b) < 1e-8 for a, b in zip(physical, costs["physical"]["attempt_seconds"]))
    assert costs["physical"]["attempts"] == len(attempts)
    assert costs["physical"]["request_tokens"] == sum(calls[a["call_id"]]["request_tokens"] for a in attempts)
    assert costs["physical"]["output_tokens"] == sum(len(json.loads(r["raw_json"])["token_ids"]) for r in calls.values() if r["raw_json"])
    for row in costs["policy_costs"]:
        branch = by_branch[row["branch_id"]]
        used = (*by_branch[branch.prefix_parent].calls, *branch.calls) if branch.prefix_parent else branch.calls
        ranges = [pair for c in used for pair in duration.get(c.generation_id, ())]
        expected = [sum(pair[j] for pair in ranges) for j in (0, 1)]
        complete = all(c.call_id in calls and calls[c.call_id]["status"] in FINAL for c in used)
        assert row["call_ids"] == [c.call_id for c in used]
        assert row["generation_ids"] == [c.generation_id for c in used]
        assert row["logical_calls"] == len(used)
        assert all(abs(a - b) < 1e-8 for a, b in zip(expected, row["seconds"]))
        assert row["complete_policy_seconds"] == (row["seconds"] if complete else None)
        assert row["unknown_calls"] == sum(c.call_id not in calls or calls[c.call_id]["status"] not in FINAL for c in used)
    for row in costs["boundary_selections"]:
        current = by_world[row["world_id"]].event_world(row["event"])
        expected = {(r.record_id, r.version) for r in current.records}
        coverage = []
        for bid in row["comparator_branch_ids"].values():
            before = state(bid, 1)
            if before is None:
                possible = committed.get(bid)
                if possible and (not possible["last_slot"] or possible["last_slot"]["phase"] == "prefix"): before = possible
            if before:
                coverage.append([expected <= {(s["record_id"], s["version"]) for s in p["sources"] if "value" in s} for p in before["peers"]])
        assert not coverage or all(row == coverage[0] for row in coverage)
        policy = "C" if coverage and all(coverage[0]) else "K" if coverage else None
        assert row["selected_policy"] == policy
        assert row["selected_branch_id"] == row["comparator_branch_ids"].get(policy)
    allocated = sum(moment(row["stopped_at"] or AS_OF) - moment(row["started_at"]) for row in allocations)
    if allocations:
        assert abs(costs["resources"]["allocated_gpu_hours"] * 3600 - allocated) < 1e-7
        assert abs(sum(costs["resources"]["partition_seconds"].values()) - allocated) < 1e-7
    else: assert costs["resources"]["allocated_gpu_hours"] is None
    excerpts = []
    for branch in sorted(branches, key=lambda b: b.branch_id):
        call = next((c for c in branch.calls if c.call_id in calls and calls[c.call_id]["raw_json"]), None)
        if call:
            raw = json.loads(calls[call.call_id]["raw_json"])
            excerpts.append(dict(world_id=branch.world_id, branch_id=branch.branch_id, call_id=call.call_id,
                generation_id=call.generation_id, family=branch.task.value, phase=branch.phase,
                text=raw["text"], selection="First recorded original raw reply by immutable branch/call order; CPU validation only"))
    return dict(counts, coordinate_rows=len(actual["coordinates"]), diagnostic_rows=len(actual["peer_diagnostics"]),
        original_attempts=len(attempts), original_allocations=len(allocations), physical_seconds=physical), excerpts


def derive(worlds, branches, paths, *, estimands=True, tokenizer=True):
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.exists()}
    actual = costs_run(worlds, branches, paths, now=AS_OF, diagnostics=True,
        estimands=estimands, tokenizer=ScriptedWordCounter() if tokenizer else None)
    audit, excerpts = independent_diagnostics(worlds, branches, paths, actual, tokenizer=tokenizer)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == digest for p, digest in before.items())
    return {key: actual[key] for key in ("coverage", "information", "costs", "peer_diagnostics", "diagnostic_summaries",
        "annotations", "annotation_counts", "rounds", "trajectories")}, audit, excerpts


def reconstruct(bundle=RUN):
    cases, audits, excerpts = {}, {}, {}
    with tempfile.TemporaryDirectory(prefix="course-diagnostics-") as temporary, ZipFile(bundle) as archive:
        root = Path(temporary)
        evidence = json.loads(archive.read("evidence.json"))
        extract(archive, root, ("inputs/population.json", "inputs/schedules.json"))
        population = load_population(root / "inputs/population.json")
        schedules = load_schedules(root / "inputs/schedules.json", population)
        by_world = {w.world_id: w for w in population.main + population.development}
        by_branch = {b.branch_id: b for b in schedules.main + schedules.development}
        for case in evidence["cases"]:
            base = case["directory"]
            selection = json.loads(archive.read(base + "/selection.json"))
            extract(archive, root, [base + "/" + name for name in selection["workers"]])
            worlds = tuple(by_world[name] for name in selection["world_ids"])
            branches = tuple(by_branch[name] for name in selection["branch_ids"])
            paths = tuple(root / base / name for name in selection["workers"])
            cases[base], audits[base], excerpts[base] = derive(worlds, branches, paths)
            if "stopped_worker" in case:
                extract(archive, root, [base + "/" + case["stopped_worker"]])
                stopped = (root / base / case["stopped_worker"],)
                cases[base + "/stopped"], audits[base + "/stopped"], excerpts[base + "/stopped"] = derive(worlds, branches, stopped)
            if len(worlds) == 5:
                cases["full-main-20"], audits["full-main-20"], excerpts["full-main-20"] = derive(population.main, schedules.main, paths)
        missing = (root / "absent.sqlite",)
        for name, worlds, branches in (("unexecuted-main-20", population.main, schedules.main),
                                      ("unexecuted-development", population.development, schedules.development)):
            cases[name], audits[name], excerpts[name] = derive(worlds, branches, missing)
        assert not missing[0].exists()
    assert len(cases) == 7
    return dict(kind="Derived course CPU scripted diagnostics/costs; no model, GPU, pilot or empirical findings",
        source_bundle=Path(bundle).name, annotation_rubric="Existing narrow literal xNNN/v1=INTEGER and genuine host receipts; frozen conservative syntax, not a runtime freeze",
        atlas_examples=examples(), cases=cases, independent_original_checks=audits, raw_unchanged_excerpts=excerpts)


def worker_audit(bundle=WORKERS):
    result = {}
    with tempfile.TemporaryDirectory(prefix="course-diagnostic-workers-") as temporary, ZipFile(bundle) as archive:
        root = Path(temporary)
        evidence = json.loads(archive.read("evidence.json"))
        extract(archive, root, ("inputs/population.json", "inputs/schedules.json"))
        population = load_population(root / "inputs/population.json")
        schedules = load_schedules(root / "inputs/schedules.json", population)
        by_world = {w.world_id: w for w in population.main + population.development}
        by_branch = {b.branch_id: b for b in schedules.main + schedules.development}
        for case in evidence["cases"]:
            base = case["directory"]
            selection = json.loads(archive.read(base + "/selection.json"))
            extract(archive, root, [base + "/" + name for name in selection["workers"]])
            paths = tuple(root / base / name for name in selection["workers"])
            worlds = tuple(by_world[name] for name in selection["world_ids"])
            branches = tuple(by_branch[name] for name in selection["branch_ids"])
            _, result[base], _ = derive(worlds, branches, paths, estimands=len({w.development for w in worlds}) == 1)
    assert len(result) == 16
    return result


def native_audit():
    """Original native requests retain measured IDs; no scripted retokenization."""
    bundle = ROOT / "tests/fixtures/course_native_worker_run.zip"
    with tempfile.TemporaryDirectory(prefix="course-diagnostic-native-") as temporary, ZipFile(bundle) as archive:
        root = Path(temporary)
        extract(archive, root, ("inputs/population.json", "inputs/schedules.json", "parent.sqlite", "child.sqlite"))
        population = load_population(root / "inputs/population.json")
        schedules = load_schedules(root / "inputs/schedules.json", population)
        paths = (root / "parent.sqlite", root / "child.sqlite")
        calls, inputs, _, _, _, _ = originals(paths)
        branch_ids = {row["branch_id"] for row in calls.values()}
        bound_branches = []
        for path in paths:
            with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as con:
                con.execute("PRAGMA query_only=ON")
                bound = con.execute("SELECT inputs_json FROM run_inputs WHERE singleton=1").fetchone()
                if bound: bound_branches.extend(json.loads(bound[0])["branches"])
        bound_keys = {tuple(branch[k] for k in ("world_id", "phase", "event", "policy", "replicate")) for branch in bound_branches}
        branches = tuple(branch for branch in schedules.main if branch.branch_id in branch_ids or
            tuple(getattr(branch, k) for k in ("world_id", "phase", "event", "policy", "replicate")) in bound_keys)
        worlds = tuple(world for world in population.main if world.world_id in {branch.world_id for branch in branches})
        actual, audit, _ = derive(worlds, branches, paths, tokenizer=False)
        audit["native_saved_requests"] = 4 * len(inputs)
        audit["native_input_token_counts"] = sum(row["input_tokens"] is not None for row in actual["information"]["communication"])
        audit["nonempty_history_tokens_unavailable_without_matching_tokenizer"] = sum(
            row["history_content_tokens"] is None for row in actual["information"]["communication"] if row.get("history_characters"))
        return audit


def summary(actual):
    return {name: dict(coverage=case["coverage"], rows={key: len(rows) for key, rows in case["information"].items() if isinstance(rows, list)},
        boundary_choices=dict(Counter(str(row["selected_policy"]) for row in case["costs"]["boundary_selections"])),
        selected_available=sum(row["available"] for row in case["costs"]["boundary_selections"]),
        physical=case["costs"]["physical"]) for name, case in actual["cases"].items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    parser.add_argument("--worker-audit", action="store_true")
    parser.add_argument("--native-audit", action="store_true")
    args = parser.parse_args()
    if args.worker_audit:
        print(json.dumps(worker_audit(), sort_keys=True))
        return 0
    if args.native_audit:
        print(json.dumps(native_audit(), sort_keys=True))
        return 0
    actual = reconstruct()
    if args.write_fixture:
        write_evaluation(args.write_fixture, actual)
    else:
        with gzip.open(args.fixture, "rt", encoding="utf-8") as source:
            assert actual == json.load(source), "course diagnostic/cost tables differ from retained expectations"
    print(json.dumps(summary(actual), sort_keys=True))
    print("Course original diagnostics/costs reproduced offline; no inference or empirical result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
