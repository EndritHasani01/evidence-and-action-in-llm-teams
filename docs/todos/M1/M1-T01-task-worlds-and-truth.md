# M1-T01 — Exact task worlds and coordinate contracts

**Status:** done

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
The revision/coordinate adversaries, candidate rejection checks and clean CPU
installation validation below completed the remaining criteria.

**Completion evidence (4 October 2026):** Windows x64 (build 26200), CPython
3.11.9. The final suite passed **23/23 tests**, with no inference or experiment
execution. Executed commands:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --no-deps -e .
.\.venv\Scripts\python.exe -m recovery validate
.\.venv\Scripts\python.exe -m pip check
python -S -m recovery validate
git diff --check
```

Editable installation succeeded; `pip check` reported no broken requirements.
The fresh environment contains only this project 0.1.0, pip 24.0 and setuptools
65.5.0 at runtime (build dependencies use an isolated build environment).
The installed validation command also passed from the host temporary directory,
confirming discovery/configuration do not depend on the working directory.
These versions describe CPU evidence, not the accepted M5 inference lock.

| Acceptance area | Executed checks / artifacts | Result |
|---|---|---|
| Five target/fallback generators and exact solvers | `GeneratedWorldTests.test_all_families_both_sizes_independent_truth_and_contracts`; [independent references](../../../tests/references.py) | 1,000 deterministic draws agree; all assigned and full-information outputs/lengths/keys pass. |
| Specified distributions, ownership and IDs | `GeneratedWorldTests` in [test_tasks.py](../../../tests/test_tasks.py) | Inclusive value domains; all 16 four-node Prüfer sequences yield distinct connected trees; tree plus exactly five sampled nonedges; equal source partitions; value-independent manifests and endpoint-independent shuffled BFS slots. |
| Ordered/multiplicity-preserving exact contracts | `CandidateContractTests` in [test_truth_contracts.py](../../../tests/test_truth_contracts.py) | Correct shapes accepted; bool/float/string/nonfinite/coerced candidates, wrong lengths and noncanonical BFS keys rejected. Wrong integer answers remain shape-valid and score false; same-set/wrong-order or wrong-multiplicity answers score false. |
| D/U, shard boundaries and old/new truth | `RevisionTruthTests` in [test_truth_contracts.py](../../../tests/test_truth_contracts.py) | Every numeric Prefix/Difference position at both sizes, positive/negative deltas, duplicate Top-K cutoffs and missing reserves, Sort crossings across all four peers, BFS preserving/longer-path/disconnecting deletions, source distance 0 and unreachable −1 pass. Empty/nonempty D and unique/peer-copy counts pass. |
| Immutable raw sources and evaluator separation | `WorldValidationTests`, revision and identity checks | Invalid raw types/ranges/positions/owners/edges fail; record order does not change truth; updates preserve IDs and do not mutate old worlds or retained candidates. Gold/footprints stay in evaluator records; public source manifests contain only ID/owner/position. |
| Selected native fixtures | `NativeFixtureTests`; [fixture provenance](../../../tests/fixtures/README.md) | Ten I-09/II-11/II-17/III-21/III-24 native cases (2/5 peers) independently match stored gold, and extracted fields match attributed vendor JSON. |
| CPU isolation and configuration | [test_cpu_entrypoint.py](../../../tests/test_cpu_entrypoint.py), site-disabled run, fresh editable install | Both size choices work; undeclared/mixed configuration fails; fresh process forbids model/numerical/framework imports; global and unrelated local RNG streams remain unchanged. |

An inline documentation audit verified 120 relative links/anchors and all 29
task-file statuses against the index, including completed/ready/blocked counts
and the M1-T01 → M1-T02 readiness transition. A wrong fixture-attribution relative
link was corrected before that passing audit. No scientific design change or new
CPU dependency was required. M1-T02 now owns eligibility conditioning, legal
edit sampling, persisted populations and streams; M1-T03 owns schedules. The
M1 milestone gate and all GPU/protocol/pilot/empirical gates remain open.

