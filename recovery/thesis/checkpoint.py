"""Portable checkpoints, newest-first restore and an optional private mirror.

Specification section 7.5. A checkpoint holds the canonical SQLite store
(backup API, taken under the store lock), the run inputs, receipts and a
manifest. Exports are written to a temporary name, verified by reopening, then
renamed; an interrupted export never replaces a good checkpoint.
"""

from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import sqlite3
import stat
import tempfile
import zipfile

from ..i01.archive import atomic_json, digest, inventory

FORMAT = "thesis-checkpoint-v1"
NAME = re.compile(r"^thesis-checkpoint-(?P<study>[A-Za-z0-9._-]+)-(?P<seq>\d{5})\.zip$")
ALLOWED_TOP = {"study.sqlite", "checkpoint.json", "inputs", "receipts"}
KEEP_LOCAL = 2


def utc():
    return datetime.now(timezone.utc).isoformat()


def name_for(study, seq):
    return f"thesis-checkpoint-{study}-{seq:05d}.zip"


def counts(db_path):
    with closing(sqlite3.connect(Path(db_path).resolve().as_uri() + "?mode=ro", uri=True)) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("checkpoint database failed integrity_check")
        episodes = [json.loads(s) for (s,) in db.execute("SELECT state FROM episodes")]
        return dict(attempts=db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0],
                    calls_with_outcome=db.execute("SELECT COUNT(*) FROM calls WHERE outcome IS NOT NULL").fetchone()[0],
                    episodes=len(episodes), terminal_episodes=sum(bool(e.get("terminal")) for e in episodes))


def export(run, store, *, study, session, reason, mirror=None, progress=print):
    """Write, verify and keep the newest two local checkpoints; mirror if configured."""
    run = Path(run)
    folder = run / "checkpoints"
    folder.mkdir(exist_ok=True)
    with store.transaction():
        row = store.db.execute("SELECT value FROM meta WHERE key='checkpoint_seq'").fetchone()
        seq = (json.loads(row[0]) if row else 0) + 1
        store.db.execute("INSERT OR REPLACE INTO meta VALUES ('checkpoint_seq', ?)", (json.dumps(seq),))
    final = folder / name_for(study, seq)
    with tempfile.TemporaryDirectory(prefix=".export-", dir=folder) as temp:
        bundle = Path(temp) / "bundle"
        bundle.mkdir()
        store.backup(bundle / "study.sqlite")
        for name in ("inputs", "receipts"):
            if (run / name).exists():
                shutil.copytree(run / name, bundle / name)
        row = store.db.execute("SELECT evidence FROM sessions WHERE id=?", (f"session/{session}",)).fetchone()
        closed = bool(row and json.loads(row[0]).get("closed"))  # lets a later restore tell a finished writer
        manifest = dict(format=FORMAT, study=study, seq=seq, parent_seq=seq - 1, session=session,
                        session_closed=closed, reason=reason, created_at=utc(), binding=store.meta("binding"),
                        counts=counts(bundle / "study.sqlite"), files=inventory(bundle))
        atomic_json(bundle / "checkpoint.json", manifest)
        partial = Path(temp) / (final.name + ".partial")
        with zipfile.ZipFile(partial, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(bundle.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(bundle).as_posix())
        verify(partial)
        partial.replace(final)
    for old in sorted(folder.glob(f"thesis-checkpoint-{study}-*.zip"))[:-KEEP_LOCAL]:
        old.unlink()
    receipt = dict(path=str(final), seq=seq, bytes=final.stat().st_size, sha256=digest(final),
                   created_at=manifest["created_at"], reason=reason, counts=manifest["counts"],
                   mirror=None, download_verified=False)
    if mirror is not None:
        try:
            receipt["mirror"] = mirror.upload(final)
        except Exception as error:  # the local copy stays valid; retry at the next checkpoint
            receipt["mirror"] = dict(uploaded=False, error=f"{type(error).__name__}: {error}")
            progress(f"[checkpoint] WARNING: mirror upload failed ({type(error).__name__}); local checkpoint kept")
    atomic_json(folder / "latest.json", receipt)
    return receipt


def _safe_members(archive, max_bytes):
    seen, total = set(), 0
    for item in archive.infolist():
        name = PurePosixPath(item.filename)
        total += item.file_size
        if (item.filename in seen or name.is_absolute() or ".." in name.parts or "\\" in item.filename
                or ":" in item.filename or stat.S_ISLNK(item.external_attr >> 16) or total > max_bytes
                or name.parts[0] not in ALLOWED_TOP):
            raise ValueError("unsafe, unexpected, duplicate or oversized checkpoint member: " + item.filename)
        seen.add(item.filename)


def verify(path, *, max_bytes=8 * 2**30):
    """Full verification: ZIP CRC, member safety, inventory hashes, SQLite integrity."""
    path = Path(path)
    with zipfile.ZipFile(path) as archive:
        _safe_members(archive, max_bytes)
        if archive.testzip() is not None:
            raise ValueError("checkpoint ZIP CRC failed")
        with tempfile.TemporaryDirectory(prefix="thesis-verify-") as temp:
            archive.extractall(temp)
            root = Path(temp)
            manifest = json.loads((root / "checkpoint.json").read_text(encoding="utf-8"))
            if manifest.get("format") != FORMAT:
                raise ValueError("not a thesis checkpoint")
            actual = {k: v for k, v in inventory(root).items() if k != "checkpoint.json"}
            if actual != manifest["files"]:
                raise ValueError("checkpoint file inventory differs")
            if counts(root / "study.sqlite") != manifest["counts"]:
                raise ValueError("checkpoint counts differ from its database")
    return manifest


def find(study, roots=(), mirror=None):
    """Every visible checkpoint of this study: attached inputs, local folders, mirror."""
    found = []
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        for path in root.rglob("thesis-checkpoint-*.zip"):
            match = NAME.match(path.name)
            if match and match["study"] == study:
                found.append(dict(seq=int(match["seq"]), location=str(path), origin="file", sha256=digest(path)))
    if mirror is not None:
        for entry in mirror.list(study):
            found.append(dict(entry, origin="mirror"))
    return sorted(found, key=lambda c: (c["seq"], c["origin"]))


def select(candidates):
    """Highest sequence; equal sequences must be byte-identical."""
    if not candidates:
        return None
    top = max(c["seq"] for c in candidates)
    best = [c for c in candidates if c["seq"] == top]
    if len({c["sha256"] for c in best if c.get("sha256")}) > 1:
        raise ValueError(f"two different checkpoints claim sequence {top} (concurrent sessions?): "
                         + ", ".join(c["location"] for c in best) + "; choose one explicitly")
    return next((c for c in best if c["origin"] == "file"), best[0])


def restore(path, run):
    """Extract a verified checkpoint into an empty run directory."""
    path, run = Path(path), Path(run)
    if (run / "study.sqlite").exists():
        raise ValueError("restore requires a run directory without a study store")
    manifest = verify(path)
    run.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path) as archive:
        _safe_members(archive, 8 * 2**30)
        with tempfile.TemporaryDirectory(prefix=".restore-", dir=run) as temp:
            archive.extractall(temp)
            for name in ("study.sqlite", "inputs", "receipts"):
                source = Path(temp) / name
                if source.is_dir():
                    shutil.copytree(source, run / name, dirs_exist_ok=True)
                elif source.exists():
                    shutil.copy2(source, run / name)
    (run / "checkpoints").mkdir(exist_ok=True)
    shutil.copy2(path, run / "checkpoints" / path.name)
    return manifest


class DirectoryMirror:
    """A folder used as the off-session copy (tests, or a manually synced drive)."""

    def __init__(self, folder):
        self.folder = Path(folder)

    def upload(self, path):
        self.folder.mkdir(parents=True, exist_ok=True)
        target = self.folder / Path(path).name
        shutil.copy2(path, target)
        if digest(target) != digest(path):
            raise ValueError("mirror copy differs")
        return dict(uploaded=True, location=str(target), sha256_verified=True)

    def list(self, study):
        return [dict(seq=int(m["seq"]), location=str(p), sha256=digest(p))
                for p in sorted(self.folder.glob(f"thesis-checkpoint-{study}-*.zip"))
                if (m := NAME.match(p.name)) and m["study"] == study]

    def fetch(self, location, destination):
        Path(destination).mkdir(parents=True, exist_ok=True)
        target = Path(destination) / Path(location).name
        shutil.copy2(location, target)
        return target


def _git_blob_id(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


class HubMirror:
    """Private Hugging Face dataset; refuses a public repository."""

    def __init__(self, repo, token, api=None):
        if not repo or not token:
            raise ValueError("mirror needs a repository name and the HF_TOKEN secret")
        if api is None:
            from huggingface_hub import HfApi
            api = HfApi(token=token)
        self.repo, self.api = repo, api
        self.api.create_repo(repo, repo_type="dataset", private=True, exist_ok=True)
        if not self.api.repo_info(repo, repo_type="dataset").private:
            raise ValueError(f"{repo} is public; checkpoints are only mirrored to a private dataset")

    def upload(self, path):
        """Upload, then confirm the remote bytes: LFS SHA-256, or the Git blob hash for a small file."""
        path = Path(path)
        remote = f"checkpoints/{path.name}"
        self.api.upload_file(path_or_fileobj=str(path), path_in_repo=remote, repo_id=self.repo,
                             repo_type="dataset", commit_message=f"checkpoint {path.name}")
        info = self.api.get_paths_info(self.repo, [remote], repo_type="dataset")
        if not info or getattr(info[0], "size", None) != path.stat().st_size:
            raise ValueError("mirror size differs from the local checkpoint")
        sha = getattr(getattr(info[0], "lfs", None), "sha256", None)
        if sha is not None and sha != digest(path):
            raise ValueError("mirror SHA-256 differs from the local checkpoint")
        blob = None
        if sha is None and getattr(info[0], "xet_hash", None) is None and getattr(info[0], "blob_id", None):
            blob = info[0].blob_id
            if blob != _git_blob_id(path):
                raise ValueError("mirror Git blob hash differs from the local checkpoint")
        return dict(uploaded=True, location=f"{self.repo}:{remote}", sha256_verified=sha is not None,
                    content_verified=sha is not None or blob is not None)

    def list(self, study):
        remotes = [remote for remote in self.api.list_repo_files(self.repo, repo_type="dataset")
                   if (m := NAME.match(remote.rsplit("/", 1)[-1])) and m["study"] == study]
        infos = {i.path: i for i in self.api.get_paths_info(self.repo, remotes, repo_type="dataset")} if remotes else {}
        return [dict(seq=int(NAME.match(remote.rsplit("/", 1)[-1])["seq"]), location=remote,
                     sha256=getattr(getattr(infos.get(remote), "lfs", None), "sha256", None))
                for remote in remotes]

    def fetch(self, location, destination):
        from huggingface_hub import hf_hub_download
        return Path(hf_hub_download(self.repo, location, repo_type="dataset", local_dir=destination,
                                    token=self.api.token))
