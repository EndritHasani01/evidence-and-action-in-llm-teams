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


def verify_research_notebook(notebook):
    """Execute ordinary stage cells only against a recording, zero-model stub."""
    expected={
        'workspace':[], 'setup':['install_runtime'], 'open-study':['open'],
        'selfcheck':['check_implementation'], 'weights':['download_weights'], 'session-window':['configure_session'], 'load':['load_models'],
        'readiness':['check_readiness'], 'direct-screen':['qualify_direct'],
        'qualification':['inspect_qualification'], 'thinking-history':['inspect_thinking'],
        'envelope':['check_headroom'], 'pilot-1':['run_pilot'], 'review-pilot-1':['record_pilot_review'],
        'pilot-2':['run_pilot'], 'review-pilot-2':['record_pilot_review'], 'pilot-3':['run_pilot'],
        'review-pilot-3':['record_pilot_review'], 'pre-freeze':['review_configuration'],
        'freeze':['freeze_configuration'], 'prepare-batch':['prepare_main_batch'],
        'main-batch':['run_main_batch'], 'review-batch':['record_batch_review'],
        'report':['build_report'], 'archive':['save_checkpoint'], 'close':['finish_session']}
    cells=[c for c in notebook['cells'] if c['cell_type']=='code']
    assert [c['id'] for c in cells]==list(expected),'ordinary stage order differs'
    assert all(c['execution_count'] is None and not c['outputs'] for c in cells)
    assert notebook['metadata']['i01']['run_all_can_execute_inference'] is True
    assert 'Do not use Run All' in ''.join(notebook['cells'][0]['source'])
    class Stub:
        def __init__(self): self.calls=[]
        def __getattr__(self,name):
            assert name in {n for names in expected.values() for n in names}
            def record(*args,**kwargs):
                self.calls.append(dict(method=name,args=list(args),kwargs=kwargs))
                return {}
            return record
    stub=Stub()
    namespace=dict(study=stub,START_MODE='new',SESSION_DEADLINE_UTC=None,SESSION_ALLOWANCE_EVIDENCE='')
    receipts={}
    for cell in cells:
        source=''.join(cell['source']); compile(source,cell['id'],'exec')
        tree=ast.parse(source)
        assert 'ui.' not in source
        assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('panel','inspect_panel','generate','start','run_all','run','run_action','action') for n in ast.walk(tree))
        if cell['id']=='workspace': continue  # Real extraction is checked below.
        stub.calls=[]
        exec(compile(source,cell['id'],'exec'),namespace)
        assert [c['method'] for c in stub.calls]==expected[cell['id']],cell['id']
        receipts[cell['id']]=stub.calls
    for number in (1,2,3):
        assert receipts[f'pilot-{number}'][0]['args']==[number]
        review=receipts[f'review-pilot-{number}'][0]
        assert review['args']==[number]
        assert review['kwargs']==dict(useful_communication=None,usable=None,notes='')
    assert receipts['direct-screen'][0]['kwargs']=={}
    assert 'deadline' not in receipts['open-study'][0]['kwargs']
    assert receipts['session-window'][0]['kwargs']==dict(remaining_minutes=None,evidence='')
    assert receipts['prepare-batch'][0]['kwargs']==dict(count=2)
    assert receipts['thinking-history'][0]['args']==[]
    assert next(c for c in cells if c['id']=='thinking-history')['metadata']['i01']['generation'] is False
    assert receipts['open-study'][0]['kwargs']['prior_checkpoints'] is None
    assert receipts['open-study'][0]['kwargs']['independent'] is True
    assert receipts['freeze'][0]['args']==['']
    assert receipts['archive'][0]['kwargs']==dict(verify=True)
    return dict(code_cells=len(cells),widget_panels=0,independent_cell_scopes=receipts,
                run_all_can_execute_inference=True,model_attempts=0)


def verify_notebook(notebook):
    """Run every preparation stage sequentially with a zero-model recorder."""
    expected=dict(configuration=[],workspace=[],**{'session-window':['configure_session'],
        'setup':['install_runtime'],'open-study':['start_new'],'selfcheck':['check_implementation'],
        'weights':['download_weights'],'load':['load_models'],'readiness':['check_readiness'],
        'direct-screen':['qualify_direct'],'qualification':['inspect_qualification'],
        'envelope':['check_headroom'],'report':['build_report'],'archive':['save_checkpoint']})
    cells=[c for c in notebook['cells'] if c['cell_type']=='code']
    assert [c['id'] for c in cells]==list(expected)
    assert all(c['execution_count'] is None and not c['outputs'] for c in cells)
    assert notebook['metadata']['i01']['run_all_supported'] is True
    assert notebook['metadata']['i01']['first_attempt_ceiling']==20
    assert 'Run All' in ''.join(notebook['cells'][0]['source'])
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
                       ('panel','inspect_panel','generate','run_all','run','run_action','action','qualify_thinking','run_pilot','freeze_configuration','run_main_batch') for n in ast.walk(tree))
        assert not any(isinstance(n,(ast.For,ast.While)) for n in ast.walk(tree)) or cell['id']=='workspace'
        if cell['id']=='workspace':continue  # Actual ZIP/expanded extraction checked separately.
        stub.calls=[];exec(compile(source,cell['id'],'exec'),namespace)
        assert [c['method'] for c in stub.calls]==expected[cell['id']],cell['id']
        receipts[cell['id']]=stub.calls
    assert receipts['session-window'][0]['kwargs']==dict(remaining_minutes=None,evidence='')
    assert receipts['open-study'][0]['args']==[] and receipts['open-study'][0]['kwargs']=={}
    assert receipts['qualification'][0]['kwargs']==dict(mode='direct')
    assert receipts['archive'][0]['kwargs']==dict(verify=True)
    return dict(code_cells=len(cells),widget_panels=0,independent_cell_scopes=receipts,
                run_all_supported=True,first_attempt_ceiling=20,run_all_can_execute_inference=True,model_attempts=0)


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
        except RuntimeError as error:assert 'requires the repaired' in str(error)
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
    atomic_json(root/"notebooks/validation/i01-development/fresh-release-review.json",receipt)
    return receipt


if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]
    print(json.dumps(verify(root,root/"dist/i01-course-fresh"),indent=2))
