"""Pinned model files: metadata for CPU checks, weights only for GPU stages.

Generalizes recovery.i01.setup.download to the two adopted systems. Every file
is checked against the Hub's recorded size and SHA-256 (or Git blob hash); a
cache hit never substitutes for verification.
"""

import hashlib
import json
from pathlib import Path
import shutil
from time import monotonic

from ..i01.archive import atomic_json, digest
from . import load_config

METADATA = {"config.json", "generation_config.json", "tokenizer.json", "tokenizer_config.json",
            "chat_template.jinja", "vocab.json", "merges.txt", "model.safetensors.index.json",
            "special_tokens_map.json", "preprocessor_config.json", "processor_config.json"}


def download(model, scratch, receipts, *, weights, config=None, progress=print):
    """Download and verify; returns the local snapshot directory and file hashes."""
    from huggingface_hub import HfApi, snapshot_download
    config = config or load_config()
    entry = config["models"][model]
    scratch, receipts = Path(scratch), Path(receipts)
    cache = scratch / "hf-cache"
    cache.mkdir(parents=True, exist_ok=True)
    info = HfApi().model_info(entry["repo"], revision=entry["revision"], files_metadata=True)
    if info.sha != entry["revision"]:
        raise ValueError(f"{model}: pinned revision differs from the Hub response")
    files = [f for f in info.siblings if f.rfilename in METADATA or weights and f.rfilename.endswith(".safetensors")]
    if weights and not any(f.rfilename.endswith(".safetensors") for f in files):
        raise ValueError(f"{model}: weight shard inventory missing")
    needed = sum(f.size or 0 for f in files)
    free = shutil.disk_usage(scratch).free
    if free < needed + 2 * 2**30:
        raise ValueError(f"{model}: needs {needed:,} bytes plus a 2 GiB reserve; scratch free {free:,}")
    started = monotonic()
    progress(f"[assets] {model}: {len(files)} pinned files, {needed / 2**30:.2f} GiB ({'with' if weights else 'without'} weights)")
    snapshot = None
    for attempt in range(3):
        try:
            snapshot = Path(snapshot_download(entry["repo"], revision=entry["revision"], cache_dir=cache,
                                              allow_patterns=[f.rfilename for f in files], max_workers=4,
                                              etag_timeout=30))
            break
        except Exception as error:  # transport errors; partial files are reused and re-verified
            if attempt == 2:
                raise
            progress(f"[assets] transport retry {attempt + 1}/2 after {type(error).__name__}")
    verified = {}
    for number, f in enumerate(files, 1):
        path = snapshot / f.rfilename
        if path.stat().st_size != f.size:
            raise ValueError(f"{model}: byte size differs for {f.rfilename}")
        actual = digest(path)
        if f.lfs is not None:
            if actual != f.lfs.sha256:
                raise ValueError(f"{model}: LFS hash differs for {f.rfilename}")
        else:
            blob = hashlib.sha1(b"blob " + str(f.size).encode() + b"\0" + path.read_bytes()).hexdigest()
            if blob != f.blob_id:
                raise ValueError(f"{model}: Git blob hash differs for {f.rfilename}")
        verified[f.rfilename] = dict(bytes=f.size, sha256=actual)
        if f.size and f.size > 2**28:
            progress(f"[assets] verified {number}/{len(files)} {f.rfilename} ({f.size / 2**30:.2f} GiB)")
    receipt = dict(model=model, repo=entry["repo"], revision=entry["revision"], snapshot=str(snapshot),
                   weights=weights, files=verified, total_bytes=needed, seconds=round(monotonic() - started, 1),
                   model_attempts=0)
    atomic_json(receipts / f"assets-{model}-{'weights' if weights else 'metadata'}.json", receipt)
    progress(f"[assets] {model}: verified in {receipt['seconds']} s")
    return receipt


def files_digest(receipt):
    return hashlib.sha256(json.dumps(receipt["files"], sort_keys=True).encode()).hexdigest()
