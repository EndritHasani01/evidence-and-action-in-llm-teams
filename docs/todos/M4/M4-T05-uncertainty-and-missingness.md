# M4-T05 — Paired uncertainty and shared-response missingness

**Status:** active

**Dependencies:** [M4-T02](../M4/M4-T02-estimands-and-repeatability.md), [M4-T04](../M4/M4-T04-policy-costs-and-boundary-rule.md). M1–M3 must have passed.
M4-T02 is done as of 6 October 2026: its exact world components/weights, endpoint
ranges, fixed populations, original shared-response IDs and separate conditional
repeats are ready for use. M4-T04 is done as of 6 October 2026: its
[cost/rule handoff](M4-T04-policy-costs-and-boundary-rule.md#completion-and-handoff)
supplies complete policy costs, original generation/attempt joins, paired
quality/preservation components, sixteen continuation identities, whole selected
branch provenance, fixed population denominators and unavailable results for
missing selected branches. Both prerequisites and M1–M3's CPU gates pass.

## References

- [Repository contract](../../../AGENTS.md) and [plan uncertainty/incompletion](../../IMPLEMENTATION_PLAN.md#uncertainty-and-incomplete-execution).
- Specification [§5](../../../PROJECT_SPECIFICATION.md#5-outcomes-and-prespecified-estimands), [§6](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), and [§7.3](../../../PROJECT_SPECIFICATION.md#73-quality-retained-work-and-cost).
- Technical evidence: [statistical defaults and identity constraints](../../implementation-research/repository-and-validation.md#analysis-and-allocation-defaults-that-would-change-the-result).

## Intended outcome

Complete and incomplete runs yield the prescribed uncertainty, coverage and bounded sensitivity without treating peers, repeats or shared response copies as independent observations.

## Scope and boundaries

- Use 10,000 paired world-cluster bootstrap draws within each eligible family at its observed sample size. Carry all sibling events/policies/groups/peers/rounds/controls/repeats together.
- Use equal eligible-family weighting, saved resampling seeds and quantile convention; 1.25/98.75 percentiles for both primaries and 2.5/97.5 for descriptive secondaries. Preserve fixed subset populations and shared world IDs in overlapping displays.
- Show world contrasts and family means. When within-family contrasts are constant, add the §6 weighted Hoeffding companion with weights 1/(F*n_f), α=0.025 for primaries and the formula-appropriate range: θ [-2,2], φ/direct differences [-1,1], interactions as derived.
- Report eligible-family completion counts and appropriate exact binomial bounds for all-success/all-failure cases. Keep 0.10 and the specified power/fallback sensitivity calculations as reporting references, never equivalence or achieved-power claims.
- Publish scheduled/executed counts and paired coverage. Bound unknown correctness in [0,1] through each estimand.
- Combine coefficients of a shared unknown response identity before assigning extrema for linear contrasts. Nonlinear joint/trajectory summaries retain shared variables and conservatively labeled bounds; small enumerated fixtures suffice, without a generic optimizer.
- Incomplete trajectories remain separate; complete-case displays cannot replace the frozen population. Include paired uncertainty for policy quality/preservation/cost displays.

## Completion criteria

- Resampling units, family weights, interval settings and seeds are explicit and reproducible.
- Degenerate bootstrap output has its bounded-mean companion, correct contrast range and stated limits.
- Recorded failures remain zero and unexecuted slots remain unknown through all summaries.
- Shared first-round logical uses cannot independently vary in sensitivity bounds; cancellations and feasible joint completions are respected.

## Validation and evidence

Test paired clustering/family stratification, repeats not increasing N, overlap identity, quantile endpoints, constant-within-family degeneracy, clipped Hoeffding ranges and exact completion bounds. Enumerate tiny shared-response linear/nonlinear fixtures independently, including missingness cancellation and fragmented/incomplete trajectories. Check empty eligible populations yield explicit N/A, not false certainty.

**Evidence:** Started 6 October 2026 from clean `ed579e4` on
`feat/m4-offline-analysis`. The repository contract, specification §§5–7,
plan uncertainty/cost requirements, technical synthesis and M1–M3/M4-T02/T04
CPU evidence were inspected. The unchanged prerequisite formula/cost checks
pass: `python -S -m unittest tests.test_analysis tests.test_costs -q`, 45 tests
in 4.231 seconds on Python 3.11.9 with site packages disabled.

Implementation will derive uncertainty and missingness from the existing
outcome/component/cost joins, using standard-library arithmetic, saved seeds,
explicit percentile interpolation and shared world/response identities.
Independent tiny enumerations, original-worker reconstruction, read-only CLI
checks, complete CPU regression and installed-library verification are required
before completion. No new persistence, dependency, scientific configuration,
GPU/model execution or empirical result is part of this task.

The statistical core in [uncertainty.py](../../../recovery/uncertainty.py)
now passes fifteen dependency-free checks in 1.520 seconds. Independent fixtures
verify explicit primary/secondary quantiles, exact binomial tail inversion,
equal-family weights, degenerate/clipped Hoeffding intervals, shared linear
cancellation, feasible nonlinear completions, fixed missingness denominators,
repeat exclusion and common overlapping world IDs. The default saved seed is
20261006; each family uses that seed plus its existing task-order index. Exactly
10,000 draws use sorted world IDs and linear type-7 quantiles. Complete-case
intervals remain separately labeled descriptions. Original-worker/CLI/cost and
trajectory integration and the complete CPU gate are still pending.

The saved-run integration now passes 32 dependency-free focused checks in
16.533 seconds. [CLI/API usage](../../../README.md#offline-uncertainty-and-missingness)
adds uncertainty, original costs and estimands from one read-only worker snapshot.
[Sixteen retained cases](../../../tests/fixtures/uncertainty_tables.json.gz)
reproduce directly from the ordinary M3 workers; the archive check passes in
60.607 seconds and checks worker bytes. Complete and incomplete trajectories,
family completion bounds, unknown selected branches, shared cost cancellation,
paired preservation/cost cohorts and empty diagnostic populations are covered.
Whole-policy IDs are checked against the original schedule. Large nonlinear
bounds are conservative, shared-variable envelopes; missing future cost ends
are explicitly unbounded. No missing reply or completion time is imputed.

Independent reference verification in the existing system Python environment
(NumPy 2.4.2 / SciPy 1.17.1, separate from project dependencies) agrees on 156
two-sided exact-binomial intervals, six quantile endpoints and a complete
unequal-family paired bootstrap. Maximum binomial difference is 4.95e-13.
The [exact-binomial method](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html)
and [type-7 quantile convention](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html)
are documented primary references. Temporary reference/log helpers use
`$env:TEMP/m4-t05-*`. Full source/core regression, installed-library validation,
hash-seed reproduction and final documentation/protected-artifact checks remain
pending; the task is active.

