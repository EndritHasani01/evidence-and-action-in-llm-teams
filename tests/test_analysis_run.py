"""Read-only saved-worker/CLI integration and observed versus inactive Q prose."""

import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recovery.analysis import analyze_run, prose_activity
from recovery.evaluate import evaluate_records, write_evaluation
from recovery.tasks import Task
from tests.estimand_fixture import selection
from tests.outcome_fixture import ROOT, saved_records, write_worker


def saved_selection(task):
    worlds, branches = selection(task, size="target")
    return worlds, tuple(b for b in branches if b.phase != "control")


class OfflineEstimandRunTests(unittest.TestCase):
    def test_original_worker_joins_and_exclusive_json_exports(self):
        worlds, branches = saved_selection(Task.SORT)
        records, inputs, attempts = saved_records(worlds, branches)
        # The original replies have send=[]; retain their observed inactive Q
        # boundaries in the ordinary-worker fixture, rather than dropping them.
        for branch in branches:
            if branch.policy in ("Q_B", "Q_C"):
                saved = inputs[branch.branch_id, 2]
                state = json.loads(saved["requests"]["before"])
                state.update(committed=True, last_slot={"phase": "recovery", "round_number": 1}, pending=[])
                state["deliveries"] = [dict(d, text=None, generated=None) for d in state["deliveries"]]
                saved["requests"]["before"] = json.dumps(state)
        expected = evaluate_records(worlds, branches, records, inputs,
            sorted(attempts, key=lambda r: (r["call_id"], r["number"])))
        with tempfile.TemporaryDirectory() as directory:
            worker = Path(directory) / "worker.sqlite"
            write_worker(worker, records, inputs, attempts)
            before = worker.read_bytes()
            actual = analyze_run(worlds, branches, [worker])
            self.assertEqual({k: v for k, v in actual.items() if k != "estimands"}, expected)
            self.assertEqual(worker.read_bytes(), before)
            self.assertTrue(actual["estimands"]["world_contrasts"])
            self.assertEqual(len(actual["estimands"]["prose_activity"]), 4)
            self.assertTrue(all(r["active"] is False for r in actual["estimands"]["prose_activity"]))
            for suffix in ("json", "json.gz"):
                export = Path(directory) / ("tables." + suffix)
                write_evaluation(export, actual)
                opener = gzip.open if suffix.endswith("gz") else open
                with opener(export, "rt", encoding="utf-8") as source:
                    self.assertEqual(json.load(source), actual)
                with self.assertRaises(FileExistsError):
                    write_evaluation(export, actual)
            with self.assertRaises(ValueError):
                analyze_run(worlds, branches, [worker, worker])
            missing = Path(directory) / "unknown.sqlite"
            incomplete = analyze_run(worlds, branches, [missing])
            self.assertFalse(missing.exists())
            self.assertTrue(all(r["value"] is None for r in incomplete["estimands"]["world_contrasts"]))

    def test_observed_held_empty_inactive_and_unknown_prose_never_selects_worlds(self):
        worlds, branches = saved_selection(Task.SORT)
        _, inputs, _ = saved_records(worlds, branches)
        Q = next(b for b in branches if b.policy == "Q_B" and b.event == "revision")
        state = json.loads(inputs[Q.branch_id, 2]["requests"]["before"])
        state.update(committed=True, last_slot={"phase": "recovery", "round_number": 1}, pending=[], deliveries=[])
        def delivery(text, recipient, number):
            return {"delivery_id": f"{Q.branch_id}/r1/text/{number}", "recipient": recipient,
                "generated": {"phase": "recovery", "round_number": 1}, "text": text,
                "first_usable": None, "source": None}
        state["pending"] = [delivery("useful or harmful prose", 1, 0), delivery("", 2, 1)]
        inputs[Q.branch_id, 2]["requests"]["before"] = json.dumps(state)
        activity = prose_activity(worlds, branches, inputs)
        row = next(r for r in activity if r["branch_id"] == Q.branch_id)
        self.assertTrue(row["active"])
        self.assertEqual(row["nonempty_texts_per_recipient"], [0, 1, 0, 0])
        self.assertEqual(row["queued_text_components"], 2)
        state["pending"] = [delivery("", 2, 1)]
        inputs[Q.branch_id, 2]["requests"]["before"] = json.dumps(state)
        row = next(r for r in prose_activity(worlds, branches, inputs) if r["branch_id"] == Q.branch_id)
        self.assertFalse(row["active"])
        self.assertEqual(row["nonempty_texts"], 0)
        self.assertEqual(len(activity), 4)  # Both Q policies in both events, never selected by activity.
        unknown = prose_activity(worlds, branches, {})
        self.assertEqual(len(unknown), 4)
        self.assertTrue(all(r["active"] is None for r in unknown))

    def test_counts_survive_release_and_wrong_release_is_a_protocol_defect(self):
        worlds, branches = saved_selection(Task.BFS)
        _, inputs, _ = saved_records(worlds, branches)
        Q = next(b for b in branches if b.policy == "Q_C" and b.event == "sham")
        state = json.loads(inputs[Q.branch_id, 3]["requests"]["before"])
        state.update(committed=True, last_slot={"phase": "recovery", "round_number": 2}, pending=[])
        state["deliveries"] = [{"delivery_id": Q.branch_id + "/text", "recipient": 0, "text": " x ",
            "source": None, "generated": {"phase": "recovery", "round_number": 1},
            "first_usable": {"phase": "recovery", "round_number": 3}}]
        inputs.pop((Q.branch_id, 2))
        inputs[Q.branch_id, 3]["requests"]["before"] = json.dumps(state)
        row = next(r for r in prose_activity(worlds, branches, inputs) if r["branch_id"] == Q.branch_id)
        self.assertEqual(row["nonempty_texts"], 1)
        state["deliveries"][0]["first_usable"]["round_number"] = 2
        inputs[Q.branch_id, 3]["requests"]["before"] = json.dumps(state)
        with self.assertRaises(ValueError):
            prose_activity(worlds, branches, inputs)

    def test_cli_full_development_schedule_is_offline_and_protects_existing_exports(self):
        with tempfile.TemporaryDirectory() as directory:
            export, worker = Path(directory) / "analysis.json.gz", Path(directory) / "missing.sqlite"
            command = [sys.executable, "-S", "-m", "recovery", "analyze", "--estimands", "--stage", "development",
                "--manifest", str(ROOT / "tests/fixtures/population_target.json"),
                "--schedule", str(ROOT / "tests/fixtures/schedules_target.json"),
                "--worker", str(worker), "--output", str(export)]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=45)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("0/1178 recorded", result.stdout)
            self.assertFalse(worker.exists())
            with gzip.open(export, "rt", encoding="utf-8") as source:
                actual = json.load(source)
            self.assertEqual(actual["coverage"]["unknown"], 1178)
            self.assertTrue(actual["estimands"]["summaries"])
            self.assertEqual(actual["estimands"]["scope"], "development validation")
            self.assertEqual(actual["estimands"]["repeatability"], [])
            before = export.read_bytes()
            repeated = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=45)
            self.assertEqual(repeated.returncode, 2)
            self.assertEqual(export.read_bytes(), before)
