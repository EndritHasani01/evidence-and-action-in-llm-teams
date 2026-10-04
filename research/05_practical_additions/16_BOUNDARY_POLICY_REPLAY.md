# 16. Evaluate one practical reset rule without new model runs

**Recommendation: useful optional analysis, with a strict half-to-one-day scope. Extra calls: 0.**

## Idea in simple terms

The experiment already runs B and C from the same checkpoint. A rule that chooses between them **at that checkpoint** can be evaluated by selecting the corresponding complete recorded branch. No additional rollout is necessary if the rule is fixed beforehand and uses only information a runtime really has.

Start with one deliberately simple rule: **clear history only when every peer already holds the complete current raw source table; otherwise retain history.** The motivation is that complete source evidence makes fresh computation possible without recollecting records. This does not guarantee reset is better or that the model can recompute successfully.

## Question and why the result would be useful

Can a cheap, understandable state check improve on always retaining or always clearing? Or does it collapse to one fixed policy or choose badly because raw-source completeness is a poor proxy for useful reasoning?

This gives the thesis an operational policy question without training a classifier or adding a recovery arm. Existing literature need not regard the rule as new for its empirical answer to be useful.

## Minimum analysis

Before main inference, freeze the rule using only the common corrected B/C source-table snapshot. Completeness means every required record ID is represented at its current version, including an explicit deletion/tombstone where appropriate. The host uses its normal record manifest and delivery ledger, not gold answers, D/U coordinates or a semantic relevance oracle.

For each world, select the **entire** already-run B or C changed-event branch according to the rule. Calculate its AUC, final joint correctness, collateral damage and policy-specific token/time cost. Compare descriptively with always B and always C, preserving task balance and world pairing.

Two accounting views must remain separate:

- The actual evaluation paid for all B/C branches in the original matrix.
- A hypothetical deployed boundary rule would execute only its selected branch, plus its cheap state check. Its observed branch cost can be reported as an offline policy-cost estimate, not as saved GPU allocation in this study.

The matched experimental design makes this valid for a boundary choice: selected state, prompt and four-round continuation are exactly those of the corresponding existing intervention. It does **not** authorize switching at arbitrary later times by splicing B's round one with C's round two. Those states have different histories and would need a new live branch.

## Prevent an attractive but invalid analysis

- Freeze this single rule before inspecting main outcomes. Do not search thresholds, task-specific rules or old-candidate correctness labels until a policy wins.
- Do not choose using the gold score of the prefix; a normal runtime lacks it. Peer confidence and agreement also do not certify correctness.
- If the rule always chooses B or always C, report this degeneracy and stop. Do not invent an outcome-tuned replacement.
- A per-world best-of-B/C curve may be a separately labeled **hindsight envelope**, but it is not achievable policy performance or a reliable estimate of learnable headroom. One noisy continuation per arm makes apparent switching gains optimistic.
- With only 36–48 worlds, use descriptive paired intervals, all chosen-arm counts and transparent limitations. This is not a large policy-learning study.

## Effort and possible outcomes

About half to one day once current-table coverage and paired branch outcomes are available. CPU selection/bootstrap work only; no new prompts or inference.

- A simple rule captures much of the observed quality/cost tradeoff: a practical lesson without extra infrastructure.
- Complete evidence is common, so the rule is simply C: provenance/coverage-based adaptivity adds little here.
- Complete evidence is rare, so the rule is simply B: raw-source coverage provides little usable selection.
- The rule performs worse than both fixed policies on average: complete raw evidence does not tell us whether dropping computation is wise.

Add one table and a short explanation only if the rule produces a meaningful comparison. If it degenerates, one sentence is enough. Do not let this optional analysis displace the core estimates or become a search for a winning router.
