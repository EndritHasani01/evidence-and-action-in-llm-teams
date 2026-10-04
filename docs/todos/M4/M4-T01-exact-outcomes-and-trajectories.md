# M4-T01 — Exact outcomes, preservation and trajectories

**Status:** blocked

**Dependencies:** [M3-T05](../M3/M3-T05-crash-safe-scripted-lifecycle.md). M1–M3 must have passed.

## References

- [Repository contract](../../../AGENTS.md), [plan exact outcomes](../../IMPLEMENTATION_PLAN.md#exact-outcomes-and-contrasts), and [explanatory outcomes](../../IMPLEMENTATION_PLAN.md#explanatory-outcomes-and-costs).
- Specification [§5.1](../../../PROJECT_SPECIFICATION.md#51-exact-outcomes), [§6](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), and [§7.1](../../../PROJECT_SPECIFICATION.md#71-repair-preservation-and-synchronized-completion).

## Intended outcome

Offline scoring turns the complete slot manifest and recorded replies into exact outcomes, coordinate diagnostics, trajectory categories and observable annotations with explicit denominators.

## Scope and boundaries

- Join the full schedule before scoring. Event-specific gold stays evaluator-only. Preserve list order/multiplicity and the full BFS key set; recorded invalid/failed slots score zero while unexecuted slots remain unknown.
- Compute per-round mean peer correctness, normalized recovery AUC over all sixteen opportunities, and final all-four correctness. The reset boundary is not an extra failed round.
- Use unique task coordinates to define D/U. Measure revised correctness and explicit old-gold persistence on D. Preservation/collateral damage on U is eligible only where that same peer's protocol-valid prefix-round-four candidate was correct.
- Separate repair of old U errors from damage to old correct outputs. Invalid answers count incorrect for accuracy/preservation but remain a distinct malformed/missing category for explicit old-value persistence.
- Empty denominators are N/A. Average eligible peers, then worlds, then equal eligible families; publish unique-coordinate and peer-copy counts without removing worlds from main outcomes.
- Derive first joint correctness, first joint correctness maintained through round four, regression, the four specified complete-branch categories and fragmentation. Keep incomplete branches separate. No successful-only time averages, invented fifth round or best-answer splicing.
- Identical-but-wrong agreement applies only to replicated-output tasks. Implement six nonexclusive annotations: protocol/inference failure, v2 unavailable, incorrect after v2, explicit old-value persistence, collateral error and regression, with counts/intersections and archived provenance.

## Completion criteria

- Outcome/diagnostic tables preserve world/event/policy/replicate/peer/round and generation/replay relationships.
- Recorded failure and unknown execution produce distinct scoring and trajectory results.
- Eligibility, empty-denominator reasons and annotation overlaps are auditable from saved records.
- Evaluation can run entirely offline without importing inference or feeding correctness into the runner.

## Validation and evidence

Use hand-checked exact and duplicate-sensitive answers, full BFS dictionaries, malformed/failed/unknown slots, invalid final-prefix candidates, empty D/U eligibility, repaired old errors and collateral damage. Include continuously correct, delayed, regressing, transient, never-joint and fragmented trajectories, plus differently assigned Prefix/Sort outputs. Reproduce expected peer/world/family denominators and failure annotations.

**Evidence:** Not yet recorded. Add fixture expectations, evaluator commands and generated table paths before marking done.

