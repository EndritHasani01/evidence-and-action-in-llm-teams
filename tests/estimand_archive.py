"""Reproduce M4-T02 contrasts from original M3 workers, without inference."""

import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import tempfile
from zipfile import ZipFile

from recovery.analysis import analyze_run
from recovery.evaluate import write_evaluation
from recovery.manifests import load_population, load_schedules
from tests.outcome_archive import ROOT, RUN

FIXTURE = ROOT / "tests/fixtures/estimand_tables.json.gz"


def reconstruct(bundle=RUN):
    cases = {}
    with tempfile.TemporaryDirectory(prefix="m4-estimands-") as directory, ZipFile(bundle) as archive:
        root = Path(directory)
        evidence = json.loads(archive.read("evidence.json"))
        selected = [case for case in evidence["cases"].values() if isinstance(case, dict) and
            "workers" in case and case["directory"].startswith("test_every_family_")]
        for case in selected:
            base = case["directory"].replace("\\", "/")
            names = [base + "/selection.json", *[base + "/" + name for name in case["workers"]]]
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
            tables = analyze_run(worlds, branches, paths)
            if tables["coverage"]["recorded"] != case["counts"]["finished_logical"]:
                raise AssertionError("retained M3 executed coverage differs")
            cases[base] = dict(tables["estimands"], coverage=tables["coverage"])
            count = 60 if selection["size"] == "target" else 40
            full = analyze_run(population.worlds(count), schedules.main_for(population, count), paths)
            cases[f"full-main-{selection['size']}-{count}"] = dict(full["estimands"], coverage=full["coverage"])
    if len(cases) != 4:
        raise AssertionError("both complete fixtures and full intended manifests are required")
    return {"kind": "M4-T02 derived scripted CPU validation; not model or empirical findings",
            "source_bundle": Path(bundle).name, "cases": cases}


def summary(tables):
    result = {}
    for name, case in tables["cases"].items():
        result[name] = {"coverage": case["coverage"],
            "primary_estimates": [{k: r[k] for k in ("estimand", "value", "scheduled_worlds", "observed_worlds")}
                for r in case["summaries"] if r["primary"] and r["level"] == "all_families"],
            "table_rows": {key: len(value) for key, value in case.items() if isinstance(value, list)},
            "Q_activity": dict(sorted(Counter("unknown" if r["active"] is None else
                "active" if r["active"] else "inactive" for r in case["prose_activity"]).items()))}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-bundle", type=Path, default=RUN)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create derived analysis evidence")
    args = parser.parse_args()
    actual = reconstruct(args.run_bundle)
    if args.write_fixture:
        write_evaluation(args.write_fixture, actual)
    else:
        with gzip.open(args.fixture, "rt", encoding="utf-8") as source:
            if actual != json.load(source):
                raise AssertionError("estimand tables differ from retained expectations")
    print(json.dumps(summary(actual), sort_keys=True))
    print("Offline prespecified CPU estimates verified; no inference or empirical result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
