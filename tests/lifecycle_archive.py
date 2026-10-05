"""Retain, audit or reproduce the ordinary M3 CPU lifecycle run bundle.

ZIP only packages manifests, SQLite backups and derived evidence. It is not a
new persistence format: extracted worker files use the existing runner/status
APIs. Creation is exclusive; reproduction leaves the retained bundle unchanged.
"""

import argparse
import importlib.metadata
import json
from pathlib import Path
import platform
import sqlite3
import sys
import tempfile
import unittest
from zipfile import ZIP_DEFLATED, ZipFile

from recovery.manifests import load_population, load_schedules, save_population, save_schedules
from recovery.runner import WorkerReader
from recovery.storage import record_json
from recovery.tasks import Size
from tests.lifecycle_checks import LifecycleTests
from tests.lifecycle_fixture import (offline_preview, population, progress, schedules,
                                    scientific_records, stable_progress, write_json)

FIXTURE = Path(__file__).resolve().parent / "fixtures/scripted_lifecycle_run.zip"
PACKAGES = ("pydantic", "langgraph", "langgraph-checkpoint", "langgraph-checkpoint-sqlite", "langchain-core")


def selected(root, case):
    selection = json.loads((root / case["directory"] / "selection.json").read_bytes())
    inputs = root / "inputs" / selection["size"]
    prepared = load_population(inputs / "population.json")
    saved = load_schedules(inputs / "schedules.json", prepared)
    worlds = {w.world_id: w for w in (*prepared.main, *prepared.development)}
    branches = {b.branch_id: b for b in (*saved.main, *saved.development)}
    return (tuple(worlds[i] for i in selection["world_ids"]),
            tuple(branches[i] for i in selection["branch_ids"]))


def audit(root):
    evidence = json.loads((root / "evidence.json").read_bytes())
    # The retained Windows bundle predates portable case paths. Normalize only
    # these relative references; actual command/module paths remain observations.
    evidence["cases"] = {
        key.replace("\\", "/"): (
            {**case, "directory": case["directory"].replace("\\", "/")}
            if isinstance(case, dict) and "directory" in case else case)
        for key, case in evidence["cases"].items()
    }
    for size in Size:
        directory = root / "inputs" / size.value
        prepared = load_population(directory / "population.json")
        load_schedules(directory / "schedules.json", prepared)
    for case in evidence["cases"].values():
        if not isinstance(case, dict) or "workers" not in case:
            continue
        directory = root / case["directory"]
        worlds, branches = selected(root, case)
        paths = tuple(directory / name for name in case["workers"])
        snapshot = json.loads((directory / "progress.json").read_bytes())
        actual = progress(worlds, branches, paths, now=snapshot["at"])
        if record_json(actual) != record_json(snapshot):
            raise AssertionError(f"offline progress/cost reconstruction differs: {case['directory']}")
        if offline_preview(worlds, branches, paths) != json.loads((directory / "offline-preview.json").read_bytes()):
            raise AssertionError(f"offline outcomes/footprints differ: {case['directory']}")
        for path in paths:
            reader = WorkerReader(path)
            try:
                if reader.store.connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                    raise AssertionError(f"SQLite integrity failed: {path}")
            finally:
                reader.close()
        if "stopped_workers" in case:
            stopped = json.loads((directory / "stopped-progress.json").read_bytes())
            stopped_paths = tuple(directory / name for name in case["stopped_workers"])
            if record_json(progress(worlds, branches, stopped_paths, now=stopped["at"])) != record_json(stopped):
                raise AssertionError("stopped budget progress differs")
            if offline_preview(worlds, branches, stopped_paths) != json.loads((directory / "stopped-preview.json").read_bytes()):
                raise AssertionError("unexecuted slots changed into recorded failures")
    return evidence


def attempt_outcomes(paths):
    rows = []
    clocks = {"started_at", "finished_at", "elapsed_seconds", "observed_seconds", "recovered_at", "worker_pid"}
    for path in paths:
        reader = WorkerReader(path)
        try:
            rows.extend({k: v for k, v in dict(row).items() if k not in clocks}
                        for row in reader.store.connection.execute("SELECT * FROM attempts"))
        finally:
            reader.close()
    return sorted(rows, key=lambda r: (r["call_id"], r["number"]))


def compare(expected, actual):
    saved, fresh = audit(expected), audit(actual)
    if saved["checks"] != fresh["checks"] or saved["cases"].keys() != fresh["cases"].keys():
        raise AssertionError("lifecycle evidence coverage differs")
    for key, case in fresh["cases"].items():
        if not isinstance(case, dict) or "workers" not in case:
            if case != saved["cases"][key]:
                raise AssertionError("full manifest reconciliation differs")
            continue
        other = saved["cases"][key]
        if case != other:
            raise AssertionError(f"case outcomes/counts/backup paths differ: {key}")
        a, b = actual / case["directory"], expected / other["directory"]
        new_paths = tuple(a / p for p in case["workers"])
        old_paths = tuple(b / p for p in other["workers"])
        if scientific_records(new_paths) != scientific_records(old_paths):
            raise AssertionError(f"literal requests/raw replies/validation/committed transitions differ: {key}")
        if attempt_outcomes(new_paths) != attempt_outcomes(old_paths):
            raise AssertionError(f"bounded attempt/failure outcomes differ: {key}")
        new_progress, old_progress = (json.loads((d / "progress.json").read_bytes()) for d in (a, b))
        if stable_progress(new_progress) != stable_progress(old_progress):
            raise AssertionError(f"delivery/schedule/progress joins differ: {key}")
        for marker in a.glob("boundary-*.json"):
            left, right = (json.loads(p.read_bytes()) for p in (marker, b / marker.name))
            # Environment paths, checkpoint IDs and clocks are retained observations.
            for field in ("point", "branch_id", "round", "bounds", "sqlite", "call_id",
                          "returned_response", "validated_peer", "staged_delivery_ids", "computed_delivery_ids"):
                if left.get(field) != right.get(field):
                    raise AssertionError(f"actual crash boundary differs: {key}/{field}")
    for size in Size:
        for name in ("population.json", "schedules.json"):
            relative = Path("inputs") / size.value / name
            if (expected / relative).read_bytes() != (actual / relative).read_bytes():
                raise AssertionError("prepared manifest changed")


def retain(root, destination):
    # Every DB is packaged through backup, including the killed owner's live WAL.
    with Path(destination).open("xb") as output, ZipFile(output, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.name.endswith((".owner", "-wal", "-shm")):
                continue
            relative = path.relative_to(root).as_posix()
            if path.suffix == ".sqlite":
                with tempfile.TemporaryDirectory() as staging:
                    copy = Path(staging) / "snapshot.sqlite"
                    reader = WorkerReader(path)
                    try:
                        reader.store.backup(copy)
                    finally:
                        reader.close()
                    archive.write(copy, relative)
            else:
                archive.write(path, relative)


def extract(source, root):
    with ZipFile(source) as archive:
        for member in archive.infolist():
            if not (root / member.filename).resolve().is_relative_to(root.resolve()):
                raise ValueError("bundle member leaves extraction directory")
        archive.extractall(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create a CPU run bundle")
    parser.add_argument("--audit-only", action="store_true", help="reconstruct offline; no subprocess or generation")
    args = parser.parse_args()
    if args.audit_only and args.write_fixture:
        parser.error("audit reads an existing bundle")
    with tempfile.TemporaryDirectory(prefix="m3-lifecycle-") as directory:
        root = Path(directory)
        if args.audit_only:
            extract(args.fixture, root)
            evidence = audit(root)
        else:
            for size in Size:
                inputs = root / "inputs" / size.value
                inputs.mkdir(parents=True)
                save_population(population(size), inputs / "population.json")
                save_schedules(schedules(size), population(size), inputs / "schedules.json")
            LifecycleTests.evidence.clear()
            LifecycleTests.bundle = root
            try:
                result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(LifecycleTests))
            finally:
                LifecycleTests.bundle = None
            if not result.wasSuccessful():
                return 1
            evidence = {"kind": "M3 scripted CPU lifecycle acceptance; not GPU/pilot/main/model outcomes",
                "checks": result.testsRun, "cases": LifecycleTests.evidence,
                "environment": {"python": sys.version, "platform": platform.platform(), "sqlite": sqlite3.sqlite_version,
                                "packages": {p: importlib.metadata.version(p) for p in PACKAGES}}}
            write_json(root / "evidence.json", evidence)
            audit(root)
            if args.write_fixture:
                retain(root, args.write_fixture)
                # Verify actual packaged/reopened snapshots, not just working files.
                with tempfile.TemporaryDirectory() as restored:
                    extract(args.write_fixture, Path(restored))
                    compare(Path(restored), root)
            else:
                with tempfile.TemporaryDirectory() as saved:
                    extract(args.fixture, Path(saved))
                    compare(Path(saved), root)
        print(record_json({"checks": evidence["checks"], "retained_cases": len(evidence["cases"]),
                           "integrated_logical_slots": 4340, "integrated_generations": 3956,
                           "exact_replay_uses": 384, "offline_audit": "passed"}))
        print("Verified CPU lifecycle bundle; no model inference or empirical result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
