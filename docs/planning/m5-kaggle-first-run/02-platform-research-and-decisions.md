# Platform research, decisions and remaining questions

Research date: 8 October 2026. Current documentation and metadata were consulted read-only. No provider session, upload, environment installation or weight download was started. The evidence classifications below distinguish documented behavior, this run's observations, static inference and pending experiments.

## What the platform contract actually promises

| Topic | Primary evidence | Consequence for this project |
|---|---|---|
| Dataset archive processing | Kaggle documents extraction of uploaded archives while preserving directories. [Dataset documentation](https://www.kaggle.com/docs/datasets) | An outer ZIP upload is not a byte-preserving archive-storage contract. Nested gzip/ZIP behavior for this exact upload still needs an inventory or canary. |
| CLI upload options | Official CLI documents `--keep-tabular` for tabular conversion and `--dir-mode` for directory upload handling. [Dataset commands](https://github.com/Kaggle/kaggle-cli/blob/main/docs/datasets.md) | Neither option is a documented general switch to preserve every nested archive byte. Do not present it as the fix without an experiment. |
| Saved output and rerun behavior | Kaggle describes up to 20 GB of saved working output and says Save & Run All uses a separate execution session. [Notebook documentation](https://www.kaggle.com/docs/notebooks) | Separate scratch from retained output. Saving by executing can repeat inference and allocation; use a verified export path that does not run the study twice. |
| GPU settings and stopping | NVIDIA describes selecting T4 x2 and stopping the GPU session after work. [NVIDIA Kaggle guidance](https://docs.nvidia.com/datascience/deployment/latest/platforms/kaggle/) | User settings were sufficient in the first run. Provider release still needs external acknowledgement; model-process exit is insufficient. |
| Image source | Kaggle publishes CPU and GPU image build sources. [Kaggle image repository](https://github.com/Kaggle/docker-python) | Image names alone are not an accepted lock. Record the actual interpreter, Torch build, imports, wheels and device facts. |

Kaggle documentation pages expose limited body text through the browsing interface; relevant indexed official text and accessible official repository documentation were used. No account-specific quota, scratch hard limit, pricing, availability or persistence behavior was inferred from a general documentation page. The actual run is stronger evidence for this session's device/software facts than a forum post or an older image description.

## Environment research

A venv created with `--system-site-packages` exposes all base packages. The first notebook therefore proposes an overlay, rather than an isolated candidate closure, when base Torch is reusable. A full `pip check` in that overlay may include unrelated inherited packages. That is a latent reproducibility risk; this run did not reach installation and did not demonstrate such a conflict. [Python venv documentation](https://docs.python.org/3.13/library/venv.html), [pip check documentation](https://pip.pypa.io/en/stable/cli/pip_check/).

Prefer a clean candidate environment on scratch. The official CUDA 12.8 index contains a Linux x86-64, CPython 3.13 `torch-2.11.0+cu128` wheel. This aligns with the observed build instead of needlessly replacing it with CUDA 12.6. Wheel availability is not proof that the quantized Qwen path passes. [Official CUDA 12.8 Torch index](https://download.pytorch.org/whl/cu128/torch/).

bitsandbytes 0.49.2 supplies `bitsandbytes-0.49.2-py3-none-manylinux_2_24_x86_64.whl`; its documented CUDA 12.8–12.9 Linux targets include `sm75`. The observed glibc 2.39 and T4 capability are compatible candidates for that wheel family. Native import and a bounded tiny NF4 operation still require the actual environment. [Pinned installation guide](https://huggingface.co/docs/bitsandbytes/v0.49.2/en/installation), [release metadata](https://pypi.org/pypi/bitsandbytes/0.49.2/json).

The eleven root package release metadata records were fetched from PyPI without installing them. Their Python requirements admit Python 3.13; root wheel formats are pure Python, CPython 3.13, ABI3, or the generic Python Linux bitsandbytes wheel. This is not a full transitive wheel audit. In particular, native dependencies such as `pydantic-core`, `sqlite-vec`, `numpy`, `uuid-utils`, and Torch's CUDA runtime closure need the actual resolver's platform result.

Transformers 5.12.0 declares Hub >=1.5,<2 and tokenizers >=0.22,<=0.23.0. The reviewed Hub 1.19.0/tokenizers 0.22.2 roots satisfy those ranges; observed Kaggle tokenizers 0.23.1 cannot simply be combined with the older Transformers pin. LangGraph 1.2.12 accepts checkpoint >=4.1,<5 and Core >=1.4.7,<2, while the SQLite saver requires checkpoint >=4.1,<5. Preserve the reviewed roots first and let a clean resolver expose any concrete closure failure. [Transformers metadata](https://pypi.org/pypi/transformers/5.12.0/json), [LangGraph metadata](https://pypi.org/pypi/langgraph/1.2.12/json), [SQLite saver metadata](https://pypi.org/pypi/langgraph-checkpoint-sqlite/3.1.1/json).

Use pip's dry-run/install report to record resolved requirements, wheel URLs and hashes, followed by actual imports and `pip check`. Freeze the installed transitive closure only after it passes. Do not package-copy a populated venv between CPU/GPU sessions: venvs contain interpreter/path assumptions; stage compatible wheel artifacts or recreate it. [pip install documentation](https://pip.pypa.io/en/stable/cli/pip_install/), [Python venv documentation](https://docs.python.org/3.13/library/venv.html).

## Exact pinned model file research

Read-only Hub metadata was fetched with `blobs=true` for both immutable revisions. Selected files are the index-named shards plus `config.json`, `tokenizer.json`, `tokenizer_config.json`, `chat_template.jinja`, and `model.safetensors.index.json`. No `generation_config.json` appears at these revisions; the adapter already constructs an explicit fresh generation configuration.

| Candidate | Revision | Shards | Exact shard bytes | Exact selected-file bytes |
|---|---|---:|---:|---:|
| 9B | `c202236235762e1c871ad0ccb60c8ee5ba337b9a` | 4 | 19,306,310,880 | 19,319,226,111 = 17.9924314 GiB |
| 4B | `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` | 2 | 9,319,828,096 | 9,332,739,901 = 8.6917914 GiB |

Retain the following shard checks in the future staging manifest; suffixes below follow the common `model.safetensors-` prefix and `.safetensors` extension:

| Model / shard suffix | Bytes | LFS SHA-256 |
|---|---:|---|
| 9B / `00001-of-00004` | 5,276,436,216 | `db6f444b43d318c92f360a13a25561a6a65b10c0631b8ed305a426dbaa6c380e` |
| 9B / `00002-of-00004` | 5,335,161,512 | `31c7d7e2dd5d207840b31cc59083c8f4c4718959149e0358c0364052bb9a0330` |
| 9B / `00003-of-00004` | 5,368,717,440 | `7ec36ba3a4176a44c3c0876ad80c56a2f70c84bf008d82e9501df642f17dadec` |
| 9B / `00004-of-00004` | 3,325,995,712 | `b62b0c4cd7e44edee103ee8f4fe225f246d5e768e07bfd5f25b63a8aa1fdd0c6` |
| 4B / `00001-of-00002` | 5,329,398,688 | `26a93f066e1916adb13453dae5a0c707c0fbc71299ed98779571a907b8e74c61` |
| 4B / `00002-of-00002` | 3,990,429,408 | `cb544bd9bfae93dc59b0f22b292f5933573854a7f9b97835c67060d7d910e188` |

These sums come from the [9B pinned metadata](https://huggingface.co/api/models/Qwen/Qwen3.5-9B/revision/c202236235762e1c871ad0ccb60c8ee5ba337b9a?blobs=true) and [4B pinned metadata](https://huggingface.co/api/models/Qwen/Qwen3.5-4B/revision/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a?blobs=true). They improve on tensor-payload estimates but do not include environment installations, temporary transfers, duplicate caches, source extraction, ZIP creation or worker growth.

The 9B selected files alone exceed this run's final working free space by about 2.45 GiB, before artifact reserves. Storing both candidates there would require about 26.68 GiB before anything else. NF4 is an in-memory quantization choice and does not reduce these original downloads. No evidence warrants changing models solely to avoid that disk-layout problem.

The pinned Hub client supports revision selection, file filtering, dry-run metadata and configurable download locations. Choose one explicit cache/local snapshot strategy and audit partial-transfer/double-copy behavior; do not rely on default home-directory caches. [Hub 1.19.0 file-download documentation](https://huggingface.co/docs/huggingface_hub/v1.19.0/en/package_reference/file_download).

## Bounded remaining research

| ID | Question and minimal experiment | Required evidence / stop condition |
|---|---|---|
| R1 | What happened to the first dataset's `.gz` and nested `.zip` members? Export the actual relevant input inventory in CPU mode, or compare the dataset file listing with the original manifest. | Names, sizes, dataset version and transformed counterparts. Until then, keep automatic nested extraction an inference. |
| R2 | Can one archive payload survive upload exactly? CPU canary: outer ZIP with a tiny gzip and nested ZIP, uploaded as a single renamed `.payload`; compare its exact SHA-256 and extracted member bytes. | One retained file with the expected bytes. If the server still processes it, test base64 ASCII delivery instead and ship only the passing transport. No GPU needed. |
| R3 | Does the complete reviewed closure resolve/install on Linux/Python 3.13? Run resolver report and imports in a clean venv; test imports from installed code outside the source directory. | Full package/wheel records, `pip check`, maintained Qwen text-class and native tokenizer checks. Change only roots implicated by an actual failure, and repeat affected checks. |
| R4 | What scratch quota and lifecycle apply to the actual account/image? Inspect mount/stat facts and account documentation; stage the required files in CPU mode with exact byte verification. | Planned files successfully resident, remaining space/reserves recorded. Pool free space or a tiny write probe alone is insufficient. |
| R5 | Which private save/export action retains output without executing it again? CPU canary creates a small file/SQLite backup, saves using the proposed action, then retrieves it from a fresh session and the local machine. | Matching hashes, reopened SQLite and exact action/version identifiers. If saving reruns cells or drops output, use independently downloaded verified backups as the primary path. |
| R6 | Can allocation assignment/release and account quota units be recorded? Capture session-start bound, both device intervals and external stop acknowledgement; inspect the displayed terms. | Complete or explicitly bounded allocation intervals. Unknown stop time remains unknown; quota entitlement does not prove a scientific budget. |
| R7 | Does the smoke's longest legal request cover the required live envelope? Compare materialized B/Q requests with the retained bound, prove coverage or tighten the bound using the existing tokenizer/capacity machinery. | A reviewed bound/request relationship; no arbitrary padding, dropped text or natural-output assumptions. This is a prerequisite to full model-memory acceptance. |
| R8 | Are maintained SDPA/recurrent/NF4 paths viable on T4? Static review predicts a mask-free GQA math-fallback risk; tiny T4 probes must compare actual 16/4-head dispatch with explicit KV expansion before model loading. Then inspect the admitted model smoke. | Actual eligibility/kernel/mask paths, precision, language-weight diagnostics, finite outputs, peak memory and latency. If an attention compatibility change is needed, review a maintained/public route and reopen affected gates; no optional/custom CUDA kernel. |
| R9 | Can attempt/retry admission honor the short screen? Scripted dry-run of prepared smoke calls, retry exhaustion, timeout and remaining-time stops against existing attempt/allocation rows. | No 25th physical attempt, deadline overshoot or fabricated outcome; confirmed child exits. A missing narrow admission hook is an implementation issue, not a reason to widen the budget. |
| R10 | Will durable evidence fit beyond smoke? Measure actual worker/checkpoint/backup growth during the accepted pilot and extrapolate complete schedule plus export overlap. | A storage forecast with uncertainty and restore plan before main admission. A one-GiB smoke artifact allowance is not a complete main-storage forecast. |

R1–R6 can be resolved during preparation. R7 requires focused capacity review before model admission. The SDPA part of R8 is now an urgent small-library GPU prerequisite, explained in [the feasibility plan](04-model-feasibility-and-smoke.md#sdpa-dispatch-is-a-separate-runtime-risk); its remaining model observations stay within smoke. R9 is primarily scripted/CPU work. R10 belongs to pilot/freeze planning and must not delay the immediate source repair.

## Provider decision

Continue with Kaggle while R2–R6 have workable answers: the actual T4 pair and compatible-looking CUDA build are available, and the present failure concerns packaging. Prefer CPU staging of source/environment/model assets, followed by a short GPU verification/smoke. A fresh GPU image must recreate and verify its environment rather than assume CPU persistence.

If Kaggle cannot preserve verified input, keep scratch within real limits, provide a reproducible candidate environment, export/restore workers, or confirm release within the budget, collect the failed contract and compare another T4 host. The comparison must preserve one full replica per T4, actual memory, local WAL/FULL storage, durable off-host export, complete allocation accounting and the same scientific gates. Current price/availability/terms would require new primary-source research at that point. No alternative provider, paid reservation or platform migration is selected in this plan.

If the blocker is model/context feasibility on a single T4, changing the website does not solve it. Follow the specified 4B fallback and uniform size rules only when their gates apply; retain failed-configuration evidence and the limited-evidence path if none passes.
