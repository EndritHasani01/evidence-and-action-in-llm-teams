# M3-T04 — Resource accounting, progress and safe budget stops

**Status:** done

**Dependencies:** [M3-T03](M3-T03-local-worker-scheduling.md#completion-and-handoff).
M2 passed and M3-T03 completed on 5 October 2026. Use its original physical
parent references, exclusive worker files, durable controls, process visibility
and manifest/checkpoint-derived scheduling status; preserve T02's measured and
uncertain work when adding resource attribution and budget admission.

## References

- [Repository contract](../../../AGENTS.md) and [plan M3](../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Specification [§6](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), [§7.3](../../../PROJECT_SPECIFICATION.md#73-quality-retained-work-and-cost), and [§8.3–8.4](../../../PROJECT_SPECIFICATION.md#83-exact-main-schedule).
- Specification [§9 accounting/status/acceptance](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).

## Intended outcome

Manifest-derived progress and reconciled physical/policy accounting show remaining work, failures, dependencies and allocation, and stop new work safely before the ceiling.

## Scope and boundaries

- Join every logical slot to its generation/replay parent and every generation to attempts. Charge physical attempts once; policy accounting includes the shared prefix and all sixteen continuation calls, original measured replay costs and F's abandoned prefix.
- Record request/output tokens, validated source/text deliveries, durations, memory, device allocation intervals, setup/idle/interruption overhead and uncertain lost work. Make overhead attribution explicit and nonduplicative; provider billing is distinct from aggregate physical allocation.
- Provide terminal progress and a read-only status operation at call/round transitions with a bounded heartbeat during long calls.
- Show stage/family/world/branch/replicate/round/peer/device, elapsed attempt time, last checkpoint, scheduled/finished/remaining logical slots and distinct generations, replay uses, attempts/retries, failures and unknowns.
- Show completed worlds and matched comparison groups by family/event/subset, ready/dependency-waiting branches, current gate/stop reason and resumable work.
- Report allocated GPU-hours including idle devices, reserves and remaining ceiling, plus conservative measured remaining-cost/elapsed-time ranges by phase/condition/device. Mark estimates unavailable before measurements; slot percentage is not runtime percentage.
- Admission checks include active devices, timeout/termination allowance, overhead and remaining forecast. Stop safely before the frozen ceiling without deleting scheduled work. Store only necessary allocation transitions beyond existing records; no progress database.

## Completion criteria

- Progress reconstructs entirely from manifests/ledgers/checkpoints after restart, counting completed invalid outcomes as finished work without calling them successes.
- Physical and hypothetical policy totals reconcile for replayed, failed and retried calls.
- Synthetic allocation exhaustion halts admission/terminates safely and retains explicit unknown slots and resumable state.
- CLI/status operations are read-only and responsive while workers are active.

## Validation and evidence

Use hand-calculated schedules with shared prefixes, mixed/Q replay, F, timeouts, ambiguous attempts, idle devices and setup. Verify no double overhead or physical replay charge. Test cost-range unavailability before measurements, later slower-device forecasts, heartbeat behavior, backup/restart reconstruction and budget exhaustion at an adverse timeout boundary.

The [23 focused CPU checks](../../../tests/accounting_checks.py) pass, with nine
cases retained in [accounting_progress_traces.json.gz](../../../tests/fixtures/accounting_progress_traces.json.gz).
The final source and installed suites each pass **244 checks**. These are
scripted validation cases, not experimental coverage or GPU measurements.

### Implementation approach

Use existing call/attempt keys, saved barriers and committed checkpoints as
the accounting and progress authority. Allocation start/confirmed-release
intervals stay in worker files. Existing calls record input-token counts for
responsive reads, verified against exact barriers; attempts optionally record
measured peak memory. There is no progress database. Count invalid durable replies as finished,
and retain unexecuted and ambiguous work separately. Policy costs include the
original prefix and all continuation uses, resolving physical parents across
workers. Loading within an attempt is already part of its measured cost;
allocation overhead is partitioned separately without adding it twice.

Read-only status and terminal transition/heartbeat reports must work with live
workers and reopened backups. Budget admission uses the complete remaining
forecast when available, active allocation, reserves and bounded termination;
an allocation deadline also protects long calls. CPU fixtures use explicit
synthetic allocation/release acknowledgements. Actual provider release and GPU
measurements remain M5 integration, with unconfirmed release left chargeable.

### Implemented attribution and status

[accounting.py](../../../recovery/accounting.py) joins every manifest slot to
its original generation and attempts. Replays add logical uses, without new
physical attempts. Each policy includes the original 16-call prefix and all
16 continuation calls, including F and measured costs of invalid/failed/retried
parents. Partial costs retain unknown calls, output tokens and durations.
Observed crash work supplies a lower bound; confirmed recovery supplies its
upper bound without inventing an attempt finish time.

Allocation is independently partitioned into setup, interruption, attempt,
potential unobserved work and idle time, including devices without a model.
Loading within an attempt is already included in that attempt's measured cost;
the allocation partition is never added to it. Outside overhead remains
experiment overhead rather than being assigned again to each call. Provider
reservation start and billing are separate inputs from model/process lifetime.
Release requires acknowledgement; unconfirmed allocations remain open.

`recovery status` and `LocalScheduler.progress()` reconstruct counts, exact
resumable slots, current peer/device/attempt elapsed time, durable checkpoints,
balanced dependencies and complete matched groups from read-only records.
`report=terminal_progress` supplies call/round transitions and bounded live
heartbeats. No correctness, gold or missing-slot imputation enters these views.
See [operator commands and API](../../../README.md#resource-accounting-and-read-only-status).

Budget admission includes all active devices, remaining reserves, external
overhead, complete measured main forecasts and every still-possible attempt's
timeout/termination in the next round. An independent deadline stops long calls.
Forecasts pool measured families within phase/condition, require every device,
retain observed prompt ranges and use the slower maximum plus 25%; the allocated
upper also charges idle devices during serialized dependencies. Unmeasured
cells are unavailable. Prior configurations remain charged, while only identical
saved generation settings supply forecast samples. Existing saved configuration
and call IDs distinguish prior configurations without another identity system.

### Hand reconciliation

The Sort fixture has one shared prefix and revised B/C/F/P_G/Q_B/Q_C. It assigns
two recorded synthetic seconds to each original call and three to the lost
attempt, enabling independent hand arithmetic; these are not measured CPU or
GPU inference times.

| Quantity | Independent expected and observed |
|---|---:|
| Logical slots / distinct generations / exact replays | 112 / 100 / 12 |
| Physical attempts / infrastructure retries | 101 / 1 |
| Recorded synthetic physical attempt seconds | 203 |
| Policy seconds: B / C / F / P_G / Q_B / Q_C | 67 / 64 / 64 / 67 / 67 / 64 |
| Calls per continuation policy including prefix | 32 |
| Two synthetic allocations of 200 seconds each | 400 seconds |
| Setup / interruption / attempt / idle allocation seconds | 2 / 3 / 198 / 197 |
| Ambiguous three-second attempt with one second observed | Physical attempt range [201, 203]; finish remains absent |

Request tokens reconcile to the exact persisted inputs for every physical
attempt, including the retry. Replay policy costs reuse those original tokens
and costs. Committed prefix deliveries are deduplicated by their existing IDs;
branch-local source/text deliveries remain distinct. Invalid/failed outcomes
count as finished and are never called successes. Both complete main counts
(16,152/17,656 and 11,504/12,560 distinct/logical) and the 1,114/1,178 development
counts reconstruct without running their calls.

### Executed verification, 5 October 2026

| Executed check | Result |
|---|---|
| Final source `.venv/Scripts/python.exe -m recovery validate` | 244 passed in 548.821 seconds |
| Installed-library harness from host temporary directory | 244 passed in 551.166 seconds; all five implementation module paths/bytes asserted, spawned worker imports checked |
| `python -S -m recovery validate --core-only` | 81 passed with site packages disabled |
| `tests.accounting_archive` creation / fresh hash-seed-37 reproduction | 23 passed; nine retained cases reproduce their joins/counts/hand costs/deliveries/stop outcomes |
| Final `tests.worker_archive` / `tests.attempt_archive`, hash seed 37 | 14 / 22 passed; every retained scientific field reproduces |
| CPU / native `tests.durable_archive`, hash seed 37 | Both unchanged: 60 branches, 240 rounds, 960 logical calls, 864 attempts, 96 parent reuses and two resumed deliveries |
| `pip check`, compilation, documentation/status/protected-file audit and `git diff --check` | Passed; scientific specification/configuration and all prior fixtures unchanged |

The actual live CLI and API reads remain responsive during CPU generation.
The retained heartbeat case has 28 reports and a maximum 0.141-second gap;
these are CPU observations, not a GPU timing forecast. Reopened SQLite backups
reconstruct identical progress, policy/physical costs and committed deliveries.
Legacy token-count migration uses SQLite JSON array lengths; normal status
queries never read archived request token arrays.

The first full regression exposed the pinned saver's initial public read:
`executescript` commits an existing transaction even when its tables already
exist. Priming that read before the status transaction prevents inconsistent
call/current/checkpoint views. A deterministic concurrent-completion check and
the final suites pass. Separate worker files have no global SQLite snapshot;
a newly committed replay parent permits at most two fresh read attempts, with
no generation, delivery or physical retry. An actual cross-worker commit check
passes; genuinely missing parents still fail. Earlier archive comparators omit
only the new derived input-token scalar and absent memory field, preserving
every original scientific field; exact-input resource checks verify the additions.

Safe-stop evidence includes four final timeouts with no retries and twelve
unknown slots, a hard deadline retaining sixteen unknown slots and one uncertain
attempt, and exact resume to sixteen finished slots with seventeen attempts and
one permitted retry. Unconfirmed release remains chargeable. Reservations
starting before worker setup and failed configurations retain their allocation;
the latter do not contaminate accepted timing samples. The two-device forecast
uses measured 2/8-second synthetic samples and gives [2, 20] allocated seconds
for the remaining call, with a [1, 10] elapsed range before external overhead.

Environment: Windows, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5,
LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and core 1.6.6. Native
durable reproduction uses the existing host Transformers/tokenizers and pinned
local 9B metadata, with no weights loaded. These CPU dependency pins are not
the M5 freeze. Independent checks ran concurrently; validation times are not
model timings. Local installation used normal build isolation after the
no-isolation build reported missing `bdist_wheel`; runtime dependencies did not
change.

Logs and harnesses are in `$env:TEMP`: `m3-t04-source-final-validation.log`,
`m3-t04-installed-validation.{py,log}`, `m3-t04-core-validation.log`,
`m3-t04-accounting-{final-archive,reproduction}.log`,
`m3-t04-{worker,attempt}-final-reproduction.log`,
`m3-t04-{durable,native}-reproduction.log` and
`m3-t04-documentation-audit.{py,log}`. PowerShell commands propagate the actual
exit code. The retained archive and [reproduction commands](../../../tests/fixtures/README.md#resource-accounting-and-progress-traces)
are the durable evidence; temporary logs supply command details.

### Completion and handoff

M3-T04 is implemented and verified on CPU. [M3-T05](M3-T05-crash-safe-scripted-lifecycle.md)
is ready to close the combined lifecycle gate using these accounting/status
joins and allocation stops. M3 remains open. M5 must verify actual provider
reservation/release bounds, GPU allocation/memory/timing, forecast adequacy and
the accepted model/environment before authorized inference.

Progress is thirteen done, one ready and fifteen blocked. No scientific or
frozen-configuration change, actual GPU allocation, model inference, pilot,
main experiment or publication occurred.

