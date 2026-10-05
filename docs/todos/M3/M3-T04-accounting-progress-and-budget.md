# M3-T04 — Resource accounting, progress and safe budget stops

**Status:** active

**Dependencies:** [M3-T03](M3-T03-local-worker-scheduling.md#completion-and-handoff).
M2 passed and M3-T03 completed on 5 October 2026. Use its original physical
parent references, exclusive worker files, durable controls, process visibility
and manifest/checkpoint-derived scheduling status; preserve T02's measured and
uncertain work when adding resource attribution and budget admission.

## References

- [Repository contract](../../../AGENTS.md) and [plan M3](../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Specification [§6](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), [§7.3](../../../PROJECT_SPECIFICATION.md#73-quality-retained-work-and-cost), and [§8.3–8.4](../../../PROJECT_SPECIFICATION.md#83-exact-main-schedule).

## Intended outcome

Manifest-derived progress and reconciled physical/policy accounting show remaining work, failures, dependencies and allocation, and stop new work safely before the ceiling.

## Scope and boundaries

- Join every logical slot to its generation/replay parent and every generation to attempts. Charge physical attempts once; policy accounting includes the shared prefix and all sixteen continuation calls, original measured replay costs and F's abandoned prefix.
- Record request/output tokens, validated source/text deliveries, durations, memory, device allocation intervals, setup/idle/interruption overhead and uncertain lost work. Make overhead attribution explicit and nonduplicative; provider billing is distinct from aggregate physical allocation.
- Provide terminal progress and a read-only status operation at call/round transitions with a bounded heartbeat during long calls.
- Show stage/family/world/branch/replicate/round/peer/device, elapsed attempt time, last checkpoint, scheduled/finished/remaining logical slots and distinct generations, replay uses, attempts/retries, failures and unknowns.
- Show completed worlds and matched comparison groups by family/event/subset, ready/dependency-waiting branches, current gate/stop reason and resumable work.
- Report allocated GPU-hours including idle devices, reserves and remaining ceiling, plus conservative measured remaining-cost/elapsed-time ranges by phase/condition/device. Mark estimates unavailable before measurements; slot percentage is not runtime percentage.
- Admission checks include active devices, timeout/termination allowance, overhead and remaining forecast. Stop safely before the frozen ceiling without deleting scheduled work. Store only necessary allocation transitions beyond existing records; no progress database.

## Completion criteria

- Progress reconstructs entirely from manifests/ledgers/checkpoints after restart, counting completed invalid outcomes as finished work without calling them successes.
- Physical and hypothetical policy totals reconcile for replayed, failed and retried calls.
- Synthetic allocation exhaustion halts admission/terminates safely and retains explicit unknown slots and resumable state.
- CLI/status operations are read-only and responsive while workers are active.

## Validation and evidence

Use hand-calculated schedules with shared prefixes, mixed/Q replay, F, timeouts, ambiguous attempts, idle devices and setup. Verify no double overhead or physical replay charge. Test cost-range unavailability before measurements, later slower-device forecasts, heartbeat behavior, backup/restart reconstruction and budget exhaustion at an adverse timeout boundary.

**Evidence:** Not yet recorded. Add reconciliation tables, status captures and safe-stop results before marking done.

### Implementation approach

Use existing call/attempt keys, saved barriers and committed checkpoints as
the accounting and progress authority. Add allocation start/confirmed-release
intervals in worker files and optional measured peak memory on attempts;
do not persist derived counters. Count invalid durable replies as finished,
and retain unexecuted and ambiguous work separately. Policy costs include the
original prefix and all continuation uses, resolving physical parents across
workers. Loading within an attempt is already part of its measured cost;
allocation overhead is partitioned separately without adding it twice.

Read-only status and terminal transition/heartbeat reports must work with live
workers and reopened backups. Budget admission uses the complete remaining
forecast when available, active allocation, reserves and bounded termination;
an allocation deadline also protects long calls. CPU fixtures will use explicit
synthetic allocation/release acknowledgements. Actual provider release and GPU
measurements remain M5 integration, with unconfirmed release left chargeable.

