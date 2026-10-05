# M3-T03 — Local worker scheduling and cross-worker replay

**Status:** done

**Dependencies:** [M3-T02](../M3/M3-T02-bounded-attempts-and-failures.md#completion-and-handoff).
M2 passed and M3-T02 completed on 5 October 2026. Use its bounded
`ProcessProvider` and exclusive worker-local ledger/checkpoints; preserve known
timeouts, the single identical retry and observed/uncertain process work.

## References

- [Repository contract](../../../AGENTS.md), [plan worker ownership](../../IMPLEMENTATION_PLAN.md#round-execution-persistence-and-worker-ownership), and [M3](../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Specification [§8.1](../../../PROJECT_SPECIFICATION.md#81-model-and-capability-controls), [§8.4](../../../PROJECT_SPECIFICATION.md#84-resource-gate-and-freeze), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [fresh-call/RNG ownership](../../implementation-research/inference-and-capacity.md#rendering-termination-and-call-independence).

## Intended outcome

A small local scheduler executes balanced blocks across isolated serial workers and resolves exact replay dependencies regardless of worker placement.

## Scope and boundaries

- One process and database per worker, serial calls within each worker; M5 attaches one full model replica to each T4. Validate now with CPU scripted workers.
- Schedule balanced task/world blocks and rotate eligible sibling order/device assignment while respecting prefix and B/C first-round parent dependencies.
- Make immutable prefix/reply records available to an assigned worker with original physical generation IDs. A copied/accessed parent remains the same physical generation, not a new charge or fresh result.
- Preserve independent branch state, cursors and queues across workers. Set intended device visibility before CUDA initialization in the future backend; process-global RNG must not race across threads.
- Use existing IDs, saved seeds, records and local process coordination. No distributed queue, shared writable peer state, fixed-affinity requirement or transfer service is warranted.
- Resume from existing manifests/checkpoints, retaining which work is dependency-waiting or runnable. Never select work by correctness or drop silence/early-success branches.

## Completion criteria

- Cross-worker prefix and mixed/Q parent access preserves original identities, exact raw replies and branch-local effects.
- Worker/order changes do not change seed assignment, logical schedule, scripted results or replay parents.
- A missing/inconsistent dependency stops clearly instead of silently regenerating it.
- A worker restart can resume assigned work without a new configuration or duplicate logical slot.

## Validation and evidence

Run two local CPU worker processes with intentionally uneven delays and order reversal. Move a mixed/Q continuation to the other worker, including invalid parent replies and held prose. Check parent identity/cost references, immutable snapshots, independent queues, saved seeds and equal committed scripted outcomes. Deliberately remove/mis-scope a parent and verify rejection. Test scheduler recovery from one interrupted worker.

### Implemented scheduling and record ownership

[workers.py](../../../recovery/workers.py) supplies `LocalScheduler`,
`WorkerSpec` and a read-only scheduling status view. `from_manifests` loads the
existing population/schedule formats without resampling. Balanced index blocks
contain one world per family; prefix/control opportunities precede recovery
within each block. The five development worlds retain their complete 90-call
capability prelude. Eligible sibling order and available-worker assignment
rotate; all seeds, logical calls, replicates and replay parents remain those
saved by M1. Correctness is never an admission or stopping input.

Each worker has one serial controller owning its SQLite file and the existing
bounded `ProcessProvider` generation process. Only that generation process will
load a full replica in M5. Factories are importable and spawn compatible; loaded
models/tokenizers/CUDA state are not passed between processes. Intended
`CUDA_VISIBLE_DEVICES` is inherited at spawn before interpreter imports and
set before either worker factory runs. CPU fixtures verify independent process
RNGs reset from each saved call seed; native CPU/CUDA seeding and fresh model
KV/recurrent state remain M5 adapter checks.

[runner.py](../../../recovery/runner.py)'s `WorkerReader` accesses original
ledgers/checkpoints with SQLite `mode=ro` and `query_only=ON`. The public pinned
saver read path works without writes and excludes synthesized pending node
effects. Every sibling deep-deserializes the original drained prefix. B/C
parents supply exact saved pre-delivery replies, including Unicode-invalid
outputs and recorded failures; their post-delivery recipient state is never
imported. Replay rows reference the original `generation_id`/`replay_parent`;
parent raw calls and attempts remain solely in their original file. Access
adds no physical attempt or charge. Independent branch checkpoints own all
queues, cursors, delivery IDs and effects.

[storage.py](../../../recovery/storage.py) binds each worker to the literal
saved worlds/branches, settings and attempt bounds before admission. This one
row in the existing file rejects restart drift; order/device placement are
operational choices. Ownership and completed rounds reconstruct from existing
inputs/checkpoints, with runnable, dependency-waiting, active and done work.
There is no scheduler progress database, reply copy, transfer service or new ID
scheme. Full-information controls now use the same raw-call/attempt ledger,
whole-world candidate shape and empty-send validation, without peer delivery
threads. Completed controls resume from their exact valid/invalid/failure record.

An OS lock on a one-byte `.owner` sidecar enforces exclusive file ownership,
including idle workers that have no provider PID yet. It stores no status or
scientific data and releases on owner death. A restart requires the previous
controller and registered generation process to have exited before the same
file reopens. Raw outcomes/checkpoints always win over lost acknowledgements;
uncertain unpersisted work permits only T02's identical single retry. Bounds
remain 120 seconds per attempt and one second each for terminate/kill, with a
one-second heartbeat by default. Process records also retain intended device
visibility for later allocation attribution; CPU labels are not CUDA evidence.

### Executed verification, 5 October 2026

The [14 focused checks](../../../tests/worker_checks.py) pass, including:

- Two actual worker controllers with separate resident CPU generation processes,
  uneven 0.006/0.001-second scripted delays, reversed peer/sibling order and
  rotated placement. Exact requests, saved seeds/RNG probes, raw results and
  committed outcomes match. Child module paths match the parent source or
  installed package, and intended visibility stays process local.
- Cross-worker original-prefix access and both mixed/Q parents, including
  invalid Unicode and failed replies. Parent snapshots stay unchanged; branch
  source/prose effects, queues and delivery IDs remain independent. Logical
  replays have no attempts and resolve original measured parent attempts.
- Missing/event/seed/validation defects stop before inference or effects.
  Deleting an already committed parent rejects scheduler reopen without new
  generations. A second controller cannot open even an idle owned worker file.
- A real Q worker terminated while first-round prose remains held resumes its
  exact checkpoint. The first interrupted attempt retains uncertainty and an
  unknown finish time; its one identical retry completes. Final states match
  uninterrupted execution with no duplicated delivery. A kill after committed
  effects but before acknowledgement creates no extra physical attempt.
- Both sizes/all families have durable full-information control shapes and
  empty sends; drift rejects reuse. Five fallback-family prefixes/controls
  execute all 90 prelude calls before recovery, then finish 170 fixed calls,
  including invalid/failed slots. Both complete main schedules and the 1,114
  distinct development slots retain their existing counts/seeds without runs.

The [retained archive](../../../tests/fixtures/worker_scheduling_traces.json.gz),
derived by [worker_archive.py](../../../tests/worker_archive.py), records eight
separate CPU validation scenarios: **666 logical calls, 618 distinct generations,
619 attempts, 48 exact replay uses, 17 process intervals and one uncertain
completion**. These are validation scenario totals, not experimental coverage.
It preserves requests, raw replies, original identity/cost joins, committed
states/queues, actual process/attempt clocks and the held-prose interruption.
The original archive used the 13-check precursor; the final 14-check code,
including exclusive idle ownership, reproduces its scientific records exactly.

The first reproduction exposed an export-comparison defect: in-memory tuple
fields were compared directly with parsed JSON arrays. Canonical JSON
normalization fixes that comparison without dropping any request, reply, seed,
parent, outcome or state field. A fresh hash-seed-37 reproduction passes;
placement/clocks/PIDs remain measured fields and are not asserted identical.

| Executed check | Result |
|---|---|
| `.venv/Scripts/python.exe -m recovery validate` (final source) | 221 passed: prior 207 plus 14 worker checks |
| Actual installed-library harness, including spawned/Popen children | 221 passed; runner/attempt/storage/worker paths and generation-child imports asserted |
| `python -S -m recovery validate --core-only` | 81 passed with site packages disabled |
| `.venv/Scripts/python.exe -m tests.worker_archive`, hash seed 37 | 14 checks and exact canonical archive comparison passed |
| CPU and native durable archive reproduction, hash seed 37 | Both unchanged: 60 branches, 240 rounds, 960 logical calls, 864 attempts and 96 parent reuses each |
| `pip check`, compilation and `git diff --check` | Passed |
| Documentation/status/protected-file audit | 216 relative links/anchors across six documents and all 29 task/index statuses pass; specification/configuration/research/vendor and every prior fixture have empty diffs |

Final source/installed validation took 367.658 / 367.106 seconds; final focused
archive reproduction took 90.361 seconds. Independent checks ran concurrently;
these are CPU validation durations, not inference forecasts. PowerShell log
redirections explicitly propagate `exit $LASTEXITCODE`.

Environment: Windows, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5,
LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and core 1.6.6. Native
durable reproduction uses host Transformers 5.12.0 / tokenizers 0.22.2 and the
same pinned local 9B tokenizer metadata; no model weights are loaded.

The installed harness is `$env:TEMP/m3-t03-installed-validation.py`. It imports
and asserts installed package paths before adding checkout tests, then preserves
installed precedence in child imports. Logs are
`m3-t03-{source-final,installed,core}-validation.log`,
`m3-t03-worker-{archive,reproduction-final}.log` and
`m3-t03-{durable,native}-reproduction.log` in the host temporary directory.
Ordinary archive reproduction is read-only; `--write-fixture` exclusively
creates a new file. See [fixture commands](../../../tests/fixtures/README.md#local-worker-scheduling-traces).
The documentation audit is `m3-t03-documentation-audit.py` with its matching
`.log` in the same temporary directory; it compares protected files to task-start
commit `9774325` and reconciles all task/index statuses.

### Completion and handoff

M3-T03 is implemented and verified on CPU. [M3-T04](M3-T04-accounting-progress-and-budget.md)
is ready: it owns physical/policy allocation attribution, terminal/status output
and budget admission/stops. M3-T05 retains the combined lifecycle gate; M3
remains open. M5 must attach and verify the accepted full model replicas,
seeding/state, timeout adequacy, device placement, memory and capability.

Specification/configuration, research/vendor and all prior evidence archives
remain unchanged. No scientific/frozen-configuration change, GPU allocation,
model inference, pilot, main experiment or publication occurred.

