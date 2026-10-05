"""Bounded CPU process failures and the existing worker-local attempt ledger."""

from contextlib import closing
from dataclasses import asdict, replace
from functools import partial
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from time import monotonic, sleep
import unittest
from unittest.mock import patch

from recovery.attempts import InfrastructureInterruption, ProcessProvider, ProviderDefect
from recovery.rounds import initial_branch, prepare_round, run_round, snapshot_bytes
from recovery.runner import DurableRunner
from recovery.storage import RecordedFailure, UnresolvedAttempt, WorkerStore, settings_json
from recovery.tasks import Task
from tests.durable_checks import prefix_branch, provider
from tests.event_checks import case_world, event_provider
from tests.replay_checks import SETTINGS
from tests.round_checks import TOKENIZER, placeholder, raw_reply, reply


def append_trace(path, value):
    with Path(path).open("a", encoding="utf-8") as output:
        output.write(json.dumps(value, ensure_ascii=True, sort_keys=True) + "\n")


def read_trace(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines(keepends=True)
            if line.endswith("\n")] if Path(path).exists() else []


def process_factory(mode, trace):
    """Importable CPU-only loader; intentional failures never run a model."""
    import recovery.runner
    append_trace(trace, {"event": "load", "pid": os.getpid(), "module": recovery.runner.__file__})
    if mode == "hang_load":
        while True:
            sleep(1)
    return partial(process_reply, mode, trace)


def process_reply(mode, trace, view, rendered, tokenized, *, seed, settings):
    append_trace(trace, {"event": "generation", "pid": os.getpid(), "view": asdict(view),
        "rendered": asdict(rendered), "tokenized": asdict(tokenized), "seed": seed, "settings": settings})
    if view.peer == 0 and ((mode == "hang" and view.slot.round_number == 2) or mode == "hang_first"):
        while True:
            sleep(1)
    response = provider(view, rendered, tokenized, seed=seed, settings=settings)
    if mode == "normal":
        sleep(0.02)  # A slow completed CPU call, distinct from a hung call.
    if mode in ("interrupt_once", "interrupt_always") and view.peer == 0:
        # The backend may have completed even though no reply reaches SQLite.
        append_trace(trace, {"event": "backend_completed", "peer": 0, "raw": asdict(response)})
        seen = sum(e["event"] == "backend_completed" for e in read_trace(trace))
        if mode == "interrupt_always" or seen == 1:
            os._exit(77)
    if mode == "invalid" and view.slot.round_number == 1:
        if view.peer == 0:
            response = raw_reply(TOKENIZER, "{invalid literal \ud800")
        elif view.peer == 1:
            response = replace(raw_reply(TOKENIZER, '{"candidate": ['), termination="length", truncated=True)
        elif view.peer == 2:
            response = reply(TOKENIZER, view, candidate=[-999] * len(placeholder(view)))
        else:
            response = RecordedFailure("timeout", "known scripted backend timeout")
    if mode == "defect":
        raise ValueError("diagnosed CPU adapter defect")
    if mode == "explicit_interrupt" and view.peer == 0:
        raise InfrastructureInterruption("declared backend interruption without response")
    return response


def process_alive(pid):
    if os.name == "nt":
        import ctypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.OpenProcess.argtypes = (ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong)
        kernel.WaitForSingleObject.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
        kernel.CloseHandle.argtypes = (ctypes.c_void_p,)
        handle = kernel.OpenProcess(0x100000, False, pid)
        if not handle:
            return False
        try:
            return kernel.WaitForSingleObject(handle, 0) == 258
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


class AttemptLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "worker.sqlite"
        self.world = case_world(Task.SORT)
        self.branch = prefix_branch(self.world)
        with DurableRunner(self.path, TOKENIZER, provider, scripted=True) as runner:
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


class ProcessAttemptTests(unittest.TestCase):
    evidence = []  # Derived validation traces only; never scientific authority.

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "worker.sqlite"
        self.trace = Path(self.temp.name) / "physical.jsonl"
        self.world = case_world(Task.SORT)
        self.branch = prefix_branch(self.world)

    def boundary(self, mode="normal", timeout=5):
        return ProcessProvider(partial(process_factory, mode, str(self.trace)),
                               timeout_seconds=timeout, termination_seconds=0.25, heartbeat_seconds=0.05)

    def capture(self, runner, label):
        self.evidence.append({"case": label, "calls": [dict(r) for r in runner.store.connection.execute(
            "SELECT * FROM calls ORDER BY round_number,peer")],
            "attempts": [dict(r) for r in runner.store.connection.execute("SELECT * FROM attempts ORDER BY call_id,number")],
            "processes": [dict(r) for r in runner.store.connection.execute("SELECT * FROM provider_processes ORDER BY started_at")],
            "physical_trace": read_trace(self.trace),
            "state": snapshot_bytes(runner.state(self.branch.branch_id)).decode("utf-8")})

    def test_default_bounds_and_direct_provider_guard_prevent_unbounded_inference(self):
        self.assertEqual(ProcessProvider(partial(process_factory, "normal", str(self.trace))).timeout_seconds, 120)
        with self.assertRaisesRegex(ValueError, "ProcessProvider"):
            DurableRunner(self.path, TOKENIZER, provider)
        self.assertFalse(self.path.exists())
        for name, value in (("timeout_seconds", 0), ("timeout_seconds", float("nan")),
                            ("termination_seconds", -1), ("heartbeat_seconds", 61)):
            with self.assertRaises(ValueError):
                ProcessProvider(partial(process_factory, "normal", str(self.trace)), **{name: value})

    def test_resident_slow_process_is_bounded_and_retains_loading_idle_and_seeded_request_records(self):
        with DurableRunner(self.path, TOKENIZER, self.boundary()) as runner:
            runner.start(self.world, self.branch, settings=SETTINGS)
            result = runner.run_round(self.branch.branch_id, 1)
            self.assertEqual(result.committed, run_round(initial_branch(self.world.world, self.branch.branch_id),
                             TOKENIZER, event_provider(TOKENIZER)).committed)
            trace = read_trace(self.trace)
            self.assertEqual([e["event"] for e in trace], ["load"] + ["generation"] * 4)
            self.assertEqual(len({e["pid"] for e in trace}), 1)
            self.assertEqual(Path(trace[0]["module"]).resolve(), Path(sys.modules["recovery.runner"].__file__).resolve())
            for call, actual, view, rendered, native in zip(self.branch.calls, trace[1:],
                    result.barrier.requests.views, result.barrier.requests.rendered, result.barrier.requests.tokenized):
                self.assertEqual(actual["seed"], call.seed)
                self.assertEqual(actual["settings"], SETTINGS)
                self.assertEqual(actual["view"], json.loads(json.dumps(asdict(view))))
                self.assertEqual(actual["rendered"], asdict(rendered))
                self.assertEqual(actual["tokenized"], json.loads(json.dumps(asdict(native))))
            sleep(0.05)  # Allocated idle time must remain inside the process interval.
            runner.reply_provider.close()
            interval = dict(runner.store.connection.execute("SELECT * FROM provider_processes").fetchone())
            self.assertIsNotNone(interval["ready_at"])
            self.assertIsNotNone(interval["stopped_at"])
            self.capture(runner, "resident_seeded_process")

    def test_hung_generation_times_out_once_and_continues_without_prior_candidate_fallback(self):
        with DurableRunner(self.path, TOKENIZER, self.boundary("hang", timeout=5)) as runner:
            runner.start(self.world, self.branch, settings=SETTINGS)
            before = runner.run_round(self.branch.branch_id, 1)
            self.assertEqual(before.committed.peers[0].candidate.status, "valid")
            started = monotonic()
            result = runner.run_round(self.branch.branch_id, 2)
            self.assertLess(monotonic() - started, 12)
            call = self.branch.calls[4].call_id
            self.assertEqual(runner.store.call(call)["status"], "timeout")
            self.assertEqual(len(runner.store.attempts(call)), 1)
            self.assertEqual(runner.store.attempts(call)[0]["termination_reason"], "attempt_timeout")
            self.assertEqual(result.committed.peers[0].candidate.status, "failed")
            self.assertIsNone(result.committed.peers[0].candidate.value)
            self.assertTrue(all(result.committed.peers[p].candidate.status == "valid" for p in (1, 2)))
            self.assertEqual(result.committed.peers[3].candidate.status, "invalid")
            self.assertEqual(runner.run_round(self.branch.branch_id, 2), result)
            for r in (3, 4):
                runner.run_round(self.branch.branch_id, r)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM calls").fetchone()[0], 16)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 16)
            runner.reply_provider.close()
            self.capture(runner, "hung_timeout_continues")
        with DurableRunner(self.path, TOKENIZER) as runner:
            self.assertEqual(runner.store.response(call).status, "timeout")
            runner.run_round(self.branch.branch_id, 2)

    def test_interrupted_backend_retries_identical_inputs_and_preserves_ambiguous_completed_work(self):
        with DurableRunner(self.path, TOKENIZER, self.boundary("interrupt_once")) as runner:
            runner.start(self.world, self.branch, settings=SETTINGS)
            result = runner.run_round(self.branch.branch_id, 1)
            call = self.branch.calls[0].call_id
            attempts = runner.store.attempts(call)
            self.assertEqual([a["status"] for a in attempts], ["interrupted", "completed"])
            self.assertEqual([a["uncertain_completion"] for a in attempts], [1, 0])
            self.assertTrue(all(a["elapsed_seconds"] > 0 for a in attempts))
            actual = [e for e in read_trace(self.trace) if e["event"] == "generation" and e["view"]["peer"] == 0]
            self.assertEqual({k: v for k, v in actual[0].items() if k != "pid"},
                             {k: v for k, v in actual[1].items() if k != "pid"})
            self.assertEqual(result.committed, run_round(initial_branch(self.world.world, self.branch.branch_id),
                             TOKENIZER, event_provider(TOKENIZER)).committed)
            runner.reply_provider.close()
            self.capture(runner, "identical_interruption_retry")

    def test_two_backend_interruptions_exhaust_slot_and_declared_interruption_is_separate_from_timeout(self):
        for mode in ("interrupt_always", "explicit_interrupt"):
            with self.subTest(mode=mode):
                path = Path(self.temp.name) / f"{mode}.sqlite"
                with DurableRunner(path, TOKENIZER, self.boundary(mode)) as runner:
                    runner.start(self.world, self.branch, settings=SETTINGS)
                    result = runner.run_round(self.branch.branch_id, 1)
                    call = self.branch.calls[0].call_id
                    self.assertEqual(runner.store.response(call).status, "infrastructure_failure")
                    self.assertEqual([a["status"] for a in runner.store.attempts(call)], ["interrupted"] * 2)
                    self.assertEqual(result.committed.peers[0].candidate.status, "failed")
                    self.assertIsNone(result.committed.peers[0].candidate.value)
                    runner.reply_provider.close()
                    self.capture(runner, mode)
                with DurableRunner(path, TOKENIZER) as runner:
                    runner.run_round(self.branch.branch_id, 1)
                    self.assertEqual(len(runner.store.attempts(call)), 2)

    def test_invalid_truncated_wrong_and_known_timeout_results_never_resample(self):
        with DurableRunner(self.path, TOKENIZER, self.boundary("invalid")) as runner:
            runner.start(self.world, self.branch, settings=SETTINGS)
            result = runner.run_round(self.branch.branch_id, 1)
            self.assertEqual([r.candidate.status for r in result.barrier.replies], ["invalid", "invalid", "valid", "failed"])
            self.assertEqual(result.barrier.replies[0].generated.text, "{invalid literal \ud800")
            self.assertTrue(result.barrier.replies[1].generated.truncated)
            raw = [runner.store.response(c.call_id) for c in self.branch.calls[:4]]
        with DurableRunner(self.path, TOKENIZER, self.boundary()) as runner:
            self.assertEqual(runner.run_round(self.branch.branch_id, 1), result)
            for c, outcome in zip(self.branch.calls, raw):
                self.assertEqual(runner.store.response(c.call_id), outcome)
                self.assertEqual(len(runner.store.attempts(c.call_id)), 1)
            for r in (2, 3, 4):
                runner.run_round(self.branch.branch_id, r)
            self.assertEqual(sum(e["event"] == "generation" for e in read_trace(self.trace)), 16)
            runner.reply_provider.close()
            self.capture(runner, "literal_invalid_wrong_timeout")

    def test_hung_loading_times_out_before_generation_and_status_reads_remain_responsive(self):
        import threading
        observations = []
        finished = threading.Event()

        def observe():
            while not finished.is_set():
                if self.path.exists():
                    with closing(sqlite3.connect(f"file:{self.path.as_posix()}?mode=ro", uri=True, timeout=0.5)) as db:
                        try:
                            observations.extend(db.execute("SELECT status,observed_seconds FROM attempts").fetchall())
                        except sqlite3.OperationalError:
                            pass  # Initial schema transaction has not completed.
                finished.wait(0.02)

        reader = threading.Thread(target=observe, daemon=True)
        reader.start()
        try:
            with DurableRunner(self.path, TOKENIZER, self.boundary("hang_load", timeout=1)) as runner:
                runner.start(self.world, self.branch, settings=SETTINGS)
                started = monotonic()
                result = runner.run_round(self.branch.branch_id, 1)
                self.assertLess(monotonic() - started, 8)
                self.assertEqual([r.candidate.status for r in result.barrier.replies], ["failed"] * 4)
                self.assertEqual(sum(e["event"] == "generation" for e in read_trace(self.trace)), 0)
                self.assertTrue(all(r[0] is None for r in runner.store.connection.execute("SELECT ready_at FROM provider_processes")))
                self.capture(runner, "hung_load_timeout_status")
        finally:
            finished.set()
            reader.join(1)
        self.assertTrue(any(status == "running" and elapsed > 0 for status, elapsed in observations))
        self.assertTrue(any(status == "timeout" for status, elapsed in observations))

    def test_adapter_defect_stops_without_retry_or_turning_unknown_work_into_a_model_error(self):
        with DurableRunner(self.path, TOKENIZER, self.boundary("defect")) as runner:
            initial = runner.start(self.world, self.branch, settings=SETTINGS)
            with self.assertRaisesRegex(ProviderDefect, "diagnosed CPU adapter defect"):
                runner.run_round(self.branch.branch_id, 1)
            self.assertEqual(runner.state(self.branch.branch_id), initial)
            self.assertEqual(runner.store.attempts(self.branch.calls[0].call_id)[0]["status"], "blocked")
            self.assertTrue(all(runner.store.call(c.call_id)["raw_json"] is None for c in self.branch.calls[:4]))
        with DurableRunner(self.path, TOKENIZER, self.boundary()) as runner:
            with self.assertRaises(UnresolvedAttempt):
                runner.run_round(self.branch.branch_id, 1)
            self.assertEqual(sum(e["event"] == "generation" for e in read_trace(self.trace)), 1)

    def test_context_overflow_stops_before_factory_or_attempt_and_preserves_unknown_opportunities(self):
        from recovery.prompts import MAX_CONTEXT_TOKENS
        from tests.round_checks import RoundTokenizer

        class Oversized(RoundTokenizer):
            def __call__(self, *args, **kwargs):
                return {"input_ids": [1] * MAX_CONTEXT_TOKENS, "attention_mask": [1] * MAX_CONTEXT_TOKENS}
        with DurableRunner(self.path, Oversized(), self.boundary()) as runner:
            before = runner.start(self.world, self.branch, settings=SETTINGS)
            with self.assertRaisesRegex(ValueError, "context limit"):
                runner.run_round(self.branch.branch_id, 1)
            self.assertEqual(runner.state(self.branch.branch_id), before)
            self.assertEqual(runner.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0], 0)
            self.assertFalse(self.trace.exists())

    def test_unconfirmed_termination_stops_promptly_without_retrying_a_known_timeout(self):
        boundary = self.boundary("hang", timeout=5)
        with DurableRunner(self.path, TOKENIZER, boundary) as runner:
            runner.start(self.world, self.branch, settings=SETTINGS)
            runner.run_round(self.branch.branch_id, 1)
            process = boundary._process
            started = monotonic()
            with patch.object(process, "terminate"), patch.object(process, "kill"):
                with self.assertRaisesRegex(UnresolvedAttempt, "termination could not be confirmed"):
                    runner.run_round(self.branch.branch_id, 2)
                self.assertLess(monotonic() - started, 7)
                self.assertEqual(runner.store.response(self.branch.calls[4].call_id).status, "timeout")
                self.assertEqual(len(runner.store.attempts(self.branch.calls[4].call_id)), 1)
                with self.assertRaises(UnresolvedAttempt):
                    runner.run_round(self.branch.branch_id, 2)
            boundary.close()  # Real termination after the bounded fault injection.

    def kill_at_point(self, point, *, mode="normal", timeout=5):
        output_path = Path(self.temp.name) / "controller.log"
        env = dict(os.environ, PYTHONPATH=os.pathsep.join(p for p in sys.path if p))
        with output_path.open("ab") as output:
            process = subprocess.Popen([sys.executable, "-m", "tests.attempt_worker",
                "--path", str(self.path), "--trace", str(self.trace), "--point", point,
                "--timeout", str(timeout), "--mode", mode], stdout=output, stderr=subprocess.STDOUT, env=env)
            try:
                deadline = monotonic() + 12
                while monotonic() < deadline:
                    events = read_trace(self.trace)
                    if point == "loading":
                        reached = any(e["event"] == "load" for e in events)
                    else:
                        reached = any(e["event"] == "controller_point" and e["point"] == point for e in events)
                    if reached:
                        break
                    if process.poll() is not None:
                        self.fail(output_path.read_text(encoding="utf-8"))
                    sleep(0.02)
                else:
                    self.fail("controller did not reach the real persistence boundary")
                with closing(sqlite3.connect(self.path)) as db:
                    pid = db.execute("SELECT pid FROM provider_processes ORDER BY started_at DESC LIMIT 1").fetchone()[0]
                self.assertTrue(process_alive(pid))
                process.kill()
                process.wait(timeout=5)
                deadline = monotonic() + 5
                while process_alive(pid) and monotonic() < deadline:
                    sleep(0.02)
                self.assertFalse(process_alive(pid), "orphaned inference survived its controller")
            finally:
                if process.poll() is None:
                    process.kill()
                process.wait(timeout=5)

    def test_killed_controller_before_raw_commit_retries_exactly_once_and_matches_uninterrupted_effects(self):
        self.kill_at_point("before_raw")
        with DurableRunner(self.path, TOKENIZER, self.boundary()) as runner:
            result = runner.run_round(self.branch.branch_id, 1)
            self.assertEqual(result.committed, run_round(initial_branch(self.world.world, self.branch.branch_id),
                             TOKENIZER, event_provider(TOKENIZER)).committed)
            attempts = runner.store.attempts(self.branch.calls[0].call_id)
            self.assertEqual([a["status"] for a in attempts], ["interrupted", "completed"])
            self.assertIsNone(attempts[0]["elapsed_seconds"])
            self.assertIsNone(attempts[0]["finished_at"])
            self.assertGreater(attempts[0]["observed_seconds"], 0)
            self.assertEqual(attempts[0]["uncertain_completion"], 1)
            generations = [e for e in read_trace(self.trace) if e["event"] == "generation" and e["view"]["peer"] == 0]
            self.assertEqual({k: v for k, v in generations[0].items() if k != "pid"},
                             {k: v for k, v in generations[1].items() if k != "pid"})
            runner.reply_provider.close()
            self.capture(runner, "killed_before_raw")

    def test_killed_controller_after_durable_invalid_reply_never_resamples_it(self):
        self.kill_at_point("after_raw", mode="invalid")
        with closing(WorkerStore(self.path)) as store:
            raw = store.response(self.branch.calls[0].call_id)
            self.assertEqual(raw.text, "{invalid literal \ud800")
            self.assertIsNone(store.call(self.branch.calls[0].call_id)["validation_json"])
        with DurableRunner(self.path, TOKENIZER, self.boundary()) as runner:
            result = runner.run_round(self.branch.branch_id, 1)
            self.assertEqual(result.barrier.replies[0].generated, raw)
            self.assertEqual(result.committed.peers[0].candidate.status, "invalid")
            self.assertIsNone(result.committed.peers[0].candidate.value)
            self.assertEqual(len(runner.store.attempts(self.branch.calls[0].call_id)), 1)
            self.assertEqual(sum(e["event"] == "generation" and e["view"]["peer"] == 0
                                 for e in read_trace(self.trace)), 1)
            runner.reply_provider.close()
            self.capture(runner, "killed_after_invalid_raw")

    def test_two_killed_controllers_exhaust_without_a_third_physical_attempt(self):
        self.kill_at_point("before_raw")
        # A fresh trace boundary must be reached on the second physical attempt.
        self.trace = Path(self.temp.name) / "second-physical.jsonl"
        self.kill_at_point("before_raw")
        with DurableRunner(self.path, TOKENIZER, self.boundary()) as runner:
            result = runner.run_round(self.branch.branch_id, 1)
            attempts = runner.store.attempts(self.branch.calls[0].call_id)
            self.assertEqual([a["status"] for a in attempts], ["interrupted"] * 2)
            self.assertTrue(all(a["uncertain_completion"] for a in attempts))
            self.assertEqual(runner.store.response(self.branch.calls[0].call_id).status, "infrastructure_failure")
            self.assertEqual(result.committed.peers[0].candidate.status, "failed")
            self.assertEqual(sum(e["event"] == "generation" and e["view"]["peer"] == 0
                                 for e in read_trace(self.trace)), 1)
            runner.reply_provider.close()
            self.capture(runner, "two_killed_controllers")

    def test_killed_controller_after_known_timeout_decision_cannot_reopen_that_slot(self):
        self.kill_at_point("after_timeout", timeout=5)
        with DurableRunner(self.path, TOKENIZER, self.boundary(timeout=5)) as runner:
            result = runner.run_round(self.branch.branch_id, 1)
            attempts = runner.store.attempts(self.branch.calls[0].call_id)
            self.assertEqual(len(attempts), 1)
            self.assertEqual(attempts[0]["status"], "timeout")
            self.assertEqual(attempts[0]["termination_reason"], "timeout_termination_pending")
            self.assertEqual(runner.store.response(self.branch.calls[0].call_id).status, "timeout")
            self.assertEqual(result.committed.peers[0].candidate.status, "failed")
            self.assertEqual(sum(e["event"] == "generation" and e["view"]["peer"] == 0
                                 for e in read_trace(self.trace)), 1)
            runner.reply_provider.close()
            self.capture(runner, "killed_during_timeout_termination")

    def test_killed_loading_process_dies_with_owner_and_retry_reloads_from_saved_state(self):
        self.kill_at_point("loading")
        with DurableRunner(self.path, TOKENIZER, self.boundary()) as runner:
            result = runner.run_round(self.branch.branch_id, 1)
            self.assertEqual([a["status"] for a in runner.store.attempts(self.branch.calls[0].call_id)],
                             ["interrupted", "completed"])
            self.assertEqual(result.committed, run_round(initial_branch(self.world.world, self.branch.branch_id),
                             TOKENIZER, event_provider(TOKENIZER)).committed)
            self.assertEqual(sum(e["event"] == "load" for e in read_trace(self.trace)), 2)
            runner.reply_provider.close()
            self.capture(runner, "killed_loading_reloads")
