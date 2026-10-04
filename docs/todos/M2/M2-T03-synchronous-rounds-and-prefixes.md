# M2-T03 — Synchronous rounds and immutable shared prefixes

**Status:** active

**Dependencies:** [M2-T02](../M2/M2-T02-strict-replies-and-feedback.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md), [plan round procedure](../../IMPLEMENTATION_PLAN.md#round-execution-persistence-and-worker-ownership), and [M2](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§2.2](../../../PROJECT_SPECIFICATION.md#22-sampling-and-reproducibility), [§3](../../../PROJECT_SPECIFICATION.md#3-common-peer-protocol), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [state semantics](../../implementation-research/state-and-replay.md#semantics-that-belong-to-the-application).

## Intended outcome

A deterministic in-memory round runner executes scripted replies through the real views, renderer, validator and source/text delivery interface, and produces a drained immutable prefix.

## Scope and boundaries

- Use the fixed barrier: freeze four views, render all requests, obtain replies, validate all, stage outgoing source/text effects, commit together, then advance. Serial physical invocation must not expose current-round output.
- All four peers receive four prefix and four continuation opportunities. Submission, success, invalid replies and silence never deactivate peers.
- Forward exact payloads only from sender-held current references. Never fetch unseen records or compute aggregates for peers. Treat free text/candidates as untrusted derived work.
- Record sender/recipient, source ID/version or text, generation round, first usable round, host/agent origin and stable branch-scoped message relationships. Track delivery attempts separately from unique acquisitions.
- Drain prefix-round-four messages before snapshot serialization. Preserve enough state for new siblings, replay pre-delivery barriers and later queue/checkpoint integration; no persistence framework is required yet.
- Archive rendered owner-v1 exposure and all four prefix rounds. Exposure is a factual check, not proof of model use or a world-selection rule.

## Completion criteria

- Reversing peer invocation order produces identical scripted committed states, messages and outcomes.
- No recipient can observe another peer's current-round reply before the barrier.
- A prefix round-four snapshot has no pending deliveries and can be deep-deserialized without nested sharing.
- The in-memory procedure can later accept event-specific retention and delivery rules without changing protocol semantics.
- Delivery metadata provides the timing/origin/acquisition fields required by later analysis without leaking hidden payloads into prompts.

## Validation and evidence

Exercise source-plus-text, text-only, empty and wholly invalid replies; repeat source references; tombstone versus pending coverage; and all four scheduled opportunities after early success/failure. Mutate nested state in one deserialized sibling and assert original/other siblings unchanged. Verify full round-four drain and owner-v1 rendered exposure from actual requests.

**Evidence:** Not yet recorded. Add scripted traces, order-reversal assertions and command/environment results before marking done.

**Start checkpoint (4 October 2026):** The clean `405a171` checkout passes
`python -m recovery validate`: 103 CPU checks on Windows / CPython 3.11.9,
Pydantic 2.12.5. M1's recorded gate and M2-T02's staging handoff are confirmed
against the current interfaces. Work is limited to the deterministic in-memory
barrier, delivery records and drained prefix; durable execution, event policies,
mixed/Q replay and complete capacity remain their subsequent tasks.

**Prerequisite handoff (4 October 2026):** [M2-T02 completion](M2-T02-strict-replies-and-feedback.md#completion-and-handoff)
passes 103 source/installed CPU checks, six native protocol checks and the five
unchanged native renderer checks. `validate_reply` returns separate validity
stages, literal generated text/IDs, candidate absence/validity, public feedback
and immutable staged messages resolved only from sender-held current sources.
Repeated references preserve separate delivery attempts; no effects are applied.
Use these records for the fixed four-view barrier and assign message/delivery
relationships here. This task is ready; synchronous commits and drained immutable
prefixes remain unimplemented. M2's complete protocol/capacity gate remains open.

