# M4-T05 — Paired uncertainty and shared-response missingness

**Status:** done

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

The preparation checkpoint planned uncertainty and missingness from the existing
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
trajectory integration and the complete CPU gate were still pending at that checkpoint.

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
hash-seed reproduction and final documentation/protected-artifact checks were
pending at that checkpoint; the task was active.

Final identity review adds the actual scheduled Q replay fixture: four absent
logical uses remain unknown while their recorded B parents make the round-one
contrast exactly zero and constrain the full cost to 67 fixture seconds.
Fixed coverage still reports four unexecuted uses and no unresolved physical
response. Full-main archive assertions additionally require every shared Q/
retained-group/cleared-group first-round sensitivity to cancel to zero.
The offline join also rejects a changed selected policy outside C/K, even if its
branch ID is otherwise valid. All 33 final focused checks pass in 17.357 seconds;
these are review additions to unchanged statistical arithmetic and retained
tables. Complete regression and final installed/archive checks were then in progress.

The complete CPU regression passes 396 checks in 1,870.135 seconds, including
all nine real-controller lifecycle checks. Subsequent metadata review makes
repeat trajectory displays explicitly target the conditional `repeat` population
and names replicate zero as the population-estimate source. An independent
comparison of all sixteen regenerated cases confirms every estimate, bound,
component, cost and coverage value is unchanged; only scope/population labels
change. Nonnegative resampling seeds are now required: the verified Python
integer-seed absolute-value convention otherwise aliases family streams when
`seed + family_index` straddles zero. All 33 updated focused checks pass in
18.676 seconds. Final package/core/archive and documentation checks were then open.

### Implementation and scientific semantics

[uncertainty.py](../../../recovery/uncertainty.py) and the
[offline CLI/API](../../../README.md#offline-uncertainty-and-missingness) derive
uncertainty from the existing original worker snapshots. `--uncertainty` includes
estimands and costs; diagnostics are optional. Exports are exclusive. Source
outcomes, attempts, inputs/checkpoints and frozen populations remain authoritative;
there is no new persistence, dependency, optimizer or identity system.

- Each generated world and its one realized prefix is the cluster. Exactly
  10,000 draws resample sorted world IDs within eligible families at their observed
  sample sizes. Same family/world cohorts share draws across siblings/endpoints
  and overlapping displays. All family weights, world IDs, denominators, seeds
  and quantile settings are exported. Replicate zero supplies population estimates;
  conditional repeat trajectories explicitly target the fixed `repeat` population.
- Primary pooled θ and φ use 1.25/98.75 percentiles; family descriptions and
  secondaries use 2.5/97.5. Type-7 linear interpolation is explicit. Constant
  within-family contrasts receive the weighted Hoeffding companion with α=0.025
  for primaries and the formula's range: θ/interactions [-2,2], direct differences/
  φ [-1,1], and cell rates [0,1]. Bounds are clipped. Approximate coverage and
  independent-world assumptions are stated; systematic errors are not covered.
- Recorded invalid/failed slots stay zero. Missing logical uses stay unexecuted
  even when an original shared response constrains sensitivity. Linear coefficients
  combine before extrema. Shared conjunctions are enumerated up to twelve unknowns;
  larger expressions retain shared terms with conservative labels. Trajectories
  enumerate up to eight unknown replies, then use conservative shared-variable
  envelopes checked independently. Marginal extrema need not be jointly attainable.
- Original scheduled/executed counts and paired world coverage remain explicit.
  Unknown eligibility can change preservation denominators and leave an endpoint
  undefined; its bounds are conditional and conservative. Empty eligible
  populations are N/A. Complete-case descriptions never replace the frozen
  population. Incomplete trajectories remain a distinct category; no missing
  first/stable completion time or fifth failure round is invented.
- Family final-completion tables retain success/failure/unknown counts. Two-sided
  95% Clopper-Pearson bounds use the whole eligible population only when all final
  observations exist; incomplete complete-case bounds are separately labeled.
  The 0.10 and normal-approximation power/fallback figures remain reporting
  references, with no equivalence, detection guarantee or achieved-power claim.
- Policy quality/preservation and original full-policy durations use paired world
  cohorts and draws. Preservation's `paired_cost` uses its own eligible worlds.
  Whole selected/comparator branch IDs and prefix-plus-continuation identities
  remain checked against the schedule. Shared costs cancel before duration bounds;
  uncertain measured durations have percentile envelopes. Missing future costs
  have explicitly unbounded ends. Allocation overhead and billing remain separate.

### Independent expectations and retained evidence

[Focused fixtures](../../../tests/test_uncertainty.py) and
[worker/CLI checks](../../../tests/test_uncertainty_run.py) cover finite stratified
support, primary/secondary quantiles, equal family weights, overlap identity,
repeats not increasing N, constant-family degeneracy, clipping, exact completion
bounds, shared cancellation, nonlinear feasible completions, fragmentation,
empty populations, unknown selected branches, read-only bytes and exclusive exports.

| Hand expectation | Result |
|---|---|
| Two families: two 0/1 worlds plus a constant 0.5 world | Equal-family bootstrap support 0.25/0.5/0.75 with probabilities 0.25/0.5/0.25; primary endpoints 0.25/0.75 |
| θ at N=60, five families with twelve worlds | Hoeffding half-width `4*sqrt(log(80)/120)`, about 0.7644; φ width is half that |
| Twelve successes / twelve failures | Exact 95% intervals [0.7353515306029488,1] / [0,0.2646484693970512] |
| Shared unknown with coefficients +1 and -1 | Exact [0,0], with no independently varying copies |
| Shared nonlinear `x + y - x*y` | Feasible [0,1]; independent endpoint bounds would be [-1,2] |
| Rotating incorrect peers | All individually ever correct; never jointly correct; fragmentation [1,1] |
| Four absent Q first-round logical uses with recorded B parents | Unknown execution count four, unresolved original responses zero; first-round contrast [0,0], full cost sensitivity [67,67] fixture seconds |
| Preservation eligible only in the ten-second world | Paired preservation cost is ten seconds, excluding the ineligible twenty-second world |

[Reconstruction](../../../tests/uncertainty_archive.py) and its
[archive check](../../../tests/test_uncertainty_archive.py) reproduce every table
in the [sixteen-case export](../../../tests/fixtures/uncertainty_tables.json.gz).
Original worker bytes are checked; the source is the unchanged ordinary M3 bundle.
The repeat-label comparison proves all estimates, bounds, components, costs and
coverage values are unchanged by that final metadata correction.

| Retained population | Scheduled / executed / unknown outcomes | Main family denominators | θ / φ frozen sensitivity |
|---|---|---|---|
| Complete five-family fixture, each size | 2,170 / 2,170 / 0 | One world in each family | [0,0] / [0,0], with Hoeffding companions |
| Full target-60 | 17,656 / 2,170 / 15,486 | Twelve per family | [-1.8333333333333333,1.8333333333333333] / [-0.9166666666666666,0.9166666666666666] |
| Full fallback-40 | 12,560 / 2,170 / 10,390 | Eight per family | [-1.75,1.75] / [-0.875,0.875] |
| Stopped prefix | 16 / 0 / 16 | No complete eligible primary population | N/A |

Full-manifest intended point intervals remain unavailable. Their five-world
complete-case zero intervals have separate denominators and bounded-mean
companions. Repeated worlds remain ten in each full manifest, with conditional
trajectories and all incomplete pairs retained. These are scripted CPU validation
joins, not model recovery estimates or completed main experiments.

### Reproduction and executed checks

```powershell
python -S -m unittest tests.test_uncertainty tests.test_uncertainty_run -q
python -S -m recovery validate --core-only
.venv/Scripts/python.exe -m recovery validate
.venv/Scripts/python.exe -m unittest tests.test_uncertainty_archive -q
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.uncertainty_archive
.venv/Scripts/python.exe -m pip install --no-deps .
.venv/Scripts/python.exe -m pip check
.venv/Scripts/python.exe -m compileall -q recovery tests
```

| Executed check | Result |
|---|---|
| Final focused dependency-free checks, including repeat labels and seed guard | 33 passed in 18.676 seconds |
| Final core with site packages disabled | 225 run: 221 passed, four optional skips; 169.204 seconds |
| Complete CPU source regression | 396 passed in 1,870.135 seconds, including all nine real-controller lifecycle checks; final rule/label/seed review is additionally covered by the final focused/core/installed/archive checks |
| Final installed-library M4 suite outside checkout | 144 passed in 252.673 seconds; nine installed module paths/bytes match final source |
| Final installed CLI outside checkout | Uncertainty plus costs/estimands/diagnostics preserve all 1,178 unknown development slots, saved seed 37 and absent worker files |
| Final hash-seed-37 reconstruction | All sixteen cases and every table match in 66.566 seconds; source worker bytes remain unchanged |
| Independent NumPy 2.4.2 / SciPy 1.17.1 reference environment | 156 exact-binomial intervals, six quantiles and an unequal-family paired bootstrap agree; maximum binomial difference 4.95e-13 |
| Ordinary non-editable wheel build/install, `pip check`, compilation, whitespace | Passed; dependencies unchanged |

Windows build 26200, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5, LangGraph
1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and core 1.6.6 are the tested CPU
environment. This is not the accepted M5 freeze. Concurrent CPU validation times
are not model or GPU timing evidence. Temporary reproducible logs/harnesses use
`$env:TEMP/m4-t05-*`; retained tables and reconstruction are durable evidence.
Final link/status/protected-artifact audits pass: 449 local links/anchors across
fourteen documents, including the task, index, plan, README, fixture notes and
prerequisite documents. All 29 statuses and six
milestone counts agree. Specification, configurations, dependencies, earlier
task evidence and all prerequisite/raw fixtures remain unchanged.

### Completion and handoff

M4-T05 is implemented and verified on CPU on 6 October 2026. Checkpoints
`63610bf`, `8c44275`, `0edb126`, `cb4e495` and `f6a09f6` separately record
prerequisite preparation, statistical arithmetic, saved-run exports/evidence,
actual replay/frozen-rule checks and conditional-repeat/seed review. The final
evidence commit closes this task. Progress is nineteen done, one ready and nine
blocked. [M4-T06](M4-T06-reproducible-report-and-cpu-gate.md) is ready to assemble
the complete report from the existing component, uncertainty, coverage, trajectory
and paired cost tables. Its full M4 report/CPU gate remains required before GPU use.

No GPU allocation, model inference, pilot, main experiment, scientific/frozen
configuration change, important-artifact deletion or publication occurred.

