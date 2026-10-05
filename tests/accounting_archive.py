"""Retain/reproduce CPU accounting evidence; no model or experiment execution."""

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
from tests.accounting_checks import AccountingTests, BudgetTests


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "accounting_progress_traces.json.gz"


def stable_evidence(cases):
    """Compare declared joins/counts/bounds; retain real clocks separately."""
    hand = cases["reconciliation"]
    policies = [{k: v for k, v in row.items()} for row in hand["policy_costs"]]
    result = {"reconciliation": {"counts": hand["counts"], "physical": hand["physical"],
        "policy_costs": policies, "partition_seconds": hand["resources"]["partition_seconds"],
        "allocated_gpu_hours": hand["resources"]["allocated_gpu_hours"], "deliveries": hand["validated_deliveries"]},
        "ambiguous": {"physical": cases["ambiguous"]["physical"],
                      "partition_seconds": cases["ambiguous"]["resources"]["partition_seconds"]},
        "slower_device_forecast": cases["slower_device_forecast"],
        "failed_configuration": cases["failed_configuration"],
        "historical_admission": {"before_counts": cases["historical_admission"]["before"]["counts"],
            "before_forecast": cases["historical_admission"]["before"]["forecast"],
            "after_counts": cases["historical_admission"]["after"]["counts"]}}
    for name in ("timeout_admission_stop", "hard_deadline_stop", "resumed_deadline_stop"):
        case = cases[name]
        result[name] = {"counts": case["counts"], "work": case["work"],
            "slots": [{k: row[k] for k in ("call_id", "generation_id", "replay_parent", "status", "protocol_outcome", "finished")}
                      for row in case["logical_slots"]], "active_devices": case["resources"]["active_devices"]}
    # Normalize dataclass tuple fields to the retained JSON representation.
    return json.loads(record_json(result))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    args = parser.parse_args()
    AccountingTests.evidence.clear()
    BudgetTests.evidence.clear()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName("tests.accounting_checks"))
    if not result.wasSuccessful():
        return 1
    archive = {"kind": "CPU protocol/accounting validation with synthetic allocations; not GPU, pilot or main outcomes",
        "environment": {"python": sys.version, "platform": platform.platform(), "sqlite": sqlite3.sqlite_version,
            "packages": {p: importlib.metadata.version(p) for p in ("pydantic", "langgraph", "langgraph-checkpoint",
                         "langgraph-checkpoint-sqlite", "langchain-core")}},
        "checks": result.testsRun, "cases": dict(AccountingTests.evidence, **BudgetTests.evidence)}
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as stream:
                stream.write((record_json(archive) + "\n").encode("utf-8"))
        print(f"Created {args.write_fixture}; {result.testsRun} checks, {len(archive['cases'])} evidence cases.")
    else:
        with gzip.open(args.fixture, "rt", encoding="utf-8") as source:
            saved = json.load(source)
        if stable_evidence(archive["cases"]) != stable_evidence(saved["cases"]):
            print("Accounting joins/counts/bounds differ from the retained evidence.", file=sys.stderr)
            return 1
        print(f"Reproduced {args.fixture}; hand accounting, measured forecast and safe-stop/resume records match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
