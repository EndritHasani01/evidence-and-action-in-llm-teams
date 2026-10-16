"""Real isolated startup/spawn and local-loader boundary; no GPU/model imports."""
import json
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from recovery.i01.runtime import command

ROOT=Path(__file__).parents[1]

class Runtime(unittest.TestCase):
    def test_real_venv_blocks_site_and_pth_hooks_and_preserves_spawn_prefix(self):
        with tempfile.TemporaryDirectory(prefix='i01-hooks-') as name:
            root=Path(name);venv=root/'venv'
            subprocess.run([sys.executable,'-I','-S','-m','venv','--without-pip',str(venv)],check=True,timeout=60)
            python=venv/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
            site=venv/'Lib/site-packages' if os.name=='nt' else venv/'lib'/f'python{sys.version_info.major}.{sys.version_info.minor}'/'site-packages'
            shutil.copytree(ROOT/'recovery',site/'recovery',ignore=shutil.ignore_patterns('__pycache__'))
            # Reuse small locally installed protocol dependencies; no network or
            # scientific runtime/model installation. Verify ordinary package
            # discovery while .pth processing is disabled.
            for name in ('pydantic','pydantic_core','annotated_types','typing_extensions','typing_inspection'):
                spec=importlib.util.find_spec(name)
                if spec.submodule_search_locations:
                    shutil.copytree(Path(spec.origin).parent,site/name,ignore=shutil.ignore_patterns('__pycache__'))
                else:shutil.copy2(spec.origin,site/Path(spec.origin).name)
            sentinel=root/'host-hook-ran';hook=f'import pathlib; pathlib.Path({str(sentinel)!r}).write_text("unapproved")\n'
            (site/'sitecustomize.py').write_text(hook)
            (site/'unapproved.pth').write_text(hook)
            (site/'fixture_worker.py').write_text('''import sys
class Factory:
    def __call__(self):
        self.load_report={'prefix':sys.prefix,'no_site':bool(sys.flags.no_site),'isolated':bool(sys.flags.isolated)}
        return self
''')
            code='''import json
from recovery.i01.runtime import inventory
from recovery.i01.process import Resident
from fixture_worker import Factory
worker=Resident(Factory())
try:print(json.dumps({'startup':inventory(),'spawn':worker.load(timeout=20)}))
finally:worker.close()
'''
            result=subprocess.run(command(python,ROOT,'-c',code),cwd=root,text=True,encoding='utf-8',capture_output=True,timeout=35)
            self.assertEqual(result.returncode,0,result.stderr)
            r=json.loads(result.stdout)
            self.assertEqual(Path(r['startup']['prefix']).resolve(),venv.resolve())
            self.assertEqual(Path(r['spawn']['prefix']).resolve(),venv.resolve())
            self.assertTrue(r['spawn']['no_site'] and r['spawn']['isolated'])
            self.assertFalse(sentinel.exists())
            self.assertFalse(r['startup']['hook_automatically_imported'])
            self.assertIn(str(site/'unapproved.pth'),r['startup']['pth_files'])
    def test_i01_factory_passes_verified_snapshot_to_reviewed_loader(self):
        from recovery.i01.inference import ModelFactory
        from recovery.prompts import COURSE_LIMITS
        backend=SimpleNamespace(load_report={},torch=SimpleNamespace(cuda=SimpleNamespace(get_device_properties=lambda device:SimpleNamespace(uuid='GPU-scripted',total_memory=1))))
        config=json.loads((ROOT/'configs/i01-course.json').read_text())
        with patch('recovery.inference.ModelFactory') as factory:
            factory.return_value.return_value=backend
            adapter=ModelFactory(config,'1','/verified/local/snapshot')()
        self.assertEqual(factory.call_args.kwargs['local_directory'],'/verified/local/snapshot')
        self.assertEqual(factory.call_args.args[2],COURSE_LIMITS)
        self.assertEqual(adapter.load_report['verified_snapshot'],'/verified/local/snapshot')
    def test_cached_environment_rechecks_inventory_and_preserves_existing_receipts(self):
        from recovery.i01.setup import install
        from recovery.i01.archive import digest
        from recovery.i01.workflow import source_files
        with tempfile.TemporaryDirectory(prefix='i01-cache-recheck-') as name:
            base=Path(name);source=base/'source';(source/'configs').mkdir(parents=True)
            for rel in ('configs/i01-course.json','configs/i01-runtime.lock','pyproject.toml'):
                shutil.copy2(ROOT/rel,source/rel)
            wheel=source/'source.whl';wheel.write_bytes(b'scripted wheel identity; never installed')
            scratch=base/'scratch';python=scratch/'i01-venv/bin/python';python.parent.mkdir(parents=True);python.write_bytes(b'scripted interpreter; never executed')
            working=base/'working';receipts=working/'i01-setup';receipts.mkdir(parents=True)
            saved={'identity':{'runtime_lock':digest(source/'configs/i01-runtime.lock'),'source_identity':source_files(source),'wheel_sha256':digest(wheel)},'interpreter':str(python)}
            path=receipts/'environment.json';path.write_text(json.dumps(saved));before=path.read_bytes()
            host={'system':'Linux','machine':'x86_64','python_version':[3,13,15],'gpus':[{'name':'T4'},{'name':'T4'}],'paths':{k:{'free':100*2**30} for k in ('scratch','working')}}
            with patch('recovery.i01.setup.host_inventory',return_value=host),patch('recovery.i01.setup.verify_environment') as verify:
                self.assertEqual(install(source,scratch,working),saved)
                verify.assert_called_once()
            self.assertEqual(path.read_bytes(),before)

if __name__=='__main__':unittest.main()
