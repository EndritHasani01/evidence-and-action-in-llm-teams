"""Real source/SQLite/export/process tests with named external outcomes controlled."""

from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import warnings
import zipfile

from scripts.build_kaggle_bundle import BASELINE_COMMIT, archive_manifest
from scripts import m5_kaggle_preflight as preflight
from scripts.m5_kaggle_continue import continue_preflight


def zip_bytes(members):
    output = io.BytesIO()
    with zipfile.ZipFile(output,"w") as archive:
        for name,content in members.items():
            archive.writestr(name,content)
    return output.getvalue()


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.inputs,self.output,self.scratch = [self.root/n for n in ('input','output','scratch')]
        self.inputs.mkdir()
        self.payload = self.inputs/'m5-kaggle-source.payload'
        self.members = {'SOURCE_COMMIT.txt':(BASELINE_COMMIT+'\n').encode(),
                        'recovery/__init__.py':b'"""Synthetic package."""\n',
                        'pyproject.toml':b'[build-system]\nrequires=["setuptools>=68"]\n',
                        'tests/fixtures/capacity_report.json.gz':b'synthetic-compressed-marker'}
        self.payload.write_bytes(zip_bytes(self.members))
        self.expected = archive_manifest(self.payload)
        self.wheel_bytes = {}
        files=[]
        for name,version in preflight.PINNED.items():
            filename=f'{name.replace("-","_")}-{version}-py3-none-any.whl'
            content=zip_bytes({'marker':name.encode()})
            self.wheel_bytes[filename]=content
            files.append({'name':name,'version':version,'filename':filename,'bytes':len(content),
                          'sha256':hashlib.sha256(content).hexdigest(),'url':'https://files.pythonhosted.org/'+filename})
        self.lock=''.join(f"{p['name']}=={p['version']} --hash=sha256:{p['sha256']}\n" for p in files)
        tools={}
        for name,version in [('pip','26.2.1'),('setuptools','84.0.0'),('wheel','0.48.0')]:
            filename=f'{name}-{version}-py3-none-any.whl'
            content=zip_bytes({'marker':name.encode()});self.wheel_bytes[filename]=content
            tools[name]={'version':version,'wheels':[{'filename':filename,'bytes':len(content),
                 'sha256':hashlib.sha256(content).hexdigest(),'url':'https://files.pythonhosted.org/'+filename}]}
        self.expected.update(candidate_lock_sha256=hashlib.sha256(self.lock.encode()).hexdigest(),
                             candidate_wheels=files,build_tools=tools,build_commit='a'*40)
        self.command_calls=[]
        self.fault=None

    def controlled_command(self,output,name,args,**kwargs):
        self.command_calls.append((name,list(map(str,args)),kwargs))
        logs=output/'logs';logs.mkdir(exist_ok=True)
        stdout,stderr=logs/(name+'.stdout.txt'),logs/(name+'.stderr.txt')
        stdout.write_text('');stderr.write_text('harmless controlled warning\n')
        if self.fault==name:
            raise RuntimeError('controlled '+name+' failure')
        scratch=kwargs['cwd'] if name!='focused-checks' and not name.startswith('native-') else kwargs['cwd'].parent
        if name=='create-venv':
            directory=Path(args[-1]);directory.mkdir()
            (directory/'pyvenv.cfg').write_text('include-system-site-packages = false\n')
        elif name=='download-pip-wheel':
            wanted=self.expected['build_tools']['pip']['wheels'][0]
            directory=scratch/'pip-bootstrap'
            (directory/wanted['filename']).write_bytes(self.wheel_bytes[wanted['filename']])
            stdout.write_text(json.dumps(dict(wanted,verified=True)))
            if self.fault=='empty-pip-receipt': stdout.write_text('{}')
            if self.fault=='corrupt-pip-wheel': (directory/wanted['filename']).write_bytes(b'corrupt')
        elif name in {'download-candidate','download-build-tools'}:
            destination=Path(args[args.index('--dest')+1])
            wanted=self.expected['candidate_wheels'] if name=='download-candidate' else [
                self.expected['build_tools'][n]['wheels'][0] for n in ['setuptools','wheel']]
            for p in wanted: (destination/p['filename']).write_bytes(self.wheel_bytes[p['filename']])
        elif name=='resolve-candidate':
            report={'install':[{'metadata':{'name':p['name'],'version':p['version']}}
                               for p in self.expected['candidate_wheels']]}
            Path(args[args.index('--report')+1]).write_text(json.dumps(report))
        elif name=='build-source':
            directory=Path(args[args.index('--wheel-dir')+1])
            (directory/'synthetic_project-0.1-py3-none-any.whl').write_bytes(zip_bytes(self.members))
        elif name=='installed-probe':
            result={'versions':dict(preflight.PINNED),'verified_module_hashes':{
                    n:hashlib.sha256(b).hexdigest() for n,b in self.members.items()
                    if n.startswith('recovery/') and n.endswith('.py')},
                    'qwen_text_class':'Qwen3_5ForCausalLM','torch_cuda_build':'12.8','model_generations':0}
            stdout.write_text('[ERROR] controlled third-party documentation diagnostic\n')
            machine=output/'installed-probe-result.json'
            machine.write_text(json.dumps(result))
            if self.fault=='malformed-probe': machine.write_text('warning before JSON\n{}')
            if self.fault=='empty-probe': machine.write_text('{}')
            if self.fault=='missing-probe': machine.unlink()
        elif name=='pip-list': stdout.write_text('[]')
        elif name in {'focused-checks','native-9b','native-4b','native-capacity'}:
            count={'focused-checks':81,'native-9b':4,'native-4b':4,'native-capacity':8}[name]
            stderr.write_text(f'Ran {count} tests in 0.1s\n\nOK\n')
            if self.fault=='skipped-checks' and name=='focused-checks':
                stderr.write_text('Ran 81 tests in 0.1s\n\nOK (skipped=1)\n')
        return {'name':name,'stdout':stdout.relative_to(output).as_posix(),
                'stderr':stderr.relative_to(output).as_posix(),'exit_code':0,'leader_exited':True}

    def controlled_run(self):
        with patch.object(preflight.platform,'system',return_value='Linux'), \
             patch.object(preflight.platform,'machine',return_value='x86_64'), \
             patch.object(preflight.sys,'version_info',(3,13,15,'final',0)), \
             patch.object(preflight,'command',side_effect=self.controlled_command), \
             patch.object(preflight,'process_tree_diagnostic',return_value={'scope':'controlled Linux process diagnostic'}):
            return preflight.run_preflight(self.inputs,self.output,self.scratch,self.expected,self.lock)

    def assert_export(self,result):
        path=Path(result['zip_path'])
        self.assertEqual(preflight.sha256_file(path),result['zip_sha256'])
        with zipfile.ZipFile(path) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(json.loads(archive.read('summary.json')),result['summary'])
            self.assertNotIn('source/',archive.namelist())
            self.assertFalse(any('/venv/' in p or p.endswith('.whl') for p in archive.namelist()))

    def test_complete_controlled_workflow_preserves_inputs_and_isolates_modes(self):
        original=self.payload.read_bytes()
        result=self.controlled_run()
        self.assertTrue(result['summary']['preparation_checks_passed'])
        self.assertEqual(result['summary']['tests_passed'],97)
        self.assertEqual(result['summary']['model_generations'],0)
        self.assertFalse(result['summary']['model_smoke_ready'])
        self.assertEqual(self.payload.read_bytes(),original)
        self.assert_export(result)
        for name,args,kwargs in self.command_calls:
            if name=='create-venv': self.assertIn('--without-pip',args)
            if name=='bootstrap-pip':
                self.assertIn('-I',args);self.assertIn('--no-index',args)
                self.assertNotIn('--index-url',args)
                self.assertIn(preflight.PIP_WHEEL_RUNNER,args)
            if name=='installed-probe':
                self.assertIn('-I',args);self.assertNotIn('PYTHONPATH',kwargs['env'])
                self.assertNotEqual(kwargs['cwd'].name,'source')
            if name=='focused-checks' or name.startswith('native-'):
                self.assertEqual(kwargs['cwd'].name,'source')
                self.assertEqual(kwargs['env']['PYTHONPATH'],str(kwargs['cwd']))
        again=self.controlled_run()
        self.assertNotEqual(result['run_directory'],again['run_directory'])
        self.assertTrue(Path(result['zip_path']).is_file())

    def test_observed_transformed_input_exports_root_diagnosis(self):
        self.payload.unlink()
        (self.inputs/'SOURCE_COMMIT.txt').write_text(BASELINE_COMMIT)
        fixtures=self.inputs/'tests/fixtures';fixtures.mkdir(parents=True)
        (fixtures/'capacity_report.json').write_text('{"synthetic":true}')
        (fixtures/'scripted_lifecycle_run').mkdir()
        result=self.controlled_run()
        self.assertIn('payload_missing',result['summary']['root_blocker'])
        self.assertEqual(result['report']['stages']['environment']['status'],'blocked')
        self.assertEqual(self.command_calls,[])
        self.assert_export(result)
        with zipfile.ZipFile(result['zip_path']) as archive:
            sources=json.loads(archive.read('source-input-diagnosis.json'))['transformed_sources']
            self.assertEqual(sources[0]['paths']['capacity_report.json']['kind'],'file')

    def test_ambiguous_and_corrupt_payload_stop_before_environment(self):
        second=self.inputs/'second';second.mkdir();shutil.copyfile(self.payload,second/self.payload.name)
        result=self.controlled_run();self.assertIn('payload_ambiguous',result['summary']['root_blocker'])
        self.assert_export(result);self.assertEqual(self.command_calls,[])
        (second/self.payload.name).unlink()
        self.payload.write_bytes(b'corrupt')
        result=self.controlled_run();self.assertIn('payload_size_mismatch',result['summary']['root_blocker'])
        self.assert_export(result);self.assertEqual(self.command_calls,[])
        original=bytearray(zip_bytes(self.members));original[-1]^=1
        self.payload.write_bytes(original)
        result=self.controlled_run();self.assertIn('payload_hash_mismatch',result['summary']['root_blocker'])
        self.assert_export(result);self.assertEqual(self.command_calls,[])

    def test_complete_member_hash_rejects_same_marker_with_changed_fixture(self):
        changed=dict(self.members);changed['tests/fixtures/capacity_report.json.gz']=b'changed-compressed-member'
        self.payload.write_bytes(zip_bytes(changed))
        expected=dict(self.expected,archive_bytes=self.payload.stat().st_size,
                      archive_sha256=preflight.sha256_file(self.payload))
        expected['members']={n:dict(p) for n,p in expected['members'].items()}
        expected['members']['tests/fixtures/capacity_report.json.gz']['bytes']=len(changed['tests/fixtures/capacity_report.json.gz'])
        expected['expanded_bytes']=sum(p['bytes'] for p in expected['members'].values())
        with self.assertRaisesRegex(ValueError,'archive_member_hash'):
            preflight.admit_source(self.payload,self.root/'not-copied',expected)
        self.assertFalse((self.root/'not-copied').exists())

    def test_archive_safety_rejects_raw_headers_before_copy(self):
        for name in ['../out','/out','C:/out','a\\out','a//out','a/./out','a\0out']:
            with self.subTest(name=name):
                data=io.BytesIO()
                with zipfile.ZipFile(data,'w') as archive:
                    info=zipfile.ZipInfo('member');info.filename=name;archive.writestr(info,b'x')
                with zipfile.ZipFile(io.BytesIO(data.getvalue())) as archive:
                    with self.assertRaisesRegex(ValueError,'unsafe_archive_member'):
                        preflight.safe_members(archive,{})
        for members in [[('a',b'x'),('a/b',b'x')],[('a/b',b'x'),('a',b'x')],[('a',b'x'),('a',b'x')]]:
            data=io.BytesIO()
            with warnings.catch_warnings(record=True),zipfile.ZipFile(data,'w') as archive:
                for name,content in members:archive.writestr(name,content)
            with zipfile.ZipFile(io.BytesIO(data.getvalue())) as archive:
                with self.assertRaises(ValueError):preflight.safe_members(archive,{})

    def test_candidate_failures_and_bad_machine_output_export(self):
        for fault in ['create-venv','download-pip-wheel','empty-pip-receipt','corrupt-pip-wheel',
                      'bootstrap-pip','download-candidate','install-candidate','build-source','pip-check',
                      'malformed-probe','empty-probe','missing-probe','focused-checks','skipped-checks','native-9b']:
            with self.subTest(fault=fault):
                self.fault=fault
                self.command_calls.clear()
                result=self.controlled_run()
                self.assertFalse(result['summary']['preparation_checks_passed'])
                self.assertIsNotNone(result['summary']['root_blocker']);self.assert_export(result)
                self.assertEqual(result['report']['stages']['filesystem_backup']['status'],'passed')
                if fault in {'download-pip-wheel','empty-pip-receipt','corrupt-pip-wheel'}:
                    # This failure must stop before any bootstrap or bulk download.
                    self.assertFalse(any(n in {'bootstrap-pip','download-candidate'}
                                         for n,_,_ in self.command_calls))
                    with zipfile.ZipFile(result['zip_path']) as archive:
                        self.assertNotIn('pip-bootstrap-wheel.json',archive.namelist())

    def test_same_session_continuation_uses_existing_environment_and_keeps_failed_export(self):
        self.fault='malformed-probe'
        prior=self.controlled_run()
        original_hash=preflight.sha256_file(Path(prior['zip_path']))
        self.assertEqual(prior['summary']['tests_passed'],0)
        scratch=Path(prior['report']['scratch_directory'])
        interpreter=scratch/'venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
        interpreter.parent.mkdir(exist_ok=True);interpreter.touch()
        self.fault=None;self.command_calls.clear()
        with patch.object(preflight.platform,'system',return_value='Linux'), \
             patch.object(preflight.sys,'version_info',(3,13,15,'final',0)), \
             patch.object(preflight,'command',side_effect=self.controlled_command):
            result=continue_preflight(preflight.__dict__,prior,self.expected)
        self.assertTrue(result['summary']['continuation_checks_passed'])
        self.assertEqual(result['summary']['tests_passed'],97)
        self.assertEqual(result['summary']['model_generations'],0)
        self.assertEqual(preflight.sha256_file(Path(prior['zip_path'])),original_hash)
        self.assertFalse(any(n.startswith(('download-','install-','create-venv')) for n,_,_ in self.command_calls))
        self.assert_export(result)
        self.command_calls.clear()
        (scratch/'source/tests/fixtures/capacity_report.json.gz').write_bytes(b'changed')
        result=continue_preflight(preflight.__dict__,prior,self.expected)
        self.assertFalse(result['summary']['continuation_checks_passed'])
        self.assertEqual(result['report']['stages']['source_recheck']['status'],'failed')
        self.assertEqual(result['summary']['tests_passed'],0)
        self.assertEqual(self.command_calls,[]);self.assert_export(result)

    def test_generated_probe_writes_machine_file_in_real_noisy_subprocess(self):
        # Control unavailable external imports; exercise the complete producer and
        # actual subprocess/file/stdout transport rather than fabricating its file.
        prefix=self.root/'fake-venv';package=prefix/'recovery';package.mkdir(parents=True)
        (package/'__init__.py').write_bytes(self.members['recovery/__init__.py'])
        self.output.mkdir()
        machine=self.output/'installed-probe-result.json'
        program=preflight.installed_probe_script(self.expected,preflight.PINNED,machine)
        setup='\n'.join([
            'import importlib.metadata,sys,types',
            f'sys.prefix={str(prefix)!r}',
            f'wanted={preflight.PINNED!r}',
            'importlib.metadata.version=lambda name:wanted[name]',
            "for name in ['recovery','recovery.inference','recovery.runner','langgraph','langgraph.checkpoint','langgraph.checkpoint.sqlite','transformers','torch']:",
            "    module=types.ModuleType(name);module.__path__=[];sys.modules[name]=module",
            f"sys.modules['recovery'].__file__={str(package/'__init__.py')!r}",
            "sys.modules['langgraph.checkpoint.sqlite'].SqliteSaver=object",
            "sys.modules['transformers'].Qwen3_5ForCausalLM=type('Qwen3_5ForCausalLM',(),{})",
            "sys.modules['torch'].__version__='2.11.0+cu128'",
            "sys.modules['torch'].version=types.SimpleNamespace(cuda='12.8')",
            "print('[ERROR] controlled third-party documentation diagnostic')",''])
        record=preflight.command(self.output,'probe-output',[sys.executable,'-I','-c',setup+program],
            deadline=time.monotonic()+180,timeout=30,cwd=self.root,env=preflight.candidate_environment(self.root))
        result=preflight.installed_provenance(machine,self.expected,preflight.PINNED)
        self.assertEqual(result['versions'],preflight.PINNED)
        self.assertEqual(result['model_generations'],0)
        self.assertIn('[ERROR]',(self.output/record['stdout']).read_text())
        with self.assertRaises(json.JSONDecodeError):preflight.json_stdout(self.output,record)

    def test_pinned_pip_download_verifies_bytes_before_publish(self):
        metadata=self.expected['build_tools']['pip']['wheels'][0]
        content=self.wheel_bytes[metadata['filename']]
        destination=self.root/metadata['filename']
        response=io.BytesIO(content);response.geturl=lambda:metadata['url']
        stdout=io.StringIO()
        with patch('urllib.request.urlopen',return_value=response) as fetch, redirect_stdout(stdout):
            exec(preflight.pip_wheel_download_script(metadata,destination),{})
        fetch.assert_called_once_with(metadata['url'],timeout=30)
        self.assertEqual(destination.read_bytes(),content)
        self.assertEqual(json.loads(stdout.getvalue()),dict(metadata,verified=True))
        self.assertFalse(destination.with_suffix('.whl.partial').exists())

    def test_pinned_pip_download_refuses_bad_bytes_and_origins(self):
        metadata=self.expected['build_tools']['pip']['wheels'][0]
        content=self.wheel_bytes[metadata['filename']]
        cases=[('short',content[:-1],metadata,metadata['url'],'pip_bootstrap_size'),
               ('long',content+b'x',metadata,metadata['url'],'pip_bootstrap_size'),
               ('hash',b'x'*len(content),metadata,metadata['url'],'pip_bootstrap_hash'),
               ('redirect',content,metadata,'https://unreviewed.invalid/pip.whl','pip_bootstrap_origin'),
               ('origin',content,dict(metadata,url='http://files.pythonhosted.org/pip.whl'),
                metadata['url'],'pip_bootstrap_origin')]
        for name,data,wanted,final_url,error in cases:
            with self.subTest(name=name):
                directory=self.root/name;directory.mkdir()
                destination=directory/metadata['filename']
                response=io.BytesIO(data);response.geturl=lambda:final_url
                with patch('urllib.request.urlopen',return_value=response) as fetch:
                    with self.assertRaisesRegex(ValueError,error):
                        exec(preflight.pip_wheel_download_script(wanted,destination),{})
                self.assertFalse(destination.exists())
                if name=='origin': fetch.assert_not_called()

    def test_deadline_and_interruption_preserve_readable_evidence(self):
        result=preflight.run_preflight(self.inputs,self.output,self.scratch,self.expected,self.lock,workflow_seconds=0)
        self.assertEqual(result['summary']['root_blocker'],'cpu_deadline_before_stage');self.assert_export(result)
        with patch.object(preflight,'inventory',side_effect=KeyboardInterrupt):
            result=preflight.run_preflight(self.inputs,self.output,self.scratch,self.expected,self.lock)
        self.assertEqual(result['summary']['root_blocker'],'user_interruption')
        self.assertEqual(result['report']['stages']['input_inventory']['status'],'failed');self.assert_export(result)

    def test_shared_pool_and_storage_failure_prevent_download(self):
        self.scratch.mkdir();self.output.mkdir()
        facts=preflight.filesystem_facts({'scratch':self.scratch,'output':self.output})
        self.assertEqual(len(facts['pools']),1)
        with patch.object(preflight.shutil,'disk_usage',return_value=shutil._ntuple_diskusage(100,99,1)):
            result=self.controlled_run()
        self.assertIn('output_evidence_reserve',result['summary']['root_blocker'])
        self.assertFalse(any(n=='download-candidate' for n,_,_ in self.command_calls));self.assert_export(result)

    def test_shared_pool_admission_uses_the_smallest_observed_capacity(self):
        self.scratch.mkdir();self.output.mkdir()
        def usage(path):
            free=4*2**30 if Path(path)==self.scratch else 512*2**20
            return shutil._ntuple_diskusage(8*2**30,8*2**30-free,free)
        with patch.object(preflight.shutil,'disk_usage',side_effect=usage):
            with self.assertRaisesRegex(ValueError,'scratch_capacity'):
                preflight.require_space(self.scratch,self.output,2**30)

    def test_inventory_limit_symlinks_and_gpu_refusal(self):
        listing=preflight.inventory(self.inputs,limit=0)
        self.assertTrue(listing['truncated'])
        linked=self.inputs/'link'
        linked.symlink_to(self.payload)
        self.assertEqual(next(p for p in preflight.inventory(self.inputs)['entries'] if p['path']=='link')['kind'],'symlink')
        original_is_dir=Path.is_dir
        original_iterdir=Path.iterdir
        with patch.object(Path,'is_dir',lambda p:True if p.as_posix()=='/proc/driver/nvidia/gpus' else original_is_dir(p)), \
             patch.object(Path,'iterdir',lambda p:iter([Path('fake-gpu')]) if p.as_posix()=='/proc/driver/nvidia/gpus' else original_iterdir(p)):
            # Stop before environment; no CUDA initialization or installer is called.
            result=preflight.run_preflight(self.inputs,self.output,self.scratch,self.expected,self.lock)
        self.assertIn('cpu_stage_gpu_visible',result['summary']['root_blocker']);self.assert_export(result)

    def test_backup_and_export_failures_are_named(self):
        with patch.object(preflight,'sqlite_diagnostic',side_effect=ValueError('controlled SQLite failure')):
            result=self.controlled_run()
        self.assertIn('controlled SQLite failure',result['summary']['root_blocker']);self.assert_export(result)
        with patch.object(preflight,'export_evidence',side_effect=OSError('controlled unwritable ZIP')):
            result=self.controlled_run()
        self.assertIsNone(result['zip_path']);self.assertIn('controlled unwritable ZIP',result['report']['export_error'])
        self.assertTrue((Path(result['run_directory'])/'summary.json').is_file())

    def test_linux_group_inspection_distinguishes_live_members_from_exited_zombies(self):
        proc=self.root/'proc';proc.mkdir()
        own=proc/'123';own.mkdir()
        other=proc/'456';other.mkdir()
        (other/'stat').write_text('456 (other task) S 1 456 456 0')
        with patch.object(preflight.os,'killpg',return_value=None,create=True):
            (own/'stat').write_text('123 (owned task) Z 1 123 123 0')
            self.assertFalse(preflight._group_exists(123,proc))
            (own/'stat').write_text('123 (owned task) S 1 123 123 0')
            self.assertTrue(preflight._group_exists(123,proc))
            (own/'stat').write_text('malformed')
            self.assertTrue(preflight._group_exists(123,proc))


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory();self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name).resolve()

    def command(self,name,script,timeout=3,deadline=None):
        return preflight.command(self.root,name,[sys.executable,'-c',script],deadline=deadline or time.monotonic()+120,
                                 timeout=timeout,cwd=self.root,env=os.environ.copy())

    def test_real_stdout_stderr_exit_and_deadline(self):
        record=self.command('streams',"import sys;print('{\"value\":7}');print('warning',file=sys.stderr)")
        self.assertEqual(preflight.json_stdout(self.root,record),{'value':7})
        self.assertEqual((self.root/record['stderr']).read_text().strip(),'warning')
        with self.assertRaisesRegex(RuntimeError,'command_failed'):self.command('bad-exit','raise SystemExit(2)')
        with self.assertRaisesRegex(TimeoutError,'deadline_before_command'):
            self.command('no-start','raise RuntimeError()',deadline=time.monotonic()+1)
        self.assertFalse((self.root/'logs/no-start.stdout.txt').exists())

    def test_real_timeout_reaps_owned_child_tree_and_keeps_partial_logs(self):
        ticker=self.root/'ticks'
        grandchild="import pathlib,time;p=pathlib.Path("+repr(str(ticker))+");[(p.write_text(str(n)),time.sleep(.05)) for n in range(1000)]"
        child="import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',"+repr(grandchild)+"]);time.sleep(30)"
        parent="import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',"+repr(child)+"]);print('started',flush=True);time.sleep(30)"
        with self.assertRaises(subprocess.TimeoutExpired):self.command('timeout',parent,timeout=1)
        record=json.loads((self.root/'logs/timeout.json').read_text())
        self.assertTrue(record['leader_exited'])
        self.assertEqual(record['tree_confirmation'],'taskkill' if os.name=='nt' else 'exited')
        self.assertIn('started',(self.root/'logs/timeout.stdout.txt').read_text())
        before=ticker.read_text();time.sleep(.2);self.assertEqual(ticker.read_text(),before)

    def test_real_interruption_and_machine_schema_failure(self):
        original_wait=subprocess.Popen.wait
        interrupted=False
        def interrupt_once(process,*args,**kwargs):
            nonlocal interrupted
            if not interrupted and process.args[-1]=='import time;time.sleep(30)':
                interrupted=True
                raise KeyboardInterrupt
            return original_wait(process,*args,**kwargs)
        with patch.object(preflight.subprocess.Popen,'wait',interrupt_once):
            # Only interruption delivery is controlled; the child and cleanup are real.
            with self.assertRaises(KeyboardInterrupt):self.command('interrupt','import time;time.sleep(30)')
        record=json.loads((self.root/'logs/interrupt.json').read_text());self.assertTrue(record['leader_exited'])
        record=self.command('malformed',"print('not JSON')")
        with self.assertRaises(json.JSONDecodeError):preflight.json_stdout(self.root,record)

    def test_real_preinstallation_process_diagnostic(self):
        result=preflight.process_tree_diagnostic(self.root,self.root,time.monotonic()+120,os.environ.copy())
        self.assertTrue(result['expected_timeout']);self.assertTrue(result['grandchild_stopped'])


if __name__=='__main__':
    unittest.main()
