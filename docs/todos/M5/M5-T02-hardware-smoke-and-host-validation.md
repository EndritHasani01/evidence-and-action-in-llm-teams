# M5-T02 — Bounded hardware smoke and host validation

**Status:** blocked

**Current evidence, 9 October:** runs 4/5 accept CPU preparation and
[run 6](../../validation/m5-t4-compatibility-run-6.md) accepts the standalone
tiny T4 attention/NF4 diagnostic. No repeat CPU or tiny-GPU run is requested.
[Offline integration and memory audit](../../validation/m5-attention-memory.md)
now pass 127 focused/native source and 15 installed checks. The opt-in layout
still needs actual T4 acceptance; complete-envelope memory, full-candidate GPU
checks and actual model smoke still block this task. The user reports the GPU
session stopped; its exact allocation interval remains unknown.

**Dependencies:** [M5-T01](../M5/M5-T01-inference-and-allocation-preparation.md). M1–M4 must have passed. Explicit authorization covering the GPU/paid-compute scope is also required.

M5-T01 completes on 7 October 2026 with its
[CPU completion checks](M5-T01-inference-and-allocation-preparation.md#completion-and-handoff)
and [proposed private Kaggle T4-x2 packet](../../validation/m5-inference-preparation.md).
The preparation dependency is satisfied. At the T01 handoff, execution authorization was absent;
actual account/quota/monetary terms, device/host/storage checks, all 24 exact
smoke requests, durable off-host export and confirmed provider release remain
preflight work. The proposed ceiling is 24 physical attempts / 0.5 aggregate
GPU-hour (at most 900 wall seconds with two allocated T4s), including loading,
idle GPU 1 and shutdown. No upload, reservation or model inference has occurred.

## References

- [Repository contract/authorization](../../../AGENTS.md), [plan runtime validation](../../IMPLEMENTATION_PLAN.md#runtimeenvironment-validation), and [smoke/pilot gates](../../IMPLEMENTATION_PLAN.md#bounded-smoke-and-capability-pilot).
- Specification [§8.1–8.2](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls), [§8.4](../../../PROJECT_SPECIFICATION.md#84-resource-gate-and-freeze), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [inference uncertainty](../../implementation-research/inference-and-capacity.md#resource-and-validation-conclusions).

## Intended outcome

One candidate configuration passes actual T4 loading, finite-output, worst-context memory, decoding and call-independence checks inside the smoke allowance.

## Scope and boundaries

- Explicit GPU/paid-compute authorization must cover this action. Passing M1–M4 or writing this task is not authorization; reuse valid existing authorization rather than asking again.
- Stop at 24 smoke calls or 0.5 aggregate GPU-hour, whichever comes first. Charge inference validation calls, failed attempts, loading and allocated idle time appropriately against the shared development/setup envelope; the allowance cannot override time limits.
- Test worst requests, all output shapes, useful forwarding, a corrected continuation, raw decode/termination and timeout handling.
- Inspect actual language-weight inventory/loading diagnostics, device placement, CUDA/driver/packages, selected attention/recurrent paths, precision, allocated/reserved/peak memory and finite outputs. Require >=1.5 GiB free headroom at the accepted worst prompt, no unexplained language weights, offload or splitting.
- Verify fresh cache/recurrent state, seeds and isolation under prior-call/order/resume perturbations, and document stochastic/device limits. Replay still uses saved exact parents.
- Rerun focused replacement/checkpoint/process-crash/backup checks in the candidate GPU host environment and verify its SQLite/durability/storage behavior. CPU Windows evidence is not host validation.
- If 9B fails hardware/runtime gates, only the specified 4B fallback is eligible, within the same development allocation. A changed model/template/lock/backend/timeout reopens affected earlier checks; never pool configurations.

## Completion criteria

- A named candidate passes all smoke/host checks with actual measured artifacts and no unresolved isolation/leakage/queue issue.
- Calls, attempts and aggregate allocation reconcile within both smoke and shared budgets; record all failed configurations.
- The candidate can proceed only to the first 90 capability slots, not recovery or main execution.
- If none passes within resources, keep the task blocked, record terminal feasibility evidence and enable the limited-evidence audit path in M6-T02. Do not mark the gate passed.

## Validation and evidence

Link every acceptance statement to load logs, actual requests/replies/token IDs, memory/device traces, cache instrumentation, host CPU/crash checks and cost rows. State accepted settings and limits, timeout observations, failed checks and any required fallback/reruns.

**Evidence:** CPU preparation is linked above; actual smoke/host acceptance
evidence is not yet recorded. No GPU work or compute authorization has been
supplied by completion of M5-T01.

### 8 October GPU-host preparation follow-up

The user supplied a CPU notebook package/disk report and chose GPU-host
preparation, reporting available quota and willingness to use it. The
[host follow-up and first inspection cell](../../validation/m5-kaggle-preflight.md)
record those facts and provide the next concrete step. Brief device/package/disk
inspection precedes CUDA selection and exact request preparation, with all
allocated time charged under the existing limits. Actual GPU-host output,
storage admission, the candidate environment checks and measured model smoke
are still pending. This task remains blocked by these execution prerequisites;
no model/host acceptance or empirical result is claimed.

At the user's request, the next preparation action is now the
[ready Kaggle preflight notebook](../../../notebooks/recovery_m5_kaggle_preflight.ipynb),
with a companion private input ZIP and fixed package defaults. Its
[planning and local evidence](../../validation/m5-kaggle-notebook-plan.md#completion-evidence)
include 22 controlled workflows, actual local CPU Jupyter execution and the
81-focused/16-native check commands. It reports installation/storage failures
and exports diagnostics before any model download or generation. Actual Kaggle
execution and the exact bounded smoke remain pending; this does not complete T02.

### First-run review and CPU transport canary

The supplied [first Kaggle run](../../planning/m5-kaggle-first-run/01-first-run-evidence.md)
records two T4s and CUDA-enabled Torch, then rejects a missing compressed source
fixture. Installation and native checks skipped; no language weights or model
generations ran. The original failed run and snapshots remain unchanged. These
observations supersede earlier pending-inspection statements without passing
candidate-host or model acceptance.

The separately authorized [CPU upload canary](../../validation/m5-kaggle-upload-canary.md)
is implemented: 12 focused standard-library checks pass; the exact shipped
notebook executes in real local Jupyter for valid/missing input and exports
readable diagnostics in both cases. Verified checkout provenance and logical
commits are available in the isolated review checkout.

The user returned the [actual Kaggle run-2 notebook and ZIP](../../validation/m5-kaggle-upload-canary-run-2.md).
All five canary stages pass; notebook source/manifest and export receipt match,
and all three synthetic databases reopen independently off-host. The original
dataset inventory shows all 14 gzip paths and two nested ZIP paths absent, with
exposed counterparts. This explains the first source rejection and selects raw
`.payload` transport for the next full-source packet. Exact dataset version and
provider release remain unrecorded. Full-source upload verification and actual
candidate preparation remain required; no repeat canary is requested. T02 model smoke and
all dependent gates remain blocked, with zero model generations in this run.

### Full-source CPU preparation delivery

The [v2 preparation packet](../../validation/m5-kaggle-full-preparation.md) now
implements K2–K7, with 23 passing operational checks, an 88-package target
resolution and real local Jupyter valid/missing-source execution. The valid
case verifies all 143 canonical source members; both cases export readable
diagnostics and independently reopened synthetic SQLite backups. The actual
Linux/Python 3.13 installation, owned-process cleanup and 81 focused/16 native
checks remain unexecuted. Controlled candidate outcomes are not host evidence.

Next import the new v2 notebook, upload its single raw source payload as a new
private dataset, and run **Accelerator None / Internet On**. Return its executed
notebook and ZIP under `notebooks/run/3/` after stopping the session. This is K8's
full-source/candidate-host preparation and K9's interim handoff; it does not
construct models or claim T4 library, memory, finite-output or smoke acceptance.
Existing GPU authorization persists. Scientific caps/settings/attempt/replay
semantics and allocation ceilings are unchanged; T02 stays blocked by actual
host/model gates, with all dependent task statuses unchanged.

### Returned full-source run 3

The [actual run-3 review](../../validation/m5-kaggle-full-preparation-run-3.md)
accepts complete canonical source upload, Linux/Python 3.13 CPU inspection,
owned-process timeout cleanup and synthetic WAL/FULL/off-host snapshots.
Candidate setup fails when `venv` invokes `ensurepip`; its lower-level cause
is not captured. Package installation, provenance and all 97 focused/native
checks are blocked, with zero model generations. K8 has partial actual evidence,
while K4/K8/K9 acceptance remains open. A narrow pinned-pip bootstrap repair
precedes the next CPU run; the already accepted dataset can be reused unchanged.
T02 model/host gates and task statuses remain blocked as before.

### Run-3 repair and v3 retry handoff

The [pinned-pip bootstrap repair](../../validation/m5-kaggle-pip-bootstrap-repair.md)
creates the clean venv without `ensurepip`, verifies the already pinned wheel in
an owned bounded process and installs pip offline before the unchanged candidate
pipeline. Twenty-five operational checks, a real local isolated pip installation
and exact-v3 Jupyter valid/missing-source runs pass. Windows checks do not pass
actual Linux installation or the 81/16 scientific checks, which remain pending.

Import the [v3 notebook](../../../notebooks/recovery_m5_kaggle_preflight_v3.ipynb),
reuse the accepted private `m5-kaggle-source-v2` dataset and run **Accelerator None /
Internet On**. Return the executed notebook and ZIP under `notebooks/run/4/`
after stopping the session. No repeat upload is required; earlier artifacts and
scientific/package/resource semantics are preserved. T02 remains blocked and
the existing GPU authorization remains recorded.

The user subsequently reports successful isolated pip 26.2.1 installation on
Kaggle/Python 3.13 from the standalone manual cell. The retained
[console output and review](../../validation/m5-kaggle-pip-bootstrap-repair.md)
also record a `sitecustomize`/missing-`wrapt` warning of unlocated origin, which
did not prevent that reported bootstrap result. Full v3 candidate installation,
provenance, scientific checks and model acceptance remain pending. This narrow
manual evidence requires no package-pin or scientific-status change.

### Actual run 4 and same-session continuation

The [returned run-4 review](../../validation/m5-kaggle-full-preparation-run-4.md)
verifies source/cleanup, all 88 candidate package versions/wheel hashes, isolated
project build/install and independently reopened snapshots. The installed probe
exits zero and its receipt verifies all 28 scientific modules, but documentation
messages on stdout cause strict JSON parsing to fail. All 97 focused/native
checks remain unexecuted; six preparation stages pass, one fails and four block.

The [dedicated JSON output repair and continuation](../../validation/m5-kaggle-probe-output-repair.md)
pass 27 focused checks and real local Jupyter wiring with controlled candidate
outcomes. The user confirms the original session is still open. Paste the
[continuation cell](../../../notebooks/recovery_m5_kaggle_continue_run4.py) into
one new cell in that existing notebook, keep Accelerator None and run only the
new cell. It verifies the existing source/venv and executes the remaining checks
without downloading/installing packages. Return its ZIP/updated notebook under
`notebooks/run/4/continuation/`. Original results and scientific/package/resource
semantics are unchanged; actual continuation/model acceptance and T02 remain open.

### Actual run 5 CPU acceptance, reviewed 8–9 October

The [returned continuation review](../../validation/m5-kaggle-full-preparation-run-5.md)
accepts all 97 actual CPU checks with zero skips: 81 focused inference/durable/
attempt/worker checks and 4/4/8 native metadata/capacity checks. Installed
provenance matches all 88 candidate versions and 28 scientific module hashes.
All eight commands exit zero with confirmed process-group cleanup; both closed
SQLite copies reopen independently off-host with integrity `ok`, row `7` and
rejected writes. The exact delivered cell reuses run 4's unchanged source and
venv; no download/install or model generation occurs. CPU wall time is 319.030
seconds. Supplied files remain under `notebooks/run/5/`; original run 4 stays intact.

The CPU portion of K4/K8 and K9's CPU review pass. No further CPU preflight is
requested. [K10's complete-envelope and tiny T4 attention/runtime checks](../../planning/m5-kaggle-first-run/04-model-feasibility-and-smoke.md)
come next, followed by verified asset staging, exact smoke requests and attempt/
allocation admission. The model-smoke notebook is not yet ready. GPU-specific
host/library/headroom, physical language loading/finite outputs/state behavior,
provider release and all model/pilot/freeze acceptance remain unknown. This task
therefore stays **blocked**; existing GPU authorization persists and all shared
resource limits, candidate/scientific settings and task statuses are unchanged.

### Tiny T4 compatibility delivery, 9 October, completed by run 6

The [next-step plan](../../planning/m5-kaggle-first-run/07-t4-compatibility.md)
and [standalone library notebook](../../../notebooks/recovery_m5_kaggle_t4_compatibility.ipynb)
are implemented. [Local evidence and instructions](../../validation/m5-t4-compatibility.md)
record 42 focused operational checks and four real CPU operator checks, zero
skips, plus exact-cell real Jupyter host-refusal and controlled-complete exports.
The latter verifies the real pinned Linux wheel's 85 extracted files; GPU
receipts remain explicitly controlled. Both ZIPs and four copied SQLite
snapshots independently reopen correctly. Earlier failures/results stay intact.

Next import this file into a new private notebook, attach no dataset, select
Internet On / GPU T4 x2 and Run All once within one minute of assignment.
Download the ZIP/executed notebook, stop GPU allocation immediately and return
them under `notebooks/run/6/` with displayed allocation duration. Only the verified
60.7-MB bitsandbytes wheel is staged; matching host Torch is required and no base
packages or model weights change. The conditional 0.3 aggregate GPU-hour bound
depends on the declared start/retrieval/stop discipline, not provider timestamps.
Earlier/setup/idle time still counts under the unchanged shared budgets.

This prepares R8's tiny operators, not the full accepted model environment.
Actual T4 kernels/native NF4, R7 complete-envelope memory, full-candidate GPU
provenance, Qwen loading/recurrent/isolation, bounded exact smoke and release
reconciliation remain pending. Zero model generations run here. This task stays
**blocked**, with existing authorization and all dependent task statuses unchanged.

### Actual run 6 standalone GPU acceptance, 9 October

The [returned notebook and ZIP review](../../validation/m5-t4-compatibility-run-6.md)
accepts all six stages, four clean command exits, 14 attention cases and four
NF4/double-quantized matmuls on two distinct physical T4s. Original cell sources,
all 85 staged wheel files, UUID/library origins, profiled backend/CUDA traces,
numerical comparisons and ZIP receipts verify. Both closed SQLite snapshots
independently reopen read-only off-host. Native GQA uses math; explicit repeated
K/V uses efficient SM75 kernels at the tested shapes. Zero pretrained weights
or model generations ran; all original supplied artifacts remain unchanged.

This accepts R8's small-operator portion for the standalone host-Torch/private-
wheel environment, not the complete candidate lock (33 host-package differences)
or Qwen paths. Torch reports 14.562 GiB usable total per T4; fully materialized
repeated K/V adds a separate conditional 4-GiB temporary at the cap. Next review
supported model attention integration and sound R7 memory coverage offline
before K11 assets, K12/K13 exact requests/admission and K14 actual model smoke.
No backend, package, model/fallback, cap or frozen setting changes in this review.

The observed workflow lasts 38.664 seconds. The user reports the GPU session
stopped and offers a rerun, which is unnecessary. Exact allocation duration,
provider assignment/release timestamps and earlier spending remain unknown;
the conditional 0.3-hour ceiling is not verified spending. Retain uncertainty
within unchanged shared limits. No further user run is requested now. This task
stays **blocked**, with T01 done and progress at 21 done/eight blocked.

### Offline integration and memory review, 9 October

The [next-step contract](../../planning/m5-kaggle-first-run/08-attention-and-memory.md)
is implemented at `8528105`, following separate planning `2182014`. The new
opt-in public SDPA path retains K/V aliases, native masks/head order and fixed
256-token maintained prefill. The baseline stays unchanged, exact settings
separate saved calls, and unsupported CUDA stacks fail before model loading.
[Local evidence](../../validation/m5-attention-memory.md) passes 127 focused/native
source checks plus 15 installed attention checks, with no skips. Actual small
random CPU hybrid Qwen forwards preserve chunk/full logits, KV/conv/recurrent
state and subsequent decode; they are not pretrained-model or T4 evidence.

The read-only report uses original capacity/config/run-6 bytes for both models
and both mathematical sizes. It preserves complete bounds versus constructed
fixture maxima, tied heads, repeat/copy/chunk terms and historical native memory.
Conditional subtotals prove neither fit nor empirical failure; R7 remains open.
No fallback, cap, package, retained-byte, scoring or freeze change is made.

Actual T4 acceptance of this new layout, a sound complete-envelope memory
argument, full candidate GPU/host checks, allocation reconciliation and smoke
still precede completion. Old source-v2 payloads remain preserved and contain
earlier source. No new GPU run, model generations, upload or model-smoke notebook
is requested by this step. This task stays **blocked** with 21 done/eight blocked.

