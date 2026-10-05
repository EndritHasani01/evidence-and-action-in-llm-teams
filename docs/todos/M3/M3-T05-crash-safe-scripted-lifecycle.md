# M3-T05 — Crash-safe scripted lifecycle acceptance

**Status:** done

**Dependencies:** [M3-T04](../M3/M3-T04-accounting-progress-and-budget.md). The M2 gate must have passed.
M2 passed and M3-T04 completed on 5 October 2026. Use its
[CPU evidence](M3-T04-accounting-progress-and-budget.md#validation-and-evidence),
manifest-derived status, exact physical/policy joins, allocation intervals and
confirmed-release budget stops. Keep recorded failures, unexecuted slots and
uncertain interrupted work distinct when integrating the killed-process suite.

## References

- [Repository contract](../../../AGENTS.md) and [plan M3 acceptance](../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Specification [§4.2](../../../PROJECT_SPECIFICATION.md#42-complementary-groups-recovery-is-a-team-intervention), [§4.4](../../../PROJECT_SPECIFICATION.md#44-early-prose-availability-with-current-sources-fixed), and [§9 checks](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [limits of the toy probe](../../implementation-research/state-and-replay.md#remaining-implementation-validation-not-further-framework-research).

## Intended outcome

The integrated durable runner produces an auditable CPU run bundle and survives real process crashes across the critical persistence/delivery boundaries.

## Scope and boundaries

- Exercise every family, event/intervention, control and repeat path in a tiny scripted fixture. Full main/pilot manifests must reconcile, without executing every possible scripted slot or making any model call.
- Kill a real subprocess before response commit, after durable reply, during validation/staging and before/after delivery checkpoint. Cover a cross-worker replay parent and Q with held prose.
- Compare uninterrupted and resumed authoritative states, delivery records and derived outcomes. Only documented physical attempts/allocation may differ due to interruption.
- Include invalid parent responses, known timeouts, uncertain pre-persistence inference, exhausted infrastructure retries, cleared fields and persistent notices.
- Validate supported backup/close/reopen and progress reconstruction. Archive evidence in the ordinary run bundle, not a separate persistence or test-management system.

## Completion criteria

- Completed outputs remain unchanged; no completed invalid/timeout result is resampled; infrastructure attempts remain bounded.
- No duplicated delivery, restored cleared field, repeated boundary application, premature/lost held prose or mutation of parent/sibling snapshots occurs.
- Exact mixed/Q equality/reuse and branch-local effects survive restart and worker relocation.
- All schedule/cost/progress joins reconcile, including synthetic budget exhaustion with explicit unknown slots.
- The CPU fixture contains the fields needed for M4 outcomes, diagnostics, costs and report reproduction.
- Close M3 only after all M3 evidence passes and is linked from the plan. M4 remains mandatory before GPU use.

## Validation and evidence

Record the actual killed-process commands, crash boundaries, SQLite/durability settings, environments, fixture IDs, comparison outputs and reopened backup paths. A raised exception or the historical nine-check toy is insufficient evidence. Fix discovered defects in their owning implementation, rerun the affected checks, and preserve the accepted integrated fixture for offline analysis.

Work started on 5 October 2026 from clean commit `70ac24d`, after inspecting M2
and M3-T01–T04 evidence and retained fixtures. The accepted
[ordinary CPU run bundle](../../../tests/fixtures/scripted_lifecycle_run.zip)
was committed at `528c224`. It contains the existing population/schedule formats,
application raw-call/attempt ledger and replacement LangGraph checkpoints;
SQLite backup packages the databases, including committed WAL. No persistence
layer, dependency or scientific/configuration change is added.

### Implementation and retained coverage

[Nine lifecycle checks](../../../tests/lifecycle_checks.py) exercise the actual
durable runner and scheduler. The [test controller](../../../tests/lifecycle_worker.py)
pauses at the real response transaction, validation/staging or public saver
boundary; the test parent kills that process externally. Instrumentation stays
inside the test controller. Production code has no crash hooks.
[Fixture helpers](../../../tests/lifecycle_fixture.py) derive records, progress
and a minimal offline correctness/D/U preview from saved inputs and databases.
The [archive entry point](../../../tests/lifecycle_archive.py) retains, audits or
reproduces those ordinary files. Full `recovery validate` includes these checks;
`--core-only` continues to exclude dependency/runtime checks explicitly.

The complete fixture selects the first already prepared main world of each
family at **each size**, without outcome-based selection. It retains every
scheduled sibling, event, receipt, complementary mask, Q variant, preserving
continuation, control and repeat for those worlds. Two real local workers run
the target schedule normally and the fallback in reversed order with worker
rotation. Providers use only permitted peer inputs and an injected CPU word
tokenizer; no model or evaluator truth enters the provider.

| Reconciled quantity | Per size | Both sizes |
|---|---:|---:|
| Selected worlds / branches | 5 / 145 | 10 / 290 |
| Four-peer rounds / single-call controls | 540 / 10 | 1,080 / 20 |
| Finished logical slots | 2,170 | 4,340 |
| Physical generations / attempts | 1,978 / 1,978 | 3,956 / 3,956 |
| Exact required replay uses | 192 | 384 |
| Valid / invalid / failed logical outcomes | 1,765 / 270 / 135 | 3,530 / 540 / 270 |
| Unknown logical slots / retries | 0 / 0 | 0 / 0 |

Every replay joins its original physical parent, exact request/settings/seed
and literal validation outcome, including malformed Unicode and timeout parents.
Each continuation costs its prefix plus all sixteen continuation uses, including
F's abandoned prefix. Independent SQL sums reconcile physical attempt seconds,
request/output tokens and policy time/request-token totals. Current source/own
reply equality survives Q's different prose availability; held round-one prose
is absent initially and released in chronological order for recovery round three.
Persistent notices/receipts survive cleared C/F starts and later rounds.

The separate full-manifest check executes **zero** slots. For both sizes it
reconciles main 60 at 16,152 distinct / 17,656 logical and main 40 at
11,504 / 12,560; development is 1,114 / 1,178, with the complete 90-slot capability
prelude. Every unexecuted slot stays unknown. These saved validation populations
are not an accepted M5 freeze or an empirical run.

### Actual externally killed boundaries

The nine checks cover **eleven controller kills**, in addition to the synthetic
budget deadline. Each subprocess launches with the actual argv retained in
`kill-N.json`, using the following controller interface:

```powershell
python -m tests.lifecycle_worker --path <worker-killed.sqlite> --parent <worker-parent.sqlite> --marker <boundary-N.json> --trace <physical-N.jsonl> --policy <policy> --round <round> --peer <peer> --point <point>
```

The test parent calls `Popen.kill()`, waits for a nonzero exit, confirms every
active inference subprocess exited and reacquires the dead owner's OS lock
before reopening. These are real external process deaths, not raised exceptions.
Markers verify **WAL / synchronous FULL (`2`)** on both the application ledger
and checkpoint connections, and verify the controller imports the same runner
module as its parent. Default fixture bounds are eight-second attempts,
0.25-second termination graces and 0.05-second heartbeats; the actual known-timeout
case uses two seconds. M3-T02's production defaults remain unchanged.

| Point / policy / recovery round | Kills | Persisted observation and resume result |
|---|---:|---|
| `before_raw` / Q_B / 2, peer 0 | 1 | Provider returned, but no raw outcome committed. Held prose/checkpoint stay unchanged. One identical retry; uncertain original work keeps absent finish/duration and positive observed work. |
| `after_raw` / Q_B / 2, peer 1 | 1 | Literal malformed reply durable before validation. Same raw outcome and one attempt after resume; no inherited candidate or resampling. |
| `after_timeout` / Q_B / 2, peer 0 | 1 | Real hung inference reaches its deadline; timeout commits before termination. Resume never retries it and confirms inference exit. |
| `validation` / P_G / 1 | 1 | First peer validated; original cross-worker B/C replies already durable. The replay worker has zero physical attempts at the kill. Revalidation/effects remain branch-local. |
| `staging` / Q_C / 2 | 1 | Effects computed before checkpoint. Reconstruction uses saved outcomes and preserves held-prose release. |
| `before_checkpoint` / Q_B / 2 | 1 | Computed delivery state is not authoritative; saved round-one checkpoint still holds prose. Resume commits delivery exactly once. |
| `after_checkpoint` / Q_B / 2 | 1 | Round-two checkpoint is durable and queue drained. Lost acknowledgement cannot duplicate delivery or generation. |
| `after_boundary` / C and F / 1 | 2 | Boundary flag, cleared histories/feedback/candidates and F source removal are durable. Restart/start never reapplies the event or restores cleared work. |
| `before_raw` twice / Q_B / 2, peer 0 | 2 | Both permitted attempts interrupted. Resume records infrastructure failure with two uncertain attempts and one retry; no third attempt or stale candidate. |

Each killed worker is relocated through supported SQLite backup to
`worker-resumed.sqlite`; original parent/sibling records stay unchanged.
Comparisons cover **all** literal call rows, frozen round inputs, validation,
unique committed state transitions, delivery records and offline outcomes,
against uninterrupted `worker-baseline.sqlite`. Only interruption attempts and
measured clocks/process/allocation observations may differ. All attempt numbers
stay at most two. Required replay and already completed failures add no inference.

Each case retains `backup-0.sqlite` (and `backup-1.sqlite` when applicable).
Clean close/reopen reconstructs exact progress/costs at the saved timestamp,
passes SQLite integrity checks and repeats completed round/control operations
with a provider that fails if invoked. Parent snapshots and scientific records
remain identical. The ZIP is 66,344,034 bytes; its actual extracted/reopened
snapshots were compared with the working files before acceptance.

### Safe stop and M4 handoff

The budget case uses a **synthetic** 90-second allocation ceiling and three-second
shutdown reserve. A shortened hard deadline stops hung prefix inference,
confirms release and retains sixteen unknown logical slots, one uncertain
attempt and no fabricated raw failure. `worker-stopped.sqlite`,
`stopped-progress.json` and `stopped-preview.json` preserve that state. Resume
with the same saved configuration finishes sixteen slots with seventeen attempts,
one retry and one uncertain attempt. Allocation partitions sum to the recorded
allocated seconds; released devices remain closed and under the synthetic ceiling.

The bundle contains fourteen evidence cases: two complete fixtures, ten crash
scenarios, one stopped/resumed budget scenario and one full-manifest reconciliation.
Each `selection.json` references saved manifest IDs. `evidence.json` names the
accepted worker files and baseline/backup paths. Use those workers together;
baselines, killed originals and backups are copies of the same call identities.
The reader normalizes retained Windows directory separators to ZIP-relative
paths; new captures use forward slashes without changing the retained ZIP.

Saved manifests, raw/tokenized requests, settings/seeds, attempts/failures,
validation, candidate state, source/text histories, acquisition/delivery timing,
queues, allocations and logical-parent joins provide M4's offline inputs.
`offline-preview.json` demonstrates failure-versus-unknown scoring and exact
event-specific truth/D/U reconstruction. The full estimands, trajectories,
diagnostics, uncertainty and reproducible report remain M4 work; this preview
does not complete them.

### Executed verification, 5 October 2026

| Executed check | Result |
|---|---|
| `.venv/Scripts/python.exe -m recovery validate` | 253 passed in 2,076.658 seconds, including all nine lifecycle checks |
| Installed-library harness run outside the checkout | 253 passed in 2,079.772 seconds; all six implementation module paths/bytes asserted and subprocess runner imports verified |
| `python -S -m recovery validate --core-only` | 81 passed in 55.002 seconds with site packages disabled |
| Focused worker regression | 14 passed in 92.296 seconds after removing redundant checkpoint reads |
| `tests.lifecycle_archive --write-fixture tests/fixtures/scripted_lifecycle_run.zip` | Nine passed in 1,326.735 seconds; fourteen cases packaged, extracted and compared exactly |
| `tests.lifecycle_archive --audit-only` | All accepted databases reopened; complete saved progress/costs/outcomes and stopped snapshots reproduce; repeated after portable path handling |
| Fresh `tests.lifecycle_archive`, hash seed 37 | Nine passed in 1,108.269 seconds; exact fourteen-case records, attempt outcomes, boundary markers and complete inputs reproduce |
| `tests.worker_archive` / `tests.attempt_archive`, hash seed 37 | 14 / 22 passed; eight worker and twelve attempt cases reproduce |
| `tests.accounting_archive`, hash seed 37 | 23 passed; all nine hand-accounting/forecast/stop cases reproduce |
| CPU / native `tests.durable_archive`, hash seed 37 | Each unchanged: 60 branches, 240 rounds, 960 logical calls, 864 attempts, 96 exact parent reuses and two resumed deliveries |
| `pip check`, compilation, documentation/status/protected-file audit and `git diff --check` | Passed; 247 relative links/anchors and all 29 task/index statuses agree. Scientific specification/configuration/dependencies and all prior fixtures unchanged. |

```powershell
.venv/Scripts/python.exe -m recovery validate
python -S -m recovery validate --core-only
.venv/Scripts/python.exe -m tests.lifecycle_archive --audit-only
$env:PYTHONHASHSEED = '37'
.venv/Scripts/python.exe -m tests.lifecycle_archive
.venv/Scripts/python.exe -m tests.worker_archive
.venv/Scripts/python.exe -m tests.attempt_archive
.venv/Scripts/python.exe -m tests.accounting_archive
.venv/Scripts/python.exe -m tests.durable_archive
```

Native durable reproduction used existing pinned local 9B tokenizer metadata
at `$env:TEMP/recovery-capacity-wr5ya_42/9B`, the retained native fixture and the
host Transformers/tokenizers through the existing archive entry point. It loaded
no weights. The executed native command and installed harness invocation were:

```powershell
python -c "import sys; from pathlib import Path; sys.path.insert(1,str(Path('.venv/Lib/site-packages').resolve())); from tests.durable_archive import main; raise SystemExit(main())" --tokenizer "$env:TEMP/recovery-capacity-wr5ya_42/9B" --fixture tests/fixtures/durable_native_traces.json.gz
# From the host temporary directory, using the checkout's absolute .venv Python:
& 'C:/Users/EndritHasani/Downloads/recovery_blueprint/recovery_blueprint/.venv/Scripts/python.exe' './m3-t05-installed-validation.py' 'C:/Users/EndritHasani/Downloads/recovery_blueprint/recovery_blueprint'
```

[Bundle documentation](../../../tests/fixtures/README.md#crash-safe-scripted-lifecycle-run-bundle)
provides focused and offline-only commands. Archive creation is exclusive;
ordinary audit/reproduction preserves the existing ZIP.

Environment: Windows build 26200, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5,
LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and core 1.6.6. The ordinary
non-editable package was built/installed successfully. CPU dependency pins are
not the M5 freeze; concurrent CPU validation durations are not model timings.

Temporary host logs are `m3-t05-{source,installed,core}-validation.log`,
`m3-t05-installed-validation.py`, `m3-t05-worker-regression.log`,
`m3-t05-{worker,attempt,accounting,durable,native}-reproduction.log`,
`m3-t05-lifecycle-{archive,reproduction,offline-audit,portable-audit}.log` and
`m3-t05-documentation-audit.{py,log}`.
The retained ZIP and executed reconstruction are durable evidence; temporary
logs supply full-suite command details.

The initial incomplete fixture exposed repeated readiness scans while workers
were busy and a second read of a checkpoint already fetched for metadata.
`dispatch` now returns when no worker is idle, and scheduling derives state from
the same committed checkpoint. No cache or extra record is introduced; the
fourteen worker checks and full regressions pass. That superseded incomplete run
is not acceptance evidence. Portable archive references were subsequently checked
through the retained bundle's full offline audit; its scientific records and
production runner are unchanged.

### Completion and M3 gate

M3-T05 is implemented and verified on CPU. All five M3 tasks and the combined
durable lifecycle gate pass, with executed checks and reproducible ordinary
artifacts linked above. [M4-T01](../M4/M4-T01-exact-outcomes-and-trajectories.md)
is ready. Progress is fourteen done, one ready and fourteen blocked.

M4 remains mandatory before GPU use. M5 must repeat persistence/host checks
in its accepted environment and verify actual provider release, device
memory/timing and model capability. No GPU allocation, model inference, pilot,
main experiment, frozen-configuration or scientific-design change, or publication
occurred.

