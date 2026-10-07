"""Reconstruct policy costs/rule from accepted original M3 workers, entirely offline."""

import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import tempfile
from zipfile import ZipFile

from recovery.costs import costs_run
from recovery.evaluate import write_evaluation
from recovery.manifests import load_population, load_schedules
from recovery.tasks import Size
from tests.outcome_archive import ROOT, RUN

FIXTURE = ROOT / "tests/fixtures/policy_cost_tables.json.gz"
AS_OF = "2026-10-06T00:00:00+00:00"


def _reconcile(worlds, branches, paths, tables):
    from recovery.accounting import progress_snapshot
    old = progress_snapshot(worlds, branches, paths, now=AS_OF)
    costs = tables["costs"]
    for key, value in old["physical"].items():
        if costs["physical"][key] != value:
            raise AssertionError("M3 physical ledger differs: " + key)
    actual = {r["branch_id"]: r for r in costs["policy_costs"]}
    for row in old["policy_costs"]:
        if any(actual[row["branch_id"]][k] != v for k, v in row.items()):
            raise AssertionError("M3 whole-policy ledger differs: " + row["branch_id"])
    for key in ("allocated_gpu_hours", "partition_seconds", "provider_billing", "allocation_mode"):
        if costs["resources"][key] != old["resources"][key]:
            raise AssertionError("M3 allocation/overhead differs: " + key)
    if costs["delivery_counts"] != old["delivery_counts"]:
        raise AssertionError("M3 committed delivery totals differ")
    old_deliveries = json.loads(json.dumps(old["validated_deliveries"]))
    if {r["delivery_id"]: r for r in costs["validated_deliveries"]} != {r["delivery_id"]: r for r in old_deliveries}:
        raise AssertionError("M3 original deliveries differ")
    if costs["physical"]["attempts"] != old["counts"]["attempts"]:
        raise AssertionError("M3 physical attempts differ")


def reconstruct(bundle=RUN):
    cases = {}
    with tempfile.TemporaryDirectory(prefix="m4-costs-") as directory, ZipFile(bundle) as archive:
        root = Path(directory)
        evidence = json.loads(archive.read("evidence.json"))
        selected = [dict(c, directory=c["directory"].replace("\\", "/"))
                    for c in evidence["cases"].values() if isinstance(c, dict) and "workers" in c]
        names = {f"inputs/{size.value}/{name}.json" for size in Size for name in ("population", "schedules")}
        for case in selected:
            base = case["directory"]
            names.add(base + "/selection.json")
            names.update(base + "/" + name for name in (*case["workers"], *case.get("stopped_workers", ())))
        for name in sorted(names):
            if not (root / name).resolve().is_relative_to(root.resolve()):
                raise ValueError("bundle path leaves extraction directory")
            archive.extract(name, root)
        populations = {size.value: load_population(root / f"inputs/{size.value}/population.json") for size in Size}
        schedules = {size: load_schedules(root / f"inputs/{size}/schedules.json", p) for size, p in populations.items()}
        for case in selected:
            base = case["directory"]
            selection = json.loads((root / base / "selection.json").read_bytes())
            population, saved = populations[selection["size"]], schedules[selection["size"]]
            by_world = {w.world_id: w for w in (*population.main, *population.development)}
            by_branch = {b.branch_id: b for b in (*saved.main, *saved.development)}
            worlds = tuple(by_world[w] for w in selection["world_ids"])
            branches = tuple(by_branch[b] for b in selection["branch_ids"])
            paths = [root / base / name for name in case["workers"]]
            tables = costs_run(worlds, branches, paths, now=AS_OF)
            _reconcile(worlds, branches, paths, tables)
            cases[base] = dict(tables["costs"], coverage=tables["coverage"])
            if "stopped_workers" in case:
                stopped_paths = [root / base / name for name in case["stopped_workers"]]
                stopped = costs_run(worlds, branches, stopped_paths, now=AS_OF)
                _reconcile(worlds, branches, stopped_paths, stopped)
                cases[base + "/stopped"] = dict(stopped["costs"], coverage=stopped["coverage"])
            if base.startswith("test_every_family_"):
                count = 60 if selection["size"] == "target" else 40
                full_worlds, full_branches = population.worlds(count), saved.main_for(population, count)
                full = costs_run(full_worlds, full_branches, paths, now=AS_OF)
                # M3 live status requires its exact bound execution subset.
                # The offline full manifest additionally joins unknown worlds;
                # those cannot add physical work or alter known policy totals.
                for key, value in tables["costs"]["physical"].items():
                    if key not in ("scheduled_generations", "unknown_generations") and full["costs"]["physical"][key] != value:
                        raise AssertionError("unexecuted full population changed physical work")
                known = {r["branch_id"]: r for r in full["costs"]["policy_costs"]}
                if any(known[r["branch_id"]] != r for r in tables["costs"]["policy_costs"]):
                    raise AssertionError("full population changed known whole-policy costs")
                cases[f"full-main-{selection['size']}-{count}"] = dict(full["costs"], coverage=full["coverage"])
    if len(cases) != 16:
        raise AssertionError("all fourteen evidence cases, full schedules and stopped work are required")
    return dict(kind="M4-T04 scripted CPU costs/rule validation; not GPU/model or empirical findings",
                source_bundle=Path(bundle).name, cases=cases)


def summary(tables):
    return {name: dict(coverage=c["coverage"], physical_attempts=c["physical"]["attempts"],
        scheduled_replay_calls=len({cid for row in c["policy_costs"] for cid, gid in zip(row["call_ids"], row["generation_ids"]) if cid != gid}),
        choices=dict(Counter(str(r["selected_policy"]) for r in c["boundary_selections"])),
        available_selected_branches=sum(r["available"] for r in c["boundary_selections"]),
        allocated_gpu_hours=c["resources"]["allocated_gpu_hours"]) for name, c in tables["cases"].items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-bundle", type=Path, default=RUN)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create derived cost evidence")
    args = parser.parse_args()
    actual = reconstruct(args.run_bundle)
    if args.write_fixture:
        write_evaluation(args.write_fixture, actual)
    else:
        with gzip.open(args.fixture, "rt", encoding="utf-8") as source:
            if actual != json.load(source):
                raise AssertionError("offline costs/rule differ from retained expectations")
    print(json.dumps(summary(actual), sort_keys=True))
    print("M3 physical/policy/overhead reconciliation and frozen rule verified offline; no inference.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
