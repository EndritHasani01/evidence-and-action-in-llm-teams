# Course M3 durable workers and bounded failures

Started 11 October 2026 for [course/M3-T01](../todos/course/M3/M3-T01-course-durable-workers-and-failures.md).
Authority is [specification Section 11](../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime)
and the [course living handoff](../IMPLEMENTATION_PLAN.md#11-course-living-handoff).
The [M2 prerequisite audit](../../notebooks/validation/course-m2-capacity/handoff-audit.json)
passes: saved inputs/schedules, explicit 256/64 limits, exact pinned 4B settings,
25 native world traces and the complete 156,251-token resident bound.

This task reuses serial workers, application SQLite records, replacement
LangGraph checkpoints, read-only original parents, bounded resident children and
ownership locks. It will verify course configuration/parent scope, completed
valid/invalid/failed reuse, real process kills around persistence and effects,
held Q prose, and backup/reopen equality. Course accounting, resource admission
and the combined lifecycle gate remain M3-T02. No GPU, model, pilot, freeze,
main experiment or publication is authorized by this task.

[Starting tracked bytes](../../notebooks/validation/course-m3-workers/baseline-files.json.gz)
preserve thesis specification/defaults/todos, all earlier fixtures and the
pre-existing unstaged M5 evidence edit. Executed commands/logs will be retained in
the [existing validation layout](../../notebooks/validation/course-m3-workers/).
Acceptance is pending the retained bundle, installed verification and final regression.

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
The original worker archive comparator encounters a pre-existing additive
`backend_json=null` attempt field absent from its 619 archived attempts. Its
comparison now treats absent and null optional diagnostics identically, as the
attempt comparator already does, retaining every non-null field and the
original fixture bytes. Final reproduction remains to be checked.

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
clock and checks SQLite integrity without inference. Source reproduction and
installed/full regression remain pending at this checkpoint. These scenario
totals are not empirical coverage of course main or development worlds.

Each case reuses saved course world/branch/call IDs and original physical
parents. Scientific comparisons include literal inputs/outputs, native arrays,
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
