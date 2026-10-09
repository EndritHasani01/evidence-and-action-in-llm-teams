# Course M4-T03 — Course paired uncertainty and shared-response missingness

**Status:** blocked

**Dependencies:** [M4-T01](M4-T01-course-outcomes-and-estimands.md), [M4-T02](M4-T02-course-diagnostics-and-policy-costs.md).

## References

- [Specification statistical/missingness rules](../../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), [paired quality/cost](../../../../PROJECT_SPECIFICATION.md#73-quality-retained-work-and-cost), accepted course clause and [plan uncertainty](../../../IMPLEMENTATION_PLAN.md#6-milestone-m4--offline-analysis-and-report-reproduction).
- Existing [uncertainty/shared-response evidence](../../M4/M4-T05-uncertainty-and-missingness.md) and [course precision limits](../../../planning/abs-iis-course-study-proposal.md#strength-and-limits-of-the-resulting-evidence).

## Intended outcome

Course estimates, cost comparisons and incomplete-run summaries use correct paired world units, small-sample caveats and shared physical-response constraints.

## Scope and boundaries

- Reuse 10,000 saved-seed paired world bootstrap draws within each eligible family at its actual course population size. Keep events/policies/peers/rounds/groups/controls/repeats together and preserve common world identities for overlapping subsets. Retain equal-family weighting, quantile convention, 97.5% primary and descriptive 95% secondary intervals, raw world contrasts and family means.
- On constant within-family contrasts, include the weighted Hoeffding companion with weights 1/(F*n_f) and correct ranges: theta [-2,2], phi/direct differences [-1,1], other interactions as defined. Include appropriate eligible-family binomial bounds for all-success/all-failure completion. Four worlds per family and five repeated continuations do not justify precise population claims, equivalence or thousands of independent samples.
- Publish scheduled/executed and paired coverage against the complete declared course population. Bound unexecuted correctness in [0,1] through each estimand; combine coefficients for shared physical-response identities before choosing bounds. Keep known parent constraints without inventing executed logical rows. Nonlinear completion/trajectory bounds retain shared variables with conservative labels and tiny enumeration references; no generic optimizer.
- Keep incomplete trajectories, unknown future costs and absent diagnostic denominators explicit. Complete-case summaries supplement rather than replace intended populations. Use the same eligible cohorts/draws for paired preservation/quality/cost; 0.10 and power sensitivities are reporting references, not achieved power or equivalence margins.

## Completion criteria

- Course primary/focal/repeat/cost resampling has correct cluster and cohort identities; uncertainty output remains labeled exploratory with small-sample limits.
- Independent quantile/binomial/bounded-mean, degeneracy, empty-denominator and shared-replay missingness/cost-cancellation cases pass, including safely stopped course scopes.

## Validation and evidence

Compare hand-derived and tiny enumerated cases with existing uncertainty functions on course-shaped records. Verify paired bootstrap reproducibility, raw contrast/family counts and unchanged thesis results. Record exact settings, commands, expected bounds and artifacts; no inference or worker-data writes.

**Evidence:** Not yet recorded. Existing statistical implementation is verified; new course populations are not.
