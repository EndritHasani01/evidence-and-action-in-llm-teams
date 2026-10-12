"""Focused CPU contracts; fixtures grant no actual GPU/resource admission."""

from contextlib import closing
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from recovery.accounting import BudgetStop
from recovery.attempts import InfrastructureInterruption, ProcessProvider
from recovery.protocol import GeneratedReply
from recovery.storage import WorkerStore, settings_json
from scripts.m5_course_preparation import peer_view, read
from scripts.m5_course_smoke import admission, launch_defaults, resources, run, smoke_branch
from recovery.prompts import RenderedRequest, TokenizedRequest

ROOT = Path(__file__).resolve().parents[1]


def known_launch():
    launch = launch_defaults()
    launch.update(authorization="synthetic CPU fixture; no compute approval",provider_session_seconds=3600,
        release_instructions="CPU fixture only",allocated_at="2026-10-12T10:00:00+00:00")
    launch["budget"]["prior_evidence"] = "synthetic zero-prior CPU fixture, never available quota"
    for name in ("development","setup","interruption","other_course","other_overall","smoke"):
        launch["budget"]["prior_"+name+"_gpu_hours"] = [0,0]
    launch["budget"]["prior_smoke_attempts"] = 0
    return launch


class CourseHardwareSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = read(ROOT/"notebooks/validation/course-m5-preparation/inputs/smoke-requests.json.gz")

    def prepare(self, store, index=0):
        row = self.packet["requests"][index]
        view, branch = peer_view(row["view"]), smoke_branch(row)
        rendered = RenderedRequest(**row["rendered"])
        tokens = TokenizedRequest(row["tokenized"]["text"],tuple(row["tokenized"]["input_ids"]),tuple(row["tokenized"]["attention_mask"]))
        store.prepare_control(branch,settings_json(row["settings"]),view,rendered,tokens)
        return row,view,branch,rendered,tokens

    def test_isolated_smoke_uses_actual_peer_and_exact_identity_without_relabelled_controls(self):
        with tempfile.TemporaryDirectory() as directory:
            store = WorkerStore(Path(directory)/"worker.sqlite")
            try:
                for index in (0,5,13):
                    row,view,branch,rendered,tokens = self.prepare(store,index)
                    saved = store.call(row["smoke_call_id"])
                    self.assertEqual(saved["peer"],-1 if view.peer is None else view.peer)
                    self.assertEqual(saved["seed"],row["seed"])
                    self.assertEqual(saved["generation_id"],row["physical_generation_id"])
                    self.assertEqual(branch.phase,"smoke")
                    self.assertIsNone(saved["replay_parent"])
                    self.prepare(store,index)
                    with self.assertRaises(ValueError):
                        store.prepare_control(branch,settings_json(row["settings"]),view,replace(rendered,content="changed"),tokens)
                self.assertEqual(store.connection.execute("SELECT count(*) FROM calls").fetchone()[0],3)
            finally:
                store.close()

    def test_completed_raw_probe_resumes_without_factory_or_admission(self):
        with tempfile.TemporaryDirectory() as directory:
            store = WorkerStore(Path(directory)/"worker.sqlite")
            try:
                row,view,branch,rendered,tokens = self.prepare(store)
                raw = GeneratedReply("invalid literal mock",(1,2),"eos")
                store.begin_attempt(row["smoke_call_id"])
                store.finish_attempt(row["smoke_call_id"],raw,.01)
                def forbidden(*unused):
                    raise AssertionError("a completed physical probe cannot be resampled")
                provider = ProcessProvider(forbidden,before_attempt=forbidden)
                self.assertEqual(provider.obtain(store,row["smoke_call_id"],view,rendered,tokens,
                    seed=row["seed"],settings=row["settings"]),raw)
                self.assertEqual(len(store.attempts(row["smoke_call_id"])),1)
            finally:
                store.close()

    def test_retry_rechecks_physical_admission_and_retains_unresolved_outcome(self):
        with tempfile.TemporaryDirectory() as directory:
            store = WorkerStore(Path(directory)/"worker.sqlite")
            try:
                row,view,branch,rendered,tokens = self.prepare(store)
                seen = []
                def admit(store,call_id,number):
                    seen.append(number)
                    if number == 2:
                        raise BudgetStop("no physical allowance for retry")
                provider = ProcessProvider(lambda:None,before_attempt=admit)
                with patch.object(provider,"_execute",side_effect=InfrastructureInterruption("CPU interrupted")):
                    with self.assertRaises(BudgetStop):
                        provider.obtain(store,row["smoke_call_id"],view,rendered,tokens,seed=row["seed"],settings=row["settings"])
                self.assertEqual(seen,[1,2])
                attempt, = store.attempts(row["smoke_call_id"])
                self.assertEqual(attempt["status"],"interrupted")
                self.assertTrue(attempt["uncertain_completion"])
                self.assertIsNone(store.call(row["smoke_call_id"])["raw_json"])
            finally:
                store.close()

    def test_user_reported_quota_and_stopped_sessions_do_not_erase_unknown_prior_usage(self):
        launch = known_launch()
        launch["budget"]["prior_setup_gpu_hours"] = None
        with self.assertRaisesRegex(BudgetStop,"unknown_prior_allocation"):
            admission(launch,now=launch["allocated_at"])
        launch = known_launch()
        launch["budget"]["prior_smoke_gpu_hours"] = None
        with self.assertRaisesRegex(BudgetStop,"unknown_prior_smoke"):
            admission(launch,now=launch["allocated_at"])

    def test_assignment_delay_both_devices_and_release_reserve_reduce_admission(self):
        launch = known_launch()
        _,wall = admission(launch,now="2026-10-12T10:01:00+00:00",next_attempt=True)
        self.assertEqual(wall,840)
        launch["budget"]["prior_smoke_gpu_hours"] = [.3,.3]
        _,wall = admission(launch,now=launch["allocated_at"],next_attempt=True)
        self.assertAlmostEqual(wall,360)
        with self.assertRaisesRegex(BudgetStop,"insufficient_smoke_time"):
            admission(launch,now="2026-10-12T10:02:00+00:00",next_attempt=True)
        launch["budget"]["prior_smoke_attempts"] = 24
        with self.assertRaisesRegex(BudgetStop,"cumulative_smoke_attempt_limit"):
            admission(launch,now=launch["allocated_at"],next_attempt=True)

    def test_missing_authorization_provider_terms_and_future_clock_are_refused(self):
        for key,value in (("authorization",""),("prior_sessions_released",False),
            ("reported_quota_gpu_hours",None),("provider_session_seconds",None),
            ("release_instructions",""),("allocated_at",None)):
            launch = known_launch()
            launch[key] = value
            with self.subTest(key=key),self.assertRaises(BudgetStop):
                admission(launch,now="2026-10-12T10:00:00+00:00")
        with self.assertRaisesRegex(ValueError,"future"):
            admission(known_launch(),now="2026-10-12T09:59:59+00:00")

    def test_disabled_launch_exports_honest_blocker_without_factory_or_weights(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/"output"
            with patch("scripts.m5_course_smoke.ModelFactory",side_effect=AssertionError("no loading")):
                report = run(ROOT,launch_defaults(),output)
            self.assertEqual(report["status"],"blocked")
            self.assertIn("gpu_execution_disabled",report["root_blocker"])
            self.assertEqual(report["model_generations"],0)
            self.assertFalse(report["physical_memory_accepted"])
            self.assertIsNone(report["complete_live_memory_upper_bound_bytes"])
            self.assertFalse(report["provider_release_confirmed"])
            self.assertTrue((output/"preflight-results.zip").exists())
            self.assertEqual(list(output.glob("worker-*.sqlite")),[])
            with self.assertRaises(FileExistsError):
                run(ROOT,launch_defaults(),output)
