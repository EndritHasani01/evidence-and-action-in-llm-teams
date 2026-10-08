"""CPU-only, dependency-free diagnosis of Kaggle archive transport.

All fixtures are synthetic. This does not validate the study or load a model.
"""

from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import platform
import sqlite3
import stat
import time
import uuid
import zipfile


BASELINE_COMMIT = "ca46bcd55486b38bb453f5294e01f943bc7f7752"
GZIP_PATH = "tests/fixtures/capacity_report.json.gz"
NESTED_PATH = "tests/fixtures/scripted_lifecycle_run.zip"
INVENTORY_LIMIT = 2000
PAYLOAD_LIMIT = 1024 * 1024


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def visible_gpu_devices() -> list[str]:
    """Inspect driver entries without importing Torch or initializing CUDA."""
    location = Path("/proc/driver/nvidia/gpus")
    return sorted(p.name for p in location.iterdir()) if location.is_dir() else []


def inventory(root: Path, limit: int = INVENTORY_LIMIT) -> dict:
    """Bound the scan and never follow an attached symlink."""
    if not root.is_dir():
        raise ValueError(f"input_root_missing: {root}")
    entries, errors, pending = [], [], [root]
    truncated = False
    while pending:
        directory = pending.pop()
        try:
            with os.scandir(directory) as children:
                for child in children:
                    if len(entries) >= limit:
                        truncated = True
                        break
                    path = Path(child.path)
                    item = {"path": path.relative_to(root).as_posix()}
                    try:
                        info = child.stat(follow_symlinks=False)
                        item["bytes"] = info.st_size
                        if child.is_symlink():
                            item["kind"] = "symlink"
                        elif child.is_dir(follow_symlinks=False):
                            item["kind"] = "directory"
                            pending.append(path)
                        elif child.is_file(follow_symlinks=False):
                            item["kind"] = "file"
                        else:
                            item["kind"] = "other"
                    except OSError as exc:
                        item["kind"] = "error"
                        errors.append({"path": item["path"], "reason": str(exc)})
                    entries.append(item)
        except OSError as exc:
            errors.append({"path": directory.relative_to(root).as_posix(), "reason": str(exc)})
        if truncated:
            break
    return {"root": str(root), "limit": limit, "truncated": truncated, "errors": errors,
            "entries": sorted(entries, key=lambda item: item["path"])}


def legacy_source_observations(root: Path, listing: dict) -> dict:
    """R1 observations are separate from admission of the synthetic R2 payload."""
    sources = []
    for item in listing["entries"]:
        path = root / item["path"]
        if item["kind"] != "file" or path.name != "SOURCE_COMMIT.txt" or item["bytes"] > 128:
            continue
        marker = path.read_bytes().decode("utf-8", errors="replace").strip()
        if marker != BASELINE_COMMIT:
            continue
        source = path.parent
        observed = {"root": str(source), "baseline_marker": marker, "paths": {}}
        for name in [GZIP_PATH, GZIP_PATH[:-3], NESTED_PATH, NESTED_PATH[:-4]]:
            candidate = source / name
            # Check every component so a symlinked fixtures directory is not followed.
            current = source
            linked = False
            for part in PurePosixPath(name).parts:
                current = current / part
                if current.is_symlink():
                    linked = True
                    break
            kind = "symlink" if linked else (
                "file" if candidate.is_file() else "directory" if candidate.is_dir() else "missing")
            observed["paths"][name] = {"kind": kind}
            if kind == "file":
                observed["paths"][name]["bytes"] = candidate.stat().st_size
        sources.append(observed)
    return {"status": "observed" if sources else "not_observed", "sources": sources,
            "complete_inventory": not listing["truncated"] and not listing["errors"],
            "interpretation": "Path observations only; no automatic recompression or source repair."}


def verify_zip(data: bytes, expected: dict[str, dict]) -> dict[str, bytes]:
    """Verify bounded member bytes without extracting an untrusted tree."""
    if len(data) > PAYLOAD_LIMIT or sum(item["bytes"] for item in expected.values()) > PAYLOAD_LIMIT:
        raise ValueError("archive_too_large: this is a tiny synthetic canary")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        infos = archive.infolist()
        names = [item.filename for item in infos]
        if len(names) != len(set(names)):
            raise ValueError("duplicate_archive_member")
        for item in infos:
            name = item.filename
            path = PurePosixPath(name)
            if (not name or "\\" in name or ":" in name or name.startswith("/")
                    or any(part in {"", ".", ".."} for part in name.split("/"))
                    or path.is_absolute()):
                raise ValueError(f"unsafe_archive_path: {name}")
            if stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError(f"archive_symlink: {name}")
        if set(names) != set(expected):
            raise ValueError(f"archive_member_set: missing={sorted(set(expected)-set(names))}; "
                             f"unexpected={sorted(set(names)-set(expected))}")
        members = {}
        for item in infos:
            wanted = expected[item.filename]
            if item.file_size != wanted["bytes"]:
                raise ValueError(f"archive_member_size: {item.filename}")
            content = archive.read(item)
            if sha256(content) != wanted["sha256"]:
                raise ValueError(f"archive_member_hash: {item.filename}")
            members[item.filename] = content
        return members


def verify_payload(path: Path, expected: dict) -> dict[str, bytes]:
    if path.is_symlink() or not path.is_file():
        raise ValueError("payload_not_regular_file")
    if expected["archive_bytes"] > PAYLOAD_LIMIT or path.stat().st_size != expected["archive_bytes"]:
        raise ValueError("payload_size_mismatch")
    data = path.read_bytes()
    if sha256(data) != expected["archive_sha256"]:
        raise ValueError("payload_hash_mismatch")
    return verify_zip(data, expected["members"])


def check_sqlite(path: Path) -> dict:
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro&immutable=1", uri=True)) as db:
        integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
        rows = db.execute("SELECT value FROM probe").fetchall()
        try:
            db.execute("INSERT INTO probe VALUES (8)")
        except sqlite3.OperationalError as exc:
            if "readonly" not in str(exc).lower():
                raise
        else:
            raise ValueError("sqlite_read_only_not_enforced")
    if integrity != "ok" or rows != [(7,)]:
        raise ValueError(f"sqlite_contents: integrity={integrity}, rows={rows}")
    return {"integrity": integrity, "rows": [[7]], "read_only_enforced": True}


def filesystem_probe(run: Path) -> dict:
    original, backup = run / "filesystem.sqlite", run / "filesystem-backup.sqlite"
    with closing(sqlite3.connect(original, timeout=1)) as db:
        journal = db.execute("PRAGMA journal_mode=WAL").fetchone()[0]
        db.execute("PRAGMA synchronous=FULL")
        synchronous = db.execute("PRAGMA synchronous").fetchone()[0]
        db.execute("CREATE TABLE probe (value INTEGER NOT NULL)")
        db.execute("INSERT INTO probe VALUES (7)")
        db.commit()
        with closing(sqlite3.connect(backup, timeout=1)) as destination:
            db.backup(destination)
    if journal != "wal" or synchronous != 2:
        raise ValueError(f"sqlite_settings: journal={journal}, synchronous={synchronous}")
    return {"journal_mode": journal, "synchronous": synchronous, "backup": check_sqlite(backup),
            "scope": "Small synthetic host diagnostic; actual worker recovery remains untested."}


def export_results(run: Path) -> tuple[Path, str]:
    names = ["canary-report.json", "summary.json", "input-inventory.json", "expected-manifest.json",
             "transport.sqlite", "filesystem.sqlite", "filesystem-backup.sqlite"]
    retained = [name for name in names if (run / name).is_file()]
    temporary, final = run / "canary-results.zip.partial", run / "canary-results.zip"
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in retained:
            archive.write(run / name, name)
    with zipfile.ZipFile(temporary) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(retained):
            raise ValueError("export_integrity_failed")
    temporary.replace(final)
    digest = sha256(final.read_bytes())
    (run / "canary-results.sha256").write_text(f"{digest}  {final.name}\n", encoding="utf-8")
    return final, digest


def run_canary(input_root: Path, output_root: Path, expected: dict) -> dict:
    input_root, output_root = Path(input_root).resolve(), Path(output_root).resolve()
    label = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-" + uuid.uuid4().hex[:8]
    run = output_root / ("recovery-m5-upload-canary-" + label)
    run.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    report = {"schema_version": 1, "kind": "synthetic-kaggle-transport-canary",
              "started_utc": datetime.now(timezone.utc).isoformat(), "output_directory": str(run),
              "expected_archive_sha256": expected["archive_sha256"], "stages": {},
              "legacy_source": {"status": "not_observed"}}
    write_json(run / "expected-manifest.json", expected)

    def stage(name, action):
        entry = {"status": "not_run", "reason": None}
        report["stages"][name] = entry
        before = time.monotonic()
        try:
            if before - started >= 60:
                raise TimeoutError("canary_deadline_reached")
            value = action()
        except (Exception, KeyboardInterrupt) as exc:
            entry.update(status="failed", reason=f"{type(exc).__name__}: {exc}")
            value = None
        else:
            entry["status"] = "passed"
        entry["elapsed_seconds"] = round(time.monotonic() - before, 6)
        write_json(run / "canary-report.json", report)
        return value

    def host_check():
        gpus = visible_gpu_devices()
        report["host"] = {"python": platform.python_version(), "os": platform.platform(),
                          "sqlite": sqlite3.sqlite_version, "input_root": str(input_root),
                          "visible_driver_gpu_entries": gpus,
                          "gpu_probe": "Driver directory only; no CUDA initialization or billing claim."}
        if gpus:
            raise ValueError("gpu_visible: set Kaggle accelerator to None and rerun on CPU")
        return True

    def input_check():
        listing = inventory(input_root)
        write_json(run / "input-inventory.json", listing)
        report["legacy_source"] = legacy_source_observations(input_root, listing)
        if listing["truncated"] or listing["errors"]:
            raise ValueError("input_inventory_incomplete: remove unrelated inputs or report the scan errors")
        return listing

    try:
        host_ready = stage("cpu_host", host_check)
        listing = stage("input_inventory", input_check)
        members = None
        if host_ready and listing is not None:
            def payload_check():
                candidates = [input_root / item["path"] for item in listing["entries"]
                              if item["kind"] == "file"
                              and Path(item["path"]).name == expected["payload_filename"]]
                if not candidates:
                    raise ValueError(f"payload_missing: expected {expected['payload_filename']}; "
                                     "see input-inventory.json for transformed or absent input")
                if len(candidates) != 1:
                    raise ValueError("payload_ambiguous: attach exactly one copy of the canary dataset")
                report["selected_payload"] = str(candidates[0])
                return verify_payload(candidates[0], expected)
            members = stage("transport_bytes", payload_check)
        else:
            report["stages"]["transport_bytes"] = {"status": "blocked", "reason": "cpu_host/input_inventory"}

        if members is not None:
            def compressed_check():
                with gzip.GzipFile(fileobj=io.BytesIO(members[GZIP_PATH])) as stream:
                    raw = stream.read(expected["gzip_decoded"]["bytes"] + 1)
                if len(raw) != expected["gzip_decoded"]["bytes"] or sha256(raw) != expected["gzip_decoded"]["sha256"]:
                    raise ValueError("gzip_decoded_bytes_mismatch")
                nested = verify_zip(members[NESTED_PATH], expected["nested_members"])
                (run / "transport.sqlite").write_bytes(nested["worker.sqlite"])
                report["compressed_contents"] = {"gzip_bytes_preserved": True, "nested_zip_bytes_preserved": True,
                                                  "nested_sqlite": check_sqlite(run / "transport.sqlite")}
                return True
            stage("compressed_contents", compressed_check)
        else:
            report["stages"]["compressed_contents"] = {"status": "blocked", "reason": "transport_bytes"}
        probe = stage("filesystem_backup", lambda: filesystem_probe(run))
        if probe is not None:
            report["filesystem"] = probe
    finally:
        required = ["cpu_host", "input_inventory", "transport_bytes", "compressed_contents", "filesystem_backup"]
        for name in required:
            report["stages"].setdefault(name, {"status": "not_run", "reason": "earlier interruption"})
        failures = [f"{name}: {entry['reason']}" for name, entry in report["stages"].items() if entry["status"] == "failed"]
        passed = all(report["stages"][name]["status"] == "passed" for name in required)
        summary = {"canary_checks_passed": passed, "root_blocker": failures[0] if failures else None,
                   "transport": "raw_payload", "payload_filename": expected["payload_filename"],
                   "model_generations": 0, "full_source_preparation": None, "model_smoke": None,
                   "legacy_source_status": report["legacy_source"]["status"],
                   "observed_wall_seconds": round(time.monotonic() - started, 6),
                   "provider_assignment_utc": None, "provider_release_utc": None,
                   "next_action": "Download this ZIP, stop the session, and return it for transport review."
                                  if passed else "Download this ZIP and return the failure report; keep the original payload unchanged."}
        report["summary"] = summary
        write_json(run / "canary-report.json", report)
        write_json(run / "summary.json", summary)
        try:
            result_zip, digest = export_results(run)
        except Exception as exc:
            report["export_error"] = f"{type(exc).__name__}: {exc}"
            write_json(run / "canary-report.json", report)
            result_zip, digest = None, None
    return {"report": report, "summary": summary, "run_directory": str(run),
            "zip_path": str(result_zip) if result_zip else None, "zip_sha256": digest}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root", type=Path, default=Path("/kaggle/input"))
    parser.add_argument("--output-root", type=Path, default=Path("/kaggle/working"))
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    result = run_canary(args.input_root, args.output_root, json.loads(args.manifest.read_text(encoding="utf-8")))
    print(json.dumps({key: value for key, value in result.items() if key != "report"}, indent=2))
    return 0 if result["summary"]["canary_checks_passed"] and result["zip_path"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
