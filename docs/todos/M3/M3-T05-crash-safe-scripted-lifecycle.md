# M3-T05 — Crash-safe scripted lifecycle acceptance

**Status:** ready

**Dependencies:** [M3-T04](../M3/M3-T04-accounting-progress-and-budget.md). The M2 gate must have passed.
M2 passed and M3-T04 completed on 5 October 2026. Use its
[CPU evidence](M3-T04-accounting-progress-and-budget.md#validation-and-evidence),
manifest-derived status, exact physical/policy joins, allocation intervals and
confirmed-release budget stops. Keep recorded failures, unexecuted slots and
uncertain interrupted work distinct when integrating the killed-process suite.

## References

- [Repository contract](../../../AGENTS.md) and [plan M3 acceptance](../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Specification [§4.2](../../../PROJECT_SPECIFICATION.md#42-complementary-groups-recovery-is-a-team-intervention), [§4.4](../../../PROJECT_SPECIFICATION.md#44-early-prose-availability-with-current-sources-fixed), and [§9 checks](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [limits of the toy probe](../../implementation-research/state-and-replay.md#remaining-implementation-validation-not-further-framework-research).

## Intended outcome

The integrated durable runner produces an auditable CPU run bundle and survives real process crashes across the critical persistence/delivery boundaries.

## Scope and boundaries

- Exercise every family, event/intervention, control and repeat path in a tiny scripted fixture. Full main/pilot manifests must reconcile, without executing every possible scripted slot or making any model call.
- Kill a real subprocess before response commit, after durable reply, during validation/staging and before/after delivery checkpoint. Cover a cross-worker replay parent and Q with held prose.
- Compare uninterrupted and resumed authoritative states, delivery records and derived outcomes. Only documented physical attempts/allocation may differ due to interruption.
- Include invalid parent responses, known timeouts, uncertain pre-persistence inference, exhausted infrastructure retries, cleared fields and persistent notices.
- Validate supported backup/close/reopen and progress reconstruction. Archive evidence in the ordinary run bundle, not a separate persistence or test-management system.

## Completion criteria

- Completed outputs remain unchanged; no completed invalid/timeout result is resampled; infrastructure attempts remain bounded.
- No duplicated delivery, restored cleared field, repeated boundary application, premature/lost held prose or mutation of parent/sibling snapshots occurs.
- Exact mixed/Q equality/reuse and branch-local effects survive restart and worker relocation.
- All schedule/cost/progress joins reconcile, including synthetic budget exhaustion with explicit unknown slots.
- The CPU fixture contains the fields needed for M4 outcomes, diagnostics, costs and report reproduction.
- Close M3 only after all M3 evidence passes and is linked from the plan. M4 remains mandatory before GPU use.

## Validation and evidence

Record the actual killed-process commands, crash boundaries, SQLite/durability settings, environments, fixture IDs, comparison outputs and reopened backup paths. A raised exception or the historical nine-check toy is insufficient evidence. Fix discovered defects in their owning implementation, rerun the affected checks, and preserve the accepted integrated fixture for offline analysis.

**Evidence:** Not yet recorded. These are deterministic runtime checks, not pilot or empirical results.

