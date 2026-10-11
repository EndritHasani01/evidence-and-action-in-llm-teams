# Course M3-T01 — Course durable workers and bounded failures

**Status:** ready

**Dependencies:** [M2-T03](../M2/M2-T03-course-attainability-and-capacity.md).

## References

- [Specification persistence/check categories](../../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements), accepted course clause, [plan architecture](../../../IMPLEMENTATION_PLAN.md#2-small-implementation-architecture), and [plan M3](../../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Existing [durable runner](../../M3/M3-T01-durable-round-runner.md), [bounded attempts](../../M3/M3-T02-bounded-attempts-and-failures.md), [local scheduling](../../M3/M3-T03-local-worker-scheduling.md), and [state/replay evidence](../../../implementation-research/state-and-replay.md).

## Intended outcome

Existing worker/checkpoint/attempt machinery executes and resumes the course scope while rejecting changed settings, cross-bundle parent confusion and duplicate effects.

## Scope and boundaries

- Use existing LangGraph replacement state, application SQLite records, pre-delivery barriers and one owned SQLite file per serial worker. Persist exact raw replies/failures before effects; committed checkpoints own states/queues/cursors. Do not add another ledger, identity/transfer service, worker framework or compatibility migration without an observed need.
- Propagate accepted course inputs/configuration through worker assignment, controls, generation/replay, snapshots and resume. Reuse balanced blocks, eligible sibling/device rotation, original read-only physical parents and ownership locking. Keep course and thesis bundle/configuration scope distinct even when local IDs have the same spelling.
- Completed valid, invalid or failed calls resume exactly without resampling. Replay is event/replicate-specific and verifies request/native tokens/state/settings/seed; equal seeds or unrelated equal requests never authorize caching. Boundary and message effects remain branch-local/idempotent; checkpoints never restore cleared fields.
- Persist attempt starts and replies/timeouts; allow only one identical-request retry after infrastructure interruption with no durable response. No retry for wrong/invalid/truncated replies or completed timeout. Retain the initial 120-second timeout, bounded child termination, uncertain possibly completed inference and all charged attempts. Overflow stops visibly as a capacity defect, not truncation or favorable exclusion.

## Completion criteria

- Course worker/attempt/replay/control paths run with correct shapes/settings and reject mutated inputs/settings and foreign-bundle parents.
- Real CPU process interruption/timeout tests preserve exact replies, bounded attempts, independent effects and Q held prose; ordinary synchronous checkpoint/SQLite durability and ownership remain verified.
- Safe close/backup/reopen preserves scientific and progress records. No pretrained-model/GPU claim is made.

## Validation and evidence

Run affected installed-library worker/durable/attempt checks and focused course crashes before/after raw persistence, staging and delivery commit; include cross-worker parents, invalid completed replies, held Q prose and concurrent ownership rejection. Compare uninterrupted/resumed states and original parent records, isolating genuine physical-attempt differences. Reuse unchanged failure fixtures; retain course artifacts in the existing bundle format.

**Evidence:** Not yet recorded. Durable foundations are implemented and verified; course propagation/resume is pending.

**Prerequisite handoff, 11 October 2026:** Course/M2-T03 passes the
[M2 witness/capacity gate](../../../validation/course-m2-attainability-and-capacity.md#completion-and-handoff).
Reuse saved course inputs/schedules, explicit `COURSE_LIMITS`, pinned 4B
`candidate_settings`, existing prefix snapshots and exact B/C `SavedRound`
parents. Native traces cover all 25 worlds/7,458 logical opportunities/592
parent joins. The complete permitted input upper bound is 155,995 with the full
256 output reserve (156,251 resident tokens), within the unchanged 262,144
window. Keep overflow as a visible defect; no cap, truncation or new fallback
is authorized. Continue with the existing worker/SQLite/checkpoint/attempt
machinery and focused course interruption/resume checks. This prerequisite
accepts CPU protocol capacity, not course durability, GPU/model feasibility,
resource admission, a freeze or execution authorization.
