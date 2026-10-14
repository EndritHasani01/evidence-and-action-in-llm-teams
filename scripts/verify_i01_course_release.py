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


def verify_notebook(notebook):
    """Execute ordinary stage cells only against a recording, zero-model stub."""
    expected={
        'workspace':[], 'setup':['run'], 'open-study':['open_study'],
        'selfcheck':['run'], 'weights':['run'], 'load':['run'], 'readiness':['run'],
        'direct-screen':['run'], 'qualification':['inspect'], 'thinking-screen':['thinking_screen'],
        'envelope':['envelope'], 'pilot-1':['run'], 'review-pilot-1':['review_pilot'],
        'pilot-2':['run'], 'review-pilot-2':['review_pilot'], 'pilot-3':['run'],
        'review-pilot-3':['review_pilot'], 'pre-freeze':['preview_freeze'], 'freeze':['run'],
        'prepare-batch':['run'], 'main-batch':['run_batch'], 'review-batch':['review_batch'],
        'report':['final_report'], 'archive':['run','verify_checkpoint'], 'close':['run','run']}
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
    namespace=dict(ui=stub,START_MODE='new',SESSION_DEADLINE_UTC=None,SESSION_ALLOWANCE_EVIDENCE='')
    receipts={}
    for cell in cells:
        source=''.join(cell['source']); compile(source,cell['id'],'exec')
        tree=ast.parse(source)
        assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('panel','inspect_panel','generate','start','run_all') for n in ast.walk(tree))
        if cell['id']=='workspace': continue  # Real extraction is checked below.
        stub.calls=[]
        exec(compile(source,cell['id'],'exec'),namespace)
        assert [c['method'] for c in stub.calls]==expected[cell['id']],cell['id']
        receipts[cell['id']]=stub.calls
        for call in stub.calls:
            if call['method']=='run':
                allowed=[cell['metadata']['i01']['action']]
                if cell['id']=='close': allowed=['close_models','shutdown']
                assert call['args'][0] in allowed,cell['id']
    for number in (1,2,3):
        assert receipts[f'pilot-{number}'][0]['kwargs']==dict(number=number)
        review=receipts[f'review-pilot-{number}'][0]
        assert review['args']==[number]
        assert review['kwargs']==dict(useful_communication=None,usable=None,notes='')
    assert receipts['direct-screen'][0]['kwargs']==dict(mode='direct')
    assert receipts['prepare-batch'][0]['kwargs']==dict(count=2)
    assert receipts['thinking-screen'][0]['args']==[None]
    assert receipts['freeze'][0]['kwargs']==dict(notes='')
    assert [c['args'][0] for c in receipts['close']]==['close_models','shutdown']
    return dict(code_cells=len(cells),widget_panels=0,independent_cell_scopes=receipts,
                run_all_can_execute_inference=True,model_attempts=0)


def verify(root,delivery):
    root,delivery=Path(root).resolve(),Path(delivery).resolve()
    notebook=json.loads((delivery/"i01_course_kaggle.ipynb").read_text(encoding="utf-8"))
    cells=[c for c in notebook["cells"] if c["cell_type"]=="code"]
    import nbformat
    nbformat.validate(nbformat.from_dict(notebook))
    notebook_receipt=verify_notebook(notebook)
    assert (root/'notebooks/i01_course_kaggle.ipynb').read_bytes()==(delivery/'i01_course_kaggle.ipynb').read_bytes()
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
        class BootstrapStub:
            def __init__(self,*args): pass
            def bootstrap_status(self): pass
        bootstrap="".join(cells[0]["source"]).replace("/kaggle/input",inputs.as_posix()).replace("/kaggle/working",working.as_posix())
        bootstrap=bootstrap.replace("from recovery.i01.ui import Operator","Operator = BootstrapStub")
        bootstrap_namespace={"BootstrapStub":BootstrapStub}
        exec(compile(bootstrap,"n01-zip","exec"),bootstrap_namespace)
        exec(compile(bootstrap,"n01-rerun","exec"),bootstrap_namespace)
        expanded=bootstrap.replace("SOURCE_BUNDLE = None",f"SOURCE_BUNDLE = {source.as_posix()!r}")
        exec(compile(expanded,"n01-expanded","exec"),bootstrap_namespace)
        wheels=list(source.glob("*.whl")); assert len(wheels)==1
        installed=temp/"installed"
        subprocess.run([sys.executable,"-m","pip","install","--no-deps","--no-index","--target",str(installed),str(wheels[0])],check=True,timeout=60)
        for rel,wanted in manifest["files"].items():
            if rel.startswith("recovery/") and rel.endswith(".py"):
                assert digest(installed/rel)==wanted["sha256"],rel
        env=dict(os.environ,PYTHONPATH=str(installed))
        command=[sys.executable,"-m","recovery.i01.cli","--source",str(source)]
        run=temp/"scripted-empty"
        subprocess.run(command+["--run",str(run),"init"],cwd=temp,env=env,check=True,stdout=subprocess.DEVNULL,timeout=30)
        status=json.loads(subprocess.check_output(command+["--run",str(run),"status"],cwd=temp,env=env,text=True,timeout=30))
        assert status["attempts"]==0 and status["known_pairs"]==0 and status["missingness_bounds"]==[-1,1]
        for rel,wanted in manifest["files"].items():
            assert digest(run/"source"/rel)==wanted["sha256"],rel
        assert not any(".safetensors" in p or ".env" in p or "/site-packages/" in p for p in manifest["files"])
    receipt=dict(passed=True,**notebook_receipt,source_members=len(manifest["files"]),
                 source_zip_bytes=(delivery/"i01-source.zip").stat().st_size,source_zip_sha256=digest(delivery/"i01-source.zip"),
                 installed_wheel_source_matches=True,installed_outside_checkout_cli=True,
                 zip_expanded_source_bootstrap_and_rerun=True,complete_source_preserved_in_checkpoints=True,
                 notebook_execution_outputs_empty=True,
                 kaggle_host_verified=False,qualification_pilot_main_executed=False)
    atomic_json(root/"notebooks/validation/i01-development/release-review.json",receipt)
    return receipt


if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]
    print(json.dumps(verify(root,root/"dist/i01-course"),indent=2))
