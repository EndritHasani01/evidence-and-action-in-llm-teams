"""Ordinary portable course accounting/lifecycle bundle; exclusive creation."""

import argparse
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from recovery.accounting import progress_snapshot
from recovery.storage import record_json
from tests.course_accounting_checks import independent_records
from tests.course_intervention_cases import course_inputs
from tests.course_lifecycle_checks import CourseLifecycleTests
from tests.course_worker_archive import compare, selected
from tests.lifecycle_archive import extract, retain
from tests.lifecycle_fixture import offline_preview, write_json

FIXTURE = Path(__file__).resolve().parent / "fixtures/course_lifecycle_run.zip"


def audit(root):
    evidence = json.loads((root / "evidence.json").read_bytes())
    counts = dict(cases=0, logical_calls=0, generations=0, attempts=0, replay_uses=0, uncertain_attempts=0)
    for case in evidence["cases"]:
        directory, worlds, branches, paths = selected(root, case)
        expected = json.loads((directory / "progress.json").read_bytes())
        actual = progress_snapshot(worlds, branches, paths, now=expected["at"], regime="course")
        assert record_json(actual) == record_json(expected), case
        assert independent_records(worlds, branches, paths, actual) == case["independent_counts"]
        assert offline_preview(worlds, branches, paths) == json.loads((directory / "offline-preview.json").read_bytes())
        copies = tuple(directory / name for name in json.loads((directory / "backup-workers.json").read_bytes()))
        assert record_json(progress_snapshot(worlds, branches, copies, now=expected["at"], regime="course")) == record_json(expected)
        if "stopped_worker" in case:
            stopped = json.loads((directory / "stopped-progress.json").read_bytes())
            actual_stop = progress_snapshot(worlds, branches, (directory / case["stopped_worker"],), now=stopped["at"], regime="course")
            assert record_json(actual_stop) == record_json(stopped)
            independent_records(worlds, branches, (directory / case["stopped_worker"],), actual_stop)
            assert actual_stop["counts"]["unknown_logical"] == 16 and actual_stop["counts"]["recorded_failures"] == 0
        counts["cases"] += 1
        counts["logical_calls"] += actual["counts"]["finished_logical"]
        counts["generations"] += actual["counts"]["finished_generations"]
        for key in ("attempts", "replay_uses", "uncertain_attempts"):
            counts[key] += actual["counts"][key]
    p, s = course_inputs()
    reconciliation = []
    for worlds, branches, expected in ((p.main, s.main, (5752, 6280)), (p.development, s.development, (1114, 1178))):
        snapshot = progress_snapshot(worlds, branches, (root / "absent.sqlite",), regime="course")
        assert (snapshot["counts"]["scheduled_generations"], snapshot["counts"]["scheduled_logical"]) == expected
        assert snapshot["counts"]["unknown_logical"] == expected[1] and snapshot["counts"]["attempts"] == 0
        reconciliation.append(snapshot["counts"])
    assert not (root / "absent.sqlite").exists()
    assert reconciliation == evidence["full_schedule_reconciliation"]
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    if args.audit_only and args.write_fixture: parser.error("audit reads an existing bundle")
    with tempfile.TemporaryDirectory(prefix="course-lifecycle-") as temporary:
        root = Path(temporary)
        if args.audit_only:
            extract(args.fixture, root)
        else:
            (root / "inputs").mkdir()
            for source, name in (("population_course.json", "population.json"), ("schedules_course.json", "schedules.json")):
                shutil.copyfile(FIXTURE.parent / source, root / "inputs" / name)
            CourseLifecycleTests.bundle = root
            CourseLifecycleTests.evidence.clear()
            try:
                result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName("tests.course_lifecycle_checks"))
            finally:
                CourseLifecycleTests.bundle = None
            if not result.wasSuccessful(): return 1
            p, s = course_inputs()
            full = [progress_snapshot(worlds, branches, (root / "absent.sqlite",), regime="course")["counts"]
                    for worlds, branches in ((p.main, s.main), (p.development, s.development))]
            write_json(root / "evidence.json", dict(kind="course CPU scripted accounting/lifecycle; no empirical population coverage",
                environment=dict(python=sys.version, platform=platform.platform(), sqlite=sqlite3.sqlite_version,
                    packages={p: importlib.metadata.version(p) for p in
                        ("pydantic", "langgraph", "langgraph-checkpoint", "langgraph-checkpoint-sqlite", "langchain-core")}),
                prerequisite_crashes="course_worker_run.zip: ten real kills, independently reconstructed by course_accounting_checks",
                full_schedule_reconciliation=full, cases=sorted(CourseLifecycleTests.evidence, key=lambda c: c["directory"])))
        summary = audit(root)
        if args.write_fixture:
            retain(root, args.write_fixture)
            with tempfile.TemporaryDirectory(prefix="course-portable-") as restored:
                extract(args.write_fixture, Path(restored))
                compare(Path(restored), root)
            # An independent process reads the actual packaged ordinary snapshots.
            subprocess.run([sys.executable, "-X", "utf8", "-m", "tests.course_lifecycle_archive", "--fixture", str(args.write_fixture.resolve()), "--audit-only"], check=True)
        elif not args.audit_only:
            with tempfile.TemporaryDirectory(prefix="course-reference-") as reference:
                extract(args.fixture, Path(reference))
                audit(Path(reference))
                compare(Path(reference), root)
        print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
