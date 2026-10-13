"""Actual online setup controller with tiny pinned assets and CPU command doubles."""

from contextlib import ExitStack, closing
import hashlib
import io
import json
from pathlib import Path
import shutil
import sqlite3
import os
import sys
import tempfile
import time
import traceback
import unittest
from unittest.mock import patch
import zipfile

from scripts import m5_course_smoke_assets as assets
from scripts import m5_kaggle_preflight as preflight
from scripts.course_kaggle_bootstrap import online, check_resume
from tests.test_course_smoke_assets import CourseSmokeAssetTests, item

GIB = 2**30


class OnlineSetupRepairTests(unittest.TestCase):
    def fixture(self, directory):
        root,manifest,_,_,_,_,_ = CourseSmokeAssetTests.fixture(self,directory)
        scratch = Path(directory)/'workspace/gpu-environment/scratch'
        output = scratch.parent/'bootstrap'
        blobs = {'first.safetensors':b'first CPU fixture','second.safetensors':b'second CPU fixture'}
        expected = {n:item(v) for n,v in blobs.items()}
        inspection = dict(model='Qwen/Qwen3.5-4B',revision='4'*40,
            checkpoint_index=dict(shard_files=list(blobs),total_checkpoint_bytes=sum(map(len,blobs.values()))))
        location = assets.inspection_path(root)
        location.parent.mkdir(parents=True)
        location.write_text(json.dumps(inspection))
        raw = io.BytesIO()
        with zipfile.ZipFile(raw,'w') as z:
            z.writestr('tiny.txt','CPU wheel fixture')
        wheel_bytes = raw.getvalue()

        def wheel(name,version):
            return dict(name=name,version=version,filename=f'{name}-{version}.whl',
                        url=f'https://files.pythonhosted.org/{name}.whl',**item(wheel_bytes))

        runtime = wheel('setuptools','81.0.0')
        tools = {n:dict(version=v,wheels=[wheel(n,v)])
                 for n,v in (('pip','26.2.1'),('setuptools','84.0.0'),('wheel','0.48.0'))}
        manifest.update(candidate_wheels=[runtime],build_tools=tools)
        launch = dict(stage_weights=True,authorization='tiny CPU setup fixture',resource_policy='observe',
                      allocated_at=None,budget=dict(shutdown_seconds=120,prior_smoke_attempts=23))
        state = dict(commands=[],download_fails=False,bad_reuse=False,free=100*GIB)

        def command(evidence,name,args,**kwargs):
            state['commands'].append(name)
            install = Path(args[-1]) if name=='create-candidate' else None
            if install:
                (install/'bin').mkdir(parents=True)
                (install/'bin/python').write_bytes(b'CPU interpreter placeholder; never executed')
            if name.startswith('download-'):
                owned_scratch = Path(kwargs['cwd'])
                for w in [runtime]+[v['wheels'][0] for v in tools.values()]:
                    (owned_scratch/'wheels'/w['filename']).write_bytes(wheel_bytes)
            if name=='build-project':
                (Path(kwargs['cwd'])/'built/fixture.whl').write_bytes(wheel_bytes)
            if name in ('installed-provenance','reused-installed-provenance'):
                versions = {'setuptools':'wrong' if name.startswith('reused-') and state['bad_reuse'] else '81.0.0'}
                (evidence/'installed.json').write_text(json.dumps(dict(versions=versions,
                    verified_module_hashes={},qwen_text_class='Qwen3_5ForCausalLM',
                    torch_cuda_build='12.8',model_generations=0)))
            if name=='hardware-plan-contract':
                current=json.loads(Path(args[args.index('--launch')+1]).read_bytes())
                self.assertEqual(current['resource_policy'],'observe')
                self.assertEqual(current['authorization'],'tiny CPU setup fixture')
            if name=='stage-pinned-checkpoint':
                if state['download_fails']:
                    raise TimeoutError('transient fixture network interruption; no inference')
                cache = Path(args[args.index('--cache')+1])
                snapshot = cache/'models--Qwen--Qwen3.5-4B/snapshots'/inspection['revision']
                snapshot.mkdir(parents=True,exist_ok=True)
                for n,v in blobs.items():
                    (snapshot/n).write_bytes(v)
                (evidence/'weights.json').write_text(json.dumps(dict(checkpoint_files=expected,
                    model=inspection['model'],revision=inspection['revision'],gpu_execution=False)))
            return dict(status='passed',gpu_calls=0,fixture=True)

        return root,manifest,launch,scratch,output,expected,inspection,state,command

    def run_setup(self, fixture, *, output=None, extra=None):
        root,manifest,launch,scratch,original,expected,_,state,command = fixture
        with ExitStack() as stack:
            stack.enter_context(patch.object(assets,'native_checkpoint_files',return_value=expected))
            stack.enter_context(patch.object(assets,'command',side_effect=command))
            stack.enter_context(patch.object(assets,'assigned_device_count',return_value=0))
            stack.enter_context(patch.object(assets.platform,'system',return_value='Linux'))
            stack.enter_context(patch.object(assets.platform,'machine',return_value='x86_64'))
            stack.enter_context(patch.object(assets.sys,'version_info',(3,13)))
            stack.enter_context(patch.object(preflight.shutil,'disk_usage',side_effect=lambda p:
                shutil._ntuple_diskusage(200*GIB,200*GIB-state['free'],state['free'])))
            if extra:
                extra(stack)
            return assets.prepare(root,manifest,launch,scratch,output or original,online_config=Path('CPU-fixture.json'))

    def test_success_uses_real_online_path_and_actual_cache_admission(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            cache = Path(d)/'external-cache'
            f[2]['hf_cache'] = str(cache)
            result = self.run_setup(f)
            self.assertEqual(result['status'],'prepared',result)
            facts = json.loads((f[4]/'storage-checkpoint.json').read_bytes())
            self.assertEqual(facts['locations']['scratch']['path'],str(cache))
            self.assertTrue(facts['admitted'])
            self.assertTrue(result['installed_verified'])
            self.assertFalse(result['gpu_execution'])
            self.assertFalse(result['model_weights_loaded'])

    def test_early_capacity_failure_exports_facts_without_installing(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            f[5]['first.safetensors']['bytes'] = 20*GIB
            f[7]['free'] = 10*GIB
            result = self.run_setup(f)
            self.assertEqual(result['status'],'blocked')
            self.assertEqual(f[7]['commands'],[])
            facts = json.loads((f[4]/'storage-location.json').read_bytes())
            self.assertEqual(facts['available_bytes'],10*GIB)
            self.assertFalse(facts['admitted'])
            self.assertIn('available=',result['root_blocker'])
            self.assertTrue((f[4]/'preflight-results.zip').exists())

    def test_undersized_preferred_cache_moves_without_reinstalling(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            preferred=Path(d)/'preferred-cache'
            f[2]['hf_cache']=str(preferred)
            f[7]['download_fails']=True
            self.assertTrue(self.run_setup(f)['installed_verified'])
            f[2]['setup_resume_report']=str(f[4]/'report.json')
            f[7]['download_fails']=False
            def extra(stack):
                stack.enter_context(patch.object(preflight.shutil,'disk_usage',side_effect=lambda p:
                    shutil._ntuple_diskusage(200*GIB,0,512*2**20 if Path(p)==preferred else 100*GIB)))
            output=f[4].with_name('bootstrap-new-cache')
            second=self.run_setup(f,output=output,extra=extra)
            self.assertEqual(second['status'],'prepared',second)
            self.assertEqual(second['hf_cache'],str(f[3]/'hub'))
            self.assertEqual(f[7]['commands'].count('install-candidate'),1)
            self.assertTrue(second['reused_installation'])
            self.assertTrue(preferred.exists())

    def test_rejected_temporary_location_automatically_tries_next(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            first,second = Path(d)/'temp-full',Path(d)/'temp-fit'
            def extra(stack):
                stack.enter_context(patch.object(assets,'storage_locations',return_value=[first,second,f[3]]))
                stack.enter_context(patch.object(preflight.shutil,'disk_usage',side_effect=lambda p:
                    shutil._ntuple_diskusage(200*GIB,0,512*2**20 if Path(p)==first else 100*GIB)))
            result = self.run_setup(f,extra=extra)
            self.assertEqual(result['status'],'prepared',result)
            self.assertEqual(result['scratch'],str(second))
            decision = json.loads((f[4]/'storage-selection.json').read_bytes())
            self.assertEqual([r['status'] for r in decision['attempts']],['refused','selected'])

    def test_download_interruption_reuses_verified_installation(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            f[7]['download_fails'] = True
            first = self.run_setup(f)
            old_report = (f[4]/'report.json').read_bytes()
            self.assertTrue(first['installed_verified'])
            self.assertEqual(first['stage'],'stage-pinned-checkpoint')
            f[2]['setup_resume_report'] = str(f[4]/'report.json')
            f[7]['download_fails'] = False
            second = self.run_setup(f,output=f[4].with_name('bootstrap-retry'))
            self.assertEqual(second['status'],'prepared',second)
            self.assertTrue(second['reused_installation'])
            self.assertEqual(f[7]['commands'].count('install-candidate'),1)
            self.assertEqual(f[7]['commands'].count('download-candidate'),1)
            self.assertIn('reused-installed-provenance',f[7]['commands'])
            self.assertEqual((f[4]/'report.json').read_bytes(),old_report)

    def test_missing_temporary_installation_is_rebuilt_without_duplicate_directories(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            self.assertEqual(self.run_setup(f)['status'],'prepared')
            f[2]['setup_resume_report'] = str(f[4]/'report.json')
            assets.reclaim_installation(f[3],f[1]['source_baseline_commit'])
            second = self.run_setup(f,output=f[4].with_name('bootstrap-new-session'))
            self.assertEqual(second['status'],'prepared',second)
            self.assertFalse(second['reused_installation'])
            self.assertEqual(f[7]['commands'].count('install-candidate'),2)

    def test_damaged_installation_rebuild_preserves_old_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            self.run_setup(f)
            old = (f[4]/'installed.json').read_bytes()
            f[2]['setup_resume_report'] = str(f[4]/'report.json')
            f[7]['bad_reuse'] = True
            output = f[4].with_name('bootstrap-damaged')
            repaired = self.run_setup(f,output=output)
            self.assertEqual(repaired['status'],'prepared',repaired)
            self.assertFalse(repaired['reused_installation'])
            self.assertTrue((output/'installation-reuse-refused.json').is_file())
            self.assertEqual((f[4]/'installed.json').read_bytes(),old)

    def test_changed_source_resume_is_refused_before_subprocess(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            report = Path(d)/'other-source.json'
            report.write_text(json.dumps(dict(source_commit='foreign',installed_verified=True)))
            f[2]['setup_resume_report'] = str(report)
            result = self.run_setup(f)
            self.assertIn('setup resume source differs',result['root_blocker'])
            self.assertEqual(f[7]['commands'],[])

    def test_cache_credit_ignores_duplicate_partial_and_requires_native_hash(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            cache = Path(d)/'cache'
            inspection,expected = f[6],f[5]
            snapshot = cache/'models--Qwen--Qwen3.5-4B/snapshots'/inspection['revision']
            snapshot.mkdir(parents=True)
            name = 'first.safetensors'
            (snapshot/name).write_bytes(b'first CPU fixture')
            (snapshot/(name+'.partial')).write_bytes(b'obsolete prefix')
            (snapshot/'second.safetensors.partial').write_bytes(b'second')
            result = assets.checkpoint_pending(cache,inspection,expected,f[1])
            self.assertEqual(result['remaining_bytes'],expected['second.safetensors']['bytes']-6)
            (snapshot/name).write_bytes(b'corrupt')
            with self.assertRaisesRegex(ValueError,'native cached asset identity'):
                assets.checkpoint_pending(cache,inspection,expected,f[1])

    def test_oversized_partial_is_refused_before_downloading(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            cache = Path(d)/'cache'
            snapshot = cache/'models--Qwen--Qwen3.5-4B/snapshots'/f[6]['revision']
            snapshot.mkdir(parents=True)
            (snapshot/'first.safetensors.partial').write_bytes(b'x'*100)
            with self.assertRaisesRegex(ValueError,'partial asset is larger'):
                assets.checkpoint_pending(cache,f[6],f[5],f[1])

    def test_bootstrap_selects_existing_fallback_before_weights_and_keeps_base_history(self):
        with tempfile.TemporaryDirectory() as d:
            f = self.fixture(d)
            root,manifest = f[:2]
            (root/'source-manifest.json').write_text(json.dumps(manifest))
            bundle = Path(d)/'bundle'
            (bundle/'candidates/9B').mkdir(parents=True)
            (bundle/'candidates/9B/automatic-run.json').write_text(json.dumps(dict(reason='recorded_model_attempt_failure')))
            config = dict(candidate='9B',candidate_order=['9B','4B'],budget=dict(prior_smoke_attempts=23,prior_evidence='CPU fixture retained predecessor'),
                          resource_policy='observe',smoke_attempt_limit=71,smoke_attempt_allowance='final-online-4/qualification',
                          assets_receipt=str(Path(d)/'lost-temporary-assets.json'),
                          authorizations=dict(weights='CPU fixture',hardware='CPU fixture'))
            (bundle/'asset-receipt.json').write_text(json.dumps(dict(model='Qwen/Qwen3.5-9B',source_commit=manifest['source_baseline_commit'])))
            path = bundle/'operator-config.json'; path.write_text(json.dumps(config))
            result = dict(status='prepared',interpreter='CPU-fixture',assets_receipt='CPU-fixture',hf_cache='CPU-fixture',
                          source_commit=manifest['source_baseline_commit'],scratch='CPU-fixture',installed_verified=True)
            with patch('scripts.course_kaggle_bootstrap.validate_smoke_predecessor'),patch.object(assets,'prepare',return_value=result) as prepare:
                online(root,path,Path(d)/'scratch',Path(d)/'output')
            self.assertEqual(prepare.call_args.args[2]['candidate'],'4B')
            self.assertEqual(prepare.call_args.args[2]['retired_assets']['model'],'Qwen/Qwen3.5-9B')
            self.assertEqual(json.loads(path.read_bytes())['budget']['prior_smoke_attempts'],23)

    def test_observational_resume_uses_selected_child_and_never_manual_budget_admission(self):
        for label in ('9B','4B'):
            with self.subTest(candidate=label),tempfile.TemporaryDirectory() as d:
                bundle = Path(d)/'bundle'
                child = bundle/'candidates'/label; child.mkdir(parents=True)
                (child/'run.json').write_text(json.dumps(dict(freeze=dict(accepted=True))))
                if label=='4B':
                    first = bundle/'candidates/9B'; first.mkdir()
                    (first/'automatic-run.json').write_text(json.dumps(dict(reason='recorded_model_attempt_failure')))
                config = dict(candidate_order=['9B','4B'],resource_policy='observe')
                path=bundle/'operator-config.json'; path.write_text(json.dumps(config))
                output=Path(d)/'receipts'; output.mkdir()
                with patch('scripts.course_kaggle_workflow.recover_bootstrap_refusals'), \
                     patch('scripts.course_kaggle_workflow.end_observations') as observe, \
                     patch('scripts.course_kaggle_workflow.session_window',return_value=600), \
                     patch('scripts.course_kaggle_workflow.snapshot',side_effect=AssertionError('no legacy budget calculation')):
                    check_resume(Path(d)/'source',path,output)
                self.assertEqual(observe.call_args.args[0].resolve(),child.resolve())
                receipt=json.loads((output/'admission.json').read_bytes())
                self.assertEqual(receipt['stage'],'main')
                self.assertEqual(receipt['provider_wall_seconds'],600)
                self.assertFalse((bundle/'run.json').exists())


class FallbackCacheSafetyTests(unittest.TestCase):
    def fixture(self,d):
        cache,output = Path(d)/'scratch/hub',Path(d)/'receipts'
        output.mkdir(); cache.mkdir(parents=True)
        commit = 'a'*40
        (cache.parent/'SOURCE_COMMIT.txt').write_text(commit+'\n')
        retired = dict(model='Qwen/Qwen3.5-9B',revision='9'*40,source_commit=commit,
                       checkpoint_files={'old.safetensors':item(b'tiny retired CPU blob')})
        snapshot = cache/'models--Qwen--Qwen3.5-9B/snapshots'/retired['revision']
        snapshot.mkdir(parents=True); (snapshot/'old.safetensors').write_bytes(b'tiny retired CPU blob')
        inspection = dict(model='Qwen/Qwen3.5-4B',revision='4'*40)
        expected = {'new.safetensors':item(b'tiny new CPU blob')}
        manifest = dict(source_baseline_commit=commit,members={})
        return cache,output,retired,snapshot,inspection,expected,manifest

    def test_low_space_reclaims_only_retired_snapshot_and_keeps_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            cache,output,old,snapshot,inspection,expected,manifest = self.fixture(d)
            retained = cache.parent/'scientific-evidence.json'; retained.write_text('keep')
            with patch.object(preflight.shutil,'disk_usage',side_effect=lambda p:
                    shutil._ntuple_diskusage(10*GIB,0,512*2**20 if snapshot.exists() else 4*GIB)):
                facts = assets.admit_checkpoint(cache,output,inspection,expected,manifest,retired_assets=old)
            self.assertTrue(facts['admitted'])
            self.assertFalse(snapshot.exists())
            self.assertEqual(retained.read_text(),'keep')
            self.assertTrue((output/'checkpoint-cache-reclaimed.json').exists())

    def test_live_process_or_unowned_file_prevents_cache_reclamation(self):
        for live in (True,False):
            with self.subTest(live_process=live),tempfile.TemporaryDirectory() as d:
                cache,output,old,snapshot,inspection,expected,manifest = self.fixture(d)
                workers=[]
                if live:
                    path=Path(d)/'worker.sqlite'
                    with closing(sqlite3.connect(path)) as db:
                        db.execute('CREATE TABLE provider_processes(stopped_at TEXT,uncertain_stop INTEGER)')
                        db.execute('INSERT INTO provider_processes VALUES(NULL,0)')
                        db.commit()
                    workers=[path]
                else:
                    (snapshot/'unowned.txt').write_text('retain')
                with patch.object(preflight.shutil,'disk_usage',return_value=shutil._ntuple_diskusage(10*GIB,0,512*2**20)), \
                     self.assertRaisesRegex(ValueError,'quiescent|unowned'):
                    assets.admit_checkpoint(cache,output,inspection,expected,manifest,retired_assets=old,retired_workers=workers)
                self.assertTrue(snapshot.exists())


class NotebookSetupFailureTests(unittest.TestCase):
    def test_literal_cells_keep_root_cause_latest_resume_and_exports_across_retries(self):
        from scripts.build_course_kaggle import notebook
        document = notebook('CPU-fixture','a'*40)
        execution = ''.join(next(c['source'] for c in document['cells'] if c['id']=='execute'))
        export = ''.join(next(c['source'] for c in document['cells'] if c['id']=='export'))
        with tempfile.TemporaryDirectory() as d:
            workspace = Path(d)/'workspace'; workspace.mkdir()
            bundle = workspace/'bundle'; bundle.mkdir()
            inputs = Path(d)/'inputs'; inputs.mkdir()
            source = bundle/'source'; source.mkdir()
            config_path = bundle/'operator-config.json'
            config = dict(candidate='9B',allocated_at='2026-10-13T17:15:21+00:00',max_work_seconds=36000)
            config_path.write_text(json.dumps(config))
            reason = 'scratch_capacity: path=/CPU/cache available=123 additional_required=20648488160'
            calls = []

            def failed_bootstrap(args,**kwargs):
                evidence = Path(args[args.index('--output')+1]); evidence.mkdir(parents=True)
                calls.append(dict(scratch=args[args.index('--scratch')+1],output=evidence,
                                  config=json.loads(config_path.read_bytes())))
                report = dict(status='blocked',reason=reason,root_blocker=reason,stage='checkpoint-capacity',
                              source_commit='a'*40,weights_staged=False,installed_verified=True,
                              interpreter=None,setup_report=str(evidence/'report.json'))
                (evidence/'report.json').write_text(json.dumps(report))
                (evidence/'bootstrap.json').write_text(json.dumps(report))
                class Process:
                    stdout=io.StringIO('CPU bootstrap failure fixture; no inference\n')
                    returncode=1
                    def poll(self): return 1
                    def wait(self,**kwargs): return 1
                return Process()

            values = dict(SOURCE_READY=True,ACTION='run_all',ENABLE_GPU=True,CONFIG=config,
                EXPECTED_SOURCE_COMMIT='a'*40,ASSETS_ZIP=None,workspace=workspace,bundle=bundle,
                inputs=inputs,source=source,config_path=config_path,attached=lambda *a:None,
                Path=Path,os=os,sys=sys,time=time,json=json,shutil=shutil,traceback=traceback,
                zipfile=zipfile,display=lambda *a:None,HTML=lambda s:s,FileLink=lambda s:s)
            with patch('subprocess.Popen',side_effect=failed_bootstrap):
                for _ in range(3):
                    exec(execution,values)
            self.assertEqual(len(calls),3)
            self.assertEqual(len({c['scratch'] for c in calls}),1)
            self.assertEqual(len({c['output'] for c in calls}),3)
            self.assertEqual(calls[2]['config']['setup_resume_report'],str(calls[1]['output']/'report.json'))
            self.assertEqual(len(list((bundle/'environment-receipts').glob('*/report.json'))),3)
            self.assertEqual(json.loads((bundle/'last-action.json').read_bytes())['reason'],reason)
            # Build output is disposable, not a second copy of canonical source.
            (source/'build/lib').mkdir(parents=True)
            (source/'build/lib/duplicate.py').write_text('do not export')
            (source/'research.py').write_text('keep canonical source')
            exec(export,values)
            with zipfile.ZipFile(workspace/'course-resume.payload') as z:
                self.assertIsNone(z.testzip())
                self.assertNotIn('source/build/lib/duplicate.py',z.namelist())
                self.assertIn('source/research.py',z.namelist())
            with zipfile.ZipFile(workspace/'course-results.zip') as z:
                self.assertIsNone(z.testzip())
                self.assertIn(reason,z.read('RESULT.html').decode())
                self.assertIn('Setup stopped before weights',z.read('RESULT.html').decode())
            # A later source refusal must not inherit old bootstrap or GPU locals.
            values.update(SOURCE_READY=False,receipt={'stale':'allocation receipt'},assigned=True)
            with patch('subprocess.Popen',side_effect=AssertionError('no child on source refusal')):
                exec(execution,values)
            final=json.loads((bundle/'last-action.json').read_bytes())
            self.assertIn('Source setup failed',final['reason'])
            exec(export,values)
            with zipfile.ZipFile(workspace/'course-results.zip') as z:
                self.assertIn('Source setup failed',z.read('RESULT.html').decode())

    def test_portable_backup_refusal_preserves_previous_export(self):
        from scripts.course_kaggle_workflow import backup_bundle
        with tempfile.TemporaryDirectory() as d:
            bundle = Path(d)/'bundle'; bundle.mkdir()
            (bundle/'canonical.json').write_text('keep')
            previous = Path(d)/'course-resume.payload'; previous.write_bytes(b'original complete export')
            with patch.object(preflight.shutil,'disk_usage',return_value=shutil._ntuple_diskusage(GIB,0,100)), \
                 self.assertRaisesRegex(ValueError,'output_evidence_reserve'):
                backup_bundle(bundle,previous)
            self.assertEqual(previous.read_bytes(),b'original complete export')
            self.assertEqual((bundle/'canonical.json').read_text(),'keep')


if __name__=='__main__':
    unittest.main()
