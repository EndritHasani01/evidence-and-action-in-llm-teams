# Actual Kaggle T4 compatibility run 6

Reviewed 9 October 2026 against the [delivered notebook and plan](m5-t4-compatibility.md). **The standalone library diagnostic passes on both physical T4s:** six stages, 14 finite/reference-matched attention cases, four finite/reference-matched NF4 matmuls and four clean command exits. The [independent review](../../notebooks/validation/m5-t4-compatibility-run-6/validation.json) verifies original source, package bytes, dispatch traces, ZIP receipt and off-host snapshots. **No repeat GPU compatibility run is requested.** No pretrained weights or model generations ran; full-candidate/model/headroom acceptance and M5-T02 remain open.

## Artifact and source verification

| Supplied artifact | Bytes | SHA-256 |
|---|---:|---|
| [Executed notebook](../../notebooks/run/6/notebook-exec.ipynb) | 96,106 | `ee5f8b1c80f02ea8110f3b9381ac3456bb4737991cda002d5f60383e86b283bd` |
| [Result ZIP](../../notebooks/run/6/preflight-results.zip) | 42,834 | `332237aa5b5b73b39bce42dc7ac98c7434bbea15148019b96dd615022c997a96` |

The first six cell sources exactly match the delivered notebook. Code counts are 1–3 with no cell errors; the seventh cell is empty and unexecuted. Embedded program/helper/config/wheel inputs match source checkpoint `79ae1169e8a1a1e79c58171ce855535348b3db16`; the archived program is exact. The 23-member ZIP has 268,136 expanded bytes, safe allowlisted paths, good CRCs and the same hash as the notebook's printed receipt. All supplied bytes remain unchanged.

The [review script](../../notebooks/validation/m5-t4-compatibility-run-6/review_run.py) parses notebook literals without executing cells, independently checks all 85 staged file hashes against the real pinned Linux wheel, cross-checks each device receipt with its command and report, derives dispatch from operator names and checks CUDA kernel traces. It runs locally with `python -X utf8 notebooks/validation/m5-t4-compatibility-run-6/review_run.py`; [stdout](../../notebooks/validation/m5-t4-compatibility-run-6/review.stdout.txt) records acceptance and stderr is empty. This is an off-host artifact review, not another GPU run or a new scientific regression.

## Actual hardware and library observations

Host: Python **3.13.15**, Linux 6.18.48+, glibc 2.39; Torch **2.11.0+cu128**, CUDA build **12.8**, driver **580.178.04**. Both workers see exactly one device with capability **7.5** and match their distinct physical UUIDs:

- GPU 0: `GPU-ddddfa14-2a47-edfd-6d1a-c649a466d2fb`.
- GPU 1: `GPU-b908c8b9-fb0d-3032-e3d4-36c5ba908698`.

The private verified bitsandbytes **0.49.2** package and `libbitsandbytes_cuda128.so` load from owned scratch on both workers. Torch comes from the recorded host installation. Host software has **33 differences** from the 88-package CPU candidate; host Transformers is 5.16.1, not the candidate's 5.12.0. This probe neither imports that Transformers helper nor accepts the full scientific model environment. Its public Torch calls match the reviewed head/mask semantics; full candidate integration must be checked later.

## Attention and quantization findings

Both T4s have the same observed results for the tiny batch-one 16-query/4-KV-head, dimension-256 geometry:

| Case | Actual backend | Maximum absolute error against CPU FP32 |
|---|---|---:|
| Causal prefill, native GQA | math | 0.0003750324 |
| Causal prefill, repeated K/V | efficient | 0.0004026890 |
| Causal prefill, repeated K/V, forced efficient | efficient | 0.0004026890 |
| Explicit causal mask, repeated K/V | efficient | 0.0004026890 |
| Single-query decode, native GQA | math | 0.0000509247 |
| Single-query decode, repeated K/V | efficient | 0.0000730604 |
| Single-query decode, repeated K/V, forced efficient | efficient | 0.0000730604 |

All cases are finite and match at `rtol=0.02, atol=0.002`, with CUDA traces present. Efficient cases contain the actual `fmha_cutlassF_f16_aligned_32x128_gmem_sm75` kernel; GQA cases contain `aten::_scaled_dot_product_attention_math`. Public eligibility agrees: efficient accepts repeated heads and rejects unequal heads; Flash/cuDNN are ineligible on this hardware. Retained debug warnings explain those reasons. No unsupported forced case or CUDA failure occurred. Timing is not used to infer dispatch or predict model throughput.

Both devices also pass NF4/double quantization with FP16 weights/computation, block size 64 and the synthetic 128-by-256 weight. Batch-eight and single-row outputs match that same dequantized weight at `rtol=0.02, atol=0.01`; maximum absolute errors are **0.0001215339 / 0.0002491474**. These are four synthetic matmuls, not four language calls or capability outcomes.

The previously predicted small-tensor GQA math fallback is now observed. This establishes a supported efficient alternative at the tested shapes, **not an implemented model attention fix**. Review a maintained/public integration and its causal/mask/cache semantics before long model prefill. Do not silently change backend settings or count a successful tiny kernel as T02 acceptance.

## Memory, timing and persistence limits

Each device's `nvidia-smi` inventory reports **15 GiB** total, while Torch reports **14.56219482421875 GiB** (15,636,037,632 bytes) usable total. Retain both observations; no cause is inferred for their difference. Tiny-probe peaks are **12,161,024 allocated bytes / 25,165,824 reserved bytes** on each device; post-probe free memory is **14.39727783203125 GiB**. These are tiny-library measurements, not worst-context model peaks. Complete model memory must use the relevant native/free measurements and include the required 1.5-GiB headroom.

R7 remains unresolved. At the conservative 262,144 resident-token assumption, the existing conditional subtotals are 14.0390625 / 10.23876953125 GiB for 9B/4B. A fully materialized repeated-K/V temporary adds another 4 GiB for one active full-attention layer. That implementation's conditional subtotals become **18.0390625 / 14.23876953125 GiB**, before omitted memory, versus only **13.06219482421875 GiB** after native total minus required headroom. This shows why copying the tiny repeated-K/V path into a model is insufficient as a memory argument. It does not prove a legal view attains the cap or that either model has empirically failed. No cap/retention/fallback changes are made.

The recorded first-cell-to-pre-export workflow lasts **38.664189147 seconds**, giving a lower bound of **77.328378294 aggregate GPU-seconds** for two assigned devices. Device commands take 23.676 / 11.195 seconds and both exit before their 60-second limits, in serial order with confirmed process-group cleanup. Download/inventory also exit cleanly. Warmup/profile/import time is included; none is a language-call timing measurement.

The user reports the GPU session **is stopped**, describes the run as fast and offers a rerun. No rerun is needed. Exact allocation duration, provider assignment/release timestamps and earlier spending remain unknown. The notebook's conditional 1,080-GPU-second ceiling depends on unverified start/stop discipline and is **not a verified allocation total**. Preserve this uncertainty for shared resource reconciliation; another run cannot recover the old interval.

Both closed synthetic SQLite copies independently reopen off-host with integrity `ok`, row `7`, rejected writes and unchanged bytes. The backup hash matches its exported receipt. Source/wheel/device/library/persistence facts pass for this diagnostic scope; a full model lock, Qwen loading/recurrent/isolation, complete-envelope headroom, exact smoke requests, capability/pilot/freeze and main results remain later gates.

## Handoff

Measured-evidence checkpoint: `0f9407f`. T01 stays done, T02 stays blocked, and progress stays **21 done/eight blocked**. Keep GPU allocation stopped; no further user execution is requested by this review. Next complete **offline review of the supported attention integration and R7 memory coverage**, then prepare verified full-candidate/model staging and exact bounded smoke admission. Reuse the actual run-6 findings instead of repeating accepted tiny diagnostics.

The [handoff audit](../../notebooks/validation/m5-t4-compatibility-run-6/handoff-validation.json) passes **334 local references in 12 documents**, all **29 task states**, exact bytes for **448 earlier notebook/evidence files** and all **479 files at the run-6 evidence checkpoint**, including **22 supplied-run files**. Both canonical payload versions equal the original archive; scientific/operational/root diffs are empty. It independently confirms the conditional repeated-K/V/native-memory arithmetic and syntax of the two review scripts. The pre-existing user edit retains SHA-256 `c071fbb83438a9831b073fd80da4d60f92eed3d5945674d2f84fbd8348b55dca` and remains unstaged. No publication or GPU execution is performed locally.
