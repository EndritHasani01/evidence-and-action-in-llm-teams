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
Package/weight preparation should occur on CPU before the short allocated run;
GPU-host provenance and affected host checks remain required.

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

The delivered launch defaults must refuse staging/GPU work until the concrete
action has its explicit authorization, supported prior-use inputs, provider
clock/duration/release terms and storage admission. Existing historical
GPU-host/tiny-operator authorization is reused within that scope, without
assuming it accepts this new course model action. The smoke ceiling remains
**24 cumulative attempts / 1,800 allocated device-seconds**. Two assigned T4s
give at most 900 wall seconds before earlier spending and release reserves.

## Validation and progress

Focused checks will cover only changed single-call persistence, retry/deadline
admission, literal raw outcome/resume, source/asset guards, unknown resources,
partial evidence/export and refusal of fabricated physical-memory acceptance.
Actual GPU loading/smoke, R7 coverage, provider release and off-host reopening
remain unexecuted until their prerequisites pass. Commands and receipts belong
in [the task evidence folder](../../notebooks/validation/course-m5-hardware/).
