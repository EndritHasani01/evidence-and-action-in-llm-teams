"""Quiescent SQLite backups, exact source transport and safe portable restore."""

import hashlib
from contextlib import closing
import json
from pathlib import Path, PurePosixPath
import shutil
import sqlite3
import stat
import tempfile
import zipfile

from .core import canonical
from .store import utc


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix+".partial")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False)+"\n", encoding="utf-8")
    temp.replace(path)


def inventory(root):
    return {p.relative_to(root).as_posix(): dict(bytes=p.stat().st_size, sha256=digest(p))
            for p in sorted(Path(root).rglob("*")) if p.is_file() and p.name != "integrity.json"}


def verify(root):
    root = Path(root)
    manifest = json.loads((root/"integrity.json").read_text())
    if inventory(root) != manifest["files"]:
        raise ValueError("bundle file inventory/bytes/hash differs")
    for slot in range(2):
        with closing(sqlite3.connect((root/f'worker-{slot}.sqlite').resolve().as_uri()+"?mode=ro", uri=True)) as db:
            if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("canonical snapshot failed integrity")
    return manifest


def export(run, stores, *, boundary, reports=True):
    """Caller holds the session action lock; no call is in flight on either writer."""
    from .report import write_report
    run = Path(run)
    if any(r["status"] == "admitted" for s in stores for r in s.rows("attempts")):
        # Unknown spending is allowed in a snapshot, but active calls are not.
        if any(s.meta("active_generation", False) for s in stores):
            raise ValueError("quiescent acknowledgement required from both writers")
    out = run/"exports"
    out.mkdir(exist_ok=True)
    if reports:
        write_report(run, run/"reports")
    with tempfile.TemporaryDirectory(prefix="i01-snapshot-", dir=out) as temp:
        bundle = Path(temp)
        for slot, store in enumerate(stores):
            store.backup(bundle/f"worker-{slot}.sqlite")
        for name in ("run.json",):
            shutil.copy2(run/name, bundle/name)
        for name in ("source", "reports", "receipts"):
            if (run/name).exists():
                shutil.copytree(run/name, bundle/name)
        attempts = sum(len(s.rows("attempts")) for s in stores)
        atomic_json(bundle/"integrity.json", dict(format="i01-portable-v1", boundary=boundary,
                    created_at=utc(), attempts=attempts, files=inventory(bundle)))
        receipt = verify(bundle)
        reopened = 0
        for slot in range(2):
            with closing(sqlite3.connect(bundle/f"worker-{slot}.sqlite")) as db:
                reopened += db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]
        if reopened != attempts:
            raise ValueError("snapshot attempt reconciliation differs")
        if reports:
            from .report import analysis
            if canonical(analysis(bundle)) != canonical(analysis(run)):
                raise ValueError("fresh-snapshot outcomes/costs/trace reconstruction differs")
        target = out/"latest.zip"
        partial = out/"latest.zip.partial"
        with zipfile.ZipFile(partial, "w", zipfile.ZIP_DEFLATED) as archive:
            for p in sorted(bundle.rglob("*")):
                if p.is_file():
                    archive.write(p, p.relative_to(bundle).as_posix())
        with zipfile.ZipFile(partial) as archive:
            if archive.testzip() is not None:
                raise ValueError("ZIP CRC failed")
        partial.replace(target)
        return dict(path=str(target), bytes=target.stat().st_size, sha256=digest(target),
                    boundary=boundary, created_at=receipt["created_at"], integrity="passed",
                    attempts=attempts, contents=list(receipt["files"]), browser_download_verified=False)


def extract_selected(selected, target, *, max_bytes=2**30):
    selected, target = Path(selected), Path(target)
    if target.exists() and any(target.iterdir()):
        raise ValueError("restore requires a fresh writable destination")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="i01-restore-", dir=target.parent) as temp:
        staging = Path(temp)
        if selected.is_file():
            with zipfile.ZipFile(selected) as archive:
                seen, total = set(), 0
                for item in archive.infolist():
                    name = PurePosixPath(item.filename)
                    total += item.file_size
                    if (item.filename in seen or name.is_absolute() or ".." in name.parts or
                        "\\" in item.filename or ":" in item.filename or
                        stat.S_ISLNK(item.external_attr >> 16) or total > max_bytes):
                        raise ValueError("unsafe, duplicate or oversized archive member")
                    seen.add(item.filename)
                if archive.testzip() is not None:
                    raise ValueError("ZIP CRC failed")
                archive.extractall(staging)
        elif selected.is_dir():
            if not (selected/"integrity.json").is_file():
                raise ValueError("select the exact verified expanded bundle root")
            if any(p.is_symlink() for p in selected.rglob("*")):
                raise ValueError("expanded restore cannot contain symbolic links")
            if sum(p.stat().st_size for p in selected.rglob("*") if p.is_file()) > max_bytes:
                raise ValueError("expanded bundle too large")
            shutil.copytree(selected, staging, dirs_exist_ok=True)
        else:
            raise ValueError("select one existing ZIP or verified expanded directory")
        receipt = verify(staging)
        target.mkdir(exist_ok=True)
        shutil.copytree(staging, target, dirs_exist_ok=True)
    return receipt
