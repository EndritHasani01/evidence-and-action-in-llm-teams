"""Run the literal CPU review notebook, reject drift, reopen its closed exports."""

import argparse
import ast
from contextlib import closing
from copy import deepcopy
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import zipfile

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[3]


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--reuse-executed", action="store_true",
        help="audit the retained successful execution after a harness-only failure")
    args = parser.parse_args()
    packet, work, evidence = args.packet.resolve(), args.work.resolve(), args.evidence.resolve()
    assert not evidence.exists()
    if not args.reuse_executed:
        assert not work.exists()
        work.mkdir(parents=True)
    notebook = nbformat.read(packet/"course_m5_cpu_review.ipynb", as_version=4)
    nbformat.validate(notebook)
    assert all(c.execution_count is None and not c.outputs for c in notebook.cells if c.cell_type == "code")
    expected = json.loads((packet/"source-manifest.json").read_bytes())
    payload = packet/expected["payload_filename"]
    payload_hash = digest(payload)
    environment = dict(os.environ, COURSE_M5_PAYLOAD=str(payload), COURSE_M5_OUTPUT=str(work/"review"))
    environment.pop("PYTHONPATH", None)
    if args.reuse_executed:
        executed = nbformat.read(work/"executed.ipynb", as_version=4)
        assert [(c.id, c.cell_type, c.source) for c in executed.cells] == [
            (c.id, c.cell_type, c.source) for c in notebook.cells]
        assert not any(o.output_type == "error" for c in executed.cells
            if c.cell_type == "code" for o in c.outputs)
        notebook = executed
    else:
        NotebookClient(notebook, timeout=60, startup_timeout=30, kernel_name="python3").execute(
            cwd=str(work), env=environment)
    assert [c.execution_count for c in notebook.cells if c.cell_type == "code"] == [1, 2, 3]
    nbformat.write(notebook, work/"executed.ipynb")
    output = work/"review"
    report = json.loads((output/"report.json").read_bytes())
    assert report["status"] == "blocked" and report["prepared_requests"] == 24
    assert report["model_generations"] == 0 and not report["pretrained_weights_staged"]
    assert not report["gpu_admission"] and not report["runtime_freeze"]
    assert all(report[k] is None for k in ("provider_quota", "provider_duration", "prior_allocation", "provider_release"))
    assert report["r7"]["complete_live_memory_upper_bound_bytes"] is None
    assert not report["r7"]["terminal_model_feasibility_failure"]
    assert report["source_verification"]["baseline_commit"] == expected["source_baseline_commit"]
    archive_path = output/"preflight-results.zip"
    exported = {}
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        assert not any(name.endswith((".safetensors", ".whl")) for name in archive.namelist())
        for name in ("filesystem.sqlite", "filesystem-backup.sqlite"):
            closed_copy = work/name
            closed_copy.write_bytes(archive.read(name))
            with closing(sqlite3.connect(closed_copy.as_uri()+"?mode=ro&immutable=1", uri=True)) as db:
                assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
                assert db.execute("SELECT value FROM probe").fetchall() == [(7,)]
                try:
                    db.execute("INSERT INTO probe VALUES (8)")
                except sqlite3.OperationalError:
                    pass
                else:
                    raise AssertionError("exported copy must be read-only")
            exported[name] = digest(closed_copy)
    # Exercise the embedded helper without another notebook/kernel or extraction.
    bootstrap = next(c.source for c in notebook.cells if c.id == "course-source")
    helper = next(ast.literal_eval(n.value) for n in ast.parse(bootstrap).body
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "HELPER" for t in n.targets))
    assert hashlib.sha256(helper.encode()).hexdigest() == expected["review_helper_sha256"]
    helpers = {"__name__": "course_review_audit_helper"}
    exec(compile(helper, "embedded_preflight_helper", "exec"), helpers)
    admit_source = helpers["admit_source"]
    wrong = deepcopy(expected)
    wrong["archive_sha256"] = "0"*64
    refused = work/"wrong-source"
    try:
        admit_source(payload, refused, wrong)
    except ValueError as error:
        assert str(error) == "payload_hash_mismatch"
    else:
        raise AssertionError("changed source provenance accepted")
    assert not refused.exists()
    saved = {k: os.environ.get(k) for k in ("COURSE_M5_PAYLOAD", "COURSE_M5_OUTPUT")}
    try:
        os.environ.update(COURSE_M5_PAYLOAD=str(payload), COURSE_M5_OUTPUT=str(output))
        try:
            exec(compile(bootstrap, "course-source", "exec"), {})
        except AssertionError as error:
            assert str(error) == "Use a fresh output; preserve previous evidence"
        else:
            raise AssertionError("existing output accepted")
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    assert digest(payload) == payload_hash
    receipt = dict(source_commit=expected["source_baseline_commit"], interpreter=sys.executable,
        notebook_cells_executed=3, source_members=report["source_verification"]["verified_members"],
        payload_bytes=payload.stat().st_size, payload_sha256=payload_hash,
        export_zip_bytes=archive_path.stat().st_size, export_zip_sha256=digest(archive_path),
        reopened_closed_exports=exported, wrong_source_rejected=True, existing_output_preserved=True,
        model_generations=0, gpu_admission=False, r7_status="blocked", work=str(work))
    evidence.mkdir(parents=True)
    shutil.copyfile(packet/"course_m5_cpu_review.ipynb", evidence/"course_m5_cpu_review.ipynb")
    shutil.copyfile(work/"executed.ipynb", evidence/"executed.ipynb")
    shutil.copyfile(packet/"candidate-linux313.lock", evidence/"candidate-linux313.lock")
    for name in ("source-manifest.json",):
        (evidence/(name+".gz")).write_bytes(gzip.compress((packet/name).read_bytes(), mtime=0))
    for name in ("report.json", "preflight-results.zip"):
        shutil.copyfile(output/name, evidence/name)
    (evidence/"verification.json").write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
