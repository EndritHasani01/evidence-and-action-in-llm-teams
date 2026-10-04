# M6-T02 — Independent artifact and coverage audit

**Status:** blocked

**Dependencies:** [M4-T06](../M4/M4-T06-reproducible-report-and-cpu-gate.md). A quiescent evidence handoff from [M6-T01](../M6/M6-T01-frozen-execution-and-resume.md), complete or safely stopped, OR a documented terminal feasibility failure from M5. Passing a failed gate is not required for limited reporting.

## References

- [Repository contract](../../../AGENTS.md), [plan M6 audit/completion](../../IMPLEMENTATION_PLAN.md#8-milestone-m6--complete-execution-audit-and-reproducible-results), and [coverage map](../../IMPLEMENTATION_PLAN.md#9-coverage-map).
- Specification [§5.1](../../../PROJECT_SPECIFICATION.md#51-exact-outcomes), [§6](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), and [§9 essential checks](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).

## Intended outcome

An independent offline audit establishes exactly what the recorded evidence supports, including coverage limits after a failed pilot or interrupted experiment.

## Scope and boundaries

- Normal route: audit the accepted main bundle after execution stops. Limited route: audit a safely stopped incomplete run or terminal M5 feasibility evidence without requiring an accepted freeze or completed main schedule.
- Join complete manifests, calls, attempts, replay parents, delivery/checkpoint records and exported outcomes. Check source visibility/versioning, literal retention boundaries, exact mixed/Q request/settings/seed/view equality and parent scoping, Q release order, grouping/denominators, repeat identities and environment consistency.
- Independently recompute gold and replay delivery/evaluation from archived inputs/raw replies without inference. Compare with committed checkpoints and exports.
- Reconcile physical/policy cost, allocations, failures, unknowns and superseded defect/rerun records. Duplicated IDs, unexplained missing records and inconsistency are audit failures, not exclusions.
- Revisit all seven §9 check categories for the actual evidence. Distinguish unexecuted slots from completed failures and report matched coverage by population.
- For feasibility-only evidence, audit available pilot/CPU/allocation artifacts and clearly mark all main outcomes/gates unavailable. Do not fabricate a main run or estimates from development rows.
- A pure analysis defect is repaired from unchanged raw calls. Execution defects return to their owning task with the full affected dependency set and remaining resources/authorization constraints.

## Completion criteria

- A reproducible audit report identifies actual scope, coverage, unresolved work and supported claims, with artifact-linked comparisons and accounted discrepancies.
- Available records pass consistency checks; any truly unavailable evidence remains explicit and limits conclusions.
- Incomplete/feasibility handoffs may pass this audit for limited reporting while M5/M6 execution gates remain blocked.
- No model call or outcome-adaptive regeneration is needed to reproduce the audit.

## Validation and evidence

Run independent gold and archived-response replays; compare committed states, delivery IDs, table values and counts. Exercise the audit's failure detection on missing/duplicated/mis-scoped records without altering canonical evidence. Retain commands, clean input locations, comparison outputs and the resulting full/limited audit decision.

**Evidence:** Not yet recorded. Audit completion never implies that the intended experimental schedule completed.

