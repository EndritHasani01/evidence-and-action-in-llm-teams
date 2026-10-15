"""Lightweight package/notebook review; no host/GPU/model qualification."""

import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from recovery.i01.archive import atomic_json,digest
from recovery.i01.runtime import command as runtime_command


def verify_notebook(notebook):
    """Execute all ordinary cells with a recorder; never load a real model."""
    expected=dict(configuration=[],workspace=[],**{'session-window':['configure_session'],
        'setup':['install_runtime'],'open-study':['start_new'],'selfcheck':['check_implementation'],
        'weights':['download_weights'],'load':['load_models'],'plan':['plan_execution'],
        'readiness':['check_readiness'],'direct-screen':['qualify_direct'],
        'qualification':['inspect_qualification'],'envelope':['check_headroom']})
    for n in (1,2,3):
        expected[f'pilot-{n}']=['run_pilot'];expected[f'check-pilot-{n}']=['check_pilot']
    expected['admit-main']=['admit_main']
    for n in range(1,11):expected[f'main-{n:02d}']=['run_main_batch']
    expected.update(report=['build_report'],archive=['save_checkpoint'],close=['finish_session'])
    cells=[c for c in notebook['cells'] if c['cell_type']=='code']
    assert [c['id'] for c in cells]==list(expected)
    assert all(c['execution_count'] is None and not c['outputs'] for c in cells)
    meta=notebook['metadata']['i01']
    assert meta['run_all_supported'] and meta['run_all_scope']=='whole-study'
    assert meta['first_attempt_ceiling']==460 and meta['hard_attempt_limit']==500 and meta['contingency_limit']==28
    assert meta['execution_policy']=='i01-recovery-admission-run-all-2026-10-15'
    class Stub:
        def __init__(self):self.calls=[]
        def __getattr__(self,name):
            assert name in {n for names in expected.values() for n in names}
            def record(*args,**kwargs):
                self.calls.append(dict(method=name,args=list(args),kwargs=kwargs));return {}
            return record
    stub=Stub();namespace=dict(study=stub);receipts={}
    for cell in cells:
        source=''.join(cell['source']);tree=ast.parse(source)
        assert 'ui.' not in source
        assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in
                       ('panel','inspect_panel','generate','run_all','run','run_action','action',
                        'qualify_thinking','record_pilot_review','record_batch_review','freeze_configuration') for n in ast.walk(tree))
        assert not any(isinstance(n,(ast.For,ast.While)) for n in ast.walk(tree)) or cell['id']=='workspace'
        if cell['id']=='workspace':continue
        stub.calls=[];exec(compile(source,cell['id'],'exec'),namespace)
        assert [c['method'] for c in stub.calls]==expected[cell['id']],cell['id']
        receipts[cell['id']]=stub.calls
    assert receipts['session-window'][0]['kwargs']['remaining_minutes']==700
    assert receipts['session-window'][0]['kwargs']['basis']=='planning_estimate'
    assert 'not independently verified' in receipts['session-window'][0]['kwargs']['evidence']
    assert receipts['plan'][0]['kwargs']=={} and receipts['admit-main'][0]['kwargs']=={}
    for n in (1,2,3):
        assert receipts[f'pilot-{n}'][0]['args']==[n]
        assert receipts[f'check-pilot-{n}'][0]['args']==[n]
    for n in range(1,11):assert receipts[f'main-{n:02d}'][0]['args']==[n]
    assert receipts['archive'][0]['kwargs']==dict(verify=True)
    return dict(code_cells=len(cells),widget_panels=0,independent_cell_scopes=receipts,
                run_all_supported=True,run_all_scope='whole-study',first_attempt_ceiling=460,
                run_all_can_execute_inference=True,model_attempts=0)


def verify_research_notebook(notebook):
    return verify_notebook(notebook)


def verify(root,delivery):
    root,delivery=Path(root).resolve(),Path(delivery).resolve()
    notebook=json.loads((delivery/"i01_course_kaggle.ipynb").read_text(encoding="utf-8"))
    cells=[c for c in notebook["cells"] if c["cell_type"]=="code"]
    import nbformat
    nbformat.validate(nbformat.from_dict(notebook))
    notebook_receipt=verify_notebook(notebook)
    research=json.loads((delivery/'i01_course_research.ipynb').read_text(encoding='utf-8'))
    nbformat.validate(nbformat.from_dict(research))
    research_receipt=verify_research_notebook(research)
    assert (root/'notebooks/i01_course_kaggle.ipynb').read_bytes()==(delivery/'i01_course_kaggle.ipynb').read_bytes()
    assert (root/'notebooks/i01_course_research.ipynb').read_bytes()==(delivery/'i01_course_research.ipynb').read_bytes()
    assert (delivery/'i01_course_research.ipynb').read_bytes()==(delivery/'i01_course_kaggle.ipynb').read_bytes()
    assert sorted(p.name for p in (delivery/'kaggle-input').iterdir())==['i01-source.zip']
    installed_continuation=False
    with tempfile.TemporaryDirectory(prefix="i01-installed-review-") as name:
        temp=Path(name); source=temp/"source"
        with zipfile.ZipFile(delivery/"i01-source.zip") as z:
            assert z.testzip() is None; z.extractall(source)
        manifest=json.loads((source/"source-release.json").read_text())
        for rel,wanted in manifest["files"].items():
            path=source/rel
            assert path.stat().st_size==wanted["bytes"] and digest(path)==wanted["sha256"],rel
        # Exercise the actual bootstrap extraction/identity code for ZIP, rerun
        # and Kaggle-expanded source inputs, replacing display construction only.
        import shutil
        inputs=temp/"input"; inputs.mkdir()
        working=temp/"working"; working.mkdir()
        shutil.copy2(delivery/"i01-source.zip",inputs/"i01-source.zip")
        # An expanded old checkpoint also has source-release.json. Its source
        # must be ignored by this repaired notebook's automatic source picker.
        old_source=inputs/'expanded-old-checkpoint/source';old_source.mkdir(parents=True)
        (old_source/'source-release.json').write_text(json.dumps(dict(format='i01-online-source-v1',files={'recovery/i01/workflow.py':{}})))
        shutil.copytree(source,inputs/'expanded-repaired-source')
        class BootstrapStub:
            def __init__(self,source,**kwargs):self.source=Path(source);self.run_dir=Path(kwargs['run'])
            def bootstrap_status(self): pass
        bootstrap="".join(next(c for c in cells if c['id']=='workspace')["source"]).replace("/kaggle/input",inputs.as_posix()).replace("/kaggle/working",working.as_posix())
        bootstrap=bootstrap.replace("from recovery.i01.notebook import Study","Study = BootstrapStub")
        # Verification already imported recovery from the checkout, so first
        # prove the guard rejects cached foreign code, then bypass that guard
        # solely while exercising ZIP/extracted source selection with the stub.
        bootstrap_namespace={"BootstrapStub":BootstrapStub,'RUN_DIR':str(working/'fresh-study')}
        try:
            exec(compile(bootstrap,'stale-import-guard','exec'),dict(bootstrap_namespace))
        except RuntimeError as error:
            assert 'Restart the notebook kernel' in str(error)
        else: raise AssertionError('Cached foreign source was not rejected')
        bootstrap=bootstrap.replace("loaded_source = sys.modules.get('recovery')","loaded_source = None")
        exec(compile(bootstrap,"n01-zip","exec"),bootstrap_namespace)
        exec(compile(bootstrap,"n01-rerun","exec"),bootstrap_namespace)
        expanded=bootstrap.replace("SOURCE_BUNDLE = None",f"SOURCE_BUNDLE = {source.as_posix()!r}")
        exec(compile(expanded,"n01-expanded","exec"),bootstrap_namespace)
        old_explicit=bootstrap.replace('SOURCE_BUNDLE = None',f'SOURCE_BUNDLE = {old_source.as_posix()!r}')
        try:exec(compile(old_explicit,'refuse-old-source','exec'),dict(bootstrap_namespace))
        except RuntimeError as error:assert 'requires the whole-study' in str(error)
        else:raise AssertionError('The repaired notebook accepted an explicit legacy source packet')
        wheels=list(source.glob("*.whl")); assert len(wheels)==1
        venv=temp/'venv'
        subprocess.run([sys.executable,'-I','-S','-m','venv','--without-pip',str(venv)],check=True,timeout=60)
        python=venv/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
        installed=venv/'Lib/site-packages' if os.name=='nt' else venv/'lib'/f'python{sys.version_info.major}.{sys.version_info.minor}'/'site-packages'
        subprocess.run([sys.executable,"-m","pip","install","--no-deps","--no-index","--target",str(installed),str(wheels[0])],check=True,timeout=60)
        for rel,wanted in manifest["files"].items():
            if rel.startswith("recovery/") and rel.endswith(".py"):
                assert digest(installed/rel)==wanted["sha256"],rel
        env=dict(os.environ,PYTHONPATH='/unapproved/host/hooks',MPLBACKEND='module://unavailable_renderer')
        command=runtime_command(python,source,'-m','recovery.i01.cli','--source',source)
        run=temp/"scripted-empty"
        subprocess.run(command+["--run",str(run),"init","--independent"],cwd=temp,env=env,check=True,stdout=subprocess.DEVNULL,timeout=30)
        status=json.loads(subprocess.check_output(command+["--run",str(run),"status"],cwd=temp,env=env,text=True,timeout=30))
        assert status["attempts"]==0 and status["known_pairs"]==0 and status["missingness_bounds"]==[-1,1]
        assert status['remaining_attempt_allowance']==500 and status['missing_prior_studies']==[]
        assert status['attempt_scope']=='independent-study' and status['prior_attempts']==0
        subprocess.run(command+['--run',str(run),'report','--output',str(temp/'fresh-report'),'--no-plots'],cwd=temp,env=env,check=True,stdout=subprocess.DEVNULL,timeout=30)
        assert 'independent-study' in (temp/'fresh-report/overview.md').read_text(encoding='utf-8')
        older=root/'notebooks/run/course-2/latest.zip';selected=root/'notebooks/run/course-3/latest.zip'
        if older.is_file() and selected.is_file():
            continued=temp/'continued'
            receipt=json.loads(subprocess.check_output(command+['--run',str(continued),'continue-checkpoint',str(selected),'--prior',str(older),'--tail','latest','--evidence','Zero-model package verification fixture; no additional exposure'],cwd=temp,env=env,text=True,timeout=45))
            assert receipt['preserved_attempts']==23 and receipt['campaign_attempts']==41
            status=json.loads(subprocess.check_output(command+['--run',str(continued),'status'],cwd=temp,env=env,text=True,timeout=30))
            assert status['attempts']==23 and status['campaign_attempts']==41 and status['contingency']==18
            assert status['qualification']['direct']['passed'] and status['qualification']['direct']['correct']==10
            assert status['qualification']['thinking']['recorded']==5 and status['qualification']['thinking']['unexecuted']==7
            offline=temp/'offline-report'
            subprocess.run(command+['--run',str(continued),'report','--output',str(offline),'--no-plots'],cwd=temp,env=env,check=True,stdout=subprocess.DEVNULL,timeout=30)
            assert (offline/'qualification_controls.csv').is_file() and (offline/'prior_spending.csv').is_file()
            assert '41/500' in (offline/'overview.md').read_text(encoding='utf-8')
            assert len(json.loads((offline/'analysis.json').read_text())['attempts'])==23
            installed_continuation=True
        for rel,wanted in manifest["files"].items():
            assert digest(run/"source"/rel)==wanted["sha256"],rel
        assert not any(".safetensors" in p or ".env" in p or "/site-packages/" in p for p in manifest["files"])
    receipt=dict(passed=True,**notebook_receipt,source_head=manifest['git_head'],source_members=len(manifest["files"]),
                 research_notebook=research_receipt,installed_fresh_independent_initialization=True,
                 source_zip_bytes=(delivery/"i01-source.zip").stat().st_size,source_zip_sha256=digest(delivery/"i01-source.zip"),
                 installed_wheel_source_matches=True,installed_outside_checkout_cli=True,
                 installed_venv_isolated_entry=True,
                 installed_actual_course3_continuation=installed_continuation,
                 installed_cpu_only_report_without_matplotlib=installed_continuation,
                 zip_expanded_source_bootstrap_and_rerun=True,complete_source_preserved_in_checkpoints=True,
                 notebook_execution_outputs_empty=True,
                 kaggle_host_verified=False,qualification_pilot_main_executed=False)
    atomic_json(root/"notebooks/validation/i01-development/recovery-run-all-release-review.json",receipt)
    return receipt


if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]
    print(json.dumps(verify(root,root/"dist/i01-course-recovery-run-all"),indent=2))
