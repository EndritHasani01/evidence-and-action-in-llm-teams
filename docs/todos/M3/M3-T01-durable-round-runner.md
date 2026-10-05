# M3-T01 — Durable rounds and exact response reuse

**Status:** done

**Dependencies:** [M2-T06](../M2/M2-T06-attainability-and-capacity.md). The M2 CPU gate passed on 5 October 2026; use its finalized literal renderer, scalar-message contract and 262,144 input limit.

## References

- [Repository contract](../../../AGENTS.md), [plan persistence architecture](../../IMPLEMENTATION_PLAN.md#round-execution-persistence-and-worker-ownership), and [M3](../../IMPLEMENTATION_PLAN.md#5-milestone-m3--durable-runner-failures-cost-and-progress).
- Specification [§3–4](../../../PROJECT_SPECIFICATION.md#3-common-peer-protocol) and [§9](../../../PROJECT_SPECIFICATION.md#9-implementation-and-consistency-requirements).
- Technical evidence: [persistence limits](../../implementation-research/state-and-replay.md#persistence-recommendation-and-its-limits).

## Intended outcome

The validated round procedure runs through LangGraph/local SQLite, with exact durable replies committed before effects and reconstructible branch checkpoints.

## Scope and boundaries

- Use one SQLite file per worker, ordinary application-owned transactions for calls/attempts, and explicit replacement checkpoint state for the four peers. No append reducer may restore cleared history.
- Start each branch in a new thread from a deep-deserialized drained original prefix. Persist boundary application so resume cannot apply it twice.
- Retain exact requests/settings/seeds, raw text/generated IDs or failure records, pre-delivery parent barriers, phase/round/prefix relationships, queue/cursor state and branch-scoped applied message IDs.
- Completed call identities always return their exact persisted response/failure, including invalid outcomes. Mixed/Q replay checks request/settings/seed/view equality and uses the proper event/replicate parent; never import parent post-delivery tables or deduplicate unrelated matching requests.
- Committed checkpoints own peer state and delivery effects. Derive delivery exports from committed transitions; do not add a competing authoritative effect store.
- Verify synchronous checkpoint durability and SQLite settings. Do not use saver-private transaction helpers for application writes or hold write locks during inference. Use clean checkpoint/close or SQLite backup for archives.
- Start with LangGraph as approved. Use the small-loop fallback only if the real integration demonstrates an unresolved semantic incompatibility, documenting it in the plan while retaining all contracts/tests.

## Completion criteria

- Raw responses/failures are durable before validation-dependent effects.
- Restart reconstructs an interrupted transition from saved replies without inference; stable delivery IDs prevent repeated effects within a branch.
- Explicit slot/generation/replay identities and statuses distinguish pending, active attempt, completed raw reply, timeout, exhausted infrastructure failure and replay use; validity/correctness are separate.
- Database reopen and backup preserve the authoritative committed state without restoring cleared fields or mutating siblings.

## Validation and evidence

Run scripted save/reopen/resume checks, invalid parent reuse, equality mismatch rejection, per-branch delivery idempotence and replacement clearing. Inspect actual SQLite/durability behavior instead of assuming the research toy's results transfer. M3-T05 performs the full killed-process acceptance suite after attempt/scheduler/accounting integration.

### Implemented persistence ownership

[runner.py](../../../recovery/runner.py) wraps the validated pure protocol in
`prepare → obtain → commit`, using `durability="sync"` and replacement byte
snapshots. `start` commits a new prefix/event boundary in its own scheduled
thread. Repeating a start compares the original inputs without clearing newly
accumulated work. Explicit round arguments return already committed results
without advancing another opportunity. Every read deep-deserializes peer state.

[storage.py](../../../recovery/storage.py) owns ordinary application transactions
on a separate connection to the same worker file. `round_inputs` preserves exact
pre-delivery state, rendered/native requests, schedule and settings; `calls`
preserves logical/generation/replay joins, seeds, statuses, raw outputs/failures
and separate deterministic validation. `attempts` records start/completion and
elapsed time. Physical raw outcomes live once; replay rows reference their
prescribed parent. Providers receive only permitted inputs and fresh settings,
and no write transaction spans generation.

Checkpoints exclusively own peer state, queues, delivery cursors and applied
component IDs; delivery exports derive from them. Actual saver failure tests
showed that durable pending node writes must be excluded from these exports.
The runner reads the public saved checkpoint configuration before obtaining
state, then lets normal graph resume consume pending writes. There is no second
effect table, identity scheme, append reducer or alternative runner.

### Executed verification, 5 October 2026

The [18 focused durable checks](../../../tests/durable_checks.py) passed,
including these named scientific failure modes:

- `test_raw_invalid_and_failures_commit_before_validation_and_resume_without_inference`
  and `test_partial_raw_commit_resume_skips_only_completed_calls` preserve exact
  invalid text/IDs, known timeout/exhausted failures and completed slot identities.
- `test_boundary_replacement_all_families_sizes_siblings_events_and_replicates_survives_reopen`
  covers every scheduled first-round continuation of ten family/size cases;
  repeated starts/reopen preserve clearing, K's actual result/absence and siblings.
- `test_durable_invalid_failed_and_unicode_parent_reuse_is_exact_and_branch_local`
  and `test_equality_mismatches_missing_parents_and_recorded_validation_stop_without_effects`
  verify replay, nine missing/equality defects, branch-local effects and delivery IDs.
- `test_q_held_queue_and_release_survive_interrupted_delivery_resume`,
  `test_interrupted_pure_effects_reconstruct_from_saved_replies_without_mutation`
  and `test_checkpoint_write_failure_before_and_after_commit_has_one_authoritative_effect`
  test queue/cursor recovery, no repeated effects and committed versus pending writes.
- `test_identical_nonreplay_q_parent_requests_settings_and_seeds_are_not_deduplicated`
  and `test_unrelated_equal_requests_and_repeat_seeds_keep_distinct_physical_generations`
  prevent unauthorized response sharing. Actual WAL/FULL, synchronous durability,
  rollback, unlocked providers, backup, tokenizer/settings drift, overflow and
  active-without-raw blocking are separately exercised.

| Executed check | Result |
|---|---|
| `.venv/Scripts/python.exe -m recovery validate` | 185 passed: original 167 plus 18 durable checks |
| Installed-library harness from the host temporary directory | 185 passed; asserted/imported `.venv/Lib/site-packages/recovery/runner.py` before adding checkout tests |
| `python -S -m recovery validate --core-only` | 81 passed with site packages disabled |
| Fresh-process CPU/native archive reproduction, hash seed 37 | Both passed; exact requests, outcomes, state/queue and joins reproduce |
| `pip check`, compilation, 198 relative links/anchors across six changed documents, task counts and `git diff --check` | Passed |
| Protected specification/configuration, M2 archives, research and vendor diff | Empty |

Source and installed regressions took 238.076 / 237.540 seconds with independent
CPU checks running concurrently; these are validation timings, not an inference
forecast. The installed harness discovers checkout tests and explicitly adds
`protocol_checks`, `round_checks`, `event_checks`, `replay_checks`,
`attainability_checks` and `durable_checks`. CLI validation intentionally requires
the checkout. Command logs are `m3-t01-{source,installed,core}-validation.log` in
the host temporary directory; the installed harness is
`m3-t01-installed-validation.py` there.
The documentation/count/protected-file audit is
`m3-t01-documentation-audit.py` in the same directory.

The [CPU archive](../../../tests/fixtures/durable_round_traces.json.gz) and
[native archive](../../../tests/fixtures/durable_native_traces.json.gz), produced
by [durable_archive.py](../../../tests/durable_archive.py), each record target
Sort and fallback BFS through all their scheduled four-peer branches and full
horizons: **60 branches, 240 rounds, 960 logical calls, 864 physical attempts,
96 exact parent reuses and two interrupted Q delivery transitions**. Both live
SQLite backups reopen with identical committed states and successful integrity
checks. Wall clocks remain in the application ledger and are omitted from the
deterministic derived fixtures. See [archive reproduction](../../../tests/fixtures/README.md#durable-round-runner-traces).

Environment: Windows, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5,
LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1, core 1.6.6. Native checks
use host Transformers 5.12.0 / tokenizers 0.22.2 with those `.venv` graph packages.
The local 9B metadata at `$env:TEMP/recovery-capacity-wr5ya_42/9B` match M2's
tokenizer/config/template file identities and revision
`c202236235762e1c871ad0ccb60c8ee5ba337b9a`. No weights or model were loaded.

### Completion and handoff

M3-T01 is implemented and verified on CPU. [M3-T02](M3-T02-bounded-attempts-and-failures.md)
is ready. Its process boundary must resolve `running` attempts with no durable
raw outcome, record uncertain completion, enforce termination/timeout and the
single identical-request retry. T01 safely blocks such attempts; it does not
resample them or claim exactly-once generation. Recorded completed failures and
invalid replies already resume exactly. Worker scheduling/control integration,
cross-worker parent access and resource accounting remain M3-T03/T04.

The interruption checks use injected exceptions and actual disk close/reopen;
M3-T05 still owns the full killed-process suite after attempts/scheduling/accounting
integration. M3's gate remains open. Progress is ten done, one ready and eighteen
blocked. There was no scientific/frozen-configuration change, GPU allocation,
model inference, pilot, main experiment or publication.

