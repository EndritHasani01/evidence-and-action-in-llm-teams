# M2-T06 — Protocol attainability and complete tokenizer capacity

**Status:** in progress

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

**CPU witness checkpoint (4 October 2026):** [witness.py](../../../recovery/witness.py)
accepts only a permitted local view, forwards each current private shard to a
different peer in rounds 1–3, and uses the existing mathematical functions only
after all current records are locally held. Pending replacements prevent solving;
known BFS tombstones are excluded from the local active graph. Legal placeholders
fill earlier slots. Active prose exercises Q without contributing solver input.
All five [attainability checks](../../../tests/attainability_checks.py) pass with
the injected CPU counter (`python -m unittest tests.attainability_checks -q`):
five families, both sizes, every scheduled sibling/repeat of the first saved
world per family, full-information controls, L replacement timing, F reacquisition,
and reversed invocation order. The full CPU entry point includes these checks.
Native witness traces, actual output token tables and complete capacity admission
were still open at this checkpoint. No scripted evidence is a model-capability result.

**Native witness checkpoint:** Four checks in
[tokenizer_attainability.py](../../../tests/tokenizer_attainability.py) pass using
the pinned Qwen3.5-9B tokenizer. The losslessly compressed
[local-view archive](../../../tests/fixtures/attainability_traces.json.gz) retains
10 family/size cases, 1,080 four-peer rounds plus 20 controls, 4,340 calls and
384 exact parent joins. Sources, delivery labels, physical output IDs, solver
availability, Q queues/release and actual reply serialization reproduce. Every
prefix and continuation attains joint correctness by round four; controls are
correct. Inputs use 699–4,915 tokens plus the full 384 output reserve; actual
witness replies use 20–195 tokens. Correct-width candidate/control/one-shard
fixtures use at most 210 tokens at target and 162 at fallback. Compression is
only for the offline evidence file; peer rendering and retention are unchanged.
Complete capacity admission remains open and adversarial investigation has
identified a real overflow; this checkpoint does not close M2.

**Prerequisite handoff (4 October 2026):** [M2-T05 completion](M2-T05-mixed-and-prose-delay-replay.md#completion-and-handoff)
passes 158 source/installed CPU checks and all 22 native-tokenizer checks.
`start_continuation` now supplies Q's parent-equivalent boundary.
`obtain_continuation_round` captures scheduled settings/seeds/replies in an
in-memory `SavedRound`; mixed/Q round one requires exact matching B/C parent
records, including invalid/failed outcomes. `commit_continuation_round` assembles
branch-local effects and Q source/prose delivery, with chronological release
before round three. Use this pair for the witness's scheduled continuations;
the provider receives permitted view/render/native input plus keyword seed and
settings. Held counts derive from committed queues/deliveries. The retained
54-round native replay archive verifies controls and timing, not attainability
or complete capacity. Durable save-before-effects integration remains M3.

