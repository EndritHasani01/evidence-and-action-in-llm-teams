"""Focused course-5 policy, diagnostics and unattended failure regressions."""
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from recovery.i01.core import validate_action, apply_outcome, initial_episode
from recovery.i01.policy import AUTOMATIC_POLICY, RECOVERY_POLICY, validation_detail, runtime_safe
from recovery.i01.report import analysis, write_report
from recovery.i01.notebook import Study
from tests import test_i01_run_all as base

BAD_REPLIES=(
    '{"message":"Agent 0 has submitted 988. My shard maximum is 923. Since 988 > 923, I will not submit a new value. I am waiting for Agent 0\'s final submission confirmation.","submit":null,"wait":true}',
    '{"message":"I see a revision notice updating my shard index 15 to 672. I will wait for the partner\'s submission to confirm the global maximum before finalizing.","submit":null,"wait":true}')


class RecoveryAdmission(unittest.TestCase):
    setUp=base.RunAll.setUp
    tearDown=base.RunAll.tearDown

    def recovery_errors(self):
        for worker in self.workers:
            worker.reply=lambda req:dict(failure=None,visible_text=BAD_REPLIES[req['view']['agent']] if 'revision_notice' in req['view'] else
                '{"message":null,"submit":-1000,"wait":false}',truncated=False,generated_tokens=1,ready_seconds=.001,input_tokens=1)

    def test_exact_replies_remain_invalid_without_delivery_and_pass_only_new_gate(self):
        world=next(w for w in self.s.manifest['worlds'] if w['group']=='pilot')
        for raw in BAD_REPLIES:
            action,error=validate_action(raw)
            self.assertIsNone(action);self.assertEqual(error,'malformed_action')
            detail=validation_detail(dict(visible_text=raw))
            self.assertTrue(detail['json_valid']);self.assertTrue(detail['schema_valid'])
            self.assertFalse(detail['legal_action'])
            self.assertEqual(detail['reason'],'wait_requires_null_message_and_submit')
            state=apply_outcome(initial_episode(world,'prefix'),0,action,error,'test')
            self.assertEqual(state['turns'],[1,0]);self.assertEqual(state['submissions'],[None,None])
            self.assertFalse(state['history'][1])
        self.recovery_errors();self.s.pilot(1)
        before=[store.rows('calls') for store in self.s.stores]
        receipt=self.s.check_pilot(1)
        self.assertTrue(receipt['passed']);self.assertEqual(receipt['recovery_protocol_errors'],12)
        self.assertEqual(before,[store.rows('calls') for store in self.s.stores])
        plan=self.s.meta.meta('execution_plan')
        self.s.meta.put_meta('execution_plan',dict(plan,policy=AUTOMATIC_POLICY))  # Historical-policy fixture only.
        with self.assertRaisesRegex(ValueError,'valid_protocol'):self.s.check_pilot(1)
        self.assertEqual(before,[store.rows('calls') for store in self.s.stores])

    def test_freeze_reconstructs_phase_sensitive_evidence_and_legacy_stays_strict(self):
        self.recovery_errors()
        for n in (1,2,3):self.s.pilot(n);self.s.check_pilot(n)
        plan=self.s.meta.meta('execution_plan')
        self.s.meta.put_meta('execution_plan',dict(plan,policy=AUTOMATIC_POLICY))
        with self.assertRaisesRegex(ValueError,'evidence no longer'):self.s.admit_main()
        self.s.meta.put_meta('execution_plan',plan)
        self.assertEqual(self.s.admit_main()['execution_policy'],RECOVERY_POLICY)
        self.assertEqual(self.s.admission.usage()['contingency'],0)

    def test_baseline_state_errors_cannot_hide_behind_legal_raw_calls(self):
        self.s.pilot(1)
        world=next(w for w in self.s.manifest['worlds'] if w['group']=='pilot')
        store=self.s.stores[world['device']]
        state=store.state(world['id']+'/prefix')
        state['events'][0]['error']='malformed_action'  # Inconsistent-state fixture.
        with store.transaction():store.db.execute('UPDATE episodes SET state=? WHERE id=?',(json.dumps(state),world['id']+'/prefix'))
        with self.assertRaisesRegex(ValueError,'valid_protocol'):self.s.check_pilot(1)

    def test_invalid_controls_and_unconfirmed_termination_or_backend_still_block(self):
        self.recovery_errors();self.s.pilot(1)
        world=next(w for w in self.s.manifest['worlds'] if w['group']=='pilot')
        store=self.s.stores[world['device']]
        call=next(r for r in store.rows('calls') if r['episode']==world['id']+'/retain')
        raw=json.loads(call['outcome'])
        for defect in (dict(failure='provider_defect'),dict(failure='timeout',termination_pending=True)):
            with store.transaction():store.db.execute('UPDATE calls SET outcome=? WHERE id=?',(json.dumps(dict(raw,**defect)),call['id']))
            with self.assertRaisesRegex(ValueError,'runtime_integrity'):self.s.check_pilot(1)
        store.put_meta('timeout_termination/'+call['id'],dict(termination_confirmed=True,reason='Scripted confirmed death'))
        self.assertTrue(self.s.check_pilot(1)['passed'])
        control=next(r for r in store.rows('calls') if r['episode']==world['id']+'/control-original-direct')
        with store.transaction():store.db.execute('UPDATE calls SET outcome=? WHERE id=?',(json.dumps(dict(raw,visible_text=BAD_REPLIES[0])),control['id']))
        with self.assertRaisesRegex(ValueError,'valid_protocol'):self.s.check_pilot(1)
        self.assertFalse(runtime_safe(dict(failure='timeout')))
        self.assertFalse(runtime_safe(dict(failure='provider_defect',termination_confirmed=True)))

    def test_unattended_failure_exports_before_closure_and_snapshot_keeps_blocked_status(self):
        events=[]
        checkpoint=self.s.checkpoint
        def saved(boundary):events.append(('export',boundary));return checkpoint(boundary)
        for slot,worker in enumerate(self.workers):
            worker.close=lambda slot=slot:events.append(('close',slot)) or dict(termination_confirmed=True)
        with patch.object(self.s,'checkpoint',side_effect=saved),patch.object(self.s,'check_pilot',side_effect=ValueError('Scripted real gate failure')):
            stopped=self.s.run_action('check_pilot',number=1)
        self.assertIn('Scripted real gate failure',stopped['error'])
        self.assertEqual(events[0],('export','action/check_pilot'))
        self.assertEqual([e[0] for e in events],['export','close','close','export'])
        self.assertTrue(self.s.meta.meta('failure_cleanup')['termination_confirmed'])
        self.s.run_action('snapshot')
        self.assertEqual(analysis(self.run)['summary']['scientific_gate_status'],'blocked')
        self.assertEqual(self.s.meta.meta('failure_cleanup')['provider_release'],'unknown')
        write_report(self.run,self.run/'reports',plot=False)
        self.assertIn('Scientific gate: <b>blocked</b>',(self.run/'reports/overview.html').read_text(encoding='utf-8'))

    def test_export_failure_preserves_archive_and_attempts_both_closures_without_fake_confirmation(self):
        self.s.checkpoint('last-good')
        before=(self.run/'exports/latest.zip').read_bytes()
        closed=[]
        def unknown():closed.append(0);raise ValueError('termination unconfirmed')
        self.workers[0].close=unknown
        self.workers[1].close=lambda:closed.append(1) or dict(termination_confirmed=True)
        try:
            with patch.object(self.s,'checkpoint',side_effect=OSError('disk full')):
                receipt=self.s.failure_cleanup('pilot','Scripted storage failure')
            self.assertEqual(closed,[0,1]);self.assertFalse(receipt['termination_confirmed'])
            self.assertEqual(receipt['workers'][1]['termination_confirmed'],True)
            self.assertEqual((self.run/'exports/latest.zip').read_bytes(),before)
            self.assertIn('disk full',receipt['checkpoint']['error'])
        finally:self.workers[0].close=lambda:dict(termination_confirmed=True)

    def test_receipt_write_failure_does_not_skip_worker_closure(self):
        closed=[]
        for slot,worker in enumerate(self.workers):worker.close=lambda slot=slot:closed.append(slot) or dict(termination_confirmed=True)
        with patch('recovery.i01.workflow.atomic_json',side_effect=OSError('receipt disk full')),patch.object(self.s,'checkpoint',side_effect=OSError('export disk full')):
            receipt=self.s.failure_cleanup('pilot','Scripted failed export')
        self.assertEqual(closed,[0,1]);self.assertTrue(receipt['termination_confirmed'])
        self.assertIn('receipt disk full',receipt['stage_receipt_error'])
        self.assertIn('receipt disk full',receipt['cleanup_receipt_error'])


class SessionClock(unittest.TestCase):
    def test_failed_portable_verification_uses_failure_finalizer(self):
        study=Study.__new__(Study)
        study.run=lambda *args,**kwargs:dict(checkpoint={'integrity':'passed'})
        with patch.object(study,'verify_checkpoint',side_effect=ValueError('broken portable evidence')),patch.object(study,'operation_error') as saved:
            with self.assertRaisesRegex(ValueError,'broken portable'):study.save_checkpoint(verify=True)
        self.assertEqual(saved.call_args.args[0],'verify_checkpoint')

    def test_original_planning_observation_survives_handoff_and_rerun(self):
        with tempfile.TemporaryDirectory() as name:
            with patch('recovery.i01.ui.host_inventory',return_value={}):study=Study(base.ROOT,Path(name)/'scratch',name,Path(name)/'run')
            with redirect_stdout(io.StringIO()):study.configure_session(remaining_minutes=700,evidence='Unverified planning estimate',basis='planning_estimate')
            original=dict(study.window_observation);deadline=study.deadline
            with redirect_stdout(io.StringIO()):study.set_window(deadline,study.allowance_evidence)
            self.assertEqual(study.window_observation,original)
            from recovery.i01.workflow import initialize,Session
            initialize(study.run_dir,base.ROOT,base.CONFIG,independent=True)
            session=Session(study.run_dir,base.ROOT)
            try:
                value=session.window(deadline,study.allowance_evidence,observation=study.window_observation)
                self.assertEqual(value['observation'],original)
                self.assertEqual(value['observation']['remaining_minutes'],700)
                self.assertEqual(value['observation']['basis'],'planning_estimate')
            finally:session.close()


if __name__=='__main__':unittest.main()
