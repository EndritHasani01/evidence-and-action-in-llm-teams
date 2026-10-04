# Addition 01: show how recovery unfolds

**Recommendation: include. High thesis value; zero additional model calls.**

**Simple idea:** show whether teams recover immediately, need further rounds, temporarily become correct and regress, or never reach a correct team answer within the allowance. This makes the existing recovery comparison understandable even when final accuracy is similar.

**Status:** analysis proposal for the planned PS experiment. No natural LLM recovery trajectories have been collected in this repository. Existing v2 CPU examples establish logical possibilities, not measured recovery patterns.

## Question and value

When two recovery policies finish with the same accuracy, did they get there by equally useful paths? Does one recover earlier but damage still-correct work or become wrong again?

The practical value is a clearer answer to “what should the team retain?” A four-round allowance can hide meaningful temporary failures, and a single successful round can hide unstable recovery. The thesis can explain these differences without adding another experimental arm.

## Already in the PS versus the addition

PS §6 already requires exact-agent AUC, round curves, first all-correct round, first observed stable-correct round, and unchanged-coordinate preservation. This proposal does **not** claim those metrics as a new design. The addition is a small, coordinated analysis and presentation layer: a paired trajectory figure, four interpretable trajectory descriptions, and explicit regression annotations. Preserve the PS's sole primary estimand and existing uncertainty procedure.

## Minimum worthwhile analysis

Produce one main figure and one compact supporting table:

1. **Main figure:** four-round exact-agent accuracy curves for L/B/C/F, with B/C sham curves alongside the B/C changed-event contrast. Include small per-family panels or an appendix to prevent the pooled curve concealing opposite task patterns. Use the PS's world-paired estimates and task balancing.
2. **Supporting table:** the number of complete branches in each observed trajectory description, by policy. Keep a separate count for incomplete infrastructure runs. Add one column identifying whether any previously all-correct team subsequently became incorrect.

The descriptions should be literal, mutually exclusive, and limited to the observed four rounds:

| Description | Rule |
|---|---|
| Immediately correct and remains correct | Team is all-correct in all four rounds. |
| Correct by the end after a delay or regression | Final round is all-correct, but the preceding rule does not hold. |
| Temporarily all-correct, ends incorrect | At least one round is all-correct, but the final round is not. |
| Never all-correct within the allowance | No round is all-correct. |

These descriptions supplement, rather than replace, exact-agent accuracy: a team with three correct peers throughout belongs to the last row but is visibly different from a team with none correct. Do not rank policies solely by these bins.

One optional paired heatmap can show the four round values for each world, keeping sibling policies adjacent. It is useful when averaged curves hide substantial heterogeneity; omit it if the main figure is already clear. Sort worlds by task and immutable world ID, rather than ordering them to emphasize a favorable policy.

## Data and definitions

Required fields already belong in PS records: `world_id`, `task`, `prefix_id`, `event`, `policy`, `round`, `peer_id`, parse/call status, typed candidate, and evaluator-only old/new gold answers.

For a branch and recovery round r:

- `c[i,r] = 1` when peer i's complete candidate is valid and exactly correct; a known failed or malformed slot scores zero.
- `a[r] = sum_i c[i,r] / 4`.
- `q[r] = 1` when all four peers are correct.
- `A = sum_r a[r] / 4`, exactly as in the PS.
- `T_first = min{r : q[r]=1}` when observed.
- `T_stable = min{r : q[s]=1 for every observed s from r through 4}` when the complete branch permits this determination.
- `regressed = 1` if some earlier all-correct round is followed by a later incorrect round.

“Stable” means stable **to the end of the observed window**, not indefinitely. A first correct answer in round four supplies no evidence about round five. If no stable recovery is observed, retain the censoring status at four rounds; never invent a recovery time of five and average it with successful times. Report the fraction reaching each milestone within the allowance instead of averaging successful recovery times only.

For a prefix-quality inset, evaluate prefix answers against the **old** gold. Recovery uses **new** gold. Label that change of target explicitly; do not connect the reset boundary as an extra failed recovery round.

## Scientific safeguards

- Keep all generated valid worlds in the primary analysis, including poor prefixes. A pre-event-correct subgroup is secondary and must show its denominator.
- Resample whole world/prefix clusters within task families. Four peers and four rounds are repeated observations, not 16 independent experiments.
- Distinguish a recorded failed slot from an unexecuted infrastructure slot. Show missing observations explicitly and use the PS's paired-coverage and best/worst sensitivity rules; do not quietly present only complete branches as the intended population.
- Keep no-change and answer-preserving results distinct. Answer-preserving corrections test avoiding damage; they do not have changed coordinates to repair.
- Treat the classifications as descriptive. Do not add significance tests for every bin, round, and task.

Simple analysis checks should cover sequences such as all-correct indicators `[1,0,1,1]` (first=1, observed stable=3, regression present), `[0,1,0,0]` (temporary success, no observed stable recovery), and `[0,0,0,0]` (never all-correct). These are validation examples, not observed results.

## Extra cost and effort

**Extra inference: 0 calls and 0 GPU-hours.** Estimated analysis effort after valid logs/evaluators exist: roughly 1–2 focused days, sharing data preparation with the other analysis additions. This excludes building the PS runner and gathering the original runs. No new models, judges, prompts, or dependencies are needed.

## Interesting outcomes, including negatives

- All policies finish correctly, but one consistently loses fewer intermediate correct answers: recovery speed/preservation matters beyond endpoint accuracy.
- Reset reaches correctness quickly and then regresses: report that limitation instead of calling the first correct round a complete success.
- Retention is initially helpful and later harmful, or the reverse: the full path gives a more useful policy story than a single winner label.
- Curves and trajectories coincide with reasonably bounded uncertainty: the simpler protocol may be adequate in this setting.
- Widespread failure is already present before correction or in capability controls: the thesis identifies a competence boundary instead of mislabeling it as a correction phenomenon.

**Minimum recommendation:** implement the existing trajectory requirements well and add the small descriptive table. This is valuable irrespective of whether any new recovery mechanism is adopted.

## Sources and read scope

Grounded in [PS §§5–6, 8–10](../PROJECT_SPECIFICATION.md), [foundation assessment](../research_innovation_v2/FOUNDATION_ASSESSMENT.md), [untapped structure](../research_innovation_v2/UNTAPPED_STRUCTURE.md), and the v2 evidence/review files. For this additions pass, the author reread the PS in full; `FOUNDATION_ASSESSMENT.md`, `CURRENT_THINKING.md`, `UNTAPPED_STRUCTURE.md`, `reviews/STRUCTURE_CANDIDATES.md`, `reviews/FINAL_DESIGN_REVIEW.md`; and all seven files in `research_innovation_v2/evidence/`. Both JSON files were fully parsed; their finite probes and six budget records were inspected as prior research artifacts, not rerun or treated as LLM results. No new literature search was needed for this analysis proposal.
