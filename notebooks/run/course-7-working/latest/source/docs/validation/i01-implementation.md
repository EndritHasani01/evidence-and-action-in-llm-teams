# I-01 implementation evidence

14 October 2026, Windows Python 3.11.9 development checkout. This document
records focused implementation checks, not an extensive CPU campaign or Kaggle
research acceptance. No model is loaded and no empirical study call is made.

## M0 / M1 checkpoint

Design adoption: `6875aae`. Native fixture maximum 827 and revision
agent 0 row 12 → 100 maximum 780 were recomputed by `recovery.i01.core.oracle`.
The focused development command generated 29 saved worlds, checked the legal
three-call confirmation sequence ends with both submissions, and checked literal
retain and empty clear histories. Those checks passed. Fixed main assignment
contains five worlds in each owner/first-speaker stratum, with paired recovery
seeds and balanced treatment execution order. Actual tokenizer, model capability,
runtime, hardware/headroom and Kaggle operation remain pending.

## Durable design

The old four-peer `WorkerStore` is not used for synthetic I-01 rounds. The small
I-01 registration schema uses the same WAL/FULL transaction discipline. Each
world belongs to one canonical database. Admission is serialized by the one
controller across the explicit two-store inventory; raw replies/failures and
effects are separate transactions, with effects and checkpoint atomic together.
Only stage/gate/session metadata is held in slot 0. Historical DBs are untouched.

The packaged `recovery.i01.checks.run_checks()` passed its focused scripted
development run (receipt: `notebooks/validation/i01-development/scripted-checks.json`).
It checks interruption before raw persistence with one confirmed identical retry,
interruption after raw persistence with idempotent effects, 499/500 admission,
backup exclusion, ZIP and expanded restoration, unknown versus terminal failure,
native fixture mathematics and phase-final/wait/view behavior. The native-tokenizer
portion is not run by this local command and remains the N04 Kaggle prerequisite.
Two integration faults were corrected: explicit SQLite connection closure and
portable backup journal mode, preventing open-handle/sidecar export discrepancies.

## M3 / M4 Python integration

`python -m unittest tests.test_i01_integration -v` covers scripted raw-persistence
interruption and exact resume, phase finality and retention, escaped model HTML,
read-only twenty-world unknown coverage, missing-prerequisite refusal before
admission, restored-envelope refusal, and the retained controller/client command
path. A discovered Windows NumPy import deadlock was diagnosed with a bounded
thread dump and fixed by initializing CPU plotting on the controller main thread.
The retained client test then passed (5.710 seconds); no model was loaded.

The adapter reuses the existing reviewed NF4 loader and fresh-cache/finite-score
engine while binding exact I-01 requests and direct/thinking framing. The online
deployment lock inherits the demonstrated Linux Python 3.13 hash lock and adds
explicit pinned reporting dependencies with hashes from their PyPI releases.
No GPU loading, model qualification, actual envelope, pilot or main action was
executed. Native framing and the candidate deployment lock require Kaggle checks.

The Python interfaces implement host/setup/download, initialization/restore,
self-checks, load-only resident workers, six counted readiness calls, separate
mode screens, selected/reload envelopes, individual pilots, human reviews,
explicit freeze, prepared one/two-world batches, pause, annotations, read-only
analysis, complete reports/figures, snapshots and shutdown. Two-world batches
use one serial child per slot, global admission, and shared quiescent boundaries.

## Initial integration and widget-notebook checks (historical)

The final focused integration suite has six tests (latest run: 19.185 seconds),
including parallel scripted writers and exact fresh-snapshot reconstruction.
The packaged 499/500 check now races two admissions and permits exactly one.
Snapshots stop registration as well as generation/effects across both writers;
their reopened analysis matches live outcomes, costs, traces and gates exactly.
Terminal timeouts preserve observed dispatch time separately from unknown
ready-model time. Load/reload/close records are idempotent, and failed loads
require no fictitious generation. Missing-session spending requires a bound and
affected world IDs; lost prefixes cannot be silently regenerated.

N00–N24 exist in `notebooks/i01_course_kaggle.ipynb`. All 24 code cells compile,
have empty outputs, and pass notebook schema/order checks. Executing the 23
post-bootstrap cells against a rendering-only stub produces 35 control panels
and starts zero actions. The paired-outcome PNG was inspected visually; its
20 unknown main worlds are labelled as unexecuted, not failures. Local Markdown
links and `git diff --check` pass. Sections 1–11 of the scientific specification
compare exactly to baseline `0b0a44a` after newline normalization.

Actual Kaggle widgets/download links, native tokenizer bounds/framing, Linux
installation and T4 process residency/cleanup remain target-host checks. The
prepared GPU readiness/envelope/competence/pilot/freeze/main paths have not been
executed on a pretrained model. All intended I-01 main outcomes remain unknown.

The small source/wheel release review passed outside the checkout: every
installed Python module equals the source manifest, the installed CLI initializes
and reads a twenty-world unknown study with zero attempts, and all 24 code cells
compile/render without research actions. The source ZIP CRC/file inventory passes.
During final real operator testing, a run-directory attribute/method collision
was fixed; `Operator.run` now routes through the retained client/controller.
The seventh focused integration case exercises that actual path through reopen,
status and snapshot with zero model calls. Snapshot creates one fresh archive,
and controller close snapshots after recording model termination.

Final seven-case run: **7 passed, zero failures/errors, 36.048 seconds**;
receipt `notebooks/validation/i01-development/integration-checks.json`.
The source bootstrap was exercised with the exact ZIP, a repeated cell and an
expanded directory using a display stub; scientific actions remain absent.
Installed initialization preserves every source-release member inside the run's
portable source directory. Full synthetic envelope text and native IDs are both
archived. Final archive/native capacity/model checks remain Kaggle-only.

## Ordinary-cell workflow completion (14 October 2026)

The user authorized the ordinary-cell follow-up after rejecting widget forms and
extra stage buttons. Operator checkpoint `a8fa948` and notebook checkpoint
`cbbe200` implement UX-01–UX-04 from the workflow plan. The current notebook has
25 named execution cells and zero widget panels. Running a stage cell performs
its finite action; Run All can execute inference and is explicitly unsupported.
The previous N00–N24/rendering-only receipt above is historical evidence.

Changed behavior: readable tables and concise receipts; automatic pilot/batch
conversation, outcomes/costs and current checkpoint links; failed controller,
gate or export results stop the cell after evidence display. Pilot findings stay
unset until supplied, selected mode/current batch derive from saved state, and
the existing client interrupt requests pause without implying settlement.
Complete private/raw audits remain accessible with `audit_limit=None` and the
HTML/text/JSONL exports. Final/partial reporting works without loading models.

Focused Windows Python 3.11.9 verification: **16 passed, zero failures/errors/
skips, 26.115 seconds**, recorded in `ordinary-cell-checks.json`. Nine changed UI
checks plus seven affected integration cases cover conditional thinking,
derived mode/reload/current batch, actual human findings, escaped conversation
and errors, ordinary stopped-cell behavior, actual controller/status/snapshot,
interrupt pause, unknown populations, exact raw reuse and literal siblings,
parallel quiescence and archive reconstruction. Temporary scripted/fake stores
and controllers made zero actual model calls.

Notebook schema/compile/empty-output checks and 25 independent cell scopes pass
against a recording fake operator. The review checks individual pilot scopes,
unset review defaults, explicit mode/count, freeze notes, archive verification,
ordered closure and the honest Run All metadata. The final release review checks
matching checkout/delivery notebook, source/wheel bytes, ZIP and expanded source
bootstrap/rerun, installed outside-checkout CLI and exact complete-source
preservation in a temporary run. See `release-review.json` for exact package
identity and executed acceptance.

Synthetic output is reviewed using a headless local browser; fixture output is
explicitly labelled as scripted presentation, not model evidence. It shows the
ordinary pilot matrix, exact messages, audit disclosure and current archive/file
links. Actual Kaggle ordinary output updates, interrupt responsiveness and browser
downloads remain unverified.

Specification, scientific configuration/runtime pins, core lifecycle/private
views, fixed schedules, persistence/admission, model inference adapter, analysis
formulas and historical research artifacts are unchanged. No GPU/model inference,
actual qualification, pilot, freeze, main or publication ran. Linux/native/T4
acceptance and all empirical outcomes remain the operator's later execution.

## Reported ensurepip failure and named research steps

The user supplied this Kaggle setup log after environment creation failed:

```text
Error: Command '['/kaggle/temp/i01/i01-venv/bin/python3', '-m', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1.
```

This locates the failure inside default pip bootstrapping, before this setup
action installed the runtime or dispatched model calls. The deeper ensurepip
cause is not present in that log and is not inferred.

The correction reuses earlier accepted bootstrap semantics: create the plain
venv with `--without-pip`; retrieve/verify/install pip 26.2.1 by its exact native
wheel size/SHA256; prove pip's file/prefix belongs to the isolated interpreter.
The wheel is the one in the preserved M5 run-5 build-tool manifest. Scientific
dependency/runtime pins are unchanged. A recognized incomplete isolated venv
can recover without clearing it; unknown or completed mismatching environments
are refused. Logs append and expected subprocess failures expose their actual
last lines through a concise notebook traceback.

Four focused setup checks pass in 10.799 seconds, including real recovery of a
tiny Windows Python 3.11 pip-less environment, correct pinned pip isolation/cache,
corrupt-wheel refusal, preserved existing files and failure logs. Only the 1.8 MB
installer wheel was installed; the full runtime and model weights were not.
One real named `Study` controller/status/blocked-batch/snapshot/reconstruction
case passes in 15.276 seconds with zero model calls. All 25 named cell scopes,
compile/schema/empty outputs and absence of generic UI dispatch pass.

`recovery/i01/notebook.py` exposes the named steps and reuses the existing
operator/controller. The source bootstrap extracts under the existing release
commit label and rejects cached imports from another source until restart;
previous source directories and experiment files are preserved. The upload
package must replace both the old notebook and old source dataset attachment.

Evidence: `setup-repair-checks.json` and the regenerated `release-review.json`.
Actual Kaggle installation after this repair, frontend/interrupt/download,
native/model qualification and empirical execution remain unverified. No GPU
inference, qualification, pilot, freeze or main experiment was run locally.

The [Python venv documentation](https://docs.python.org/3.13/library/venv.html)
explains that `--without-pip` skips the default ensurepip bootstrap. No unpinned
get-pip script or inheritance of the kernel's scientific packages is used.

## Reported Kaggle controller startup incident (14 October 2026)

The operator reported successful runtime installation in 177.780 seconds and
zero model attempts under source 4db263ea25c8, Python 3.13.15 and two distinct
Tesla T4 devices. The next supplied stderr contains a sitecustomize warning for
missing wrapt and a fatal Matplotlib backend error for
module://matplotlib_inline.backend_inline. This identifies inherited notebook
environment settings; it does not establish controller/model acceptance.

The correction strips inherited Python/pip/plotting overrides only in child
environments and selects Agg before import. Authentication/proxies remain
available; scientific/runtime pins, saved source binding, settings, attempt
accounting and old logs remain unchanged. Early exit is detected immediately,
with the current startup's stderr tail and bounded child cleanup. The runbook
provides temporary environment cleanup for the already installed matching
source; upgrading a bound study's source is prohibited.

Opening/inspection without a session window is now supported. The load cell
explicitly records actual session deadline/allowance before loading. Existing
backend load/call checks still reject absent or previous-controller windows,
before physical admission. No quota duration or allowance is inferred.

Fourteen focused checks pass in 22.269 seconds on Windows Python 3.11.9: three
child-environment/startup-failure cases, nine ordinary-interface cases, one real
controller launched under hostile inline/PYTHONPATH/sitecustomize settings with
zero attempts and fresh checkpoint reconstruction, and one scripted missing/
previous-session admission refusal with zero provider calls. Parent environment
and prior logs are preserved. These are lightweight implementation checks;
Kaggle controller attachment, native checks, T4 residency/headroom/competence,
pilot/freeze/main execution and frontend/download acceptance remain pending.

Evidence: controller-startup-checks.json and the regenerated release-review.json
under notebooks/validation/i01-development/. The complete package retains
25 ordinary code cells and an unchanged scientific runtime lock.

Final package review passes for source checkpoint `659c056`: 63 source members,
593,940-byte ZIP, SHA256
ada4a9e9eed09c9325bc120ff70e5bed51979aa2c91dc165189152f1b4f63edc.
The exact older 4db263ea25c8 source attachment was additionally extracted into
a temporary directory; the documented environment-recovery cell reopened its
already initialized study successfully, restored parent environment and made
zero model calls. The matching old attachment is preserved locally. Supplied
venv/controller logs are preserved without staging them as implementation files.
