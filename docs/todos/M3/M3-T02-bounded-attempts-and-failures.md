# M3-T02 — Bounded attempts, timeouts and interruption semantics

**Status:** active

**Dependencies:** [M3-T01](../M3/M3-T01-durable-round-runner.md#completion-and-handoff).
The M2 gate passed and M3-T01 completed on 5 October 2026. Use its exact
application ledger and replacement checkpoints; active attempts without a
durable response currently stop with `UnresolvedAttempt` for this task to resolve.

## References

- [Repository contract](../../../AGENTS.md) and [plan M3](../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Specification [§3.2](../../../PROJECT_SPECIFICATION.md#32-synchronous-rounds-and-replies), [§6 failure/missingness](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [remaining process-failure validation](../../implementation-research/state-and-replay.md#remaining-implementation-validation-not-further-framework-research).

## Intended outcome

Every scheduled attempt terminates or resumes under the declared bounds, preserving failures, unknown work and ambiguous crash costs without resampling completed outcomes.

## Scope and boundaries

- Persist attempt start before generation and raw output/failure before effects. Start development with a 120-second per-attempt timeout.
- Allow at most one identical-request retry only after an infrastructure interruption without a durable response. No retries for incorrect answers, invalid formatting, truncation or completed timeouts.
- If inference may have completed before response persistence, record an uncertain completion/physical attempt; do not claim exactly-once generation.
- A hung attempt must be terminable, its known timeout durable, and status remain responsive. Restarted workers reload their state/model; lost work, load and allocated idle time remain chargeable.
- A context overflow fails visibly before generation and stops for capacity/protocol diagnosis. Do not shorten history, turn the defect into a favorable exclusion, or carry an older candidate into the failed slot.
- Keep unknown/unexecuted opportunities distinct from zero-credit recorded failures. Continue fixed opportunities after ordinary invalid replies.

## Completion criteria

- Attempt/failure state transitions survive worker interruption without admitting more than two allowed infrastructure attempts.
- Durable invalid replies/timeouts are final records for their call ID and resume without generation.
- Timeout and interruption produce distinct justified records; hung-process termination does not stall the controller indefinitely.
- Failure records retain identity, request, timing, termination and known/uncertain work needed for later accounting.

## Validation and evidence

Use CPU subprocesses simulating slow, hung, interrupted and completed calls. Kill before/after raw persistence; assert retry eligibility, identical retry request/settings/seed, no formatting/timeout resampling and no prior-candidate fallback. Trigger pre-generation overflow. Verify a durable result wins on resume and ambiguous work stays charged. Test ordinary continued scheduled opportunities after failures.

**Evidence:** Implementation started on 5 October 2026 after inspecting M3-T01's
ledger/checkpoints, its 18 deterministic checks and the M2 capacity prerequisite.
Attempt recovery will use the same call/attempt identities and database; a bounded
inference subprocess will enforce termination without holding SQLite locks.
Executed process-failure evidence and final regression results remain pending.

