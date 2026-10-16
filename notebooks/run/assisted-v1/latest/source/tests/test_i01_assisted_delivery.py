"""Finite notebook/source/CPU operator checks; no inference or model load."""
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from recovery.i01.archive import atomic_json
from recovery.i01.checks import input_separation
from recovery.i01.notebook import Study
from scripts.build_i01_course_notebook import notebook,research_notebook
from scripts.verify_i01_course_release import verify_notebook

ROOT=Path(__file__).parents[1]
CONFIG=json.loads((ROOT/'configs/i01-course-assisted.json').read_text())


class AssistedDelivery(unittest.TestCase):
    def test_new_and_legacy_notebooks_keep_complete_finite_scopes(self):
        with redirect_stdout(io.StringIO()):
            old=verify_notebook(notebook());new=verify_notebook(notebook(assisted=True))
        self.assertEqual((old['code_cells'],old['first_attempt_ceiling']),(33,460))
        self.assertEqual((new['code_cells'],new['first_attempt_ceiling']),(37,480))
        self.assertEqual(notebook(assisted=True),research_notebook(assisted=True))
        self.assertIn('diagnostics',new['independent_cell_scopes'])
        self.assertIn('pilot-4',new['independent_cell_scopes'])
        self.assertEqual(new['independent_cell_scopes']['prepared-checkpoint'][0]['kwargs'],{'verify':True})
        workspace=''.join(next(c for c in notebook(assisted=True)['cells'] if c.get('id')=='workspace')['source'])
        self.assertIn('assisted=True',workspace)
        self.assertIn('i01-assisted-feasibility-2026-10-16',workspace)

    def test_actual_exposed_inventory_and_exact_packet_world_binding(self):
        proof=input_separation(ROOT,CONFIG)
        self.assertTrue(proof['passed']);self.assertEqual(proof['checked_new_inputs'],56)
        self.assertEqual(proof['historical_courses'],list(range(1,8)))
        self.assertEqual(len(proof['new_worlds']),28)
        with tempfile.TemporaryDirectory(prefix='i01-input-proof-') as name:
            source=Path(name);atomic_json(source/'source-release.json',dict(input_separation=proof))
            self.assertEqual(input_separation(source,CONFIG),proof)
            changed=deepcopy(proof);changed['new_worlds'][0]['original'][0][0]+=1
            atomic_json(source/'source-release.json',dict(input_separation=changed))
            with self.assertRaisesRegex(ValueError,'exact config-bound'):
                input_separation(source,CONFIG)
            (source/'source-release.json').unlink()
            with self.assertRaisesRegex(ValueError,'Incomplete exposed'):
                input_separation(source,CONFIG)

    def test_real_assisted_operator_opens_inspects_and_exports_without_model_calls(self):
        with tempfile.TemporaryDirectory(prefix='i01-assisted-ui-') as name:
            base=Path(name)
            (base/'working').mkdir()
            with patch('recovery.i01.ui.host_inventory',return_value={}):
                study=Study(ROOT,base/'scratch',base/'working',base/'study',assisted=True)
            study.environment={'interpreter':sys.executable}
            study.show=lambda result:None;study.links=lambda *args,**kwargs:None;study.emit=lambda value:None
            try:
                with redirect_stdout(io.StringIO()) as output:
                    study.open('new',independent=True)
                    status=study.show_status()
                    self.assertEqual(status['attempts'],0)
                    self.assertEqual(status['qualification']['direct']['planned'],8)
                    self.assertEqual(status['contingency_limit'],20)
                    inspected=study.inspect_qualification('direct')
                    receipt=study.save_checkpoint(verify=True)
                self.assertEqual(len(inspected['diagnostics']),4)
                self.assertIn('0/8',output.getvalue())
                self.assertNotIn('0/12',output.getvalue())
                self.assertEqual(receipt['checkpoint']['attempts'],0)
                self.assertEqual(receipt['checkpoint']['integrity'],'passed')
                manifest=json.loads((base/'study/run.json').read_text())
                self.assertEqual(manifest['config']['regime'],'i01-course-assisted-v2')
                self.assertEqual(study.client.command('status')['usage']['attempts'],0)
            finally:
                if study.client:study.client.close()


if __name__=='__main__':unittest.main()
