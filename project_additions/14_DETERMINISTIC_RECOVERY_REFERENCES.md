# 14 — CPU references that explain what the LLM had to do

**Recommendation: include two small references, with a third simple visibility annotation. Additional model calls: 0. Estimated work: 1–2 focused days beyond the exact evaluators.**

## The idea and question

Ask **whether a failure arises despite a straightforward exact update, because old work was already wrong, or because the retained representation lacks something necessary**. CPU references make these possibilities concrete.

They are explanatory tools, not fair LLM competitors. A program supplied with all current inputs and the exact mathematical algorithm has different information and capabilities from four private-information models. A statement such as “the CPU solver beats the agents” would add little; using it to verify outcomes and expose a failure is useful.

The reference principles come from standard exact algorithms and incremental computation. No novelty claim is needed to make them worth including.

## Reference 1: exact fresh recomputation

The PS already requires independent before/after gold solvers. Use them to show the exact revised answer and affected coordinates in trace examples, and to verify that an alleged stale answer really belongs to the prior world.

This is **already-required evaluation**, not a new experiment or added inference baseline. Gold and D/U remain outside every model prompt. CPU runtime can be recorded for reproducibility, but it must not be interpreted as an estimate of how quickly an LLM team could perform the same work.

## Reference 2: apply the correct update to the model's actual old answer

For Prefix Sum and Difference Array, take the model's round-four prefix candidate exactly as generated, provided it has the required shape. Offline, apply the mathematical delta update using the actual historical and current input values. Then score the resulting candidate against the revised gold. If that boundary candidate is malformed, record the reference as malformed/ineligible; do not backfill an earlier valid answer.

For Prefix Sum, add delta to the candidate coordinates at or after the edited position. For Difference Array, add delta to output coordinate k and subtract it from k+1, omitting nonexistent endpoint coordinates. This is a tiny evaluator-side calculation, not a model tool or repaired answer injected into a branch.

The useful identity is exact: if the true output changes by vector d, then

`(old_candidate + d) - (old_gold + d) = old_candidate - old_gold`.

A correct arithmetic adjustment preserves the prior residual error. It does not repair an old wrong computation merely because the world changed. Conversely, every originally correct coordinate remains correct after this exact adjustment. This gives a concrete benchmark for interpreting whether model recovery improved, preserved or damaged previous work.

### Minimal report

For each of the two families, compare the actual old candidate, this offline adjusted candidate, and the observed B/C recovery candidates. Report exact correctness plus coordinate correctness; retain malformed old outputs as a separate ineligible/malformed category with their denominator. Do not replace them with gold or silently omit them from the main analysis.

Possible outcomes are useful in both directions:

- A model can exceed the adjustment reference by correcting old errors as well as incorporating the edit.
- It can match the reference, preserving the quality of prior work.
- It can fall below it through new calculation or formatting errors.
- If the old answer was poor, the reference shows why blindly preserving it is an unattractive strategy even with a perfect update.

The reference receives the true old value, which may be absent from a model's current prompt. Therefore it is a **conditional, sometimes privileged diagnostic**, not an executable policy competitor or proof that the model failed despite equal information. The [atlas](06_RECOVERY_INFORMATION_ATLAS.md) supplies that information boundary. Do not automatically extend the residual identity to nonlinear max/top-K/sort/BFS updates.

## Visibility annotation: when raw sources alone suffice

At each call, record whether the peer holds a simple sufficient set of current source records for exact fresh recomputation. For a local Prefix Sum segment, all records through that segment's final global position suffice. For complete replicated Difference Array, max/top-K/BFS, or a Sort segment, having every current record is an easy sufficient condition. These are deliberately coarse conditions, not necessary ones.

Missing one raw record does **not** prove insufficient information: a peer may have received a useful aggregate or candidate, and some domain bounds can settle an answer early. Avoid building an elaborate solver for every partial-information case. The coarse annotation already supports a useful observation: wrong output despite a sufficient raw-source view cannot be explained solely by lack of those raw facts. Capability, prompt use, output budget and schema failure remain possible explanations.

Cost: **0 model calls**. Reuse source-table snapshots and evaluator code. No additional semantic extractor or reviewer is required.

## What not to build by default

A full deterministic peer team obeying every source-reference and serialization cap could demonstrate that these small tasks are solvable under the protocol, but implementing six independent distributed algorithms adds little to the central LLM retention question. Free all-to-all forwarding may already make a simple dissemination strategy sufficient; an exact round bound still requires checking the actual tokenized message format.

Likewise, do not give a runtime validator the gold solver and then credit the retention policy for corrected answers. If a future project intentionally studies tool-assisted recovery, that is a new experimental factor and needs its own matched tool access.

## Recommended scope

Keep exact fresh recomputation as the ground truth; add the two linear-task adjustment references and the simple source-coverage annotation. This is a small, useful companion to [task structure](05_TASK_STRUCTURE_AND_RECOVERY.md) and the [atlas](06_RECOVERY_INFORMATION_ATLAS.md). Together they can turn a null B/C result into an informative explanation without spending additional GPU hours.

Basis: [PS task definitions, exact evaluation and state visibility](../PROJECT_SPECIFICATION.md), plus previously checked [update identities and counterexamples](../research_innovation_v2/evidence/PROTOCOL_AUDIT.md). This planning note adds no implementation code or model runs.
