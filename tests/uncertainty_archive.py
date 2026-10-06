"""Reconstruct paired uncertainty/coverage from the original M3 ordinary workers."""

import argparse
import gzip
import json
from pathlib import Path
import tempfile
from zipfile import ZipFile

from recovery.evaluate import write_evaluation
from recovery.manifests import load_population, load_schedules
from recovery.tasks import Size
from recovery.uncertainty import DEFAULT_SEED, uncertainty_run
from tests.cost_archive import AS_OF
from tests.outcome_archive import ROOT, RUN

FIXTURE = ROOT/"tests/fixtures/uncertainty_tables.json.gz"


def reconstruct(bundle=RUN):
    cases = {}
    with tempfile.TemporaryDirectory(prefix="m4-uncertainty-") as directory, ZipFile(bundle) as archive:
        root = Path(directory)
        evidence = json.loads(archive.read("evidence.json"))
        selected = [dict(c, directory=c["directory"].replace("\\", "/"))
                    for c in evidence["cases"].values() if isinstance(c, dict) and "workers" in c]
        names = {f"inputs/{size.value}/{name}.json" for size in Size for name in ("population", "schedules")}
        for case in selected:
            base = case["directory"]
            names.add(base+"/selection.json")
            names.update(base+"/"+name for name in (*case["workers"], *case.get("stopped_workers", ())))
        for name in sorted(names):
            if not (root/name).resolve().is_relative_to(root.resolve()):
                raise ValueError("bundle path leaves extraction directory")
            archive.extract(name, root)
        populations = {size.value: load_population(root/f"inputs/{size.value}/population.json") for size in Size}
        schedules = {size: load_schedules(root/f"inputs/{size}/schedules.json", p) for size, p in populations.items()}
        def analyze(worlds, branches, paths):
            before = {path: path.read_bytes() for path in paths}
            tables = uncertainty_run(worlds, branches, paths, now=AS_OF, seed=DEFAULT_SEED)
            if any(path.read_bytes() != value for path, value in before.items()):
                raise AssertionError("uncertainty analysis changed an original worker")
            return dict(tables["uncertainty"], world_contrasts=tables["estimands"]["world_contrasts"],
                repeat_contrasts=tables["estimands"]["repeat_contrasts"],
                repeatability=tables["estimands"]["repeatability"], trajectory_changes=tables["estimands"]["trajectory_changes"])
        for case in selected:
            base = case["directory"]
            selection = json.loads((root/base/"selection.json").read_bytes())
            population, saved = populations[selection["size"]], schedules[selection["size"]]
            by_world = {w.world_id: w for w in (*population.main, *population.development)}
            by_branch = {b.branch_id: b for b in (*saved.main, *saved.development)}
            worlds = tuple(by_world[w] for w in selection["world_ids"])
            branches = tuple(by_branch[b] for b in selection["branch_ids"])
            paths = [root/base/name for name in case["workers"]]
            cases[base] = analyze(worlds, branches, paths)
            if cases[base]["coverage"]["recorded"] != case["counts"]["finished_logical"]:
                raise AssertionError("uncertainty coverage differs from original M3 execution")
            if "stopped_workers" in case:
                cases[base+"/stopped"] = analyze(worlds, branches, [root/base/name for name in case["stopped_workers"]])
            if base.startswith("test_every_family_"):
                count = 60 if selection["size"] == "target" else 40
                cases[f"full-main-{selection['size']}-{count}"] = analyze(population.worlds(count),
                    saved.main_for(population, count), paths)
    if len(cases) != 16:
        raise AssertionError("all original selections, full populations and stopped work are required")
    return dict(kind="M4-T05 scripted CPU uncertainty validation; not model/pilot/empirical effects",
        source_bundle=Path(bundle).name, cases=cases)


def summary(tables):
    return {name: dict(coverage=case["coverage"], resampling_seed=case["settings"]["seed"],
        primaries=[dict(estimand=r["estimand"], family_denominators=r["family_denominators"],
            observed_worlds=r["observed_worlds"], interval=r["intended_population"]["interval"],
            sensitivity=r["sensitivity"]["interval"], complete_case_interval=r["complete_case_description"]["interval"])
            for r in case["summaries"] if r["primary_interval"]],
        incomplete_trajectories=sum(not r["observed"]["complete"] for r in case["world_trajectories"]),
        paired_policy_worlds=len(case["policy_world_displays"])) for name, case in tables["cases"].items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-bundle", type=Path, default=RUN)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create derived uncertainty evidence")
    args = parser.parse_args()
    actual = reconstruct(args.run_bundle)
    if args.write_fixture:
        write_evaluation(args.write_fixture, actual)
    else:
        with gzip.open(args.fixture, "rt", encoding="utf-8") as source:
            if actual != json.load(source):
                raise AssertionError("paired uncertainty/coverage differs from retained evidence")
    print(json.dumps(summary(actual), sort_keys=True))
    print("All paired intervals, fixed populations, shared sensitivity and original workers reproduce offline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
