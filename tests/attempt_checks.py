"""Bounded CPU process failures and the existing worker-local attempt ledger."""

from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest

from recovery.rounds import prepare_round
from recovery.runner import DurableRunner
from recovery.storage import RecordedFailure, UnresolvedAttempt, WorkerStore, settings_json
from recovery.tasks import Task
from tests.durable_checks import prefix_branch, provider
from tests.event_checks import case_world
from tests.replay_checks import SETTINGS
from tests.round_checks import TOKENIZER, raw_reply


class AttemptLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "worker.sqlite"
        self.world = case_world(Task.SORT)
        self.branch = prefix_branch(self.world)
        with DurableRunner(self.path, TOKENIZER, provider) as runner:
            state = runner.start(self.world, self.branch, settings=SETTINGS)
            runner.store.prepare(self.branch, settings_json(SETTINGS), prepare_round(state, TOKENIZER))
        self.store = WorkerStore(self.path)
        self.addCleanup(self.store.close)
        self.call = self.branch.calls[0].call_id

    def begin(self):
        return self.store.begin_attempt(self.call, timeout_seconds=120, termination_seconds=1)

    def test_start_is_durable_and_readable_without_holding_an_inference_lock(self):
        self.assertEqual(self.begin(), 1)
        reader = sqlite3.connect(self.path)
        self.addCleanup(reader.close)
        self.assertEqual(reader.execute("SELECT status FROM calls WHERE call_id=?", (self.call,)).fetchone()[0], "running")
        self.assertEqual(reader.execute("SELECT timeout_seconds FROM attempts").fetchone()[0], 120)
        with reader:
            reader.execute("CREATE TABLE unlocked_probe (n INTEGER)")
        self.assertEqual(self.store.call(self.branch.calls[1].call_id)["status"], "pending")
        self.assertEqual(self.store.attempts(self.branch.calls[1].call_id), ())

    def test_one_interruption_allows_only_one_identical_bound_retry(self):
        self.begin()
        with self.assertRaises(UnresolvedAttempt):
            self.begin()
        self.store.interrupt_attempt(self.call, "lost worker before raw persistence", elapsed_seconds=0.25)
        with self.assertRaisesRegex(ValueError, "original attempt bounds"):
            self.store.begin_attempt(self.call, timeout_seconds=121, termination_seconds=1)
        self.assertEqual(self.begin(), 2)
        self.store.interrupt_attempt(self.call, "second worker interruption", elapsed_seconds=0.5)
        self.assertEqual(self.store.call(self.call)["status"], "infrastructure_failure")
        self.assertEqual(self.store.response(self.call).status, "infrastructure_failure")
        self.assertEqual([r["number"] for r in self.store.attempts(self.call)], [1, 2])
        self.assertTrue(all(r["uncertain_completion"] for r in self.store.attempts(self.call)))
        self.assertEqual(sum(r["elapsed_seconds"] for r in self.store.attempts(self.call)), 0.75)
        with self.assertRaises(ValueError):
            self.begin()

    def test_durable_invalid_timeout_and_exhausted_results_win_over_interruption(self):
        for response in (raw_reply(TOKENIZER, "{invalid"), RecordedFailure("timeout", "known deadline"),
                         RecordedFailure("infrastructure_failure", "known exhausted provider")):
            with self.subTest(response=response):
                call = self.branch.calls[(0 if hasattr(response, "text") else
                                         1 if response.status == "timeout" else 2)].call_id
                self.store.begin_attempt(call)
                self.store.finish_attempt(call, response, 0.3)
                before = self.store.attempts(call)
                self.store.interrupt_attempt(call, "late lost acknowledgement")
                self.assertEqual(self.store.response(call), response)
                self.assertEqual(self.store.attempts(call), before)
                with self.assertRaises(ValueError):
                    self.store.begin_attempt(call)

    def test_unknown_crash_duration_preserves_observed_work_and_process_loading_idle_interval(self):
        self.begin()
        self.store.process_started(self.call, 1, 1234)
        self.store.process_ready(self.call, 1)
        self.store.observe_attempt(self.call, 1, 0.2, 1234)
        self.store.interrupt_attempt(self.call, "owner killed, end unobserved")
        attempt = self.store.attempts(self.call)[0]
        self.assertIsNone(attempt["finished_at"])
        self.assertIsNone(attempt["elapsed_seconds"])
        self.assertEqual(attempt["observed_seconds"], 0.2)
        self.assertEqual(attempt["worker_pid"], 1234)
        self.assertEqual(attempt["uncertain_completion"], 1)
        self.assertIsNotNone(attempt["recovered_at"])
        interval = dict(self.store.connection.execute("SELECT * FROM provider_processes").fetchone())
        self.assertIsNotNone(interval["ready_at"])
        self.assertIsNone(interval["stopped_at"])
        self.assertEqual(interval["uncertain_stop"], 1)
        self.assertIsNotNone(interval["recovered_at"])

    def test_second_interruption_survives_reopen_and_never_starts_a_third_attempt(self):
        self.begin()
        self.store.interrupt_attempt(self.call, "first owner death")
        self.begin()
        self.store.interrupt_attempt(self.call, "second owner death")
        with closing(WorkerStore(self.path)) as reopened:
            self.assertEqual(len(reopened.attempts(self.call)), 2)
            self.assertEqual(reopened.response(self.call).status, "infrastructure_failure")
            with self.assertRaises(ValueError):
                reopened.begin_attempt(self.call)

    def test_invalid_timings_rollback_and_provider_defects_do_not_authorize_retry(self):
        self.begin()
        for elapsed in (-1, float("nan"), float("inf"), True):
            with self.assertRaises(ValueError):
                self.store.finish_attempt(self.call, raw_reply(TOKENIZER, "{}"), elapsed)
        self.assertEqual(self.store.call(self.call)["status"], "running")
        self.store.block_attempt(self.call, "provider returned a non-response", 0.4)
        with self.assertRaises(UnresolvedAttempt):
            self.store.interrupt_attempt(self.call, "restart cannot make adapter bug retryable")
        self.assertIsNone(self.store.call(self.call)["raw_json"])

    def test_original_attempt_schema_reopens_without_replacing_calls_or_checkpoints(self):
        # T01 schema has the original eight columns and no process records.
        with self.store.connection:
            self.store.connection.execute("DROP TABLE provider_processes")
            self.store.connection.execute("DROP TABLE attempts")
            self.store.connection.execute("""CREATE TABLE attempts (
                call_id TEXT NOT NULL REFERENCES calls(call_id),number INTEGER NOT NULL,
                status TEXT NOT NULL,started_at TEXT NOT NULL,finished_at TEXT,
                elapsed_seconds REAL,uncertain_completion INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (call_id,number))""")
        with closing(WorkerStore(self.path)) as reopened:
            self.assertEqual(reopened.call(self.call), self.store.call(self.call))
            self.assertEqual(reopened.begin_attempt(self.call), 1)
            self.assertGreater(reopened.connection.execute("SELECT count(*) FROM checkpoints").fetchone()[0], 0)
