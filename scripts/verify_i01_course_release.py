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


def verify(root,delivery):
    root,delivery=Path(root).resolve(),Path(delivery).resolve()
    notebook=json.loads((delivery/"i01_course_kaggle.ipynb").read_text(encoding="utf-8"))
    cells=[c for c in notebook["cells"] if c["cell_type"]=="code"]
    assert [c["id"] for c in cells]==[f"n{i:02d}" for i in range(1,25)]
    assert all(c["execution_count"] is None and not c["outputs"] for c in cells)
    import nbformat
    nbformat.validate(nbformat.from_dict(notebook))
    class Stub:
        panels=0
        def panel(self,*args,**kwargs): self.panels+=1
        def inspect_panel(self,*args,**kwargs): pass
        def links(self): pass
    stub=Stub(); namespace={"ui":stub}
    for cell in cells:
        source="".join(cell["source"])
        compile(source,cell["id"],"exec")
        tree=ast.parse(source)
        assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ("run","run_action","action","start","generate","run_all") for n in ast.walk(tree))
        if cell["id"]!="n01": exec(compile(source,cell["id"],"exec"),namespace)
    with tempfile.TemporaryDirectory(prefix="i01-installed-review-") as name:
        temp=Path(name); source=temp/"source"
        with zipfile.ZipFile(delivery/"i01-source.zip") as z:
            assert z.testzip() is None; z.extractall(source)
        manifest=json.loads((source/"source-release.json").read_text())
        for rel,wanted in manifest["files"].items():
            path=source/rel
            assert path.stat().st_size==wanted["bytes"] and digest(path)==wanted["sha256"],rel
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
        assert not any(".safetensors" in p or ".env" in p or "/site-packages/" in p for p in manifest["files"])
    receipt=dict(passed=True,code_cells=24,rendered_panels=stub.panels,source_members=len(manifest["files"]),
                 source_zip_bytes=(delivery/"i01-source.zip").stat().st_size,source_zip_sha256=digest(delivery/"i01-source.zip"),
                 installed_wheel_source_matches=True,installed_outside_checkout_cli=True,
                 notebook_execution_outputs_empty=True,run_all_starts_actions=False,model_attempts=0,
                 kaggle_host_verified=False,qualification_pilot_main_executed=False)
    atomic_json(root/"notebooks/validation/i01-development/release-review.json",receipt)
    return receipt


if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]
    print(json.dumps(verify(root,root/"dist/i01-course"),indent=2))
