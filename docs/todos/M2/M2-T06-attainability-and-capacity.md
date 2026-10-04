# M2-T06 — Protocol attainability and complete tokenizer capacity

**Status:** blocked

**Dependencies:** [M2-T05](../M2/M2-T05-mixed-and-prose-delay-replay.md). M1 must have passed before M2 work begins.

## References

- [Repository contract](../../../AGENTS.md) and [plan M2 acceptance](../../IMPLEMENTATION_PLAN.md#4-milestone-m2--lawful-protocol-and-matched-interventions).
- Specification [§3.2](../../../PROJECT_SPECIFICATION.md#32-synchronous-rounds-and-replies), [§8.2](../../../PROJECT_SPECIFICATION.md#82-cpu-checks-and-bounded-development-pilot), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [tokenizer probe and its limits](../../implementation-research/inference-and-capacity.md#tokenizer-only-capacity-probe) and [remaining gates](../../implementation-research/SYNTHESIS.md#small-remaining-validation-gates).

## Intended outcome

A locally informed scripted strategy proves the real protocol is usable within four recovery rounds, and the complete renderer has a defensible worst-context bound before GPU use.

## Scope and boundaries

- Each scripted peer forwards its own currently held shard to a different peer in the first three rounds, uses legal placeholder candidates earlier, and computes only from acquired local evidence when sufficient. The solver never sees host gold or unseen records.
- Exercise all five families, both size contracts, local/broadcast revision, sham/preserving siblings, resets, receipts, mixed replay and Q through the real schemas and renderer. Include L replacement forwarding and F reacquisition.
- Tokenize actual serialized team/control candidates and useful one-shard messages. The simultaneous maximum prose/reference payload need not fit, but the witness and required output contracts must fit 384 generated tokens.
- Bound actual retained requests over the complete prefix/recovery horizon, reserving all 384 output tokens inside 8,192. Include invalid own replies, maximum received prose, feedback, labels, tables, notices/receipts, source-delivery metadata, escaping, large wrong integers and special-looking strings.
- Use both an accounting argument and adversarial rendered fixtures. Q release cannot duplicate retained history. The research's illustrative context and correct-output examples are not a worst-case proof.

## Completion criteria

- Revised correctness is attained by the lawful scripted strategy within the stated horizon for all required interventions, without privileged solver input.
- Actual candidate/control/witness serialization meets output limits; every permitted retained context for an admitted size/template has a complete capacity argument and passing fixtures.
- Evaluate both declared sizes and state explicitly which pass. Failure at target size can use only lossless representation or the specified uniform fallback, with all affected contracts/witness checks renewed. M5 still determines final accepted size.
- If no permitted contract fits, or the bound has a gap, keep M2 blocked and record the exact incompatibility for an explicit scientific decision. Never truncate history or invent new caps.
- Close M2 only with all six tasks' evidence linked in the plan. This does not permit GPU use: M3 and M4 must also pass.

## Validation and evidence

Retain the local-view witness trace, per-shape token table, tokenizer/template identity, worst-case accounting and adversarial input/output fixtures. Recheck visibility, synchrony, retention and replay against the finalized renderer where it changed. Show requested versus admitted sizes and the command/environment for every capacity result.

**Evidence:** Not yet recorded. No tokenizer-only or scripted evidence is a model-capability result.

