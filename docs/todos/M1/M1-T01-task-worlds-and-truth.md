# M1-T01 — Exact task worlds and coordinate contracts

**Status:** active

**Dependencies:** None.

## References

- [Repository contract](../../../AGENTS.md).
- [Plan §2: small architecture](../../IMPLEMENTATION_PLAN.md#2-small-implementation-architecture) and [M1](../../IMPLEMENTATION_PLAN.md#3-milestone-m1--reproducible-worlds-truth-and-schedules).
- Specification [§2.1](../../../PROJECT_SPECIFICATION.md#21-task-definitions), [§5.1](../../../PROJECT_SPECIFICATION.md#51-exact-outcomes), [§7.1](../../../PROJECT_SPECIFICATION.md#71-repair-preservation-and-synchronized-completion), [§8.1–8.2](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls), and [§9–10](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [repository reuse and task risks](../../implementation-research/repository-and-validation.md#task-generation-contains-the-meaningful-hidden-risks).

## Intended outcome

A CPU-usable mathematical core generates the five declared task families and independently evaluates their exact output contracts, with explicit source ownership and output-coordinate mappings.

## Scope and boundaries

- Establish only the small Python 3.11 package/configuration and CPU validation entry point needed for this outcome. Keep inference dependencies optional and unimported during CPU validation. Use the plan's direct functions and explicit records; filenames remain implementation choices.
- Implement Top-K, Prefix Sum, Difference Array, Distributed Sort and BFS with their specified value ranges, ownership and answer placement. BFS uses a uniform labeled Prüfer tree plus five uniformly sampled nonedges.
- Support the target and only the declared uniform fallback: numeric m=8/6; BFS 12 nodes/16 edges/four edges per peer or eight nodes/12 edges/three per peer. Top-K always returns ten values. Full-information Prefix/Sort return all n coordinates.
- Separate numeric source ownership, public positions and output ranks. Use value-independent IDs; BFS IDs and ordering must not disclose endpoints. Keep full inputs/gold/coordinate footprints evaluator-side.
- Reuse selected SILO mathematics/fixtures with provenance and attribution. Do not install its Python >=3.13 package, import its RNG-seeding generators, reuse its runner/scorer, or run archive scripts that overwrite evidence. CPU Max is a later information illustration, never a sixth live family.

## Completion criteria

- All five target/fallback generators and exact solvers satisfy the specification, including list order/multiplicity, full canonical BFS keys and unreachable -1.
- Explicit unique-coordinate and peer-assignment maps support old/new D/U sets without treating replicated answers as independent coordinates.
- Team and full-information candidate contracts are available to the protocol and schedule tasks.
- CPU validation runs without loading or importing the model stack; selected reference fixtures retain source attribution.

## Validation and evidence

Compare production solvers with independently implemented small references and selected native fixtures. Cover duplicate cutoffs/discarded reserves, numeric endpoints and shard boundaries, negative differences, Sort rank crossings, BFS alternatives/disconnection, and both size configurations. Include old/new examples with empty and nonempty D and assert every output length/key/coordinate assignment. Verify generators do not disturb unrelated random streams.

**Evidence (checkpoint, 4 October 2026):** On Windows / Python 3.11.9,
`python -m recovery validate` passed 8 tests. These compare all five families
at both sizes over 1,000 deterministic draws against independent references,
verify ten attributed native fixtures, Prüfer bijection and five-nonedge sampling,
ownership/identity separation, inclusive numeric domains and RNG isolation.
Code: [tasks.py](../../../recovery/tasks.py), [truth.py](../../../recovery/truth.py).
Checks: [test_tasks.py](../../../tests/test_tasks.py),
[independent references](../../../tests/references.py),
[fixture provenance](../../../tests/fixtures/README.md).
Revision/coordinate adversaries, candidate rejection checks and clean CPU
installation validation remain before completion.

