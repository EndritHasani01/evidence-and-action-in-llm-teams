# Final-online-6: complete results and failure analysis

Date: 13 October 2026. Status: **actual 9B hardware diagnostics executed;
hardware rejected; 4B staging blocked by a software defect; no pilot or main results**.

This analysis reads the ten original files in
[final-online-6](../../notebooks/run/final-online-6), including the executed
[notebook](../../notebooks/run/final-online-6/notebook-exec.ipynb),
[results ZIP](../../notebooks/run/final-online-6/course-results.zip) and
[resume payload](../../notebooks/run/final-online-6/course-resume.payload).
All remain unchanged. The separate
[complete fix proposal](course-kaggle-final-online-6-proposal.md) describes work
that has not yet been implemented or GPU-tested.

## 1. What happened

The final-online-5 storage repair worked in this session. Kaggle selected writable
temporary storage, installed the pinned environment, verified ordinary installed
research modules, completed native CPU preflight, downloaded and verified the 9B
checkpoint, and ran actual Qwen3.5-9B inference on two distinct T4s.

The 9B hardware run stopped correctly after its first complete-input probe:
although generation finished within the new 600-second diagnostic deadline,
minimum observed free memory was only **17,629,184 bytes / 16.813 MiB**.
The approved acceptance rule requires **1,610,612,736 bytes / 1.5 GiB** throughout
the measured stress evidence. The 9B candidate did not pass this configuration's
hardware gate. Its second envelope probe and controlled cleanup probe were never
executed.

The workflow retained the failed candidate and selected the predeclared 4B
fallback. Before downloading or loading 4B weights, it raised:

```text
ValueError: pinned checkpoint byte inventory differs
```

That exception is a deterministic metadata-accounting bug, independently
reproduced on CPU. A second bug counted the 9B SQLite backup copies as new
physical attempts. It falsely set the 4B prior to 67 instead of 45. Fixing only
the checkpoint exception would leave the fallback with an incorrect allowance.

## 2. Evidence identity and integrity

| Check | Verified result |
|---|---|
| Branch inspected | `feat/course-m5-inference-preparation` |
| Submitted runtime source | `ae0b98f5774f6217fb2f2dfb8118ef0ac56c3afe` |
| Source manifest SHA-256 | `b5cfd116cd5e905a4b3cb3e6a972eaf96d289af0198f29a9ad0483a2ada1bc3a` |
| Executed notebook | All nine cell sources literally match the delivered final-online-5 notebook |
| Packaged runtime | All 85 source members match manifested byte counts and SHA-256 |
| Results ZIP | 72 members; CRC passes; 21,766,405 expanded bytes |
| Resume payload | 205 members; CRC passes; 63,191,077 expanded bytes |
| Worker evidence | Two canonical hardware databases and their two backups; all SQLite integrity checks pass |
| Backup contents | Calls, attempts, processes and saved inputs match canonical records; allocation rows predate observation closure |
| Standalone HTML/CSV/plotting files | Byte-identical to the corresponding saved 9B report exports |
| Final failure receipt | Identical across standalone `last-action.json`, results ZIP and resume payload |

The [machine-readable receipt](../../notebooks/validation/course-kaggle/final-online-6-analysis.json)
contains all original file hashes, every attempt's raw model text, evaluator-only
gold, validation, timing, memory summaries, process records and both CPU defect
reproductions. Source integrity establishes which code ran; it does not establish
scientific acceptance.

## 3. Setup and progression

All **13 recorded setup commands passed**, including `stage-pinned-checkpoint`.
The bootstrap receipt says `installed_verified=true`, `weights_staged=true` and
`status=prepared`. Its `gpu_execution=false` means the *setup command* does not
run inference; the subsequent hardware worker databases prove actual GPU work.

| Phase | Observed evidence |
|---|---|
| Observation clock | Starts `19:23:25 UTC` |
| Pinned dependency download | 78.384 seconds |
| Dependency installation | 87.937 seconds |
| Installed provenance | 17.119 seconds |
| Native hardware-plan contract | 7.719 seconds; CPU construction/processor checks |
| 9B checkpoint download | `19:26:59.592–19:34:16.554 UTC`; 436.962 seconds |
| Hardware execution | 21 ordinary diagnostics plus one full-envelope probe |
| Hardware observation closure | `19:54:37.716 UTC`; inference processes confirmed stopped |
| Limited 9B analysis | `19:54:40.312 UTC`; main outcomes remain unknown |
| Fallback error | `19:55:20.116 UTC`; metadata refusal before 4B weights/model calls |

Temporary scratch/cache were placed under
`/kaggle/temp/course-workspace-ae0b98f5774f/gpu-environment/scratch`.
Early admission measured about **1,069.89 GiB filesystem free**, with a calculated
34.22 GiB setup/checkpoint requirement. Output storage was a separate
`/kaggle/working` pool. Those are saved path-specific filesystem readings,
not a promise about Kaggle's session quota. There is no evidence of a disk
refusal in this run.

The notebook completed all five code cells without an uncaught notebook error.
Cell 7 intentionally converted the controller failure into an exported blocked
receipt; cell 9 still produced reports. A completed notebook execution therefore
does not mean the research finished. The final action is
`blocked_or_safely_stopped`, with no scientific gates bypassed.

## 4. Actual hardware and memory result

Three resident provider processes are recorded: the first device's ordinary
model, the second device's model, and the first device's restarted envelope
model. Their identities are:

- `GPU-ae85d40d-cf10-251e-1847-4c37e1bb42a8`
- `GPU-7af3c468-e6cf-675d-be5e-28bc570e4f60`

Both are actual Tesla T4s. The saved loader evidence identifies the immutable
9B revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`,
`Qwen3_5ForCausalLM`, `recovery_t4_sdpa`, CUDA 12.8, GPU-resident tensors and
empty missing/unexpected/mismatched/error loading lists. The native loading gate
passes. The recurrent fast path is recorded as disabled; this is an observed
implementation detail, not proof that enabling another kernel would fix the run.

| First envelope probe | Observed result |
|---|---|
| Input | 110,416 tokens; full reviewed bound |
| Output | All 256 forced diagnostic tokens |
| Resident bound with output reserve | 110,672 tokens |
| Attempt time | 394.043 seconds, including the attempt's recorded startup/generation interval |
| Diagnostic deadline | 600 seconds |
| Finite generation score steps | 256 |
| Fresh cache | Initially empty; same call-owned cache; disposed after call |
| Memory samples | 1,374 model-edge samples |
| Minimum device free | **0.0164 GiB** |
| End-of-generation free with cache | 2.2762 GiB |
| Peak PyTorch allocated | 10.7821 GiB |
| Peak PyTorch reserved | 14.4082 GiB |
| Peak occupied device memory derived from free/total | 14.5458 GiB |
| Hardware acceptance | **Failed** |

The final 2.2762 GiB reading does not override the much lower transient minimum.
At the lowest-free sample, allocated memory was 10,043,645,952 bytes while reserved
memory was 15,462,301,696 bytes. Allocator reservation contributes to pressure;
this evidence does **not** prove that weights alone require the entire device,
nor that every possible 9B implementation is infeasible. It rejects the tested
configuration under the approved measured-headroom rule. Altering allocator or
inference settings and requalifying 9B would be separate work requiring a valid
remaining scope and actual GPU evidence.

Ordinary diagnostics retained at least roughly 6.21 GiB free, even for the two
22k-token requests. Short-input success cannot substitute for full-input stress.
The envelope's forced repeated `a` output is a tensor/numerical diagnostic,
intentionally excluded from model-answer accuracy and protocol percentages.

All three provider-process records have confirmed stops and no uncertain stop.
That establishes inference quiescence. It does not establish Kaggle provider
deallocation; `provider_release_confirmed=false` remains accurate.

## 5. What the 21 ordinary attempts actually show

These are the fixed **hardware smoke diagnostics**, constructed from saved CPU
local-view witnesses. They are not the five-world first-90 capability run,
complete pilot, or main experimental trajectories. Each recorded outcome is
preserved exactly, including invalid or wrong answers.

| Attempt | Task / role | Input tokens | Output tokens | Protocol result | Seconds |
|---|---|---:|---:|---|---:|
| 01 | Top-k private shard | 1,233 | 249 | Invalid: prose 75 > 64 | 110.19 |
| 02 | Prefix-sum private shard | 1,217 | 116 | Valid | 16.13 |
| 03 | Difference-array private shard | 1,290 | 183 | Valid | 24.73 |
| 04 | Sort private shard | 1,224 | 150 | Valid | 20.76 |
| 05 | BFS private shard | 814 | 112 | Valid | 15.33 |
| 06 | Prefix-sum full-information control | 2,106 | 55 | Valid, wrong answer | 10.46 |
| 07 | Sort full-information control | 2,126 | 76 | Valid, wrong answer | 12.95 |
| 08 | Revised BFS full-information control | 1,224 | 39 | Valid, wrong answer | 6.58 |
| 09 | Top-k acquired-evidence witness | 2,614 | 179 | Valid | 26.24 |
| 10 | Prefix-sum acquired-evidence witness | 2,562 | 256 | Invalid: incomplete JSON at length limit | 35.21 |
| 11 | Difference-array acquired-evidence witness | 2,746 | 256 | Invalid: incomplete JSON at length limit | 35.56 |
| 12 | Sort acquired-evidence witness | 2,582 | 256 | Invalid: incomplete JSON at length limit | 35.34 |
| 13 | BFS acquired-evidence witness | 1,665 | 228 | Valid | 30.44 |
| 14 | Revised prefix-sum C, peer 0 | 2,169 | 256 | Invalid: incomplete JSON at length limit | 34.62 |
| 15 | Revised prefix-sum C, peer 1 | 2,169 | 256 | Invalid: incomplete JSON at length limit | 34.28 |
| 16 | Revised prefix-sum C, peer 2 | 2,173 | 203 | Invalid: prose 95 > 64 | 28.68 |
| 17 | Revised prefix-sum C, peer 3 | 2,173 | 256 | Invalid: incomplete JSON at length limit | 34.44 |
| 18 | Retained prefix-sum stress | 22,299 | 256 | Invalid: incomplete JSON at length limit | 72.73 |
| 19 | Retained sort Q_B stress | 22,318 | 256 | Invalid: incomplete JSON at length limit | 72.19 |
| 20 | Device-1 repeated prefix-sum request | 1,217 | 116 | Valid | 60.84 |
| 21 | Device-1 BFS request | 814 | 112 | Valid | 14.66 |

There are **11/21 valid replies (52.38%)**, eight length-ended malformed JSON
replies, and two prose-limit violations. All ordinary attempts completed before
their 120-second deadline. None has a recorded timeout, infrastructure failure,
retry, or uncertain completion. Median attempt time is 30.443 seconds; first-call
load/startup and unusually large requests make this a poor main-runtime forecast.

The existing exact evaluator finds **0/21 exact full assigned answers** when
grading these diagnostics against their original/revised saved worlds. Many
private-shard/witness requests intentionally lack complete current information,
so that denominator is not a capability estimate. The three full-information
controls are the clearest answer-quality warning:

- **Prefix sums:** the model returned the original input array, beginning
  `[6,2,9,4,8,4,…]`. Correct cumulative output begins `[6,8,17,21,29,33,…]`.
- **Sort:** it returned the original unsorted array, beginning `[24,72,62,92,…]`.
  Correct ascending output begins `[0,2,5,12,15,15,15,24,…]`.
- **Revised BFS:** it returned distances
  `{"0":0,"1":1,"2":1,"3":1,"4":2,"5":2,"6":2,"7":1}`.
  Correct distances are
  `{"0":0,"1":2,"2":1,"3":1,"4":2,"5":1,"6":1,"7":2}`.

These are syntactically valid wrong answers, not parser errors. Repairing their
values, sorting them, completing truncated JSON, increasing output caps, or
retrying wrong replies would change the approved experiment. No such action
was taken.

Replies 02/20 and 05/21 match exactly across the recorded device processes,
including raw output, settings and seed. That is useful limited repeat evidence,
not completion of the complete A/B/A/A restart matrix or universal determinism.

## 6. Why the 4B fallback crashed

The saved controller traceback follows this exact path:

```text
course_kaggle_workflow.py:1377 main
  -> run_qualification:1295 native_checkpoint_files(inspection)
  -> m5_course_smoke_assets.py:84
     sum(native LFS file sizes) != inspection.total_checkpoint_bytes
```

The 4B inspection populated `total_checkpoint_bytes` with **9,319,737,856**,
the native checkpoint index's tensor payload total. Actual shard files total
**9,319,828,096** bytes. The 90,240-byte difference consists exactly of their
Safetensors JSON headers and eight-byte header-length prefixes. The
[pinned checkpoint index](https://huggingface.co/Qwen/Qwen3.5-4B/raw/851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/model.safetensors.index.json)
and [official Safetensors format](https://github.com/safetensors/safetensors#format)
support that distinction.

| Pinned 4B shard | Tensor payload | Header + prefix | Native file size |
|---|---:|---:|---:|
| 00001 | 5,329,387,520 | 11,168 | 5,329,398,688 |
| 00002 | 3,990,350,336 | 79,072 | 3,990,429,408 |
| Total | **9,319,737,856** | **90,240** | **9,319,828,096** |

Small immutable Hub metadata and header-only HTTP range requests verified this
without downloading tensor bodies or loading a model. The
[metadata fixtures](../../notebooks/validation/course-kaggle/final-online-6-metadata/README.md)
retain both native shard hashes/sizes and the exact header receipts. The archived
inventory function reproduces the 4B exception using these offline fixtures;
the 9B inventory passes. Thus this is not evidence of corrupt model weights,
a changed revision, internet failure, or a need for another model.

The 4B native CPU hardware-plan/processor contract passed before this refusal.
There are **no 4B hardware databases, model attempts, or empirical GPU-fit results**.

## 7. Additional engineering defects and misleading summaries

1. **Backup double counting.** `qualification_choice` and the coordinator's
   cumulative summary use `worker-*.sqlite` plus `COUNT(*)`. That pattern includes
   `worker-0-backup.sqlite` and `worker-1-backup.sqlite`. Their 22 attempts duplicate
   the canonical 22, falsely producing `23 + 44 = 67`. The existing
   `smoke_attempt_usage` deduplicates `(call_id, number, started_at)` and correctly
   reports **23 historical + 22 new = 45**. The original selector reproducibly
   returns `("4B", 67)` on the submitted files. The 4B operator config persists
   the same incorrect prior. This would wrongly constrain later execution even
   after the inventory bug is fixed.
2. **Transition status lags the last failure.** Root `automatic-run.json` still
   says selected candidate 9B / limited headroom result. The 4B child config and
   traceback prove the workflow was preparing 4B when it failed. Preserve both
   candidate history and the latest active-stage failure in the coordinator
   summary.
3. **The plan is a construction snapshot.** All 24 rows in
   `executed-plan.json` retain `executed=false` and `outcome=null`, despite 22
   persisted outcomes. The databases, gate and live progress are authoritative.
   This filename/unused field combination misleads readers.
4. **Largest-request summary omits the envelope.** The hardware report says
   `largest_prepared_request_resident_tokens=22574`, taken from ordinary packet
   rows. The actually executed full-envelope request has **110,672** resident
   tokens. The gate uses the correct bound; the summary should derive its largest
   prepared/executed sizes from the real plan/ledger.
5. **Generic feasibility report omits the final fallback failure.** The exported
   HTML/CSV files reproduce the 9B main-scope limited report generated before
   4B failed. They accurately show unknown main data, but cannot replace the
   final controller traceback. Its independent main audit passes with **zero
   model calls checked**; that is not a passed pilot/model audit.

## 8. Accounting, populations and defensible claims

Canonical history is **45 physical preparation attempts**, not 67. The adopted
ceiling remains 71; the 4B candidate still has its own maximum of 24 new hardware
attempts. Its complete matrix would bring the cumulative total to at most **69**.
The two unused 9B matrix positions are not an extra 4B allowance.

The hardware receipt records 1.04008 aggregate GPU-hours over its bounded notebook
observation segment. The observation clock through the controller exception spans
1,915.116 seconds (31m55s). GPU-process setup, attempted work and idle intervals
are separately recorded. Startup inside an attempt can also appear in the setup
partition; summing attempt wall times and setup partitions again would double
count time. Earlier/later assignment time and actual provider release are unknown.
These observations do not prove total billed GPU-hours or remaining provider quota.

No development worker databases, `run.json`, accepted freeze, pilot gate, or main
worker databases exist. The full main manifest remains **0 recorded / 6,280
scheduled logical uses / 6,280 unknown**, corresponding to 5,752 scheduled distinct
generations over 20 worlds. The five-world pilot (1,114 distinct / 1,178 logical)
and first-90 qualification have not run. No primary causal contrast, treatment
effect, recovery success rate, empirical confidence interval, or policy-cost
comparison can be estimated from this run. Empty plots and null estimates are
missing evidence, not zero effects or negative experimental results.

The defensible result is: **this pinned 9B configuration loads and generates on
both T4s, but fails measured full-input headroom acceptance; its ordinary hardware
answers also show serious quality/protocol weaknesses; the authorized 4B fallback
remains untested because software refused valid checkpoint metadata.**

## 9. Reproduction and limits of this investigation

From the repository root:

```powershell
.venv/Scripts/python notebooks/validation/course-kaggle/analyse_final_online_6.py
```

The [read-only script](../../notebooks/validation/course-kaggle/analyse_final_online_6.py)
checks all manifested source bytes and original submissions, ZIP/SQLite integrity,
canonical/backup equivalence for calls and attempts, exact evaluator scores,
hardware memory/process evidence, notebook/report identity, absent experimental
stages, native header arithmetic, and both archived software failure boundaries.
It passed locally on CPU with **zero GPU calls, zero downloaded tensor bytes,
no scientific outcome writes and no production-code changes**. Reproduction uses
saved metadata and requires no network.

This investigation cannot certify 4B fit or capability, a successful future Kaggle
session, or absence of future provider/network/model errors. Those require the
unchanged empirical gates. The separate proposal addresses the observed bugs,
their missed integration boundaries, and safe continuation without discarding
evidence or repeating the rejected 9B matrix.
