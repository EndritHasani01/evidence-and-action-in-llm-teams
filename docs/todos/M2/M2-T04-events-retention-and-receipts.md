# M2-T04 — Literal events, retention boundaries and receipts

**Status:** active

**Dependencies:** [M2-T03](../M2/M2-T03-synchronous-rounds-and-prefixes.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md) and [plan M2 differential checks](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§2.3](../../../PROJECT_SPECIFICATION.md#23-events-and-populations), [§4.1](../../../PROJECT_SPECIFICATION.md#41-what-each-peer-retains), [§4.2](../../../PROJECT_SPECIFICATION.md#42-complementary-groups-recovery-is-a-team-intervention), and [§4.3](../../../PROJECT_SPECIFICATION.md#43-historical-information--retained-representation).
- Technical evidence: [state boundaries](../../implementation-research/state-and-replay.md#semantics-that-belong-to-the-application).

## Intended outcome

Each event and retention policy creates exactly its prescribed starting state from a fresh copy of the original drained prefix.

## Scope and boundaries

- Use explicit small policy cases and deterministic transformations, not a generalized intervention language.
- Main revision and preserving revision invalidate v1 everywhere, publish the same permitted persistent notice and deliver v2 according to L/broadcast. Unknown v2 remains pending; BFS tombstone endpoints are hidden until content delivery.
- Sham keeps all sources unchanged and gives every peer the same neutral continue-solving notice.
- B retains derived work. C clears history, candidate and feedback. K retains exactly its own protocol-valid prefix-round-four candidate, even if wrong, or an absence marker. F clears derived work and acquired remote sources while keeping its corrected private shard and broadcast revision.
- Mixed masks use the corresponding B/C boundary per peer. Initial B/C/K/mask current sources are identical within an event; C/F differ only in retained acquired remote evidence.
- BΔ/CΔ/KΔ add genuine archived before-values with changed ID/owner/versions/public position outside current lookup. Ordinary receipts say "not included in this receipt", without claiming the value is absent everywhere. Current v2 content is identical across receipt modes.
- Never include a computed delta, formula, footprint, corrected candidate or extra unchanged record in receipts. All policies accumulate ordinary new history after the boundary; K is not continual compression.

## Completion criteria

- Every policy/event/subset uses the original prefix, including preserving siblings and repeats.
- Transformations preserve the parent and all siblings, notices/receipts survive clearing, and source updates never rewrite a candidate.
- Boundary application is identifiable for later apply-once checkpoint integration.
- Receipt contrasts change only the specified disclosure package and record its actual token cost.

## Validation and evidence

Run the plan's L/B, B/C/K/mask, C/F, sham and receipt differential fixtures, including wrong/invalid fourth-round candidates and richer earlier candidates that must not be backfilled. Test old values in retained prose, remote acquired evidence, unknown replacements, tombstones and nested mutations. Include CPU v1→v2→v3 authority tests without introducing a live second revision or new arms.

**Evidence:** Not yet recorded. Add boundary snapshots, paired renders and executed results before marking done.

**Start checkpoint (4 October 2026):** The clean `7f56c1b` checkout passes
`python -m recovery validate`: 121 CPU checks on Windows / CPython 3.11.9.
M1's gate and M2-T03's drained-prefix, replacement-state and delivery interfaces
are confirmed. Implementation will use explicit event/policy cases, the saved
world/branch identities and existing source/receipt layouts. Exact mixed/Q
reply reuse, complete capacity and durable apply-once execution remain later
tasks; this task supplies identifiable, serializable boundary results.

**Implementation checkpoint:** [events.py](../../../recovery/events.py) starts
each scheduled continuation from its original drained prefix and applies the
literal event/retention rule. Seventeen focused CPU checks in
[event_checks.py](../../../tests/event_checks.py) pass, including every
scheduled non-Q boundary in both saved mathematical-size populations and
development sets. All 61 existing view/protocol/round checks also pass.
Persistent notices identify boundary application without another stored flag
or ID. The numeric ordinary receipt layout also appears in L/F/masks, preserving
delivery/reset contrasts; an ordinary pending receipt has no before-value or
replacement payload. Disclosed before-values still require delivered v2.
Native paired artifacts, final source/installed checks and handoff remain open.

**Native checkpoint:** Four checks in
[tokenizer_events.py](../../../tests/tokenizer_events.py) pass using pinned
Qwen3.5-9B revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a` on Windows /
CPython 3.11.9, Pydantic 2.12.5, Transformers 5.12.0, Tokenizers 0.22.2,
Jinja2 3.1.6 and Hugging Face Hub 1.19.0. The retained
[boundary archive](../../../tests/fixtures/event_boundaries.json) contains
four original prefixes, 15 complete boundary snapshots and 60 exact first
requests/native sequences, including all six receipt pairs across Prefix Sum
and Sort. Actual complete-input disclosure differences are −4 tokens per peer
for the saved Prefix Sum pairs and −3 for Sort; no padding is added. Dynamic
native checks cover all five families/both sizes, exact mixed-parent requests,
and full ordinary history accumulation in four representative continuations.
Observed boundary inputs are 736–3,218 tokens plus the full 384 output reserve;
prefix replies are 3–269 tokens. These are fixture measurements, not complete
capacity, replay, model or empirical admission. Final regression checks remain.

**Prerequisite handoff (4 October 2026):** [M2-T03 completion](M2-T03-synchronous-rounds-and-prefixes.md#completion-and-handoff)
passes 121 source/installed CPU checks and 14 native-tokenizer checks. Its
immutable, fully drained original prefix retains all current sources, own/
received history, actual fourth-slot candidate/absence, feedback and delivery
audit. `fork_prefix` deep-deserializes each fresh continuation with its original
parent ID; `PeerState` supports literal replacement while persistent notice/
receipt fields remain separate. `RoundResult.barrier` preserves exact original
requests/replies for the subsequent replay task. Use these interfaces without
repairing candidates or treating an untransformed scripted continuation as an
implemented event/policy. This task is ready; its transformations and paired
renders remain unimplemented, and M2's gate is open.

