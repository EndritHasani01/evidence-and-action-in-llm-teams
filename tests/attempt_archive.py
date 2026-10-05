"""Run bounded CPU failure checks and retain their derived traces/measurements."""

import argparse
import gzip
import importlib.metadata
import json
from pathlib import Path
import platform
import sqlite3
import sys
import unittest

from recovery.storage import record_json
from tests.attempt_checks import ProcessAttemptTests


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "attempt_failure_traces.json.gz"


def stable_cases(archive):
    """Compare scientific records exactly; clocks/PIDs remain measured evidence."""
    result = []
    for case in archive["cases"]:
        attempts = [{k: v for k, v in attempt.items() if k not in (
            "started_at", "finished_at", "elapsed_seconds", "observed_seconds", "recovered_at", "worker_pid")
                    and not (k == "peak_memory_bytes" and v is None)}
            for attempt in case["attempts"]]
        result.append({"case": case["case"], "calls": case["calls"], "attempts": attempts,
                       "state": case["state"]})
    return result


def summary(archive):
    attempts = [a for c in archive["cases"] for a in c["attempts"]]
    timeouts = [a for a in attempts if a["termination_reason"] == "attempt_timeout"]
    return {"cases": len(archive["cases"]), "attempts": len(attempts),
        "uncertain_completion": sum(a["uncertain_completion"] for a in attempts),
        "unknown_end_times": sum(a["elapsed_seconds"] is None for a in attempts),
        "confirmed_hung_timeouts": len(timeouts),
        "timeout_excess_seconds": [a["elapsed_seconds"] - a["timeout_seconds"] for a in timeouts],
        "process_intervals": sum(len(c["processes"]) for c in archive["cases"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    args = parser.parse_args()
    ProcessAttemptTests.evidence.clear()
    suite = unittest.defaultTestLoader.loadTestsFromName("tests.attempt_checks")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    archive = {"kind": "bounded CPU subprocess protocol evidence; not model or empirical outcomes",
        "environment": {"python": sys.version, "platform": platform.platform(),
            "sqlite": sqlite3.sqlite_version, "packages": {p: importlib.metadata.version(p) for p in
                ("pydantic", "langgraph", "langgraph-checkpoint", "langgraph-checkpoint-sqlite", "langchain-core")}},
        "cases": sorted(ProcessAttemptTests.evidence, key=lambda c: c["case"])}
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            output.write(gzip.compress((record_json(archive) + "\n").encode("utf-8"), mtime=0))
    else:
        saved = json.loads(gzip.decompress(args.fixture.read_bytes()))
        if stable_cases(archive) != stable_cases(saved):
            raise AssertionError("failure archive's exact calls/attempt outcomes/committed states differ")
    print(json.dumps(summary(archive), sort_keys=True))
    print("Verified bounded CPU failure records; timings are measurements, not inference forecasts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
