# M2-T02 — Strict reply validation and public feedback

**Status:** blocked

**Dependencies:** [M2-T01](../M2/M2-T01-peer-views-and-rendering.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md) and [plan M2](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§3.2](../../../PROJECT_SPECIFICATION.md#32-synchronous-rounds-and-replies), [§5.1](../../../PROJECT_SPECIFICATION.md#51-exact-outcomes), and [§8.1](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls).
- Technical evidence: [strict parsing](../../implementation-research/repository-and-validation.md#strict-parsing-needs-two-small-layers).

## Intended outcome

A complete reply receives one deterministic protocol-valid/invalid result, with lawful messages and bounded public feedback, without judging or repairing mathematical correctness.

## Scope and boundaries

- Decode one complete JSON object before strict Pydantic 2 validation. Reject duplicate keys recursively, nonfinite constants/overflow/coercion, booleans/floats/strings as integers, extra nested fields, fences, trailing prose and incomplete fragments.
- Require candidate/send schemas, task-specific integer shapes and canonical full BFS keys. Full-information controls require empty sends and complete-world candidate lengths.
- Validate against the immutable sender view: another peer as recipient, at most one message per recipient/three total, and at most eight distinct currently held ID/version references per recipient. Repetition of a valid reference is not independently forbidden by the distinct-reference limit.
- Apply actual tokenizer limits: 384 generated tokens, 128 prose tokens summed across message texts and at most 32 feedback tokens per slot. Complete valid JSON at the output cap is valid; record termination separately from truncation.
- Any invalid message invalidates the entire reply, including its candidate and all sends. Wrong numbers in a structurally valid candidate remain valid protocol output.
- Deliver only schema/permission feedback at the next scheduled call. Never echo hidden payloads, library validation dumps, correctness, or extra opportunities. Failed/invalid slots have no new candidate; never inherit an earlier answer.

## Completion criteria

- Parsing, structural validity, permissions, token limits and numeric correctness are separate concepts and outputs.
- Invalid replies produce zero staged messages and an explicit invalid/absent candidate.
- Raw replies remain unchanged for audit/history under the retention contract; no JSON repair, sorting, fragment extraction or schema-constrained generation is introduced.
- Feedback remains useful, public and within the actual token cap.

## Validation and evidence

Test duplicate keys at every nesting level, nonfinite/huge exponent tokens, coercions, wrong lengths, BFS key "01", extra fields, self/unknown/duplicate recipients, stale/unheld refs, repeated lawful refs, per-recipient distinct-reference limits and aggregate prose limits. Include a valid candidate with one invalid send, wrong but valid integers, complete cap-ending JSON, malformed outputs below/at cap, failed slots, and feedback sentinel leaks. Preserve repeated delivery attempts for later accounting.

**Evidence:** Not yet recorded. Add adversarial fixture results, tokenizer identity and executed commands before marking done.

