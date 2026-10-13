# Course M5-T02 hardware smoke

Started 12 October 2026 from `2f2523f`, with a clean tree on
`feat/course-m5-inference-preparation`. Follow
[the task](../todos/course/M5/M5-T02-course-hardware-smoke-and-memory.md),
[specification Sections 8 and 11.3](../../PROJECT_SPECIFICATION.md#113-cumulative-resources-and-admission)
and [completed M5-T01 preparation](course-m5-preparation-completion.md).
This checkpoint implements the concrete bounded action; it accepts no hardware,
physical memory, model capability, pilot, freeze or main result.

## Scope and reused evidence

Reuse the pinned 4B/256/64 adapter, exact 24 unexecuted smoke requests, complete
110,107-token input proof, source/package manifests, installed-source checks,
ordinary worker/attempt/allocation records and unknown-aware `CourseBudget`.
Reuse the accepted M1–M4 gates and standalone run-6 results within their scope.
Do not repeat broad CPU or tiny-operator suites without an affected requirement.
Preserve thesis defaults/todos, source-v2 and all earlier notebook/results.

The new path must persist each isolated smoke request/reply in the existing
worker ledger, keep distinct physical independence probes, resume final outcomes
without resampling, use bounded existing process cleanup, and charge both
assigned T4s during loading/idle/export/release. Source/request/settings drift,
unknown prior usage or missing authorization must stop before weight loading.
The user now permits T4 x2 assignment from the start. Package/weight preparation
still uses CPU operations, but its complete assigned interval counts toward the
same smoke ceiling and is independently bounded. GPU-host provenance and affected
host checks remain required; no scientific/resource limit changes.

Physical R7 acceptance still requires justified complete-envelope coverage with
at least 1.5 GiB free headroom, including loading, workspace, cache growth,
allocator/context occupancy and peak liveness. Short successful model requests
or arbitrary padding cannot supply this. Record raw observations and incomplete
coverage honestly; no synthetic or operator-supplied passing flag substitutes
for reviewed supported evidence.

## Resource and authorization inputs

The user reports full Kaggle T4 x2 quota, approximately 30 GPU-hours available
per account, prefers materially less spending, confirms earlier GPU sessions
stopped, and requests a **30-hour project upper bound**. The adopted course
ceiling already provides that bound, cumulative across accounts/configurations.
Availability is user-reported, independently of recorded allocated study time.

Returned repository runs record zero pretrained-model generations. Prior study
allocation/category bounds and cumulative compatibility/smoke usage remain
unknown: the latest reply supplies available quota/the project ceiling, not
previous spending. Do not turn these unknowns into zero or verified remaining
allowance. Run 6's observed 38.664-second workflow is not its provider allocation;
its conditional 0.3-hour ceiling remains unverified spending.

The delivered launch defaults refuse staging/GPU work until the operator records
the authorized bounded scope, supported prior-use inputs, provider
clock/duration/release terms and storage admission. On 12 October the user
assigned **all execution and provider work to themselves**, asking for the
implementation and generated files only. No further execution-information or
permission request is needed to complete this software handoff. The smoke ceiling remains
**24 cumulative attempts / 1,800 allocated device-seconds**. Two assigned T4s
give at most 900 wall seconds before earlier spending and release reserves.

## Validation and progress

Implementation was delivered at `c82ca7b`, with GPU-first support at `c8bb9bd`.
It adds guarded asset staging and
an independently bounded GPU controller. Smoke requests use existing SQLite
call/attempt/allocation records; completed raw outcomes resume without sampling.
Each retry is admitted separately, and two-device allocation includes idle time.
The existing inference adapter, scientific requests, limits and defaults remain
unchanged. Loading inventory, affected CUDA attention cases, model-edge/allocator
observations, state/RNG observations and ordinary backups are retained for review.
Full-envelope R7 acceptance remains explicitly incomplete until supported.

The [source receipt](../../notebooks/validation/course-m5-hardware/source-focused-command.json)
records **14 focused checks**, with zero skips, at `c1dc767`.
The [ordinary installed-wheel receipt](../../notebooks/validation/course-m5-hardware/installed-focused.json)
records **four affected persistence checks**, zero skips, hash seed 37,
all 29 matching production modules, no source Python path and passing `pip check`.
Reuse the earlier nine ledger/attempt checks and single existing control check;
no broad prerequisite rerun is needed. Windows/Python 3.11 CPU evidence is not
Linux/T4 execution evidence. The Linux candidate remains pinned separately.

The first packet's four guarded notebook cells execute successfully outside the
checkout and its closed export reopens, with zero weights/generations/GPU use.
The earlier v2 delivery exposes editable launch fields before source admission and
in the GPU cell, so enabling the later action does not rerun source extraction.
Only that changed notebook/export path is checked again; production checks are
reused. The [v2 notebook/export receipt](../../notebooks/validation/course-m5-hardware/delivery-packet/verification.json)
passes all four cells and closed-export reopening, with zero weights or GPU work.
The exact payload is 203,742,121 bytes with SHA-256
`2dccebc482a460b70d86ae56eefc88db71596d3726ec23da9d2f568b8a87f3e1`.
Commands and receipts belong in
[the task evidence folder](../../notebooks/validation/course-m5-hardware/).

The user requested T4 x2 from the beginning, with one launch configuration.
The [GPU-first focused receipt](../../notebooks/validation/course-m5-hardware/gpu-first-final-focused-command.json)
passes nine checks with zero skips: the original clock survives installed
admission, missing/unknown/exhausted bounds stop before downloads, preparation
preserves export/release time, and tiny CPU fixtures exercise both unassigned
and assigned-host staging. No actual GPU/package/weight work occurs in fixtures.
A dependency-free import succeeds without optional packages/CUDA. The bootstrap
screen is conservative; the existing installed `CourseBudget` remains the
full admission gate before weights. Ordinary model ledgers retain the original
assignment clock, including preparation, with no second charging store.
All 29 production modules, scientific requests and prerequisite proof remain
unchanged, so their passing checks are reused. The
[v3 guarded notebook/export receipt](../../notebooks/validation/course-m5-hardware/gpu-first-packet/verification.json)
checks only the changed delivery path; it grants no hardware acceptance.

## User-run handoff

The final local packet is [dist/course-m5-hardware-v3](../../dist/course-m5-hardware-v3/),
from committed source `c8bb9bd`. Import `course_m5_hardware_smoke.ipynb` into
Kaggle and attach its exact `course-m5-source.payload` as a private input.
`launch-template.json` mirrors the guarded editable fields; do not reuse a
historical source payload with this notebook.
The v3 payload is 203,744,407 bytes, SHA-256
`2c2288ee2cf17a83c73e87c2e385484a2ed08687723c002fb336c15f2968fd43`.
Replace the attached dataset file with this version; its title can stay unchanged.

1. Select **T4 x2 from the start**, fill the visible `LAUNCH` dictionary once,
   record supported prior-use bounds/provider terms and the actual UTC
   `allocated_at`, and set both `stage_weights=True` and `execute_gpu=True`.
2. Run the source, asset-preparation and model cells in order. No accelerator
   switch or second launch edit is needed. Installation/downloads/idle time are
   charged from the same assignment clock; insufficient remaining time stops
   work and preserves the report rather than extending the allowance.
3. Run the export cell, download the actual executed notebook/result ZIP and
   **Stop Session**. Retain actual provider release evidence for off-host ledger
   reconciliation. Do not rerun model work to save its output.

All running, provider accounting and actual-host evidence are user-owned.
M5-T02's hardware acceptance remains pending: full-envelope R7/headroom, actual
loading/state/decoding/runtime, host persistence and confirmed provider release.
This is a delivered implementation, not a passing model gate or terminal failure;
M5-T03, pilot/main/freeze gates remain closed.
