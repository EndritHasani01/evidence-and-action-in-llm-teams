"""Build the small private online source attachment; no dependencies/weights."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from recovery.i01.archive import atomic_json, digest, inventory
from recovery.i01.policy import RECOVERY_POLICY


def build(root, out):
    root,out=Path(root).resolve(),Path(out).resolve()
    out.mkdir(parents=True,exist_ok=True)
    attachment=out/'kaggle-input'
    if attachment.exists() and any(p.name!='i01-source.zip' for p in attachment.iterdir()):
        raise ValueError('Fresh upload directory must contain only i01-source.zip; preserve old deliveries and select a fresh output directory')
    with tempfile.TemporaryDirectory(prefix="i01-release-",dir=out) as temp:
        source=Path(temp)/"source"; source.mkdir()
        relative=[p.relative_to(root) for p in (root/"recovery").rglob("*.py")]
        relative += [Path(p) for p in ("pyproject.toml","configs/i01-course.json","configs/i01-runtime.lock",
                     "PROJECT_SPECIFICATION.md","AGENTS.md","docs/I01_KAGGLE.md",
                     "docs/validation/i01-implementation.md",
                     "docs/plans/i01-course-implementation-wbs.md","scripts/i01_course.py",
                     "scripts/build_i01_course_notebook.py","scripts/build_i01_course_release.py")]
        relative += [Path("scripts/verify_i01_course_release.py"),Path("tests/__init__.py"),Path("tests/test_i01_integration.py")]
        relative += [Path('tests/test_i01_notebook_ui.py'),Path('docs/plans/i01-notebook-natural-workflow.md')]
        relative += [Path('tests/test_i01_setup.py'),Path('tests/test_i01_client_startup.py'),Path('tests/test_i01_repairs.py'),Path('tests/test_i01_runtime.py')]
        relative += [Path('docs/validation/i01-course-1-repair.md')]
        relative += [Path('tests/test_i01_course3_repairs.py'),Path('docs/validation/i01-course-3-repair.md')]
        relative += [Path('tests/test_i01_fresh_run.py'),Path('docs/validation/i01-fresh-run.md')]
        relative += [Path('tests/test_i01_recovery_admission.py'),Path('docs/validation/i01-course-5-repair.md')]
        relative += [Path('docs/validation/i01-course-5-results-analysis.md'),Path('docs/proposals/i01-course-5-fix-and-improvement-proposal.md')]
        relative += [Path('tests/test_i01_run_all.py'),Path('docs/validation/i01-course-4-run-all.md')]
        relative += [Path('notebooks/validation/i01-development')/(name+'.json') for name in
                     ('course3-core-checks','course3-final-checks','course3-format-checks','fresh-run-checks','run-all-checks',
                      'recovery-final-checks','recovery-guard-checks','recovery-admission-checks','recovery-saved-evidence')]
        # Builder can make a Python-only release before notebook completion.
        for name in ('i01_course_kaggle.ipynb','i01_course_research.ipynb'):
            if (root/'notebooks'/name).exists():relative.append(Path('notebooks')/name)
        for rel in relative:
            destination=source/rel; destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(root/rel,destination)
        subprocess.run([sys.executable,"-m","pip","wheel","--no-deps","--no-build-isolation",
                        "--wheel-dir",str(source),str(root)],check=True,timeout=120)
        wheels=list(source.glob("*.whl"))
        if len(wheels)!=1: raise ValueError("one complete wheel required")
        with zipfile.ZipFile(wheels[0]) as z:
            if any('recovery/i01/'+name+'.py' not in z.namelist() for name in ('workflow','ui','policy','continuation')):
                raise ValueError("wheel is missing I-01 package")
        head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=root,text=True).strip()
        dirty=subprocess.check_output(["git","status","--porcelain"],cwd=root,text=True).splitlines()
        manifest=dict(format="i01-online-source-v1",git_head=head,working_tree=dirty,
                      execution_policy=RECOVERY_POLICY,run_all_scope='whole-study',
                      files=inventory(source),model_weights_included=False,dependencies_included=False)
        atomic_json(source/"source-release.json",manifest)
        target=out/"i01-source.zip"; partial=out/"i01-source.zip.partial"
        with zipfile.ZipFile(partial,"w",zipfile.ZIP_DEFLATED) as z:
            for p in sorted(source.rglob("*")):
                if p.is_file(): z.write(p,p.relative_to(source).as_posix())
        with zipfile.ZipFile(partial) as z:
            if z.testzip() is not None: raise ValueError("source ZIP CRC failure")
        partial.replace(target)
        shutil.copy2(source/"source-release.json",out/"source-release.json")
        shutil.copy2(wheels[0],out/wheels[0].name)
        for name in ('i01_course_kaggle.ipynb','i01_course_research.ipynb'):
            notebook=root/'notebooks'/name
            if notebook.exists():shutil.copy2(notebook,out/name)
        shutil.copy2(root/"docs/I01_KAGGLE.md",out/"START_HERE.md")
        attachment=out/'kaggle-input';attachment.mkdir(exist_ok=True)
        shutil.copy2(target,attachment/'i01-source.zip')
        atomic_json(out/"delivery.json",dict(source_zip=str(target),bytes=target.stat().st_size,sha256=digest(target),
                    notebook=str(out/"i01_course_kaggle.ipynb"),source_head=head,files=list(manifest["files"]),
                    research_notebook=str(out/'i01_course_research.ipynb'),
                    kaggle_input_directory=str(attachment),continuation_inputs=[],
                    attempt_scope='independent-study',run_all_supported=True,run_all_scope='whole-study',
                    first_attempt_ceiling=460,hard_attempt_limit=500,contingency_limit=28,
                    execution_policy=RECOVERY_POLICY,human_review='retrospective_pending',
                    implemented=True,kaggle_verified=False,model_attempts=0))
        return target


if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--output",type=Path,default=Path("dist/i01-course-recovery-run-all"))
    args=p.parse_args(); print(build(Path(__file__).resolve().parents[1],args.output))
