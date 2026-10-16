"""Hand-scored saved-data cases; no model or experiment execution."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from recovery.i01.core import (apply_outcome,canonical,initial_episode,next_agent,permitted_view)
from recovery.i01.report import analysis,bootstrap,DEGENERATE_WARNING,write_report
from recovery.i01.store import Admission,Store
from recovery.i01.workflow import initialize
from recovery.i01.policy import outcome_feedback

ROOT=Path(__file__).parents[1]
CONFIG=json.loads((ROOT/'configs/i01-course-assisted.json').read_text())


class AssistedReport(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='i01-assisted-report-')
        self.run=Path(self.temp.name)/'run';self.manifest=initialize(self.run,ROOT,CONFIG,independent=True)
        self.stores=[Store(self.run/f'worker-{i}.sqlite',{'manifest':self.manifest}) for i in (0,1)]
        self.admission=Admission(self.stores)
        self.main=[w for w in self.manifest['worlds'] if w['group']=='main']
    def tearDown(self):
        for store in self.stores:store.close()
        self.temp.cleanup()
    def episode(self,w,phase,submissions,*,illegal=False,unknown_time=False,interrupted=False):
        store=self.stores[w['device']];identity=w['id']+'/'+phase
        state=initial_episode(w,phase,store.state(w['id']+'/prefix'))
        store.start(identity,state)
        first=True
        while next_agent(state) is not None:
            agent=next_agent(state);cid=f"{identity}/agent-{agent}/invocation-{state['turns'][agent]}"
            request=dict(view=permitted_view(w,state,agent),seed=w['seeds']['prefix' if phase=='prefix' else 'recovery'][agent][state['turns'][agent]],settings={'mode':'direct'},rendered='',input_ids=[])
            store.register(cid,identity,request);attempt=self.admission.admit(store,cid,'main')
            if first and interrupted:
                self.admission.reconcile(store,attempt,dict(termination_confirmed=True,reason='Synthetic interruption'))
                attempt=self.admission.admit(store,cid,'main')
            action=dict(message='invalid',submit=None,wait=True) if first and illegal else dict(message=None,submit=submissions[agent],wait=False)
            outcome=dict(visible_text=canonical(action),ready_seconds=None if first and unknown_time else .25,
                         generated_tokens=1,input_tokens=0,failure=None,truncated=False)
            store.raw(cid,attempt,outcome)
            error='malformed_action' if first and illegal else None
            state=apply_outcome(state,agent,None if error else action,error,cid,feedback=outcome_feedback(outcome) if error else None)
            store.effects(cid,identity,state);first=False
        return state
    def cases(self):
        for i,w in enumerate(self.main[:4]):
            truth=w['revised_truth']
            self.episode(w,'prefix',[w['original_truth']]*2,illegal=i==0,interrupted=i==0)
            retain=[-1001,-1001] if i==0 else [w['before']]*2 if i==2 else [truth]*2
            clear=[-1001]*2 if i in (1,2) else [truth]*2
            self.episode(w,'retain',retain,unknown_time=i==0)
            self.episode(w,'clear',clear)

    def test_hand_scored_pairs_bounds_process_and_fixed_casebook(self):
        self.cases();result=analysis(self.run);summary=result['summary']
        self.assertEqual(summary['known_pairs'],4)
        self.assertEqual(summary['paired_counts'],{'clear_only':1,'retain_only':1,'neither':1,'both':1,'unknown':16})
        self.assertEqual(summary['missingness_bounds'],[-.8,.8])
        self.assertIsNone(summary['clear_minus_retain']);self.assertIsNone(summary['interval'])
        self.assertEqual(summary['retain_successes'],2)
        self.assertEqual(summary['clear_successes'],2)
        self.assertIsNone(summary['retain_success_rate'])
        self.assertEqual(summary['retain_rate_completion_bounds'],[.1,.9])
        self.assertEqual(summary['correct_prefix_recovery'],dict(denominator=4,retain_correct=2,retain_unknown=0,clear_correct=2,clear_unknown=0))
        self.assertIsNone(summary['correct_prefix_mean'])
        rows={r['phase']:r for r in result['process_outcomes']}
        self.assertEqual(rows['prefix']['episodes_with_illegal_model_action'],1)
        self.assertEqual(rows['retain']['locally_refutable_submissions'],2)
        self.assertEqual(rows['clear']['locally_refutable_submissions'],4)
        self.assertEqual(rows['retain']['obsolete_submissions'],2)
        self.assertEqual(rows['retain']['obsolete_worlds'],1)
        self.assertEqual(rows['clear']['obsolete_submissions'],0)
        self.assertEqual(rows['retain']['wrong_agreement'],2)
        self.assertEqual(rows['clear']['present_submissions'],8)
        self.assertEqual(rows['clear']['unknown_submission_slots'],32)
        self.assertEqual([r['world'] for r in result['casebook']],['main-00','main-00','main-02','main-00','main-01','main-03'])
        self.assertTrue(all(r['human_review']=='pending' for r in result['casebook']))
        self.assertIn('/prefix/',result['casebook'][0]['selected_call'])
        self.assertIn('/retain/',result['casebook'][1]['selected_call'])

    def test_unknown_effort_is_unavailable_and_retries_have_attempt_denominators(self):
        self.cases();result=analysis(self.run);summary=result['summary']
        self.assertIsNone(summary['principal_effort_clear_minus_retain_seconds'])
        self.assertIsNone(summary['principal_effort_interval'])
        self.assertEqual(summary['cost_complete_pairs'],3)
        r=next(r for r in result['costs'] if r['world']=='main-00' and r['phase']=='retain')
        self.assertIsNone(r['ready_seconds']);self.assertIsNone(r['observed_seconds'])
        self.assertEqual(r['attempts_unknown_ready_seconds'],1)
        self.assertEqual(summary['attempts_unknown_input_tokens'],1)
        self.assertIsNone(next(r for r in result['costs'] if r['world']=='main-00' and r['phase']=='prefix')['input_tokens'])
        row=next(r for r in result['attempt_compliance'] if r['group']=='main' and r['phase']=='prefix')
        self.assertEqual((row['physical_attempts'],row['unknown_outcomes']),(10,1))
        row=next(r for r in result['protocol_compliance'] if r['group']=='main' and r['phase']=='prefix')
        self.assertEqual((row['registered_calls'],row['recorded_calls']),(9,9))
        unknown=next(r for r in result['attempt_validation'] if not r['recorded'])
        self.assertIsNone(unknown['legal_action']);self.assertIsNone(unknown['json_valid'])

    def test_no_qualification_team_costs_or_unexecuted_zero_submissions(self):
        result=analysis(self.run)
        self.assertEqual(len(result['policy_costs']),48)
        self.assertEqual(len(result['costs']),72)
        self.assertTrue(all(r['input_tokens'] is None and r['ready_seconds'] is None for r in result['costs']))
        self.assertTrue(all(r['observed_ready_seconds']==0 for r in result['costs']))
        self.assertTrue(all(r['unknown_submission_slots']==40 for r in result['process_outcomes']))
        self.assertTrue(all(not r['present'] for r in result['casebook']))
        self.assertEqual(result['summary']['missingness_bounds'],[-1,1])

    def test_bootstrap_order_degeneracy_and_incomplete_pairs(self):
        rows=[dict(world=w['id'],owner=w['owner'],first=w['first'],retain=1,clear=1) for w in self.main]
        interval=bootstrap(rows,CONFIG)
        self.assertEqual((interval['low'],interval['high']),(0,0))
        self.assertEqual(interval['caveat'],DEGENERATE_WARNING)
        self.assertEqual(interval['constant_strata'],[[0,0],[0,1],[1,0],[1,1]])
        rows[0]['retain']=0;rows[1]['clear']=0
        interval=bootstrap(rows,CONFIG)
        self.assertEqual(interval,bootstrap(list(reversed(rows)),CONFIG))
        self.assertEqual((interval['low'],interval['high']),(-.1,.1))
        missing=deepcopy(rows);missing[0]['retain']=None
        self.assertIsNone(bootstrap(missing,CONFIG))
        with self.assertRaisesRegex(ValueError,'all twenty pairs'):
            bootstrap(rows[:5],CONFIG)

    def test_full_report_has_new_tables_and_eight_figures_with_eight_control_scope(self):
        self.cases();out=self.run/'reports';write_report(self.run,out,plot=True)
        for name in ('diagnostics','process_outcomes','attempt_validation','attempt_compliance','casebook'):
            self.assertTrue((out/(name+'.csv')).is_file())
        self.assertEqual(len(list((out/'figures').glob('*.svg'))),8)
        self.assertEqual(len(list((out/'figures').glob('*.png'))),8)
        html=(out/'overview.html').read_text(encoding='utf-8')
        self.assertIn('/8',html);self.assertNotIn('/12',html)
        self.assertIn('Four supplied-view diagnostics',html)
        self.assertIn('conversations.html#main-00/prefix/',html)
        self.assertIn('Exact main process observables',(out/'overview.md').read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
