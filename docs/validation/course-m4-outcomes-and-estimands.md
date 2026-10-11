# Course exact outcomes and estimands

Completed and verified on CPU 11 October 2026 for [course/M4-T01](../todos/course/M4/M4-T01-course-outcomes-and-estimands.md), started
from `adaceac` on `feat/course-m3-m4-durable-execution-and-analysis`.
Authority is [specification outcomes](../../PROJECT_SPECIFICATION.md#5-outcomes-and-prespecified-estimands),
[repetition/missingness](../../PROJECT_SPECIFICATION.md#6-statistical-analysis-repetition-and-missingness),
the [adopted course clause](../../PROJECT_SPECIFICATION.md#11-adopted-absiis-course-regime)
and [plan exact analysis](../IMPLEMENTATION_PLAN.md#exact-outcomes-and-contrasts).
The [course handoff](../planning/course-study-session-handoff.md) and
[completed M3 prerequisite](course-m3-accounting-and-lifecycle.md#completion-and-handoff)
have been inspected. Their original lifecycle/worker bundles supply CPU scripted
records, not empirical population coverage.

Reuse `evaluate.py` and `analysis.py`, exact raw/validated response joins,
original generation/replay/prefix identities and the saved course manifests.
Preserve unknown unexecuted slots, zero-credit recorded failures, all intended
20/eight/five-world populations and separate replicate-zero summaries.
No additional runtime, scientific parameters or persistence layer is needed.

Preparation identified two course integration gaps: the analysis CLI fixes the
main count at 60, and repeat analysis fixes eligibility at the thesis's first two
worlds per family. The saved population already declares its main count and
continuation seed streams. Use those existing declarations, preserving thesis
60/40 and ten-repeat behavior.

[Starting tracked bytes](../../notebooks/validation/course-m4-outcomes/baseline-files.json.gz)
capture protected files and the user's unrelated local M5 evidence edit.
Exact executed commands and logs will use the
[existing validation layout](../../notebooks/validation/course-m4-outcomes/).
At the preparation checkpoint, outcome/estimand acceptance, retained
reconstruction and installed verification remained pending. Later course diagnostics, costs,
uncertainty and the complete M4 report gate remain separate work. No GPU/model,
pilot/main execution, frozen-configuration change or publication is authorized.

## Formula and implementation checkpoint

The analysis CLI now infers the saved population's main count (20 course,
60 thesis) and permits explicit declared 20/60/40 scopes. Invalid cross-regime
counts fail before export. Every repeat population/contrast/category join uses
the world's saved two continuation seed streams: five course prefixes, ten
thesis prefixes. `evaluate.py` now checks valid raw replies against the exact
saved protocol limits; accepting a course reply above 256 tokens as valid would
contradict its archived validation. Old thesis settings retain 384 by default.
No renderer, runtime protocol or scientific formula changes.

[Focused formula/record/CLI acceptance](../../notebooks/validation/course-m4-outcomes/formulas-corrected-command.json)
passes 68 methods in 105.118 seconds, including 17 independent course checks and
the existing thesis outcome/estimand suites. The complete course matrix retains
6,824 primary contrast rows, 1,240 repeated rows, 80 conditional comparison rows
and 50 trajectory pairs. All non-preservation summaries keep four worlds per
eligible family. Preservation's unknown or empty eligibility remains explicit.
The initial failing test log is retained: test construction used analysis labels
instead of manifest subset keys, omitted a CLI flag and retained orphan attempt
records after removing replies. Corrected fixtures honor the existing contracts;
no production guard was relaxed.

Original-worker reconstruction, fresh-process reproduction, affected M4/core
regressions, installed verification and completion audits remained pending at this
checkpoint; these focused tests alone did not close the task.

## Original-worker reconstruction checkpoint

[Seven retained scopes](../../tests/fixtures/course_analysis_tables.json.gz)
reconstruct from the untouched course M3 lifecycle using
[course_analysis_archive.py](../../tests/course_analysis_archive.py).
They retain all three ordinary cases, the stopped snapshot, the full intended
main join with the five-family workers and completely missing main/development
workers. Independent raw SQLite joins use the existing insertion-order numeric
references and synchronous edge-relaxation gold, with separate direct AUC,
all-four and theta/phi calculations. No scorer, truth solver, runtime, parser,
tokenizer or inference provider is used by that independent reference.

[Archive acceptance](../../notebooks/validation/course-m4-outcomes/archive-worker-final-command.json)
passes all three methods in 53.744 seconds under hash seed 37. Every derived
table matches the saved export. A fresh subprocess blocks runtime/model imports
and reproduces the complete export. Original SQLite bytes and ZIPs remain
unchanged. The full main join has 2,170 recorded/4,110 unknown slots; recorded
135 failures and 270 invalid replies remain zero. Intended theta/phi stay
unknown over all 20 worlds, with four-per-family denominators and only five
complete worlds. Their separately labeled complete-case values are zero.
Receipts/Q/preserving retain eight worlds, and repeats retain five fixed prefixes.

The earlier course worker bundle is audited separately across all sixteen
original scopes: 1,422 recorded/312 unknown slots. These fault probes execute
selected rounds; acceptance of restart mechanics did not execute their complete
schedules. Its controls-only ledger spans main/development; slot-level evaluation
passes while the original domain-pooling guard rejects estimand aggregation.
Backups/baselines are never pooled with original physical workers.

Initial reference failures remain in the command logs. The independent helper
now uses actual `bfs_distance` labels, skips deleted edges, keeps unordered Top-K
records and explicitly closes SQLite handles. The worker audit preserves its
intentional unknowns and domain guard. No production guard was relaxed and no
original fixture was edited. Affected M4/core regression, installed acceptance
and final documentation/protected-byte audits remain pending here.

## Independent course expectations

[Course hand fixtures](../../tests/test_course_analysis.py) use explicit binary
matrices and exact fractions, independently of replies or model behavior.
Actual U-coordinate eligibility is checked on the original workers; the receipt
companion fixture separately states one synthetic eligible coordinate per peer.
These expectations establish implementation semantics, not measured effects.

| Requirement | Independent expectation |
|---|---|
| Revised C-B = 1/2; sham C-B = 1/2, 0, 1 | theta = 0, +1/2, -1/2; both direct components displayed |
| Same retained peers, no / beneficial / harmful teammate reset | phi = 0 / +1 / -1 over six peer-round slots per group |
| Same beneficial effect under revision and sham | phi = +1; phi_corr = 0; round-one E_keep = 0 by exact parent reuse |
| Complementary G/H matrix with cancelling retained effects | E_keep = 0, E_clear = 1/2, own-reset effects = -3/4 and -1/4; all four masks visible |
| Revised C-B / K-C / K-B / B-L / C-F | AUC = 1/4 / 1/4 / 1/2 / 1/4 / -1/2; final C-F = -1 |
| Sham K-C / K-B and correction interactions | Sham = -1/4 / -1/2; interactions = +1/2 / +1 |
| Receipt B/C/K cells = 1/4, 1/2, 3/4; disclosed = 1/2, 1/4, 1 | eta = 1/2; direct effects = +1/4, -1/4, +1/4; all representation/endpoint companions |
| C and K each gain 1/2 from the receipt | eta = 0, with both direct benefits visible |
| Q_B-B / Q_C-C, revision then sham | Round two = +1/2, -1/2 / -1/4, +1/2; round one = 0; constant later effects yield AUC = 3/4 of the immediate effect |
| Preserving B/C/K continuously correct for one/two/four rounds | Cells = 1/4, 1/2, 1; C-B/K-C/K-B = 1/4, 1/2, 3/4; final and preservation companions match |
| Three +1 worlds in one family, zero in the other four | Equal-family theta = 1/5, not pooled 3/7 |
| Three +1 Prefix receipt worlds and one zero Sort world | Equal two-family eta = 1/2, not pooled 3/4 |
| Peer preservation 9/10 and 0/1 | Mean = 9/20; ten unique coordinates and eleven peer copies; unknown prefix eligibility stays unknown |
| One unknown world in the complete 20-world manifest | Intended theta unknown; 19 observed worlds and four-per-family denominators; separate complete-case value 1 |
| Correct earlier replies followed by invalid/timeout/unexecuted final slot | Current credit = 0/0/unknown; AUC = 15/16, 15/16, unknown; no answer inheritance |
| Changed repeat seeds/outcomes | Main tables unchanged; exact ties distinct from strict sign reversals; incomplete trajectory changes unknown; only five fixed repeated prefixes |
| Missing parent, malformed complete BFS keys or over-cap valid course reply | Reject inconsistent evidence; no replay synthesis or reply repair |

The course non-preservation family denominators are four in full main summaries;
named focal populations each have eight worlds. Preservation's eligible peer,
world and family denominators may differ and remain explicit. Every primary
component retains exact scheduled call/generation/replay/prefix IDs, rounds,
peers, seed and rational coefficients. There is no added reset-boundary round,
world selection, repeat averaging or outcome-adaptive admission.

## Core and preservation checkpoint

[Core-only acceptance](../../notebooks/validation/course-m4-outcomes/core-accepted-command.json)
passes 368 methods in 450.352 seconds: 360 passed and eight expected declared-package
skips under `python -S`, with hash seed 73. The command validates the actual
course TOML, saved population/schedules and exact authoritative input equality
without resampling, then checks both mathematical sizes. Runtime suites and
optional checkpoint/plot consumers are not accepted by this core run; the
affected integrated source/installed M4 checks remain pending here.

[Dependency checking](../../notebooks/validation/course-m4-outcomes/pip-check-command.json)
and [compilation](../../notebooks/validation/course-m4-outcomes/compile-check-command.json)
pass. The [implementation audit](../../notebooks/validation/course-m4-outcomes/implementation-audit.json)
verifies all 1,469 protected starting files byte-for-byte, including the user's
unchanged unstaged M5 edit, all scientific/configuration/old fixture evidence,
thesis todos and plan Sections 1–10. All 21 task/index states and milestone
counts agree; 701 scoped local references and 288 heading anchors resolve.
`git diff --check` passes. The task remains active pending integrated acceptance
and the final completed-handoff audit.

The executed environment is Windows build 26200, Python 3.11.9, SQLite 3.45.1,
Pydantic 2.13.5, LangGraph 1.2.12, checkpoint 4.2.0, SQLite saver 3.1.1 and
langchain-core 1.6.6. No dependency was added or changed. CPU test durations
include archive reconstruction and concurrent tests; they are not model/GPU
timing evidence or an accepted inference freeze. Test counts overlap across
commands and are not additive independent checks.

## Completion and handoff

Course/M4-T01 is implemented and verified on CPU.
[Complete affected source acceptance](../../notebooks/validation/course-m4-outcomes/source-m4-accepted-command.json)
passes all 191 methods in 1,171.766 seconds with zero skips.
[Outside-checkout installed acceptance](../../notebooks/validation/course-m4-outcomes/installed-accepted-command.json)
passes the same 191 methods in 1,176.501 seconds with zero skips; its complete
build/install/provenance/dependency command takes 1,195.953 seconds. Both runs
cover outcomes, all estimands, independent course cohorts/signs/nulls/companions,
record/CLI integration, every affected M4 consumer and original thesis archives.
All sixteen original thesis report scopes reproduce twice with exact tables,
case IDs and deterministic plotting inputs. Seven course table scopes and all
sixteen earlier course worker scopes reconstruct independently without inference
or worker mutation.

The [installed provenance](../../notebooks/validation/course-m4-outcomes/installed-provenance.json)
verifies a fresh wheel/target, outside-checkout imports with no source PYTHONPATH,
and all 29 production module bytes. Both acceptance commands began from
`c6dc31a`; the installed completion receipt records later documentation commit
`5d4ff6c`. Production, tests, inputs and configurations are identical between
those commits and throughout acceptance. The final audit checks that distinction
and every installed module byte, rather than treating a documentation commit
as changed production. Installation used the existing declared CPU packages
and changed no repository dependency environment.

| Executed acceptance | Result |
|---|---|
| [Focused formulas/records/CLI](../../notebooks/validation/course-m4-outcomes/formulas-corrected-command.json) | 68 passed; 17 new course cases plus thesis regressions |
| [Course archive and import guard](../../notebooks/validation/course-m4-outcomes/archive-worker-final-command.json) | Three methods passed under hash seed 37; every retained table, original-worker scope and inference-free fresh process checked |
| [Complete affected source M4](../../notebooks/validation/course-m4-outcomes/source-m4-accepted-command.json) | 191 passed, zero skips |
| [Installed M4 packet](../../notebooks/validation/course-m4-outcomes/installed-accepted-command.json) | 191 passed, zero skips; exact 29-module provenance and dependency check |
| [Core/config/input/schedule](../../notebooks/validation/course-m4-outcomes/core-accepted-command.json) | 368 run: 360 passed, eight expected optional-package skips; hash seed 73 |
| [Dependency check](../../notebooks/validation/course-m4-outcomes/pip-check-command.json) / [compilation](../../notebooks/validation/course-m4-outcomes/compile-check-command.json) | Passed |

Commands, literal argv, clocks, exit status and lossless logs are retained beside
the receipts. The affected integrated checks supply optional checkpoint/plot
coverage skipped under `-S`. Unchanged M3 runtime/replay/native/kill acceptance is
reused from the [passing prerequisite](course-m3-accounting-and-lifecycle.md#completion-and-handoff);
its code, inputs, settings and original artifacts remain protected. No GPU/model
or main experiment execution is required for this offline task.

```powershell
.venv/Scripts/python.exe -X utf8 -m unittest tests.test_course_analysis tests.test_course_analysis_archive -v
.venv/Scripts/python.exe -S -X utf8 -m recovery validate --core-only --regime course --config configs/course-inputs.toml --manifest tests/fixtures/population_course.json --schedule tests/fixtures/schedules_course.json --authoritative tests/fixtures/population_course.json
python -S -m tests.course_analysis_archive
python -S -m tests.course_analysis_archive --worker-audit
```

Course/M4-T01 is done; [M4-T02](../todos/course/M4/M4-T02-course-diagnostics-and-policy-costs.md)
is ready. Progress is eight done, two ready and eleven blocked. Course diagnostics,
costs/rule, uncertainty and complete report/CPU acceptance remain open. M5 CPU
packet preparation is separately ready; model/runtime/headroom, capability, pilot,
resource reconciliation, authorized freeze/main execution and publication remain
later gates. Intended course outcomes remain unknown where records are absent;
the selected scripted scopes establish no empirical 20-world result.

The [completion audit](../../notebooks/validation/course-m4-outcomes/completion-audit.json)
and [exact command](../../notebooks/validation/course-m4-outcomes/completion-audit-command.json)
pass: final statuses/counts, local links/anchors, accepted logs/module provenance,
seven retained scopes and all 1,469 protected starting files, including the
unchanged unstaged M5 edit. Thesis defaults/todos, specification/configuration,
old fixtures and plan Sections 1-10 remain intact. No inference configuration
was frozen, and no model/GPU/pilot/main run or publication occurred.
