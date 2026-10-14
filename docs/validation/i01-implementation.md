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

## Final integration and notebook checks

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
