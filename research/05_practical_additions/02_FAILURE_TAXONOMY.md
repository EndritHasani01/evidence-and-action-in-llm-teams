# Addition 02: explain failures with observable labels and a small casebook

**Recommendation: include a lean version. High explanatory value; zero additional model calls.**

**Simple idea:** accompany accuracy with a few precisely defined labels describing what went wrong in the recorded outputs and delivery traces. Then show a small, reproducibly selected set of matched examples, including examples that oppose the preferred interpretation.

**Status:** proposed analysis of future PS runs. Existing repository counterexamples are constructed CPU cases, not naturally observed model failures. This addition does not require a semantic dependency extractor or an LLM judge.

## Question and value

When a policy fails to recover, what can the evidence actually establish? Was the reply malformed, was the authoritative update still absent, did an old answer value persist after receipt, or did a previously correct unaffected output become wrong?

A compact taxonomy makes an unsuccessful or mixed experiment useful. It also prevents the thesis from calling every wrong answer “stale reasoning” or every eventual success “effective correction propagation.”

## Already in the PS versus the addition

The PS already requests protocol-failure counts, old-gold retention on changed coordinates, collateral damage, propagation logs, and illustrative traces. The addition is an explicit annotation dictionary and a reproducible case-selection rule that join those records. It is not a new causal diagnosis engine.

## Minimum annotation set

Use **nonexclusive annotations**. One branch can exhibit several. Do not force all failures into a single presumed root cause, and do not stack overlapping percentages as if they sum to 100%.

| Annotation | Exact evidence | What it does not establish |
|---|---|---|
| Protocol/inference problem | Recorded schema error, truncation, invalid reference, overflow, timeout, or infrastructure status, preserving the exact subtype. | That the mathematical problem was intrinsically too hard. |
| Authoritative update not yet available | v2 is absent from the peer's rendered source view at a scheduled call in L. | That the peer lacks all updated information; prose or deduction might suffice. |
| Incorrect after authoritative receipt | Candidate remains wrong on at least one required changed coordinate in a call whose view includes v2. | A hidden reasoning cause; it may reflect arithmetic, missing other evidence, or formatting. |
| Old-value persistence | On a changed coordinate, a valid candidate equals the old gold and differs from the new gold. | That the old value was copied or causally influenced this answer. It could be recomputed or guessed. |
| Collateral error | An unchanged coordinate correct at the prefix boundary becomes incorrect in recovery. | That every changed candidate value is harmful; an old mistake can also be repaired. |
| Recovery regression | A previously correct post-event peer answer or team answer becomes wrong later in the observed window. | That a newly received message caused it. |

Record pre-event correctness as a **context field**, not a reason to exclude the branch. A wrong answer that predates correction must not automatically become a recovery-induced failure. Compare central full-information and distributed outcomes descriptively, while remembering they are different interfaces and the controls do not diagnose a unique cause.

## Data and formulas

Use the PS's exact coordinate maps. Let `g0[j]` and `g1[j]` be old/new gold values, `D={j:g0[j] != g1[j]}`, and `U` its complement. These are evaluator-only labels.

For peer i with assigned coordinates `J_i`:

- `old_value[i,j,r] = 1` iff the candidate is valid, `j` is in `D ∩ J_i`, and its value equals `g0[j]`.
- `incorrect_after_receipt[i,j,r] = 1` iff v2 is in that call's source view and its required value is not correct under the normal evaluator convention.
- `eligible_U[i] = {j in U ∩ J_i : prefix candidate was valid and correct at j}`.
- `collateral_rate[i,r] = number of incorrect coordinates in eligible_U[i] / |eligible_U[i]|`, when that denominator is nonempty.

Keep malformed/missing values separate from explicit old-value persistence. Their required coordinates remain incorrect for ordinary accuracy and preservation scoring, but absence of a parseable old value is not successful revision. If `eligible_U` is empty, return not applicable and report the count.

Required records: world/task/prefix/event/policy IDs; peer/round; raw reply and parse status; candidate; old/new gold and coordinate assignment; the actually rendered source table or an equivalent auditable snapshot; first authoritative-receipt boundary; and immutable message IDs/content.

Aggregate coordinate rates within peers, then worlds, then equally over eligible task families, as in the PS. Also show counts of worlds with each label. Replicated copies are not independent task instances. A scalar maximum has no unchanged coordinate after an answer-changing edit; it is absent only from that diagnostic's denominator.

## A reproducible casebook instead of hand-picked anecdotes

Publish the full branch annotation table. Case cards may use completed pairs with available transcripts; this illustration filter never changes the main analysis or its missing-run sensitivity. Select at most four main-text case cards using a frozen rule:

1. For each of the three core contrasts—C versus B, B versus L, C versus F—find the median strictly positive and median strictly negative world-level AUC difference, if each sign exists. Sort by effect value with immutable world ID as the tie-breaker; take the lower of the two middle observations for an even-sized group, so selection always returns an actual world. This produces at most six candidate examples and avoids selecting only spectacular extremes.
2. Use the fixed order C–B positive, C–B negative, B–L positive, B–L negative, C–F positive, C–F negative, omitting empty groups. Show the first four available cards in the main text and remaining cards in an appendix rather than replacing them after reading their narrative.
3. If all contrasts are zero, select the smallest world ID with a recovery regression; if none exists, select the smallest complete world ID. Describe the null rather than manufacturing a failure story.

An even simpler acceptable implementation is all six cards in an appendix. Do not spend time perfecting an elaborate sampling system. The essential requirement is that the selection can be reproduced from the outcome table without reading persuasive messages first. Selected cards illustrate behavior; their selection does not estimate population prevalence.

Each card should contain the source edit, the paired policy trajectories, affected/unchanged-coordinate outcomes, update availability by call, and only the necessary excerpts linked to raw call/message IDs. Clearly separate observed facts from interpretations. Include counterexamples where the allegedly better policy loses. Do not rewrite model text into a cleaner reasoning story.

## Handling implementation defects

A verified evaluator, generator, source-leakage, or branch-isolation defect is not another ordinary model-failure category. It threatens the experiment's validity and requires the PS's defect correction, matched rerun, cost accounting, and disclosure procedure. Distinguish that from a valid model reply containing a wrong answer or an invalid model-produced source reference, both of which are outcomes.

Unexecuted infrastructure slots need explicit coverage and sensitivity reporting; do not classify unknown answers as demonstrated old-value persistence or silently omit them. No taxonomy label authorizes a hidden retry.

## Extra cost and effort

**Extra inference: 0.** Approximately 2–3 focused analysis days after structured logs exist, including checking a few selected excerpts. Most fields already exist in the PS. A modest manual reading of selected traces is enough; no human-labeling campaign or semantic-cause coding is proposed.

## Interesting outcomes, including negatives

- B and C have similar final accuracy but fail differently: one retains explicit old values, the other introduces collateral errors.
- L's delayed receipt is common, yet peers often answer correctly beforehand: raw authoritative delivery is not a complete description of information use.
- Most wrong answers persist even with v2 available and no formatting defect: the correction broadcast alone is insufficient, without identifying the remaining hidden cause.
- Many apparent recovery failures began with an incorrect prefix: initial competence must remain visible in the thesis story.
- Protocol problems dominate: this is an actionable implementation/capability limitation, not evidence for a sophisticated memory policy.
- Few distinctive failures occur: publish the small rates and uncertainty; the categories still make the null interpretable.

**Minimum recommendation:** use the six labels and three to six matched trace cards. Avoid expanding this into dozens of psychological failure types.

## Sources

Grounded in [PS §§5–6 and 9](../../PROJECT_SPECIFICATION.md), the [protocol audit](../04_design_extensions/evidence/PROTOCOL_AUDIT.md), and [final scientific-design review](../04_design_extensions/reviews/FINAL_DESIGN_REVIEW.md). The additions-pass read ledger is in [Addition 01](01_RECOVERY_TRAJECTORIES.md#sources-and-read-scope). The previous investigation's recommendations are contextual evidence, not a priority rule for this proposal.
