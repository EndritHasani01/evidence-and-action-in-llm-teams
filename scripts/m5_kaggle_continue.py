"""Finish run 4's remaining CPU checks in its unchanged, still-open session."""


def continue_preflight(namespace: dict, previous_result: dict, expected: dict) -> dict:
    import json
    import os
    from pathlib import Path
    import platform
    import shutil
    import sys
    import time
    import uuid

    n = namespace
    previous = Path(previous_result['run_directory']).resolve()
    output = previous.parent/('recovery-m5-continuation-'+uuid.uuid4().hex[:12])
    output.mkdir(exist_ok=False)
    started = time.monotonic()
    deadline = started+900
    stages = {name:{'status':'blocked','reason':'earlier check incomplete'} for name in
              ['source_recheck','installed_packages','focused_checks','native_9b','native_4b','native_capacity','filesystem_backup']}
    report = {'kind':'cpu-run4-continuation','started_utc':n['utc'](),'cpu_limit_seconds':900,
              'previous_directory':str(previous),'stages':stages,'root_blocker':None}
    result = {'run_directory':str(output),'zip_path':None,'zip_sha256':None,'report':report}
    current = 'source_recheck'
    cleanup_unconfirmed = False

    try:
        prior = json.loads((previous/'preflight-report.json').read_text())
        assert json.loads((previous/'expected-source-manifest.json').read_text())==expected
        assert all(prior['stages'][name]['status']=='passed' for name in
                   ['source','cpu_host','command_cleanup','environment'])
        assert prior['stages']['installed_packages']['status']=='failed'
        assert prior['root_blocker'].startswith('JSONDecodeError:')
        assert platform.system()=='Linux' and sys.version_info[:2]==(3,13)
        gpu_directory = Path('/proc/driver/nvidia/gpus')
        assert not gpu_directory.is_dir() or not list(gpu_directory.iterdir()), 'Select Accelerator None'
        scratch = Path(prior['scratch_directory'])
        source, candidate = scratch/'source', scratch/'venv'
        interpreter = candidate/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
        assert interpreter.is_file(), 'Original session environment is unavailable'
        assert 'include-system-site-packages = false' in (candidate/'pyvenv.cfg').read_text().lower()
        n['require_space'](scratch,output,n['BUILD_RESERVE'])
        for name,item in expected['members'].items():
            path = source/name
            assert path.is_file() and not path.is_symlink() and path.stat().st_size==item['bytes']
            assert n['sha256_file'](path)==item['sha256'], 'Changed source: '+name
        versions = prior['stages']['environment']['result']['versions']
        assert versions=={p['name']:p['version'] for p in expected['candidate_wheels']}
        shutil.copyfile(previous/'preflight-report.json',output/'prior-preflight-report.json')
        shutil.copyfile(previous/'expected-source-manifest.json',output/'expected-source-manifest.json')
        report['prior_report_sha256'] = n['sha256_file'](previous/'preflight-report.json')
        stages[current] = {'status':'passed','verified_members':len(expected['members'])}
        env = n['candidate_environment'](scratch)

        def invoke(name,args,bound,source_mode=False):
            nonlocal cleanup_unconfirmed
            if cleanup_unconfirmed:
                raise RuntimeError('prior_process_cleanup_unconfirmed')
            n['require_space'](scratch,output,n['BUILD_RESERVE'])
            process_env = dict(env)
            if source_mode: process_env['PYTHONPATH'] = str(source)
            print('Running '+name+' ...',flush=True)
            try:
                return n['command'](output,name,args,deadline=deadline,timeout=bound,
                                    cwd=source if source_mode else scratch,env=process_env)
            except BaseException:
                log = output/'logs'/(name+'.json')
                if log.is_file() and json.loads(log.read_text()).get('tree_confirmation')=='unconfirmed':
                    cleanup_unconfirmed = True
                raise

        current = 'installed_packages'
        invoke('pip-check',[interpreter,'-m','pip','--isolated','check'],30)
        probe = output/'installed-probe.py'
        machine = output/'installed-probe-result.json'
        probe.write_text(n['installed_probe_script'](expected,versions,machine),encoding='utf-8')
        shutil.copyfile(probe,output/'installed-probe-program.txt')
        invoke('installed-probe',[interpreter,'-I',probe],90)
        provenance = n['installed_provenance'](machine,expected,versions)
        n['save_json'](output/'installed-provenance.json',provenance)
        listed = invoke('pip-list',[interpreter,'-m','pip','--isolated','list','--format=json'],30)
        n['save_json'](output/'installed-packages.json',n['json_stdout'](output,listed))
        frozen = invoke('pip-freeze',[interpreter,'-m','pip','--isolated','freeze','--all'],30)
        shutil.copyfile(output/frozen['stdout'],output/'installed-freeze.txt')
        stages[current] = {'status':'passed','verified_packages':len(versions),'verified_modules':len(provenance['verified_module_hashes'])}
        n['save_json'](output/'continuation-report.json',report)

        checks = [('focused_checks',['-m','unittest',*n['FOCUSED'],'-q'],81,360),
                  ('native_9b',['-m','tests.tokenizer_inference','--tokenizer','metadata/9B'],4,60),
                  ('native_4b',['-m','tests.tokenizer_inference','--tokenizer','metadata/4B'],4,60),
                  ('native_capacity',['-m','tests.tokenizer_capacity','--tokenizer','metadata/9B'],8,90)]
        for current,args,count,bound in checks:
            record = invoke(current.replace('_','-'),[interpreter,*args],bound,source_mode=True)
            stages[current] = {'status':'passed','result':n['test_result'](output,record,count)}
            n['save_json'](output/'continuation-report.json',report)
            print(current+': passed',flush=True)
    except BaseException as exc:
        stages[current] = {'status':'failed','reason':f'{type(exc).__name__}: {exc}'}
        report['root_blocker'] = stages[current]['reason']
    finally:
        try:
            stages['filesystem_backup'] = {'status':'passed','result':n['sqlite_diagnostic'](output)}
        except Exception as exc:
            stages['filesystem_backup'] = {'status':'failed','reason':f'{type(exc).__name__}: {exc}'}
            report['root_blocker'] = report['root_blocker'] or stages['filesystem_backup']['reason']
        passed = sum(s.get('result',{}).get('tests',0) for s in stages.values() if s['status']=='passed')
        summary = {'continuation_checks_passed':all(s['status']=='passed' for s in stages.values()),
                   'tests_passed':passed,'root_blocker':report['root_blocker'],'model_generations':0,
                   'model_smoke_ready':False,'gpu_native_diagnostics':None,'model_smoke':None,
                   'provider_assignment_utc':None,'provider_release_utc':None,
                   'observed_cpu_wall_seconds':time.monotonic()-started}
        report.update(summary=summary,ended_utc=n['utc'](),process_cleanup_unconfirmed=cleanup_unconfirmed)
        result['summary'] = summary
        n['save_json'](output/'continuation-report.json',report)
        n['save_json'](output/'summary.json',summary)
        try: result.update(n['export_evidence'](output))
        except Exception as exc:
            report['export_error'] = f'{type(exc).__name__}: {exc}'
            n['save_json'](output/'continuation-report.json',report)
        print(json.dumps(summary,indent=2),flush=True)
        print('Result ZIP SHA-256:',result['zip_sha256'],flush=True)
    return result
