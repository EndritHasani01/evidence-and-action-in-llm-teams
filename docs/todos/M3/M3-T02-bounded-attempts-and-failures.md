# M3-T02 — Bounded attempts, timeouts and interruption semantics

**Status:** done

**Dependencies:** [M3-T01](../M3/M3-T01-durable-round-runner.md#completion-and-handoff).
The M2 gate passed and M3-T01 completed on 5 October 2026. This task extends
its exact application ledger and replacement checkpoints with bounded process
execution and explicit recovery of interrupted attempts.

## References

- [Repository contract](../../../AGENTS.md) and [plan M3](../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Specification [§3.2](../../../PROJECT_SPECIFICATION.md#32-synchronous-rounds-and-replies), [§6 failure/missingness](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [remaining process-failure validation](../../implementation-research/state-and-replay.md#remaining-implementation-validation-not-further-framework-research).

## Intended outcome

Every scheduled attempt terminates or resumes under the declared bounds, preserving failures, unknown work and ambiguous crash costs without resampling completed outcomes.

## Scope and boundaries

- Persist attempt start before generation and raw output/failure before effects. Start development with a 120-second per-attempt timeout.
- Allow at most one identical-request retry only after an infrastructure interruption without a durable response. No retries for incorrect answers, invalid formatting, truncation or completed timeouts.
- If inference may have completed before response persistence, record an uncertain completion/physical attempt; do not claim exactly-once generation.
- A hung attempt must be terminable, its known timeout durable, and status remain responsive. Restarted workers reload their state/model; lost work, load and allocated idle time remain chargeable.
- A context overflow fails visibly before generation and stops for capacity/protocol diagnosis. Do not shorten history, turn the defect into a favorable exclusion, or carry an older candidate into the failed slot.
- Keep unknown/unexecuted opportunities distinct from zero-credit recorded failures. Continue fixed opportunities after ordinary invalid replies.

## Completion criteria

- Attempt/failure state transitions survive worker interruption without admitting more than two allowed infrastructure attempts.
- Durable invalid replies/timeouts are final records for their call ID and resume without generation.
- Timeout and interruption produce distinct justified records; hung-process termination does not stall the controller indefinitely.
- Failure records retain identity, request, timing, termination and known/uncertain work needed for later accounting.

## Validation and evidence

Use CPU subprocesses simulating slow, hung, interrupted and completed calls. Kill before/after raw persistence; assert retry eligibility, identical retry request/settings/seed, no formatting/timeout resampling and no prior-candidate fallback. Trigger pre-generation overflow. Verify a durable result wins on resume and ambiguous work stays charged. Test ordinary continued scheduled opportunities after failures.

### Implemented boundary and persistence

[attempts.py](../../../recovery/attempts.py) supplies `ProcessProvider(factory)`.
An importable, spawn-compatible factory loads one resident provider in a child
process; a restarted process reloads it. The factory is required to avoid passing
a loaded model or CUDA state between processes. Generation receives only the
permitted view, exact rendered/native request, saved seed and settings. M5 must
implement and verify the independent-call model adapter; weights may remain
resident, conversation/KV/recurrent state may not cross calls.

The default attempt bound is **120 seconds**, including loading and transport.
Terminate and kill each have a **one-second** grace. Pipe I/O runs in a small
thread so a blocked transfer cannot prevent the controller from enforcing the
deadline. Durable heartbeats default to one second. An unconfirmed termination
stops with `UnresolvedAttempt` and admits no retry. A child watches its owner's
actual process sentinel and exits if that owner dies, including during loading
or a hung generation. See [Python's process semantics](https://docs.python.org/3.11/library/multiprocessing.html#process-objects).

[runner.py](../../../recovery/runner.py) requires this boundary for inference.
`scripted=True` explicitly permits the existing deterministic CPU fixtures to
exercise pure graph/ledger exceptions directly. It is not an inference path.
One owner serially owns each worker file; the preceding owner must be stopped
before reopening it. There is no scheduler, shared writer or new identity scheme.

[storage.py](../../../recovery/storage.py) uses the existing `(call_id, number)`
attempt keys. Only an established infrastructure interruption without a durable
outcome changes a running call to retry-pending. The retry uses the same saved
request/settings/seed and attempt bounds. A second interruption atomically saves
an exhausted infrastructure failure; a third attempt is prohibited. Recorded
invalid, truncated, wrong, timeout and exhausted outcomes remain final. Generic
adapter/protocol defects stop as blocked attempts with unknown outcomes and do
not authorize a retry or fabricate zero-credit model errors. Possible completion
before an adapter error is flagged uncertain too; its known elapsed work remains
charged without making the blocked call retryable.

The timeout decision is durable **before** terminating the child. Confirmed
termination then records its complete measured duration. Owner death between
those steps leaves the known timeout final and termination overhead uncertain.
The raw/failure ledger still precedes validation and committed delivery; no
previous candidate enters a failed slot. Ordinary failures preserve the remaining
fixed opportunities. Context overflow stops in the existing untruncated renderer
before a process, physical attempt or delivery is admitted.

Attempt rows retain bounds, observed work, PID, termination reason and recovery
time. An unobserved crash end has **no invented finish time or exact duration**;
its measured heartbeat work and uncertain-completion flag survive. One
`provider_processes` table, keyed by the starting attempt, retains loading,
resident idle and stop/uncertain-stop intervals for later M3-T04 accounting.
These process records are necessary because attempt durations alone omit idle
time and interrupted loading. They contain no peer state or delivery effects.
T01 databases acquire these columns/table without replacing calls or checkpoints.

### Executed verification, 5 October 2026

The [22 focused checks](../../../tests/attempt_checks.py) pass. They include:

- Hung generation and loading, responsive independent SQLite status reads,
  bounded terminate/kill failure and continued fixed opportunities with no
  previous-candidate fallback.
- A backend exit after possible completion, exact request/settings/seed retry,
  two interrupted attempts exhausted without a third, and explicit
  infrastructure interruption distinct from a known timeout.
- Durable malformed/truncated/wrong replies and known timeouts reused without
  generation; pre-generation overflow preserves unknown work and literal state.
- A [real CPU controller subprocess](../../../tests/attempt_worker.py) killed
  before raw persistence, after durable invalid output, during loading and
  during timeout termination. Its inference child dies with it. Reopen restores
  exact outputs/effects, reloads the provider where necessary and preserves
  uncertain work; two killed owners never produce a third attempt.
- Actual WAL/FULL transactions, unlocked inference, durable attempt starts,
  T01 schema reopening, measured versus unknown times and process idle/loading
  records. Provider defects remain stopped and unexecuted peers remain unknown.

The [failure archive](../../../tests/fixtures/attempt_failure_traces.json.gz),
derived by [attempt_archive.py](../../../tests/attempt_archive.py), retains
**12 cases, 78 attempts, 28 process intervals, nine uncertain completions and
four unknown attempt end times**. Five confirmed hung timeouts exceeded their
CPU deadlines by **0.015–0.031 seconds** in this retained run. These are Windows
CPU termination measurements, not GPU inference timings or adequacy of the
120-second model timeout. Fresh hash-seed-37 execution reproduces exact call
outcomes, attempt statuses and committed states; clocks/PIDs are measurements
and are not asserted byte-identical.

| Executed check | Result |
|---|---|
| `.venv/Scripts/python.exe -m unittest tests.attempt_checks -v` | 22 passed |
| `.venv/Scripts/python.exe -m recovery validate` | 207 passed: original 185 plus 22 attempt checks |
| Actual installed-library harness, including spawned/Popen children | 207 passed; installed runner/attempt module paths and child imports asserted |
| `python -S -m recovery validate --core-only` | 81 passed with site packages disabled |
| `python -m tests.attempt_archive` with hash seed 37 | 22 checks and exact archive comparison passed |
| CPU and native durable archive reproduction, hash seed 37 | Both passed unchanged: 60 branches, 240 rounds, 960 logical calls, 864 physical attempts and 96 exact parent reuses each |
| `pip check` and compilation | Passed |
| Documentation/count/protected-artifact audit | 210 relative links/anchors across six changed documents and all 29 task/index statuses pass; specification/configuration/research/vendor and all prior fixtures have empty diffs |

Final source/installed full validation took 431.769 / 380.777 seconds; focused verification took 80.976
seconds and the retained archive's check run took 72.538 seconds. Independent
CPU checks were run concurrently; these are validation durations. Redirected
PowerShell commands explicitly propagate `exit $LASTEXITCODE`, since unittest
writes successful progress to stderr as well as failures.

The installed harness is `$env:TEMP/m3-t02-installed-validation.py`; it asserts
the installed runner/attempt module paths, then keeps site-packages ahead of
checkout tests in spawned child imports. Logs are
`m3-t02-{source,source-final,installed,installed-final,core}-validation.log`,
`m3-t02-attempt-{archive,reproduction}.log` and
`m3-t02-{durable,native}-reproduction.log` in the host temporary directory.
The documentation/count/protected-file audit is `m3-t02-documentation-audit.py`
in that same directory. Final regressions include the corrected uncertainty
flag for blocked adapter failures; its two direct checks also passed separately.
Ordinary fixture reproduction is read-only; `--write-fixture` exclusively creates
a new archive. See [fixture commands](../../../tests/fixtures/README.md#bounded-attempt-and-process-failure-traces).

Environment: Windows, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5,
LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and core 1.6.6.
Native reproduction uses host Transformers 5.12.0 / tokenizers 0.22.2 and the
same local pinned 9B metadata used by M3-T01. No model weights were loaded.

### Completion and handoff

M3-T02 is implemented and verified on CPU. [M3-T03](M3-T03-local-worker-scheduling.md)
is ready and owns scheduling, controls and cross-worker parents. M3-T04 owns resource attribution/status and
M3-T05 the combined killed-process gate after those integrations. M3 remains
open, and M5 must verify the boundary and timeout in its accepted GPU environment.
No scientific/frozen-configuration change, GPU allocation, model inference,
pilot, main experiment or publication occurred.

