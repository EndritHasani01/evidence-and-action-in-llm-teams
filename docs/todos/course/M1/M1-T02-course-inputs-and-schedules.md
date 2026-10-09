# Course M1-T02 — Course inputs and schedules

**Status:** done

**Dependencies:** [M1-T01](M1-T01-course-contract-and-reuse-boundary.md).

## References

- [Specification tasks/sampling/events](../../../../PROJECT_SPECIFICATION.md#2-worlds-task-structure-and-events), [controls and pilot](../../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls), [adopted course clause](../../../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime) from M1-T01, and [plan M1](../../../IMPLEMENTATION_PLAN.md#3-milestone-m1--reproducible-worlds-truth-and-schedules).
- [Proposed exact course budget](../../../planning/abs-iis-course-study-proposal.md#exact-call-budget); reusable [task truth](../../M1/M1-T01-task-worlds-and-truth.md), [populations](../../M1/M1-T02-edits-and-populations.md), and [schedules](../../M1/M1-T03-complete-schedules.md).

## Intended outcome

Existing mathematical generation/truth and schedule preparation support one reproducible, complete course population without changing thesis preparation.

## Scope and boundaries

- Reuse the five generators, independent exact references and supported small size. Preserve value ranges, ownership/position/output-coordinate distinctions, Top-K multiplicity, Prefix/Sort full-world control shapes, 23 difference coordinates, canonical eight-node BFS keys and the Pruefer-tree-plus-five-nonedges distribution. Preserve source-ID privacy and supplied attribution.
- Prepare four worlds per family with one balanced edited-owner block, five separate development worlds, uniformly selected unordered two-pair partitions and canonical G containing peer zero. Verify disjoint course-development/main/thesis seed domains and save actual inputs, edits, partitions and rejection counts. Match continuation seeds across events/policies for the same world/replicate/round/peer; extra replicates have new seeds/IDs and retain the original prefix/partition. Derivation must not depend on worker order or process hashing. Retain specified main/preserving sampling, mathematical eligibility and the 1,000-attempt limit; model outcomes never select worlds.
- Schedule revised L/B/C/K/F and masks on every world; sham B/C/K and masks; receipts only on revised Prefix/Sort; Q on Sort/BFS under both events; preserving B/C/K on all four Top-K and four BFS worlds; extra B/C/K/mask replicate under both events on first one per family; two controls per main world. Events fork the original prefix, not each other. Keep original IDs/seeds/replay relationships within a separate course bundle.
- Independently enumerate new-generation components: prefix 320; revised 1,600; sham 960; masks 960; controls 40; preserving 384; receipts 384; Q 384; repeats 720. Total 5,752 plus 528 replay uses gives 6,280 logical slots. Development retains 730+96+96+96+96=1,114 new slots, 1,178 logical slots, beginning with 80 prefix plus ten control opportunities. Smoke is separate.

## Completion criteria

- Course inputs/manifests/schedules round-trip reproducibly, select exactly the declared cohorts, preserve all parents and new-replicate identities, and reject edits/inconsistent configuration.
- Independent component, subset, owner/partition, seed and dependency checks pass. Existing 60/40 thesis counts and both existing size contracts remain correct.
- M1 course gate is passed with input/schedule evidence; no model capability or allocation claim is made.

## Validation and evidence

Run affected mathematical/manifest/schedule checks, including duplicate cutoffs, endpoints/shard boundaries, rank crossings, alternatives/disconnection, D empty/nonempty, legal edit sampling and exhausted rejection. Reuse unchanged solver evidence rather than rebuilding solvers. Record commands/environment, course input/schedule locations and independent count/seed comparisons. No inference.

The authority, course handoff, referenced plan/specification and M1-T01
[adoption/reuse evidence](../../../validation/course-m1-contract-and-reuse.md#completion-and-handoff)
were inspected before implementation. Meaningful checkpoints are `105c327`
(populations; 66 focused regression checks), `5521961` (saved schedule/CPU CLI;
13 course checks) and `913da21` (explicit native-test discovery boundary).

## Completion and handoff

**Passed 9 October 2026 on Windows/CPython 3.11.9.** The complete course
[population](../../../../tests/fixtures/population_course.json) and
[schedule](../../../../tests/fixtures/schedules_course.json) were prepared with
master seed `20261009` using explicit `--regime course` and the new
[input-only size config](../../../../configs/course-inputs.toml). They contain
20 main/five development worlds, balanced owners, exact eight-world focal cohorts
and five extra continuation replicates. Independent enumeration reconciles
**5,752 new / 6,280 logical / 528 replay main slots** and
**1,114 / 1,178 / 64 development slots**, with the initial 90 capability slots.

The corrected full CPU CLI passes **534 tests, zero skips**; dependency-free
core validation passes **342 tests (334 passed, six checkpoint-library and two
optional-renderer skips)**. Installed M1/course validation passes 73 tests, and
all fourteen installed course tests pass separately under hash seed 37, with
zero skips and no source-path injection. Fresh hash seeds 1/3981 also reproduce
both canonical artifacts with optional imports blocked. Exact commands, logs,
the retained initial discovery failure/fix, independent component/seed/parent
checks, link/status checks and protected-file audit are in
[M1 input/schedule evidence](../../../validation/course-m1-inputs-and-schedules.md).
Both original sizes and 60/40 counts/defaults remain correct; 1,148 protected
baseline files, including the pre-existing unstaged M5 edit, remain byte-identical.

The course M1 input/schedule gate is passed. [Course/M2-T01](../M2/M2-T01-course-protocol-and-limits.md)
is ready to carry the adopted 256/64 limits through the real protocol. Later
intervention/capacity, runtime/analysis, CPU, model/resource, pilot, freeze and
execution gates remain open. No model generation, GPU allocation, freeze or
empirical execution was performed or authorized by this handoff.
