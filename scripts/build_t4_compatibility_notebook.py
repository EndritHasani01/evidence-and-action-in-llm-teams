"""Build one immutable, self-contained T4 library diagnostic notebook."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SHA256 = "57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f"
BASELINE = "ca46bcd55486b38bb453f5294e01f943bc7f7752"


def notebook_document(program: str, operations: str, expected: dict) -> dict:
    def cell(kind, source, identity):
        result = {"cell_type": kind, "id": identity, "metadata": {}, "source": source}
        if kind == "code":
            result.update(execution_count=None, outputs=[])
        return result

    instructions = """# M5: tiny T4 attention and NF4 compatibility check

CPU preparation already passed. This checks small library operations before model weights.

1. Import this file as a **new private Kaggle notebook**. **No input dataset is needed.**
2. Select **Internet On** and **GPU T4 x2** only when ready. Start **Run All within one minute** of GPU assignment. If the session has already been allocated longer, stop it and report the displayed elapsed time before running.
3. Run once. The only download is the verified **60.7 MB bitsandbytes wheel** into temporary storage. The base environment is unchanged. No model weights or generations run.
4. Download the result ZIP and the executed notebook with outputs, then **stop the GPU session immediately**. Save them under **`notebooks/run/6/`** and report the displayed allocation duration. Avoid Save & Run All: that can execute the work again.

The controller admits work within 360 seconds, including a 90-second export reserve. Allow 120 seconds for retrieval/stopping. With at most 60 seconds before the first cell, the conditional ceiling is 0.3 aggregate GPU-hour for two assigned T4s. Prior/setup/idle time still counts; this grants no fresh model-smoke allowance. Provider start/release is not inferred from cell timestamps.

Matching host Torch 2.11.0+cu128 is required; a mismatch exports diagnostics without changing packages. This standalone library environment is not the accepted scientific model lock. Tiny successful operations cannot pass full-context memory, Qwen loading/recurrent behavior or model smoke. The final cell exports failures too; return the first result rather than rerunning.
"""
    setup = ("import hashlib,json,os,time\nfrom pathlib import Path\n\n"
             "if 'COMPATIBILITY_STARTED' not in globals():\n    COMPATIBILITY_STARTED=time.monotonic()\n"
             f"OPERATIONS_PROGRAM={operations!r}\nCOMPATIBILITY_PROGRAM={program!r}\n"
             f"EXPECTED=json.loads({json.dumps(expected,sort_keys=True)!r})\n"
             "assert hashlib.sha256(OPERATIONS_PROGRAM.encode()).hexdigest()==EXPECTED['operations_sha256']\n"
             "assert hashlib.sha256(COMPATIBILITY_PROGRAM.encode()).hexdigest()==EXPECTED['program_sha256']\n"
             "operations_namespace={'__name__':'m5_compatibility_operations'}\n"
             "exec(compile(OPERATIONS_PROGRAM,'m5_kaggle_preflight.py','exec'),operations_namespace)\n"
             "compatibility_namespace={'__name__':'m5_t4_compatibility'}\n"
             "exec(compile(COMPATIBILITY_PROGRAM,'m5_t4_compatibility.py','exec'),compatibility_namespace)\n")
    run = ("# Path overrides are only for local validation; Kaggle defaults need no edits.\n"
           "if 'COMPATIBILITY_RESULT' not in globals():\n"
           "    COMPATIBILITY_RESULT=compatibility_namespace['run_compatibility'](\n"
           "        Path(os.environ.get('M5_COMPAT_OUTPUT_ROOT','/kaggle/working')),\n"
           "        Path(os.environ.get('M5_COMPAT_SCRATCH_ROOT','/tmp/recovery-m5-t4')),\n"
           "        EXPECTED,operations_namespace,COMPATIBILITY_PROGRAM,COMPATIBILITY_STARTED)\n"
           "else:\n    print('Already executed in this kernel; showing the retained result without another run.')\n")
    display = ("from IPython.display import FileLink,display\n\n"
               "print(COMPATIBILITY_RESULT['summary']['next_action'])\n"
               "if COMPATIBILITY_RESULT['zip_path']:\n"
               "    print('Result ZIP SHA-256:',COMPATIBILITY_RESULT['zip_sha256'])\n"
               "    display(FileLink(os.path.relpath(COMPATIBILITY_RESULT['zip_path'],Path.cwd())))\n"
               "else:\n"
               "    print('Export failed; retain JSON/logs from:',COMPATIBILITY_RESULT['run_directory'])\n"
               "    print(COMPATIBILITY_RESULT['report'].get('export_error'))\n"
               "print('Stop the GPU session now. Model smoke remains unexecuted.')\n")
    return {"nbformat": 4, "nbformat_minor": 5, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}}, "cells": [
            cell("markdown", instructions, "t4-instructions"), cell("code", setup, "t4-bootstrap"),
            cell("markdown", "## Run the bounded library checks\n", "t4-run-title"), cell("code", run, "t4-run"),
            cell("markdown", "## Download the evidence and stop\n", "t4-export-title"), cell("code", display, "t4-export")]}


def build(archive_path: Path, notebook_path: Path, build_commit: str) -> dict:
    if notebook_path.exists():
        raise FileExistsError("Preserve previous notebook artifacts: " + str(notebook_path))
    with archive_path.open("rb") as incoming:
        if hashlib.file_digest(incoming, "sha256").hexdigest() != CANONICAL_SHA256:
            raise ValueError("canonical_source_archive_changed")
    configs = {}
    with zipfile.ZipFile(archive_path) as archive:
        for model in ("9B", "4B"):
            raw = archive.read("metadata/" + model + "/config.json")
            configs[model] = {"text": raw.decode("utf-8"), "sha256": hashlib.sha256(raw).hexdigest()}
    files = json.loads((ROOT / "notebooks/validation/m5-full-preparation/candidate-wheel-files.json").read_text(encoding="utf-8"))
    wheel = next(p for p in files if p["name"] == "bitsandbytes")
    audit = json.loads((ROOT / "notebooks/validation/m5-t4-compatibility/wheel-audit.json").read_text(encoding="utf-8"))
    if audit["wheel"] != wheel or audit["crc"] != "passed":
        raise ValueError("reviewed_wheel_audit_differs")
    expected = {"scientific_baseline_commit": BASELINE, "canonical_archive_sha256": CANONICAL_SHA256,
                "build_commit": build_commit, "configs": configs, "candidate_versions": {p["name"]: p["version"] for p in files},
                "bitsandbytes_wheel": dict(wheel, expanded_bytes=audit["actual_expanded_bytes"], members=audit["members"])}
    paths = [ROOT / "scripts/m5_t4_compatibility.py", ROOT / "scripts/m5_kaggle_preflight.py"]
    for path in [*paths, Path(__file__).resolve(),
                 ROOT / "notebooks/validation/m5-full-preparation/candidate-wheel-files.json",
                 ROOT / "notebooks/validation/m5-t4-compatibility/wheel-audit.json"]:
        committed = subprocess.check_output(["git", "show", build_commit + ":" + path.relative_to(ROOT).as_posix()], cwd=ROOT)
        if committed.decode("utf-8").replace("\r\n", "\n") != path.read_text(encoding="utf-8").replace("\r\n", "\n"):
            raise ValueError("build_checkpoint_differs_from_source: " + str(path))
    program, operations = [p.read_text(encoding="utf-8") for p in paths]
    expected.update(program_sha256=hashlib.sha256(program.encode()).hexdigest(),
                    operations_sha256=hashlib.sha256(operations.encode()).hexdigest())
    notebook_path.parent.mkdir(parents=True, exist_ok=True)
    notebook_path.write_text(json.dumps(notebook_document(program, operations, expected), indent=1)+"\n", encoding="utf-8", newline="\n")
    return expected


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-archive", type=Path, default=ROOT / "dist/m5-kaggle-preflight.zip")
    parser.add_argument("--notebook", type=Path, default=ROOT / "notebooks/recovery_m5_kaggle_t4_compatibility.ipynb")
    args = parser.parse_args()
    identity = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    result = build(args.source_archive, args.notebook, identity)
    print(json.dumps({"notebook": str(args.notebook), "build_commit": identity,
                      "program_sha256": result["program_sha256"]}, indent=2))
