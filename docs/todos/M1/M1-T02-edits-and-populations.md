# M1-T02 — Eligible edits and reproducible populations

**Status:** active

**Dependencies:** [M1-T01](../M1/M1-T01-task-worlds-and-truth.md).

## References

- [Repository contract](../../../AGENTS.md) and [plan M1](../../IMPLEMENTATION_PLAN.md#3-milestone-m1--reproducible-worlds-truth-and-schedules).
- Specification [§2.2–2.3](../../../PROJECT_SPECIFICATION.md#22-sampling-and-reproducibility), [§4.2](../../../PROJECT_SPECIFICATION.md#42-complementary-groups-recovery-is-a-team-intervention), [§6](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), [§8.2](../../../PROJECT_SPECIFICATION.md#82-cpu-checks-and-bounded-development-pilot), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [generation risks](../../implementation-research/repository-and-validation.md#task-generation-contains-the-meaningful-hidden-risks).

## Intended outcome

Serializable populations contain actual worlds, edits, partitions, eligibility/rejection records and all preassigned random streams, independently of model outcomes.

## Scope and boundaries

- Randomize owner order in blocks of four before conditioning generation. Preserve three main edits per owner in 12 worlds/family and two in the nested first eight.
- Prefix/Difference/Sort select an owner-held position uniformly, then a different in-range replacement uniformly. Main Top-K selects an eligible record uniformly, then a legal lower value; preserving Top-K samples uniformly over legal record/replacement pairs. BFS samples eligible owner-held changing edges; preserving deletions have no owner-matching constraint.
- Require both changing and preserving eligibility in every Top-K/BFS world. Limit generation to 1,000 attempts/world, record rejections, and fail explicitly on exhaustion. Never regenerate based on a prefix or other model result.
- Prepare 60 worlds and the nested 40, five disjoint development worlds, receipt and Q subsets, first-eight Top-K/BFS preserving subsets, and first-two-per-family repeat subsets. Draw a uniform unordered two-pair partition per world; G contains peer 0. Retain it across events/repeats.
- Save separate generation/edit/partition/prefix/continuation streams and actual inputs/edits. Continuation seeds match across policies/events for a given world/replicate/round/peer. Extra repeats have new continuation seeds, while retaining the prefix. Scheduling and process hashing must not determine seeds.
- Main, sham and preserving events refer to the original world; there is only one live edit per episode. These are prepared manifests, not the accepted M5 freeze.

## Completion criteria

- Mathematical eligibility, edit distributions, owner balance and all fixed subsets are explicit and testable for both sizes.
- Persisted manifests can be reloaded without resampling or changing worlds, IDs, ownership, partitions or streams.
- Changed serialized inputs are detected through comparison with the saved authoritative manifest using existing IDs/configuration; no separate identity registry or custom checksum system is introduced.
- Evaluator gold/footprints stay separate from public manifests and future peer views.

## Validation and evidence

Test exact legal sets and deterministic selection boundaries rather than a flaky frequency threshold. Force exhausted rejection. Check development/main disjointness, target/fallback nesting, fixed subset sizes/overlap, all three partition possibilities, owner balance, distinct repeat seeds and sibling seed matching. Reordering preparation or consuming an unrelated stream must not shift other identities. Verify byte-stable regeneration from saved inputs and detection of a modified manifest.

**Evidence (start, 4 October 2026):** M1-T01 is done and its implementation,
23-check CPU evidence, specification sections and generation-risk investigation
have been inspected. Implement legal edit sets first, then immutable population
records and isolated saved streams, then reload/mutation and population checks.
No inference, accepted M5 freeze or scientific-design change is part of this task.

**Edit checkpoint:** `python -S -m unittest tests.test_edits -v` passed five
focused checks on CPython 3.11.9. [edits.py](../../../recovery/edits.py) implements
immutable single-source revisions/shams, exact legal sets and the two sampling
rules; [test_edits.py](../../../tests/test_edits.py) enumerates selection boundaries,
numeric endpoints, unique/duplicate Top-K values, zero cutoffs, and every BFS
deletion against independent relaxation at both sizes. Preserving Top-K requires
the original value strictly below the cutoff; a replacement equal to the cutoff
is legal because it leaves the complete ten-value answer unchanged, including
multiplicity. No record-identity tie-break is part of the answer contract.

**Population checkpoint:** `python -S -m unittest tests.test_populations -v`
passed ten checks on CPython 3.11.9. [populations.py](../../../recovery/populations.py)
prepares 60 main/five development worlds for either mathematical size, nested
40-world views, all fixed subsets, G/H partitions and disjoint integer seed slots.
[manifests.py](../../../recovery/manifests.py) saves actual host inputs and loads
them without resampling; equality with a saved authoritative population detects
even mathematically valid changed inputs. [test_populations.py](../../../tests/test_populations.py)
checks three seed roots/both sizes, all subset counts/owner blocks, reordering,
two process hash seeds, optional-import isolation, exact 1,000-attempt exhaustion
and acceptance on attempt 1,000, rejection reasons, byte-stable regeneration,
and malformed/modified manifests. CLI, retained fixture and final evidence remain.

