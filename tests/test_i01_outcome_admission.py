"""Course-6 counterexamples and new post-qualification admission; no inference."""
import json
import unittest
import zipfile
from unittest.mock import patch

from recovery.i01.core import validate_action, apply_outcome, initial_episode
from recovery.i01.policy import (AUTOMATIC_POLICY, RECOVERY_POLICY, OUTCOME_POLICY,
                                 admission_blocks, validation_detail, runtime_safe)
from recovery.i01.report import analysis, write_report
from tests import test_i01_run_all as base

PREFIX_REPLY='{"message":"I see your shard. I will scan for the maximum value. My shard: [497, 966, -234, 36, 849, 815, -663, -6, -768, 34, -430, 328, -282, -891, 740, 985, -998, -348, 150, -746]. Max in my shard is 985. I will wait for your shard to confirm the global maximum.","submit":null,"wait":true}'


class OutcomeAdmission(unittest.TestCase):
    setUp=base.RunAll.setUp
    tearDown=base.RunAll.tearDown

    def errors(self):
        for worker in self.workers:
            worker.reply=lambda req:dict(failure=None,visible_text='invalid JSON' if req.get('control') else PREFIX_REPLY,
                truncated=False,generated_tokens=1,ready_seconds=.001,input_tokens=1)

    def test_exact_prefix_and_control_mistakes_stay_invalid_and_are_admissible(self):
        world=next(w for w in self.s.manifest['worlds'] if w['group']=='pilot')
        action,error=validate_action(PREFIX_REPLY)
        self.assertIsNone(action);self.assertEqual(error,'malformed_action')
        state=apply_outcome(initial_episode(world,'prefix'),0,action,error,'fixture')
        self.assertEqual(state['turns'],[1,0]);self.assertFalse(state['history'][1])
        detail=validation_detail(dict(visible_text=PREFIX_REPLY))
        self.assertTrue(detail['json_valid'] and detail['schema_valid']);self.assertFalse(detail['legal_action'])
        for policy in (AUTOMATIC_POLICY,RECOVERY_POLICY):self.assertTrue(admission_blocks(policy,'pilot','prefix',detail))
        self.assertFalse(admission_blocks(OUTCOME_POLICY,'pilot','prefix',detail))
        self.errors();self.s.pilot(1)
        before=[store.rows('calls') for store in self.s.stores]
        receipt=self.s.check_pilot(1)
        self.assertTrue(receipt['passed']);self.assertFalse(receipt['original_team_completed'])
        self.assertNotIn('valid_protocol',receipt['checks'])
        self.assertNotIn('original_team_completed',receipt['checks'])
        self.assertEqual((receipt['prefix_protocol_errors'],receipt['recovery_protocol_errors'],receipt['control_protocol_errors']),(6,12,2))
        self.assertEqual(before,[store.rows('calls') for store in self.s.stores])
        self.assertFalse(any(v['admission_blocking'] for v in receipt['validation']))

    def test_main_gate_reconstructs_new_rule_and_historical_rule_still_rejects(self):
        self.errors()
        for n in (1,2,3):self.s.pilot(n);self.s.check_pilot(n)
        plan=self.s.meta.meta('execution_plan')
        for old in (AUTOMATIC_POLICY,RECOVERY_POLICY):
            self.s.meta.put_meta('execution_plan',dict(plan,policy=old))  # Historical-policy fixture only.
            with self.assertRaisesRegex(ValueError,'evidence no longer'):self.s.admit_main()
        self.s.meta.put_meta('execution_plan',plan)
        frozen=self.s.admit_main()
        self.assertEqual(frozen['execution_policy'],OUTCOME_POLICY)
        self.assertEqual(self.s.admission.usage()['contingency'],0)

    def test_missing_raw_effect_or_terminal_evidence_never_becomes_an_outcome(self):
        self.s.pilot(1)
        world=next(w for w in self.s.manifest['worlds'] if w['group']=='pilot')
        store=self.s.stores[world['device']]
        row=next(c for c in store.rows('calls') if c['episode']==world['id']+'/prefix')
        for column,bad in (('outcome',None),('effect_committed',0)):
            with store.transaction():store.db.execute(f'UPDATE calls SET {column}=? WHERE id=?',(bad,row['id']))
            with self.assertRaisesRegex(ValueError,'committed_calls'):self.s.check_pilot(1)
            with store.transaction():store.db.execute(f'UPDATE calls SET {column}=? WHERE id=?',(row[column],row['id']))
        saved=store.state(row['episode']);bad=dict(saved,terminal=None)
        with store.transaction():store.db.execute('UPDATE episodes SET state=? WHERE id=?',(json.dumps(bad),row['episode']))
        with self.assertRaisesRegex(ValueError,'terminal_evidence'):self.s.check_pilot(1)
        with store.transaction():store.db.execute('UPDATE episodes SET state=? WHERE id=?',(json.dumps(saved),row['episode']))

    def test_invalid_fixed_qualification_still_blocks_before_any_new_call(self):
        store=self.s.stores[0]
        row=next(r for r in store.rows('calls') if r['episode'].startswith('qualification-'))
        outcome=dict(json.loads(row['outcome']),visible_text='invalid JSON')
        with store.transaction():store.db.execute('UPDATE calls SET outcome=? WHERE id=?',(json.dumps(outcome),row['id']))
        before=sum(w.calls for w in self.workers)
        with self.assertRaisesRegex(ValueError,'qualification'):self.s.pilot(1)
        self.assertEqual(sum(w.calls for w in self.workers),before)

    def test_real_fault_and_unknown_spending_block_and_new_policy_closes_workers(self):
        self.s.pilot(1)
        self.s.meta.put_meta('model_defect',dict(call='fixture',reason='actual cache fault fixture'))
        with self.assertRaisesRegex(ValueError,'runtime integrity'):self.s.check_pilot(1)
        self.s.meta.put_meta('model_defect',None)
        self.s.meta.put_meta('lost_spending',dict(resolved=False,upper=None,evidence='Unknown additional tail fixture'))
        closed=[]
        for slot,worker in enumerate(self.workers):worker.close=lambda slot=slot:closed.append(slot) or dict(termination_confirmed=True)
        stopped=self.s.run_action('check_pilot',number=1)
        self.assertIn('reconciled_spending',stopped['error'])
        self.assertEqual(closed,[0,1]);self.assertTrue(self.s.meta.meta('failure_cleanup')['termination_confirmed'])
        self.assertIsNone(self.s.admission.usage()['remaining'])
        self.assertEqual(analysis(self.run)['summary']['scientific_gate_status'],'blocked')

    def test_remaining_work_forecast_and_precise_failure_references(self):
        self.errors();self.s.pilot(1);self.s.check_pilot(1)
        forecast=self.s.forecast()
        self.assertEqual(forecast['remaining_pilot_first_attempts'],40)
        self.assertEqual(forecast['worst_remaining_first_attempts'],380)
        self.assertGreater(forecast['estimated_checkpoint_overhead_seconds'],0)
        self.assertGreater(forecast['whole_remaining_wall_seconds'],forecast['conservative_wall_seconds'])
        result=analysis(self.run)
        for row in result['failure_analysis']:
            if row['label']=='malformed_action':
                self.assertEqual(row['call_scope'],'exact_offending_calls')
                self.assertTrue(all(c.startswith(row['episode']+'/') or c==row['episode'] for c in row['calls']))
        write_report(self.run,self.run/'reports',plot=False)
        html=(self.run/'reports/overview.html').read_text(encoding='utf-8')
        self.assertIn('Admitted recorded outcomes',html)
        self.assertIn('Pilot 3',html)
        self.assertIn('admission_blocking',(self.run/'reports/validation_details.csv').read_text())

    def test_historical_block_message_names_exact_call_phase_and_reason(self):
        self.errors();self.s.pilot(1)
        plan=self.s.meta.meta('execution_plan')
        self.s.meta.put_meta('execution_plan',dict(plan,policy=RECOVERY_POLICY))
        with self.assertRaisesRegex(ValueError,r'pilot-00/prefix/agent-0/invocation-0: wait_requires_null_message_and_submit \[prefix\]'):
            self.s.check_pilot(1)


class Classification(unittest.TestCase):
    def test_output_error_classes_diagnostic_but_real_faults_and_qualification_strict(self):
        scalar='{"message":null,"submit":1,"wait":false}'
        ordinary=[dict(visible_text='bad JSON'),dict(visible_text=scalar,truncated=True),dict(visible_text=scalar,framing_error='native_output_framing')]
        for outcome in ordinary:
            detail=validation_detail(outcome)
            self.assertFalse(detail['legal_action'])
            for phase in ('prefix','retain','clear','control-original-direct','control-revised-direct'):
                self.assertFalse(admission_blocks(OUTCOME_POLICY,'pilot',phase,detail,safe=runtime_safe(outcome)))
            self.assertTrue(admission_blocks(OUTCOME_POLICY,'qualification','control-original-direct',detail))
        for outcome in (dict(failure='provider_defect'),dict(failure='timeout',termination_pending=True)):
            self.assertTrue(admission_blocks(OUTCOME_POLICY,'pilot','prefix',validation_detail(outcome),safe=runtime_safe(outcome)))


class SavedCourse6(unittest.TestCase):
    @unittest.skipUnless((base.ROOT/'notebooks/run/course-6/latest.zip').is_file(),'Saved operator evidence is not bundled in source-only releases')
    def test_saved_prefix_reply_and_historical_failed_decision_remain_exact(self):
        with zipfile.ZipFile(base.ROOT/'notebooks/run/course-6/latest.zip') as z:
            result=json.loads(z.read('reports/analysis.json'))
        self.assertEqual(result['summary']['attempts'],43)
        self.assertFalse(result['pilot_checks'][1]['passed'])
        call=next(t for t in result['traces'] if t['id']=='pilot-01/prefix/agent-1/invocation-0')
        outcome=json.loads(call['outcome'])
        self.assertEqual(json.loads(outcome['visible_text']),json.loads(PREFIX_REPLY))
        for row in result['validation_details']:
            if row['group']=='pilot':
                self.assertFalse(admission_blocks(OUTCOME_POLICY,'pilot',row['phase'],row,safe=row['runtime_safe']))
        self.assertFalse(result['pilot_checks'][1]['passed'])


if __name__=='__main__':unittest.main()
