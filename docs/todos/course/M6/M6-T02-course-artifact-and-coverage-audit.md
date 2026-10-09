# Course M6-T02 — Course artifact and coverage audit

**Status:** blocked

**Dependencies:** [M4-T04](../M4/M4-T04-course-report-and-cpu-gate.md), plus the alternative evidence handoff below. A failed feasibility gate need not be passed to audit limited evidence.

## References

- [Specification exact outcomes](../../../../PROJECT_SPECIFICATION.md#51-exact-outcomes), [statistics/missingness](../../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), [seven consistency categories](../../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements), and [plan M6 audit](../../../IMPLEMENTATION_PLAN.md#8-milestone-m6--complete-execution-audit-and-reproducible-results).
- [Existing artifact audit](../../M6/M6-T02-independent-artifact-audit.md), accepted course clause, and applicable course freeze or terminal feasibility decision.

## Intended outcome

An independent offline audit determines exactly which course claims and coverage the recorded evidence supports, including failed feasibility or incomplete execution.

## Scope and boundaries

- Accept one quiescent evidence handoff: complete or safely stopped [course M6-T01](M6-T01-course-frozen-execution-and-resume.md), OR documented terminal feasibility evidence from the course [preparation](../M5/M5-T01-course-inference-and-smoke-preparation.md), [smoke](../M5/M5-T02-course-hardware-smoke-and-memory.md), [capability](../M5/M5-T03-course-capability-first-pilot.md), [pilot](../M5/M5-T04-course-complete-pilot-and-timing.md) or [admission](../M5/M5-T05-course-admission-and-freeze.md) stage. Do not require main execution or a successful freeze for the limited route.
- Join original manifests, immutable prefixes, raw calls/attempts, replay parents, delivery/checkpoint records and exports. Audit source visibility/versioning/tombstones, literal boundaries, mixed/Q view/request/settings/seed equality, parent scope, Q release ordering, grouping/denominators, repeat identities and environment consistency.
- Independently recompute gold and replay archived delivery/evaluation without inference. Compare committed checkpoints and exported tables; preserve one canonical source of evidence rather than building another store.
- Reconcile physical/policy costs, provider allocations, recorded failures versus unknowns, shared logical-response identities, coverage and superseded defect/rerun records. Duplicated IDs, inconsistent joins and unexplained missing records fail the audit; intentional unexecuted slots remain explicit.
- Review all seven specification consistency categories for the actual scope. For feasibility-only evidence, audit available CPU/pilot/allocation records and mark main outcomes, freeze and unexecuted gates unavailable; development rows cannot stand in for main estimates.
- Return execution defects to their owning task with complete affected dependencies/resources; repair pure analysis defects from unchanged raw evidence. Never delete important artifacts or resample unfavorable answers to make the audit pass.

## Completion criteria

- A reproducible audit links each scope/coverage/consistency claim to independent comparisons and explains all discrepancies and limitations.
- Available records pass the applicable checks; genuinely unavailable evidence is identified and limits conclusions. The original intended population remains visible.
- A limited audit can pass while M5/main execution remains blocked or unfinished; no completed empirical study is claimed.

## Validation and evidence

Run independent gold and archived-response replay, compare states/deliveries/tables/counts, and demonstrate detection of missing/duplicate/mis-scoped records on copies. Record input/bundle identities, named commands, comparison outputs and the full or limited audit decision; no model calls are required.

**Evidence:** Not yet recorded. The alternative handoff is unavailable.
