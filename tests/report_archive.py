"""Reproduce every M4 report scope twice from original M3 workers, offline."""

import argparse
import gzip
import json
from pathlib import Path
import tempfile
from zipfile import ZipFile

from recovery.evaluate import write_evaluation
from recovery.manifests import load_population, load_schedules
from recovery.report import report_run, write_report
from recovery.tasks import Size
from tests.cost_archive import AS_OF
from tests.outcome_archive import ROOT, RUN
from tests.test_report_run import audit_links

FIXTURE = ROOT/"tests/fixtures/report_tables.json.gz"
RETAINED_SCOPES = {
    "test_every_family_intervention_control_and_repeat_at_both_sizes/target": "complete-target",
    "test_every_family_intervention_control_and_repeat_at_both_sizes/fallback": "complete-fallback",
    "full-main-target-60": "incomplete-target-60",
    "full-main-fallback-40": "incomplete-fallback-40",
    "test_synthetic_budget_stop_retains_unknown_slots_and_resumes_same_configuration/budget/stopped": "stopped-prefix",
}


def reconstruct(bundle=RUN, *, export=None):
    """Compare complete tables, cases, plotting inputs and every exported byte."""
    cases = {}
    export = Path(export) if export else None
    if export:
        export.mkdir()  # Existing outputs are protected.
    with tempfile.TemporaryDirectory(prefix="m4-report-") as directory, ZipFile(bundle) as archive:
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
        populations = {s.value: load_population(root/f"inputs/{s.value}/population.json") for s in Size}
        schedules = {s: load_schedules(root/f"inputs/{s}/schedules.json", p) for s, p in populations.items()}

        def reproduce(name, worlds, branches, paths, counts):
            before = {path: path.read_bytes() for path in paths}
            provenance = dict(source_bundle=Path(bundle).name, source_scope=name,
                workers=[p.name for p in paths], accounting_as_of=AS_OF)
            left = report_run(worlds, branches, paths, now=AS_OF, provenance=provenance)
            right = report_run(worlds, branches, paths, now=AS_OF, provenance=provenance)
            for key in left:
                if left[key] != right[key]:
                    raise AssertionError("repeated report differs: "+name+"/"+key)
            if any(path.read_bytes() != value for path, value in before.items()):
                raise AssertionError("report changed an original worker: "+name)
            coverage = left["tables"]["coverage"]
            if (coverage["scheduled"], coverage["recorded"], coverage["unknown"]) != counts:
                raise AssertionError("report coverage differs from original M3 scope: "+name)
            first, second = root/"first", root/"second"
            # Unique child directories also keep the operation exclusive.
            first.mkdir(exist_ok=True)
            second.mkdir(exist_ok=True)
            index = str(len(cases))
            write_report(first/index, left)
            write_report(second/index, right)
            for path in (first/index).iterdir():
                if path.read_bytes() != (second/index/path.name).read_bytes():
                    raise AssertionError("repeated export bytes differ: "+name+"/"+path.name)
            links = audit_links(first/index)
            if export and name in RETAINED_SCOPES:
                write_report(export/RETAINED_SCOPES[name], left)
            # Compare the public JSON shape, including BFS endpoint arrays from
            # immutable dataclass tuples. Raw strings remain unchanged.
            cases[name] = dict(report=json.loads(json.dumps(left["report"], ensure_ascii=True, allow_nan=False)), links_checked=links,
                table_rows={key: len(value) for key, value in left["tables"].items() if isinstance(value, list)},
                repeated_outputs=sorted(p.name for p in (first/index).iterdir()))
            print(f"Verified twice: {name}; {coverage['recorded']}/{coverage['scheduled']} recorded, {coverage['unknown']} unknown.", flush=True)

        for case in selected:
            base = case["directory"]
            selection = json.loads((root/base/"selection.json").read_bytes())
            population, saved = populations[selection["size"]], schedules[selection["size"]]
            by_world = {w.world_id: w for w in (*population.main, *population.development)}
            by_branch = {b.branch_id: b for b in (*saved.main, *saved.development)}
            worlds = tuple(by_world[w] for w in selection["world_ids"])
            branches = tuple(by_branch[b] for b in selection["branch_ids"])
            paths = [root/base/name for name in case["workers"]]
            counts = case["counts"]
            reproduce(base, worlds, branches, paths,
                (counts["scheduled_logical"], counts["finished_logical"], counts["unknown_logical"]))
            if "stopped_workers" in case:
                counts = case["stopped_counts"]
                reproduce(base+"/stopped", worlds, branches, [root/base/name for name in case["stopped_workers"]],
                    (counts["scheduled_logical"], counts["finished_logical"], counts["unknown_logical"]))
            if base.startswith("test_every_family_"):
                count = 60 if selection["size"] == "target" else 40
                total = 17656 if count == 60 else 12560
                reproduce(f"full-main-{selection['size']}-{count}", population.worlds(count),
                    saved.main_for(population, count), paths, (total, 2170, total-2170))
    if len(cases) != 16:
        raise AssertionError("all original selections, full populations and stopped work are required")
    return dict(kind="M4-T06 synthetic CPU report validation; not empirical findings",
        source_bundle=Path(bundle).name, accounting_as_of=AS_OF, cases=cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-bundle", type=Path, default=RUN)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    parser.add_argument("--export", type=Path, help="new directory containing five complete/incomplete portable reports")
    args = parser.parse_args()
    actual = reconstruct(args.run_bundle, export=args.export)
    if args.write_fixture:
        write_evaluation(args.write_fixture, actual)
    else:
        with gzip.open(args.fixture, "rt", encoding="utf-8") as source:
            expected = json.load(source)
        for name, case in actual["cases"].items():
            if case != expected["cases"][name]:
                raise AssertionError("retained report differs: "+name)
    print(json.dumps({name: dict(coverage=case["report"]["coverage"],
        selected_ids=[r["world_id"] for r in case["report"]["cases"]],
        exhibits=len(case["report"]["exhibits"]), links=case["links_checked"]) for name, case in actual["cases"].items()}, sort_keys=True))
    print("All sixteen scopes reproduce every table, case, plotting input and exported byte twice; original workers remain unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
