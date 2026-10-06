# M4-T02 — All prespecified contrasts and repeatability

**Status:** active

**Dependencies:** [M4-T01](../M4/M4-T01-exact-outcomes-and-trajectories.md). M1–M3 must have passed.

## References

- [Repository contract](../../../AGENTS.md) and [plan exact outcomes/contrasts](../../IMPLEMENTATION_PLAN.md#exact-outcomes-and-contrasts).
- Specification [§5.2 θ](../../../PROJECT_SPECIFICATION.md#52-primary-1-correction-specific-reset-value), [§5.3 φ](../../../PROJECT_SPECIFICATION.md#53-primary-2-effects-on-retained-collaborators), [§5.4 secondary estimates](../../../PROJECT_SPECIFICATION.md#54-secondary-estimates), and [§6 repeatability](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness).

## Intended outcome

Every prespecified estimate has an explicit formula, population and endpoint, with world/family contrasts and separately identified conditional repeats.

## Scope and boundaries

- Implement θ and its direct revised/sham C−B components with equal five-family weighting.
- Implement φ as revised E_keep over the same focal peers in rounds 2–4. Include sham E_keep, φ_corr, both E_clear effects, complementary own-group reset contrasts, four-mask trajectories and average mixed-policy performance. Round one remains a construction reference.
- Include revised C−B, K−C, K−B, B−L and C−F AUC/final-joint effects; compact-state sham effects and revision-minus-sham interactions.
- On Prefix/Sort implement round-one receipt η, all six cell means, three direct receipt effects, B-versus-C/B-versus-K under both formats, and AUC/final/preservation companions.
- On Sort/BFS implement Q_B−B and Q_C−C round-two effects separately under revision/sham, with subsequent trajectories/AUC and preservation; retain inactive no-prose cases.
- Include preserving B/C/K AUC, joint completion and preservation on its fixed sixteen-world population.
- Keep replicate zero primary. On ten repeated prefixes show per-world θ/φ/compact-state contrasts, ties versus sign reversals and trajectory-category changes; retain original prefix/partition and new continuation seeds.

## Completion criteria

- All §5.4 comparisons and companions exist on the correct eligible populations, with exact formulas and denominator provenance.
- Family balancing and fixed subsets are explicit, including overlapping world identities.
- Repeats never replace replicate zero, become new independent worlds or imply new-prefix, receipt or Q repeatability.
- Each contrast can retain unknown components for the later missingness calculation; complete-case summaries do not silently redefine the estimand.

## Validation and evidence

Use independently hand-calculated θ equal-effect null/positive/negative cases; φ no-influence null and beneficial/harmful cases; φ positive with φ_corr zero for equal event effects; and round-one exclusion. Verify focal-peer matching, own-group/E_clear signs, every secondary contrast/endpoint, equal-family rather than pooled weighting, subset eligibility, replicate separation and ties/sign reversals.

**Evidence:** Started on 6 October 2026 on `feat/m4-offline-analysis` from clean
commit `9a51df7`. The specification, plan, M4-T01 handoff and M1–M3 gate evidence
have been inspected. Analysis will reuse the full scheduled outcome/diagnostic
tables and their original generation/replay/prefix joins. The full M4 gate remains
open; uncertainty and missingness bounds remain M4-T05 work.

The first checkpoint implements [analysis.py](../../../recovery/analysis.py)'s
explicit world components, equal-family summaries and separate conditional
repeats. `python -S -m unittest tests.test_analysis -q` passes 21 formula checks;
`python -S -m unittest tests.test_analysis tests.test_evaluate -q` passes 47 checks
in 7.593 seconds. Exact rational means preserve mathematical ties; each component
retains logical/physical call IDs, rounds, peers, prefix eligibility, coefficients
and unknowns. Saved-run/CLI integration and retained reconstruction remain open
at this checkpoint. The initial fixture read incorrectly assumed a separate
fallback schedule file; tests now derive it from the existing saved fallback
population, without generating worlds or changing any retained fixture.

Saved-worker integration now provides `analyze_run` and `recovery analyze
--estimands`, preserving M4-T01's ordinary outcome export. The new
[retained contrast tables](../../../tests/fixtures/estimand_tables.json.gz)
reconstruct four cases from original accepted M3 workers, including all missing
worlds in both full main manifests. `python -S -m unittest tests.test_analysis
tests.test_analysis_run tests.test_estimand_archive tests.test_evaluate
tests.test_outcome_archive -q` passes 53 checks in 74.566 seconds. Broader CPU,
installed-library and documentation/protected-artifact checks remain open at
this second checkpoint.

