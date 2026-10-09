"""Build the tiny synthetic raw-payload candidate and its standalone notebook."""

from __future__ import annotations

import argparse
from contextlib import closing
import gzip
import hashlib
import io
import json
from pathlib import Path
import platform
import re
import sqlite3
import stat
import tempfile
import zipfile

from scripts.m5_kaggle_upload_canary import BASELINE_COMMIT, GZIP_PATH, NESTED_PATH


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_NAME = "m5-source-canary.payload"


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def zip_bytes(members: dict[str, bytes]) -> bytes:
    result = io.BytesIO()
    with zipfile.ZipFile(result, "w") as archive:
        for name, data in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    return result.getvalue()


def member_manifest(members: dict[str, bytes]) -> dict:
    return {name: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            for name, data in sorted(members.items())}


def build(output: Path, notebook: Path, source_commit: str | None = None) -> dict:
    if source_commit is not None and re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        raise ValueError("source_commit must be a full verified Git commit or None")
    if output.exists() or notebook.exists():
        raise FileExistsError("Use new output paths; existing evidence is never overwritten.")
    with tempfile.TemporaryDirectory(prefix="m5-canary-build-") as temporary:
        db_path = Path(temporary) / "worker.sqlite"
        with closing(sqlite3.connect(db_path)) as db:
            db.execute("PRAGMA journal_mode=DELETE")
            db.execute("CREATE TABLE probe (value INTEGER NOT NULL)")
            db.execute("INSERT INTO probe VALUES (7)")
            db.commit()
        nested_members = {"worker.sqlite": db_path.read_bytes(),
                          "report.json": json_bytes({"kind": "synthetic-transport-report", "value": 7})}
    decoded = json_bytes({"kind": "synthetic-capacity-fixture", "value": 7,
                          "unicode": "ทดลอง", "scientific_evidence": False})
    members = {"SOURCE_COMMIT.txt": b"synthetic-m5-transport-canary-v1\n",
               "canary.json": json_bytes({"kind": "synthetic-source-transport-canary", "schema_version": 1,
                                          "source_baseline_commit": BASELINE_COMMIT,
                                          "build_source_commit": source_commit}),
               GZIP_PATH: gzip.compress(decoded, mtime=0), NESTED_PATH: zip_bytes(nested_members)}
    payload = zip_bytes(members)
    program = (ROOT / "scripts/m5_kaggle_upload_canary.py").read_text(encoding="utf-8")
    expected = {"schema_version": 1, "kind": "synthetic-source-transport-canary",
                "transport": "raw_payload", "payload_filename": PAYLOAD_NAME,
                "source_baseline_commit": BASELINE_COMMIT, "build_source_commit": source_commit,
                "build_environment": {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version},
                "archive_bytes": len(payload), "archive_sha256": hashlib.sha256(payload).hexdigest(),
                "members": member_manifest(members), "nested_members": member_manifest(nested_members),
                "gzip_decoded": {"bytes": len(decoded), "sha256": hashlib.sha256(decoded).hexdigest()},
                "helper_sha256": hashlib.sha256(program.encode("utf-8")).hexdigest()}

    def cell(kind, text, identifier):
        result = {"cell_type": kind, "id": identifier, "metadata": {}, "source": text.splitlines(keepends=True)}
        if kind == "code":
            result.update(execution_count=None, outputs=[])
        return result

    introduction = """# M5 Kaggle upload test — CPU only

This small test checks whether Kaggle preserves one uploaded archive's exact bytes,
including a gzip fixture and a nested ZIP with a synthetic SQLite file.

1. Create a **private dataset** named `m5-source-canary` and upload only
   **`m5-source-canary.payload`**, keeping that filename and extension.
2. Import this notebook into a **private Kaggle notebook**. Set **Accelerator: None**
   and **Internet: Off**. Attach the new canary dataset using Add Input.
3. If convenient, also attach the original `m5-kaggle-preflight` dataset to collect
   its file inventory. This is optional; the upload test works with just the canary.
4. Select **Run All**. Download the result ZIP from the last cell, stop the session,
   and put the ZIP and the executed notebook in your local `notebooks/run/` folder.

Keep the payload unchanged. If Kaggle refuses the upload, return its error message.
All fixture data are synthetic. This notebook installs no packages, downloads no
weights and performs no language-model generations. A passing result verifies the
tiny transport candidate; full-source preparation and model acceptance remain open.
"""
    setup = ("import hashlib, json, os\nfrom pathlib import Path\n\n"
             f"CANARY_PROGRAM = {program!r}\n"
             f"EXPECTED = json.loads({json.dumps(expected, sort_keys=True)!r})\n"
             "assert hashlib.sha256(CANARY_PROGRAM.encode('utf-8')).hexdigest() == EXPECTED['helper_sha256']\n"
             "canary_namespace = {'__name__': 'recovery_m5_transport_canary'}\n"
             "exec(compile(CANARY_PROGRAM, 'm5_kaggle_upload_canary.py', 'exec'), canary_namespace)\n")
    run = ("# Defaults need no edits on Kaggle. Overrides are for controlled local validation.\n"
           "input_root = Path(os.environ.get('M5_CANARY_INPUT_ROOT', '/kaggle/input'))\n"
           "output_root = Path(os.environ.get('M5_CANARY_OUTPUT_ROOT', '/kaggle/working'))\n"
           "CANARY_RESULT = canary_namespace['run_canary'](input_root, output_root, EXPECTED)\n"
           "print(json.dumps(CANARY_RESULT['summary'], indent=2))\n")
    download = ("from IPython.display import FileLink, display\n\n"
                "if CANARY_RESULT['zip_path']:\n"
                "    print('Download this result ZIP, then stop the Kaggle session:')\n"
                "    print('SHA-256:', CANARY_RESULT['zip_sha256'])\n"
                "    zip_file = Path(CANARY_RESULT['zip_path'])\n"
                "    display(FileLink(os.path.relpath(zip_file, Path.cwd())))\n"
                "else:\n"
                "    print('Export failed. Retain the JSON files in:', CANARY_RESULT['run_directory'])\n"
                "    print(CANARY_RESULT['report'].get('export_error'))\n"
                "print('No model calls were made. Return the results before running the original preflight again.')\n")
    document = {"nbformat": 4, "nbformat_minor": 5,
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                             "language_info": {"name": "python"}},
                "cells": [cell("markdown", introduction, "canary-instructions"),
                          cell("code", setup, "canary-program"),
                          cell("markdown", "## Run the bounded input and backup checks\n", "canary-run-title"),
                          cell("code", run, "canary-run"),
                          cell("markdown", "## Download the evidence\nBoth success and handled failure produce diagnostics.\n", "canary-download-title"),
                          cell("code", download, "canary-download")]}
    output.mkdir(parents=True, exist_ok=False)
    (output / PAYLOAD_NAME).write_bytes(payload)
    (output / "canary-manifest.json").write_bytes(json_bytes(expected))
    (output / "m5-source-canary.sha256").write_text(f"{expected['archive_sha256']}  {PAYLOAD_NAME}\n", encoding="utf-8")
    notebook.parent.mkdir(parents=True, exist_ok=True)
    with notebook.open("x", encoding="utf-8") as handle:
        json.dump(document, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return {"payload": str(output / PAYLOAD_NAME), "notebook": str(notebook), "expected": expected}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist/m5-kaggle-upload-canary")
    parser.add_argument("--notebook", type=Path, default=ROOT / "notebooks/recovery_m5_kaggle_upload_canary.ipynb")
    parser.add_argument("--source-commit", help="Verified commit containing the builder/helper, or omit to record unknown")
    args = parser.parse_args()
    result = build(args.output_dir, args.notebook, args.source_commit)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
