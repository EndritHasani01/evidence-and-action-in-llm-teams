# Course M3-T02 — Course accounting, progress and lifecycle gate

**Status:** done

**Dependencies:** [M3-T01](M3-T01-course-durable-workers-and-failures.md).

## References

- [Specification quality/cost](../../../../PROJECT_SPECIFICATION.md#73-quality-retained-work-and-cost), [resources](../../../../PROJECT_SPECIFICATION.md#84-resource-gate-and-freeze), [adopted cumulative course resources](../../../../PROJECT_SPECIFICATION.md#113-cumulative-resources-and-admission) and [plan M3](../../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Existing [accounting/status/budget evidence](../../M3/M3-T04-accounting-progress-and-budget.md) and [lifecycle acceptance](../../M3/M3-T05-crash-safe-scripted-lifecycle.md).

## Intended outcome

Course execution has honest reconstructible progress, physical versus policy costs, safe budget admission/stopping, and a durable scripted lifecycle handoff for analysis.

## Scope and boundaries

- Reuse existing slot/generation/attempt/allocation joins. Charge physical prefixes/replies once, every real attempt/retry/uncertain work, and assigned idle/setup/interruption time. Hypothetical policies pay their prefix plus all sixteen logical continuation calls and original replay cost; F includes its abandoned prefix. Provider billing, allocation and process lifetime remain distinct.
- Apply adopted course ceilings/reserves and prior-spending treatment without resetting cost for a new account. Preserve unavailable interval/cost states; no invented remaining allowance, zero unknown duration or double-counted overhead. Keep an explicit overhead attribution rule and token/delivery/attempt/device/memory records sufficient for the frozen analysis. Forecast from measured phase/condition/device data when available; CPU data does not predict T4 throughput.
- Derive read-only terminal/status progress from manifests, original ledgers and checkpoints: stage/world/branch/peer/device, bounded heartbeat, elapsed attempts/checkpoint, logical/generation/replay/attempt/remaining counts, failures versus unknowns, ready/waiting comparisons, cohort coverage and allocation/forecast/stop reason. Work percentage is not runtime percentage.
- Check resources before admission using active devices, timeout/termination/setup allowance and remaining reserves. Stop/release safely before the ceiling; correctness, silence or early success never removes scheduled work. Complete a tiny scripted course lifecycle covering all families/interventions/controls/repeat paths; enumerate the full schedule without simulating every model call.

## Completion criteria

- Independent accounting/status reconstruction matches original records before/after restart and reconciles 5,752/6,280 main and 1,114/1,178 development generation/logical counts.
- Budget exhaustion leaves explicit unexecuted slots and resumable original scope; forecasts remain unavailable without sufficient evidence.
- M3 course gate passes with crash-safe, portable scripted records/checkpoints and offline handoff, while old bundles remain readable and intact.

## Validation and evidence

Use synthetic allocation/setup/idle/uncertain-attempt scenarios, replay and failed-slot costs, controller-kill/held-prose cases, changed input/config rejection and database backup reopen. Compare uninterrupted/resumed logical states and allowed physical differences; verify read-only progress creates no effect or inference. Record commands/environment and ordinary course lifecycle artifacts for M4. No GPU.

**Evidence:** Completed 11 October 2026 from `11609f4` after inspecting the
course handoff, scientific/resource clause, task references and completed
M3-T01 evidence. [Accounting/lifecycle evidence](../../../validation/course-m3-accounting-and-lifecycle.md)
records 607 full source/91 installed checks with zero skips, 13 final focused
checks, packaged/fresh-process/offline lifecycle acceptance, independent full
main/development count and cost reconstruction, and protected starting bytes.
The course M3 CPU gate passes; no GPU or empirical execution is included.

**Prerequisite handoff before M3-T02, 11 October 2026:** Course/M3-T01 passes
[durable-worker acceptance](../../../validation/course-m3-durable-workers-and-failures.md#completion-and-handoff).
Reuse explicit course `run_inputs` bindings, manifest-selected 20/five-world
scope, pinned 4B `candidate_settings` with `COURSE_LIMITS`, original read-only
parents and existing attempt/checkpoint/worker records. The
[ordinary CPU bundle](../../../../tests/fixtures/course_worker_run.zip)
retains 16 scenarios, ten real kills and exact fresh-process reproduction;
it supports accounting/restart checks, not empirical population coverage.
Timeout defaults remain 120 seconds with bounded one-second termination graces.
At that handoff, status/analysis CLI count choices addressed thesis 60/40 and
needed their course adaptation. Apply the adopted cumulative resource rules without
inventing available quota; complete the tiny all-family course lifecycle and
independent accounting/progress reconstruction required above. The full M3
course gate, resource admission and actual-host/model gates were still open.

**Completion handoff, 11 October 2026:** Course/M3-T02 passes
[accounting/lifecycle acceptance](../../../validation/course-m3-accounting-and-lifecycle.md#completion-and-handoff).
The ordinary three-case course lifecycle retains all-family interventions,
controls/repeats, hand costs and safe stop/resume; the intact prerequisite
bundle supplies ten real kills. Full schedules reconcile 5,752/6,280 main and
1,114/1,178 development without executing every slot. Read-only status now
uses the manifest's declared count for main, while analysis CLI adaptation
belongs to course/M4-T01. `CourseBudget` preserves cumulative bounds and
unknowns through the existing binding; neither CPU timing nor unknown prior/
loading/smoke can establish GPU admission. Course/M4-T01 and CPU preparation in
course/M5-T01 are ready. Actual model/runtime/resource, course M4, pilot/freeze,
main execution and publication gates remain separate.
