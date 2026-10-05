"""Actual LangGraph/SQLite save, reopen and resume; scripted CPU providers only."""

from dataclasses import asdict, replace
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import recovery.runner as runner_module
from recovery.events import start_continuation
from recovery.replay import commit_continuation_round, held_prose_counts
from recovery.rounds import (commit_round, drain_deliveries, initial_branch, prefix_snapshot,
                             prepare_round, run_round, snapshot_bytes, validate_round)
from recovery.runner import DurableRunner
from recovery.schedule import _prepare_branches
from recovery.state import OwnReply, ReceivedProse, Slot
from recovery.storage import RecordedFailure, UnresolvedAttempt
from recovery.tasks import PEERS, Size, Task
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
        return DurableRunner(self.path, TOKENIZER, reply_provider, **kwargs, scripted=True)

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
        with DurableRunner(backup, TOKENIZER, forbidden, scripted=True) as runner:
            self.assertEqual(runner.state(self.branch.branch_id), expected)
            runner.run_round(self.branch.branch_id, 4)
            self.assertEqual(runner.store.connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")

    def parents(self, runner, *, event="revision", replicate=0, mode="rich"):
        runner.reply_provider = replay_provider(TOKENIZER, mode)
        for policy in ("B", "C"):
            branch = scheduled(self.world, event, policy, replicate)
            runner.start(self.world, branch, settings=SETTINGS)
            runner.run_round(branch.branch_id, 1)

    def test_durable_invalid_failed_and_unicode_parent_reuse_is_exact_and_branch_local(self):
        for mode in ("rich", "unicode"):
            path = Path(self.temp.name) / f"{mode}.sqlite"
            with DurableRunner(path, TOKENIZER, provider, scripted=True) as runner:
                prefix(runner, self.world)
                self.parents(runner, mode=mode)
                parents = {p: scheduled(self.world, "revision", p) for p in ("B", "C")}
                original = {p: snapshot_bytes(runner.state(b.branch_id)) for p, b in parents.items()}
                runner.reply_provider = forbidden
                for policy in ("P_G", "P_H"):
                    branch = scheduled(self.world, "revision", policy)
                    before = runner.start(self.world, branch, settings=SETTINGS)
                    result = runner.run_round(branch.branch_id, 1)
                    for p, call in enumerate(branch.calls[:4]):
                        row = runner.store.call(call.call_id)
                        self.assertEqual(row["status"], "replay")
                        self.assertEqual(row["generation_id"], call.replay_parent)
                        self.assertIsNone(row["raw_json"])
                        self.assertEqual(result.barrier.replies[p].generated,
                                         runner.store.saved_round(row["generation_id"].rsplit("/r1/", 1)[0], 1,
                                                                  TOKENIZER).barrier.replies[p].generated)
                    self.assertEqual(result.barrier.requests.before, before)
                    self.assertEqual(result.committed, commit_continuation_round(
                        runner.store.saved_round(branch.branch_id, 1, TOKENIZER)).committed)
                    self.assertEqual(result.committed, drain_deliveries(result.committed,
                                     tuple(d.delivery_id for d in result.committed.deliveries)))
                    self.assertEqual(runner.run_round(branch.branch_id, 1), result)
                    self.assertEqual(len({d.delivery_id for d in result.committed.deliveries}),
                                     len(result.committed.deliveries))
                self.assertEqual(original, {p: snapshot_bytes(runner.state(b.branch_id)) for p, b in parents.items()})
                self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 24)

    def test_equality_mismatches_missing_parents_and_recorded_validation_stop_without_effects(self):
        for defect in ("missing", "settings", "seed", "rendered", "native", "view", "validation", "event", "replicate"):
            with self.subTest(defect=defect):
                path = Path(self.temp.name) / f"defect-{defect}.sqlite"
                with DurableRunner(path, TOKENIZER, provider, scripted=True) as runner:
                    prefix(runner, self.world)
                    if defect != "missing":
                        self.parents(runner)
                    branch = scheduled(self.world, "revision", "P_G")
                    before = runner.start(self.world, branch, settings=SETTINGS)
                    if defect != "missing":
                        # Peer zero is cleared in P_G, so its actual parent is C.
                        parent = scheduled(self.world, "revision", "C")
                        connection = runner.store.connection
                        with connection:
                            if defect == "seed":
                                connection.execute("UPDATE calls SET seed=seed+1 WHERE call_id=?", (parent.calls[0].call_id,))
                            elif defect == "validation":
                                connection.execute("UPDATE calls SET validation_json='{}' WHERE call_id=?", (parent.calls[0].call_id,))
                            else:
                                row = connection.execute("SELECT * FROM round_inputs WHERE branch_id=?", (parent.branch_id,)).fetchone()
                                if defect == "settings":
                                    connection.execute("UPDATE round_inputs SET settings_json='{}' WHERE branch_id=?", (parent.branch_id,))
                                elif defect in ("event", "replicate"):
                                    data = json.loads(row["branch_json"])
                                    data[defect] = "sham" if defect == "event" else 1
                                    connection.execute("UPDATE round_inputs SET branch_json=? WHERE branch_id=?",
                                                       (json.dumps(data), parent.branch_id))
                                else:
                                    data = json.loads(row["requests_json"])
                                    if defect == "rendered":
                                        data["rendered"][0]["content"] += " altered"
                                    elif defect == "native":
                                        data["tokenized"][0]["input_ids"][0] += 1
                                    else:
                                        state = json.loads(data["before"])
                                        state["peers"][0]["sources"][0]["value"] += 1
                                        data["before"] = json.dumps(state)
                                    connection.execute("UPDATE round_inputs SET requests_json=? WHERE branch_id=?",
                                                       (json.dumps(data), parent.branch_id))
                    runner.reply_provider = forbidden
                    with self.assertRaises(ValueError):
                        runner.run_round(branch.branch_id, 1)
                    self.assertEqual(runner.state(branch.branch_id), before)
                    self.assertTrue(all(runner.store.call(c.call_id)["status"] == "pending" for c in branch.calls[:4]))

    def test_boundary_replacement_all_families_sizes_siblings_events_and_replicates_survives_reopen(self):
        for size in Size:
            for task in Task:
                with self.subTest(size=size, task=task):
                    world = case_world(task, size)
                    path = Path(self.temp.name) / f"{size.value}-{task.value}.sqlite"
                    expected = {}
                    with DurableRunner(path, TOKENIZER, provider, scripted=True) as runner:
                        old = prefix(runner, world)
                        original = prefix_snapshot(runner.state(old.branch_id))
                        runner.reply_provider = replay_provider(TOKENIZER)
                        branches = [b for b in _prepare_branches((world,)) if b.phase == "continuation"]
                        # Prescribed parents precede their mixed/Q consumers.
                        branches.sort(key=lambda b: any(c.replay_parent for c in b.calls))
                        for branch in branches:
                            before = runner.start(world, branch, settings=SETTINGS)
                            self.assertEqual(before, start_continuation(original, world, branch))
                            self.assertTrue(before.boundary_applied)
                            if branch.policy in ("C", "F", "C_delta", "Q_C"):
                                self.assertTrue(all(not p.history and not p.feedback and p.candidate.status == "unexecuted"
                                                    for p in before.peers))
                            result = runner.run_round(branch.branch_id, 1)
                            expected[branch.branch_id] = result.committed
                            # A second start must neither clear new work nor repeat the event.
                            self.assertEqual(runner.start(world, branch, settings=SETTINGS), result.committed)
                            self.assertEqual(prefix_snapshot(runner.state(old.branch_id)), original)
                    with DurableRunner(path, TOKENIZER, forbidden, scripted=True) as runner:
                        for branch_id, state in expected.items():
                            self.assertEqual(runner.state(branch_id), state)
                            self.assertEqual(runner.run_round(branch_id, 1).committed, state)

    def test_q_held_queue_and_release_survive_interrupted_delivery_resume(self):
        with self.runner() as runner:
            prefix(runner, self.world)
            self.parents(runner)
            parent = scheduled(self.world, "revision", "B")
            branch = scheduled(self.world, "revision", "Q_B")
            runner.start(self.world, branch, settings=SETTINGS)
            runner.reply_provider = forbidden
            q = runner.run_round(branch.branch_id, 1)
            b = runner.state(parent.branch_id)
            self.assertTrue(q.committed.pending)
            self.assertGreater(sum(held_prose_counts(q.committed)), 0)
            self.assertEqual(tuple(p.sources for p in q.committed.peers), tuple(p.sources for p in b.peers))
            self.assertEqual(tuple(tuple(e for e in p.history if type(e) is OwnReply) for p in q.committed.peers),
                             tuple(tuple(e for e in p.history if type(e) is OwnReply) for p in b.peers))
        with self.runner(replay_provider(TOKENIZER)) as runner:
            before = runner.state(branch.branch_id)
            with patch.object(runner_module, "commit_continuation_round", side_effect=RuntimeError("before delivery checkpoint")):
                with self.assertRaisesRegex(RuntimeError, "before delivery checkpoint"):
                    runner.run_round(branch.branch_id, 2)
            self.assertEqual(runner.state(branch.branch_id), before)
            attempts = runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0]
        with self.runner(forbidden) as runner:
            released = runner.run_round(branch.branch_id, 2).committed
            self.assertFalse(released.pending)
            prose = [e for p in released.peers for e in p.history if type(e) is ReceivedProse]
            self.assertTrue(any(e.slot == Slot("recovery", 1) for e in prose))
            self.assertTrue(all(d.first_usable == Slot("recovery", 3)
                                for d in released.deliveries if d.generated == Slot("recovery", 1) and d.text is not None))
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], attempts)
            self.assertEqual(runner.run_round(branch.branch_id, 2).committed, released)

    def test_interrupted_pure_effects_reconstruct_from_saved_replies_without_mutation(self):
        with self.runner() as runner:
            prefix(runner, self.world)
            self.parents(runner)
            branch = scheduled(self.world, "revision", "C")
            before = runner.state(branch.branch_id)
            runner.reply_provider = replay_provider(TOKENIZER)
            real_commit = runner_module.commit_continuation_round

            def interrupted(saved):
                real_commit(saved)
                raise RuntimeError("after pure effects, before checkpoint")
            with patch.object(runner_module, "commit_continuation_round", side_effect=interrupted):
                with self.assertRaisesRegex(RuntimeError, "after pure effects"):
                    runner.run_round(branch.branch_id, 2)
            self.assertEqual(runner.state(branch.branch_id), before)
        with self.runner(forbidden) as runner:
            result = runner.run_round(branch.branch_id, 2)
            self.assertEqual(result.committed, commit_continuation_round(
                runner.store.saved_round(branch.branch_id, 2, TOKENIZER)).committed)

    def test_unrelated_equal_requests_and_repeat_seeds_keep_distinct_physical_generations(self):
        with self.runner() as runner:
            prefix(runner, self.world)
            runner.reply_provider = replay_provider(TOKENIZER)
            rows = []
            for replicate in (0, 1):
                branch = scheduled(self.world, "revision", "B", replicate)
                runner.start(self.world, branch, settings=SETTINGS)
                rows.append(runner.run_round(branch.branch_id, 1))
            self.assertEqual(rows[0].barrier.requests.rendered, rows[1].barrier.requests.rendered)
            branches = [scheduled(self.world, "revision", "B", r) for r in (0, 1)]
            self.assertNotEqual(branches[0].calls[0].seed, branches[1].calls[0].seed)
            for branch in branches:
                for call in branch.calls[:4]:
                    self.assertEqual(runner.store.call(call.call_id)["generation_id"], call.call_id)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 24)

    def test_identical_nonreplay_q_parent_requests_settings_and_seeds_are_not_deduplicated(self):
        with self.runner() as runner:
            prefix(runner, self.world)
            runner.reply_provider = replay_provider(TOKENIZER, "silent")
            parent = scheduled(self.world, "revision", "B")
            q = scheduled(self.world, "revision", "Q_B")
            runner.start(self.world, parent, settings=SETTINGS)
            runner.run_round(parent.branch_id, 1)
            runner.start(self.world, q, settings=SETTINGS)
            runner.run_round(q.branch_id, 1)
            b2 = runner.run_round(parent.branch_id, 2)
            q2 = runner.run_round(q.branch_id, 2)
            self.assertEqual(b2.barrier.requests.views, q2.barrier.requests.views)
            self.assertEqual(b2.barrier.requests.rendered, q2.barrier.requests.rendered)
            self.assertEqual(b2.barrier.requests.tokenized, q2.barrier.requests.tokenized)
            for bcall, qcall in zip(parent.calls[4:8], q.calls[4:8]):
                self.assertEqual(bcall.seed, qcall.seed)
                self.assertEqual(runner.store.call(bcall.call_id)["generation_id"], bcall.call_id)
                self.assertEqual(runner.store.call(qcall.call_id)["generation_id"], qcall.call_id)
                self.assertNotEqual(bcall.call_id, qcall.call_id)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 28)

    def test_partial_raw_commit_resume_skips_only_completed_calls(self):
        seen = []
        def counted(view, rendered, tokenized, **kwargs):
            seen.append(view.peer)
            return reply(TOKENIZER, view)
        with self.runner(counted) as runner:
            runner.start(self.world, self.branch, settings=SETTINGS)
            finish = runner.store.finish_attempt
            def interrupted(call_id, raw, elapsed):
                finish(call_id, raw, elapsed)
                raise RuntimeError("one raw reply committed")
            with patch.object(runner.store, "finish_attempt", side_effect=interrupted):
                with self.assertRaisesRegex(RuntimeError, "one raw reply committed"):
                    runner.run_round(self.branch.branch_id, 1)
        with self.runner(counted) as runner:
            runner.run_round(self.branch.branch_id, 1)
        self.assertEqual(seen, [0, 1, 2, 3])

    def test_checkpoint_write_failure_before_and_after_commit_has_one_authoritative_effect(self):
        for when in ("before", "after"):
            with self.subTest(when=when):
                path = Path(self.temp.name) / f"checkpoint-{when}.sqlite"
                expected = run_round(initial_branch(self.world.world, self.branch.branch_id), TOKENIZER,
                                     event_provider(TOKENIZER)).committed
                with DurableRunner(path, TOKENIZER, provider, scripted=True) as runner:
                    initial = runner.start(self.world, self.branch, settings=SETTINGS)
                    put = runner.saver.put
                    def interrupted(config, checkpoint, metadata, versions):
                        state = checkpoint["channel_values"].get("committed")
                        delivering = state is not None and json.loads(state)["last_slot"] == asdict(Slot("prefix", 1))
                        if delivering and when == "before":
                            raise RuntimeError("before committed checkpoint write")
                        result = put(config, checkpoint, metadata, versions)
                        if delivering and when == "after":
                            raise RuntimeError("after committed checkpoint write")
                        return result
                    with patch.object(runner.saver, "put", side_effect=interrupted):
                        with self.assertRaisesRegex(RuntimeError, f"{when} committed checkpoint"):
                            runner.run_round(self.branch.branch_id, 1)
                    # Durable pending writes are not delivery exports until committed.
                    self.assertEqual(runner.state(self.branch.branch_id), initial if when == "before" else expected)
                    self.assertEqual(runner.deliveries(self.branch.branch_id),
                                     (initial if when == "before" else expected).deliveries)
                with DurableRunner(path, TOKENIZER, forbidden, scripted=True) as runner:
                    self.assertEqual(runner.run_round(self.branch.branch_id, 1).committed, expected)
                    self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 4)

    def test_context_overflow_stops_before_any_attempt_without_shortening_input(self):
        from tests.round_checks import RoundTokenizer
        from recovery.prompts import MAX_CONTEXT_TOKENS
        class Oversized(RoundTokenizer):
            def __call__(self, *args, **kwargs):
                return {"input_ids": [1] * MAX_CONTEXT_TOKENS, "attention_mask": [1] * MAX_CONTEXT_TOKENS}
        with DurableRunner(self.path, Oversized(), forbidden, scripted=True) as runner:
            initial = runner.start(self.world, self.branch, settings=SETTINGS)
            with self.assertRaisesRegex(ValueError, "context limit"):
                runner.run_round(self.branch.branch_id, 1)
            self.assertEqual(runner.state(self.branch.branch_id), initial)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 0)

    def test_restart_with_changed_tokenizer_or_start_settings_rejects_without_inference(self):
        from tests.round_checks import RoundTokenizer
        with self.runner() as runner:
            runner.start(self.world, self.branch, settings=SETTINGS)
            with patch.object(runner.store, "begin_attempt", side_effect=RuntimeError("before inference")):
                with self.assertRaisesRegex(RuntimeError, "before inference"):
                    runner.run_round(self.branch.branch_id, 1)
        class Changed(RoundTokenizer):
            def apply_chat_template(self, *args, **kwargs):
                return super().apply_chat_template(*args, **kwargs) + " changed template"
        with DurableRunner(self.path, Changed(), forbidden, scripted=True) as runner:
            with self.assertRaisesRegex(ValueError, "equality"):
                runner.run_round(self.branch.branch_id, 1)
            with self.assertRaisesRegex(ValueError, "settings"):
                runner.start(self.world, self.branch, settings={**SETTINGS, "temperature": 0.7})


if __name__ == "__main__":
    unittest.main()
