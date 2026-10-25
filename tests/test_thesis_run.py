"""Thesis controller through real spawned model processes with a scripted double.

Covers specification section 8 table B: interruption, timeout, provider
failure, raw-before-effects resume, session loss and restore, deadlines,
ceilings, gates, authorization, ownership and binding. No GPU or model.
"""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from recovery.thesis.checkpoint import DirectoryMirror
from recovery.thesis.run import Profile, Stop, close_controller, open_controller
from recovery.thesis.worlds import load_manifest

ROOT = Path(__file__).parents[1]
MANIFEST, _ = load_manifest(ROOT)
WORLDS = {w["id"]: w for w in MANIFEST["worlds"]}
NOW = lambda: datetime.now(timezone.utc)  # noqa: E731


def seed(model, wid, phase, agent, k):
    return WORLDS[wid]["seeds"][model][phase][agent][k]


def first_prefix_seed(model, wid):
    w = WORLDS[wid]
    return seed(model, wid, "prefix", w["first"], 0)


class Harness(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="thesis-run-"))
        self.lines = []
        self.mirror = DirectoryMirror(self.tmp / "mirror")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def profile(self, **kw):
        base = dict(name="rehearsal", scripted=True, development=("dev-00",), main_limit=1,
                    gates_informational=True, heartbeat_seconds=3600)
        base.update(kw)
        return Profile(**base)

    def open(self, profile, *, run="run", session="s1", start_new=True, scope="rehearsal",
             study="t-rehearsal", deadline=None, roots=(), commit="test", restore=True):
        ctl = open_controller(self.tmp / run, study=study, source=ROOT, source_commit=commit, scope=scope,
                              session=session, session_start=NOW(), deadline=deadline or NOW() + timedelta(hours=11),
                              scratch=self.tmp / "scratch", start_new=start_new, roots=roots, mirror=self.mirror,
                              progress=self.lines.append, profile=profile, restore_allowed=restore)
        if ctl.meta("input_limit") is None:
            ctl.bind("input_limit", 8192)
        ctl.put("checks", dict(passed=True, binding=ctl.store.meta("binding")))
        return ctl

    def attempts(self, ctl, call_id):
        with ctl.db() as s:
            return s.db.execute("SELECT number, status, contingency, stage FROM attempts WHERE call_id=? ORDER BY number",
                                (call_id,)).fetchall()

    def outcome(self, ctl, call_id):
        with ctl.db() as s:
            row = s.call(call_id)
        return json.loads(row["outcome"]) if row and row["outcome"] else None


class Pipeline(Harness):
    def test_rehearsal_pipeline_restore_and_identical_analysis(self):
        from recovery.thesis.analysis import analyse
        ctl = self.open(self.profile())
        try:
            report = ctl.develop()
            self.assertEqual(set(report["models"]), {"qwen", "granite"})
            frozen = ctl.freeze(report["id"])
            self.assertEqual((frozen["n"], frozen["models"]), (1, ["qwen", "granite"]))
            status = ctl.main()
            self.assertEqual(status, {"qwen": dict(complete=1, intended=1), "granite": dict(complete=1, intended=1)})
            ctl.maybe_checkpoint(force=True, reason="test")
        finally:
            close_controller(ctl)
        first = analyse(self.tmp / "run", draws=200)
        self.assertEqual(first["status"], "complete")
        # All six sibling cells ran from the one prefix, within the per-world ceiling of 44 calls.
        with sqlite3.connect(self.tmp / "run" / "study.sqlite") as db:
            cells = {r[0].split("/")[2] for r in db.execute("SELECT id FROM episodes WHERE id LIKE 'qwen/main-000/%'")}
            main_calls = db.execute("SELECT COUNT(*) FROM attempts WHERE stage='main' AND call_id LIKE 'qwen/%'").fetchone()[0]
        self.assertEqual(cells, {"prefix", "RV", "CV", "RP", "CP", "RN", "CN", "control-original", "control-revised"})
        self.assertLessEqual(main_calls, 44)
        result = first["models"]["qwen"]
        for name in ("delta_E", "delta_H", "delta_announce", "delta_answer", "reopening", "delta_H_preserving"):
            self.assertIn(name, result["estimands"])
        self.assertEqual(set(result["channels"]), {"completed", "any_wrong"})
        self.assertEqual(set(result["subgroups"]), {"correct_prefix", "incorrect_prefix", "revised_answer_with_owner",
                                                    "revised_answer_with_partner"})
        self.assertIn("agents_repeating_own_message", result["funnel"]["RP"])
        # A new session with an empty working directory restores from the mirror and repeats nothing.
        ctl2 = self.open(self.profile(), run="run2", session="s2", start_new=False)
        try:
            calls_before = ctl2.counts.copy()
            ctl2.develop()
            ctl2.main()
            self.assertEqual(ctl2.counts, calls_before)
        finally:
            close_controller(ctl2)
        second = analyse(self.tmp / "run2", draws=200)
        for key in ("models", "coverage", "freeze", "gate_report", "model_differences"):
            self.assertEqual(json.dumps(first[key], sort_keys=True), json.dumps(second[key], sort_keys=True), key)

    def test_no_interim_estimates_and_declared_stop_bounds(self):
        from recovery.thesis.analysis import analyse
        ctl = self.open(self.profile(main_limit=2))
        try:
            ctl.freeze(ctl.develop()["id"])
            ctl.run_worlds("qwen", ["main-000"])  # one of two frozen worlds, granite untouched
        except Stop:
            pass
        finally:
            close_controller(ctl)
        result = analyse(self.tmp / "run", draws=200)
        self.assertIn("withheld", result["models"]["qwen"])
        from recovery.thesis.analysis import write_report
        import csv
        write_report(self.tmp / "run", self.tmp / "interim", draws=200, plots=False)
        with (self.tmp / "interim" / "episodes.csv").open(encoding="utf-8") as stream:
            main_rows = [r for r in csv.DictReader(stream) if r["group"] == "main"]
        self.assertTrue(main_rows)
        self.assertTrue(all(r["success"] == "withheld" and r["submission_0"] == "withheld" for r in main_rows))
        self.assertNotIn("Request (user message)", (self.tmp / "interim" / "casebook.md").read_text(encoding="utf-8"))
        ctl = self.open(self.profile(main_limit=2), start_new=False)
        try:
            ctl.declare_stopped("test: campaign ended early")
        finally:
            close_controller(ctl)
        result = analyse(self.tmp / "run", draws=200)
        entry = result["models"]["qwen"]["estimands"]["delta_H"]
        self.assertIn("bounds", entry)
        self.assertLessEqual(entry["estimate_range"][0], entry["estimate_range"][1])


class Faults(Harness):
    def test_process_exit_is_interrupted_then_one_identical_retry(self):
        marker = self.tmp / "exit-marker"
        target = first_prefix_seed("qwen", "dev-00")
        profile = self.profile(behaviors={"qwen": {target: f"once:|{marker}|exit"}})
        ctl = self.open(profile)
        try:
            ctl.develop()
            w = WORLDS["dev-00"]
            call = f"qwen/dev-00/prefix/agent-{w['first']}/invocation-0"
            rows = self.attempts(ctl, call)
            self.assertEqual([(r[1], r[2]) for r in rows], [("interrupted", 0), ("completed", 1)])
            self.assertIsNotNone(self.outcome(ctl, call))
            self.assertTrue(marker.exists())
        finally:
            close_controller(ctl)

    def test_timeout_is_a_recorded_failure_and_the_replica_is_reloaded(self):
        w = WORLDS["dev-00"]
        target = first_prefix_seed("qwen", "dev-00")
        ctl = self.open(self.profile(behaviors={"qwen": {target: "hang"}}, call_timeout=3))
        try:
            ctl.develop()
            call = f"qwen/dev-00/prefix/agent-{w['first']}/invocation-0"
            outcome = self.outcome(ctl, call)
            self.assertEqual(outcome["failure"], "timeout")
            self.assertEqual([r[1] for r in self.attempts(ctl, call)], ["failed"])
            with ctl.db() as s:
                state = s.state("qwen/dev-00/prefix")
            self.assertEqual(state["history"][w["first"]][0],
                             dict(kind="feedback", text="Call failed; no action was delivered."))
            self.assertTrue(any(k.startswith("reload/qwen/") for k in ctl.meta_keys()))
            self.assertTrue(ctl.meta(f"timeout_termination/{call}")["termination_confirmed"])
        finally:
            close_controller(ctl)

    def test_provider_failures_are_recorded_and_stop_beyond_the_limit(self):
        w = WORLDS["dev-00"]
        first, other = w["first"], 1 - w["first"]
        behaviors = {seed("qwen", "dev-00", "prefix", first, 0): "defect",
                     seed("qwen", "dev-00", "prefix", other, 0): "defect"}
        ctl = self.open(self.profile(behaviors={"qwen": behaviors}))
        try:
            with self.assertRaises(Stop) as stop:
                ctl.develop()
            self.assertIn("provider failures", str(stop.exception))
            outcome = self.outcome(ctl, f"qwen/dev-00/prefix/agent-{first}/invocation-0")
            self.assertEqual(outcome["failure"], "provider_defect")
        finally:
            close_controller(ctl)

    def test_raw_reply_before_effects_resumes_without_regeneration(self):
        ctl = self.open(self.profile())
        original = ctl.store.effects
        state = dict(armed=True, call=None)

        def crash_once(call_id, episode, value):
            if state["armed"] and "/prefix/" in call_id:
                state["armed"], state["call"] = False, call_id
                raise RuntimeError("simulated crash after raw persistence")
            return original(call_id, episode, value)

        ctl.store.effects = crash_once
        try:
            with self.assertRaises(RuntimeError):
                ctl.develop()
        finally:
            close_controller(ctl)
        call = state["call"]
        ctl = self.open(self.profile(), start_new=False)
        try:
            self.assertEqual(len(self.attempts(ctl, call)), 1)
            ctl.develop()
            self.assertEqual([r[1] for r in self.attempts(ctl, call)], ["completed"])
            with ctl.db() as s:
                self.assertEqual(s.call(call)["effect_committed"], 1)
        finally:
            close_controller(ctl)

    def test_session_loss_restores_newest_checkpoint_and_retries_in_flight_once(self):
        ctl = self.open(self.profile())
        try:
            ctl.develop()
            w = WORLDS["dev-00"]
            in_flight = f"granite/dev-00/prefix/agent-{w['first']}/invocation-0"
            with ctl.db() as s, s.transaction():
                s.db.execute("DELETE FROM attempts WHERE call_id LIKE 'granite/%'")
                s.db.execute("DELETE FROM calls WHERE id LIKE 'granite/%'")
                s.db.execute("DELETE FROM episodes WHERE id LIKE 'granite/%'")
                s.db.execute("DELETE FROM meta WHERE key LIKE 'gates/granite' OR key = 'gate_report'")
            ctl.counts = ctl._attempt_counts()
            with ctl.db() as s:
                from recovery.thesis.models import ScriptedTokenizer
                from recovery.thesis import protocol
                from recovery.thesis.models import prepare
                state = protocol.start(w, "granite", "prefix")
                request = prepare(protocol.view(w, state, w["first"]), seed("granite", "dev-00", "prefix", w["first"], 0),
                                  ctl.config, "granite", ScriptedTokenizer(), 8192)
                s.start("granite/dev-00/prefix", state)
                s.register(in_flight, "granite/dev-00/prefix", request)
                with s.transaction():
                    s.db.execute("INSERT INTO attempts(call_id,number,stage,contingency,admitted_at,status) VALUES (?,?,?,?,?,?)",
                                 (in_flight, 1, "development", 0, NOW().isoformat(), "admitted"))
            receipt = ctl.maybe_checkpoint(force=True, reason="before loss")
        finally:
            ctl.store.close()
            ctl.ownership.close()
        lost_dir = self.tmp / "run"
        shutil.rmtree(lost_dir)  # the session and its working directory are gone
        ctl = self.open(self.profile(), session="s2", start_new=False, roots=[self.tmp / "mirror"])
        try:
            self.assertEqual(ctl.meta("checkpoint_seq"), receipt["seq"])
            self.assertEqual([r[1] for r in self.attempts(ctl, in_flight)], ["lost"])
            ctl.develop()
            rows = self.attempts(ctl, in_flight)
            self.assertEqual([(r[1], r[2]) for r in rows], [("lost", 0), ("completed", 1)])
            self.assertIsNotNone(ctl.meta("gate_report"))
        finally:
            close_controller(ctl)

    def test_newer_checkpoint_elsewhere_refuses_stale_local_study(self):
        ctl = self.open(self.profile())
        try:
            ctl.maybe_checkpoint(force=True)
            ctl.maybe_checkpoint(force=True)
        finally:
            close_controller(ctl)
        db = sqlite3.connect(self.tmp / "run" / "study.sqlite")
        db.execute("UPDATE meta SET value='1' WHERE key='checkpoint_seq'")
        db.commit()
        db.close()
        with self.assertRaises(Stop) as stop:
            self.open(self.profile(), start_new=False, roots=[self.tmp / "mirror"])
        self.assertIn("newer checkpoint", str(stop.exception))


class Gates(Harness):
    def test_dispatch_cutoff_stops_before_new_episodes(self):
        ctl = self.open(self.profile(), deadline=NOW() + timedelta(minutes=20))
        try:
            with self.assertRaises(Stop) as stop:
                ctl.develop()
            self.assertIn("time", str(stop.exception))
            with ctl.db() as s:
                dev = s.db.execute("SELECT COUNT(*) FROM attempts WHERE stage='development'").fetchone()[0]
            self.assertEqual(dev, 0)
        finally:
            close_controller(ctl)

    def test_contingency_ceiling_stops_a_retry(self):
        marker = self.tmp / "m"
        target = first_prefix_seed("qwen", "dev-00")
        ctl = self.open(self.profile(behaviors={"qwen": {target: f"once:|{marker}|exit"}}))
        ctl.config["ceilings"]["contingency"] = 0
        try:
            with self.assertRaises(Stop) as stop:
                ctl.develop()
            self.assertIn("contingency", str(stop.exception))
        finally:
            close_controller(ctl)

    def test_failed_gates_exclude_models_and_block_freeze(self):
        behaviors = {m: {WORLDS["dev-00"]["seeds"][m]["control"][p]: "invalid" for p in ("original", "revised")}
                     for m in ("qwen", "granite")}
        profile = self.profile(name="study", gates_informational=False, behaviors=behaviors)
        ctl = self.open(profile, scope="main", study="t-study")
        try:
            report = ctl.develop()
            for model in ("qwen", "granite"):
                self.assertFalse(report["models"][model]["G2"]["passed"])
                self.assertFalse(report["models"][model]["admitted"])
            with self.assertRaises(Stop) as stop:
                ctl.freeze(report["id"])
            self.assertIn("no model passed", str(stop.exception))
        finally:
            close_controller(ctl)

    def test_forecast_uses_the_44_call_world_and_has_no_fallback(self):
        ctl = self.open(self.profile(name="study", gates_informational=False, main_limit=None), scope="main",
                        study="t-study")
        try:
            for model, g in (("qwen", 8.7), ("granite", 9.0)):
                ctl.put(f"gates/{model}", dict(model=model, complete=True, admitted=True, g_seconds=g))
            fast = ctl.forecast()
            expected = 4 + 1.25 * (44 * 64 * (8.7 + 9.0) + 300 * 9.0) / 3600
            self.assertAlmostEqual(fast["F64"], round(expected, 2), places=2)
            self.assertEqual(fast["chosen_n"], 64)
            self.assertEqual([k for k in fast if k.startswith("F")], ["F64"])
            ctl.put("gates/granite", dict(model="granite", complete=True, admitted=True, g_seconds=85.0))
            slow = ctl.forecast()  # F(64) about 104.5 h > 100 h: no smaller fallback, stop and ask
            self.assertGreater(slow["F64"], 100)
            self.assertIsNone(slow["chosen_n"])
        finally:
            close_controller(ctl)

    def test_authorization_must_match_the_gate_report(self):
        ctl = self.open(self.profile(name="study", gates_informational=False), scope="main", study="t-study")
        try:
            report = ctl.develop()
            with self.assertRaises(Stop):
                ctl.freeze("dev-000000000000")
            with self.assertRaises(Stop):
                ctl.main()
            self.assertIsNone(ctl.meta("freeze"))
            self.assertTrue(report["id"].startswith("dev-"))
        finally:
            close_controller(ctl)

    def test_scope_boundaries(self):
        ctl = self.open(self.profile(name="study"), scope="cpu", study="t-cpu")
        try:
            with self.assertRaises(Stop) as stop:
                ctl.develop()
            self.assertTrue(str(stop.exception).startswith("skipped"))
            with self.assertRaises(Stop):
                ctl.freeze("x")
        finally:
            close_controller(ctl)

    def test_second_live_writer_and_binding_mismatch_are_refused(self):
        ctl = self.open(self.profile())
        close_controller(ctl)
        sleeper = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
        try:
            import socket
            (self.tmp / "run" / "lock.json").write_text(json.dumps(dict(pid=sleeper.pid, host=socket.gethostname(),
                                                                         session="other", command="main")))
            with self.assertRaises(Stop) as stop:
                self.open(self.profile(), start_new=False)
            self.assertIn("owns this study", str(stop.exception))
        finally:
            sleeper.kill()
            sleeper.wait()
        with self.assertRaises(Stop) as stop:
            self.open(self.profile(), start_new=False, commit="another-commit")
        self.assertIn("different source", str(stop.exception))
        ctl = self.open(self.profile(), start_new=False)  # stale lock from a dead process is replaced
        close_controller(ctl)

    def test_missing_study_requires_explicit_start(self):
        with self.assertRaises(Stop) as stop:
            self.open(self.profile(), start_new=False)
        self.assertIn("START_NEW_STUDY", str(stop.exception))


if __name__ == "__main__":
    unittest.main()
