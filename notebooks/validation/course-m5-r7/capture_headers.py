"""Read only bounded safetensors headers; never read or stage tensor payloads."""

import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
import re
import struct
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[3]
MAX_HEADER = 512 * 1024


def read_range(url, start, end, opener=urlopen):
    request = Request(url, headers={"Range": f"bytes={start}-{end}", "Accept-Encoding": "identity"})
    with opener(request, timeout=45) as response:
        match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", response.headers.get("Content-Range", ""))
        if (response.status != 206 or not match
                or tuple(map(int, match.groups()[:2])) != (start, end)
                or response.headers.get("Content-Encoding", "identity") != "identity"):
            raise ValueError("server did not honor exact metadata range; body not read")
        count = end - start + 1
        content = response.read(count)
        if len(content) != count:
            raise ValueError("incomplete metadata range")
        return content, dict(start=start, end=end, file_bytes=int(match[3]), status=206, bytes_read=count)


def header(url, opener=urlopen):
    length_bytes, first = read_range(url, 0, 7, opener)
    length = struct.unpack("<Q", length_bytes)[0]
    if not 2 <= length <= MAX_HEADER or 8 + length > first["file_bytes"]:
        raise ValueError("safetensors header length outside metadata-only bound")
    body, second = read_range(url, 8, 7 + length, opener)
    if first["file_bytes"] != second["file_bytes"]:
        raise ValueError("checkpoint size changed between ranges")
    json.loads(body)  # Validate JSON, retaining exact original metadata bytes.
    prefix = length_bytes + body
    return dict(url=url, file_bytes=first["file_bytes"], header_bytes=length,
        prefix_base64=base64.b64encode(prefix).decode("ascii"),
        prefix_sha256=hashlib.sha256(prefix).hexdigest(), ranges=[first, second])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("retain old evidence; use a fresh output")
    inspection = json.loads((ROOT/"notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json").read_bytes())
    rows = {}
    for name in inspection["checkpoint_index"]["shard_files"]:
        if Path(name).name != name or not name.endswith(".safetensors"):
            raise ValueError("unexpected checkpoint shard name")
        url = f"https://huggingface.co/{inspection['model']}/resolve/{inspection['revision']}/{name}"
        rows[name] = header(url)
    result = dict(model=inspection["model"], revision=inspection["revision"], headers=rows,
        checkpoint_index_sha256=inspection["checkpoint_index"]["sha256"],
        downloaded_metadata_bytes=sum(8+r["header_bytes"] for r in rows.values()),
        tensor_payload_bytes_read=0, model_weights_staged=False, gpu_execution=False,
        scope="Exact length prefixes and JSON headers only. Shapes/dtypes/offsets are metadata, not loaded language weights.")
    with args.output.open("xb") as stream:
        stream.write(gzip.compress(json.dumps(result, sort_keys=True).encode("utf-8"), mtime=0))
    print(json.dumps({k:v for k,v in result.items() if k != "headers"}, indent=2))


if __name__ == "__main__":
    main()
