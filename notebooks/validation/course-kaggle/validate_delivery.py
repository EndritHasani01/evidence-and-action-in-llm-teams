"""Exercise the literal delivered notebook and ordinary CPU package, no inference."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet",type=Path,required=True)
    parser.add_argument("--work",type=Path,required=True)
    parser.add_argument("--cpu-python",type=Path,required=True)
    args=parser.parse_args()
    packet,work=args.packet.resolve(),args.work.resolve()
    if work.exists():
        raise FileExistsError(work)
    work.mkdir(parents=True)
    dataset=work/"input/dataset"
    dataset.mkdir(parents=True)
    with zipfile.ZipFile(packet/"course-kaggle-dataset.zip") as z:
        assert z.testzip() is None
        z.extractall(dataset)
    summary=json.loads((packet/"package-summary.json").read_bytes())
    manifest=json.loads((dataset/"source-manifest.json").read_bytes())
    assert summary["dataset_sha256"]==hashlib.sha256((packet/"course-kaggle-dataset.zip").read_bytes()).hexdigest()
    for name,wanted in manifest["members"].items():
        data=(dataset/name).read_bytes()
        assert len(data)==wanted["bytes"] and hashlib.sha256(data).hexdigest()==wanted["sha256"],name
    import nbclient,nbformat
    notebook=nbformat.read(packet/"course_kaggle.ipynb",as_version=4)
    nbformat.validate(notebook)
    environment=dict(os.environ,COURSE_WORKSPACE=str(work/"workspace"),COURSE_INPUT=str(work/"input"))
    nbclient.NotebookClient(notebook,timeout=120,kernel_name="python3").execute(env=environment,cwd=str(work))
    nbformat.write(notebook,work/"executed-inspect.ipynb")
    bundle=work/"workspace/bundle"
    source=bundle/"source"
    assert (work/"workspace/course-resume.zip").exists()
    assert not list(bundle.rglob("worker-*.sqlite"))
    config=json.loads((bundle/"operator-config.json").read_bytes())
    assert config["execute_gpu"] is False and not any(config["authorizations"].values())
    python=args.cpu_python.resolve()
    def command(name,arguments,allowed=(0,),timeout=180):
        completed=subprocess.run([str(p) for p in arguments],cwd=work,capture_output=True,text=True,timeout=timeout)
        (work/(name+".stdout.txt")).write_text(completed.stdout,encoding="utf-8")
        (work/(name+".stderr.txt")).write_text(completed.stderr,encoding="utf-8")
        if completed.returncode not in allowed:
            raise AssertionError(f"{name}: {completed.returncode}: {completed.stderr[-3000:]}")
        return completed
    command("install-delivered-project",[python,"-m","pip","install","--no-deps",source])
    command("installed-CPU-check",[python,"-m","pip","check"])
    base=[python,"-I",source/"scripts/course_kaggle_workflow.py","--root",source,"--bundle",bundle,
          "--config",bundle/"operator-config.json"]
    command("guarded-hardware",base+["--action","hardware"],allowed=(2,))
    blocked=json.loads((bundle/"last-action.json").read_bytes())
    assert "authorization_missing" in blocked["reason"]
    assert not list(bundle.rglob("worker-*.sqlite"))
    command("three-host-checks",[python,"-I",source/"scripts/m5_course_smoke.py","--root",source,
        "--launch",source/"configs/course-smoke-launch.json","--output",work/"unused-host-output","--host-checks"],timeout=180)
    command("offline-analysis",base+["--action","analyze"],timeout=300)
    receipt=json.loads((bundle/"analysis-receipt.json").read_bytes())
    assert receipt["status"]=="feasibility" and receipt["coverage"]["unknown"]==6280
    assert receipt["byte_identical_reproductions"]==2 and receipt["inference_calls"]==0
    report_path=bundle/receipt["report"]
    report=json.loads((report_path.parent/"report.json").read_bytes())
    assert len(report["exhibits"])==7
    assert len(list((report_path.parent/"figures").glob("*.svg")))==7
    assert len(list((report_path.parent/"figures").glob("*.png")))==7
    assert "Limited course feasibility" in report_path.read_text(encoding="utf-8")
    # Reopen the actual export in another workspace, no source-checkout path.
    restored=work/"restored"
    with zipfile.ZipFile(work/"workspace/course-resume.zip") as z:
        assert z.testzip() is None
        z.extractall(restored)
    command("restored-offline-analysis",[python,"-I",restored/"source/scripts/course_kaggle_workflow.py",
        "--root",restored/"source","--bundle",restored,"--config",restored/"operator-config.json","--action","analyze"],timeout=300)
    new=json.loads((restored/"analysis-receipt.json").read_bytes())
    assert new==receipt
    for p in report_path.parent.rglob("*"):
        if p.is_file():
            other=restored/Path(new["report"]).parent/p.relative_to(report_path.parent)
            assert other.read_bytes()==p.read_bytes(),p.name
    facts=dict(passed=True,source_commit=summary["source_commit"],dataset_bytes=summary["dataset_bytes"],
        source_members=len(manifest["members"]),literal_notebook_executed=True,guarded_model_calls=0,
        ordinary_installed_CPU_environment=True,source_pythonpath=False,host_checks=3,
        intended_main_slots=6280,recorded_main_slots=0,unknown_main_slots=6280,
        seven_figures_svg_png=True,portable_restore_report_bytes_identical=True,
        native_weights_loaded=False,actual_T4_acceptance=False)
    (work/"delivery-evidence.json").write_text(json.dumps(facts,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(facts,indent=2))


if __name__=="__main__":
    main()
