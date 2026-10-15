"""Course-1 counterexamples; temporary scripted evidence, no model inference."""
from datetime import datetime,timedelta,timezone
import json
from pathlib import Path
import tempfile
import threading
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import patch

from recovery.i01.core import canonical
from recovery.i01.workflow import initialize,Session
from recovery.i01.report import analysis,write_report

ROOT=Path(__file__).parents[1]

def prepare(view,seed,mode,**flags):
    return dict(view=view,seed=seed,settings={'mode':mode},input_ids=[1],rendered=canonical(view),**flags)

class Worker:
    def __init__(self): self.calls=0;self.reply=None
    def obtain(self,request,timeout):
        self.calls+=1
        if self.reply: return self.reply(request)
        return dict(failure=None,visible_text='',ready_seconds=.001,input_tokens=1,generated_tokens=512,
                    token_ids=[request['seed']],backend=dict(finite_score_steps=1,
                    cache=dict(initial_empty=True,same_call_cache=True),observed_peak_free_lower_bytes=2**31))
    def close(self): return dict(termination_confirmed=True)

class Repairs(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='i01-repair-');self.run=Path(self.temp.name)/'run'
        self.manifest=initialize(self.run,ROOT,json.loads((ROOT/'configs/i01-course.json').read_text()))
        self.session=None
    def tearDown(self):
        if self.session:self.session.close()
        self.temp.cleanup()
    def open(self):
        workers=[Worker(),Worker()]
        self.session=Session(self.run,providers=workers,prepare_request=prepare)
        self.session.window((datetime.now(timezone.utc)+timedelta(hours=2)).isoformat(),'Scripted test only')
        for slot,store in enumerate(self.session.stores):store.put_meta('resident_load',f'{self.session.session_id}/load-{slot}')
        return self.session,workers
    def test_missing_database_or_table_never_recreated(self):
        for slot in (0,1):
            p=self.run/f'worker-{slot}.sqlite';saved=p.with_suffix('.saved');p.rename(saved)
            with self.assertRaisesRegex(ValueError,'Missing canonical'):Session(self.run)
            self.assertFalse(p.exists());saved.rename(p)
        from recovery.i01.store import connection
        db=connection(self.run/'worker-1.sqlite')
        try:db.execute('DROP TABLE attempts');db.commit()
        finally:db.close()
        with self.assertRaisesRegex(ValueError,'Incomplete canonical'):Session(self.run)
        db=connection(self.run/'worker-1.sqlite',True)
        try:self.assertFalse(db.execute("SELECT name FROM sqlite_master WHERE name='attempts'").fetchone())
        finally:db.close()
    def test_partial_initialization_is_not_published(self):
        from recovery.i01.store import Store
        path=Path(self.temp.name)/'new'
        count=0
        def create(*args,**kwargs):
            nonlocal count
            count+=1
            if count==2:raise ValueError('scripted initialization interruption')
            return Store(*args,**kwargs)
        with patch('recovery.i01.workflow.Store',side_effect=create):
            with self.assertRaises(ValueError):initialize(path,ROOT,self.manifest['config'])
        self.assertFalse(path.exists())
    def test_each_replaced_load_pair_gets_two_probes_and_exact_rerun_zero(self):
        s,w=self.open();s.screen_result=lambda mode:dict(passed=True);s.envelope('direct')
        for n in (1,2):
            s.stores[1].put_meta('resident_load',f'{s.session_id}/replacement-{n}')
            s.meta.put_meta('reload_required',True);before=sum(x.calls for x in w)
            self.assertTrue(s.envelope('direct',reload=True)['passed'])
            self.assertEqual(sum(x.calls for x in w)-before,2)
            s.envelope('direct',reload=True)
            self.assertEqual(sum(x.calls for x in w)-before,2)
        self.assertEqual(s.admission.usage()['contingency'],4)
    def test_original_and_revised_control_labels_and_empty_export(self):
        s,w=self.open();world=s.manifest['worlds'][0]
        write_report(self.run,self.run/'reports',plot=False)
        self.assertIn('No model calls',(self.run/'reports/conversations.txt').read_text())
        for mode in ('direct','thinking'):
            for phase in ('original','revised'):
                w[world['device']].reply=lambda req,phase=phase:dict(failure=None,visible_text=canonical(dict(message=None,submit=world[phase+'_truth'],wait=False)),ready_seconds=.001,input_tokens=1,generated_tokens=1)
                self.assertEqual(s.control(world,phase,mode,stage=mode)['correct'],1)
        self.assertEqual(analysis(self.run)['failure_analysis'],[])
    def test_failed_second_world_pauses_before_first_completes(self):
        s,w=self.open();s.qualified=lambda:'direct';s.meta.put_meta('freeze',{'mode':'direct'})
        s.meta.put_meta('batch',dict(worlds=['main-00','main-01'],complete=False))
        release=threading.Event();failed=threading.Event();errors=[]
        def world(case,mode):
            if case['id']=='main-00':release.wait(5)
            else:failed.set();raise ValueError('scripted second world failure')
        s.world=world
        def main():
            try:s.main()
            except ValueError as exc:errors.append(str(exc))
        thread=threading.Thread(target=main);thread.start()
        try:self.assertTrue(failed.wait(5));self.assertTrue(s.pause.wait(5))
        finally:release.set();thread.join(5)
        self.assertTrue(errors);self.assertFalse(s.meta.meta('batch')['complete'])
    def test_periodic_control_export_after_settlement(self):
        s,w=self.open();world=s.manifest['worlds'][0]
        w[0].reply=lambda req:dict(failure=None,visible_text=canonical(dict(message=None,submit=world['original_truth'],wait=False)),ready_seconds=.001,input_tokens=1,generated_tokens=1)
        s.last_checkpoint=0;seen=[]
        def checkpoint(boundary):self.assertFalse(s.active_calls);seen.append(boundary)
        s.checkpoint=checkpoint;s.control(world,'original','direct',stage='direct')
        self.assertEqual(seen,['periodic-settled-call-boundary'])
    def test_aba_differences_require_review_without_resampling(self):
        s,w=self.open();s.meta.put_meta('loaded_session',s.session_id)
        for worker in w:
            original=worker.obtain
            worker.obtain=lambda req,timeout,worker=worker,original=original:dict(original(req,timeout),token_ids=[worker.calls])
        r=s.readiness();self.assertTrue(r['needs_review'])
        with self.assertRaisesRegex(ValueError,'A/B/A differs'):s.screen('direct')
        self.assertEqual(sum(x.calls for x in w),6)
        (self.run/'exports').mkdir();(self.run/'exports/latest.zip').write_bytes(b'scripted archive prerequisite')
        s.review('readiness','Inspected exact fixture cache and token records; diagnostic discrepancy documented')
        self.assertTrue(s.meta.meta('review/readiness'))
    def test_named_session_load_rerun_expiration_and_disconnected_inspection(self):
        from recovery.i01.notebook import Study
        from recovery.i01.ui import ActionStopped
        s,w=self.open();s.workers=[None,None];s.meta.put_meta('selfcheck',{'passed':True,'native_tokenizer':True})
        host={'gpus':[{'uuid':str(i),'name':'Tesla T4'} for i in range(2)]}
        class Resident:
            def __init__(self,factory,termination):self.slot=int(factory.device);self.process=None;self.unconfirmed=False
            def load(self,timeout):
                self.process=SimpleNamespace(is_alive=lambda:True)
                self.load_report={'cuda_device_uuid':'GPU-'+str(self.slot),'total_device_bytes':1,'load_seconds':0}
                return self.load_report
            def close(self):self.process=None;return {'termination_confirmed':True}
        class Client:
            def __init__(self):self.process=SimpleNamespace(poll=lambda:None);self.dead=False
            def command(self,op):
                if self.dead:raise ValueError('controller exited')
                return s.status() if op=='status' else s.forecast()
            def action(self,action,**args):return s.run_action(action,**args)
        base=Path(self.temp.name)
        with patch('recovery.i01.ui.host_inventory',return_value=host):ui=Study(ROOT,base/'scratch',base/'working',self.run)
        ui.client=Client();ui.environment={'interpreter':sys.executable};ui.weights={'snapshot':'/scripted/local/snapshot'}
        ui.show=lambda x:None;ui.links=lambda:None
        with self.assertRaises(ActionStopped):ui.configure_session()
        self.assertEqual(s.admission.usage()['attempts'],0)
        self.assertTrue((self.run/'receipts/operator-errors.jsonl').exists())
        ui.configure_session(remaining_minutes=60,evidence='Scripted test observation only')
        deadline=ui.deadline
        ui.configure_session(remaining_minutes=60,evidence='Same cell rerun')
        self.assertEqual(ui.deadline,deadline)
        with patch('recovery.i01.setup.runtime_inventory',return_value={}),patch('recovery.i01.process.Resident',Resident),patch.dict(sys.modules,transformers=SimpleNamespace(AutoTokenizer=SimpleNamespace(from_pretrained=lambda *a,**kw:object()))),patch('recovery.i01.ui.host_inventory',return_value=host):
            ui.load_models();refs=s.load_references();ui.load_models()
            self.assertEqual(s.load_references(),refs)
        self.assertEqual(s.admission.usage()['attempts'],0)
        s.meta.put_meta('window',{'session':s.session_id,'deadline':'2000-01-01T00:00:00+00:00','evidence':'expired fixture'})
        with patch('recovery.i01.setup.runtime_inventory',return_value={}),patch('recovery.i01.ui.host_inventory',return_value=host):
            with self.assertRaisesRegex(ActionStopped,'deadline'):ui.load_models()
        self.assertEqual(s.admission.usage()['attempts'],0)
        ui.client.dead=True
        with patch('recovery.i01.ui._display',return_value=None):
            self.assertEqual(ui.inspect(audit_limit=0,downloads=False)['summary']['attempts'],0)

if __name__=='__main__':unittest.main()
