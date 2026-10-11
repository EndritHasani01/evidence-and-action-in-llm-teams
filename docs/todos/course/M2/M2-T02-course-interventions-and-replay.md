# Course M2-T02 — Course interventions and exact replay

**Status:** done

**Dependencies:** [M2-T01](M2-T01-course-protocol-and-limits.md).

## References

- [Specification interventions](../../../../PROJECT_SPECIFICATION.md#4-recovery-interventions-and-their-controls), [synchrony](../../../../PROJECT_SPECIFICATION.md#32-synchronous-rounds-and-replies), accepted course clause and [plan state/barriers](../../../IMPLEMENTATION_PLAN.md#2-small-implementation-architecture).
- Existing [rounds/prefixes](../../M2/M2-T03-synchronous-rounds-and-prefixes.md), [events/receipts](../../M2/M2-T04-events-retention-and-receipts.md), [mixed/Q replay](../../M2/M2-T05-mixed-and-prose-delay-replay.md), and [state/replay investigation](../../../implementation-research/state-and-replay.md).

## Intended outcome

Every course event/retention/receipt/mask/Q branch preserves the implemented scientific state and delivery semantics under its new inputs and settings.

## Scope and boundaries

- Reuse synchronous freeze/render/obtain/validate/stage/deliver barriers and all four opportunities per round. Physical invocation order never changes visibility. Drain prefix-round-four deliveries and start each sibling from fresh deep-deserialization; apply its original-prefix event/boundary once.
- Verify v1 invalidation, owner-only L delivery, broadcast B/C/K/mask source equality, persistent public notices, pending replacements and known tombstones. Sham leaves sources unchanged and gives every peer the same neutral continue-solving notice while applying its retention boundary. C clears history/candidates/feedback; F also drops acquired remote evidence but keeps the corrected private shard; K retains exactly its own actual valid round-four candidate or absence, including wrong answers. New ordinary history accumulates after every boundary. Keep CPU v1-to-v2-to-v3 checks without adding a live second edit.
- Genuine before-values appear only in the intended receipt field, never current lookup/forwarding. Ordinary receipts say the before-value is not included, without falsely declaring it unavailable everywhere. No delta formula, corrected candidate, relevant-coordinate advice, extra sources or padding arms are supplied.
- Mixed first rounds use exact corresponding B/C raw replies, including invalid/failure outcomes, after permitted-state/rendered/native-token/settings/seed equality. Assemble mixed outgoing replies before independent branch-local effects; never import parent post-delivery state. Parent event/replicate identities remain exact.
- Q replays its B/C first round, delivers sources normally before round two, hides only received first-round prose, and releases it before round three ahead of second-round prose in generation/sender order. Preserve own replies, no held-text placeholders/leakage or duplicate delivery, and record inactive Q. Do not add crossings or announce teammate masks/queue policy.

## Completion criteria

- All scheduled course branch starts and replay parents pass equality/retention/source/queue assertions, including wrong K and invalid parent cases.
- Invocation-order reversal and sibling mutation tests preserve committed scripted behavior; course limit/settings mismatches reject replay.
- Metadata needed for availability, receipt cost, exposure and source/prose timing is retained in existing records.

## Validation and evidence

Run focused course scripted comparisons across all events/policies and small numeric/BFS instances, pending/tombstone/hidden-value cases, repeated deliveries, Q round-two source/own-reply equality and ordered release. Preserve raw parent/state artifacts and demonstrate no boundary mutation of the shared prefix. Existing passing libraries need only affected regression checks.

**Evidence:** Completed 10 October 2026 from `e46bd40` on
`feat/course-m1-contract-and-inputs`. The prerequisite protocol completion audit
passes at this starting commit. The [intervention evidence](../../../validation/course-m2-interventions-and-replay.md)
records the complete acceptance matrix, exact commands, environments, raw native
artifacts, retained failures/corrections and preservation/installed checks.

**Prerequisite handoff, 9 October 2026:** Course/M2-T01 passes its
[protocol and limits acceptance](../../../validation/course-m2-protocol-and-limits.md#completion-and-handoff).
Use `COURSE_LIMITS` explicitly for in-memory rounds and the pinned 4B
`candidate_settings(..., limits=COURSE_LIMITS)` for exact-settings consumers.
The existing round, replay, durable runner and saved-round revalidation paths
carry those settings without changing archived reply/state schemas. Native
256/64 boundaries, wrong-but-valid shapes, genuine receipts, permission checks
and thesis compatibility are verified. This hands off the real renderer and
validator; it does not accept all course intervention branches, the complete
witness/context bound or any GPU/model, pilot, freeze or main execution.

## Completion and handoff

All course intervention/replay criteria pass through the existing implementation.
The only production adaptation adds explicit `limits` to `run_prefix`, preserving
its thesis default; the full CPU CLI registers the new course suite. No event,
retention, replay, state/delivery semantics, schema, dependency, ID, store, input,
scientific contract or runtime freeze changes.

The affected source regression passes 127 checks; the outside-checkout installed
package passes 95 with hash seed 37 and all 29 module bytes verified. Both have
zero skips. The pinned local 4B tokenizer passes the same 15 course assertions
plus three archive checks, repeated in a fresh hash-seed-37 process. This covers
25 main/development worlds, all 438 scheduled starts and 592 prescribed parent
joins, and all 7,008 scripted continuation slots. The
[native archive](../../../../tests/fixtures/course_interventions.json.gz)
retains 100 prefix rounds, 630 continuation rounds and 2,920 exact peer requests,
including full Q release horizons and eight inactive Q starts. Wrong K, invalid/
failed parents, hidden pending/tombstone payloads, ordered idempotent delivery,
source/receipt timing metadata and nested sibling isolation are verified.

[Course/M2-T03](M2-T03-course-attainability-and-capacity.md) is ready. Reuse the
saved course population/schedule and `run_prefix(..., limits=COURSE_LIMITS)`;
continuations take pinned 4B `candidate_settings(..., limits=COURSE_LIMITS)`.
Retain exact B/C `SavedRound` parents for each event/replicate and use the existing
obtain/save/commit boundaries. The fixtures are protocol acceptance, not a locally
informed attainability witness or complete context bound. Course M2's gate remains
open for both proofs; worker/accounting, actual model/GPU, pilot, resource admission,
freeze, empirical execution and external delivery remain their separate tasks.
