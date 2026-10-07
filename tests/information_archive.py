"""Reconstruct diagnostics from accepted original workers, never backups or inference."""

import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import tempfile
from zipfile import ZipFile

from recovery.evaluate import write_evaluation
from recovery.information import information_run
from recovery.manifests import load_population, load_schedules
from tests.information_examples import examples
from tests.outcome_archive import ROOT, RUN

FIXTURE = ROOT / "tests/fixtures/information_tables.json.gz"


def reconstruct(bundle=RUN):
    cases = {}
    with tempfile.TemporaryDirectory(prefix="m4-information-") as directory, ZipFile(bundle) as archive:
        root = Path(directory)
        evidence = json.loads(archive.read("evidence.json"))
        selected = [case for case in evidence["cases"].values() if isinstance(case, dict) and
            "workers" in case and (case["directory"].startswith("test_every_family_") or
                                  "budget_stop" in case["directory"])]
        for case in selected:
            base = case["directory"].replace("\\", "/")
            names = [base + "/selection.json", *[base + "/" + name for name in (*case["workers"], *case.get("stopped_workers", ()))]]
            for size in ("target", "fallback"):
                names.extend(f"inputs/{size}/{name}.json" for name in ("population", "schedules"))
            for name in names:
                if not (root / name).resolve().is_relative_to(root.resolve()):
                    raise ValueError("bundle path leaves extraction directory")
                archive.extract(name, root)
            selection = json.loads((root / base / "selection.json").read_bytes())
            population = load_population(root / f"inputs/{selection['size']}/population.json")
            schedules = load_schedules(root / f"inputs/{selection['size']}/schedules.json", population)
            by_world = {w.world_id: w for w in population.main}
            by_branch = {b.branch_id: b for b in schedules.main}
            paths = [root / base / name for name in case["workers"]]
            worlds = tuple(by_world[w] for w in selection["world_ids"])
            branches = tuple(by_branch[b] for b in selection["branch_ids"])
            tables = information_run(worlds, branches, paths)
            if tables["coverage"]["recorded"] != case["counts"]["finished_logical"]:
                raise AssertionError("retained M3 recorded coverage differs")
            cases[base] = dict(tables["information"], coverage=tables["coverage"])
            if "stopped_workers" in case:
                stopped = information_run(worlds, branches, [root / base / name for name in case["stopped_workers"]])
                if stopped["coverage"]["unknown"] != case["stopped_counts"]["unknown_logical"]:
                    raise AssertionError("stopped unknown execution differs")
                cases[base + "/stopped"] = dict(stopped["information"], coverage=stopped["coverage"])
            if base.startswith("test_every_family_"):
                count = 60 if selection["size"] == "target" else 40
                full = information_run(population.worlds(count), schedules.main_for(population, count), paths)
                cases[f"full-main-{selection['size']}-{count}"] = dict(full["information"], coverage=full["coverage"])
    if len(cases) < 4:
        raise AssertionError("both sizes and their full intended populations are required")
    return {"kind": "M4-T03 derived scripted CPU validation; not model or empirical findings",
            "source_bundle": Path(bundle).name, "atlas_examples": examples(), "cases": cases}


def summary(tables):
    return {name: {"coverage": case["coverage"],
        "rows": {key: len(value) for key, value in case.items() if isinstance(value, list)},
        "exposure": dict(sorted(Counter(str(r["owner_v1_exposure"]) for r in case["owner_exposure"]).items())),
        "receipt_timing": dict(sorted(Counter(r["category"] for r in case["receipt_timing"]).items()))}
        for name, case in tables["cases"].items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-bundle", type=Path, default=RUN)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create derived diagnostic evidence")
    args = parser.parse_args()
    actual = reconstruct(args.run_bundle)
    if args.write_fixture:
        write_evaluation(args.write_fixture, actual)
    else:
        with gzip.open(args.fixture, "rt", encoding="utf-8") as source:
            if actual != json.load(source):
                raise AssertionError("information tables differ from retained expectations")
    print(json.dumps(summary(actual), sort_keys=True))
    print("Offline information/reference CPU evidence verified; no inference or empirical result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
