"""Reproduce course outcomes/contrasts from original M3 SQLite files, offline."""

import argparse
from collections import Counter
from contextlib import closing
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
from zipfile import ZipFile

from recovery.analysis import analyze_estimands, analyze_run
from recovery.evaluate import evaluate_run, write_evaluation
from recovery.manifests import load_population, load_schedules
from tests.outcome_fixture import ROOT
from tests.references import numeric_reference, relaxation_distances

RUN = ROOT / "tests/fixtures/course_lifecycle_run.zip"
WORKERS = ROOT / "tests/fixtures/course_worker_run.zip"
FIXTURE = ROOT / "tests/fixtures/course_analysis_tables.json.gz"


def extract(archive, root, names):
    for name in sorted(set(names)):
        if not (root / name).resolve().is_relative_to(root.resolve()):
            raise ValueError("archive path leaves extraction directory")
        archive.extract(name, root)


def independent_checks(worlds, branches, paths, actual):
    """Raw SQLite replies + independent insertion/relaxation gold and formulas.

    No production scorer, solver, endpoint, contrast or record reader is used.
    Accepted M1 event application supplies the immutable event-specific world.
    """
    records = {}
    for path in paths:
        if not path.exists():
            continue
        with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as con:
            con.row_factory = sqlite3.Row
            con.execute("PRAGMA query_only=ON")
            for row in con.execute("SELECT * FROM calls"):
                assert row["call_id"] not in records
                records[row["call_id"]] = dict(row)
    by_world = {w.world_id: w for w in worlds}
    scored, cells = {}, {}
    for branch in branches:
        prepared = by_world[branch.world_id]
        world = prepared.world if branch.event == "original" else prepared.event_world(branch.event)
        family = branch.task.value
        if family == "bfs_distance":
            full = relaxation_distances(8, [r.value for r in world.records if not r.deleted])
        else:
            ordered = world.records if family == "top_k" else sorted(world.records, key=lambda r: r.position)
            full = numeric_reference(family, [r.value for r in ordered])
        for call in branch.calls:
            saved = records.get(call.call_id)
            value = None
            if saved and saved["status"] not in ("pending", "running"):
                physical = records.get(call.generation_id)
                assert physical is not None and physical["replay_parent"] is None
                validation = json.loads(saved["validation_json"]) if saved["validation_json"] else None
                if physical["status"] in ("timeout", "infrastructure_failure") or validation["candidate"]["status"] == "invalid":
                    value = 0
                else:
                    raw = json.loads(physical["raw_json"])
                    answer = json.loads(raw["text"])["candidate"]
                    gold = full
                    if family in ("prefix_sum", "distributed_sort") and call.peer is not None:
                        gold = full[6 * call.peer:6 * (call.peer + 1)]
                    value = int(answer == gold)
            scored[call.call_id] = value
        cells[branch.world_id, branch.event, branch.policy, branch.replicate] = branch
    assert {r["call_id"]: r["correct"] for r in actual["outcomes"]} == scored

    def mean(branch, peers=(0, 1, 2, 3), rounds=(1, 2, 3, 4)):
        if branch is None:
            return None
        values = [scored[c.call_id] for c in branch.calls if c.peer in peers and c.round_number in rounds]
        return None if any(v is None for v in values) else Fraction(sum(values), len(values))

    trajectories = {r["branch_id"]: r for r in actual["trajectories"]}
    for branch in branches:
        if branch.phase == "control":
            continue
        row = trajectories[branch.branch_id]
        auc = mean(branch)
        assert row["auc"] == (None if auc is None else float(auc))
        final = [scored[c.call_id] for c in branch.calls if c.round_number == 4]
        assert row["final_joint"] == (None if any(v is None for v in final) else int(all(final)))
    counts = {"scheduled": len(scored), "recorded": sum(v is not None for v in scored.values()),
              "unknown": sum(v is None for v in scored.values()), "correct": sum(v or 0 for v in scored.values())}
    if "estimands" not in actual:
        return counts  # A mixed-domain controls-only ledger is checked slot by slot.
    contrasts = actual["estimands"]["world_contrasts"]
    for world in worlds:
        def cell(event, policy): return cells.get((world.world_id, event, policy, 0))
        aucs = [mean(cell(event, policy)) for event, policy in (("revision", "C"), ("revision", "B"), ("sham", "C"), ("sham", "B"))]
        theta = None if any(v is None for v in aucs) else aucs[0] - aucs[1] - aucs[2] + aucs[3]
        G, H = world.partition
        focal = [mean(cell("revision", policy), peers, (2, 3, 4)) for policy, peers in (("P_H", G), ("B", G), ("P_G", H), ("B", H))]
        phi = None if any(v is None for v in focal) else (focal[0] - focal[1] + focal[2] - focal[3]) / 2
        for name, endpoint, value in (("theta", "auc", theta), ("E_keep", "collaborator_accuracy", phi)):
            row = next(r for r in contrasts if r["world_id"] == world.world_id and r["estimand"] == name and r["endpoint"] == endpoint)
            assert row["value"] == (None if value is None else float(value))
    return counts


def reconstruct(bundle=RUN):
    cases, audits, original_workers = {}, {}, {}
    with tempfile.TemporaryDirectory(prefix="course-analysis-") as temporary, ZipFile(bundle) as archive:
        root = Path(temporary)
        evidence = json.loads(archive.read("evidence.json"))
        names = ["inputs/population.json", "inputs/schedules.json"]
        for case in evidence["cases"]:
            base = case["directory"]
            selection = json.loads(archive.read(base + "/selection.json"))
            names.extend([base + "/selection.json", *[base + "/" + name for name in selection["workers"]]])
            if "stopped_worker" in case: names.append(base + "/" + case["stopped_worker"])
        extract(archive, root, names)
        population = load_population(root / "inputs/population.json")
        schedules = load_schedules(root / "inputs/schedules.json", population)
        by_world = {w.world_id: w for w in population.main + population.development}
        by_branch = {b.branch_id: b for b in schedules.main + schedules.development}
        for case in evidence["cases"]:
            base = case["directory"]
            selection = json.loads((root / base / "selection.json").read_bytes())
            worlds = tuple(by_world[name] for name in selection["world_ids"])
            branches = tuple(by_branch[name] for name in selection["branch_ids"])
            paths = tuple(root / base / name for name in selection["workers"])
            for path in paths: original_workers[path] = hashlib.sha256(path.read_bytes()).hexdigest()
            result = analyze_run(worlds, branches, paths)
            audits[base] = independent_checks(worlds, branches, paths, result)
            assert audits[base]["recorded"] == case["independent_counts"]["finished_logical"]
            cases[base] = result
            if "stopped_worker" in case:
                stopped = (root / base / case["stopped_worker"],)
                original_workers[stopped[0]] = hashlib.sha256(stopped[0].read_bytes()).hexdigest()
                cases[base + "/stopped"] = analyze_run(worlds, branches, stopped)
                audits[base + "/stopped"] = independent_checks(worlds, branches, stopped, cases[base + "/stopped"])
                assert audits[base + "/stopped"]["unknown"] == 16
            if len(worlds) == 5:
                cases["full-main-20"] = analyze_run(population.main, schedules.main, paths)
                audits["full-main-20"] = independent_checks(population.main, schedules.main, paths, cases["full-main-20"])
        missing = (root / "absent.sqlite",)
        for name, worlds, branches in (("unexecuted-main-20", population.main, schedules.main),
                                      ("unexecuted-development", population.development, schedules.development)):
            cases[name] = analyze_run(worlds, branches, missing)
            audits[name] = independent_checks(worlds, branches, missing, cases[name])
        assert not missing[0].exists()
        assert all(hashlib.sha256(path.read_bytes()).hexdigest() == before for path, before in original_workers.items())
    assert len(cases) == 7
    return {"kind": "Derived course CPU scripted outcomes/estimands; no empirical effects or population execution",
            "source_bundle": Path(bundle).name, "cases": cases, "independent_raw_checks": audits}


def worker_audit(bundle=WORKERS):
    """Score each intact prerequisite scope; backups/baselines are never pooled."""
    result = {}
    with tempfile.TemporaryDirectory(prefix="course-analysis-workers-") as temporary, ZipFile(bundle) as archive:
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
            before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]
            worlds = tuple(by_world[name] for name in selection["world_ids"])
            branches = tuple(by_branch[name] for name in selection["branch_ids"])
            if len({w.development for w in worlds}) > 1:
                assert all(b.phase == "control" for b in branches)
                actual = evaluate_run(worlds, branches, paths)
                try:
                    analyze_estimands(worlds, branches, actual)
                except ValueError:
                    pass
                else:
                    raise AssertionError("main/development domains must never be pooled for estimands")
            else:
                actual = analyze_run(worlds, branches, paths)
            result[base] = independent_checks(worlds, branches, paths, actual)
            assert [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths] == before
    assert len(result) == 16
    return result


def summary(actual):
    return {name: {"coverage": case["coverage"],
        "primary_estimates": [{k: row[k] for k in ("estimand", "value", "scheduled_worlds", "observed_worlds", "family_denominators")}
            for row in case["estimands"]["summaries"] if row["primary"] and row["level"] == "all_families"],
        "rows": {key: len(value) for key, value in case["estimands"].items() if isinstance(value, list)},
        "Q_activity": dict(Counter("unknown" if row["active"] is None else "active" if row["active"] else "inactive"
            for row in case["estimands"]["prose_activity"]))} for name, case in actual["cases"].items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    parser.add_argument("--worker-audit", action="store_true")
    args = parser.parse_args()
    if args.worker_audit:
        print(json.dumps(worker_audit(), sort_keys=True))
        return 0
    actual = reconstruct()
    if args.write_fixture:
        write_evaluation(args.write_fixture, actual)
    else:
        with gzip.open(args.fixture, "rt", encoding="utf-8") as source:
            assert actual == json.load(source), "course analysis tables differ from retained expectations"
    print(json.dumps(summary(actual), sort_keys=True))
    print("Course offline CPU outcomes/estimands reproduced; no inference or empirical result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
