# Kaggle host preflight follow-up

Recorded 8 October 2026 for [M5-T02](../todos/M5/M5-T02-hardware-smoke-and-host-validation.md).
The [T01 adapter and CPU evidence](../todos/M5/M5-T01-inference-and-allocation-preparation.md#completion-and-handoff)
are complete. The user authorized GPU-host preparation and reported available
quota. The first run supplied two-T4/CUDA inspection but failed source admission;
the [actual CPU canary](m5-kaggle-upload-canary-run-2.md) then passed transport checks.
The [actual full-source run 3](m5-kaggle-full-preparation-run-3.md) then verified
all 143 members and Linux process cleanup, but failed inside `ensurepip` before
installation/tests. The next CPU run validates the repaired bootstrap and candidate;
actual model/host acceptance remains unexecuted. The existing [smoke packet](m5-inference-preparation.md)
and scientific resource limits still apply across accounts and configurations.

## Recommended notebook

Use [recovery_m5_kaggle_preflight_v3.ipynb](../../notebooks/recovery_m5_kaggle_preflight_v3.ipynb)
and reuse the accepted private dataset `m5-kaggle-source-v2` with its unchanged
`m5-kaggle-source.payload`. No new upload is needed. Import the notebook privately,
attach that dataset, select **Accelerator: None**, enable **Internet**, and Run All.
Download `preflight-results.zip` and the executed notebook, stop the session, and
return both under `notebooks/run/4/`. Fixed defaults need no cell edits.

The [bootstrap repair evidence and handoff](m5-kaggle-pip-bootstrap-repair.md)
record 25 passing operational checks, a real isolated pinned-pip installation,
and exact-v3 local Jupyter valid/missing-source exports. The notebook uses a clean
venv without `ensurepip`, verifies the pinned pip wheel, then requests the unchanged
88-package candidate install and 81 focused plus 16 native checks on Linux.
Actual Kaggle installation and model acceptance remain pending. The original
notebook and ZIP are retained as first-run evidence; the manual GPU inspection
cell below is historical and is not the next preparation action.

## Reported CPU notebook

These values came from the user's output, not an accepted inference host:

| Item | Reported value |
|---|---|
| Python / OS / SQLite | 3.13.15 / Linux 6.18.48+, x86_64, glibc 2.39 / 3.45.1 |
| Free disk | 19.5 GiB |
| torch / transformers / accelerate | 2.11.0+cpu / 5.16.1 / 1.14.0 |
| bitsandbytes | Not installed |
| tokenizers / huggingface-hub / pydantic | 0.23.1 / 1.29.0 / 2.13.5 |
| langgraph / checkpoint / SQLite saver / langchain-core | 1.2.11 / 4.2.0 / not installed / 1.6.1 |

The reported stack differs from the reviewed candidate. Python 3.13 is eligible
under the package's `>=3.11` declaration but is unverified for this project.
Inspected PyPI release metadata supplies compatible Python 3.13 Linux/universal
wheels for Transformers 5.12.0, bitsandbytes 0.49.2 and tokenizers 0.22.2.
The [official CUDA 12.6 torch index](https://download.pytorch.org/whl/cu126/torch/)
also lists the Python 3.13 torch 2.11.0 wheel. Driver/device compatibility and
the complete candidate environment still need actual host checks. Choose the
CUDA build after inspecting the GPU image; the CPU package is not a GPU build.

The pinned [9B checkpoint index](https://huggingface.co/Qwen/Qwen3.5-9B/resolve/c202236235762e1c871ad0ccb60c8ee5ba337b9a/model.safetensors.index.json)
declares 19,306,216,416 tensor bytes (17.98 GiB) across four shards. The reported
19.5 GiB therefore leaves about 1.5 GiB before shard headers, packages, caches
and experiment artifacts. NF4 loading reduces GPU storage, not these source
downloads. Inspect the actual GPU host's writable filesystems before fetching
weights; no storage or 9B/4B feasibility decision has been made.

## First GPU cell

Keep the notebook private. Select Settings -> Accelerator -> GPU T4 x2 as in
[NVIDIA's Kaggle instructions](https://docs.nvidia.com/datascience/deployment/latest/platforms/kaggle/).
Record when assignment starts, run the following cell once, and retain its
printed output. It inspects packages, devices and disk without downloading
weights or constructing a model. Its timestamp is inspection time, not proof
of allocation start.

```python
import json, os, platform, shutil, sqlite3, subprocess
from datetime import datetime, timezone
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path

info = {
    "inspection_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(), "os": platform.platform(),
    "sqlite": sqlite3.sqlite_version, "packages": {}, "filesystems": {},
}
for name in ["torch", "transformers", "accelerate", "bitsandbytes",
             "tokenizers", "huggingface-hub", "pydantic", "langgraph",
             "langgraph-checkpoint", "langgraph-checkpoint-sqlite", "langchain-core"]:
    try:
        info["packages"][name] = version(name)
    except PackageNotFoundError:
        info["packages"][name] = "not installed"
for path in ["/", "/tmp", "/kaggle/working", "/kaggle/input"]:
    if Path(path).exists():
        info["filesystems"][path] = {
            "device": os.stat(path).st_dev,
            "free_gib": round(shutil.disk_usage(path).free / 2**30, 2),
        }
try:
    result = subprocess.run([
        "nvidia-smi",
        "--query-gpu=index,uuid,name,driver_version,memory.total,memory.free",
        "--format=csv,noheader,nounits",
    ], capture_output=True, text=True, timeout=30)
    info["nvidia_smi"] = {
        "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
    }
except (FileNotFoundError, subprocess.TimeoutExpired) as error:
    info["nvidia_smi"] = {"error": str(error)}
try:
    import torch
    info["torch_runtime"] = {
        "version": torch.__version__, "cuda_build": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "device_count": torch.cuda.device_count(),
        "compiled_architectures": torch.cuda.get_arch_list(),
    }
except Exception as error:
    info["torch_runtime"] = {"error": repr(error)}
report = json.dumps(info, indent=2)
print(report)
if Path("/kaggle/working").is_dir():
    output = Path("/kaggle/working") / (
        "m5_gpu_host_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json"
    )
    with output.open("x", encoding="utf-8") as stream:
        stream.write(report + "\n")
    print("Saved:", output)
```

Stop the session after inspection and record provider release while the
environment and request preparation proceed. Inspection, loading and assigned
idle devices all count under the existing conservative smoke allowance;
separate reservations or accounts do not reset it. The source of truth remains
the actual retained allocation intervals. Send the output and assignment/release
observations to continue with the specific CUDA/package setup.

## Portable source preparation

The local handoff bundle is `dist/m5-kaggle-preflight.zip`, an ignored derived
export. It contains the committed `recovery/`, `tests/`, `configs/`, package
metadata and authority/orientation documents, plus `SOURCE_COMMIT.txt` with
the existing Git revision. `metadata/9B/` and `metadata/4B/` each contain only
the five pinned config/tokenizer/template/index files. No language weights,
credentials or mutable experiment workers are included. There is no new
identity or persistence layer. Uploading this bundle is a later private input
preparation step; no provider upload has occurred locally.

The ten metadata files were compared byte-for-byte with the two immutable
upstream revisions on 8 October. Bundle integrity, exported source equality,
the copied native tokenizer checks and documentation checks are recorded below.
The actual Kaggle installation, WAL/FULL/process/backup checks, request
materialization, disk/download strategy and measured T4 smoke remain pending.

## Local handoff verification

This original export verification is retained as historical evidence. The
export is 109,248,341 bytes (104.2 MiB), with 143 entries. Its source revision
is `ca46bcd55486b38bb453f5294e01f943bc7f7752`; the current follow-up changes only
documentation. `ZipFile.testzip()` passed, all 132 exported source files equal
`git archive` bytes, and all ten copied metadata files equal the reviewed local
files. The archive contains no weight shards, `.env` files or live `.sqlite` files.
It was extracted outside the checkout to
`C:\Users\EndritHasani\AppData\Local\Temp\recovery-kaggle-export-ai2ltopg`.

Executed from that extracted root on Windows/Python 3.11.9:

| Check | Command / environment | Result |
|---|---|---|
| Exported inference contracts | Checkout `.venv` Python: `-m unittest tests.test_inference_preparation tests.inference_checks -q` | 27 passed / 9.267 s |
| Copied 9B native metadata | Global Python: `-m tests.tokenizer_inference --tokenizer metadata/9B` | Four passed / 0.247 s |
| Copied 4B native metadata | Global Python: `-m tests.tokenizer_inference --tokenizer metadata/4B` | Four passed / 0.242 s |
| Copied native capacity | Global Python: `-m tests.tokenizer_capacity --tokenizer metadata/9B` | Eight passed / 1.848 s; maxima remain 261,388 / 259,868 including reserve |
| Documentation | All five changed documents' local paths/anchors; inspection-cell compile; `git diff --check` | 178 links/anchors and syntax/whitespace checks passed |

The native environment uses torch 2.11.0, Transformers 5.12.0, Accelerate 1.14.0,
bitsandbytes 0.49.2, tokenizers 0.22.2 and huggingface-hub 1.19.0, with Pydantic
2.12.5. Native checks do not construct a model or validate SQLite persistence;
the global environment has no SQLite saver and is not an accepted inference lock.
The capacity test's deliberate overflow tokenizer warning is expected and its
guard test passed. No source/scientific configuration changed. None of these
local export checks accepts the Kaggle GPU host.
