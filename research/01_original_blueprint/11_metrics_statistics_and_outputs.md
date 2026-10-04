# Metrics, statistical analysis, and expected outputs

The analysis is registered before confirmatory results. All output templates contain missing values until measured. Confidence intervals describe sampling/model variation in this generator population, not arbitrary real organizations.

## Endpoints

For branch i, define

\[
Y_i=\mathbf1[\text{protocol valid}\land\text{target correct}\land\text{control correct}
\land\neg\text{invalid attempt}\land\neg\text{invalid applied effect}].
\]

This **safe correct completion** is primary. A blocked bad attempt does not count as successful reasoning. A correct wait counts only when no eligible choice exists; refusing when Y is available is failure. Missing output or parse failure is not a successful wait.

Report target and control correctness separately, invalid-attempt rate, invalid-applied-effect rate, protocol failure, and incomplete-infrastructure status. Infrastructure-terminal failures count as Y=0 in the primary operational analysis; provide a sensitivity analysis excluding only externally documented infrastructure failures, with counts and reasons. Never exclude ordinary model truncation as infrastructure.

## Scope and support metrics

Let L be active typed records at the cut, U0 unsupported before correction, U1 unsupported after, D=U1\U0 newly unsupported, and I the policy's withdrawal/suspension set. Use I'=I\U0 for correction-specific scope metrics.

\[
P_{scope}=\frac{| I'\cap D|}{| I'|},\quad
R_{scope}=\frac{| I'\cap D|}{| D|},\quad
F1=\frac{2PR}{P+R}.
\]

Empty denominators are NA; report their counts, never substitute 1. Aggregate raw counts and also show world-macro means so large ledgers cannot dominate unnoticed. Record pre-existing unsupported removals separately.

| Metric | Definition and mechanism |
|---|---|
| Unnecessary withdrawal | `|I \ U1| / |L \ U1|`, valid records lost by the policy. |
| Unsupported retained state | Unsupported active typed records after repair divided by all active typed records; report raw counts if ledger empty. |
| Valid identity preservation | Fraction of pre-correction records still semantically supported after correction whose original IDs remain active at branch close. Re-created identical content is regeneration, not preservation. |
| Obsolete reference rate | References to superseded evidence or withdrawn/superseded claims divided by all emitted references. It is a citation property, not proof of causal reliance. |
| Action-binding omission | Fraction of bound actions whose estimated surviving proof justifies global feasibility but does not entail the actual action. Calculate with the exact evaluator offline. |
| Predicted-set sufficiency | Fraction of nonempty extracted proof sets that entail the typed assertion in its pre-correction evidence view. |
| Exact-proof recall | `|J_hat ∩ J_star| / |J_star|` after canonicalization; macro by claim/action, with NA for unsupported assertions. |
| Missing-alternative rate | Among nodes with≥ 2 exact proofs, fraction where estimated support misses every proof independent of the corrected root. |
| Regeneration count | Number of new successor claim/action records after correction, separated into necessary and unnecessary by evaluator labels. This is not equivalent to saved model calls. |
| Revision compliance | Fraction of notified unsupported owned records explicitly replaced/cancelled/withdrawn by the owner; distinguish runtime withdrawal from agent acknowledgment. |
| Incorrect fresh action | Invalid action created after the correction, separated from reuse/revalidation of an old invalid action. |

Exact proof metrics are operational sufficiency labels under the task model. Do not call them faithfulness scores for hidden reasoning.

## Recovery and cost

- `slot_to_correct_state`: first recovery slot after which all *currently existing* typed state is supported and both job decisions are correct. If never achieved, right-censored at>3; empty state alone does not count. For a more honest final endpoint, also report whether correctness persists to branch close.
- `recovery_latency`: elapsed time from correction commit to branch close, excluding shared prefix generation; also report allocated GPU time and generated/input tokens.
- `end_to_end_cost`: fresh-prefix cost plus the policy-specific extraction/review stage and recovery. Do not multiply physical cached prefix compute in the actual budget ledger.
- `repair_efficiency`: show completion versus tokens and valid state preserved versus tokens as separate plots. Do not collapse safety and utility into an arbitrary weighted scalar score.

There is no LLM-measured long-horizon recurrence endpoint in this budget. The deterministic final audit is only a necessary-state-consistency diagnostic.

## Primary analysis

For every base world w, compute

\[
d_w=(Y_{E, 1,1}-Y_{R, 1,1})-(Y_{E, 1,0}-Y_{R, 1,0});\quad
\widehat\theta=\frac1{64}\sum_w d_w.
\]

Use 10,000 bootstrap resamples of base worlds, stratified by family (resample 32 MATCH and 32 THRESHOLD world clusters). Carry all variants and policies together. Use the 2.5th/97.5th percentiles for the primary 95% CI. Set bootstrap seed from the registered namespace. Show family-specific contrasts with wider CIs as secondary analyses.

Boundary rule: if every observed d_w is zero, do not report a degenerate bootstrap[0,0] as certainty. Compute a Clopper–Pearson upper bound u on the probability of a nonzero world-level contrast; since | d_w|≤ 2, also report the conservative effect interval[-2u, 2u]. Give exact binomial bounds for zero observed invalid-attempt rates in a single structural cell (one outcome per base world). For nondegenerate primary data, keep the registered cluster bootstrap and disclose any sparse-cell limitations.

Fit a linear probability model on primary E/R outcomes:

```text
Y ~ policy * alternative * bound + C(family)
```

Use base-world clustered covariance with the small-sample correction and t reference df 63. Test the registered linear contrast corresponding to `policy:bound + policy:alternative:bound`. The bootstrap interval is the principal uncertainty summary; the clustered Wald p-value is supplementary. This is a marginal risk-difference analysis; the binary dependent variable does not require an unreported logistic transformation. Retain predictions only for estimating the registered cell contrasts, not as individual probabilities.

The three-way interaction comparing that contrast with unique-support worlds is secondary. N comparisons, family differences, and support-quality associations are secondary. Do not make their smallest p-value the thesis headline.

## Diagnostic tests and multiplicity

On the predeclared diagnostic 16, analyze **alternative + bound**, one binary outcome per base world and policy. Report paired differences and bootstrap CIs for O−E, O−OC, O−ON, and OR−O. For these four comparisons use exact McNemar tests on discordant pairs and Holm-adjust their p-values as one family. With 16 pairs, these tests are sensitive only to large effects; report discordant counts prominently. Do not count all four variants as independent observations in an exact McNemar test.

For state/support rates with several nodes per prefix, cluster bootstrap by base world. A regression of Y on observed extraction quality is descriptive because graph quality was not randomized. The OC intervention and O/ON/OR comparisons provide stronger causal evidence about representation or state operations; they do not establish that every naturally occurring error has that cause.

## Prefix quality and stochasticity

Primary analysis includes all prefixes. Secondary correct-prefix analysis requires initial target/control actions and B/C feasibility assertions correct, including the public X-before-Y priority, measured before policy branching. Report its denominator and initial witness choice by family/factors/policy-independent checkpoint. A feasible initial Y action is not a focal-X correction case and fails this subgroup's priority requirement. Conditioning defines a different population and does not replace the primary result.

Second-seed data are analyzed as paired within-base-world robustness, not pooled as 64 extra independent worlds. Report sign agreement and seed-specific effect estimates. The 7B and transfer checks get their own small-sample tables and intervals. Failure to reproduce on them limits the scope of the conclusion; success does not establish model-family universality.

## Precision and minimum convincing evidence

For D's empirical standard deviation s, the rough 80%-power minimum detectable interaction is `(1.96+0.84)*s/sqrt(64) = 0.35*s`. If s≈0.6, that is 21 percentage points; if s≈1,35 points. This design cannot credibly target a 5-point interaction. The theoretical maximum variance is worse still because d ranges−2…2.

Pilot simulations must use plausible paired outcome correlations, not independent Bernoulli cells alone. Simulate at least 5,000 datasets for effect sizes 0,0.1,0.2,0.3 and three within-world correlation settings. These effect values are planning alternatives, not expected results. Inspect interval coverage and expected width. If the anticipated primary 95% half-width exceeds 0.20, the design is a weak test for a moderate effect; revise the question/design before confirmation or accept an explicitly limited descriptive thesis with supervisor agreement. Do not claim an informative null with an interval spanning both substantial harm and substantial benefit.

## Final tables

1. **Dataset and capability:** family, base worlds, source/support counts, initial success, single-agent success, parse failures, mean/p95 context and generation length.
2. **Main outcomes:** N/R/E × four structural cells; safe completion, target/control correctness, invalid attempt/effect, cost, cluster CIs.
3. **Primary and secondary contrasts:** theta, three-way interaction, family contrasts, CI, supplementary p-value; explicit independent cluster count.
4. **Mechanism decomposition:** O/E/OC/ON/OR outcomes on paired diagnostic worlds; mask precision/recall, binding omissions, new versus retained bad actions.
5. **Controls:** restart, extra reviewer, full-information single, no-event; realized costs and information privileges.
6. **Robustness:** second seed, second model if admitted, and transfer, with limited denominators and no pooled headline.
7. **Operational accounting:** model/config, prefix/extraction/recovery physical calls, tokens, allocated hours, infrastructure failures, cache hits and missing blocks.

## Final figures

1. Four-cell schematic showing a surviving conclusion versus a changed action; use the worked world, not a decorative architecture diagram.
2. Main interaction plot: E−R completion difference on y-axis, unbound/bound on x-axis; separate unique/alternative lines, base-world CIs.
3. Paired diagnostic plot connecting each base world's E, O, OC, ON and OR outcomes or rates, with aggregate differences beside it.
4. Support-quality plot: claim versus action proof sufficiency and missing alternatives; overlay outcome rates only as descriptive associations.
5. Preservation/cost/invalid-attempt trade-off scatter with uncertainty and clearly marked oracle arms.
6. Failure decomposition by mechanism and task family, counting records and episodes separately.

Every figure must include model, number of independent base worlds, and whether a condition is privileged. Export PDF/SVG plus PNG and the data used to draw it. No figure is prefilled with an assumed positive outcome.
