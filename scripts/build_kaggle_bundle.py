"""Preserve the canonical M5 archive under the tested raw-payload suffix."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import stat
import zipfile


BASELINE_COMMIT = "ca46bcd55486b38bb453f5294e01f943bc7f7752"
SOURCE_ARCHIVE_SHA256 = "57f99508f47f5571769891e39603db0c2b15c99038e0a186f3e2d40a9d48622f"
PAYLOAD_NAME = "m5-kaggle-source.payload"
CHUNK = 1024 * 1024


def file_sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def archive_manifest(path: Path) -> dict:
    members = {}
    with zipfile.ZipFile(path) as archive:
        for entry in archive.infolist():
            # orig_filename retains separators/NULs hidden by ZipInfo on Windows.
            name = entry.orig_filename
            if (not name or name != entry.filename or "\\" in name or ":" in name
                    or name.startswith("/") or any(ord(char) < 32 for char in name)
                    or any(part in {"", ".", ".."} for part in name.split("/"))
                    or stat.S_ISLNK(entry.external_attr >> 16) or entry.is_dir()):
                raise ValueError(f"unsafe_source_member: {name}")
            if name in members:
                raise ValueError(f"duplicate_source_member: {name}")
            for parent in PurePosixPath(name).parents:
                if str(parent) in members:
                    raise ValueError(f"conflicting_source_member: {name}")
            if any(other.startswith(name + "/") for other in members):
                raise ValueError(f"conflicting_source_member: {name}")
            digest, size = hashlib.sha256(), 0
            with archive.open(entry) as stream:
                while data := stream.read(CHUNK):
                    digest.update(data)
                    size += len(data)
            if size != entry.file_size:
                raise ValueError(f"source_member_size: {name}")
            members[name] = {"bytes": size, "sha256": digest.hexdigest()}
        marker = archive.read("SOURCE_COMMIT.txt").decode("ascii").strip()
    if marker != BASELINE_COMMIT:
        raise ValueError("source_baseline_marker")
    return {"schema_version": 1, "kind": "canonical-m5-source",
            "transport": "raw_payload", "payload_filename": PAYLOAD_NAME,
            "source_baseline_commit": BASELINE_COMMIT,
            "archive_bytes": path.stat().st_size, "archive_sha256": file_sha256(path),
            "expanded_bytes": sum(x["bytes"] for x in members.values()),
            "members": dict(sorted(members.items()))}


def build(source: Path, output: Path, build_commit: str | None = None,
          *, expected_source_hash: str = SOURCE_ARCHIVE_SHA256) -> dict:
    if build_commit is not None and re.fullmatch(r"[0-9a-f]{40}", build_commit) is None:
        raise ValueError("build_commit must be a verified full Git commit or None")
    if output.exists():
        raise FileExistsError("Use a new directory; earlier bundles/evidence are never overwritten.")
    if source.is_symlink() or not source.is_file() or file_sha256(source) != expected_source_hash:
        raise ValueError("canonical_source_archive_hash")
    manifest = archive_manifest(source)
    manifest.update(build_commit=build_commit, build_python=platform.python_version())
    output.mkdir(parents=True, exist_ok=False)
    payload = output / PAYLOAD_NAME
    shutil.copyfile(source, payload)
    if file_sha256(payload) != manifest["archive_sha256"]:
        raise ValueError("copied_payload_hash")
    (output / "source-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-archive", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--build-commit")
    args = parser.parse_args()
    manifest = build(args.source_archive, args.output_dir, args.build_commit)
    print(json.dumps({k: manifest[k] for k in (
        "archive_bytes", "archive_sha256", "expanded_bytes", "build_commit")}, indent=2))


if __name__ == "__main__":
    main()
