"""Reproduce course uncertainty from original workers and accepted prerequisite joins."""

import argparse
from collections import defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
from zipfile import ZipFile

from recovery.evaluate import write_evaluation
from recovery.manifests import load_population, load_schedules
from recovery.uncertainty import uncertainty_run
from tests.course_analysis_archive import RUN, extract
from tests.course_diagnostics_archive import AS_OF, FIXTURE as PREREQUISITE
from tests.outcome_fixture import ROOT

FIXTURE = ROOT / "tests/fixtures/course_uncertainty_tables.json.gz"
SEED = 20261011


def independent_bounds(branches, tables):
    """Exact rational linear coefficients from accepted atoms and original IDs.

    Tiny nonlinear references live in test_course_uncertainty; this checks every
    eligible linear archive row without calling the production bound functions.
    """
    scheduled = {c.call_id: c.generation_id for b in branches for c in b.calls}
    known = {}
    for row in tables["outcomes"]:
        assert row["generation_id"] == scheduled[row["call_id"]]
        if row["correct"] is not None: known["correct", row["generation_id"]] = Fraction(row["correct"])
    for row in tables["peer_diagnostics"]:
        if row["metric"] == "preservation" and row["denominator"] and row["numerator"] is not None:
            known["preservation", row["generation_id"], tuple(row["eligible_coordinates"])] = Fraction(row["numerator"], row["denominator"])
    bounds = {(r["world_id"], r["estimand"], r["event"], r["endpoint"], r["round"], r["replicate"]): r["sensitivity"]
              for r in tables["uncertainty"]["world_bounds"]}
    checked = 0
    for row in tables["estimands"]["world_contrasts"]:
        for c in row["components"]:
            for a in c["atoms"]: assert a["generation_id"] == scheduled[a["call_id"]]
        if row["eligibility"] != "eligible" or any(c["operator"] == "all" for c in row["components"]): continue
        fixed, coefficients = Fraction(), defaultdict(Fraction)
        for c in row["components"]:
            coefficient = Fraction(str(c["coefficient"]))
            if not c["atoms"]:
                coefficients[c["branch_id"], c["endpoint"], tuple(c["rounds"]), tuple(c["peers"])] += coefficient
            for a in c["atoms"]:
                if a["exact_weight"] is None: continue
                weight = coefficient * Fraction(a["exact_weight"]["numerator"], a["exact_weight"]["denominator"])
                key = ("preservation", a["generation_id"], tuple(a["eligible_coordinates"])) if c["endpoint"] == "preservation" else ("correct", a["generation_id"])
                if key in known: fixed += weight * known[key]
                else: coefficients[key] += weight
        expected = [float(fixed + sum(min(0, v) for v in coefficients.values())),
                    float(fixed + sum(max(0, v) for v in coefficients.values()))]
        actual = bounds[row["world_id"], row["estimand"], row["event"], row["endpoint"], row["round"], row["replicate"]]
        assert actual["method"] == "exact_shared_linear"
        assert all(abs(a - b) < 1e-12 for a, b in zip(expected, actual["interval"])), row["estimand"]
        checked += 1
    return dict(independent_shared_linear_rows=checked, original_scheduled_identities=len(scheduled),
                known_physical_endpoint_constraints=len(known))


def derive(worlds, branches, paths, prerequisite):
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.exists()}
    tables = uncertainty_run(worlds, branches, paths, seed=SEED, now=AS_OF, regime="course")
    # Reuse accepted scoring/cost evidence; do not repeat its raw gold/SQL audits.
    for key in ("coverage", "costs", "peer_diagnostics"):
        assert tables[key] == prerequisite[key], "prerequisite join changed: " + key
    audit = independent_bounds(branches, tables)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in before.items())
    result = dict(tables["uncertainty"], **{k: tables["estimands"][k] for k in
        ("world_contrasts", "repeat_contrasts", "repeatability", "trajectory_changes")})
    return result, audit


def reconstruct(bundle=RUN):
    with gzip.open(PREREQUISITE, "rt", encoding="utf-8") as source: prior = json.load(source)["cases"]
    cases, audits = {}, {}
    with tempfile.TemporaryDirectory(prefix="course-uncertainty-") as temporary, ZipFile(bundle) as archive:
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
            cases[base], audits[base] = derive(worlds, branches, paths, prior[base])
            if "stopped_worker" in case:
                extract(archive, root, [base + "/" + case["stopped_worker"]])
                name = base + "/stopped"
                cases[name], audits[name] = derive(worlds, branches, (root / base / case["stopped_worker"],), prior[name])
            if len(worlds) == 5:
                cases["full-main-20"], audits["full-main-20"] = derive(population.main, schedules.main, paths, prior["full-main-20"])
        missing = (root / "absent.sqlite",)
        for name, worlds, branches in (("unexecuted-main-20", population.main, schedules.main),
                                      ("unexecuted-development", population.development, schedules.development)):
            cases[name], audits[name] = derive(worlds, branches, missing, prior[name])
        assert not missing[0].exists()
    assert len(cases) == 7
    return dict(kind="Exploratory course CPU uncertainty validation; no inference or empirical result",
                source_bundle=Path(bundle).name, cases=cases, independent_checks=audits)


def summary(actual):
    return {name: dict(coverage=case["coverage"], seed=case["settings"]["seed"],
        primaries=[dict(estimand=r["estimand"], independent_worlds=r["intended_population"]["independent_worlds"],
            family_counts=r["family_denominators"], interval=r["intended_population"]["interval"],
            sensitivity=r["sensitivity"]["interval"], paired_coverage=r["paired_coverage"])
            for r in case["summaries"] if r["primary_interval"]],
        incomplete_trajectories=sum(not r["observed"]["complete"] for r in case["world_trajectories"]),
        independent_checks=actual["independent_checks"][name]) for name, case in actual["cases"].items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create derived CPU evidence")
    args = parser.parse_args()
    actual = reconstruct()
    if args.write_fixture: write_evaluation(args.write_fixture, actual)
    else:
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as source: saved = json.load(source)
        assert actual.keys() == saved.keys()
        for name, case in actual["cases"].items():
            for key, value in case.items(): assert value == saved["cases"][name][key], name + "/" + key
        assert actual["independent_checks"] == saved["independent_checks"]
    print(json.dumps(summary(actual), sort_keys=True))
    print("Seven original course scopes reproduce paired bounds and costs; no inference or empirical result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
