# Tiny T4 compatibility notebook: preparation and local verification

Delivered 9 October 2026 for [M5-T02 preparation](../todos/M5/M5-T02-hardware-smoke-and-host-validation.md). The [next-step plan](../planning/m5-kaggle-first-run/07-t4-compatibility.md) is implemented in the [ready notebook](../../notebooks/recovery_m5_kaggle_t4_compatibility.ipynb). Actual run 5's 97 CPU checks already pass; no repeat CPU preflight is requested. **Actual T4 results are pending.** T02 remains blocked by its GPU/model/resource criteria; progress remains 21 done/eight blocked.

## What this step answers

The probe tests seven tiny attention cases on each physical T4: causal FP16 prefill and single-query decode with native GQA versus repeated K/V, an explicit causal mask, and forced memory-efficient dispatch. It records public eligibility reasons, profiled operator/backend names and available CUDA kernel traces, plus finite comparisons with a CPU FP32 reference. An expected unavailable forced backend is a retained negative observation; other CUDA failures stop admission. Unknown dispatch remains unknown.

It also tests synthetic 128-by-256 NF4/double-quantized FP16 weights with batch-eight and single-row inputs, comparing against the same dequantized weights. These are library operations, with **zero pretrained weights or model generations**. Conditional arithmetic from both pinned configs is retained separately; complete-envelope memory acceptance remains unknown.

This is a standalone library environment: require host Linux x86-64/Python 3.13 and Torch **2.11.0+cu128**, record its observed package differences, and extract only the exact **bitsandbytes 0.49.2** wheel into owned scratch. No pip installation, base-environment change, copied CPU venv or attached source dataset is needed. Its 60,651,714 compressed bytes and 184,269,948 expanded bytes are independently verified. Each fresh child sees one physical UUID before Torch import and verifies the extracted bytes, visible device and imported native-library origins. `-I -B` prevents environment Python overrides and bytecode changes between workers.

This does not establish the full scientific model lock, actual Qwen attention/recurrent behavior, full-envelope headroom or model smoke. The later model environment must repeat affected GPU checks. No attention adapter, backend selection, fallback selection, cap, package pin, scientific source or frozen configuration changes here. R7 remains unresolved; this implements the small-operator portion of R8.

## Exact user action

1. Import [recovery_m5_kaggle_t4_compatibility.ipynb](../../notebooks/recovery_m5_kaggle_t4_compatibility.ipynb) into a **new private Kaggle notebook**. Attach no dataset.
2. Select **Internet On / GPU T4 x2** when ready; start **Run All within one minute** of GPU assignment. If already allocated longer, stop and report that interval before running.
3. Run once. A host mismatch or failed check exports its first diagnostics; retain that result without a retry.
4. Download the results ZIP and the executed notebook with outputs, then **stop the GPU session immediately**. Avoid Save & Run All, which can execute again.
5. Put both files under `notebooks/run/6/` and report the displayed allocation duration and whether the GPU session is stopped.

The 360-second controller deadline includes a 90-second export reserve. Owned commands are bounded; an unconfirmed process cleanup blocks further device work. Reserve 120 seconds for retrieval/stopping, with at most 60 seconds before the first cell. Under that discipline, two assigned devices have a conditional upper bound of **1,080 GPU-seconds / 0.3 aggregate GPU-hour**. This is not a measured provider interval or a fresh smoke allowance. All setup, idle and prior spending count within the existing shared limits; account changes do not reset them. The observed first-cell-to-pre-export duration is reported separately, while actual provider start/release and earlier spending remain unknown.

## Executed local validation

Environment: Windows/Python **3.11.9**, installed Torch **2.11.0+cpu** and bitsandbytes **0.49.2**. No actual T4 execution or Linux native-library import occurred locally.

| Executed check | Result and evidence |
|---|---|
| `python -X utf8 -S -m unittest tests.test_t4_compatibility tests.test_kaggle_preflight tests.test_kaggle_bundle -v` | **42 passed, zero skipped**, [raw stderr](../../notebooks/validation/m5-t4-compatibility/verified-tests.stderr.txt). Covers host/build/UUID, wheel/hash/path/origin, refusal/deadline/cleanup, machine JSON versus noisy streams, conditional arithmetic, repeated execution and immutable builder guards. Two actual isolated import children retain identical package bytes. |
| `python -X utf8 -m unittest tests.t4_cpu_operators -v` | **Four passed, zero skipped**, [raw stderr](../../notebooks/validation/m5-t4-compatibility/verified-cpu-operators.stderr.txt). Real five-case automatic SDPA comparisons, independent decode/causal matrix formulas and NF4/double-quantized FP16 API/results. Deprecation warnings are retained; CPU operations do not prove CUDA dispatch. |
| Exact shipped cells in real Jupyter: actual host refusal | **Three code cells, counts 1–3, zero cell errors**. Refuses Windows before GPU inventory/download, then exports a six-member ZIP. [Executed notebook](../../notebooks/validation/m5-t4-compatibility/kernel/actual-host-refusal/executed.ipynb). |
| Exact shipped cells in real Jupyter: controlled complete workflow | **Five code cells, counts 1–5, zero cell errors**, including a clearly marked validation-only controls cell and repeated-run assertion. Real pinned wheel bytes/CRC/extraction verify 85 files; external Linux/GPU/download receipts are controlled. Repeated run starts no new command. Exports 23 members. [Executed notebook](../../notebooks/validation/m5-t4-compatibility/kernel/controlled-complete/executed.ipynb). |
| Independent off-host export review | Both ZIP receipts/CRCs/safe allowlisted members pass. Four copied synthetic SQLite snapshots reopen with integrity `ok`, row `7` and rejected writes. Both summaries retain null model/provider/full-envelope acceptance. [Kernel validation](../../notebooks/validation/m5-t4-compatibility/kernel/validation.json). |
| Actual canonical-config arithmetic | [Static envelope](../../notebooks/validation/m5-t4-compatibility/static-envelope.json) verifies original config hashes and reproduces conditional 9B/4B subtotals **14.0390625 / 10.23876953125 GiB**, including 8-GiB full-attention KV at the cap. Omitted memory and legal attainability remain explicit. |

The first arithmetic test used an incorrect expected 4B literal; a later test required Linux process-group status from a normally exited Windows child. Corrected assertions pass in the complete suite; both original failures remain in [implementation validation](../../notebooks/validation/m5-t4-compatibility/implementation-validation.json). Scientific settings and the existing shared helper did not change. The Jupyter checks pass on their first execution.

## Build and preservation

Planning checkpoint: `7f61fc7`. Implemented source checkpoint: **`79ae1169e8a1a1e79c58171ce855535348b3db16`**. The [builder](../../scripts/build_t4_compatibility_notebook.py) requires its source, probe, shared helper, wheel audit and selected-wheel table to match the recorded commit, refuses overwriting any existing notebook and embeds the original immutable config bytes. Generated artifact: six cells, three code cells, valid nbformat/syntax, empty shipped outputs/counts; SHA-256 **`9e9d87e3c703b7d3656ad5cf385a554ed5b12134d3a84fb0e8294c7e982afa24`**.

Probe source SHA-256 `ae6f5f945f4df06a5f23b7274f4c0670afe90a9bc001251004740fdd86ac4567`; unchanged operational helper SHA-256 `cc28a9d43ff1fd5051c7e5bfd5fdcc1154a5d85f019ef1a00dda7f3ae5fceaf8`. Scientific baseline remains `ca46bcd55486b38bb453f5294e01f943bc7f7752`. To reproduce, run `python -X utf8 -m scripts.build_t4_compatibility_notebook --notebook <new-path.ipynb>` from that source checkpoint. The delivery-review script accepts `--evidence-directory notebooks/validation/m5-t4-compatibility/kernel-new` to preserve existing evidence; it requires the delivered notebook and audited Linux wheel retained under ignored `build/`.

The [handoff audit](../../notebooks/validation/m5-t4-compatibility/handoff-validation.json) passes **319 local references in 11 documents**, all **29 task states**, exact bytes for **388 earlier notebook/evidence files including 20 supplied-run files**, unchanged shared-helper/root files and an empty protected scientific diff. Both canonical payload versions match the original archive; the existing user edit retains SHA-256 `c071fbb83438a9831b073fd80da4d60f92eed3d5945674d2f84fbd8348b55dca` and remains unstaged. The reviewer's initial operational-helper checkpoint and payload-path assertions were corrected; their failed JSON records remain as `initial-handoff-validation.json` and `payload-path-handoff-failure.json`. These are reviewer errors, not notebook or scientific failures.

Earlier notebooks/returned results, canonical source payload and important root files are retained. Local commits do not publish or run the notebook. After returned run 6, review its actual library/provenance/allocation observations; resolve R7 and any attention change before K11–K14 asset staging, exact smoke requests, admission and model execution.
