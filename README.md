# Recovery in distributed LLM teams

A controlled study of how multi-agent teams recover when information used during distributed problem solving is corrected.

The design uses five SILO-derived task families to study retained evidence and computation, historical change information, and how recovering peers affect one another. Shared-prefix revision and no-change continuations provide matched controls.

## Project status

The five task generators, exact solvers, candidate contracts and coordinate maps
are implemented and verified on CPU for both declared sizes. The correction
protocol, population/schedule preparation, workflow, Qwen3.5/T4 pilot and main
experiments remain future work. See [M1-T01 evidence](docs/todos/M1/M1-T01-task-worlds-and-truth.md#validation-and-evidence)
and the [implementation plan](docs/IMPLEMENTATION_PLAN.md#10-living-handoff).

## Start here

- [Project specification](PROJECT_SPECIFICATION.md) is the current source of truth.
- [SILO repository audit](research/07_repository_audit/SILO_REPOSITORY_AUDIT.md) records supporting inspection findings.
- [Completed research archive](research/README.md) provides an agent reading order, phase structure, full file index and machine-readable manifest. Earlier plans, blueprint code and configurations are historical; the final specification supersedes their conflicting recommendations.

## Scope

Four peers perform four rounds of collaborative work before an announced factual revision, then receive four recovery rounds. The study targets 60 worlds, with a 40-world resource fallback. The specification defines the retention and complementary team-reset comparisons, focused receipt/prose interventions, two primary estimands, exact evaluation, repetition, and measured feasibility gates.

## CPU installation and validation

Use Python 3.11. The mathematical core and its tests need only the standard
library; inference dependencies are optional and are not imported by validation.
From this source checkout, run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --no-deps -e .
.\.venv\Scripts\python.exe -m recovery validate
```

Without installation, `python -S -m recovery validate` runs the same checks with
site packages disabled. Validation requires this checkout's tests and attributed
vendor JSON. It checks both sizes regardless of the configured size, exits
nonzero on failure, and never loads a model or executes an experiment.
`--config path/to/study.toml` accepts exactly `size = "target"` or
`size = "fallback"`; [the default configuration](configs/study.toml) is a
mathematical default, not the accepted M5 model/environment freeze.

## Task core interfaces

[tasks.py](recovery/tasks.py) owns raw worlds and public shape/assignment
contracts; [truth.py](recovery/truth.py) owns offline gold and D/U footprints.
Worlds and source records are immutable. Source positions/owners and output
coordinates are explicit: Sort source ownership does not determine output rank
ownership, and Difference coordinate `j` occupies candidate list index `j−1`.

| Family | Unique coordinates | Per-peer candidate | Full-information candidate |
|---|---|---|---|
| Top-K | Ranks 0–9 | Ten descending values, including duplicates | Same ten values |
| Prefix | Positions 0–n−1 | m global cumulative sums at peer's assigned positions | All n sums |
| Difference | d₁–dₙ₋₁ | Full ordered n−1 differences | Same n−1 differences |
| Sort | Ranks 0–n−1 | m ascending values at peer's assigned ranks | All n values |
| BFS | Nodes 0–11 / 0–7 | Full dictionary of canonical decimal-string keys; unreachable −1 | Same dictionary |

Target uses m=8 and BFS 12 nodes/16 edges/four edges per peer. Fallback uses
m=6 and BFS eight nodes/12 edges/three edges per peer. Both keep top ten and
five added nonedges. `generate_world` makes one unconditioned draw; owner
eligibility, edit selection, rejection accounting and saved population streams
are the next task, [M1-T02](docs/todos/M1/M1-T02-edits-and-populations.md).

```python
from random import Random
from recovery.tasks import Task, Size, generate_world, candidate_contract, source_manifest
from recovery.truth import solve_world, changed_coordinates, exact_candidate

world = generate_world(Task.PREFIX, Size.TARGET,
                       generation_rng=Random(10), ownership_rng=Random(20))
manifest = source_manifest(world)       # Public IDs, owners and positions only.
contract = candidate_contract(world.task, world.size, peer=1)
truth = solve_world(world)             # Offline evaluator use only.
assert contract.error(truth.candidate(1)) is None
assert exact_candidate(truth, truth.candidate(1), peer=1)
assert not changed_coordinates(truth, truth).changed  # Sham: empty D.
```

`candidate_contract(..., peer=None)` gives the full-information shape;
`coordinate_map` supplies ordered peer assignments and the inverse coordinate
to peers map. Replicated answers add peer copies, not independent coordinates.
Candidate shape errors contain no gold; a wrong integer answer of valid shape
remains valid for the later protocol. `exact_candidate(..., protocol_valid=False)`
scores an invalid recorded reply as false without reusing an earlier candidate.
Strict whole-reply parsing, communication permissions and token caps belong to M2.

The [independent references and attributed fixtures](tests/fixtures/README.md)
validate task truth, not model capability, native SILO scores or recovery effects.
