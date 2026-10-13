# Kaggle final-online-2: diagnosis and complete repair proposal

Implementation update: the user subsequently requested full repair and explicitly
authorized the one-time 25-attempt incident allowance. See the
[repair evidence and delivery](course-kaggle-final-online-2-repair.md) for the
implemented changes and executed checks. The proposal below preserves the original
diagnosis and its then-pending decisions.

Prepared 13 October 2026 on `feat/course-m5-inference-preparation`, inspected HEAD
`870e0f3e7c3a21b0190bb0bc8eda2f2da1204d0f`. This is a proposal, not an implemented
repair or an accepted GPU configuration. No model was loaded and no GPU call was
made during this investigation. The submitted run itself attempted model loading.
Scientific authority remains [PROJECT_SPECIFICATION.md §11.3](../../PROJECT_SPECIFICATION.md#113-cumulative-resources-and-admission),
including the approved automatic, observational course policy.

## Decision

Keep the existing notebook, pinned environment, research runtime, SQLite ledgers,
checkpointing and reports. Repair the loading audit's assumption that every model
has `hf_device_map`; make failed-stage recovery depend on persisted state rather
than the existence of a report; preserve full exception evidence; and reconcile
the cumulative smoke-attempt limit across repaired packages. Improve setup reuse
and progress in those same code paths. A new orchestration framework, alternative
inference engine, unpinned upgrade or relaxed scientific screen is unnecessary.

The immediate error is a deterministic adapter defect, **not evidence that the
model cannot fit on T4**. Conversely, successful weight loading is not evidence
that the full-input stress, numerical, capability or timing requirements pass.
Those requirements remain untested in this run.

There is one consequential scope issue: the current matrix occupies all 24
recorded smoke-attempt slots, and this run already recorded one failed load
attempt. A fresh complete matrix plus that failure requires at least 25 cumulative
attempts. This proposal does not authorize that increase or reset the old count.
The exact options and recommended narrow amendment are in §4.

## 1. Evidence and what actually executed

Inspected the [executed notebook](../../notebooks/run/final-online-2/notebook-exec.ipynb),
`course-results.zip` and `preflight-results.zip` in the same directory. Both ZIPs
passed CRC checks. The notebook's first nine cell sources match the delivered
`final-online-1/notebook-fixed.ipynb`; Kaggle added one empty, unexecuted cell.
This was the repaired compact package, not the previous loose-file upload.

| Evidence | Finding |
|---|---|
| Package source | `46a993629d285e7c302fb1d022b84b67d2effe12` |
| Kernel | Python 3.13.15 |
| Hardware inventory | Two distinct Tesla T4 UUIDs, 15,360 MiB each, driver 580.178.04 |
| Pinned core environment | Torch 2.11.0+cu128, Transformers 5.12.0, Accelerate 1.14.0, bitsandbytes 0.49.2 |
| Source and installation | Passed; 29 ordinary installed research modules matched |
| Checkpoint | Seven files verified against pinned metadata and original hashes; revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` |
| Affected host checks | Three passed, zero skips, reported 4.852 seconds |
| Smoke | One physical model attempt; zero completed model generations; both provider cleanup entries reported confirmed process exit |
| Hardware gate | Failed; zero ordinary completions, zero full-envelope probes, no accepted native loading diagnostics |
| Capability / full pilot / main | Did not execute |
| Analysis | Limited feasibility report reproduced twice; all 6,280 main logical slots unknown |

The receipt's `actual_minimum_free_bytes: 0` and peak zero mean **no qualifying
measurement was available** here. They do not establish that the GPU had zero
free memory. The proposed presentation should use “not measured” for this case.

Cell 7 ran from 18:01:31 to 18:14:49 UTC, about 13 minutes 19 seconds. Most time
was successful preparation, not a hung experiment:

| Step | Measured elapsed |
|---|---:|
| Download 97 candidate wheels, 4.089 GB | 217.660 s |
| Install candidate dependencies | 84.034 s |
| Build / install research package | 5.066 / 0.466 s |
| Installed provenance check | 13.970 s |
| Download and verify checkpoint, 9.333 GB including metadata | 360.548 s |
| First model weight-load progress | Reached 426/426; roughly eight seconds of displayed loading progress |

The hardware receipt counted roughly 20.148 seconds as the failed attempt's
interruption time. These observations do not provide a per-generation runtime or
a complete provider billing interval. About 13.42 GB of online dependency/model
downloads remain necessary with the current pins even though the dataset is small.

The notebook generated a link to an approximately 8.65 MB `course-resume.payload`,
but **that file is absent from the supplied incident directory**. The results ZIP
has reports and receipts, not worker SQLite databases. The supplied preflight ZIP
contains setup evidence, not the hardware worker databases. Therefore I cannot
inspect original attempt rows, provider-ready records or raw subprocess evidence
from these three files alone. Receipt counts are clearly identified as such.
Retain the resume payload; a results ZIP cannot replace it for recovery.

Artifact hashes, command timings, the pinned-loader excerpt and CPU reproductions
are retained in [final-online-2-diagnosis.json](../../notebooks/validation/course-kaggle/final-online-2-diagnosis.json).
The submitted notebook SHA-256 is
`759edbc8e4da96fd20dc89af011c6a049891130839c6929e1a36ea13fc5696de`.
All three submitted files were inspected without changing their bytes.

## 2. Root cause, proven against the installed version

The causal chain is:

1. `SmokeFactory` calls `ModelFactory` to load the pinned text-only model with
   explicit `device_map={"": 0}`, NF4 double quantization and FP16 compute.
2. Weight loading reaches completion. `ModelFactory` calls
   [`audit_language_load`](../../recovery/inference.py#L97) before declaring the
   provider ready or sending a generation request.
3. That audit directly accesses `model.hf_device_map` at lines 123–124 and again
   while creating its report at line 135.
4. In the **exact hash-verified Transformers 5.12.0 wheel**, `modeling_utils.py:4346`
   calls Accelerate dispatch only if the requested map contains more than one
   distinct device. This single-device load skips that path; the returned Qwen
   object need not have `hf_device_map`.
5. Attribute access raises; the child sends the error to `ProcessProvider`;
   the provider becomes blocked; the smoke stops; Run All reports a limited result.

The exact wheel hash is
`500be9eb644ede81c3103eee7687fc36d05dd75d1c76686c3820b26396fe7c7c`.
I verified the locally cached wheel against the incident manifest before reading
its source. This is stronger evidence for this incident than assumptions based on
another Transformers release. The official [model-loading documentation](https://huggingface.co/docs/transformers/en/main_classes/model)
describes device maps and whole-model placement; it does not make an absent
dispatch annotation evidence of CPU offload.

The current condition evaluates the actual parameter/buffer device checks before
accessing `hf_device_map`. Reaching the attribute error is consistent with those
earlier checks passing in that invocation. It is not a saved exhaustive native
loading report, proof about all auxiliary quantization state, or memory acceptance.

I reproduced the exact AttributeError using the existing CPU mock with its map
attribute removed. A mock CPU tensor was still correctly rejected. The existing
11 `tests.test_inference_preparation` tests passed in 0.259 seconds, demonstrating
the coverage gap: `tests/inference_mocks.py` always assigns a device map, and the
current tests never exercise its absence. The three Kaggle persistence tests do
not test this loading contract.

## 3. Immediate production correction

Change `recovery/inference.py` and its focused tests, with the following contract:

- Require the maintained text-only class, complete loading diagnostics, no missing
  or mismatched language weights, allowed unused vision/MTP keys, correct embedding
  and head identities, actual NF4/double/FP16 settings, and permitted tensor dtypes.
- Require all named parameters and buffers to reside on local `cuda:0`. Reject CPU,
  disk/meta state, another GPU and mixed placement regardless of map annotations.
- Read `hf_device_map` with `getattr`. Its absence is allowed **only after actual
  single-device placement has passed**. If present, require a valid nonempty map
  describing only that device; reject conflicting or malformed values explicitly.
- Record requested placement, the observed optional annotation, and the derived
  actual tensor-device inventory separately in the existing load report. Use null
  for an absent annotation. Never assign a fabricated `model.hf_device_map` merely
  to satisfy the old check.
- Include named buffer placement in the report. For packed NF4 parameters, check
  supported auxiliary quantization tensors if the pinned API exposes them outside
  named parameters/buffers; document any actual host metadata separately. Do not
  invent a blanket requirement that non-tensor metadata live on CUDA.

Sketch of the core change, subject to the full checks above:

```python
observed_map = getattr(model, "hf_device_map", None)
verify_actual_parameter_and_buffer_placement(model, local_device="cuda:0")
if observed_map is not None:
    verify_observed_map_is_consistent(observed_map, local_device="cuda:0")
# Save the real optional annotation and actual placement; do not mutate the model.
```

This sketch does not prescribe new generic helper layers; the small checks can
remain explicit inside the existing audit. Both ordinary and envelope factories
share this function and must receive the correction. Keep the current checkpoint,
package pins, attention path, renderer, limits and sampling settings. An upgrade,
`device_map="auto"`, offload, blanket `.to()`/dtype casts or skipping the audit
would introduce different problems or change the intended configuration.

Required regression cases: absent map with all tensors local; ordinary integer
and `cuda:0` map values; missing map plus CPU/meta/other-GPU tensors; bad buffers;
empty/malformed/conflicting maps; unsupported precision; missing/mismatched keys;
tied and untied heads; real loader-argument assertions. Mocks must cover both
annotation shapes returned by the reviewed loader, not assume dispatch occurred.

## 4. Safe recovery and the 24-attempt constraint

### Recovering this incident

Do not edit the submitted notebook's outputs, alter original SQLite statuses,
overwrite its source, or relabel its blocked attempt as a harmless interruption.
`WorkerStore.block_attempt` records a provider defect; `begin_attempt` only permits
one retry after an established infrastructure interruption. A diagnosed loader
bug is not that retry condition. The missing full child traceback and absent
resume payload also prevent independently proving every stored lifecycle fact.

The repaired adapter changes source bytes. The original bundle must remain bound
to its original source; loading it under a new source packet is correctly rejected.
For this pre-pilot failure, the practical recovery is a **new corrected bundle**,
with the old incident retained as failed preparation evidence and its original
attempts included in cumulative smoke accounting. Before doing this, inspect the
resume payload if available and confirm the reported absence of scientific
generation/freeze. If it is unavailable, retain the receipt and explicit missing
raw evidence; do not certify a complete recovery audit from reports alone.

### An actual acceptance conflict, not a software workaround

The fixed hardware plan has 21 ordinary probes, two complete-envelope probes and
one controlled hang: 24 attempts if everything succeeds first time. The old failed
load is already one recorded attempt. Repeating the complete plan requires at
least 25 cumulative attempts. Ordinary continuation of the old blocked call is
forbidden, and changing source invalidates cross-bundle outcome reuse.

**Recommended scoped amendment, pending explicit authorization:** permit exactly
one additional cumulative attempt for this diagnosed pre-generation repair,
making the incident-plus-corrected smoke ceiling 25. Retain the old failed attempt,
all original 24 planned diagnostics, their identities within each source-bound
bundle, and all acceptance thresholds. No additional retry allowance is implied.
Any later failure that exhausts this allowance still yields a limited result.
This is an execution-constraint change and must be recorded in the specification
before use; this proposal leaves the current 24 maximum unchanged.

If that amendment is not adopted, keep 24 and report that complete corrected
acceptance cannot be established from the remaining 23 attempts. Do not drop the
hang/envelope/ordinary probes, reuse incompatible replies or reset the count.
Separating future startup events from generation counts could be a later explicit
design decision; it cannot retroactively erase this recorded attempt.

### Fix the current cross-session counter defect

In observation mode, `m5_course_smoke.admission` counts only current/resumed stores;
it does not include `budget.prior_smoke_attempts` or prior hardware stores from a
different source package. I demonstrated admission with a synthetic documented
prior count of 24 and empty current stores. This ignores a still-mandatory attempt
constraint even though removing GPU-hour admission was authorized.

Derive the smoke total once from original attempt records, current and explicitly
retained predecessor evidence. Reuse existing worker ownership/run identities and
prior-evidence fields; deduplicate references to the same original attempts and
their backups. Do not merge old calls into new worker databases or introduce a
parallel ledger. A missing predecessor database permits only an explicit evidence
bound, not an invented zero. Check the total **before downloads** and before every
physical attempt, under either the existing or separately amended ceiling.

### General Run All resumption rules

Replace the current `hardware/report.json.exists()` decision with an inspection of
the same report, original worker state and gate result:

| Persisted state | Automatic action |
|---|---|
| Accepted hardware, matching source/settings/environment | Advance; revalidate required current-host identity/evidence |
| Incomplete stage after a recoverable controller interruption | Seal old observation, confirm process ownership/quiescence, apply existing bounded exact retry/resume rules, and rerun the existing hardware entry point |
| Completed invalid reply or final timeout/failure | Reuse recorded outcome; never resample it |
| Provider/adapter defect or failed scientific gate | Retain diagnostic and limited result; no automatic repeated sample |
| Changed source, frozen settings or inputs | Refuse cross-bundle continuation; preserve original evidence |
| Partial controller setup with missing worker records | Preserve and diagnose; do not invent original call identities |

`hardware()` already supports `resume_in_place`; use it for eligible interrupted
states. Do not simply delete the failed report or retry every failed gate. Also
validate saved bootstrap receipts against actual interpreter/cache paths: a
blocked receipt is evidence of an earlier failed attempt, not a reason to skip all
future eligible setup, and a passed receipt does not guarantee files still exist.

## 5. Failure handling and future error prevention

Keep error handling explicit at existing source/bootstrap/provider/workflow/export
boundaries. Classify these operational cases in existing receipts rather than
building a new exception framework or persistence service:

| Failure class | Response and recovery | Evidence / relevant check |
|---|---|---|
| Source/dataset mismatch or rewritten gzip | Stop before imports/inference; show exact offending file and package mismatch | Payload/member hashes; corrupt/rewritten-input regression |
| Interrupted download, HTTP 429/5xx, network timeout | Bounded retry for the same native file; reuse verified complete files; resume supported partial transfers; no model sample involved | Original URL identity, bytes, chunk progress, attempt logs and final native hash |
| Hash mismatch, unexpected range or wrong checkpoint revision | Reject the file; retain receipt; only a clean same-pin transfer may replace staging bytes | Existing size/hash and Content-Range checks; corrupt-transfer regression |
| Partial installation or missing cached environment | Preserve failed setup logs; use a fresh bounded scratch directory; verify installation before reuse | Versions/module bytes/interpreter provenance; interrupted-install test |
| Loader/API incompatibility | Stop with the full child traceback and loading phase; deploy a reviewed source correction | Missing-map regression and installed contract probe |
| Unsupported GPU/driver/native kernel | Stop before scientific calls; identify actual device and failing operation | UUID, compute capability, Torch/CUDA/bitsandbytes versions and kernel trace |
| OOM, insufficient headroom, nonfinite scores or full-input timeout | Preserve physical attempt and failed gate; bounded cleanup; limited feasibility result | Both full-envelope probes, finite/cache diagnostics and actual free-memory observations |
| Invalid/wrong completed scientific output | Persist unchanged; score and audit under the approved rules; apply capability/pilot gates | Strict validation, independent gold and original raw/effect reconstruction |
| Controller/process interruption before persistence | Existing one identical retry only if eligible; otherwise preserve ambiguity | Worker ownership, attempt/process records and crash tests |
| Disk pressure, backup/export failure | Stop admitting new work before reserve is lost; retain canonical databases and any last good export | Pilot-based disk projection, SQLite backup, atomic export and locked-file tests |
| Reporting/plotting failure | Keep original scientific status and raw resume export; record reporting failure separately; rerun read-only analysis | Agg backend, standalone CPU reproduction; forced-report-error integration |
| Source/config drift during resume | Reject before any model call | Exact saved inputs/settings/environment/freeze bindings |

No mechanism can promise every possible future error disappears or that a model
passes a scientific screen. The reliable contract is bounded work, accurate status,
preserved evidence, and eligible recovery without changing the experiment.

### Warnings observed in this run

- **`sitecustomize` cannot import `wrapt`:** repeated during successful setup and
  model startup. It is not the fatal exception here. Record the startup hook's
  origin and traceback once, and verify that the candidate imports only the
  intended environment. Python's [`-I`](https://docs.python.org/3.13/using/cmdline.html#cmdoption-I)
  does not imply `-S`; [site customization](https://docs.python.org/3.13/library/site.html#sitecustomize)
  can still execute. Stdlib-only download probes can use `-I -S`; installed commands
  need correctly initialized site-packages. Do not blanket-disable site processing
  or add an unpinned package merely to hide the warning. Investigate the actual hook
  before choosing an environment-specific remedy.
- **Qwen recurrent fast path unavailable:** the pinned implementation reports a
  Torch fallback. This can affect long-input latency, but there is no measured
  generation time in this run. Keep the reviewed path and let the existing short
  and complete-envelope probes measure it. Do not install Flash/FLA/causal-conv
  packages from the warning as an automatic T4 fix; compatibility, numerical
  behavior and the candidate environment would require separate verification.
- **One leaked semaphore warning:** present at workflow shutdown despite smoke
  reporting confirmed provider exits. It is not proof of a live CUDA worker or the
  source of the AttributeError. Reproduce the provider-startup failure on Linux,
  inspect ownership and close lifecycle resources in bounded `finally` paths;
  retain the warning until resolved. Do not assert provider deallocation from it.
- **bitsandbytes FutureWarning:** nonfatal in this pinned run. Retain it in logs;
  dependency updates belong to a reviewed new environment, not error recovery.

## 6. Debug evidence and an intuitive notebook

Preserve the nine-cell orchestration interface and the default `ACTION="run_all"`.
The notebook must continue calling repository code. Cell 7 runs hardware, the
first-90 capability screen, the rest of the pilot, unchanged freeze and the full
main matrix in order. Cell 9 provides the final exports. Users should not need
to select separate pilot/main cells or fill budget/proof forms.

Improve the visible status using existing controller JSON and ledgers:

- Show current stage and substep, UTC start/last progress time, elapsed time, device
  slot, current call/attempt and last useful error. During startup, distinguish
  loading, loading audit, provider ready, prefill and generation.
- Show download bytes/total, throughput and last byte received. Keep full pip/model
  output in command logs; notebook output can be concise. A timed heartbeat must
  continue during quiet downloads, loading and reporting.
- Display physical attempts, completed distinct generations, logical slots, replay
  uses, invalid/final failures and unknowns separately. Denominators are the fixed
  hardware plan, pilot 1,114 distinct / 1,178 logical, and main 5,752 distinct /
  6,280 logical. The first 90 capability calls are part of the pilot, not additional.
- Display a timing-based remaining-work estimate when representative measured data
  exists, using phase/condition/device groups and the existing forecast. Otherwise
  show “not enough observations.” Retain the forecast as information, not a revived
  GPU-hour admission form. Logical completion percentage is not allocated cost.
- Show “Hardware failed; model loading audit” rather than “hardware finished” next
  to a zero-exit limited-result receipt. Successful export and successful experiment
  are separate statuses. Hardware failures must not all be presented as budget stops.

For exception evidence, extend the existing child error message and original
attempt reason/receipt to retain exception type, phase and `traceback.format_exc()`.
Currently `_serve` transmits only a type/message string, losing the child stack.
Handle old saved strings compatibly. These diagnostics stay outside peer views.
Capture only relevant environment fields; do not dump tokens or the entire process
environment. Retain the root scientific/operational failure if reporting or export
also fails, with both errors and paths visible in the existing final receipt.

Remove stale operator wording from generated cells/receipts: `course-resume.zip`
is now `course-resume.payload`; formal R7 review text does not describe measured
stress acceptance; the observational automatic policy does not require a manual
provider-release receipt to resume. Users still stop interactive Kaggle sessions
normally. Observed notebook intervals must never be relabeled actual provider
assignment/release. Run All cannot guarantee provider deallocation or completion
before a platform interruption merely because its own controller finished.

## 7. Online preparation without repeated unnecessary downloads

Keep the two-file dataset and pinned online downloads. Reuse a staged environment
within the same Kaggle session only after checking its saved identity, actual
interpreter, pinned versions, source module bytes and verified checkpoint path.
Avoid repeating the 4.09 GB dependency download and 9.33 GB checkpoint transfer
when these verified assets are already present. Do not assume either cache survives
a new Kaggle session.

Use the existing downloader's supported partial-transfer behavior and native
hashes; add bounded same-file network retries if absent. Preserve failed receipts
and place a rebuilt environment in fresh staging rather than clearing canonical
bundle data. A new setup attempt may update the current pointer only after verified
success. Keep assets rebuildable and out of the resume payload. Do not replace
original checkpoint integrity with a weaker cache-exists check or quietly use
another mirror/revision. Measure after the main repair before optimizing the pinned
dependency set; the incident does not demonstrate a need for wholesale removal.

## 8. Implementation sequence and acceptance

Deliver these changes as a few coherent commits, not another milestone hierarchy:

1. **Correct the load audit and tests.** Implement §3; retain exact settings and
   pins. Include a small delivered contract check that exercises missing optional
   annotations; it should not download or load the 4B checkpoint.
2. **Make recovery and failure evidence accurate.** Implement §4–6 in existing
   workflow/provider/bootstrap paths; preserve blocked attempts and cumulative
   counts. Incorporate a separately approved incident allowance only if adopted.
3. **Repair the generated interface and preparation reuse.** Update the generator,
   not just an exported notebook. Stream bounded progress, preserve debug logs,
   and replace stale status/transport/manual-review wording.
4. **Build and exercise the exact delivered artifacts.** Generate a new matching
   notebook and two-file dataset from committed source; retain the previous delivery
   and incident. Publish local artifact paths, source commit, hashes and measured
   package size. No upload or GPU run is part of these CPU preparation commits.

Focused CPU acceptance must verify the actual failure modes, not repeat every
historical repository check:

| Check | Required result |
|---|---|
| Loading-audit regressions | Correct local placement with absent annotation passes; every actual offload/split/precision/loading defect fails |
| Existing inference contract tests | Pins, limits, exact rendering/settings, fresh-cache and finite-score semantics remain correct |
| Child factory deliberately raises | Original traceback/phase persisted; bounded child cleanup; no generation/repeated sample |
| Same-source interrupted hardware | Resumes eligible original work; completed replies/effects and attempt totals unchanged |
| Failed provider/scientific gate rerun | No new sample; useful limited result and exports |
| Cross-source incident / prior attempt evidence | Cannot continue old calls or reset cumulative count; duplicates counted once; missing evidence explicit |
| Interrupted setup / vanished interpreter | Previous receipts preserved; eligible verified setup rebuild succeeds in fresh staging |
| Literal generated notebook execution with controlled provider failures | Stage status, root error, report and fallback exports are accurate |
| Export/restore/reanalysis of exact delivery | Both export types open; raw gzip and saved source intact; SQLite backups consistent; fixed-denominator analysis reproduces |

The next operator-controlled T4×2 execution is the **native integration acceptance**:
verify no missing-map error on both independently loaded replicas; then complete
the unchanged finite/cache/host checks, 21 ordinary probes, both 109,851-input +
256-output probes and controlled timeout within the adopted cumulative allowance.
Require actual ≥1.5 GiB free headroom. Only passing hardware permits the first 90
capability calls; only passing capability permits the full pilot; only complete
≥98% validity with raw/effect audit permits unchanged freeze/main. Continue the
fixed matrix and retain failures/unknowns. A source fix alone is not that acceptance.

If the full-input or capability gate fails, deliver its precise limited finding;
do not promise Run All will finish the research regardless of model feasibility.

## 9. Immediate operator path

Retain these three submitted artifacts and the generated `course-resume.payload`
if available. The current package remains affected by the diagnosed error; rerunning
it unchanged will not repair the loader. Do not attach only `course-results.zip`
and expect a resume. After the reviewed repair and the attempt-scope decision,
upload the **new matching** compact dataset/notebook, choose T4×2 with Internet On,
and Run All. This incident's failed evidence stays separate and counted; later
ordinary interruptions use the matching new dataset and its latest resume payload.

Implemented/verified in this investigation: read-only artifact analysis, native
wheel identity/source inspection, CPU reproduction of the missing-map defect,
CPU demonstration of the prior-count defect, and 11 passing existing loading tests.
Proposed but unimplemented: all production fixes and new regression cases above.
Unverified: successful native corrected load, memory/timing/capability/pilot/freeze/
main acceptance. The original scientific design and mandatory gates are unchanged.

Reproduce the diagnosis from the repository root:

```powershell
.venv/Scripts/python.exe notebooks/validation/course-kaggle/diagnose_final_online_2.py
.venv/Scripts/python.exe -m unittest tests.test_inference_preparation
```

The optional `--transformers-wheel PATH` argument verifies and inspects an already
available exact pinned wheel; it does not download one or execute its code.
