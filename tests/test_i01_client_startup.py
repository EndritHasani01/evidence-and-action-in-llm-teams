"""Real lightweight child failures; no model imports, downloads or inference."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from recovery.i01.client import Client, ControllerStartupError, child_environment


class Startup(unittest.TestCase):
    def test_child_environment_preserves_credentials_and_parent(self):
        polluted=dict(PYTHONPATH='host hook',MPLBACKEND='module://host.renderer',
                      PYTHONHOME='host interpreter',PIP_TARGET='host packages',
                      HF_TOKEN='scripted-not-a-real-secret',HTTPS_PROXY='scripted-proxy')
        with patch.dict(os.environ,polluted):
            child=child_environment('/scripted/cache')
            self.assertNotIn('PYTHONPATH',child)
            self.assertNotIn('PYTHONHOME',child)
            self.assertNotIn('PIP_TARGET',child)
            self.assertEqual(child['MPLBACKEND'],'Agg')
            self.assertEqual(child['HF_TOKEN'],polluted['HF_TOKEN'])
            self.assertEqual(child['HTTPS_PROXY'],polluted['HTTPS_PROXY'])
            self.assertEqual(os.environ['MPLBACKEND'],polluted['MPLBACKEND'])

    def launch_failure(self,code,timeout):
        actual_popen=subprocess.Popen
        processes=[]
        def launch(args,**kwargs):
            # Keep Client's actual pipes/environment/lifecycle, substitute only
            # the child program to provoke a known startup failure.
            process=actual_popen([sys.executable,'-u','-c',code],**kwargs)
            processes.append(process)
            return process
        with tempfile.TemporaryDirectory(prefix='i01-startup-') as name:
            run=Path(name); receipts=run/'receipts'; receipts.mkdir()
            log=receipts/'controller-stderr.log'
            log.write_text('Earlier startup evidence\n')
            started=time.monotonic()
            with patch('recovery.i01.client.subprocess.Popen',side_effect=launch):
                with self.assertRaises(ControllerStartupError) as raised:
                    Client(sys.executable,run,run,run/'cache',startup_timeout=timeout)
            error=raised.exception
            self.assertIn('scripted startup cause',error.tail)
            self.assertNotIn('Earlier startup evidence',error.tail)
            self.assertIn('scripted startup cause','\n'.join(error._render_traceback_()))
            self.assertTrue(log.read_text().startswith('Earlier startup evidence'))
            self.assertIsNotNone(processes[0].poll())
            self.assertTrue(processes[0].stdin.closed)
            self.assertTrue(processes[0].stdout.closed)
            # A new writer can append, including on Windows (no leaked handle).
            with log.open('a') as stream: stream.write('Later evidence\n')
            return str(error),time.monotonic()-started

    def test_early_exit_shows_cause_without_waiting_for_startup_timeout(self):
        message,elapsed=self.launch_failure(
            'import sys; print("scripted startup cause",file=sys.stderr); sys.exit(17)',30)
        self.assertIn('exited before ready',message)
        self.assertIn('exit=17',message)
        self.assertLess(elapsed,10)

    def test_pre_ready_hang_is_terminated_and_cause_preserved(self):
        message,elapsed=self.launch_failure(
            'import sys,time; print("scripted startup cause",file=sys.stderr,flush=True); time.sleep(60)',.5)
        self.assertIn('startup deadline exceeded',message)
        self.assertLess(elapsed,20)


if __name__=='__main__': unittest.main()
