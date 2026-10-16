"""Focused saved/scripted regressions; no model, CUDA, or new research outcomes."""
from contextlib import redirect_stdout
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from recovery.i01.archive import export, extract_selected, digest
from recovery.i01.continuation import continue_checkpoint, record_prior_preparation, _adjudicate_length_flag
from recovery.i01.core import canonical
from recovery.i01.policy import PROTOCOL_POLICY
from recovery.i01.report import analysis, write_report
from recovery.i01.store import connection, restore_tail, resolve_restore_tail
from recovery.i01.workflow import initialize, Session

ROOT=Path(__file__).parents[1]
C2=ROOT/'notebooks/run/course-2/latest.zip'
C3=ROOT/'notebooks/run/course-3/latest.zip'


def prepare(view, seed, mode, **flags):
    return dict(view=view,seed=seed,settings={'mode':mode},input_ids=[1],rendered=canonical(view),**flags)


class Scripted:
    def __init__(self):self.calls=0;self.reply=None
    def obtain(self,req,timeout):
        self.calls+=1
        if self.reply:return deepcopy(self.reply(req))
        action=dict(message=None if req.get('control') else 'A task-related candidate message',submit=-1000,wait=False)
        return dict(failure=None,visible_text=canonical(action),raw_text=canonical(action),
                    generated_tokens=512 if req.get('envelope') else 1,ready_seconds=.001,
                    input_tokens=1,token_ids=[1],truncated=False,framing_error=None,
                    backend=dict(finite_score_steps=1,cache=dict(initial_empty=True,same_call_cache=True),
                                 observed_peak_free_lower_bytes=2**31))
    def close(self):return dict(termination_confirmed=True)


class Course3Repairs(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='i01-course3-fix-')
        self.run=Path(self.temp.name)/'run'
        initialize(self.run,ROOT,json.loads((ROOT/'configs/i01-course.json').read_text()))
        self.workers=[Scripted(),Scripted()]
        self.s=Session(self.run,ROOT,providers=self.workers,prepare_request=prepare)
        self.s.meta.put_meta('required_preparation_studies',[])  # Isolated scripted fixture, not a new research campaign.
        self.s.window((datetime.now(timezone.utc)+timedelta(hours=2)).isoformat(),'Scripted allowance only')
    def tearDown(self):
        self.s.close();self.temp.cleanup()

    def test_wrong_mathematics_is_diagnostic_and_screen_replay_is_free(self):
        s=self.s;s.meta.put_meta('readiness',{'passed':True})
        q=s.screen('direct')
        self.assertTrue(q['passed']);self.assertEqual(q['correct'],0)
        self.assertEqual(q['committed'],12);self.assertEqual(q['protocol_errors'],0)
        count=sum(w.calls for w in self.workers)
        self.assertTrue(s.screen('direct')['passed'])
        self.assertTrue(s.screen('thinking')['skipped'])
        self.assertEqual(sum(w.calls for w in self.workers),count)

    def test_invalid_qualification_still_blocks_envelope(self):
        s=self.s;s.meta.put_meta('readiness',{'passed':True})
        self.workers[0].reply=lambda req:dict(failure=None,visible_text='not json',truncated=False,
                                            generated_tokens=1,ready_seconds=.001,input_tokens=1)
        q=s.screen('direct');self.assertFalse(q['passed']);self.assertGreater(q['protocol_errors'],0)
        before=s.admission.usage()['attempts']
        with self.assertRaisesRegex(ValueError,'protocol qualification'):s.envelope()
        self.assertEqual(s.admission.usage()['attempts'],before)

    def test_public_headroom_refusal_is_archived_without_any_generation(self):
        from recovery.i01.notebook import Study
        from recovery.i01.ui import ActionStopped
        s=self.s
        class Client:
            process=SimpleNamespace(poll=lambda:None)
            def command(self,name):return s.status()
            def action(self,name,**args):return s.run_action(name,**args)
        with patch('recovery.i01.ui.host_inventory',return_value={}):
            ui=Study(ROOT,Path(self.temp.name)/'scratch',Path(self.temp.name)/'working',self.run)
        ui.client=Client();ui.show=lambda r:None;ui.links=lambda:None
        with self.assertRaisesRegex(ActionStopped,'protocol qualification'):ui.check_headroom()
        self.assertEqual(sum(w.calls for w in self.workers),0)
        restored=Path(self.temp.name)/'refusal'
        extract_selected(self.run/'exports/latest.zip',restored)
        self.assertIn('protocol qualification',(restored/'receipts/operator-errors.jsonl').read_text())
        self.assertEqual(analysis(restored)['summary']['attempts'],0)

    def test_ordinary_truncation_consumes_turns_without_global_defect_or_retry(self):
        outcome=dict(failure=None,visible_text='',raw_text='unfinished private output',truncated=True,
                     termination='length',framing_error='thinking_framing_defect',generated_tokens=4096,
                     ready_seconds=.001,input_tokens=1)
        for worker in self.workers:worker.reply=lambda req:outcome
        world=next(w for w in self.s.manifest['worlds'] if w['id']=='pilot-00')
        state=self.s.episode(world,'prefix','thinking')
        self.assertEqual(state['turns'],[3,3]);self.assertEqual(state['submissions'],[None,None])
        self.assertEqual(state['history'][0][-1]['kind'],'feedback')
        self.assertFalse(self.s.meta.meta('model_defect'))
        self.assertTrue(all(e['error']=='truncated_action' for e in state['events']))
        self.assertEqual(sum(w.calls for w in self.workers),6)
        self.s.episode(world,'prefix','thinking')
        self.assertEqual(sum(w.calls for w in self.workers),6)

    def test_real_provider_defect_remains_blocking_and_cannot_be_adjudicated(self):
        world=self.s.manifest['worlds'][0]
        self.workers[world['device']].reply=lambda req:dict(failure='provider_defect',reason='nonfinite model scores',visible_text=canonical(dict(message=None,submit=world['original_truth'],wait=False)),ready_seconds=None,generated_tokens=None,input_tokens=1)
        with self.assertRaisesRegex(ValueError,'defect'):self.s.control(world,'original','direct',stage='direct')
        self.assertEqual(self.s.stores[world['device']].state(world['id']+'/control-original-direct')['submissions'],[])
        self.assertTrue(self.s.meta.meta('model_defect'))
        with self.assertRaisesRegex(ValueError,'cannot be cleared'):_adjudicate_length_flag(self.s.stores)
        with self.assertRaisesRegex(ValueError,'runtime defect'):self.s.control(world,'revised','direct',stage='direct')
        self.assertEqual(sum(w.calls for w in self.workers),1)

    def test_flag_independent_envelope_binding_and_zero_call_rerun(self):
        s=self.s;s.screen_result=lambda mode:dict(passed=True)
        for i,store in enumerate(s.stores):store.put_meta('resident_load',f'{s.session_id}/original-{i}')
        self.assertTrue(s.envelope()['passed'])
        s.stores[1].put_meta('resident_load',f'{s.session_id}/replacement-1')
        before=s.admission.usage()['attempts']
        self.assertFalse(s.meta.meta('reload_required',False))
        with self.assertRaisesRegex(ValueError,'reload'):s.envelope()
        self.assertEqual(s.admission.usage()['attempts'],before)
        self.assertTrue(s.envelope(reload=True)['passed'])
        self.assertEqual(s.admission.usage()['attempts'],before+2)
        self.assertEqual(s.admission.usage()['contingency'],2)
        self.assertTrue(s.envelope()['passed']);self.assertTrue(s.envelope(reload=True)['passed'])
        self.assertEqual(s.admission.usage()['attempts'],before+2)

    def test_live_reader_uses_one_snapshot_per_worker(self):
        injected=[];store=self.s.stores[0]
        class Reader:
            def __init__(self,path,*args,**kwargs):self.db=connection(path,*args,**kwargs);self.slot0=Path(path).name=='worker-0.sqlite'
            def execute(self,sql,*args):
                if self.slot0 and sql=='SELECT * FROM attempts' and not injected:
                    injected.append(True)
                    store.register('race-call','race-episode',prepare({},1,'direct'))
                    self_outer.s.admission.admit(store,'race-call','pilot')
                return self.db.execute(sql,*args)
            def close(self):self.db.close()
        self_outer=self
        with patch('recovery.i01.report.connection',Reader):
            result=analysis(self.run)
        self.assertTrue(injected);self.assertEqual(result['summary']['attempts'],0)
        self.assertEqual(self.s.admission.usage()['attempts'],1)
        self.assertEqual(analysis(self.run)['summary']['attempts'],1)

    def test_partial_envelope_is_bound_before_first_probe(self):
        s=self.s;s.screen_result=lambda mode:dict(passed=True)
        for i,store in enumerate(s.stores):store.put_meta('resident_load',f'{s.session_id}/initial-{i}')
        original=self.workers[1].obtain
        self.workers[1].obtain=lambda *a:(_ for _ in ()).throw(ValueError('Scripted interruption'))
        with self.assertRaisesRegex(ValueError,'Scripted interruption'):s.envelope()
        self.assertEqual(s.meta.meta('envelope')['loads'],s.load_references())
        s.stores[0].put_meta('resident_load',f'{s.session_id}/replacement-0')
        before=sum(w.calls for w in self.workers)
        with self.assertRaisesRegex(ValueError,'reload'):s.envelope()
        self.assertEqual(sum(w.calls for w in self.workers),before)
        self.workers[1].obtain=original

    def test_prior_reserve_and_failed_import_cannot_reset_allowance(self):
        s=self.s
        with self.assertRaises(ValueError):record_prior_preparation(self.run,s.stores,[Path(self.temp.name)/'missing.zip'])
        self.assertIsNone(s.admission.usage()['remaining'])
        with self.assertRaisesRegex(ValueError,'empty checkpoint'):record_prior_preparation(self.run,s.stores,[])
        s.meta.put_meta('prior_spending_pending',None)  # Scripted fixture reconciliation only.
        s.meta.put_meta('prior_spending',[dict(study_id='scripted-prior',attempts=18,contingency_charge=18)])
        for i in range(10):
            call=f'extra/{i}';store=s.stores[0];store.register(call,'scripted-diagnostic',prepare({},i,'direct'))
            attempt=s.admission.admit(store,call,'hardware',contingency=True)
            store.raw(call,attempt,dict(failure=None,ready_seconds=.001,generated_tokens=1))
        store.register('over-reserve','scripted-diagnostic',prepare({},99,'direct'))
        with self.assertRaisesRegex(ValueError,'contingency exhausted'):s.admission.admit(store,'over-reserve','hardware',contingency=True)
        self.assertEqual(s.admission.usage()['campaign_attempts'],28)
        self.assertEqual(s.admission.usage()['contingency'],28)

    def test_new_study_has_no_fresh_allowance_until_known_history_reconciles(self):
        run=Path(self.temp.name)/'another-study'
        initialize(run,ROOT,json.loads((ROOT/'configs/i01-course.json').read_text()))
        other=Session(run,ROOT)
        try:
            self.assertEqual(len(other.admission.usage()['missing_prior_studies']),2)
            self.assertIsNone(other.admission.usage()['remaining'])
            other.stores[0].register('new','fixture',prepare({},1,'direct'))
            with self.assertRaisesRegex(ValueError,'cannot reset the campaign'):other.admission.admit(other.stores[0],'new','direct')
        finally:other.close()

    def test_latest_tail_preserves_prior_gap_and_unknown_blocks(self):
        self.s.meta.put_meta('lost_spending',dict(upper=3,resolved=True,evidence='Earlier known upper bound'))
        self.s.meta.put_meta('blocked_worlds',['main-00'])
        restore_tail(self.s.meta,'latest','No additional tail',boundary='fixture')
        self.assertEqual(self.s.admission.usage()['remaining'],497)
        self.assertEqual(self.s.meta.meta('blocked_worlds'),['main-00'])
        restore_tail(self.s.meta,'unknown','Additional tail unknown',boundary='fixture-2')
        self.assertIsNone(self.s.admission.usage()['remaining'])
        self.assertEqual(self.s.admission.usage()['contingency'],3)
        restore_tail(self.s.meta,'latest','Latest boundary now known',boundary='fixture-3')
        self.assertIsNone(self.s.admission.usage()['remaining'])

    def test_bounding_new_tail_keeps_older_gap_and_cannot_apply_twice(self):
        self.s.meta.put_meta('lost_spending',dict(upper=3,resolved=True,evidence='Earlier gap'))
        self.s.meta.put_meta('blocked_worlds',['main-00'])
        restore_tail(self.s.meta,'unknown','Additional tail unknown',boundary='fixture')
        restore_tail(self.s.meta,'latest','A newer zero-tail boundary cannot resolve the old gap',boundary='fixture-newer')
        self.assertEqual(resolve_restore_tail(self.s.meta,2,'Fixture: at most two additional calls',['main-01'])['upper'],5)
        self.assertEqual(self.s.admission.usage()['remaining'],495)
        self.assertEqual(self.s.meta.meta('blocked_worlds'),['main-00','main-01'])
        with self.assertRaises(ValueError):resolve_restore_tail(self.s.meta,2,'Same boundary',[])
        restore_tail(self.s.meta,'latest','Latest newer boundary',boundary='next-fixture')
        self.assertEqual(self.s.admission.usage()['remaining'],495)

    def test_unknown_spending_blocks_load_and_wrong_slot_blocks_admission(self):
        self.s.meta.put_meta('selfcheck',{'passed':True})
        restore_tail(self.s.meta,'unknown','Unknown fixture tail',boundary='fixture')
        with self.assertRaisesRegex(ValueError,'before loading'):self.s.load('/not-used',{})
        world=next(w for w in self.s.manifest['worlds'] if w['device']==1)
        with self.assertRaisesRegex(ValueError,'Misplaced logical'):
            self.s.call(0,world['id']+'/test',world['id']+'/prefix',prepare({},1,'direct'),'direct')
        self.assertEqual(self.s.admission.usage()['attempts'],0)

    def test_both_restore_interfaces_preserve_saved_gap(self):
        self.s.meta.put_meta('lost_spending',dict(upper=3,resolved=True,evidence='Earlier gap'))
        self.s.meta.put_meta('blocked_worlds',['main-00'])
        packet=export(self.run,self.s.stores,boundary='saved-gap',reports=False)
        from recovery.i01.cli import main
        cli_run=Path(self.temp.name)/'cli-restored'
        with redirect_stdout(io.StringIO()):
            main(['--source',str(ROOT),'--run',str(cli_run),'restore',packet['path'],'--tail','latest','--evidence','Zero additional exposure'])
        restored=Session(cli_run,ROOT)
        try:self.assertEqual(restored.admission.usage()['remaining'],497)
        finally:restored.close()
        from recovery.i01.notebook import Study
        import sys
        with patch('recovery.i01.ui.host_inventory',return_value={}):
            ui=Study(ROOT,Path(self.temp.name)/'scratch',Path(self.temp.name)/'working',Path(self.temp.name)/'ui-restored')
        ui.environment={'interpreter':sys.executable};ui.show=lambda r:None;ui.links=lambda:None;ui.emit=lambda r:None
        try:
            ui.open('restore',selected=packet['path'],tail='latest',evidence='Zero additional exposure')
            self.assertEqual(ui.status()['usage']['remaining'],497)
            self.assertEqual(ui.status()['gates']['blocked_worlds'],['main-00'])
        finally:
            if ui.client:ui.client.close()

    def test_duplicate_tagged_worker_is_rejected(self):
        self.s.close();self.s=SimpleNamespace(close=lambda:None)
        shutil.copy2(self.run/'worker-0.sqlite',self.run/'worker-1.sqlite')
        with self.assertRaisesRegex(ValueError,'logical worker'):Session(self.run,ROOT)
        with self.assertRaisesRegex(ValueError,'logical worker'):analysis(self.run)

    def test_completed_wrong_pilot_mathematics_does_not_prevent_freeze(self):
        s=self.s;s.qualified=lambda:'direct';s.meta.put_meta('selected_mode','direct')
        for world in s.manifest['worlds']:
            if world['group']!='pilot':continue
            for phase in ('prefix','retain','clear'):s.episode(world,phase,'direct')
            for phase in ('original','revised'):s.control(world,phase,'direct')
        s.checkpoint('scripted-complete-wrong-pilots')
        for number in (1,2,3):s.review(f'pilot-{number}','Scripted communication observed',useful_communication=True,usable=True)
        self.assertTrue(all(w['prefix']==0 for w in analysis(self.run)['worlds'] if w['group']=='pilot'))
        self.assertEqual(s.freeze('Freeze scripted policy only')['qualification_policy'],PROTOCOL_POLICY)


@unittest.skipUnless(C2.is_file() and C3.is_file(),'Saved course-2/course-3 operator fixtures are not bundled in the source release')
class SavedCourse3(unittest.TestCase):
    def test_checkpoint_picker_collapses_identical_zip_and_expanded_boundaries(self):
        from recovery.i01.continuation import choose_checkpoint, COURSE_3_STUDY
        with tempfile.TemporaryDirectory(prefix='i01-input-pick-') as name:
            root=Path(name);shutil.copy2(C3,root/'course3.zip');extract_selected(C3,root/'expanded')
            self.assertEqual(choose_checkpoint(COURSE_3_STUDY,root),root/'course3.zip')
            manifest=json.loads((root/'expanded/integrity.json').read_text());manifest['created_at']='distinct boundary'
            (root/'expanded/integrity.json').write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,'2 candidates'):choose_checkpoint(COURSE_3_STUDY,root)

    def test_new_code_cannot_masquerade_as_the_old_source_packet(self):
        with tempfile.TemporaryDirectory(prefix='i01-source-refusal-') as name:
            run=Path(name)/'old';extract_selected(C3,run)
            with self.assertRaisesRegex(ValueError,'schema mismatch|Imported implementation differs'):Session(run,run/'source')
            self.assertFalse(analysis(run)['qualification']['direct']['passed'])

    def test_actual_checkpoint_transition_preserves_calls_budget_and_failed_history(self):
        before={p:digest(p) for p in (C2,C3)}
        with tempfile.TemporaryDirectory(prefix='i01-saved-transition-') as name:
            run=Path(name)/'continued'
            with patch('recovery.i01.inference.ModelFactory',side_effect=AssertionError('No model may load')):
                receipt=continue_checkpoint(C3,run,ROOT,prior_checkpoints=[C2],tail='latest',evidence='Fixture: no additional post-checkpoint exposure')
            self.assertEqual(receipt['preserved_attempts'],23);self.assertEqual(receipt['campaign_attempts'],41)
            result=analysis(run);q=result['qualification']
            self.assertTrue(q['direct']['passed']);self.assertEqual(q['direct']['correct'],10)
            self.assertFalse(q['direct']['historical_gate']['passed'])
            self.assertEqual((q['thinking']['recorded'],q['thinking']['correct'],q['thinking']['protocol_errors'],q['thinking']['unexecuted']),(5,4,1,7))
            self.assertEqual(len(result['failure_analysis']),3)
            self.assertTrue(all(r['calls'] for r in result['failure_analysis']))
            self.assertEqual(result['summary']['known_pairs'],0)
            self.assertTrue(all(c['logical_end_to_end_calls'] is None for c in result['policy_costs']))
            requests=[json.loads(t['request']) for t in result['traces']]
            def replay(view,seed,mode,**flags):
                return next(r for r in requests if r['view']==view and r['seed']==seed and r['settings']['mode']==mode)
            s=Session(run,ROOT,providers=[Scripted(),Scripted()],prepare_request=replay)
            try:
                self.assertEqual((s.admission.usage()['attempts'],s.admission.usage()['campaign_attempts'],s.admission.usage()['contingency'],s.admission.usage()['remaining']),(23,41,18,459))
                self.assertFalse(s.meta.meta('model_defect'));self.assertTrue(s.meta.meta('model_defect_adjudication'))
                import subprocess,sys
                old_source=run/'source'
                code='import sys;sys.path.insert(0,sys.argv[1]);from recovery.i01.workflow import Session;Session(sys.argv[2],sys.argv[1])'
                old=subprocess.run([sys.executable,'-I','-S','-c',code,str(old_source),str(run)],capture_output=True,text=True,timeout=20)
                self.assertNotEqual(old.returncode,0)
                self.assertIn('schema mismatch',old.stderr)
                self.assertTrue(s.screen('direct')['passed'])
                self.assertEqual(sum(w.calls for w in s.workers),0)
                record_prior_preparation(run,s.stores,[C2,C2])
                self.assertEqual(s.admission.usage()['campaign_attempts'],41)
                s.meta.put_meta('lost_spending',dict(upper=3,resolved=True,evidence='Synthetic additional gap'))
                restore_tail(s.meta,'latest','No new exposure',boundary='new-boundary')
                self.assertEqual(s.admission.usage()['remaining'],456)
                packet=s.checkpoint('repaired-saved-course3')
                clone=Path(name)/'reopened';extract_selected(packet['path'],clone)
                self.assertEqual(canonical(analysis(clone)),canonical(json.loads((clone/'reports/analysis.json').read_text())))
                self.assertTrue((clone/'receipts/pre-transition/analysis.json').is_file())
                self.assertTrue((clone/'receipts/prior-studies'/f"{result['summary']['prior_spending'][0]['study_id']}.zip").is_file())
                self.assertEqual(len(analysis(clone)['attempts']),23)
            finally:s.close()
        self.assertEqual(before,{p:digest(p) for p in (C2,C3)})

    def test_missing_known_prior_or_unreviewed_source_never_publishes(self):
        with tempfile.TemporaryDirectory(prefix='i01-refuse-transition-') as name:
            run=Path(name)/'refused'
            with self.assertRaisesRegex(ValueError,'18 known prior'):continue_checkpoint(C3,run,ROOT,evidence='Fixture')
            self.assertFalse(run.exists())
            source=Path(name)/'altered-source'
            from recovery.i01.workflow import capture_source
            capture_source(ROOT,source)
            with (source/'recovery/i01/core.py').open('a') as stream:stream.write('\n# unreviewed scientific change\n')
            with self.assertRaisesRegex(ValueError,'Unreviewed scientific'):continue_checkpoint(C3,run,source,prior_checkpoints=[C2],evidence='Fixture')
            self.assertFalse(run.exists())

    def test_legacy_duplicate_slot_and_oversized_load_display(self):
        with tempfile.TemporaryDirectory(prefix='i01-legacy-slot-') as name:
            run=Path(name)/'legacy';extract_selected(C3,run)
            loads=[json.loads(r['evidence'])['load'] for r in analysis(run)['sessions']]
            from recovery.i01.ui import Operator
            ui=Operator.__new__(Operator);ui._last_action='load'
            displayed=[]
            with patch('recovery.i01.ui._display',side_effect=lambda html,plain:displayed.append(html)),redirect_stdout(io.StringIO()) as output:
                ui.show(dict(result=loads,error=None,checkpoint={}))
            self.assertLess(len(''.join(displayed))+len(output.getvalue()),12000)
            shutil.copy2(run/'worker-0.sqlite',run/'worker-1.sqlite')
            with self.assertRaisesRegex(ValueError,'Duplicate logical|Misplaced logical'):analysis(run)


if __name__=='__main__':unittest.main()
