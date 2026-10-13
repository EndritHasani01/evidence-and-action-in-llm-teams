# final-online-5: storage diagnosis and complete repair proposal

The submitted Run All stopped in cell 7, after successful dependency installation
and before checkpoint download or model loading. The immediate blocker is the
package's filesystem admission check. The later Kaggle screenshot shows substantial
session-level disk capacity, so **the evidence does not establish that the entire
session ran out of storage**. The failed check discarded the path-specific readings
needed to reconcile those observations. Repair storage placement, admission,
diagnostics and setup reuse together; do not remove scientific gates or change models
to hide a setup failure.

This is an investigation and implementable proposal, not another repaired upload.
No production behavior, scientific configuration, frozen settings or execution
allowance changes here. The existing final-online-4 packet remains the current
delivery and should not be represented as repaired for this failure.

## 1. Verified incident and scientific scope

The [read-only diagnostic](../../notebooks/validation/course-kaggle/analyse_final_online_5.py)
and [executed CPU receipt](../../notebooks/validation/course-kaggle/final-online-5-analysis.json)
verify all four original files in [the submitted folder](../../notebooks/run/final-online-5/).
Both submitted archives and the nested preflight archive pass CRC checks. All 85
source members match their manifest, bound to
`4deee720e0f2bee12f5331cc933d542083a05f78`. Executed notebook code matches the
delivered final-online-4 notebook. This is not an accidental old upload.

| Observed stage | Result |
|---|---|
| Isolated environment creation, pip/bootstrap tools | Passed |
| Download of 97 pinned dependency wheels, 4,088,733,635 bytes | Passed; 214.15 seconds |
| Installation of those dependencies | Passed; 90.59 seconds |
| Ordinary project build/install and installed provenance | Passed |
| Loading contract | One test passed; no skips |
| Real pinned generation processors and all 24 hardware request constructors on CPU | Passed; zero GPU calls |
| Prospective admission command | Passed |
| Filesystem check immediately before checkpoint staging | Refused |
| Checkpoint download, actual GPU loading, hardware matrix | Not started |
| First-90 capability, full pilot, freeze, main, final empirical analysis | Not executed |

All 12 subprocess receipts report exit code zero. The last completed command ended
at `2026-10-13T17:21:11.567907+00:00`, approximately 350.57 seconds after the
notebook's observed assignment clock. The outer refusal was exported at 17:21:12.
That clock is observational, not evidence of the provider's complete billed interval
or release. The two T4 devices were assigned; the screenshot later shows them idle.

There are **no worker databases and zero new physical model attempts** in this
submission. The 24 CPU constructors are plan checks, not executed attempts. The
configuration retains the already approved 23 historical preparation attempts and
71 cumulative ceiling. This setup failure adds no attempt and requires no enlarged
allowance. All 6,280 intended main outcomes remain unknown.

The outer notebook catches the failure so cell 9 can export evidence. Zero uncaught
Jupyter error outputs therefore does not mean the research succeeded:
`last-action.json` correctly says `blocked_or_safely_stopped`. Its generic reason
does, however, obscure the actionable root cause.

## 2. What the storage error actually proves

The exported environment report records:

```text
ValueError: scratch_capacity: additional_required=20648488160
gpu_execution=false
model_weights_loaded=false
weights_staged=false
```

The additional bytes break down exactly as follows:

| Item | Bytes |
|---|---:|
| Pinned 9B checkpoint, original four BF16 shards | 19,306,310,880 |
| Existing build/staging reserve | 1,073,741,824 |
| Existing output reserve on the same filesystem pool | 268,435,456 |
| Required additional capacity at this check | **20,648,488,160 = 19.2304 GiB** |

This is additional disk space after installation, not GPU VRAM, host RAM, total
experiment storage, a bill or an output-token budget. Loading NF4 on the GPU does
not make the original BF16 download smaller. The full pinned files are staged and
verified before the model is quantized in memory.

The configured cache is unset, so the current code defaults to:

```text
/kaggle/working/course-workspace-4deee720e0f2/gpu-environment/scratch/hub
```

The guard checks `scratch` and `output`, groups observations by `st_dev`, and uses
the minimum observed free capacity for a shared pool. The exact error amount and
call position imply that it treated these locations as shared and credited no
already staged shards. The code refused an observed pool below 19.2304 GiB.
**Neither the measured free bytes, total bytes nor filesystem identity was saved.**
The precise original pool deficit cannot now be recovered from these exports.

The user-provided screenshot, observed later at session minute 12, shows disk
2.2/57.6 GiB, RAM 2.1/30 GiB and both T4s at 0% utilization with zero GPU memory.
It supports about 55.4 GiB of apparent session-level disk availability. It does not
identify the filesystem containing the checked path or give its earlier readings.
The actual guard **admits** the screenshot's approximate capacity when those values
are supplied for its checked pool in the CPU reproduction. Thus it would be wrong
to claim that the screenshot itself explains insufficient capacity. Different
measurement scopes, mounts or observation times remain possible explanations.

Kaggle's historical [official output-capacity announcement](https://www.kaggle.com/discussions/product-feedback/195163)
distinguishes `/kaggle/working` output storage. It is not proof of this session's
current capacity. Earlier repository evidence also measured `/kaggle/working` and
`/tmp` as different devices with very different free capacities
([prior storage observation](../../notebooks/run/1/m5-kaggle-preflight-results/storage-plan.json)).
Neither justifies assuming that a particular temporary path has sufficient space
on the next host. The repaired notebook must measure its own actual destinations.

## 3. Engineering defects and verification gap

The observed blocker and the following additional source defects should be handled
in one small repair. Only the first row is the actual final-online-5 refusal;
the other rows are demonstrated weaknesses or source-inspected risks.

| Defect | Consequence | Existing code to repair |
|---|---|---|
| Capacity facts are lost when the guard raises | The screenshot/guard disagreement cannot be diagnosed from exports | `scripts/m5_kaggle_preflight.py`: `filesystem_facts`, `require_space`; `scripts/m5_course_smoke_assets.py`: `prepare` |
| Online setup checks dependency space first and checkpoint space only after installation | About six minutes of preparation pass before discovering an unsuitable storage layout | `prepare` online admission and checkpoint staging |
| Default environment, installer temporary files and full checkpoint share the output workspace | Rebuildable assets compete with canonical workers and exports; weight files could also become saved notebook output | `scripts/build_course_kaggle.py`: environment selection; bootstrap scratch/cache arguments |
| Initial checkpoint admission checks installation scratch even if `hf_cache` points elsewhere | A large external cache can be falsely refused, or a small one falsely admitted | `prepare` checkpoint `require_space(scratch, ...)` call; reproduced both cases on CPU |
| Every blocked bootstrap is treated as an unusable environment and rebuilt under `retry-*` | Re-running can install another large venv while preserving the old one, worsening capacity and wasting time | Notebook generator's bootstrap reuse branch |
| Incoming checkpoint bytes sum both final and `.partial` copies | An obsolete partial can wrongly reduce the estimate for other shards; actual verification happens later | `prepare` staged-byte calculation; source-inspected arithmetic counterexample |
| Fallback staging charges the entire 4B checkpoint without cached-byte credit and retains 9B assets | A interrupted 4B download can be refused unnecessarily; both checkpoints can exceed the selected pool | `scripts/course_kaggle_workflow.py`: `run_qualification` fallback staging |
| Outer failure replaces the specific reason with generic `Bootstrap failed` | Notebook foreground, last action and HTML omit the required/available/path details | Notebook generator bootstrap exception and export summary |

The previous delivery validation deliberately used a CPU override, which bypassed
the real Linux GPU-environment bootstrap and large checkpoint storage path. It
verified notebook orchestration, guarded execution, SQLite/export/analysis behavior,
not Kaggle disk capacity. The actual source change from a 9.32 GB 4B checkpoint to
a 19.31 GB 9B checkpoint was not covered by a test of this online storage path.
Successful CPU delivery execution did not establish physical staging feasibility.

The repeated missing-`wrapt` sitecustomize messages and Transformers docstring
`[ERROR]` messages were nonterminal here: their commands passed and subsequent
checks completed. Retain them in full logs, but do not call them this incident's
cause or change 97 reviewed dependency pins just to silence them. If environment
isolation later exposes a real dependency/import defect, address that separately
with its own executed failing check.

## 4. Recommended complete repair

Keep the current notebook as an orchestration interface and reuse the native
downloader, pinned manifest, bootstrap receipts, worker ledgers and exports. No new
runtime, scheduler, dependency framework or progress database is needed.

**Select and record storage before installation.** Keep canonical source/config,
workers, setup logs, analysis and both portable exports in the normal output
workspace. Put rebuildable venv, wheel downloads, pip temporary files and original
checkpoint cache in a measured writable session scratch location, considering
`/kaggle/temp` and `/tmp`. Check the actual path and its resolved filesystem, not
the spelling of a directory or a panel total. If it shares a pool with output,
count the pool once and include output reserves. If it is separate, admit each
pool's needs separately. Never use read-only dataset inputs as writable scratch.

Before multi-GB downloads, print and save the selected paths, timestamp, device/pool,
total/free bytes, candidate size, required incoming bytes and output reserve. Save
these in the existing bootstrap evidence, including rejected candidate locations.
Where mount information is available, retain the relevant Linux mount observations
alongside `stat`/`disk_usage`. A small write probe checks writability, not capacity.
Dashboard or undocumented quota assumptions must never override a genuine failed
write or lower path-specific available-space observation.

Use the existing conservative dependency-size allowance for early location
selection, clearly labelled an estimate; after downloading wheels use their actual
ZIP expanded sizes, as the code already does. Recheck before installation,
checkpoint staging and exports. Plan the peak of downloaded wheels plus expanded
installation versus the installed environment plus checkpoint after wheel cleanup.
Do not sum nonoverlapping phases or treat an estimated allowance as guaranteed
physical capacity. A fallback path should be tried during this early location
selection, before any hardware attempt. If no suitable location exists, stop with
an explicit setup-limited result and exported readings.

**Measure the actual cache and exact remaining download.** Resolve/create the cache
directory and pass that path to checkpoint admission. Reuse the same size helper
for initial and fallback staging. For each pinned shard, credit exactly one usable
representation: a size/hash-verified complete file, or a valid bounded partial
prefix when no complete file exists. Never credit duplicate, oversized or symlinked
files. Include metadata and the existing reserve. Keep the native immutable revision,
LFS SHA-256, exact HTTP-range verification, two download threads and bounded transient
network retries. Rename only verified complete downloads; integrity failures remain
failures with evidence. Do not convert/requantize the checkpoint or silently change
the model, context or scientific request to save storage.

**Resume installed setup independently of checkpoint completion.** A storage or
download failure after successful installed provenance should reuse that verified
interpreter and resume eligible native download ranges. Preserve failed receipts
and logs, rather than automatically retaining and rebuilding every venv. The
existing `installed.json`, interpreter path and source/package checks are enough
to establish this boundary; extend the existing bootstrap report with its completed
stage and paths rather than creating another state store. A new notebook session
without the temporary environment reconstructs it from exact pins. Lost temporary
weights can be downloaded again; completed scientific calls must still reuse their
persisted replies without resampling.

Rebuild a damaged/incompatible installation only when its checks actually fail.
First preserve setup diagnostics, terminate/confirm any owned child, then reclaim
only the package-owned disposable installation under the verified scratch root.
Check absolute path containment and reject symlinks. Never delete canonical workers,
source, submitted evidence, raw replies, reports or portable exports. Do not put an
environment or checkpoint directory inside the recursive experiment backup tree.

**Make the already declared 4B fallback storage-safe.** Only after the existing
terminal hardware or complete capability/protocol failure may 4B be selected.
Refresh cache capacity and credit its existing complete/partial files. Retain both
checkpoint caches if they fit. If they do not, quiesce the failed 9B candidate,
preserve all its scientific and asset receipts, and reclaim only its rebuildable
checkpoint cache before downloading the exact pinned 4B files. Keep the same
verified environment and explicit per-candidate bundles. A setup capacity failure
does not become a model hardware rejection and must not trigger a model switch.
Frozen/main failures, audit defects and incomplete sessions still cannot switch.

**Expose the root cause and completion state.** On failed bootstrap, read its
existing receipt and carry the original stage, path, required/free bytes and reason
into the outer last action and HTML. Keep the full exception traceback and subprocess
logs. The notebook should foreground concise stage/candidate progress and the current
log path; detailed pip/library output remains downloadable. Preserve existing
15-second progress, download-byte updates, per-call prefill/decode progress,
ten-minute quiescent backups and final export cell. A completed export after setup
failure should say “Setup stopped before weights; 0 new model attempts”, not imply
hardware, pilot or research completion. State the genuine remediation or safe-resume
path; a known terminal scientific failure still exports a limited result.

Keep the output reserve and current pilot-derived main storage projection. Refresh
their destination readings at existing checkpoint boundaries. A failed backup or
storage write must stop new work and preserve the previous successful export;
derived files can be recreated, canonical recorded outcomes cannot.

## 5. Focused acceptance before another upload

Exercise the actual online bootstrap boundary, rather than repeating only the
CPU notebook override. Use tiny pinned wheel/shard fixtures and mocked subprocess
or platform boundaries in the existing tests; no GPU execution is needed for these
engineering checks.

| Required check | Passing evidence |
|---|---|
| Adequate, insufficient and shared/separate destination pools | Correct path-specific decision; facts exported for every refusal; shared reserves counted once |
| Approximate screenshot capacity supplied to the real guard | Current guard admits; no claim that these were the original filesystem readings |
| Scratch low/cache high and scratch high/cache low | Check the cache pool, fixing both counterexamples demonstrated by this investigation |
| Full online peak and pre-download admission | Unsuitable locations rejected before dependency installation; suitable temporary location used automatically |
| Completed installation followed by capacity/network interruption | Rerun verifies/reuses the interpreter; no second dependency install or abandoned `retry-*` venv |
| Complete shard, partial shard, both, oversized partial, corruption and range failure | Exact incoming-byte calculation; final hashes mandatory; no duplicate credit or unbounded retries |
| Actual approved 9B-to-4B fallback staging | Reuse environment and cached 4B bytes; reclaim only eligible disposable 9B cache if needed; preserve candidate ledgers |
| Notebook bootstrap failure and export | Specific root cause reaches notebook, JSON and HTML; previous export preserved; zero model calls |
| Restored bundle with deleted temporary environment/cache | Reconstruct assets; strict source/settings binding and exact persisted-call reuse preserved |
| Lightweight delivered packet | Two opaque input files, code/config/fixtures/metadata only; no venv, wheels, weights, build duplicates or old experiment payloads |

Reuse `tests/test_course_smoke_assets.py`, `tests/test_kaggle_preflight.py`,
`tests/test_course_kaggle_workflow.py` and the existing literal notebook/export
validator. Add only checks needed for the changed storage/setup behavior. Refresh
the generated notebook and source-bound package from the committed implementation,
then verify their source hashes and evidence exports. The notebook validator's
normal CPU override remains useful, but its report must say that it does not test
native large-download or T4 feasibility.

The present read-only diagnostic already executes the real current guard on CPU
to reproduce the exact error and the opposite outcomes for misplaced cache checks.
It also verifies the source/notebook/archives and retained attempt scope. The
stale-partial example is arithmetic inspection of the existing sum, not an executed
native download. The full repair acceptance matrix above is proposed, not claimed
as passed.

## 6. Execution path and limits after repair

Keep the adopted pinned 9B-first/4B-fallback design, compact prompt profile,
independent T4 replicas, complete 110,416-token input bound plus 256 outputs,
600-second envelope-only deadline, ordinary 120-second deadline, fixed populations,
sampling, replay, 256/64 limits and scoring. Hardware still requires both forced
full-input probes, finite output, fresh state and at least 1.5 GiB measured free
headroom. The first-90 thresholds, complete-pilot validity/raw-effect audit,
conditional freeze and main remain mandatory. Storage repairs neither prove those
gates nor authorize running them here. No new candidate or attempt increase is needed.

Because final-online-5 generated no model outcomes, the next corrected packet can
start a fresh normally source-bound qualification while retaining the original
submission as incident evidence and the historical 23-attempt predecessor. Keep
the earlier export unchanged. Do not attach an old source-bound payload and disable
hash checks to force it into a changed packet. If preparation evidence is carried
forward, use the existing evidence-preserving preparation migration pattern; it
must not invent workers or alter the attempt count.

The practical operator path remains: upload the corrected notebook and small
two-file dataset, select T4×2 and Internet On, then Run All. Cell 7 measures/selects
storage, installs or reuses setup, stages verified weights, qualifies the fixed
candidate(s), and conditionally runs capability, full pilot, main and reproducible
analysis. Cell 9 exports outcomes and safe-resume evidence even after a failure.
Later sessions use the same corrected dataset and one matching latest export.
After exports, stop the interactive session normally; notebook timestamps never
prove that Kaggle released the GPUs.

No engineering proposal can guarantee that provider termination, network outages,
hardware OOM or insufficient model capability will never happen. The achievable
contract is automatic setup recovery where justified, bounded execution, clear
progress and causes, preserved outcomes, and an accurate complete or limited result.
This proposal directly prevents the demonstrated placement/accounting/rebuild
defects and makes any remaining capacity disagreement diagnosable without asking
the operator to run extra diagnostic cells.

To reproduce this investigation, without modifying the submission:

```powershell
.venv/Scripts/python.exe notebooks/validation/course-kaggle/analyse_final_online_5.py --output "$env:TEMP/course-final-online-5-analysis.json"
```

The output must not already exist. This check uses local metadata and CPU only;
it performs no network requests, installs no dependencies and downloads no weights.
