# Course M2-T02 — Course interventions and exact replay

**Status:** blocked

**Dependencies:** [M2-T01](M2-T01-course-protocol-and-limits.md).

## References

- [Specification interventions](../../../../PROJECT_SPECIFICATION.md#4-recovery-interventions-and-their-controls), [synchrony](../../../../PROJECT_SPECIFICATION.md#32-synchronous-rounds-and-replies), accepted course clause and [plan state/barriers](../../../IMPLEMENTATION_PLAN.md#2-small-implementation-architecture).
- Existing [rounds/prefixes](../../M2/M2-T03-synchronous-rounds-and-prefixes.md), [events/receipts](../../M2/M2-T04-events-retention-and-receipts.md), [mixed/Q replay](../../M2/M2-T05-mixed-and-prose-delay-replay.md), and [state/replay investigation](../../../implementation-research/state-and-replay.md).

## Intended outcome

Every course event/retention/receipt/mask/Q branch preserves the implemented scientific state and delivery semantics under its new inputs and settings.

## Scope and boundaries

- Reuse synchronous freeze/render/obtain/validate/stage/deliver barriers and all four opportunities per round. Physical invocation order never changes visibility. Drain prefix-round-four deliveries and start each sibling from fresh deep-deserialization; apply its original-prefix event/boundary once.
- Verify v1 invalidation, owner-only L delivery, broadcast B/C/K/mask source equality, persistent public notices, pending replacements and known tombstones. C clears history/candidates/feedback; F also drops acquired remote evidence; K retains exactly its own actual valid round-four candidate or absence, including wrong answers. New ordinary history accumulates after every boundary. Keep CPU v1-to-v2-to-v3 checks without adding a live second edit.
- Genuine before-values appear only in the intended receipt field, never current lookup/forwarding. No delta formula, corrected candidate, relevant-coordinate advice, extra sources or padding arms are supplied.
- Mixed first rounds use exact corresponding B/C raw replies, including invalid/failure outcomes, after permitted-state/rendered/native-token/settings/seed equality. Assemble mixed outgoing replies before independent branch-local effects; never import parent post-delivery state. Parent event/replicate identities remain exact.
- Q replays its B/C first round, delivers sources normally before round two, hides only received first-round prose, and releases it before round three ahead of second-round prose in generation/sender order. Preserve own replies, no held-text placeholders/leakage or duplicate delivery, and record inactive Q. Do not add crossings or announce teammate masks/queue policy.

## Completion criteria

- All scheduled course branch starts and replay parents pass equality/retention/source/queue assertions, including wrong K and invalid parent cases.
- Invocation-order reversal and sibling mutation tests preserve committed scripted behavior; course limit/settings mismatches reject replay.
- Metadata needed for availability, receipt cost, exposure and source/prose timing is retained in existing records.

## Validation and evidence

Run focused course scripted comparisons across all events/policies and small numeric/BFS instances, pending/tombstone/hidden-value cases, repeated deliveries, Q round-two source/own-reply equality and ordered release. Preserve raw parent/state artifacts and demonstrate no boundary mutation of the shared prefix. Existing passing libraries need only affected regression checks.

**Evidence:** Not yet recorded. Original intervention/replay code exists; course-scoped acceptance is pending.
