"""Full-bound scripted assisted workflow, not a model/pilot/main experiment."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from recovery.i01.archive import export, extract_selected
from recovery.i01.core import canonical, diagnostic_fixture, manifests
from recovery.i01.policy import pilot_usefulness
from recovery.i01.report import analysis, write_report, DEGENERATE_WARNING
from recovery.i01.workflow import Session, initialize
from tests.test_i01_course3_repairs import prepare

ROOT=Path(__file__).parents[1]
CONFIG=json.loads((ROOT/'configs/i01-course-assisted.json').read_text())


class ScriptedAssisted:
    """An explicit oracle fixture uses private test metadata, never an LLM."""
    def __init__(self,manifest,correct_prefixes=3):
        self.calls=0;self.correct_prefixes=correct_prefixes;self.seeds={}
        for world in manifest['worlds']:
            for phase in ('prefix','recovery'):
                for agent in (0,1):
                    for invocation,seed in enumerate(world['seeds'][phase][agent]):
                        self.seeds[seed]=(world,phase,agent,invocation)
        self.diagnostics={diagnostic_fixture(manifest,label)['seed']:diagnostic_fixture(manifest,label)
                          for label in ('D00','D01','D02','D03')}
        pilot0=next(w for w in manifest['worlds'] if w['id']=='pilot-00')
        self.wrong_control=pilot0['control_seeds']['original']
    def obtain(self,request,timeout):
        self.calls+=1;view=request['view'];seed=request['seed']
        if request.get('control'):
            value=max(view['complete_input'])
            action=dict(message=None,submit=-1000 if seed==self.wrong_control else value,wait=False)
        elif seed in self.diagnostics:
            fixture=self.diagnostics[seed];label=fixture['label']
            # A conservative legal nonpass must not become a main veto.
            action=(dict(message='Please confirm',submit=None,wait=False) if label=='D01' else
                    dict(message=fixture['expected'] if label in ('D00','D03') else None,
                         submit=fixture['expected'] if label=='D02' else None,wait=False))
        else:
            world,phase,agent,invocation=self.seeds[seed]
            if phase=='recovery':
                action=dict(message='Rejected ordinary action',submit=None,wait=True)
            else:
                good=world['group']!='pilot' or world['index']<self.correct_prefixes
                action=dict(message=f"My local maximum is {max(view['current_shard'])}.",
                            submit=(world['original_truth'] if good else -1000) if invocation==2 else None,
                            wait=False)
        text=canonical(action);tokens=512 if request.get('envelope') else 1
        return dict(failure=None,visible_text=text,raw_text=text,generated_tokens=tokens,
                    ready_seconds=.001,input_tokens=1,token_ids=[1]*tokens,truncated=False,framing_error=None,
                    backend=dict(finite_score_steps=1,cache=dict(initial_empty=True,same_call_cache=True),
                                 observed_peak_free_lower_bytes=2**31))
    def close(self):return dict(termination_confirmed=True)


def checkpoint_without_repeated_plots(run,stores,*,boundary):
    # Test the real quiescent backup/transport per boundary; render separately once.
    return export(run,stores,boundary=boundary,reports=False)


class AssistedWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='i01-assisted-workflow-')
        self.run=Path(self.temp.name)/'study'
        self.manifest=initialize(self.run,ROOT,CONFIG,independent=True)
        self.session=None
        self.exports=patch('recovery.i01.workflow.export',side_effect=checkpoint_without_repeated_plots)
        self.exports.start()
    def tearDown(self):
        if self.session:self.session.close()
        self.exports.stop();self.temp.cleanup()
    def open(self,correct_prefixes=3):
        workers=[ScriptedAssisted(self.manifest,correct_prefixes) for _ in (0,1)]
        s=self.session=Session(self.run,ROOT,providers=workers,prepare_request=prepare)
        s.window((datetime.now(timezone.utc)+timedelta(hours=2)).isoformat(),'Synthetic CPU fixture only')
        s.meta.put_meta('loaded_session',s.session_id)
        for slot,store in enumerate(s.stores):store.put_meta('resident_load',f'{s.session_id}/fixture-{slot}')
        s.plan_execution();s.readiness();q=s.screen('direct')
        self.assertEqual(q['planned'],8);self.assertTrue(q['passed'])
        self.assertTrue(s.envelope()['passed'])
        probes=s.diagnostics();self.assertTrue(probes['complete'])
        self.assertEqual(sum(r['passed'] for r in probes['results']),3)
        s.checkpoint('prepared-with-diagnostics')
        self.assertEqual(s.admission.usage()['attempts'],20)
        return s,workers
    def pilots(self,s):
        for number in range(1,5):
            before=getattr(s,'checkpoint_timing',{}).get('successful_exports',0)
            result=s.run_action('pilot',number=number)
            self.assertIsNone(result['error'])
            checked=s.run_action('check_pilot',number=number)
            self.assertIsNone(checked['error']);self.assertTrue(checked['result']['passed'])
            self.assertEqual(s.checkpoint_timing['successful_exports']-before,2)
        self.assertEqual(s.admission.usage()['attempts'],100)

    def test_full_480_calls_ordinary_errors_do_not_veto_and_restore_replay_is_exact(self):
        s,workers=self.open();self.pilots(s)
        self.assertTrue(s.admit_main())
        for number in range(1,11):
            result=s.run_action('automatic_main',number=number)
            self.assertIsNone(result['error']);self.assertTrue(result['result']['passed'])
        self.assertEqual(s.admission.usage()['attempts'],480)
        self.assertEqual(s.admission.usage()['contingency'],0)
        result=analysis(self.run)
        self.assertEqual(result['summary']['status'],'complete')
        self.assertEqual(result['summary']['known_pairs'],20)
        self.assertEqual(result['summary']['paired_counts'],{'neither':20})
        self.assertEqual(result['summary']['interval']['caveat'],DEGENERATE_WARNING)
        self.assertIsNone(result['summary']['correct_prefix_interval'])
        self.assertEqual(len(result['pilot_checks']),4)
        self.assertEqual(len(result['qualification_controls']),8)
        self.assertEqual(len(result['diagnostics']),4)
        decision=result['summary']['assisted_feasibility']
        self.assertEqual((decision['correct_originals'],decision['correct_controls']),(3,7))
        # All 288 recovery actions fail legally, and the main population stays intact.
        self.assertEqual(sum(not r['legal_action'] for r in result['validation_details'] if r['phase'] in ('retain','clear')),288)
        before=sum(w.calls for w in workers)
        s.screen('direct');s.diagnostics();s.pilot(4);s.check_pilot(4)
        for number in range(1,11):s.automatic_main(number)
        self.assertEqual(sum(w.calls for w in workers),before)
        self.assertEqual(s.admission.usage()['attempts'],480)
        write_report(self.run,self.run/'reports',plot=False)
        saved=analysis(self.run)
        receipt=export(self.run,s.stores,boundary='complete-scripted-fixture',reports=False)
        restored=Path(self.temp.name)/'restored';extract_selected(receipt['path'],restored)
        self.assertEqual(analysis(restored),saved)
        s.close();self.session=None
        reopened=Session(restored,ROOT,providers=[ScriptedAssisted(self.manifest),ScriptedAssisted(self.manifest)],prepare_request=prepare)
        try:
            self.assertEqual(reopened.admission.usage()['attempts'],480)
            self.assertEqual(reopened.admission.usage()['remaining'],20)
            self.assertFalse(reopened.forecast()['measured_checkpoint_seconds'])
        finally:reopened.close()

    def test_failed_usefulness_collects_all_pilots_then_preserves_unknown_main(self):
        s,workers=self.open(correct_prefixes=2);self.pilots(s)
        before=sum(w.calls for w in workers)
        outcome=s.run_action('admit_main')
        self.assertIn('feasibility fails',outcome['error'])
        self.assertEqual(sum(w.calls for w in workers),before)
        result=analysis(self.run)
        self.assertEqual(result['summary']['known_pairs'],0)
        self.assertEqual(result['summary']['missingness_bounds'],[-1,1])
        self.assertEqual(result['summary']['assisted_feasibility']['correct_originals'],2)
        self.assertFalse(result['summary']['assisted_feasibility']['passed'])
        self.assertTrue(all(p['passed'] for p in result['pilot_checks']))
        self.assertFalse(s.meta.meta('freeze'))
        self.assertEqual(s.admission.usage()['attempts'],100)
        self.assertTrue(s.meta.meta('failure_cleanup')['termination_confirmed'])
        self.assertEqual(result['summary']['status'],'feasibility_complete')

    def test_reload_requires_six_state_plus_two_envelopes_and_keeps_scientific_calls(self):
        s,workers=self.open()
        for cycle in (1,2):
            for slot,store in enumerate(s.stores):store.put_meta('resident_load',f'{s.session_id}/reload-{cycle}-{slot}')
            with self.assertRaisesRegex(ValueError,'current-load'):
                s.qualified()
            with self.assertRaisesRegex(ValueError,'explicit eight-call'):
                s.readiness()
            self.assertTrue(s.envelope(reload=True)['passed'])
            self.assertEqual(s.admission.usage()['contingency'],8*cycle)
            before=sum(w.calls for w in workers)
            s.screen('direct');s.diagnostics();s.envelope(reload=True)
            self.assertEqual(sum(w.calls for w in workers),before)
        for slot,store in enumerate(s.stores):store.put_meta('resident_load',f'{s.session_id}/reload-3-{slot}')
        with self.assertRaisesRegex(ValueError,'Eight reserve attempts'):
            s.envelope(reload=True)
        self.assertEqual(s.admission.usage()['attempts'],36)

    def test_gate_boundary_uses_raw_controls_without_recovery_or_style_threshold(self):
        manifest=manifests(CONFIG)
        def tables(originals,controls):
            episodes=[];calls=[];number=0
            for world in (w for w in manifest['worlds'] if w['group']=='pilot'):
                for phase in ('prefix','retain','clear'):
                    key=world['id']+'/'+phase
                    value=world['original_truth'] if phase=='prefix' and world['index']<originals else -1000
                    episodes.append(dict(id=key,state=canonical(dict(terminal='both_submitted',submissions=[value,value]))))
                    calls.append(dict(id=key+'/call',episode=key,outcome='{}',effect_committed=1))
                for phase in ('original','revised'):
                    key=world['id']+'/control-'+phase+'-direct'
                    value=world[phase+'_truth'] if number<controls else -1000;number+=1
                    episodes.append(dict(id=key,state=canonical(dict(terminal='control_completed'))))
                    action=dict(message=None,submit=value,wait=False)
                    calls.append(dict(id=key,episode=key,outcome=canonical(dict(visible_text=canonical(action))),effect_committed=1))
            return dict(episodes=episodes,calls=calls)
        self.assertTrue(pilot_usefulness(manifest,tables(3,7))['passed'])
        self.assertFalse(pilot_usefulness(manifest,tables(2,7))['passed'])
        self.assertFalse(pilot_usefulness(manifest,tables(3,6))['passed'])
        missing=tables(3,7);missing['calls'][0]['effect_committed']=0
        self.assertFalse(pilot_usefulness(manifest,missing)['passed'])

    def test_precommit_and_fixed_clock_guard_before_any_attempt(self):
        workers=[ScriptedAssisted(self.manifest) for _ in (0,1)]
        s=self.session=Session(self.run,ROOT,providers=workers,prepare_request=prepare)
        deadline=datetime.now(timezone.utc)+timedelta(hours=2)
        s.window(deadline.isoformat(),'Synthetic fixed window')
        with self.assertRaisesRegex(ValueError,'cannot extend'):
            s.window((deadline+timedelta(minutes=1)).isoformat(),'Cell rerun')
        self.assertEqual(s.meta.meta('window')['deadline'],deadline.isoformat())
        request=prepare(dict(complete_input=[1]),0,'direct',control=True)
        with self.assertRaisesRegex(ValueError,'precommitted'):
            s.call(0,'hardware/unplanned','hardware/unplanned',request,'hardware')
        self.assertEqual(s.admission.usage()['attempts'],0)
        self.assertEqual(sum(w.calls for w in workers),0)

    def test_pending_raw_replay_does_not_consume_another_first_slot(self):
        s,workers=self.open();world=next(w for w in s.manifest['worlds'] if w['id']=='pilot-00')
        store=s.stores[world['device']];effects=store.effects
        def interrupted_effects(*args):raise RuntimeError('Synthetic stop after raw persistence')
        store.effects=interrupted_effects
        with self.assertRaisesRegex(RuntimeError,'after raw persistence'):s.pilot(1)
        store.effects=effects
        self.assertEqual(s.admission.usage()['attempts'],21)
        forecast=s.require_resources()
        self.assertEqual(forecast['pending_raw_replays'],1)
        self.assertEqual(forecast['remaining_first_stage_slots'],{'main':380,'pilot':79})
        self.assertEqual(forecast['remaining_new_model_attempts'],459)
        s.pilot(1)
        self.assertEqual(s.admission.usage()['attempts'],40)
        self.assertEqual(sum(w.calls for w in workers),40)


if __name__=='__main__':unittest.main()
