"""Fallback source packet for the thesis notebook when GitHub is unreachable.

Usage: python scripts/build_thesis_source.py --commit <40-hex> --output DIR
Writes DIR/thesis-source-<sha12>.zip from `git archive` of that exact commit,
holding only recovery/, configs/ and pyproject.toml plus .source-commit and a
file-hash manifest. Attach it as a private Kaggle dataset.
"""

import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(commit, output):
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise SystemExit("--commit must be a full 40-character commit")
    # core.autocrlf=false keeps the committed bytes (as GitHub's archive does); a Windows checkout with
    # autocrlf would otherwise write CRLF files whose hashes no longer match the study binding.
    data = subprocess.run(["git", "-c", "core.autocrlf=false", "archive", "--format=tar", commit,
                           "recovery", "configs", "pyproject.toml"], cwd=ROOT, check=True, capture_output=True).stdout
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    target = output / f"thesis-source-{commit[:12]}.zip"
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data)) as tar, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as packet:
        for member in tar.getmembers():
            if member.isfile():
                content = tar.extractfile(member).read()
                files[member.name] = hashlib.sha256(content).hexdigest()
                packet.writestr(member.name, content)
        packet.writestr(".source-commit", commit)
        packet.writestr("source-manifest.json", json.dumps(dict(commit=commit, files=files), indent=1, sort_keys=True))
    print(f"{target} ({len(files)} files)")
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output", default=str(ROOT / "dist" / "thesis-source"))
    args = parser.parse_args()
    build(args.commit, args.output)
