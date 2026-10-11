# Course M3 durable workers and bounded failures

Started 11 October 2026 for [course/M3-T01](../todos/course/M3/M3-T01-course-durable-workers-and-failures.md).
Authority is [specification Section 11](../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime)
and the [course living handoff](../IMPLEMENTATION_PLAN.md#11-course-living-handoff).
The [M2 prerequisite audit](../../notebooks/validation/course-m2-capacity/handoff-audit.json)
passes: saved inputs/schedules, explicit 256/64 limits, exact pinned 4B settings,
25 native world traces and the complete 156,251-token resident bound.

This task reuses serial workers, application SQLite records, replacement
LangGraph checkpoints, read-only original parents, bounded resident children and
ownership locks. Verification covers course configuration/parent scope, completed
valid/invalid/failed reuse, real process kills around persistence and effects,
held Q prose, and backup/reopen equality. Course accounting, resource admission
and the combined lifecycle gate remain M3-T02. No GPU, model, pilot, freeze,
main experiment or publication is authorized by this task.

[Starting tracked bytes](../../notebooks/validation/course-m3-workers/baseline-files.json.gz)
preserve thesis specification/defaults/todos, all earlier fixtures and the
pre-existing unstaged M5 evidence edit. Executed commands/logs are retained in
the [existing validation layout](../../notebooks/validation/course-m3-workers/).
The focused, native, retained-bundle, installed and full source checks pass.
The final documentary acceptance audit is recorded below before handoff.

## Implementation checkpoint

The existing worker `run_inputs` row now binds the course regime, saved
worlds/branches, exact pinned 4B settings and attempt bounds. Manifest scheduling
selects the declared 20-world course main scope while retaining the default
60-world thesis selection. Course parents require equal literal bindings;
unbound or foreign records cannot supply prefixes or raw/replay results.
Bound starts/controls reject input drift, including host fields absent from the
peer view. Local prefix parents now check exact settings too. Old standalone
round files remain readable without a migration.

[Focused verification](../../notebooks/validation/course-m3-workers/course-final-command.json)
passes all 11 course methods, including ten actual controller kills across raw,
validation, staging, boundary and delivery commit points. The
[native verification](../../notebooks/validation/course-m3-workers/native-workers-corrected-command.json)
passes 20 exact native request comparisons, eight original-parent replay uses
and backup/reopen equality using local pinned 4B metadata. This auxiliary CPU
check combines the repository SQLite environment with existing host tokenizer
packages; it is not an accepted inference environment. No weights are loaded.

The unchanged original failure archive reproduces all 12 cases/78 attempts.
The original worker archive comparator encountered a pre-existing additive
`backend_json=null` attempt field absent from its 619 archived attempts. Its
comparison now treats absent and null optional diagnostics identically, as the
attempt comparator already does, retaining every non-null field and the
original fixture bytes. The installed reproduction now passes all 14 checks
and matches all eight original worker cases/666 logical calls/48 replays.

Failed commands are retained separately. Test integration corrections cover
derived branch IDs, the actual `output_tokens` field, closing SQLite test handles,
excluding the target C branch from parent construction, forwarding provider
keywords and bounded confirmation of Windows owner-lock release after exit.
Runtime ownership, scientific outcomes and retry rules are unchanged by these
test corrections.

## Retained worker evidence

[course_worker_run.zip](../../tests/fixtures/course_worker_run.zip) retains 16
ordinary CPU worker scenarios: **1,422 completed logical calls, 1,278 generation
slots, 1,281 attempts, 144 replay uses, five uncertain attempts and ten actual
controller kills**. The offline audit reconstructs exact progress at its saved
clock and checks SQLite integrity without inference. Fresh hash-seed-37 source
reproduction passes all 11 checks and matches all 16 cases, including physical
attempt outcomes. Installed verification also passes. These scenario
totals are not empirical coverage of course main or development worlds.

Each case reuses saved course world/branch/call IDs and original physical
parents. Scientific comparisons include literal inputs/outputs, request token arrays,
settings/seeds, validation, committed transitions, queues/cursors and deliveries;
clock/PID/checkpoint identifiers and placement remain measured observations.
Recorded invalid/failed slots remain finished zero-credit outcomes; the rest of
the selected fixed schedule remains unknown. Backup checks reconstruct original
records and progress, and exclusive creation protects existing archives.

Course callers should construct workers from saved manifests, supplying exact
`candidate_settings(tokenizer, QWEN_4B, limits=COURSE_LIMITS)`. `from_manifests`
propagates the saved regime and uses its declared main count without changing
seeds or parents. Direct subset callers pass `regime="course"`. The input-only
`configs/course-inputs.toml` is unchanged and establishes no runtime freeze.
Attempt defaults remain 120 seconds with one-second terminate/kill graces;
shorter 2/8-second CPU fault probes establish bounded mechanics, not model
timeout adequacy. All course accounting/status CLI changes, cumulative resource
admission and the complete all-family course lifecycle gate remain M3-T02.

## Executed validation

Exact argument arrays, working directories, hash seeds, elapsed times, exit
codes and lossless output are retained in
[course-m3-workers](../../notebooks/validation/course-m3-workers/).

| Check | Current result |
|---|---|
| [Original durable/course-settings checks](../../notebooks/validation/course-m3-workers/baseline-durable-command.json) | 24 passed |
| [Focused course workers](../../notebooks/validation/course-m3-workers/course-final-command.json) | 11 passed, including ten real kills |
| [Course bundle creation](../../notebooks/validation/course-m3-workers/course-archive-command.json) / [fresh hash-seed-37 reproduction](../../notebooks/validation/course-m3-workers/course-reproduction-command.json) | 11 / 11 passed; all 16 cases match |
| [Read-only course bundle audit](../../notebooks/validation/course-m3-workers/offline-audit-command.json) | Passed; all 16 cases reconstruct |
| Native 4B worker probe | 20 exact request comparisons, eight replays, backup/reopen equality passed |
| [Unchanged original failure archive](../../notebooks/validation/course-m3-workers/unchanged-attempts-command.json) | 22 passed; 12 cases/78 attempts reproduce |
| Unchanged original worker archive, installed reproduction | 14 passed; eight cases/666 logical calls/48 replays reproduce |
| [Unchanged original lifecycle bundle audit](../../notebooks/validation/course-m3-workers/unchanged-lifecycle-audit-command.json) | Passed; 14 cases/4,340 logical calls/384 replays |
| [Dependency-free core](../../notebooks/validation/course-m3-workers/core-checks-command.json) | 348 run, 340 passed, eight expected optional-library skips |
| [Full source regression](../../notebooks/validation/course-m3-workers/source-full-command.json) | 591 passed, zero skips |
| Installed affected-library/child checks | 95 passed, zero skips; 29 production modules match source |
| [Repository `pip check`](../../notebooks/validation/course-m3-workers/pip-check-command.json) | Passed |
| [Completion audit](../../notebooks/validation/course-m3-workers/completion-audit-command.json) | Passed; 1,323 protected files remain byte-identical |

The CPU environment is Windows, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5,
LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and core 1.6.6. The native
probe additionally uses existing Transformers 5.12.0/tokenizers 0.22.2 metadata
packages. This records actual CPU evidence, not a study environment freeze.

The [installed packet](../../notebooks/validation/course-m3-workers/installed-checks-command.json)
builds a wheel from committed production code, installs it into a fresh
temporary target and runs outside the checkout with hash seed 37 and no source
`PYTHONPATH`. Module and child provenance are asserted. Its 95 affected checks
take 1,911.444 seconds; the complete 2,185.094-second command also reproduces
the unchanged failure and worker archives, audits the original lifecycle bundle
and checks installed dependencies. The
[provenance receipt](../../notebooks/validation/course-m3-workers/installed-provenance.json)
retains the actual wheel, source/module hashes, interpreter and package versions.

The full source CLI finishes all 591 tests in 2,957.335 seconds, with zero skips;
its complete recorded command takes 2,960.734 seconds. It covers the unchanged
thesis analysis/report reproduction and existing protocol, replay, durable,
attempt, scheduling, accounting, lifecycle and scripted inference checks as
well as the registered course worker checks. These counts overlap the focused
and installed suites; they are not additive unique-test totals.

## Completion and handoff

Course/M3-T01's implementation and CPU behavioral acceptance are complete.
The [completion audit](../../notebooks/validation/course-m3-workers/completion-audit.json)
passes: all 1,323 protected starting files remain byte-identical, task/index
counts agree, local references/anchors resolve, executed receipts pass and
installed module bytes still match source. Ten retained kills confirm inference
children exited. Thesis specification/defaults/todos, plan Sections 1–10,
earlier fixtures and saved course inputs remain unchanged; the unrelated M5
edit retains its original SHA-256 and stays unstaged. Course progress is six
done, one ready and fourteen blocked tasks.

[Course/M3-T02](../todos/course/M3/M3-T02-course-accounting-and-lifecycle-gate.md)
is ready for honest accounting/progress, cumulative resource admission and the
tiny all-family scripted lifecycle. Reuse this ordinary worker bundle and
existing records; status/analysis CLI count choices still address thesis 60/40
until the owning course adaptation. The overall course M3 gate remains open.
CPU fault probes establish durability and retry mechanics, not model timeout,
throughput, CUDA memory/headroom, pretrained-model capability, a pilot or main
results. No dependencies/configuration were installed into the repository
environment, no model weights were loaded, and no GPU, paid compute, runtime
freeze, empirical execution or external publication was performed.
