"""Actual LangGraph/SQLite save, reopen and resume; scripted CPU providers only."""

from dataclasses import asdict, replace
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import recovery.runner as runner_module
from recovery.rounds import (commit_round, drain_deliveries, initial_branch,
                             prepare_round, run_round, snapshot_bytes, validate_round)
from recovery.runner import DurableRunner
from recovery.schedule import _prepare_branches
from recovery.state import Slot
from recovery.storage import RecordedFailure, UnresolvedAttempt
from recovery.tasks import Task
from tests.event_checks import case_world, event_provider, scheduled
from tests.replay_checks import SETTINGS, replay_provider
from tests.round_checks import TOKENIZER, raw_reply, reply


def prefix_branch(world):
    return next(b for b in _prepare_branches((world,)) if b.phase == "prefix")


def provider(view, rendered, tokenized, *, seed, settings):
    return event_provider(TOKENIZER)(view, rendered, tokenized)


def prefix(runner, world):
    branch = prefix_branch(world)
    runner.start(world, branch, settings=SETTINGS)
    for r in range(1, 5):
        runner.run_round(branch.branch_id, r)
    return branch


def forbidden(*args, **kwargs):
    raise AssertionError("completed/replayed response was regenerated")


class DurableTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "worker.sqlite"
        self.world = case_world(Task.SORT)
        self.branch = prefix_branch(self.world)

    def runner(self, reply_provider=provider, **kwargs):
        return DurableRunner(self.path, TOKENIZER, reply_provider, **kwargs)

    def test_real_wal_full_settings_and_synchronous_checkpoint_reopen(self):
        with self.runner() as runner:
            initial = runner.start(self.world, self.branch, settings=SETTINGS)
            for connection in (runner.store.connection, runner.checkpoint_connection):
                self.assertEqual(connection.execute("PRAGMA journal_mode").fetchone()[0], "wal")
                self.assertEqual(connection.execute("PRAGMA synchronous").fetchone()[0], 2)
            result = runner.run_round(self.branch.branch_id, 1)
            self.assertNotEqual(initial, result.committed)
            expected = snapshot_bytes(result.committed)
            # Checkpoint is visible to an independent on-disk reader immediately.
            reader = sqlite3.connect(self.path)
            self.assertGreater(reader.execute("SELECT count(*) FROM checkpoints").fetchone()[0], 0)
            reader.close()
        with self.runner(forbidden) as runner:
            self.assertEqual(snapshot_bytes(runner.state(self.branch.branch_id)), expected)
            self.assertEqual(snapshot_bytes(runner.run_round(self.branch.branch_id, 1).committed), expected)

    def test_raw_invalid_and_failures_commit_before_validation_and_resume_without_inference(self):
        calls = []

        def outputs(view, rendered, tokenized, **kwargs):
            calls.append(view.peer)
            if view.peer == 0:
                return raw_reply(TOKENIZER, "{invalid raw \ud800")
            if view.peer == 1:
                return RecordedFailure("timeout", "completed scripted timeout")
            if view.peer == 2:
                return None
            return reply(TOKENIZER, view)

        def interrupt_validation(*args, **kwargs):
            reader = sqlite3.connect(self.path)
            rows = reader.execute("SELECT status,raw_json,failure_json,validation_json FROM calls ORDER BY peer").fetchall()
            reader.close()
            self.assertEqual([r[0] for r in rows], ["completed", "timeout", "infrastructure_failure", "completed"])
            self.assertTrue(all(r[3] is None for r in rows))
            raise RuntimeError("after all raw commits, before validation")

        with self.runner(outputs) as runner:
            runner.start(self.world, self.branch, settings=SETTINGS)
            with patch.object(runner_module, "validate_round", side_effect=interrupt_validation):
                with self.assertRaisesRegex(RuntimeError, "after all raw commits"):
                    runner.run_round(self.branch.branch_id, 1)
            self.assertIsNone(runner.state(self.branch.branch_id).last_slot)
        self.assertEqual(calls, [0, 1, 2, 3])
        with self.runner(forbidden) as runner:
            result = runner.run_round(self.branch.branch_id, 1)
            self.assertEqual([r.candidate.status for r in result.barrier.replies], ["invalid", "failed", "failed", "valid"])
            self.assertEqual(result.barrier.replies[0].generated.text, "{invalid raw \ud800")
            for p in (0, 1, 2):
                self.assertIsNone(result.committed.peers[p].candidate.value)
            self.assertFalse(any(d.origin == "peer" for d in result.committed.deliveries))
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 4)

    def test_no_write_lock_is_held_during_provider_and_attempt_start_is_durable(self):
        def unlocked(view, rendered, tokenized, **kwargs):
            reader = sqlite3.connect(self.path, timeout=0.1)
            try:
                row = reader.execute("SELECT status FROM calls WHERE peer=?", (view.peer,)).fetchone()
                self.assertEqual(row[0], "running")
                self.assertEqual(reader.execute("SELECT count(*) FROM attempts WHERE status='running'").fetchone()[0], 1)
                reader.execute("BEGIN IMMEDIATE")
                reader.rollback()
            finally:
                reader.close()
            return reply(TOKENIZER, view)
        with self.runner(unlocked) as runner:
            runner.start(self.world, self.branch, settings=SETTINGS)
            runner.run_round(self.branch.branch_id, 1)

    def test_ordinary_application_transaction_rolls_back_whole_round_on_error(self):
        with self.runner() as runner:
            state = runner.start(self.world, self.branch, settings=SETTINGS)
            broken = replace(self.branch, calls=(self.branch.calls[0], self.branch.calls[0],
                                                *self.branch.calls[2:]))
            with self.assertRaises(sqlite3.IntegrityError):
                runner.store.prepare(broken, json.dumps(SETTINGS), prepare_round(state, TOKENIZER))
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM round_inputs").fetchone()[0], 0)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM calls").fetchone()[0], 0)

    def test_active_without_raw_response_stops_for_attempt_recovery_not_resampling(self):
        with self.runner(lambda *a, **k: (_ for _ in ()).throw(RuntimeError("interrupted inference"))) as runner:
            runner.start(self.world, self.branch, settings=SETTINGS)
            with self.assertRaisesRegex(RuntimeError, "interrupted inference"):
                runner.run_round(self.branch.branch_id, 1)
            rows = [runner.store.call(c.call_id)["status"] for c in self.branch.calls[:4]]
            self.assertEqual(rows, ["running", "pending", "pending", "pending"])
        with self.runner(forbidden) as runner:
            with self.assertRaises(UnresolvedAttempt):
                runner.run_round(self.branch.branch_id, 1)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 1)

    def test_full_prefix_matches_pure_protocol_and_completed_round_operation_is_idempotent(self):
        expected = initial_branch(self.world.world, self.branch.branch_id)
        for _ in range(4):
            expected = run_round(expected, TOKENIZER, event_provider(TOKENIZER)).committed
        with self.runner() as runner:
            prefix(runner, self.world)
            self.assertEqual(runner.state(self.branch.branch_id), expected)
            self.assertEqual(runner.run_round(self.branch.branch_id, 4).committed, expected)
            self.assertEqual(runner.run_round(self.branch.branch_id, 1).committed.last_slot, Slot("prefix", 1))
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 16)

    def test_live_sqlite_backup_and_exclusive_archive_reopen(self):
        backup = Path(self.temp.name) / "archive.sqlite"
        with self.runner() as runner:
            prefix(runner, self.world)
            expected = runner.state(self.branch.branch_id)
            runner.backup(backup)
            with self.assertRaises(FileExistsError):
                runner.backup(backup)
        with DurableRunner(backup, TOKENIZER, forbidden) as runner:
            self.assertEqual(runner.state(self.branch.branch_id), expected)
            runner.run_round(self.branch.branch_id, 4)
            self.assertEqual(runner.store.connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")


if __name__ == "__main__":
    unittest.main()
