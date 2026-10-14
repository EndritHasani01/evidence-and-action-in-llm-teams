"""Focused scripted integration only. No model qualification/pilot/main run."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
import sys

from recovery.i01.core import canonical
from recovery.i01.workflow import Session, initialize
from recovery.i01.report import analysis, write_report


class Scripted:
    def __init__(self, actions):
        self.actions=list(actions); self.calls=0
    def obtain(self, request, timeout):
        self.calls+=1
        text=canonical(self.actions.pop(0))
        return dict(visible_text=text,raw_text=text,token_ids=[1],truncated=False,
                    failure=None,ready_seconds=.001,generated_tokens=1,input_tokens=1)
    def close(self): return dict(termination_confirmed=True)


def prepare(view,seed,mode,**flags):
    return dict(view=view,seed=seed,settings={"mode":mode},input_ids=[1],rendered=canonical(view),**flags)


class Integration(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="i01-integration-")
        self.run=Path(self.temp.name)/"run"
        root=Path(__file__).parents[1]
        initialize(self.run,root,json.loads((root/"configs/i01-course.json").read_text()))
        self.session=None
    def tearDown(self):
        if self.session: self.session.close()
        self.temp.cleanup()
    def open(self, actions):
        worker=Scripted(actions)
        self.session=Session(self.run,providers=[worker,Scripted([])],prepare_request=prepare)
        self.session.window((datetime.now(timezone.utc)+timedelta(hours=2)).isoformat(),"scripted test allowance")
        return self.session,worker
    def test_raw_resume_literal_siblings_report(self):
        actions=[dict(message="<script>alert(1)</script>",submit=None,wait=False),
                 dict(message="global",submit=999,wait=False),dict(message="agree",submit=999,wait=False)]
        s,w=self.open(actions)
        world=s.manifest["worlds"][6]
        store=s.stores[world["device"]]
        original=store.effects
        def crash(*args): raise RuntimeError("scripted crash after raw persistence")
        store.effects=crash
        with self.assertRaises(RuntimeError): s.episode(world,"prefix","direct")
        self.assertEqual(w.calls,1)
        self.assertEqual(s.admission.usage()["attempts"],1)
        store.effects=original
        prefix=s.episode(world,"prefix","direct")
        self.assertEqual(w.calls,3)
        self.assertEqual(prefix["terminal"],"both_submitted")
        self.assertEqual(s.episode(world,"prefix","direct"),prefix)
        self.assertEqual(w.calls,3)
        from recovery.i01.core import initial_episode
        self.assertEqual(initial_episode(world,"retain",prefix)["history"],prefix["history"])
        self.assertEqual(initial_episode(world,"clear",prefix)["history"],[[],[]])
        report=write_report(self.run,self.run/"reports")
        html=(self.run/"reports/conversations.html").read_text()
        self.assertNotIn("<script>alert",html)
        self.assertIn("&lt;script&gt;",html)
        self.assertEqual(report["summary"]["known_pairs"],0)
        checkpoint=s.checkpoint("scripted-raw-resume")
        self.assertEqual(checkpoint["attempts"],3)
    def test_missing_prerequisites_no_attempts(self):
        s,w=self.open([])
        for call in (lambda:s.pilot(1),lambda:s.main(),lambda:s.freeze("review"),lambda:s.screen("thinking","competence")):
            with self.assertRaises(ValueError): call()
        self.assertEqual(s.admission.usage()["attempts"],0)
        self.assertEqual(w.calls,0)
    def test_restore_reload_cannot_relabel_cached_envelope(self):
        s,w=self.open([])
        s.meta.put_meta("screen/direct",dict(passed=True))
        s.meta.put_meta("envelope",dict(passed=True,mode="direct",session="old-session"))
        with self.assertRaises(ValueError): s.envelope("direct")
        self.assertEqual(w.calls,0)
    def test_read_only_full_population(self):
        result=analysis(self.run)
        self.assertEqual(result["summary"]["intended_worlds"],20)
        self.assertEqual(result["summary"]["missingness_bounds"],[-1,1])
        self.assertEqual(result["summary"]["attempts"],0)
    def test_retained_client_and_explicit_fallback(self):
        from recovery.i01.client import Client
        root=Path(__file__).parents[1]
        client=Client(sys.executable,root,self.run,Path(self.temp.name)/"cache")
        try:
            first=client.command("status")
            result=client.action("prepare_batch",count=1)
            self.assertIn("prerequisite",result["error"])
            self.assertEqual(client.command("status")["usage"]["attempts"],0)
            self.assertEqual(first["session"],client.command("status")["session"])
            self.assertEqual(result["checkpoint"]["integrity"],"passed")
        finally:
            client.close()
    def test_parallel_writers_quiesce_for_snapshot(self):
        from concurrent.futures import ThreadPoolExecutor
        import threading
        import time
        actions=[dict(message=None,submit=999,wait=False)]*2
        s,w=self.open(actions)
        s.workers[1]=Scripted(actions)
        ready=threading.Barrier(2)
        for worker in s.workers:
            original=worker.obtain
            def slow(req,timeout,original=original):
                ready.wait(timeout=5); time.sleep(.05)
                return original(req,timeout)
            worker.obtain=slow
        worlds=s.manifest["worlds"][6:8]
        with ThreadPoolExecutor(max_workers=2) as pool:
            states=list(pool.map(lambda world:s.episode(world,"prefix","direct"),worlds))
        self.assertTrue(all(e["terminal"]=="both_submitted" for e in states))
        self.assertFalse(s.active_calls)
        receipt=s.checkpoint("scripted-parallel")
        self.assertEqual(receipt["attempts"],4)
        self.assertEqual(receipt["integrity"],"passed")
    def test_named_study_steps_use_real_controller(self):
        from recovery.i01.notebook import Study
        base=Path(self.temp.name)
        ui=Study(Path(__file__).parents[1],base/"scratch",base/"working",self.run)
        self.assertTrue(callable(ui.install_runtime))
        self.assertEqual(ui.run_dir,self.run)
        with self.assertRaises(ValueError): ui.show_status()
        # Real UI -> retained client -> controller, with no model or GPU call.
        ui.environment=dict(interpreter=sys.executable)
        ui.show=lambda value:None
        ui.links=lambda:None
        ui.emit=lambda event:None
        try:
            ui.open('reopen',deadline=(datetime.now(timezone.utc)+timedelta(hours=2)).isoformat(),allowance_evidence='Scripted controller window only')
            self.assertEqual(ui.show_status()["usage"]["attempts"],0)
            from recovery.i01.ui import ActionStopped
            with self.assertRaises(ActionStopped): ui.prepare_main_batch(count=1)
            self.assertEqual(ui.client.command('forecast')['remaining_attempt_allowance'],500)
            receipt=ui.save_checkpoint(verify=True)
            self.assertEqual(receipt["checkpoint"]["integrity"],"passed")
            self.assertEqual(ui.show_status()["known_pairs"],0)
        finally:
            if ui.client: ui.client.close()


if __name__=="__main__": unittest.main()
