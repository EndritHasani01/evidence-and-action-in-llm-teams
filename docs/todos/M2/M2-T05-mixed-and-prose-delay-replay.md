# M2-T05 — Exact mixed-group replay and prose-delay delivery

**Status:** active

**Dependencies:** [M2-T04](../M2/M2-T04-events-retention-and-receipts.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md), [plan round/replay architecture](../../IMPLEMENTATION_PLAN.md#round-execution-persistence-and-worker-ownership), and [M2](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§4.2](../../../PROJECT_SPECIFICATION.md#42-complementary-groups-recovery-is-a-team-intervention), [§4.4](../../../PROJECT_SPECIFICATION.md#44-early-prose-availability-with-current-sources-fixed), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [exact response reuse](../../implementation-research/state-and-replay.md#exact-reuse-is-different-from-framework-replay).

## Intended outcome

Mixed and Q branches consume exact parent first-round records and reconstruct their own deliveries with the required equality and delay controls.

## Scope and boundaries

- Before reuse compare exact rendered request, settings, saved seed and permitted state with the same-event/same-replicate B or C parent. Any mismatch is a protocol defect.
- Reuse raw replies and recorded invalid/failure outcomes. Seeds, framework replay or similar prompts do not authorize regeneration or unrelated caching.
- Mixed branches select the B/C parent appropriate to each peer, assemble the outgoing set, then apply effects inside that branch. Never copy parent post-delivery recipient tables.
- Q replays the entire B/C first round, delivers validated sources normally, retains senders' own replies, and holds only incoming round-one prose until before round three.
- Before round two, Q and parent current sources, own reply and source-delivery metadata match. Held text must not leak through summaries, placeholders, candidate sharing, feedback or queue metadata; text-only sends create no revealing placeholder.
- At the round-three boundary append held round-one prose before round-two prose, ordered by generation round/sender with stable IDs. Preserve already-seen history order and then resume ordinary delivery.
- Use the M2 in-memory saved records now; durable reuse is M3. Count held/no-held prose so inactive Q treatments remain reportable and included.

## Completion criteria

- Mixed/Q first-round generation opportunities are satisfied solely by their exact prescribed parent records.
- Recipient effects, queues and applied message IDs are independent per branch; the same saved send may affect each sibling once.
- Both complementary masks, revised/sham Q and extra-replicate parent scoping pass fixtures.
- Q neither changes the horizon nor permanently drops/reorders already-seen text; later acquisition divergence remains an outcome.

## Validation and evidence

Include invalid parents, failed parents, mixed source-plus-prose sends, text-only sends, no prose, duplicate attempts, tombstones and deliberately mismatched requests/settings/seeds/views. Assert branch-local mixed assembly, round-two source/own-reply equality, no hidden held-text sentinel, chronological release, no duplicate history and unchanged parent/sibling states.

**Evidence:** Not yet recorded. Add exact-parent comparisons, queue traces and executed results before marking done.

**Start checkpoint (4 October 2026):** Clean prerequisite `fac764f` passes
`python -m recovery validate`: 140 CPU checks on Windows / CPython 3.11.9.
The current specification, plan, synthesis, replay investigation and M2-T04
handoff have been inspected. Implementation will reuse the existing pre-delivery
barrier, validated schedule IDs, source/text component queue and pure delivery
functions. In-memory saved settings/seeds/replies will govern exact reuse;
durability remains M3. No scientific or configuration change is required.

**Prerequisite handoff (4 October 2026):** [M2-T04 completion](M2-T04-events-retention-and-receipts.md#completion-and-handoff)
passes 140 source/installed CPU checks and all 18 native-tokenizer checks.
`start_continuation(prefix_bytes, prepared_world, scheduled_branch)` supplies
fresh, literal B/C/mask/event/receipt starts from the original drained prefix;
mixed first views, requests and native IDs exactly match the appropriate B/C
parents. `BranchState.boundary_applied` derives from persistent notices and
survives serialization. Q remains explicitly rejected until this task adds its
parent-equivalent boundary and prose-delay/replay behavior. Use the existing
`RoundResult.barrier`, `stage_effects` and `drain_deliveries` interfaces to reuse
literal saved replies before branch-local delivery, including invalid/failure
outcomes. K's retained fourth-slot result/absence becomes a labeled history
entry once a new recovery slot replaces the latest candidate. This handoff
establishes boundary semantics, not completed exact replay or M2 gate passage.

