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
Acceptance is pending.
