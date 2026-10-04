# M2-T02 — Strict reply validation and public feedback

**Status:** active

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

**Evidence:** Implementation started 4 October 2026 from clean commit `fd44e57`.
The prerequisite source command `python -S -m recovery validate --manifest
tests/fixtures/population_target.json --schedule tests/fixtures/schedules_target.json
--authoritative tests/fixtures/population_target.json` passed all 79 checks on
Windows / CPython 3.11.9. M1's gate and M2-T01's artifacts are present.

**Implementation checkpoint:** [protocol.py](../../../recovery/protocol.py)
implements the complete decoder, strict nested Pydantic schemas, public candidate
contracts, sender-view permissions, physical output/prose/feedback caps and
all-or-none immutable staging. [protocol_checks.py](../../../tests/protocol_checks.py)
passes 23 focused CPU checks on both local Pydantic 2.12.5 and installed 2.13.5
with CPython 3.11.9. The initial full source integration passed 102 checks;
final integration follows the additional missing-dependency CLI regression.
`pip check` passes in `.venv`. Pydantic 2 is the required schema dependency;
`validate --core-only` explicitly preserves the earlier standard-library subset.
No accepted inference environment or scientific configuration is changed.

**Native-tokenizer checkpoint:** [tokenizer_protocol.py](../../../tests/tokenizer_protocol.py)
passes six checks against the 20 saved synthetic cases in
[protocol_replies.json](../../../tests/fixtures/protocol_replies.json). Qwen3.5-9B
revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a` uses Transformers 5.12.0,
Tokenizers 0.22.2, Jinja2 3.1.6 and Hugging Face Hub 1.19.0 in the local CPU
environment. All four metadata files (`config.json`, `tokenizer.json`,
`tokenizer_config.json`, `chat_template.jinja`) match the pinned upstream bytes
in a fresh comparison. No weights are loaded. Eight distinct references with
nine actual delivery attempts pass; nine distinct references fail. Aggregate
128/129 prose tokens produce valid/invalid replies at 180/181 generated tokens.
A complete closing brace at token 384 is accepted with length termination;
385 tokens and a truncated fragment at 384 are invalid. All fixed feedback fits
32 actual tokens. The five M2-T01 native checks still pass with unchanged saved
requests/token IDs. [Fixture documentation](../../../tests/fixtures/README.md#strict-replies-and-actual-tokenizer-limits)
records reproduction and the remaining capacity/inference boundaries.

Executed native commands:

```powershell
python -m tests.tokenizer_protocol --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_peer_views --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
```

**Prerequisite handoff (4 October 2026):** [M2-T01 completion evidence](M2-T01-peer-views-and-rendering.md#completion-and-handoff)
passes with 79 standard-library CPU checks and five native-tokenizer checks.
Immutable permitted views, held-current-source lookup, literal request rendering,
candidate absence/age guards and fixed public feedback layouts are available.
This task is ready; its strict parser, whole-reply validation and tokenizer
permissions remain unimplemented. M2's complete protocol/capacity gate is open.

