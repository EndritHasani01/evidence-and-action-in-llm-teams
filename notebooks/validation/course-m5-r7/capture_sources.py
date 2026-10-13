"""Retain inspected public library sources; no model assets or network calls."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("retain old evidence; use a fresh output")
    manifest = json.loads((args.directory/"manifest.json").read_bytes())
    sources = {}
    for name, row in manifest.items():
        if Path(name).name != name:
            raise ValueError("source filename must be local")
        content = (args.directory/name).read_bytes()
        if len(content) != row["bytes"] or hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise ValueError(f"inspected source differs: {name}")
        sources[name] = dict(**row, source=content.decode("utf-8"))
    archive = dict(sources=sources, scope="Pinned public library source inspection only; no model weights or CUDA execution.")
    with args.output.open("xb") as output:
        output.write(gzip.compress(json.dumps(archive,sort_keys=True,ensure_ascii=True).encode(),mtime=0))
    print(json.dumps(dict(sources=len(sources),source_bytes=sum(r["bytes"] for r in sources.values()),
                         archive_bytes=args.output.stat().st_size,gpu_execution=False)))


if __name__ == "__main__":
    main()
