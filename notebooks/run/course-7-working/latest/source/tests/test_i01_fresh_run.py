"""Fresh Run All/accounting regressions; scripted replies only, never a model."""
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from recovery.i01.archive import export, extract_selected
from recovery.i01.notebook import Study
from recovery.i01.report import analysis, write_report
from recovery.i01.store import restore_tail
from recovery.i01.workflow import initialize, Session
from scripts.build_i01_course_notebook import notebook, research_notebook
from scripts.verify_i01_course_release import verify_notebook, verify_research_notebook
from tests.test_i01_course3_repairs import Scripted, prepare

ROOT=Path(__file__).parents[1]
CONFIG=json.loads((ROOT/'configs/i01-course.json').read_text())


class FreshRun(unittest.TestCase):
    def test_both_notebook_names_deliver_the_complete_run_all(self):
        with redirect_stdout(io.StringIO()):
            fresh=verify_notebook(notebook())
            research=verify_research_notebook(research_notebook())
        self.assertEqual(fresh['code_cells'],33)
        self.assertEqual(research['code_cells'],33)
        self.assertEqual(fresh['first_attempt_ceiling'],460)

    def test_fresh_twenty_attempt_preparation_replay_and_checkpoint(self):
        with tempfile.TemporaryDirectory(prefix='i01-fresh-') as name:
            run=Path(name)/'study'
            manifest=initialize(run,ROOT,CONFIG,independent=True)
            workers=[Scripted(),Scripted()]
            s=Session(run,ROOT,providers=workers,prepare_request=prepare)
            try:
                before=s.admission.usage()
                self.assertEqual(before['remaining'],500)
                self.assertEqual(before['attempt_scope'],'independent-study')
                self.assertEqual(before['missing_prior_studies'],[])
                self.assertEqual(before['prior_attempts'],0)
                s.window((datetime.now(timezone.utc)+timedelta(hours=2)).isoformat(),'Scripted fixture only')
                s.meta.put_meta('loaded_session',s.session_id)
                for i,store in enumerate(s.stores):store.put_meta('resident_load',f'{s.session_id}/scripted-{i}')
                self.assertTrue(s.readiness()['passed'])
                q=s.screen('direct')
                self.assertTrue(q['passed']);self.assertEqual(q['correct'],0)
                self.assertTrue(s.envelope()['passed'])
                self.assertEqual(sum(w.calls for w in workers),20)
                self.assertEqual(s.admission.usage()['remaining'],480)
                self.assertEqual(s.admission.usage()['contingency'],0)
                s.readiness();s.screen('direct');s.envelope()
                self.assertEqual(sum(w.calls for w in workers),20)
                self.assertEqual(initialize(run,ROOT,CONFIG,independent=True)['study_id'],manifest['study_id'])
                write_report(run,run/'reports',plot=False)
                saved=analysis(run)
                self.assertEqual(saved['summary']['prior_attempts'],0)
                self.assertEqual(saved['summary']['known_pairs'],0)
                self.assertEqual(saved['summary']['missingness_bounds'],[-1,1])
                self.assertEqual(saved['qualification']['thinking']['recorded'],0)
                self.assertFalse(any(a['stage'] in ('thinking','pilot','main') for a in saved['attempts']))
                receipt=export(run,s.stores,boundary='scripted-fresh-preparation')
            finally:s.close()
            restored=Path(name)/'restored'
            extract_selected(receipt['path'],restored)
            self.assertEqual(analysis(restored),saved)
            reopened=Session(restored,ROOT)
            try:
                self.assertEqual(reopened.admission.usage()['remaining'],480)
                restore_tail(reopened.meta,'unknown','Fixture: unbounded additional tail',boundary='test')
                self.assertIsNone(reopened.admission.usage()['remaining'])
                restore_tail(reopened.meta,'latest','Fixture: latest does not erase old uncertainty',boundary='test-later')
                self.assertIsNone(reopened.admission.usage()['remaining'])
            finally:reopened.close()

    def test_explicit_fresh_request_cannot_convert_or_reset_existing_campaign(self):
        with tempfile.TemporaryDirectory(prefix='i01-fresh-guard-') as name:
            run=Path(name)/'shared'
            manifest=initialize(run,ROOT,CONFIG)
            with self.assertRaisesRegex(ValueError,'fresh destination'):
                initialize(run,ROOT,CONFIG,independent=True)
            self.assertEqual(json.loads((run/'run.json').read_text()),manifest)
            self.assertEqual(analysis(run)['summary']['attempt_scope'],'shared-campaign')
            self.assertIsNone(analysis(run)['summary']['remaining_attempt_allowance'])

    def test_fresh_facade_keeps_preparation_deadline_and_window_reruns_do_not_extend(self):
        with tempfile.TemporaryDirectory(prefix='i01-fresh-window-') as name:
            with patch('recovery.i01.ui.host_inventory',return_value={}):
                study=Study(ROOT,Path(name)/'scratch',Path(name)/'working',Path(name)/'run')
            study.show=lambda value:None
            study.configure_session(remaining_minutes=30,evidence='Scripted provider observation')
            deadline=study.deadline
            with patch.object(study,'open',return_value={}) as opened:
                study.start_new()
            opened.assert_called_once_with('new',independent=True,deadline=deadline,
                                          allowance_evidence='Scripted provider observation')
            with redirect_stdout(io.StringIO()):
                study.configure_session(remaining_minutes=30,evidence='Rerun is not a new allowance')
            self.assertEqual(study.deadline,deadline)

    def test_independent_restore_or_prior_import_refuses_before_controller(self):
        with tempfile.TemporaryDirectory(prefix='i01-fresh-conflict-') as name:
            with patch('recovery.i01.ui.host_inventory',return_value={}):
                study=Study(ROOT,Path(name)/'scratch',Path(name)/'working',Path(name)/'run')
            study.environment={'interpreter':'not-executed'}
            for args in (dict(mode='restore',independent=True),
                         dict(mode='new',independent=True,prior_checkpoints=['old.zip']),
                         dict(mode='new',independent=True,selected='old.zip')):
                with self.assertRaisesRegex(ValueError,'without prior checkpoints'):
                    study.initialize(**args)
            self.assertIsNone(study.client)


if __name__=='__main__':unittest.main()
