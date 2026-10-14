# Why the v2 proposal took this shape

**PROPOSED DECISIONS — NOT ACCEPTED ARCHITECTURAL OR SCIENTIFIC DECISIONS**

This record preserves the reasoning behind the [complete proposal](../silo-bench-lean-redesign-v2.md), especially Sections 4, 6–8, and 10–11. It is useful when revisiting a choice; it does not replace the exact design or create new requirements.

## 1. Optimize the question before optimizing inference

The original study combined several questions: retention, source retention, partial-team resets, receipts, correction delivery, message delay, and repeated continuations. A smaller sample of that matrix would preserve the engineering burden while weakening each comparison.

The proposed contribution is narrower: **what happens to correctness and recovery effort when a distributed team retains or clears the explicit work it actually produced, after a local factual revision?** This keeps the strongest idea—old work can save effort or preserve obsolete conclusions—while giving up teammate-interference and delivery-policy claims.

The rejected custom decision task was an effective cost reduction but not an acceptable final direction. The user requires authentic SILO mathematics, and a few additive scores offered little substantive historical computation to preserve.

## 2. Prefer set union for its support structure, not just its scalar answer

I-08 combines a small answer with a nontrivial dependency: removing one occurrence matters only when no other occurrence supports that value. Local distinct sets, overlap accounts, and source-specific membership knowledge can help recovery. An old union cardinality alone cannot generally tell an agent whether a value disappears.

For a replacement of one occurrence of `x` by `y`, with `x != y`, let `U` and `m(x)` be the original global union and multiplicity. Then:

\[
|U'|-|U|=\mathbf{1}[y\notin U]-\mathbf{1}[m(x)=1].
\]

The verifier may use this identity. The host must not provide the missing indicators or an update formula evaluated on hidden sources. The experiment needs actual agent work to determine support.

This is also a weakness: once enough source-specific information is shared, recovery is easy. The proposal therefore measures effort and examines naturally produced summaries. It does not claim that set union is computationally expensive or that history must affect final accuracy.

## 3. Compare credible alternatives on the question they answer

The following is a reasoning summary; exact alternative allocations are in proposal Section 6.

| Alternative | Strongest reason to choose it | Strongest reason against it |
|---|---|---|
| I-01 Global Max | Easier qualification and more independent worlds within a small budget | Thin historical computation; witness correction may be almost immediate |
| I-09 Top-K | Meaningful cached rankings and an exact mathematical endpoint | Longer ordered output, multiplicity mistakes, and harder small-model qualification |
| III-23 Components | Source retraction can invalidate substantial graph reasoning | Graph bookkeeping may dominate the retention effect and require more turns |
| II-16 Trapping Rain | Global boundary summaries can support meaningful reuse | More arithmetic and boundary reasoning; higher floor and horizon risk |
| I-08 with revision only | More worlds for the same budget | Cannot separate ordinary clearing/rebuilding costs from revision-specific behavior as well |
| I-08 with a third memory policy | Could distinguish additional mechanisms | Too few worlds per contrast; more intervention and interpretation complexity |
| Two task families | Better scope than one family | Under 500 attempts, qualification and replication become thin in both |
| Preferred I-08 four-cell design | Useful support-loss problem, short answer, paired control of ordinary reset cost | Twelve worlds and a six-turn horizon remain fragile |

If I-08 qualification fails, I-01 is a defensible separately approved simpler study, not a drop-in substitute that preserves every claim. If I-08 works but precision is poor, more independent I-08 worlds address that problem more directly than an extra memory policy.

## 4. Keep the no-change comparison despite its opportunity cost

Reset may consume more work even when nothing changes. A revision-only contrast can detect a practical policy effect, but cannot show whether the difference is special to correction or ordinary rebuilding.

Let `Delta_V` be revised-world success under reset minus retain, and `Delta_S` the analogous recheck difference. Report both and `theta = Delta_V - Delta_S`. A positive interaction does not imply reset is better on revised worlds. For example, reset could be worse in both settings but less harmful after a revision.

The sham is imperfect: a revision notice and a neutral recheck are different interfaces. The interaction is interpreted under those interfaces, not as a pure numerical-change effect. More elaborate notice controls might sharpen that claim but would consume replication and introduce additional conditions. The narrow interpretation is the deliberate trade-off.

## 5. Preserve current sources while admitting the information asymmetry

Clearing acquired source records would mix loss of evidence with loss of work. The proposal instead retains identical canonical source holdings in matched retain/reset siblings and clears only explicit working history.

That does **not** make the two conditions informationally identical. A historical message may contain a useful set or membership statement absent from canonical attachments. Retention is a policy package: it preserves derived information, previous calculations, old answers, and extra context together. A favorable result would not isolate “reasoning reuse”; an unfavorable result would not isolate “anchoring.”

Separating those mechanisms would require additional interventions such as controlled summaries or matched distractors. Those interventions would change the question and budget. The proposal favors honest identification of a practical package over an underfunded mechanism decomposition.

## 6. Make completion an agent decision, with bounded opportunities

Mandatory answers on every turn confound communication with submission. Permanent submission can strand a collaborator. Correctness-gated stopping leaks evaluator information. Unbounded autonomy makes costs and recovery opportunities difficult to compare.

The compromise is optional submissions, message-triggered reopening, and three turns per agent per phase. Both agents must have active submissions with no pending review for procedural completion. Disagreement and wrong answers can still complete; scoring happens offline.

The horizon is a substantive limitation, not a cosmetic setting. A late message can invalidate a submission when no review turn remains. If the pilot shows that this dominates competent behavior, the costed response is a longer horizon, not covert extra turns or a host decision that a message was irrelevant.

## 7. Spend the small budget on worlds, controls, and qualification

The final allocation is 384 main first attempts, 96 preparation first attempts, and 20 additional infrastructure attempts. The main unit is a world with one realized prefix, not an agent, branch, or call. Four continuations from a shared prefix improve comparability but do not create four independent worlds.

Twelve worlds are deliberately modest. The study can produce informative paired outcomes and traces; it cannot establish equivalence or reliable small effects. Under the same preparation plan, 16 worlds cost 628 attempts and 24 cost 884. These expansions buy replication, not automatic statistical power.

Qualification is not free development overhead. The six-world, two-mode before/after screen consumes 24 calls. The two-world complete pilot consumes up to 64. If those screens are insufficient, increase the stated budget or stop; do not move extra exploratory attempts outside the accounting boundary.

## 8. Treat thinking as a candidate configuration, not a cure

9B has actual short-input loading/generation evidence, but its earlier mathematical and formatting results are poor. Neither success on larger-model benchmarks nor enabling thinking resolves that uncertainty.

The proposal qualifies direct and thinking configurations, then selects the cheaper passing configuration before main outcomes. This selection is practical, not a causal experiment on reasoning mode. A 4,096-token thinking cap can still be much more expensive than a short direct answer; token and latency measurements must determine admission.

The most important reason to reject the preferred design would be failure of its empirical premise: native-size competence, useful history, natural completion, and affordable inference must coexist. Reusing implemented infrastructure and meeting a round number of attempts are insufficient reasons to proceed.
