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
exact mixed/Q replay and local-view attainability pass 167 CPU checks plus
37 native verification checks. **M2's CPU gate passes:** the authorized literal
layout preserves retained work within a complete 261,388-token upper bound,
including output reserve, under the uniform 262,144 limit. Unpaired message
surrogates are bounded whole-reply schema failures. Both sizes are CPU-admitted;
GPU memory/capability/timing remain untested. Durable rounds now run through real
LangGraph/SQLite checkpoints with exact raw reply/failure reuse and branch-local
effects. Bounded process execution and controller-death recovery enforce durable
timeouts, one identical infrastructure retry and observed/uncertain work;
18 durable, 22 attempt, 14 worker, 23 accounting and nine lifecycle checks pass
in the 253-check source/installed CPU suites; the dependency-free core passes 81.
Balanced local workers now access original prefix/replay parents read-only,
execute durable controls and resume assigned checkpoints after interruption.
Physical/policy accounting, read-only progress, allocation attribution and safe
budget stops now pass CPU checks with synthetic allocations, historical measured
costs and explicit unknowns. **M3's CPU gate passes:** eleven real external
controller kills preserve exact resumed states/deliveries, cleared fields,
held prose and bounded retries. The fourteen-case
[ordinary scripted bundle](tests/fixtures/scripted_lifecycle_run.zip) reproduces
4,340 logical slots and 384 exact replay uses, with offline reconstruction and
reopened backups. **M4-T01 is implemented and verified:** exact offline outcomes,
coordinate repair/preservation, trajectories and observable annotations reproduce
sixteen retained table cases. The complete regression passes 278 checks, final
core passes 108 and installed-library evaluation passes 27. **M4-T02 is implemented
and verified:** all prespecified contrasts, fixed/equal-family denominators,
unknown components and separate conditional repeats reconstruct from original
workers. The complete CPU regression passes 306 checks; core and installed
analysis checks pass 134 and 54. Four retained contrast-table cases reproduce,
including the full unknown main populations. **M4-T03 is implemented and
verified:** information inventories, conservative source associations, receipt
timing and deterministic work references reproduce six retained cases and 200
native history counts. The complete integrated CPU regression passes 334
checks; final core checks pass 160 with two optional skips, and installed-library
verification passes 81. **M4-T04 is implemented and verified:** original measured
costs and the frozen C/K coverage rule reproduce sixteen retained cases, with
whole-branch costs, unknown selected branches and fixed denominators. Complete
CPU regression passes 362 checks; final review passes 191 core checks (188
passed, three optional skips) and 110 installed-library checks. **M4-T05 is
implemented and verified:** paired world intervals, shared-response missingness,
completion bounds and paired whole-policy displays reproduce sixteen retained
cases. Complete CPU regression passes 396 checks; final focused checks pass 33,
core checks run 225 (221 passed, four optional skips), and installed-library M4
checks pass 144. **M4-T06 is implemented and verified; M4's CPU gate passes.**
Seven grouped exhibits, exact cases and five portable complete/incomplete/stopped
reports are retained. Full source regression passes all 424 checks, including
all nine lifecycle checks. Focused/core/installed checks pass 25/252 (244 passed,
eight optional skips)/166. All sixteen original-worker scopes reproduce twice
with identical tables, cases, plotting inputs and export bytes. **M5-T01 is ready
for CPU preparation.** Qwen3.5/T4 hardware, capability, resource admission,
pilot and main experiments remain future work. See
[M4-T06 completion evidence](docs/todos/M4/M4-T06-reproducible-report-and-cpu-gate.md#completion-and-m4-gate),
[M4-T05 completion evidence](docs/todos/M4/M4-T05-uncertainty-and-missingness.md#completion-and-handoff),
[M4-T04 completion evidence](docs/todos/M4/M4-T04-policy-costs-and-boundary-rule.md#completion-and-handoff),
[M4-T03 completion evidence](docs/todos/M4/M4-T03-information-and-work-diagnostics.md#completion-and-handoff),
[M4-T02 completion evidence](docs/todos/M4/M4-T02-estimands-and-repeatability.md#completion-and-handoff),
[M4-T01 completion evidence](docs/todos/M4/M4-T01-exact-outcomes-and-trajectories.md#completion-and-handoff),
[M3-T05 gate evidence](docs/todos/M3/M3-T05-crash-safe-scripted-lifecycle.md#completion-and-m3-gate),
[M3-T04 evidence](docs/todos/M3/M3-T04-accounting-progress-and-budget.md#validation-and-evidence),
[M3-T03 evidence](docs/todos/M3/M3-T03-local-worker-scheduling.md#validation-and-evidence),
[M3-T02 evidence](docs/todos/M3/M3-T02-bounded-attempts-and-failures.md#validation-and-evidence),
[M3-T01 evidence](docs/todos/M3/M3-T01-durable-round-runner.md#validation-and-evidence),
[M2-T06 completion evidence](docs/todos/M2/M2-T06-attainability-and-capacity.md#completion-and-m2-gate),
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
dependency; durable execution also uses the declared tested LangGraph/SQLite
packages. These CPU pins are not the M5 inference/environment freeze.
The mathematical core remains standard-library only. Inference
dependencies are optional and are not imported by CPU validation. From this
source checkout, run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m recovery validate
```

Full validation includes the core, strict-reply, scripted-round, event, replay,
local-view attainability, durable runner, bounded CPU subprocess, local worker,
accounting and externally killed lifecycle checks. Native tokenizer/capacity admission is checked
separately with local pinned metadata. Without installation,
`python -S -m recovery validate --core-only` runs only the dependency-free core
subset with site packages disabled; it explicitly excludes strict replies, rounds,
events, replay, attainability, durability, attempts and workers
and cannot establish their gate. Full validation fails if Pydantic is unavailable.
Full validation also requires LangGraph and its SQLite saver.
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
and survives serialization; M3-T01 now commits that boundary once in its new thread.
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
records 104 exact parent comparisons and complete Q release traces. Use these
scheduled obtain/commit steps through [runner.py](recovery/runner.py) for durable
execution; `rounds.py` provides the underlying pure operations. Complete CPU
capacity passes in M2-T06.

`DurableRunner(path, tokenizer, ProcessProvider(factory))` serially owns one worker
file. The importable factory loads a resident inference provider in a spawned
child, receiving only permitted inputs for each independent call. Use
`scripted=True` with direct providers only for deterministic CPU fixtures.
`start(prepared_world, scheduled_branch, settings=...)` durably initializes a
prefix or deep-forked event boundary. `run_round(branch_id, round_number)` obtains
the four exact calls, then commits branch-local delivery with synchronous
checkpoints. Repeating that explicit round returns its committed result. The
provider receives only the permitted view, literal rendered/native request,
saved seed and fresh settings. Exact raw replies/final failures live in
[storage.py](recovery/storage.py); logical replay points to its physical parent
without duplicating raw outcomes. The default 120-second attempt bound includes
loading and communication; terminate/kill each have a one-second grace. Known
timeouts are saved before termination and never retried. Restart after a stopped
owner records uncertain completion and allows at most one identical-request
infrastructure retry; completed outcomes always win. Durable heartbeats and
process loading/idle intervals retain work for later accounting. `state`, `result` and `deliveries` read
committed checkpoints, and `backup` uses SQLite's backup API, including live WAL.
The [durable archives](tests/fixtures/README.md#durable-round-runner-traces)
reproduce CPU-counter and native-tokenizer execution without model inference.
The [failure archive](tests/fixtures/README.md#bounded-attempt-and-process-failure-traces)
adds measured CPU hangs, timeout/termination and actual controller-kill recovery.

## Resource accounting and read-only status

[accounting.py](recovery/accounting.py) derives logical/generation/attempt joins,
policy costs, allocation, forecasts, matched coverage and resumable work from
saved schedules and worker files. It uses no evaluator correctness or progress
database. Invalid replies and recorded failures count as finished work;
unexecuted slots remain unknown. Each continuation's cost includes its original
16-call prefix and all 16 continuation uses, including measured replay-parent
attempts and F's abandoned prefix. Unknown durations/output tokens and absent
memory measurements stay explicit.

```powershell
.venv/Scripts/python.exe -m recovery status --manifest population.json --schedule schedules.json --worker worker-0.sqlite --worker worker-1.sqlite
.venv/Scripts/python.exe -m recovery status --manifest population.json --schedule schedules.json --worker worker-0.sqlite --worker worker-1.sqlite --stage main --count 40 --json
```

These commands only read; missing worker files are unknown work and are never
created. JSON includes every scheduled slot/parent and resumable branch. Add
`--prior-worker <path>` for every worker file from earlier measured development
or failed configurations. Historical allocation remains charged once; only
matching saved generation settings supply timing samples. Physical IDs are
scoped by the existing saved settings when configurations differ. Repeated
copies of the same physical records are rejected.

`LocalScheduler(..., report=terminal_progress)` reports call/round transitions
and bounded heartbeats while `run`/`advance` operates. Import `terminal_progress`
and `Budget` from `recovery.accounting`. For budgeted execution each `WorkerSpec`
must identify its `allocated_device`; `allocated_at` can supply the provider's
actual reservation start before worker/model setup, and `provider_billing`
records its separate billing rule. The scheduler requires a bounded
`release_device(worker_index, device)` callback acknowledging actual release
with `True` or its zoned timestamp. A local process exit alone leaves allocation
open. `MeasuredReply(exact_response, peak_memory_bytes)` optionally records an
adapter measurement without changing the scientific raw reply.

Budget binding preserves the ceiling/reserves/overhead/shutdown allowance on
restart. Admission requires conservative measured phase/condition/device
ranges for main work and reserves every possible timeout/termination in the
next round. The forecast pools measured families within each phase/condition,
shows the observed prompt envelope, uses the slower device with a 25% margin,
and charges idle devices in its serialized upper bound. Missing measurements
are unavailable. An independent allocation deadline also stops hung work;
confirmed worker/provider exit preserves uncertain attempts before release.
`BudgetStop` retains all scheduled slots and exact resumable state. Loading
inside measured attempts is already charged; the allocation partition is never
added to those attempt costs. Outside idle/setup remains experiment overhead.

[M3-T04 evidence](docs/todos/M3/M3-T04-accounting-progress-and-budget.md#validation-and-evidence)
records CPU checks with explicitly synthetic allocations. Actual GPU timing,
memory, provider release integration, timeout adequacy and the accepted freeze
remain M5 gates; the integrated lifecycle gate remains M3-T05.

## Scripted crash and offline lifecycle validation

[lifecycle_checks.py](tests/lifecycle_checks.py) exercises real externally killed
controllers at raw-reply, validation, staging, reset and delivery-checkpoint
boundaries. Resumed worker files retain exact requests, invalid/failed replies,
branch-local effects, held prose and uncertain physical attempts. The CPU
fixture uses the existing prepared worlds and schedule; it is not a pilot or
main experiment.

[lifecycle_archive.py](tests/lifecycle_archive.py) packages ordinary population/
schedule manifests, SQLite backups and derived progress/outcome evidence in
[scripted_lifecycle_run.zip](tests/fixtures/scripted_lifecycle_run.zip). Read it
without generation, or reproduce the scripted validation:

```powershell
.venv/Scripts/python.exe -m tests.lifecycle_archive --audit-only
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.lifecycle_archive
```

Extracted SQLite files use the same runner/status APIs. Each case's
`selection.json` identifies its saved world/branch IDs, and `evidence.json` names
its authoritative worker files. Baselines, interrupted originals and backups
are separate copies; combine only the listed files for a case. Full manifests
remain available for unknown-slot coverage. The offline preview demonstrates
data availability and exact scoring/footprints; M4 owns the complete analyses
and report. See [fixture reproduction](tests/fixtures/README.md#crash-safe-scripted-lifecycle-run-bundle)
and [M3-T05 evidence](docs/todos/M3/M3-T05-crash-safe-scripted-lifecycle.md#validation-and-evidence).

## Offline exact outcomes and trajectories

[evaluate.py](recovery/evaluate.py) reads the full saved schedule and original
call/attempt/pre-delivery records without importing the runner or model stack.
Recorded invalid/failed replies score zero; unexecuted opportunities remain
unknown. Exact answers preserve list order/multiplicity and every BFS node key.
Coordinate diagnostics use the same peer's valid prefix-round-four candidate
for preservation eligibility, with empty/unknown denominators explicit.
World/family summaries average eligible peers, then worlds, then equal families.
All four rounds remain present for AUC, joint completion, trajectory categories,
regression, fragmentation and six overlapping observable annotations.

```powershell
python -S -m recovery analyze --manifest population.json --schedule schedules.json --worker worker-0.sqlite --worker worker-1.sqlite --stage main --count 60 --output outcomes.json.gz
python -S -m tests.outcome_archive
```

`analyze` exclusively creates a derived JSON (or `.json.gz`) export containing
`outcomes`, `coordinates`, `peer_diagnostics`, `diagnostic_summaries`, `rounds`,
`trajectories`, `annotations`, `annotation_counts` and original `attempts`.
Each outcome retains its world/event/policy/replicate/round/peer and original
generation/replay/prefix joins. Supply each accepted worker once; duplicate
backups are rejected and missing files are never created. Use `--stage development`
for the saved pilot schedule or `--count 40` for the nested main population.
No scoring is fed into execution or stopping decisions.

```python
from recovery.evaluate import evaluate_run, write_evaluation

tables = evaluate_run(worlds, branches, worker_paths)  # Full intended schedule.
write_evaluation("outcomes.json.gz", tables)          # Existing files protected.
```

The [retained table fixture](tests/fixtures/README.md#exact-offline-outcomes-and-trajectories)
reproduces sixteen offline cases from the M3 bundle, including full population
joins and the stopped unknown slots. Scripted outcomes are validation evidence.
Information/work inventories, policy costs and uncertainty/missingness are
described below. The completed [M4 CPU audit](docs/validation/m4-cpu-gate.md)
records the report gate and remaining M5 requirements.

## Offline contrasts and conditional repeats

[analysis.py](recovery/analysis.py) adds every prespecified contrast to the
full offline outcome join. Use the saved complete schedule and original workers:

```powershell
python -S -m recovery analyze --estimands --manifest population.json --schedule schedules.json --worker worker-0.sqlite --worker worker-1.sqlite --stage main --count 60 --output analysis.json.gz
python -S -m tests.estimand_archive
```

The additional `estimands` block contains fixed `populations`, `world_contrasts`,
equal-family `summaries`, separate `repeat_contrasts`/`repeatability`,
`trajectory_changes` and observed/unknown `prose_activity`. θ uses revised minus
sham C−B AUC; φ is `E_keep(revision)` over the same retained peers in rounds 2–4.
Round one remains a construction reference. Receipt comparisons use Prefix/Sort;
Q uses Sort/BFS; preserving edits use the original first eight Top-K/BFS worlds.
All named secondary effects and accuracy/final/preservation companions are included.

Each world row exposes its formula, coefficients, endpoint, eligible peers/rounds,
original prefix/call/generation IDs, exact numerator/denominator and unknown
components. `endpoint=preservation, round=null` is the four-round mean of eligible
peer preservation rates; `round=4` is final preservation. Structural empty
denominators are N/A; unknown prefix eligibility remains unknown. Intended
population estimates require all eligible components. A separately labeled
`complete_case_description` includes its own world/family denominators.

Replicate zero supplies population estimates. The ten fixed repeated worlds retain
their original prefix/partition and new continuation seeds. Repeat tables separate
zero-effect ties, strict sign reversals and changes in complete trajectory categories;
they assess conditional stability and supply no receipt/Q or new-prefix repeatability.
Q activity never selects worlds: inactive and unobserved treatments stay included.
These tables supply the original components/identities used by the uncertainty
and missingness workflow below.

```python
from recovery.analysis import analyze_run
from recovery.evaluate import write_evaluation

tables = analyze_run(worlds, branches, worker_paths)
write_evaluation("analysis.json.gz", tables)  # Exclusive derived export.
```

The [retained contrast tables](tests/fixtures/README.md#prespecified-estimates-and-conditional-repeatability)
reconstruct directly from the original scripted lifecycle workers at both sizes,
including all unknown worlds in the full main manifests. These are CPU validation
artifacts; M4's complete analysis/report gate passes on CPU.

## Offline information and retained work

[information.py](recovery/information.py) adds the §7.2 inventories and CPU
references to the original outcome export:

```powershell
.venv/Scripts/python.exe -m recovery analyze --diagnostics --manifest population.json --schedule schedules.json --worker worker-0.sqlite --worker worker-1.sqlite --stage main --count 60 --output information.json.gz
.venv/Scripts/python.exe -m tests.information_archive
```

Combine `--diagnostics --estimands` to export both. The `information` block
contains all four prefix rounds' old-gold correctness, source coverage and
history/communication measurements; actual rendered owner-v1 exposure; L/B
receipt timing with origins and censoring; C/F initial remote evidence and
unique acquisitions versus repeated delivery attempts; source-bound receipt
annotations, offline correctness strata, transport references and edit descriptors.
The [rubric](docs/implementation-research/information-diagnostics.md) defines
conservative associations and assumptions. Cleared candidates cannot supply
receipt reconstruction. Wrong retained candidates remain literal, and missing
last candidates never inherit an earlier answer.

Committed checkpoints establish final-round acquisitions. Their public decoder
requires the declared CPU dependencies, while the pure functions and missing-worker
exports work with site packages disabled. Reads share the worker's application
snapshot and invoke neither the saver nor the runner. Unobserved final delivery
remains unknown. Existing exports and original worker files stay protected.

For exact history-content token counts, supply `--tokenizer <local-metadata-directory>`
in a tokenizer-enabled environment. It loads only local CPU metadata and requires
exact reproduction of saved input IDs. Without it, nonempty history counts are
unavailable; saved request-token counts remain visible. Content counts sum
independently encoded retained items and exclude layout headers; they are not
marginal prompt cost or GPU time. The [native fixture](tests/fixtures/information_tokens.json)
checks both sizes and all five families.

```python
from recovery.information import information_run
from recovery.evaluate import write_evaluation

tables = information_run(worlds, branches, worker_paths, estimands=True)
write_evaluation("information.json.gz", tables)
```

The [six retained cases](tests/fixtures/README.md#information-inventories-and-retained-work)
include complete fixtures, full unknown main populations and a stopped prefix.
The atlas witnesses establish sufficiency/ambiguity for named CPU views; none
is a model finding, live intervention or source of correctness feedback.

## Offline policy costs and the boundary rule

`recovery analyze --costs` reads the existing call/attempt, allocation and
checkpoint records. Add `--estimands` and/or `--diagnostics` for the other M4
tables in the same read snapshots. `--as-of` supplies an explicit zoned clock
for reproducible accounting bounds on interrupted/open work; it does not filter
the saved records to a historical run. Missing workers remain unknown and
exports exclusively create new JSON/JSON.gz files.

```powershell
python -m recovery analyze --costs --estimands --diagnostics `
  --manifest tests/fixtures/population_target.json `
  --schedule tests/fixtures/schedules_target.json --stage main --count 60 `
  --worker worker-0.sqlite --worker worker-1.sqlite `
  --as-of 2026-10-06T00:00:00+00:00 --output policy-costs.json.gz
```

The [cost implementation](recovery/costs.py) shares M3's original arithmetic
with live status. Physical generations/attempts and allocated device time are
charged once. Each hypothetical continuation includes its original sixteen-call
prefix and all sixteen continuation calls, including F's abandoned prefix and
original measured costs for replay. Unknown scheduled calls make the complete
policy cost unavailable. Measured token/duration subtotals, missing output/memory
measurements, failures and ambiguous attempts remain explicit. Allocation
setup/interruption/attempt/idle partitions reconcile separately; outside overhead
stays experiment overhead and is never added again to each policy. Provider
billing is separate from allocation time.

The frozen rule chooses C exactly when every peer initially holds all current
ID/version pairs, including known tombstones and excluding pending replacements;
otherwise it chooses K. Only recorded first-call input or a committed pre-call
boundary can supply coverage. Later sources, gold, candidates and branch
availability cannot change the choice. Incomplete/unscheduled selected branches
remain unavailable. Whole-branch comparisons with always B/C/K retain common
world/prefix/generation IDs and preservation denominators. Selection tables state
when the rule is constant and retain unknown boundaries in their population.

`retained_evidence`, `quality_preservation`, and measured `policy_costs` are
separate views. Retained remote-record counts exclude the host-injected edited
record; current-manifest completeness still includes it. `strategy_worlds` and `paired_comparisons` supply paired plotting
and uncertainty inputs; shared generation costs cancel before forming duration
differences. Oracle-recognized stable-completion cost is explicitly retrospective:
the fixed schedule still runs all calls. No utility or accuracy-per-message score
is calculated.

```python
from recovery.costs import costs_run
from recovery.evaluate import write_evaluation

tables = costs_run(worlds, branches, worker_paths, now="2026-10-06T00:00:00+00:00")
write_evaluation("policy-costs.json.gz", tables)
```

The [sixteen retained cases](tests/fixtures/README.md#policy-costs-and-frozen-boundary-rule)
reconcile with M3 and preserve full main/stopped unknowns. Pure record analysis
runs without runtime/model dependencies; decoding real committed checkpoints
requires the declared CPU serializer. This is CPU validation, not GPU timing or
empirical policy evidence. The [M4 CPU audit](docs/validation/m4-cpu-gate.md)
passes; actual GPU timing/resource admission remains M5 work.

## Offline uncertainty and missingness

[uncertainty.py](recovery/uncertainty.py) derives paired intervals, frozen-population
sensitivity and completion coverage from the same original worker snapshots.
`--uncertainty` includes estimands and costs; diagnostics remain optional:

```powershell
python -S -m recovery analyze --uncertainty --resampling-seed 20261006 --as-of 2026-10-06T00:00:00+00:00 --manifest population.json --schedule schedules.json --worker worker-0.sqlite --worker worker-1.sqlite --stage main --count 60 --output uncertainty.json.gz
.venv/Scripts/python.exe -m tests.uncertainty_archive
```

Exactly 10,000 world draws within each eligible family use sorted world IDs,
saved nonnegative family seeds, equal-family means and explicit linear type-7 quantiles.
The two pooled primaries use 1.25/98.75 percentiles; family descriptions and
secondaries use 2.5/97.5. Matching family/world cohorts reuse the same draws
across events, policies, endpoints and overlapping displays. Repeats remain
conditional comparisons of the same worlds and never increase independent N.
Within-family constants also receive the specified weighted Hoeffding companion,
with the formula's actual range. Family final-completion counts include exact
two-sided binomial bounds; incomplete-population and complete-case bounds are
separate. Approximate bootstrap coverage is not exact small-sample coverage.

The `uncertainty` block contains `settings`, `populations`, `world_bounds`,
`summaries`, `world_trajectories`, `family_completion`, `trajectory_summaries`,
`policy_world_displays`, `policy_display_summaries` and `reporting_references`.
World contrasts and family means remain in `estimands`. Recorded failures stay
zero; unknown logical uses stay unexecuted even if their recorded originals
constrain sensitivity. Shared response coefficients cancel before extrema.
Small nonlinear completions are enumerated; larger expressions retain shared
variables and conservative labels. Unknown prefix eligibility may leave
preservation undefined. Empty eligible populations are N/A.

Intended-population intervals require the full eligible outcome cohort;
`complete_case_description` never replaces it. Incomplete trajectory categories
and counts remain explicit, with no invented completion time. Policy quality
and its cost axis share a cohort and draws; preservation's `paired_cost` uses
its own eligible worlds. Ambiguous observed durations have percentile envelopes;
unmeasured future policy costs have explicitly unbounded ends. The 0.10 and
normal-approximation power/fallback references are reporting context, not
equivalence margins or achieved-power claims.

```python
from recovery.uncertainty import uncertainty_run
from recovery.evaluate import write_evaluation

tables = uncertainty_run(worlds, branches, worker_paths,
    seed=20261006, now="2026-10-06T00:00:00+00:00")
write_evaluation("uncertainty.json.gz", tables)  # Exclusive derived export.
```

[Retained uncertainty evidence](tests/fixtures/README.md#paired-uncertainty-and-shared-response-missingness)
reconstructs sixteen original-worker scopes, including both complete fixtures,
full main manifests and stopped work. Scripted values validate analysis; they
are not model findings. M4-T06's complete report gate passes on CPU; actual
hardware/capability/resource admission remains M5 work.

## Reproducible offline reports

[report.py](recovery/report.py) assembles seven explicit exhibits from one
read-only snapshot of the supplied authoritative workers. `--report` includes
all outcomes, contrasts, diagnostics, costs and uncertainty without separate
flags. An explicit zoned accounting clock is required; the output directory
must be new. Every current report and figure is labeled **synthetic CPU
validation**, with no model capability or empirical claim.

```powershell
python -m recovery analyze --manifest population.json --schedule schedules.json `
  --worker worker-0.sqlite --worker worker-1.sqlite --stage main --count 60 `
  --report --as-of '2026-10-06T00:00:00+00:00' --resampling-seed 20261006 `
  --output report-new
```

Open `report-new/report.html` locally. It links seven exhibits, exact case cards,
literal call/message traces, all scientific tables (`tables.json.gz`), original
input selection (`inputs.json.gz`), provenance/settings (`report.json`), saved
plotting inputs (`plotting.json`) and world/interval CSVs. Unknown slots and
empty eligible populations remain unavailable; invalid/failed recorded slots
keep their original outcomes. Non-scalar raw text uses reversible JSON string
notation in HTML and remains unchanged in the trace JSON.

Case medians use exact rational effects and immutable world IDs. They require
every scheduled slot in the supplied world scope recorded, including failures,
controls and scheduled repeats; selecting contrasts use replicate zero.
Duplicate worlds merge their reasons, missing signs remain explicit, and
all-zero regression/smallest-ID fallbacks are fixed. Case eligibility never
changes an estimand population. The case/annotation rules, source-association
assumptions, 10,000-draw settings and original generation settings are exported
for the later M5 freeze.

Data export imports no inference, execution or plotting module. Matplotlib is
an optional extra, needed only to render figures. Saved plotting inputs suffice;
rendering reads no workers and performs no analysis resampling.

```powershell
python -m pip install '.[report]'
python -m recovery.figures --report report-new
# Or add --figures to the original analyze --report command.
```

Rendering exclusively creates `figures/` with seven SVG/PNG pairs and a small
plotting-environment record, then links them from the HTML. That record is
separate from the accepted inference freeze. Existing reports/figure directories
are protected. Prefix-policy computation, actual allocation and billing remain
separate; CPU attempt durations do not measure GPU runtime penalties. Paired
policy differences remain in the supporting tables and use their own axes;
the quality/cost figure shows absolute whole-policy endpoints.

[Retained report evidence](tests/fixtures/README.md#reproducible-synthetic-reports)
includes sixteen repeated original-worker scopes and five portable complete,
incomplete and stopped reports with all exhibits. The
[coverage/category audit](docs/validation/m4-cpu-gate.md) records named CPU
evidence and the remaining hardware, capability, host and resource gates.

## Protocol attainability and capacity

[witness.py](recovery/witness.py) is a CPU validation strategy. Each peer forwards
its current private shard to a different peer in rounds 1–3, then solves from
locally acquired records. It uses legal placeholders earlier and receives no
host gold or unseen records. The retained
[witness trace](tests/fixtures/README.md#protocol-attainability-witness) covers
all families/sizes and scheduled siblings/repeats/controls, including L forwarding,
F reacquisition, receipts and mixed/Q replay. Candidate/control/own-shard outputs
fit 384 tokens at both sizes. This establishes attainability, not LLM capability.

The original 8,192-token regime failed with reachable 14,642 target / 14,349
fallback totals. Its [negative archive](tests/fixtures/capacity_report_8192_original.json.gz)
is preserved. The user-authorized remedy renders literal history blocks with
column labels and a footer protecting trailing whitespace. The
[complete proof](docs/implementation-research/m2-t06-capacity-proof.md) audits the
loaded vocabulary, Unicode normalization and full horizon: at most 261,388 tokens
including all 384 output tokens, within 262,144 uniformly. The renewed
[capacity report](tests/fixtures/README.md#complete-capacity-admission)
admits both sizes with 80 adversarial envelopes; observed maxima alone are not
the proof. The scalar-message guard preserves raw invalid replies without effects.
No truncation, answer repair or retention/population change is introduced.

```powershell
python -m unittest tests.attainability_checks -q
python -m tests.tokenizer_attainability --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
python -m tests.tokenizer_capacity --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B"
```

The native commands require the locally downloaded pinned tokenizer metadata
described in [M2-T06](docs/todos/M2/M2-T06-attainability-and-capacity.md#reproduction-environment-and-commands).
All eight capacity checks pass and the command exits **0** for CPU admission;
exit **1** means failed admission and **2** means failed verification. M5 still
must establish worst-context memory/headroom, capability and timing after M3–M4.
No GPU use or accepted freeze is admitted by these CPU results.

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

## M5 inference preparation

The direct [inference adapter](recovery/inference.py) is prepared for CPU review
and a separately authorized T4 smoke test. It uses the existing serial
`ProcessProvider`/`LocalScheduler`, native Qwen text loading, explicit NF4/double
quantization/FP16, fresh KV/recurrent state, saved seeds and strict raw decoding.
Process/attempt diagnostics remain in the existing SQLite worker records.
Candidates and the concrete proposed Kaggle allocation/storage/smoke matrix are
in [M5 preparation evidence](docs/validation/m5-inference-preparation.md).
The candidate environment is not a passing GPU lock or an accepted freeze.

CPU checks, with no weights or GPU calls:

```powershell
.venv/Scripts/python.exe -m unittest tests.test_inference_preparation tests.inference_checks -q
python -m tests.tokenizer_inference --tokenizer LOCAL_9B_METADATA
python -m tests.tokenizer_capacity --tokenizer LOCAL_9B_METADATA
```

`LOCAL_9B_METADATA` is the directory containing the pinned tokenizer/config/template
files. The native commands require the candidate Transformers stack; the mock
checks run in the CPU virtual environment without torch. Candidate settings can
be inspected from those metadata alone:

```python
from recovery.inference import TokenizerFactory, ModelFactory, candidate_settings

tokenizer = TokenizerFactory(local_directory="LOCAL_9B_METADATA")()
settings = candidate_settings(tokenizer)  # Includes the actual template string.
factory = ModelFactory(cuda_visible_devices="0")  # Construction does not load.
# Calling factory() loads weights/CUDA and requires separate authorization.
```

For later authorized execution, pass the model factory to the existing
`ProcessProvider`, or one matching factory/device visibility per `WorkerSpec`.
Use an importable guarded script under spawn. Keep the five existing development
worlds and saved schedule; the first 90 capability slots precede recovery work.
Raw generated IDs stay in `calls.raw_json`; `attempts.backend_json` also retains
the exact generated suffix including transport, and the original process stores
its loading inventory/configuration. Read-only old archives remain usable.
M5-T02 must still pass actual loading, finite-output, worst-context memory,
cache/RNG and host persistence checks within <=24 attempts/0.5 aggregate GPU-hour.

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
renders them as one user turn with structural JSON and labeled literal history.
The host projects an ordinary
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
262,144. Oversized requests fail without truncation. `dataclasses.asdict`/ordinary
JSON can save the request and token record in the later call ledger.
The [seven retained short request/token fixtures](tests/fixtures/README.md#permitted-peer-requests-and-tokenizer-inputs)
and [native tokenizer harness](tests/tokenizer_peer_views.py) verify literal archive
preservation and exact native inputs. M2-T01's original 79-check CPU suite and
five native-tokenizer checks passed; the current 167 CPU/37 native checks include
renewed protocol, round, event, replay, witness and complete CPU capacity evidence.
Native NFC is recorded separately from exact rendered text; the host preserves
archived strings. Hardware admission remains M5.
