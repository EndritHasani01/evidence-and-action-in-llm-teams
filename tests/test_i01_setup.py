"""Focused ensurepip failure recovery; tiny installer only, no model weights."""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from recovery.i01.setup import (PIP_BOOTSTRAP, SetupFailure, create_environment,
                               invoke, pip_wheel)


class Setup(unittest.TestCase):
    def test_failure_exposes_log_cause_and_preserves_previous_log(self):
        with tempfile.TemporaryDirectory() as name:
            log=Path(name)/'venv.log'; log.write_text('Previous ensurepip failure\n')
            with redirect_stdout(io.StringIO()):
                with self.assertRaises(SetupFailure) as caught:
                    invoke([sys.executable,'-c',"print('actual child error'); raise SystemExit(1)"],log,10)
            self.assertIn('actual child error',caught.exception.tail)
            self.assertIn('Previous ensurepip failure',log.read_text())
            self.assertIn('actual child error','\n'.join(caught.exception._render_traceback_()))

    def test_unknown_existing_directory_is_never_cleared(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name); venv=root/'venv'; venv.mkdir()
            sentinel=venv/'important.txt'; sentinel.write_text('preserve')
            with self.assertRaises(ValueError): create_environment(venv,root,root,dict(os.environ))
            self.assertEqual(sentinel.read_text(),'preserve')

    def test_corrupt_installer_is_refused_before_execution(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            with patch('recovery.i01.setup.urlopen',return_value=io.BytesIO(b'bad')),redirect_stdout(io.StringIO()):
                with self.assertRaises(ValueError): pip_wheel(root,root)
            self.assertFalse((root/'pip-bootstrap'/PIP_BOOTSTRAP['filename']).exists())

    def test_real_partial_venv_recovers_without_ensurepip(self):
        # This reproduces the completed venv shell left behind by failed
        # ensurepip. It installs only one 1.8 MB pinned pip wheel, not the runtime.
        with tempfile.TemporaryDirectory(prefix='i01-pip-') as name:
            root=Path(name); venv=root/'venv'; receipts=root/'receipts'; receipts.mkdir()
            subprocess.run([sys.executable,'-m','venv','--without-pip',str(venv)],check=True,timeout=60)
            sentinel=venv/'retain.txt'; sentinel.write_text('existing files retained')
            (receipts/'venv.log').write_text('Original ensurepip failed (1)\n')
            with patch('recovery.i01.setup.invoke',wraps=invoke) as commands,redirect_stdout(io.StringIO()):
                python=create_environment(venv,root,receipts,dict(os.environ))
            self.assertIn('--without-pip',commands.call_args_list[0].args[0])
            self.assertFalse(any('ensurepip' in str(c.args[0]) for c in commands.call_args_list))
            self.assertEqual(sentinel.read_text(),'existing files retained')
            self.assertIn('Original ensurepip failed',(receipts/'venv.log').read_text())
            probe="import json,pip,sys; print(json.dumps({'version':pip.__version__,'prefix':sys.prefix,'base':sys.base_prefix,'file':pip.__file__}))"
            value=json.loads(subprocess.check_output([str(python),'-I','-c',probe],text=True,timeout=30))
            self.assertEqual(value['version'],PIP_BOOTSTRAP['version'])
            self.assertNotEqual(value['prefix'],value['base'])
            self.assertTrue(Path(value['file']).resolve().is_relative_to(venv.resolve()))
            self.assertTrue(json.loads((receipts/'pip-bootstrap-wheel.json').read_text())['verified'])
            with patch('recovery.i01.setup.urlopen',side_effect=AssertionError('verified cache should be reused')):
                self.assertTrue(pip_wheel(root,receipts).exists())


if __name__=='__main__': unittest.main()
