"""Reproduce a small derived durable-runner trace; no model inference or results.

Default: the injected CPU counter. --tokenizer uses only local pinned metadata.
Wall-clock attempt times remain in SQLite and are omitted from this deterministic
validation export. Checkpoints own effects; this fixture is never an effect store.
"""

import argparse
from dataclasses import asdict
import gzip
import importlib.metadata
import json
from pathlib import Path
import sqlite3
import tempfile
from unittest.mock import patch

import recovery.runner as runner_module
from recovery.replay import held_prose_counts
from recovery.runner import DurableRunner
from recovery.schedule import _prepare_branches
from recovery.storage import record_json
from recovery.tasks import Size, Task
from tests.durable_checks import forbidden
from tests.event_checks import case_world, event_provider
from tests.replay_checks import SETTINGS, replay_provider
from tests.round_checks import TOKENIZER

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "durable_round_traces.json.gz"


def trace_archive(tokenizer=TOKENIZER):
    archive = {"kind": "scripted CPU durable-runner validation; not model outcomes",
               "tokenizer": "injected word counter" if tokenizer is TOKENIZER else "local native metadata",
               "context_limit": 262144, "cases": []}
    for task, size in ((Task.SORT, Size.TARGET), (Task.BFS, Size.FALLBACK)):
        world = case_world(task, size)
        branches = [b for b in _prepare_branches((world,)) if b.phase != "control"]
        branches.sort(key=lambda b: (b.phase != "prefix", any(c.replay_parent for c in b.calls)))
        with tempfile.TemporaryDirectory() as directory:
            path, backup = Path(directory) / "worker.sqlite", Path(directory) / "backup.sqlite"
            prefix_provider = event_provider(tokenizer)
            def provide(view, rendered, tokenized, **kwargs):
                return prefix_provider(view, rendered, tokenized)
            case = {"world_id": world.world_id, "task": task.value, "size": size.value, "branches": []}
            with DurableRunner(path, tokenizer, provide) as runner:
                for branch in branches:
                    initial = runner.start(world, branch, settings=SETTINGS)
                    if branch.phase == "continuation":
                        runner.reply_provider = replay_provider(tokenizer, "unicode")
                    rows = []
                    for r in range(1, 5):
                        interrupted = branch.policy == "Q_B" and branch.event == "revision" and r == 2
                        if interrupted:
                            with patch.object(runner_module, "commit_continuation_round",
                                              side_effect=RuntimeError("scripted interruption before delivery checkpoint")):
                                try:
                                    runner.run_round(branch.branch_id, r)
                                except RuntimeError as error:
                                    if str(error) != "scripted interruption before delivery checkpoint":
                                        raise
                                else:
                                    raise AssertionError("injected interruption did not execute")
                            original_provider = runner.reply_provider
                            runner.reply_provider = forbidden
                        result = runner.run_round(branch.branch_id, r)
                        if interrupted:
                            runner.reply_provider = original_provider
                        rows.append({
                            "round": r, "resumed_from_durable_replies": interrupted,
                            "requests": [{"view": asdict(v), "rendered": asdict(rendered), "tokenized": asdict(native)}
                                         for v, rendered, native in zip(result.barrier.requests.views,
                                             result.barrier.requests.rendered, result.barrier.requests.tokenized)],
                            "replies": [asdict(reply) for reply in result.barrier.replies],
                            "calls": [{k: runner.store.call(c.call_id)[k] for k in
                                      ("call_id", "generation_id", "replay_parent", "seed", "status")}
                                      for c in branch.calls if c.round_number == r],
                            "committed": asdict(result.committed),
                            "held_prose": held_prose_counts(result.committed) if branch.phase == "continuation" else None,
                        })
                    case["branches"].append({"branch": asdict(branch), "initial": asdict(initial), "rounds": rows})
                # Attempt clocks are recorded in the DB; deterministic fields only
                # enter this reproducible derived export.
                case["attempts"] = [dict(row) for row in runner.store.connection.execute(
                    "SELECT call_id,number,status,uncertain_completion FROM attempts ORDER BY call_id,number")]
                runner.backup(backup)
            with DurableRunner(backup, tokenizer, forbidden) as restored:
                for row in case["branches"]:
                    branch_id = _branch_id(row)
                    if record_json(asdict(restored.state(branch_id))) != record_json(row["rounds"][-1]["committed"]):
                        raise AssertionError("backup restored a different committed state")
                    restored.run_round(branch_id, 4)
                if restored.store.connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                    raise AssertionError("backup integrity check failed")
            archive["cases"].append(case)
    # Convert tuple/dataclass encodings to their exact JSON representation once.
    return json.loads(record_json(archive))


def _branch_id(row):
    return row["initial"]["branch_id"]


def summary(archive):
    rounds = [r for c in archive["cases"] for b in c["branches"] for r in b["rounds"]]
    calls = [call for r in rounds for call in r["calls"]]
    return {"cases": len(archive["cases"]), "branches": sum(len(c["branches"]) for c in archive["cases"]),
            "rounds": len(rounds), "logical_calls": len(calls),
            "physical_attempts": sum(len(c["attempts"]) for c in archive["cases"]),
            "exact_parent_reuses": sum(c["replay_parent"] is not None for c in calls),
            "resumed_delivery_transitions": sum(r["resumed_from_durable_replies"] for r in rounds)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create a derived CPU validation archive")
    parser.add_argument("--tokenizer", type=Path, help="optional local native metadata only; never model weights")
    args = parser.parse_args()
    tokenizer = TOKENIZER
    if args.tokenizer:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    actual = trace_archive(tokenizer)
    encoded = (record_json(actual) + "\n").encode("utf-8")
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            output.write(gzip.compress(encoded, mtime=0))
        fixture = args.write_fixture
    else:
        fixture = args.fixture
    if gzip.decompress(fixture.read_bytes()) != encoded:
        raise AssertionError("durable trace archive differs from fresh execution")
    print(json.dumps(summary(actual), sort_keys=True))
    print("Verified scripted durable trace/backup; no inference or empirical result.")
    print("SQLite", sqlite3.sqlite_version, ";", ", ".join(f"{p}={importlib.metadata.version(p)}" for p in
          ("langgraph", "langgraph-checkpoint", "langgraph-checkpoint-sqlite", "langchain-core", "pydantic")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
