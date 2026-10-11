"""Retain/reproduce course CPU workers in the existing manifest/SQLite ZIP layout."""

import argparse
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import sqlite3
import sys
import tempfile
import unittest

from recovery.manifests import load_population, load_schedules
from recovery.runner import WorkerReader
from recovery.storage import record_json
from tests.course_worker_cases import SETTINGS
from tests.course_worker_checks import CourseWorkerTests
from tests.lifecycle_archive import extract, retain
from tests.lifecycle_fixture import progress, scientific_records, stable_progress, write_json

FIXTURE = Path(__file__).resolve().parent / "fixtures/course_worker_run.zip"


def selected(root, case):
    population = load_population(root / "inputs/population.json")
    schedules = load_schedules(root / "inputs/schedules.json", population)
    directory = root / case["directory"]
    selection = json.loads((directory / "selection.json").read_bytes())
    worlds = tuple(w for w in population.main + population.development if w.world_id in selection["world_ids"])
    branches = tuple(b for b in schedules.main + schedules.development if b.branch_id in selection["branch_ids"])
    assert len(worlds) == len(selection["world_ids"]) and len(branches) == len(selection["branch_ids"])
    return directory, worlds, branches, tuple(directory / name for name in selection["workers"])


def audit(root):
    evidence = json.loads((root / "evidence.json").read_bytes())
    counts = dict(cases=0, logical_calls=0, generations=0, attempts=0, replay_uses=0,
                  uncertain_attempts=0, real_kills=0)
    for case in evidence["cases"]:
        directory, worlds, branches, paths = selected(root, case)
        expected = json.loads((directory / "progress.json").read_bytes())
        actual = progress(worlds, branches, paths, settings=SETTINGS, now=expected["at"])
        assert record_json(actual) == record_json(expected), directory
        for path in paths:
            reader = WorkerReader(path)
            try:
                assert reader.store.connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
                assert reader.store.run_inputs["regime"] == "course"
                assert reader.store.run_inputs["settings"] == SETTINGS
            finally:
                reader.close()
        counts["cases"] += 1
        records = actual["counts"]
        counts["logical_calls"] += records["finished_logical"]
        counts["generations"] += records["finished_generations"]
        for key in ("attempts", "replay_uses", "uncertain_attempts"):
            counts[key] += records[key]
        counts["real_kills"] += len(list(directory.glob("kill-*.json")))
    assert counts["real_kills"] == 10
    return counts


def compare(left, right):
    previous, current = (json.loads((root / "evidence.json").read_bytes()) for root in (left, right))
    assert previous["cases"] == current["cases"]
    for case in previous["cases"]:
        a, _, _, old_paths = selected(left, case)
        b, _, _, new_paths = selected(right, case)
        assert scientific_records(old_paths) == scientific_records(new_paths), case
        old, new = (json.loads((p / "progress.json").read_bytes()) for p in (a, b))
        assert stable_progress(old) == stable_progress(new), case
        for path in a.glob("kill-*.json"):
            old_kill, new_kill = (json.loads(p.read_bytes()) for p in (path, b / path.name))
            assert old_kill["point"] == new_kill["point"]
            assert old_kill["inference_children_exited"] and new_kill["inference_children_exited"]
        # Physical attempts are real observations; ignore clocks and process IDs only.
        clocks = {"started_at", "finished_at", "elapsed_seconds", "observed_seconds", "recovered_at", "worker_pid"}
        def attempts(paths):
            rows = []
            for path in paths:
                reader = WorkerReader(path)
                try:
                    rows.extend({k: v for k, v in dict(r).items() if k not in clocks}
                                for r in reader.store.connection.execute("SELECT * FROM attempts"))
                finally:
                    reader.close()
            return sorted(rows, key=lambda r: (r["call_id"], r["number"]))
        assert attempts(old_paths) == attempts(new_paths), case
    for name in ("population.json", "schedules.json"):
        assert (left / "inputs" / name).read_bytes() == (right / "inputs" / name).read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    if args.audit_only and args.write_fixture:
        parser.error("audit reads an existing bundle")
    with tempfile.TemporaryDirectory(prefix="course-workers-") as temporary:
        root = Path(temporary)
        if args.audit_only:
            extract(args.fixture, root)
        else:
            CourseWorkerTests.bundle = root
            CourseWorkerTests.evidence.clear()
            result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName("tests.course_worker_checks"))
            if not result.wasSuccessful(): return 1
            (root / "inputs").mkdir()
            for source, name in (("population_course.json", "population.json"), ("schedules_course.json", "schedules.json")):
                shutil.copyfile(FIXTURE.parent / source, root / "inputs" / name)
            write_json(root / "evidence.json", dict(kind="course CPU worker validation; no model or empirical results",
                environment=dict(python=sys.version, platform=platform.platform(), sqlite=sqlite3.sqlite_version,
                    packages={p: importlib.metadata.version(p) for p in
                        ("pydantic", "langgraph", "langgraph-checkpoint", "langgraph-checkpoint-sqlite", "langchain-core")}),
                cases=sorted(CourseWorkerTests.evidence, key=lambda c: c["directory"])))
        summary = audit(root)
        if args.write_fixture:
            retain(root, args.write_fixture)
        elif not args.audit_only:
            with tempfile.TemporaryDirectory(prefix="course-worker-reference-") as saved:
                extract(args.fixture, Path(saved))
                audit(Path(saved))
                compare(Path(saved), root)
        print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
