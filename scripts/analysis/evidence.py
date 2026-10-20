"""Read immutable study archives without importing the experiment runtime."""
from contextlib import closing, contextmanager
import hashlib
import json
from pathlib import Path, PurePosixPath
import sqlite3
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS = ("preliminary-experiment", "assisted-experiment")


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_copies():
    manifest = json.loads((ROOT / "scripts/analysis/support/manifest.json").read_text("utf-8"))
    for entry in manifest["immutable_files"]:
        path = ROOT / entry["release_path"]
        if path.stat().st_size != entry["bytes"] or digest(path) != entry["sha256"]:
            raise ValueError(f"Preserved file differs: {entry['release_path']}")
    return len(manifest["immutable_files"])


def extract_archive(archive, destination):
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zipped:
        names = zipped.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate archive members")
        for info in zipped.infolist():
            path = PurePosixPath(info.filename)
            target = destination.joinpath(*path.parts).resolve()
            if path.is_absolute() or ".." in path.parts or "\\" in info.filename or not target.is_relative_to(destination):
                raise ValueError(f"Unsafe archive member: {info.filename}")
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zipped.read(info))
    integrity = json.loads((destination / "integrity.json").read_text("utf-8"))
    actual = {p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file()}
    if actual != set(integrity["files"]) | {"integrity.json"}:
        raise ValueError("Archive inventory differs from its original integrity record")
    for name, expected in integrity["files"].items():
        path = destination / name
        if path.stat().st_size != expected["bytes"] or digest(path) != expected["sha256"]:
            raise ValueError(f"Archive integrity mismatch: {name}")
    run = json.loads((destination / "run.json").read_text("utf-8"))
    for name, expected in run["source_identity"].items():
        if digest(destination / "source" / name) != expected:
            raise ValueError(f"Frozen scientific source differs: {name}")
    return destination


@contextmanager
def checkpoints():
    verify_copies()
    with tempfile.TemporaryDirectory(prefix="llm-recovery-offline-") as directory:
        yield {name: extract_archive(ROOT / "experiments" / name / "kaggle-results.zip", Path(directory) / name)
               for name in EXPERIMENTS}


def read_checkpoint(directory):
    directory = Path(directory)
    run = json.loads((directory / "run.json").read_text("utf-8"))
    calls, episodes = {}, {}
    attempts = []
    for worker in range(2):
        uri = (directory / f"worker-{worker}.sqlite").as_uri() + "?mode=ro&immutable=1"
        with closing(sqlite3.connect(uri, uri=True)) as db:
            if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("SQLite integrity check failed")
            for cid, request, outcome in db.execute("SELECT id,request,outcome FROM calls"):
                if cid in calls:
                    raise ValueError(f"Duplicate canonical call: {cid}")
                calls[cid] = {"request": json.loads(request), "outcome": json.loads(outcome) if outcome else None}
            episodes.update((eid, json.loads(state)) for eid, state in db.execute("SELECT id,state FROM episodes"))
            attempts.extend(db.execute("SELECT call_id,status,number FROM attempts"))
    return run, calls, episodes, attempts


def derived_destination(value):
    path = Path(value).resolve()
    if path == ROOT or ROOT.is_relative_to(path):
        raise ValueError("Derived output must be separate from source files")
    for name in ("experiments", "report", "scripts", "results/assisted-experiment", "results/preliminary-experiment"):
        protected = (ROOT / name).resolve()
        if path == protected or path.is_relative_to(protected):
            raise ValueError("Derived output must be separate from preserved evidence")
    path.mkdir(parents=True, exist_ok=True)
    return path
