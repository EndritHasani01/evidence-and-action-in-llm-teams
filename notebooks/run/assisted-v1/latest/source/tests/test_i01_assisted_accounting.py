"""Assisted campaign admission and raw replay limits; synthetic CPU records only."""
import json
from pathlib import Path
import tempfile
import unittest

from recovery.i01.core import manifests
from recovery.i01.store import Admission, Store, restore_tail
from recovery.i01.workflow import initialize

ROOT=Path(__file__).parents[1]
CONFIG=json.loads((ROOT/'configs/i01-course-assisted.json').read_text())


class AssistedAccounting(unittest.TestCase):
    def test_joint_stage_reserve_total_caps_and_exact_interruption_retry(self):
        with tempfile.TemporaryDirectory(prefix='i01-assisted-admission-') as name:
            manifest=manifests(CONFIG);run=Path(name)
            stores=[Store(run/f'worker-{i}.sqlite',{'manifest':manifest},create=True) for i in (0,1)]
            try:
                owner=Admission(stores);store=stores[0]
                request=dict(view={},seed=1,settings={'mode':'direct'},input_ids=[1],rendered='synthetic')
                outcome=dict(visible_text='{}',ready_seconds=.001,generated_tokens=1)
                for stage,count in owner.first_limits.items():
                    for i in range(count):
                        cid=f'{stage}/{i}';store.register(cid,cid,request)
                        attempt=owner.admit(store,cid,stage)
                        if stage=='hardware' and i<4:
                            with self.assertRaisesRegex(ValueError,'unresolved attempt'):
                                owner.admit(store,cid,stage)
                            owner.reconcile(store,attempt,dict(termination_confirmed=True,reason='Scripted pre-outcome loss'))
                            with self.assertRaisesRegex(ValueError,'stage'):
                                owner.admit(store,cid,'pilot')
                            attempt=owner.admit(store,cid,stage)
                        store.raw(cid,attempt,outcome)
                        with self.assertRaisesRegex(ValueError,'completed call'):
                            owner.admit(store,cid,stage)
                    cid=f'{stage}/over';store.register(cid,cid,request)
                    with self.assertRaisesRegex(ValueError,'stage first-attempt'):
                        owner.admit(store,cid,stage)
                    with self.assertRaisesRegex(ValueError,'not ordinary scope'):
                        owner.admit(store,cid,stage,contingency=True)
                self.assertEqual(owner.usage()['attempts'],484)
                self.assertEqual(owner.usage()['contingency'],4)
                for i in range(16):
                    cid=f'hardware/state-0-A/reload-fixture-{i}'
                    store.register(cid,cid,request)
                    attempt=owner.admit(store,cid,'hardware',contingency=True)
                    store.raw(cid,attempt,outcome)
                self.assertEqual(owner.usage()['attempts'],500)
                self.assertEqual(owner.usage()['contingency'],20)
                store.register('hardware/extra/reload-fixture','extra',request)
                with self.assertRaisesRegex(ValueError,'whole-study allowance'):
                    owner.admit(store,'hardware/extra/reload-fixture','hardware',contingency=True)
                self.assertEqual(sum(not a['contingency'] for s in stores for a in s.rows('attempts')),480)
            finally:
                for store in stores:store.close()

    def test_initialization_is_explicit_independent_and_unknown_tail_blocks(self):
        with tempfile.TemporaryDirectory(prefix='i01-assisted-init-') as name:
            run=Path(name)/'study'
            with self.assertRaisesRegex(ValueError,'independent'):
                initialize(run,ROOT,CONFIG)
            manifest=initialize(run,ROOT,CONFIG,independent=True)
            self.assertEqual(len(manifest['worlds']),28)
            stores=[Store(run/f'worker-{i}.sqlite',{'manifest':manifest}) for i in (0,1)]
            try:
                owner=Admission(stores)
                self.assertEqual(owner.contingency,20)
                self.assertEqual(owner.usage()['missing_prior_studies'],[])
                restore_tail(stores[0],'unknown','Synthetic unknown tail',boundary='test')
                stores[0].register('pending','pending',dict(view={},seed=1,settings={}))
                with self.assertRaisesRegex(ValueError,'lost spending unresolved'):
                    owner.admit(stores[0],'pending','direct')
                self.assertEqual(owner.usage()['attempts'],0)
                with self.assertRaisesRegex(ValueError,'500 total and 20'):
                    Admission(stores,contingency=28)
            finally:
                for store in stores:store.close()


if __name__=='__main__':unittest.main()
