"""Execute CPU worker checks and retain/reproduce derived cross-worker traces."""

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
from tests.worker_checks import SchedulingTests

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "worker_scheduling_traces.json.gz"


def stable_cases(archive):
    """Worker placement, clocks/PIDs/module paths may vary; scientific data may not."""
    cases = []
    clocks = {"started_at", "finished_at", "elapsed_seconds", "observed_seconds", "recovered_at", "worker_pid"}
    for case in archive["cases"]:
        calls = sorted((row for w in case["workers"] for row in w["calls"]), key=lambda r: r["call_id"])
        inputs = sorted((row for w in case["workers"] for row in w["round_inputs"]),
                        key=lambda r: (r["branch_id"], r["round_number"]))
        attempts = sorted(({k: v for k, v in row.items() if k not in clocks}
                           for w in case["workers"] for row in w["attempts"]), key=lambda r: (r["call_id"], r["number"]))
        instrumentation = sorted(record_json({k: e[k] for k in
            ("seed", "rng_probe", "view", "rendered", "tokenized", "settings")})
            for w in case["workers"] for e in w["instrumentation"] if e["event"] == "generation")
        cases.append({"case": case["case"], "calls": calls, "round_inputs": inputs, "attempts": attempts,
            "states": case["states"], "instrumentation": instrumentation,
            "held_before_interruption": case.get("held_before_interruption"),
            "committed_before_interruption": case.get("committed_before_interruption")})
    # JSON is the retained representation: dataclass tuples serialize as arrays.
    # Normalize the fresh in-memory export before comparing with parsed JSON.
    return json.loads(record_json(cases))


def summary(archive):
    workers = [w for case in archive["cases"] for w in case["workers"]]
    return {"cases": len(archive["cases"]), "logical_calls": sum(len(w["calls"]) for w in workers),
        "replay_uses": sum(r["replay_parent"] is not None for w in workers for r in w["calls"]),
        "attempts": sum(len(w["attempts"]) for w in workers),
        "uncertain_completions": sum(a["uncertain_completion"] for w in workers for a in w["attempts"]),
        "process_intervals": sum(len(w["processes"]) for w in workers)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    args = parser.parse_args()
    SchedulingTests.evidence.clear()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName("tests.worker_checks"))
    if not result.wasSuccessful():
        return 1
    archive = {"kind": "two-worker CPU scripted protocol evidence; not model or empirical outcomes",
        "environment": {"python": sys.version, "platform": platform.platform(), "sqlite": sqlite3.sqlite_version,
            "packages": {p: importlib.metadata.version(p) for p in
                ("pydantic", "langgraph", "langgraph-checkpoint", "langgraph-checkpoint-sqlite", "langchain-core")}},
        "cases": sorted(SchedulingTests.evidence, key=lambda c: c["case"])}
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            output.write(gzip.compress((record_json(archive) + "\n").encode("utf-8"), mtime=0))
    else:
        saved = json.loads(gzip.decompress(args.fixture.read_bytes()))
        if stable_cases(archive) != stable_cases(saved):
            raise AssertionError("exact cross-worker requests/replies/seeds/attempt outcomes/committed states differ")
    print(json.dumps(summary(archive), sort_keys=True))
    print("Verified local CPU scheduling/replay; recorded timings are not GPU feasibility measurements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
