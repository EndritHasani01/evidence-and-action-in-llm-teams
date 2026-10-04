# M6-T01 — Frozen main execution and safe resume

**Status:** blocked

**Dependencies:** [M5-T05](../M5/M5-T05-allocation-admission-and-freeze.md). Passed M5 freeze and explicit authorization for the main experiment/GPU/paid-compute scope are required.

## References

- [Repository contract/authorization](../../../AGENTS.md) and [plan M6](../../IMPLEMENTATION_PLAN.md#8-milestone-m6--complete-execution-audit-and-reproducible-results).
- Specification [§2.2](../../../PROJECT_SPECIFICATION.md#22-sampling-and-reproducibility), [§6](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), [§8.3–8.4](../../../PROJECT_SPECIFICATION.md#83-exact-main-schedule), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).

## Intended outcome

The full frozen main schedule executes within authorized resources, with exact resume semantics, explicit deviations and no outcome-driven omissions.

## Scope and boundaries

- Explicit main-experiment/GPU/paid-compute authorization must cover the concrete accepted bundle, complete schedule and forecast. Prepare this action from M5 evidence first; do not infer authorization from gate passage.
- Run balanced family/world blocks, rotating eligible sibling/device assignment while respecting B/C replay parents. Use one natural prefix/world and all four rounds per phase.
- Check edited-owner v1 rendered exposure and drained immutable prefix snapshots before branching. Include failed prefixes, silence, redundant receipts, harmful policies and inactive Q. Controls/repeats never select treatments or replace replicate zero.
- Monitor status, actual allocation, reserves and conservative remaining forecasts. Stop safely before the frozen ceiling, preserve durable replies and explicitly mark remaining slots unknown. Resume only in the same design and remaining authorized/resource limits.
- Independently verified generator/protocol/leakage/evaluator defects require affected artifact IDs, reason and a documented deviation. Fix and rerun the entire affected matched dependency set; a defective prefix requires a new prefix plus all descendants.
- Preserve superseded artifacts, all attempt costs and the scope of corrections. Pure analysis defects use unchanged raw calls. Never regenerate unfavorable outputs. Scientific/frozen-configuration changes require explicit authorization and renewed gates.

## Completion criteria

- Every slot in the accepted 60/40 manifest is executed or satisfied by its prescribed replay, including controls, preserving subsets and fixed repeats.
- Attempts, failures, exposure, sibling/replay identities and allocation are fully recorded; spending stays within the frozen ceiling.
- Resume/settings checks reject any unapproved change.
- If the schedule cannot be completed, leave this task blocked with original coverage, unknown slots, reason and exact remaining work. A safely stopped evidence bundle may still unblock M6-T02; it does not complete this task or the study.
- Update the plan with coverage, artifact locations and consequential deviations, without claiming release readiness.

## Validation and evidence

Use the frozen schedule/status checks throughout; compare completed logical/distinct/replay totals and family/event/subset matched coverage to the manifest. Retain allocation stop/resume records and defect/rerun dependency decisions. Hand off quiescent checkpoints/databases and all raw/superseded evidence for independent audit.

**Evidence:** Not yet recorded. No main execution is authorized or claimed by this planning task.

