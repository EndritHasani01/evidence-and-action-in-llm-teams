"""Execute the delivered notebook with both staging/execution flags disabled."""

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import zipfile

import nbformat
from nbclient import NotebookClient


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("packet", "work", "evidence"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    packet, work, evidence = (getattr(args, name).resolve() for name in ("packet", "work", "evidence"))
    assert not work.exists() and not evidence.exists()
    work.mkdir(parents=True)
    notebook = nbformat.read(packet / "course_m5_hardware_smoke.ipynb", as_version=4)
    nbformat.validate(notebook)
    assert all(c.execution_count is None and not c.outputs for c in notebook.cells if c.cell_type == "code")
    manifest = json.loads((packet / "source-manifest.json").read_bytes())
    payload = packet / manifest["payload_filename"]
    output = work / "review"
    environment = dict(os.environ, COURSE_M5_PAYLOAD=str(payload), COURSE_M5_HW_OUTPUT=str(output))
    environment.pop("PYTHONPATH", None)
    NotebookClient(notebook, timeout=60, startup_timeout=30, kernel_name="python3").execute(cwd=str(work), env=environment)
    assert [c.execution_count for c in notebook.cells if c.cell_type == "code"] == [1, 2, 3, 4]
    assert not any(o.output_type == "error" for c in notebook.cells if c.cell_type == "code" for o in c.outputs)
    cpu = json.loads((output / "cpu-assets/report.json").read_bytes())
    gpu = json.loads((output / "gpu-smoke/report.json").read_bytes())
    assert cpu["status"] == gpu["status"] == "blocked"
    assert cpu["weights_staged"] is False and cpu["gpu_execution"] is False
    assert gpu["model_generations"] == 0 and gpu["gpu_admission"] is False
    assert gpu["physical_memory_accepted"] is False and gpu["provider_release_confirmed"] is False
    assert not list(output.rglob("worker-*.sqlite"))
    archive_path = output / "preflight-results.zip"
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        assert json.loads(archive.read("cpu-assets/report.json")) == cpu
        assert json.loads(archive.read("gpu-smoke/report.json")) == gpu
        assert not any(name.endswith((".safetensors", ".whl")) for name in archive.namelist())
    receipt = dict(source_commit=manifest["source_baseline_commit"], interpreter=sys.executable,
        notebook_cells_executed=4, source_members=len(manifest["members"]),
        payload_bytes=payload.stat().st_size, payload_sha256=digest(payload),
        export_zip_bytes=archive_path.stat().st_size, export_zip_sha256=digest(archive_path),
        closed_export_reopened=True, model_generations=0, pretrained_weights_staged=False,
        gpu_admission=False, physical_memory_accepted=False, work=str(work))
    evidence.mkdir(parents=True)
    nbformat.write(notebook, evidence / "executed.ipynb")
    for name in ("course_m5_hardware_smoke.ipynb", "launch-template.json", "candidate-linux313.lock"):
        shutil.copyfile(packet / name, evidence / name)
    shutil.copyfile(archive_path, evidence / "preflight-results.zip")
    (evidence / "source-manifest.json.gz").write_bytes(gzip.compress((packet / "source-manifest.json").read_bytes(), mtime=0))
    (evidence / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
