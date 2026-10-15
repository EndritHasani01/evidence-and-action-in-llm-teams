"""Whole-study procedure checks using scripted replies, never GPU/model inference."""
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from recovery.i01.archive import extract_selected
from recovery.i01.core import canonical
from recovery.i01.notebook import Study
from recovery.i01.policy import AUTOMATIC_POLICY
from recovery.i01.report import analysis, write_report
from recovery.i01.workflow import initialize, Session
from tests.test_i01_course3_repairs import Scripted, prepare

ROOT=Path(__file__).parents[1]
CONFIG=json.loads((ROOT/'configs/i01-course.json').read_text())


class RunAll(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='i01-run-all-')
        self.run=Path(self.temp.name)/'run'
        initialize(self.run,ROOT,CONFIG,independent=True)
        self.workers=[Scripted(),Scripted()]
        self.s=Session(self.run,ROOT,providers=self.workers,prepare_request=prepare)
        self.s.window((datetime.now(timezone.utc)+timedelta(minutes=700)).isoformat(),'Scripted planning window only')
        self.s.meta.put_meta('loaded_session',self.s.session_id)
        for n,store in enumerate(self.s.stores):store.put_meta('resident_load',f'{self.s.session_id}/scripted-{n}')
        self.no_plots=patch('recovery.i01.report.figures',return_value=None);self.no_plots.start()
        self.s.plan_execution()
        self.s.readiness();self.s.screen('direct');self.s.envelope()
    def tearDown(self):
        self.s.close();self.no_plots.stop();self.temp.cleanup()
    def pilots(self):
        for n in (1,2,3):self.s.pilot(n);self.s.check_pilot(n)

    def test_whole_study_through_actual_facade_reports_archive_and_free_replay(self):
        s=self.s
        class Client:
            process=SimpleNamespace(poll=lambda:None)
            def command(self,name,**args):
                if name=='status':return s.status()
                if name=='close_models':return s.close_models()
                raise AssertionError(name)
            def action(self,name,**args):return s.run_action(name,**args)
            def close(self):s.close_models()
        with patch('recovery.i01.ui.host_inventory',return_value={}):
            study=Study(ROOT,Path(self.temp.name)/'scratch',Path(self.temp.name),self.run)
        study.client=Client();study.show=lambda value:None;study.links=lambda **args:None;study.inspect=lambda **args:None
        with redirect_stdout(io.StringIO()):
            for n in (1,2,3):study.run_pilot(n);study.check_pilot(n)
            study.admit_main()
            plan=s.meta.meta('execution_plan')
            for n in range(1,11):study.run_main_batch(n)
            before=sum(w.calls for w in self.workers)
            study.run_main_batch(1);study.run_main_batch(10)
            study.run_pilot(1);study.check_pilot(1)
            self.assertEqual(sum(w.calls for w in self.workers),before)
            study.build_report();study.save_checkpoint(verify=True)
            study.finish_session()
        result=analysis(self.run)
        self.assertEqual(result['summary']['status'],'complete')
        self.assertEqual(result['summary']['known_pairs'],20)
        self.assertEqual(result['summary']['paired_counts'],{'neither':20})
        self.assertEqual(result['summary']['qualification']['direct']['correct'],0)
        self.assertEqual(result['summary']['attempts'],184)
        self.assertEqual(result['summary']['prior_attempts'],0)
        self.assertEqual(result['summary']['human_review_status'],'retrospective_pending')
        self.assertEqual(s.meta.meta('execution_plan'),plan)
        self.assertFalse(any(k.startswith('review/') for k in result['summary']['gates']))
        self.assertTrue(all(r['passed'] and r['useful_communication'] is None for r in result['pilot_checks']))
        self.assertTrue((self.run/'reports/pilot_checks.csv').is_file())
        restored=Path(self.temp.name)/'restored'
        extract_selected(self.run/'exports/latest.zip',restored)
        self.assertEqual(analysis(restored),result)

    def test_pilot_protocol_failure_is_recorded_and_blocks_next_pilot_and_main(self):
        for worker in self.workers:
            worker.reply=lambda req:dict(failure=None,visible_text='bad JSON',truncated=False,generated_tokens=1,ready_seconds=.001,input_tokens=1)
        self.s.pilot(1)
        with self.assertRaisesRegex(ValueError,'valid_protocol'):self.s.check_pilot(1)
        before=sum(w.calls for w in self.workers)
        with self.assertRaisesRegex(ValueError,'Previous automatic'):self.s.pilot(2)
        with self.assertRaisesRegex(ValueError,'Three passing'):self.s.admit_main()
        self.assertFalse(self.s.meta.meta('automatic/pilot-1')['passed'])
        self.assertEqual(sum(w.calls for w in self.workers),before)

    def test_no_message_quality_gate_but_original_team_must_finish(self):
        for worker in self.workers:
            worker.reply=lambda req:dict(failure=None,visible_text=canonical(dict(message=None,submit=-1000,wait=False)),
                                        generated_tokens=1,ready_seconds=.001,input_tokens=1)
        self.s.pilot(1)
        receipt=self.s.check_pilot(1)
        self.assertTrue(receipt['passed']);self.assertEqual(receipt['original_messages'],0)
        self.assertIsNone(receipt['useful_communication'])
        # A protocol-legal all-wait original phase is still incomplete, not useful.
        for worker in self.workers:
            worker.reply=lambda req:dict(failure=None,visible_text=canonical(dict(message=None,submit=-1000 if req.get('control') else None,wait=not req.get('control',False))),
                                        generated_tokens=1,ready_seconds=.001,input_tokens=1)
        self.s.pilot(2)
        with self.assertRaisesRegex(ValueError,'original_team_completed'):self.s.check_pilot(2)

    def test_main_invalid_actions_are_outcomes_and_numbered_scopes_do_not_skip(self):
        self.pilots();self.s.admit_main()
        with self.assertRaisesRegex(ValueError,'Previous fixed'):self.s.automatic_main(2)
        for worker in self.workers:
            worker.reply=lambda req:dict(failure=None,visible_text=canonical(dict(message=None,submit=-1000,wait=False)) if req.get('control') else 'bad JSON',
                                        generated_tokens=1,ready_seconds=.001,input_tokens=1)
        first=self.s.automatic_main(1)
        self.assertTrue(first['passed'])
        self.assertGreater(sum(e['protocol_errors'] for e in first['evidence']),0)
        self.assertEqual(analysis(self.run)['summary']['known_pairs'],2)
        self.assertEqual(self.s.automatic_main(2)['worlds'],['main-02','main-03'])

    def test_precommitted_settings_and_tight_time_cannot_be_waived(self):
        self.pilots()
        self.s.prepare_request=lambda view,seed,mode,**flags:dict(prepare(view,seed,mode,**flags),settings={'mode':mode,'changed':True})
        with self.assertRaisesRegex(ValueError,'precommitted'):self.s.admit_main()
        self.s.prepare_request=prepare
        forecast=self.s.forecast()
        self.s.remaining_time=lambda:forecast['conservative_wall_seconds']-1
        with self.assertRaisesRegex(ValueError,'adequate attempt/time'):self.s.admit_main()
        self.assertIsNone(self.s.meta.meta('freeze'))
        self.assertEqual(self.s.meta.meta('execution_plan')['policy'],AUTOMATIC_POLICY)


if __name__=='__main__':unittest.main()
