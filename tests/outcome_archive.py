"""Reproduce M4-T01 tables from ordinary retained M3 files, entirely offline.

No providers, runner, checkpoints or tokenizer are imported. Accepted workers
are selected by M3 evidence; backups/baselines are separate copies, never joined.
"""

import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import tempfile
from zipfile import ZipFile

from recovery.evaluate import evaluate_run, write_evaluation
from recovery.manifests import load_population, load_schedules
from recovery.tasks import Size

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "tests/fixtures/scripted_lifecycle_run.zip"
FIXTURE = ROOT / "tests/fixtures/exact_outcome_tables.json.gz"


def reconstruct(bundle=RUN):
    tables = {}
    with tempfile.TemporaryDirectory(prefix="m4-outcomes-") as directory, ZipFile(bundle) as archive:
        root = Path(directory)
        evidence = json.loads(archive.read("evidence.json"))
        cases = [dict(case, directory=case["directory"].replace("\\", "/"))
                 for case in evidence["cases"].values() if isinstance(case, dict) and "workers" in case]
        names = {f"inputs/{size.value}/{name}.json" for size in Size for name in ("population", "schedules")}
        for case in cases:
            base = case["directory"]
            names.add(base + "/selection.json")
            names.update(base + "/" + name for name in (*case["workers"], *case.get("stopped_workers", ())))
        for name in sorted(names):
            if not (root / name).resolve().is_relative_to(root.resolve()):
                raise ValueError("bundle path leaves extraction directory")
            archive.extract(name, root)
        prepared = {size.value: load_population(root / f"inputs/{size.value}/population.json") for size in Size}
        schedules = {size: load_schedules(root / f"inputs/{size}/schedules.json", population)
                     for size, population in prepared.items()}
        for case in cases:
            base = case["directory"]
            selection = json.loads((root / base / "selection.json").read_bytes())
            population, saved = prepared[selection["size"]], schedules[selection["size"]]
            by_world = {w.world_id: w for w in (*population.main, *population.development)}
            by_branch = {b.branch_id: b for b in (*saved.main, *saved.development)}
            worlds = tuple(by_world[w] for w in selection["world_ids"])
            branches = tuple(by_branch[b] for b in selection["branch_ids"])
            paths = [root / base / name for name in case["workers"]]
            result = evaluate_run(worlds, branches, paths)
            if (result["coverage"]["scheduled"] != case["counts"]["scheduled_logical"]
                    or result["coverage"]["recorded"] != case["counts"]["finished_logical"]
                    or result["coverage"]["unknown"] != case["counts"]["unknown_logical"]):
                raise AssertionError(f"M3 coverage differs: {base}")
            tables[base] = result
            if "stopped_workers" in case:
                result = evaluate_run(worlds, branches, [root / base / name for name in case["stopped_workers"]])
                if result["coverage"]["unknown"] != case["stopped_counts"]["unknown_logical"]:
                    raise AssertionError("stopped unknown execution differs")
                tables[base + "/stopped"] = result
            if base.startswith("test_every_family_"):
                # Retain the frozen population, including every unexecuted world.
                count = 60 if selection["size"] == "target" else 40
                full = evaluate_run(population.worlds(count), saved.main_for(population, count), paths)
                expected_slots = 17656 if count == 60 else 12560
                if full["coverage"]["scheduled"] != expected_slots or full["coverage"]["recorded"] != 2170:
                    raise AssertionError("full main schedule lost known or unknown slots")
                tables[f"full-main-{selection['size']}-{count}"] = full
    return {"kind": "M4-T01 scripted CPU validation tables; not model, pilot or empirical findings",
            "source_bundle": Path(bundle).name, "cases": tables}


def summary(tables):
    return {name: {"coverage": case["coverage"], "trajectory_categories": dict(sorted(Counter(
        row["category"] for row in case["trajectories"]).items())),
        "table_rows": {key: len(value) for key, value in case.items() if isinstance(value, list)}}
        for name, case in tables["cases"].items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-bundle", type=Path, default=RUN)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create derived validation tables")
    args = parser.parse_args()
    actual = reconstruct(args.run_bundle)
    if args.write_fixture:
        write_evaluation(args.write_fixture, actual)
    else:
        with gzip.open(args.fixture, "rt", encoding="utf-8") as source:
            saved = json.load(source)
        if actual != saved:
            raise AssertionError("offline tables differ from retained expectations")
    print(json.dumps(summary(actual), sort_keys=True))
    print("Exact offline CPU tables verified; no generation or empirical result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
