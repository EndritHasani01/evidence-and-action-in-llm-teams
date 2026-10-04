# Recovery in distributed LLM teams

A controlled study of how multi-agent teams recover when information used during distributed problem solving is corrected.

The design uses five SILO-derived task families to study retained evidence and computation, historical change information, and how recovering peers affect one another. Shared-prefix revision and no-change continuations provide matched controls.

## Project status

The five task generators, exact solvers, candidate contracts, coordinate maps,
eligible edits and saved populations/streams are implemented and verified on CPU
for both declared sizes. Complete main/development schedules and replay dependencies
also pass independent CPU checks. M1's gate is passed. Permitted peer views,
lossless request rendering, strict whole-reply validation, synchronous
scripted rounds/drained prefixes, literal event/retention/receipt boundaries and
exact mixed/Q replay and local-view attainability pass 163 CPU checks plus
32 native verification checks. **M2 is blocked at capacity:** both declared sizes
have reachable requests exceeding 8,192 tokens; literal surrogate prose also
exposes a tokenizer gap. Neither size is admitted. The durable workflow,
Qwen3.5/T4 pilot and main experiments remain future work. See
[M2-T06 blocked evidence](docs/todos/M2/M2-T06-attainability-and-capacity.md#blocked-handoff-and-required-decision),
[M2-T05 evidence](docs/todos/M2/M2-T05-mixed-and-prose-delay-replay.md#completion-and-handoff),
[M2-T04 evidence](docs/todos/M2/M2-T04-events-retention-and-receipts.md#completion-and-handoff),
[M2-T03 evidence](docs/todos/M2/M2-T03-synchronous-rounds-and-prefixes.md#completion-and-handoff),
[M2-T02 evidence](docs/todos/M2/M2-T02-strict-replies-and-feedback.md#validation-and-evidence),
[M2-T01 evidence](docs/todos/M2/M2-T01-peer-views-and-rendering.md#completion-and-handoff),
[M1-T03 gate evidence](docs/todos/M1/M1-T03-complete-schedules.md#acceptance-and-m1-gate),
[M1-T02 evidence](docs/todos/M1/M1-T02-edits-and-populations.md#validation-and-evidence),
[M1-T01 evidence](docs/todos/M1/M1-T01-task-worlds-and-truth.md#validation-and-evidence)
and the [implementation plan](docs/IMPLEMENTATION_PLAN.md#10-living-handoff).

## Start here

- [Project specification](PROJECT_SPECIFICATION.md) is the current source of truth.
- [SILO repository audit](research/07_repository_audit/SILO_REPOSITORY_AUDIT.md) records supporting inspection findings.
- [Completed research archive](research/README.md) provides an agent reading order, phase structure, full file index and machine-readable manifest. Earlier plans, blueprint code and configurations are historical; the final specification supersedes their conflicting recommendations.

## Scope

Four peers perform four rounds of collaborative work before an announced factual revision, then receive four recovery rounds. The study targets 60 worlds, with a 40-world resource fallback. The specification defines the retention and complementary team-reset comparisons, focused receipt/prose interventions, two primary estimands, exact evaluation, repetition, and measured feasibility gates.

## CPU installation and validation

Use Python 3.11. Strict reply validation requires Pydantic 2, declared as a CPU
dependency. The mathematical core remains standard-library only. Inference
dependencies are optional and are not imported by CPU validation. From this
source checkout, run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m recovery validate
```

Full validation includes the core, strict-reply, scripted-round, event, replay and
local-view attainability checks. Native tokenizer/capacity admission is checked
separately with local pinned metadata. Without installation,
`python -S -m recovery validate --core-only` runs only the dependency-free core
subset with site packages disabled; it explicitly excludes strict replies, rounds,
events, replay and attainability
and cannot establish their gate. Full validation fails if Pydantic is unavailable.
Validation requires this checkout's tests and attributed vendor JSON. It checks
both sizes regardless of the configured size, exits nonzero on failure, and
never loads a model or executes an experiment.
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
five added nonedges. `generate_world` makes one unconditioned draw;
[edits.py](recovery/edits.py) and [populations.py](recovery/populations.py) own
mathematical eligibility, edit selection, bounded rejection and saved streams.

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
Strict whole-reply parsing, communication permissions and token caps are supplied
by [protocol.py](recovery/protocol.py). `validate_reply(view, generated, tokenizer)`
takes only the immutable sender view, literal recorded text/generated token IDs,
termination information and a tokenizer. It returns separate JSON/schema/permission
checks, token counts, a candidate outcome and all-or-none staged messages. Wrong
integers remain protocol-valid. Repeated lawful references retain each delivery
attempt. Feedback uses fixed public descriptions checked against 32 actual tokens;
invalid/failed slots supply no candidate. Raw replies stay literal own-history data,
and generating-slot labels prevent feedback from entering that same call.
[rounds.py](recovery/rounds.py) prepares all four immutable requests before any
reply, validates all replies before effects, and commits exact source/text
deliveries for the next round. Component IDs retain every reference attempt
separately from unique acquisitions. `run_prefix` archives four complete rounds
and produces a drained immutable JSON snapshot; `fork_prefix` deep-deserializes
each continuation independently. `RoundResult.barrier` preserves the exact
pre-delivery views/requests/replies for later reuse.

[events.py](recovery/events.py) supplies
`start_continuation(prefix_bytes, prepared_world, scheduled_branch)`. It checks
the saved schedule and original prefix, then applies the single event and literal
L/B/C/K/F/mask/receipt boundary. All siblings, preserving edits and repeats start
from that original snapshot. Public notices invalidate stale sources; unknown
replacement content stays pending. K keeps the actual fourth-slot result or
absence and preserves it as labeled history when a new outcome replaces the
latest candidate. `BranchState.boundary_applied` derives from persistent notices
and survives serialization; durable apply-once execution remains M3.
The [boundary archive](tests/fixtures/README.md#event-boundaries-and-receipt-pairs)
records paired renders and actual receipt token costs. Mixed and Q initial
requests match their prescribed B/C parents.

[replay.py](recovery/replay.py) supplies `obtain_continuation_round` followed by
`commit_continuation_round` for scheduled continuations. Obtain returns an
in-memory `SavedRound` containing the schedule, captured settings and original
pre-delivery barrier. Mixed/Q round one requires the exact saved B/C records;
missing records or different event/replicate, view, rendered/native request,
settings, seed or recorded validation stop as protocol defects. No provider is
called for replay, including invalid/failed parents. New calls receive their
saved seed and settings alongside the permitted view/request.

Commit reconstructs branch-local effects. Q delivers sources normally, retains
own replies, holds only incoming first-round prose, and releases it before
round-two prose at the round-three boundary. Existing history order is preserved.
`held_prose_counts` derives per-recipient nonempty held-text counts from committed
queues/deliveries, including zero for inactive Q; it rejects unexecuted recovery
and uncommitted rounds. No queue data enters a peer view.
The [replay archive](tests/fixtures/README.md#exact-parent-replay-and-delayed-prose)
records 72 exact parent comparisons and complete Q release traces. Use these
scheduled obtain/commit steps for continuation execution; `rounds.py` provides
the underlying pure operations. Complete capacity is blocked in M2-T06; durable
reply persistence/checkpoints remain M3.

## Protocol attainability and capacity

[witness.py](recovery/witness.py) is a CPU validation strategy. Each peer forwards
its current private shard to a different peer in rounds 1–3, then solves from
locally acquired records. It uses legal placeholders earlier and receives no
host gold or unseen records. The retained
[witness trace](tests/fixtures/README.md#protocol-attainability-witness) covers
all families/sizes and scheduled siblings/repeats/controls, including L forwarding,
F reacquisition, receipts and mixed/Q replay. Candidate/control/own-shard outputs
fit 384 tokens at both sizes. This establishes attainability, not LLM capability.

Complete capacity fails. A permitted invalid 384-token reply retained after one
actual scripted round makes the next request use 14,642 target / 14,349 fallback
tokens including the output reserve, above 8,192. The
[capacity report](tests/fixtures/README.md#complete-capacity-failure-evidence)
retains the exact counterexamples, full-horizon accounting/adversarial views,
failed simple lossless layouts and a separate unpaired-surrogate gap. The live
renderer preserves literal history and rejects overflow. The specification and
default configuration are unchanged; an explicit protocol resolution is needed
before M2 closes.

```powershell
python -m unittest tests.attainability_checks -q
python -m tests.tokenizer_attainability --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_capacity --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
```

The native commands require the locally downloaded pinned tokenizer metadata
described in [M2-T06](docs/todos/M2/M2-T06-attainability-and-capacity.md#reproduction-environment-and-commands).
All six capacity verification checks pass, then that command deliberately exits
**1** for failed admission; exit **2** means a verification check failed. CPU
validation passing does not override this native gate. No GPU use is admitted.

The [independent references and attributed fixtures](tests/fixtures/README.md)
validate task truth, not model capability, native SILO scores or recovery effects.

## Prepared populations

Prepare a new host manifest without a model call:

```powershell
python -S -m recovery prepare --seed 20261004 --output population.json
python -m recovery validate --manifest population.json --authoritative tests/fixtures/population_target.json
```

The manifest contains 60 main worlds and five disjoint development worlds,
actual original sources/edits, balanced edited owners, partitions, eligibility,
rejection reasons and preassigned streams. Existing files are protected from
overwrite. Loading uses the saved actual records; `--authoritative` additionally
compares all inputs/configuration with a saved baseline. Mathematical validation
alone cannot prove that a valid input has stayed unchanged.

The 40-world fallback is a view of the first eight worlds per family; it is
independent of the uniform mathematical `--config` size. Receipt (Prefix/Sort),
Q (Sort/BFS), preserving (first eight Top-K/BFS), and repeat (first two per family)
subsets derive from this same authority. The extra replicate keeps the original
prefix/partition and gets new continuation seeds. Event and policy do not enter
the continuation seed key, so siblings share seeds; required exact response
parents are explicit in the schedule. Runtime equality and replay effects are
verified in memory; durable integration remains M3.

```python
from pathlib import Path
from recovery.manifests import load_population

population = load_population(Path("population.json"))
nested_worlds = population.worlds(40)
subsets = population.subsets(40)  # main 40, receipt/Q 16, preserving 16, repeat 10
world = nested_worlds[0]
revision = world.event_world("revision")  # Each event starts from world.world.
sham = world.event_world("sham")
seed = world.streams.continuation_seed(replicate=0, round_number=1, peer=0)
```

Full population manifests are host-owned and include hidden sources/future edits;
peer metadata uses only `source_manifest(world.world)`. Evaluator truth/footprints
remain separate. The retained [CPU fixtures](tests/fixtures/README.md#prepared-host-populations)
are prepared inputs, not an accepted M5 freeze, pilot or empirical results.

## Complete CPU schedules

Enumerate and save every opportunity from an existing population without resampling:

```powershell
python -S -m recovery prepare --manifest population.json --output schedules.json
python -m recovery validate --manifest population.json --schedule schedules.json --authoritative tests/fixtures/population_target.json
```

The saved schedule contains main 60 and the exact development matrix; the nested
40 derives from its existing calls. Main distinct/logical counts are
16,152/17,656 and 11,504/12,560. Development has 1,114 distinct/1,178 logical slots,
with 80 prefix and ten complete-world control calls first. Smoke is separate,
with at most 24 additional calls (1,138 distinct combined). The counts hold for
both mathematical sizes; pass the fallback configuration and population to both
commands when using `size = "fallback"`.

```python
from pathlib import Path
from recovery.manifests import load_population, load_schedules
from recovery.schedule import dependency_order

population = load_population(Path("population.json"))
schedules = load_schedules(Path("schedules.json"), population)
main = schedules.main_for(population, 40)  # Same prefix, call IDs and seeds as main 60.
ordered_calls = dependency_order(main)   # CPU order of (branch, call) pairs.
capability = schedules.capability         # First 90 development calls; no recovery.
```

Each branch supplies world/task/event/policy/replicate/phase grouping. Each call
has round/peer/seed identity and a `generation_id`: its own call ID for a distinct
generation, or its exact B/C first-round `replay_parent`. Equal seeds alone never
authorize reuse. Continuations explicitly name their original `prefix_parent`;
extra repeats have new continuation IDs/seeds and retain that prefix/partition.
Controls use `peer=None`, the full-world candidate contract and `send=[]`.
`Branch.output_contract` and `Branch.empty_send` expose those requirements to M2.

Validation checks the full matrix, seeds, parents and dependency orders without
model calls. Replay order includes previous-round/prefix dependencies. In-memory
request/state/settings equality and synchronous delivery are verified in M2;
durable raw-reply reuse remains M3. Saved files cannot be overwritten. The population is the raw
input authority; schedules are derived records, with no copied sources/gold or
accepted inference configuration. Optional saved-schedule comparison is available
through `load_schedules(..., authoritative=saved_schedule)`. Schedule labels are
host-only and must never enter peer views.

The [retained CPU schedule and reproduction notes](tests/fixtures/README.md#prepared-host-schedules)
provided M2's input handoff. M1's original 59-check suite passed with site packages
disabled and through the installed CPU package outside the checkout; current
protocol evidence is linked above. Model/resource feasibility and empirical
recovery remain untested.

## Permitted peer views and exact requests

[state.py](recovery/state.py) owns immutable permitted views; [prompts.py](recovery/prompts.py)
renders them as one user turn with labeled JSON data. The host projects an ordinary
`World` into a private peer shard or a complete-world control. The renderer itself
accepts only `PeerView`, with no evaluator, schedule, condition or delayed queue.

```python
from recovery.state import initial_view, held_source
from recovery.prompts import render_request, tokenize_request

view = initial_view(world, peer=1)  # world from the task-core example above
request = render_request(view)
chat_messages = request.messages()
record = view.sources[0]
assert held_source(view, record.record_id, record.version) == record
# With an explicitly loaded local CPU tokenizer:
# tokenized = tokenize_request(request, tokenizer)
```

Current sources render once, separately from literal own replies/received prose,
public schema feedback and persistent notices/receipts. Pending replacements have
no usable old value; known BFS tombstones retain deleted endpoints. Historical
receipt before-values never enter current-source lookup. Invalid/failed slots have
no candidate, wrong compact results remain literal, and a newer own reply/feedback
slot cannot retain an older latest candidate. Event/retention, delivery and
replay transformations are implemented by the interfaces above.

`tokenize_request` applies the injected native non-thinking template, preserves its
exact text, token IDs and attention mask, and reserves all 384 output tokens inside
8,192. Oversized requests fail without truncation. `dataclasses.asdict`/ordinary
JSON can save the request and token record in the later call ledger.
The [seven retained short request/token fixtures](tests/fixtures/README.md#permitted-peer-requests-and-tokenizer-inputs)
and [native tokenizer harness](tests/tokenizer_peer_views.py) verify literal archive
preservation and exact native inputs. M2-T01's original 79-check CPU suite and
five native-tokenizer checks passed; the current 163 CPU/32 native checks include
the subsequent protocol, round, event, replay, witness and capacity-failure
evidence. Complete worst-context admission is blocked in M2-T06.
