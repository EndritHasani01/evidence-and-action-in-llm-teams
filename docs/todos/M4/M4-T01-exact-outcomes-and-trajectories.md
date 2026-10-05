# M4-T01 — Exact outcomes, preservation and trajectories

**Status:** done

**Dependencies:** [M3-T05](../M3/M3-T05-crash-safe-scripted-lifecycle.md). M1–M3 must have passed.
As of 5 October 2026, M1–M3 have passed on CPU; see the
[M3 gate evidence](../M3/M3-T05-crash-safe-scripted-lifecycle.md#completion-and-m3-gate)
and [retained lifecycle bundle](../../../tests/fixtures/scripted_lifecycle_run.zip).
Use its saved manifests, exact raw/validated outcomes, committed histories and
original generation/replay/attempt joins, including the stopped unknown slots.
At the M3 handoff, the offline preview demonstrated input completeness. This
task adds the offline analysis and verification documented below.

## References

- [Repository contract](../../../AGENTS.md), [plan exact outcomes](../../IMPLEMENTATION_PLAN.md#exact-outcomes-and-contrasts), and [explanatory outcomes](../../IMPLEMENTATION_PLAN.md#explanatory-outcomes-and-costs).
- Specification [§5.1](../../../PROJECT_SPECIFICATION.md#51-exact-outcomes), [§6](../../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness), and [§7.1](../../../PROJECT_SPECIFICATION.md#71-repair-preservation-and-synchronized-completion).

## Intended outcome

Offline scoring turns the complete slot manifest and recorded replies into exact outcomes, coordinate diagnostics, trajectory categories and observable annotations with explicit denominators.

## Scope and boundaries

- Join the full schedule before scoring. Event-specific gold stays evaluator-only. Preserve list order/multiplicity and the full BFS key set; recorded invalid/failed slots score zero while unexecuted slots remain unknown.
- Compute per-round mean peer correctness, normalized recovery AUC over all sixteen opportunities, and final all-four correctness. The reset boundary is not an extra failed round.
- Use unique task coordinates to define D/U. Measure revised correctness and explicit old-gold persistence on D. Preservation/collateral damage on U is eligible only where that same peer's protocol-valid prefix-round-four candidate was correct.
- Separate repair of old U errors from damage to old correct outputs. Invalid answers count incorrect for accuracy/preservation but remain a distinct malformed/missing category for explicit old-value persistence.
- Empty denominators are N/A. Average eligible peers, then worlds, then equal eligible families; publish unique-coordinate and peer-copy counts without removing worlds from main outcomes.
- Derive first joint correctness, first joint correctness maintained through round four, regression, the four specified complete-branch categories and fragmentation. Keep incomplete branches separate. No successful-only time averages, invented fifth round or best-answer splicing.
- Identical-but-wrong agreement applies only to replicated-output tasks. Implement six nonexclusive annotations: protocol/inference failure, v2 unavailable, incorrect after v2, explicit old-value persistence, collateral error and regression, with counts/intersections and archived provenance.

## Completion criteria

- Outcome/diagnostic tables preserve world/event/policy/replicate/peer/round and generation/replay relationships.
- Recorded failure and unknown execution produce distinct scoring and trajectory results.
- Eligibility, empty-denominator reasons and annotation overlaps are auditable from saved records.
- Evaluation can run entirely offline without importing inference or feeding correctness into the runner.

## Validation and evidence

Use hand-checked exact and duplicate-sensitive answers, full BFS dictionaries, malformed/failed/unknown slots, invalid final-prefix candidates, empty D/U eligibility, repaired old errors and collateral damage. Include continuously correct, delayed, regressing, transient, never-joint and fragmented trajectories, plus differently assigned Prefix/Sort outputs. Reproduce expected peer/world/family denominators and failure annotations.

**Evidence:** Implementation started on 5 October 2026 on `feat/m4-offline-analysis`
from clean commit `54b434c`. Authority, M3 gate evidence, complete saved manifests,
raw/validated outcomes, pre-delivery states and stopped slots have been inspected.
M4's remaining analysis/report gate stays open.

Checkpoint `bd255db` implements the pure scoring/coordinate/trajectory core.
Checkpoint `d8a5026` adds persisted offline joins, annotations and the CLI.
`python -S -m unittest tests.test_evaluate -q` now passes 26 focused checks,
including saved-record decoding, exact parent joins, nested peer/world/family
rates, six annotation labels and overlaps, read-only workers, exclusive JSON/gzip
exports and the offline CLI's complete 1,178-slot development join. These checks
block optional runtime/model imports. The final core suite passes 108 checks;
27 installed-library checks pass outside the checkout with module paths/bytes
asserted. The [retained tables](../../../tests/fixtures/exact_outcome_tables.json.gz)
reproduce all sixteen [offline cases](../../../tests/fixtures/README.md#exact-offline-outcomes-and-trajectories),
including both full main manifests and stopped slots, under hash seed 37.
M3's retained lifecycle archive passes its offline audit after BFS preview decoding.
Complete process-crash regression passes all 278 checks in 1,459.275 seconds,
including all nine lifecycle checks. The two final source-drift/prefix-eligibility
checks added during that run pass in the final focused/core/installed suites.

### Implementation and scientific semantics

[evaluate.py](../../../recovery/evaluate.py) supplies direct offline functions
for exact scoring, coordinate diagnostics, trajectories, saved-record joins,
annotation counts and exclusive JSON/gzip exports. The
[CLI](../../../recovery/__main__.py) exposes `recovery analyze`. No dependency,
identity system, persistence layer, model call or execution decision is added.
The saved complete schedule remains the slot authority; worker calls, attempts
and pre-delivery inputs remain the outcome/provenance authority.

- Whole-list comparison retains order and duplicates; BFS comparison includes
  every node and unreachable value. Recorded invalid/failed slots score zero;
  pending/unexecuted slots are unknown. Completed raw replies require their
  saved protocol validation before analysis; missing validation is an error.
- Prefix context comes exclusively from each peer's original round-four call,
  including invalid/failed absence. It never backfills an earlier correct answer.
  D/U use unique task coordinates. Correct old U values define preservation and
  collateral eligibility; incorrect old U values separately define repair.
- Rates average eligible peers, then worlds, then equal eligible families.
  Structural empty denominators and unknown prefix eligibility have separate
  reasons/counts. Unknown eligible outcomes keep summaries unknown. Diagnostic
  ineligibility never removes a world from the complete outcome table.
- Four scheduled rounds supply sixteen opportunities for AUC. The boundary adds
  no round. First/stable joint times, observed regressions, four complete
  categories and fragmentation retain incomplete branches separately. Prefix/Sort
  segments have no identical-answer agreement requirement.
- The six annotations are observable and nonexclusive. Call-boundary sources
  determine usable v2 availability, including tombstones; delivery IDs identify
  archived receipt evidence. Counts expose applicability, observation, unknowns,
  inclusive pair intersections and exact higher-order overlap patterns.
- All tables preserve world/event/policy/replicate/round/peer and original
  generation/replay/prefix relationships. Saved replay requests, permitted views,
  settings, seeds and outcomes must equal the physical parent. An unexecuted
  logical replay stays unknown even when that parent is already recorded.

### Hand-checked expectations and retained tables

[Focused tests](../../../tests/test_evaluate.py) verify all five candidate shapes,
duplicate/order errors, complete BFS dictionaries and canonical saved pairs,
malformed/failed/unknown outcomes, invalid final-prefix candidates, empty D/U,
old-error repair versus collateral damage, nested rates and annotation overlaps.
They also block imports of runtime/model dependencies, protect existing exports,
reject duplicate workers and detect source-manifest drift in unbound workers.

The Difference coordinate fixture changes j=1,2 in a 23-coordinate old answer.
Its last-prefix candidate was wrong at unchanged j=4; the current candidate
repairs j=4, damages previously correct j=3 and persists at old gold on j=1.
Expected D accuracy/persistence are 1/2 each, preservation is 19/20, collateral
damage is 1/20 and old-error repair is 1/1. Invalid current answers yield zero
accuracy/preservation and a distinct malformed/missing changed-output category.
The family-rate fixture yields 5/8 from family means 1/4 and 1, with 31 unique
eligible coordinates versus 32 peer copies.

| Joint correctness over four rounds | AUC | First joint | First maintained through round four | Complete category |
|---|---:|---:|---:|---|
| 1,1,1,1 | 1 | 1 | 1 | continuously correct |
| 0,0,1,1 | 1/2 | 3 | 3 | correct at end after delay/regression |
| 1,0,0,1 | 1/2 | 1 | 4 | correct at end after delay/regression |
| 0,1,0,0 | 1/4 | 2 | N/A | temporarily correct, incorrect at end |
| 0,0,0,0 | 0 | N/A | N/A | never jointly correct |

These fixtures set all peers to the listed joint outcome. A separate fragmented
fixture has one different correct peer per round: all peers are ever correct,
joint completion remains zero and AUC is 1/4. Unknown opportunities make the
branch incomplete and its AUC unknown; they receive no invented recovery time.

[exact_outcome_tables.json.gz](../../../tests/fixtures/exact_outcome_tables.json.gz)
contains sixteen derived cases. [Reconstruction](../../../tests/outcome_archive.py)
reads the existing M3 manifests and evidence-named workers, with no generation.
[Archive checks](../../../tests/test_outcome_archive.py) compare every table and
independently verify scheduled/executed counts, original attempt/replay joins and
stopped uncertainty. [Fixture documentation](../../../tests/fixtures/README.md#exact-offline-outcomes-and-trajectories)
defines the table fields and reproduction contract.

| Retained case | Scheduled | Recorded | Unknown |
|---|---:|---:|---:|
| Complete five-family fixture, each size | 2,170 | 2,170 | 0 |
| Full target-60 main manifest | 17,656 | 2,170 | 15,486 |
| Full fallback-40 main manifest | 12,560 | 2,170 | 10,390 |
| Stopped budget prefix | 16 | 0 | 16 |

The complete fixtures together retain 4,340 logical outcomes, 3,956 original
physical attempts and 384 exact replay uses. Each size has 1,765 valid,
270 invalid and 135 failed logical outcomes. All their complete scripted paths
are never jointly correct; they were designed for protocol/lifecycle validation.
The hand-checked fixtures above supply the remaining trajectory cases. Neither
fixture supplies a model-capability or empirical recovery result.

### Review discoveries

M3's preview had passed serialized BFS key/value pairs directly to a dictionary
scorer. The evaluator now decodes the existing canonical format with exact key
checks, and the preview helper uses the same decoding. Hand-checked correct BFS
answers are credited. The retained M3 BFS replies are wrong, so their scores and
all prior artifacts remain unchanged; its complete offline audit passes.

A regression test also demonstrated that manually started, unbound workers
could carry sources inconsistent with the evaluator manifest. Analysis now checks
saved original/event input scope and every known/pending current source against
that manifest, including controls. This rejects drift before scoring without
adding checksums or changing the saved records.

### Reproduction and executed checks

```powershell
python -S -m unittest tests.test_evaluate -q
python -S -m recovery validate --core-only
$env:PYTHONHASHSEED = '37'
python -S -m tests.outcome_archive
.venv/Scripts/python.exe -m tests.lifecycle_archive --audit-only
.venv/Scripts/python.exe -m recovery validate
.venv/Scripts/python.exe -m pip check
```

For ordinary saved runs, [README](../../../README.md#offline-exact-outcomes-and-trajectories)
documents `python -S -m recovery analyze` and `evaluate_run`. Output paths are
exclusive. Backups/baselines cannot be supplied alongside original physical
workers. Unknown workers are read-only missing inputs and are never created.

| Executed check | Result |
|---|---|
| Focused dependency-free evaluator suite | 26 passed |
| Final `python -S -m recovery validate --core-only` | 108 passed in 90.769 seconds |
| Installed-library evaluator/archive harness outside checkout | 27 passed in 31.552 seconds; six implementation module paths/bytes asserted |
| Fresh offline table reproduction, hash seed 37 | All sixteen cases and every table match the retained export |
| Retained M3 lifecycle `--audit-only` | All fourteen original evidence cases, previews, worker integrity/progress/costs and stopped snapshots reproduce |
| Complete CPU source regression | 278 passed in 1,459.275 seconds; all nine lifecycle checks pass |
| Package build/install, `pip check`, compilation | Passed; ordinary non-editable isolated wheel build, no dependency changes |

Windows build 26200, Python 3.11.9, SQLite 3.45.1, Pydantic 2.13.5, LangGraph
1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and core 1.6.6. CPU validation only;
this package environment is not an accepted M5 freeze. The documentation/status/
protected-file audit passes all 289 relative links/anchors across nine documents
and all 29 task/index statuses. `git diff --check` passes. Temporary logs use `$env:TEMP/m4-t01-*`; durable acceptance evidence is
the retained export and executed reconstruction. Scientific specification,
configuration, dependencies and all earlier fixtures remain unchanged.

### Completion and handoff

M4-T01 is implemented and verified on CPU. Checkpoints `bd255db`, `d8a5026` and
`bb42ebf` separately commit the pure core, persisted evaluation/CLI and retained
tables/source-drift review. The final evidence commit closes this task. Progress
is fifteen done, three ready and eleven blocked; M4-T02–T04 can now consume the
saved joins and tables. M4-T05–T06 and the complete analysis/report gate remain
open. No GPU/model inference, pilot, main experiment, frozen/scientific change or
publication occurred.

