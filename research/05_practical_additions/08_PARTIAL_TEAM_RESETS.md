# 08 — Reset two peers and let two keep their history

**Recommendation: interesting alternative if the thesis should emphasize team coordination; lower priority than compact state for the smallest extension.** This proposal asks about a simple mixed team, without trying to learn the best peers to reset. No model evidence has been collected.

## Simple question and thesis value

Must all four peers forget together, or can two freshly reset peers collaborate effectively with two peers that retain the previous work?

B and C reset zero or four peers. A two-peer reset tests a realistic middle policy: retain some useful work while giving part of the team a clean context. It also makes the distributed setting matter visibly. Cleared peers may help revise retained peers; retained peers may supply useful computation or encourage obsolete answers.

## Exact policy P2

Broadcast the same revision and retain the same current source tables as B/C. Apply C's derived-state clearing to a predetermined set of exactly two peer IDs. Apply B's retention to the other two. Every peer continues for all four recovery rounds and communicates normally.

Select masks before inference using only a fixed random seed, peer IDs and the already chosen edit owner. Across the selected worlds, balance each peer's reset frequency and include the edited owner in approximately half the masks. Never select peers using prefix correctness, gold footprint, hidden dependency labels or anticipated outcomes. Store the schedule for review.

For a sham sibling use the same mask as its changed sibling. The sham does not contain a source revision. Do not tell peers which experimental condition they are in or supply extra advice to cleared peers.

## Minimum useful comparison

Use **12 predetermined main worlds, two per family**. Add one P2 branch after change and one P2 branch under sham. Compare P2 with the already scheduled B and C from each same prefix.

This estimates the performance of a particular balanced two-peer-reset policy. It does not establish the optimal mask, a smooth relationship between number of reset peers and accuracy, or general synergy. A mask chosen on one world and its complement on a different world are not matched counterfactuals for the same history.

Report AUC, exact team completion, collateral damage and trajectories. Also display outcomes for peers whose own state was reset and peers whose own state was retained, while clustering inference at the world level. For retained peers, P2 versus B changes other peers' state while preserving their own initial state; a later difference can reveal an effect of the changed team context. It still does not identify whether a specific message carried a stale premise. Inspect logs rather than naming every regression recontamination.

If the scientific goal becomes a two-group interaction, run both complementary masks on the **same prefix**, together with B and C. With sham, that costs 64 calls/world rather than 32. It supports a specified two-group factorial; it still does not explore all six possible two-peer masks or all sixteen reset subsets. Do not promise this larger design inside the smaller budget.

## Relevance across the six tasks

| Task | Interesting team-level question |
|---|---|
| Maximum | Can cleared peers replace a previously agreed winning value while retained peers contribute runner-up evidence? |
| Top-K | Can mixed peers preserve valid list entries without recirculating the removed entry? |
| Prefix sums | Resetting an upstream peer may affect downstream calculations differently from resetting a downstream peer. Fixed peer positions therefore need balancing. |
| Difference array | Replicated complete outputs allow direct observation of whether retained and reset peers converge or diverge after a local correction. |
| Distributed sort | Retained rank segments may help reset peers recover boundary values; incompatible segments may also disrupt redistribution. |
| BFS | Mixed histories may support alternative-path discovery or keep obsolete distances circulating. |

The six families are useful precisely because masks have different operational meanings. Do not interpret their differences as a controlled effect of task difficulty.

## Incremental cost and effort

| Option | Extra main calls | Interpretation |
|---|---:|---|
| One P2 mask, change+sham, 12 worlds | **384** | Recommended minimum policy comparison |
| Both complementary masks, change only, 12 worlds | 384 | Better coverage of which peers reset, but no matched P2 sham; cannot claim correction-specific mask effects |
| Both complementary masks, change+sham, 12 worlds | 768 | Clearer group-factor comparison; exceeds the preferred addition envelope |
| Both masks, change+sham, six worlds | 384 | Only six independent world clusters; best treated as a qualitative pilot |

For the recommended minimum, add P2 change+sham on two existing sham-assigned development worlds: **64 additional pilot calls**. Main totals become **6,240 / 4,872** for the 48/36-world core; development becomes 652 before smoke/failed attempts. These counts do not establish a fit within 30 GPU-hours. Reuse the original forecast and charge all model and infrastructure work.

Estimated effort: **3–6 working days** for a per-peer retention switch, a balanced mask schedule, branch isolation checks and group-aware plots. Studying all interactions would require considerably more design and inference.

## Useful outcomes and decision

- P2 offers a favorable quality/token tradeoff: partial reset is a useful operational option.
- P2 matches C with shorter retained-history loss: some preserved peer work can remain useful.
- P2 is worse than both B and C: mixed recovery states disrupt coordination in these tasks.
- Cleared peers improve while retained peers worsen, or the reverse: the policy has important within-team tradeoffs hidden by average accuracy.
- P2 behaves similarly under sham: much of the effect is ordinary team-state management rather than correction itself.

Use this as **an alternative to K**, not an automatic additional factorial. It is especially attractive if the completed thesis should foreground how reset decisions affect collaborating peers. A simple policy result remains useful even without proving a new coordination mechanism.
