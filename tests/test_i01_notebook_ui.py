"""Focused ordinary-cell behavior with fake controllers; zero model calls."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import io
import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from recovery.i01.ui import ActionStopped, Operator


class FakeClient:
    def __init__(self):
        self.calls=[]
        self.gates={}
        self.reply=dict(result={},error=None,checkpoint=dict(integrity='passed'))

    def command(self, op, **args):
        self.calls.append((op,args))
        if op=='status': return dict(gates=deepcopy(self.gates))
        if op=='forecast': return dict(remaining_attempt_allowance=500)
        return {}

    def action(self, name, **args):
        self.calls.append((name,args))
        return deepcopy(self.reply)


class NotebookUI(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='i01-ui-')
        root=Path(self.temp.name)
        with patch('recovery.i01.ui.host_inventory',return_value={}):
            self.ui=Operator(Path(__file__).parents[1],root/'scratch',root/'working',root/'run')
        self.client=FakeClient(); self.ui.client=self.client
        self.ui.show=lambda value:None
        self.ui.links=lambda:None

    def tearDown(self): self.temp.cleanup()

    def test_stopped_gate_and_checkpoint_fail_cell_without_next_stage(self):
        for reply in (dict(result=None,error='saved protocol defect',checkpoint={}),
                      dict(result=dict(passed=False),error=None,checkpoint=dict(integrity='passed')),
                      dict(result=dict(passed=True),error=None,checkpoint=dict(error='disk full'))):
            self.client.reply=reply
            with self.assertRaises(ActionStopped): self.ui.run('screen',mode='direct')
            self.assertFalse(self.ui.busy.locked())
        self.assertEqual([c[0] for c in self.client.calls if c[0]!='status'],['screen']*3)

    def test_conditional_thinking_never_falls_back_automatically(self):
        self.client.gates={'screen/direct':dict(passed=True,protocol_errors=0)}
        with redirect_stdout(io.StringIO()): self.assertTrue(self.ui.thinking_screen()['skipped'])
        self.assertNotIn('screen',[c[0] for c in self.client.calls])
        self.client.gates={'screen/direct':dict(passed=False,protocol_errors=0)}
        with self.assertRaises(ValueError): self.ui.thinking_screen()
        self.ui.thinking_screen('Observed arithmetic limitation in saved controls')
        self.assertEqual(self.client.calls[-1],('screen',dict(mode='thinking',reason='Observed arithmetic limitation in saved controls')))
        self.client.gates['screen/direct']['protocol_errors']=1
        with self.assertRaises(ValueError): self.ui.thinking_screen('Do not bypass a protocol defect')

    def test_selected_mode_and_reload_use_saved_state(self):
        self.client.reply=dict(result=None,error='No complete passing protocol qualification',checkpoint={'integrity':'passed'})
        with self.assertRaises(ValueError): self.ui.envelope()
        self.assertEqual([c for c in self.client.calls if c[0]=='envelope'],[('envelope',dict(reload=False))])
        self.client.reply=dict(result={},error=None,checkpoint={'integrity':'passed'})
        self.client.gates={'screen/direct':dict(passed=True)}
        self.ui.envelope()
        self.assertEqual(self.client.calls[-1],('envelope',dict(reload=False)))
        self.client.gates={'freeze':dict(mode='thinking'),'screen/direct':dict(passed=True)}
        self.ui.envelope(reload=True)
        self.assertEqual(self.client.calls[-1],('envelope',dict(reload=True)))

    def test_pilot_review_has_no_assumed_human_findings(self):
        with self.assertRaises(ValueError): self.ui.review_pilot(1)
        with self.assertRaises(ValueError): self.ui.review_pilot(1,useful_communication=1,usable=True,notes='actual review')
        self.assertFalse([c for c in self.client.calls if c[0]!='status'])
        self.ui.review_pilot(1,useful_communication=False,usable=True,notes='No useful public message in the original team')
        self.assertEqual(self.client.calls[-1][1]['useful_communication'],False)
        self.assertEqual(self.client.calls[-1][1]['scope'],'pilot-1')

    def test_saved_batch_only_and_derived_review_identity(self):
        with self.assertRaises(ValueError): self.ui.run_batch()
        with self.assertRaises(ValueError): self.ui.review_batch()
        self.client.gates={'batch':dict(id='batch/main-00+main-01',worlds=['main-00','main-01'],complete=False)}
        self.ui.run_batch()
        self.assertEqual(self.client.calls[-1],('main',{}))
        self.client.gates['batch']['complete']=True
        inspected=[]; self.ui.inspect=lambda **args:inspected.append(args)
        with redirect_stdout(io.StringIO()): self.ui.run_batch()
        self.assertEqual(sum(c[0]=='main' for c in self.client.calls),1)
        self.ui.review_batch()
        self.assertEqual(self.client.calls[-1][1]['scope'],'batch/main-00+main-01')
        self.assertIn('not verified',self.client.calls[-1][1]['notes'])
        self.assertNotIn('prepare_batch',[c[0] for c in self.client.calls])

    def test_open_needs_no_window_but_explicit_window_needs_actual_facts(self):
        self.ui.client=None
        self.ui.deadline='stale'; self.ui.allowance_evidence='old session'
        with patch.object(self.ui,'run',return_value={'attempts':0}) as run:
            self.ui.open_study('reopen')
            run.assert_called_once_with('initialize',mode='reopen',selected=None,tail=None,evidence='')
        self.assertIsNone(self.ui.deadline)
        self.assertIsNone(self.ui.allowance_evidence)
        with self.assertRaises(ValueError): self.ui.set_window(None,'')
        with self.assertRaises(ValueError): self.ui.set_window('2099-01-01T10:00:00','observed allowance')
        with self.assertRaises(ValueError): self.ui.set_window((datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat(),'observed allowance')
        self.assertFalse(self.client.calls)

    def test_keyboard_interrupt_preserves_existing_pause_path(self):
        self.ui.run_action=lambda *a,**k: (_ for _ in ()).throw(KeyboardInterrupt())
        with redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(KeyboardInterrupt): self.ui.run('main')
        self.assertIn('An admitted call may still be active',output.getvalue())
        self.assertFalse(self.ui.busy.locked())

    def test_client_interrupt_requests_pause_without_claiming_settlement(self):
        from recovery.i01.client import Client
        import threading
        client=Client.__new__(Client)
        client.lock=threading.RLock(); client.results={}
        class Running:
            def poll(self): return None
        client.process=Running()
        calls=[]; client.command=lambda op:calls.append(op)
        with patch('recovery.i01.client.time.sleep',side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt): client.wait('saved-action')
        self.assertEqual(calls,['pause'])

    def test_conversation_and_receipts_escape_raw_text(self):
        from recovery.i01.workflow import initialize
        from recovery.i01.core import initial_episode, apply_outcome, canonical
        from recovery.i01.store import Store
        source=Path(__file__).parents[1]
        manifest=initialize(self.ui.run_dir,source,json.loads((source/'configs/i01-course.json').read_text()))
        world=manifest['worlds'][6]
        state=apply_outcome(initial_episode(world,'prefix'),0,dict(message='<script>bad()</script>',submit=None,wait=False),None,'scripted-call')
        store=Store(self.ui.run_dir/f"worker-{world['device']}.sqlite",{'manifest':manifest})
        try:
            with store.transaction():
                store.db.execute('INSERT INTO episodes VALUES (?,?)',(world['id']+'/prefix',canonical(state)))
        finally: store.close()
        rendered=[]
        with patch('recovery.i01.ui._display',side_effect=lambda body,plain:rendered.append(body)),redirect_stdout(io.StringIO()):
            self.ui.inspect(world=world['id'],audit_limit=None,downloads=False)
            Operator.show(self.ui,dict(result=None,error='<script>bad()</script>',checkpoint={}))
        html='\n'.join(rendered)
        self.assertNotIn('<script>bad()',html)
        self.assertIn('&lt;script&gt;bad()',html)
        self.assertIn('Unknown / not executed',html)


if __name__=='__main__': unittest.main()
