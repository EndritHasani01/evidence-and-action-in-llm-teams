# I-01 course-1: executed-run diagnosis and complete fix proposal

**14 October 2026 — analysis complete; proposed repairs are not implemented by this document.**

Implementation follow-up: the user subsequently requested full repair. All
fourteen items now have implemented responses and focused verification in
[the repair evidence](../validation/i01-course-1-repair.md). The diagnosis and
proposal below remain the original audit record; Kaggle model/experiment
acceptance is still distinct from implementation acceptance.

Reviewed checkout: `E:\Github\recovery_blueprint\recovery_blueprint`,
`feat/smaller-natural-experiment`, HEAD `ebb8c7e9d42d350a50635d3df5e0bcc10d32cf17`.
Executed source: `659c056abfd195a067aa82c99a933aead9a948f5`.
The user's `run/course-1/` is located at
[notebooks/run/course-1/](../../notebooks/run/course-1/) in this checkout.

## 1. Finding and recommended decision

The executed notebook stops in its **Load both T4 workers** cell because the
session configuration is still `SESSION_DEADLINE_UTC = None` and
`SESSION_ALLOWANCE_EVIDENCE = ""`. Its first statement rejects those values;
`study.load_models()` is never reached. This is a correct resource refusal
presented through an inadequate operator flow, rather than evidence of a model,
CUDA, out-of-memory, or inference failure.

The preceding setup, retained-controller attachment, native CPU/tokenizer
self-check, and verified weight retrieval completed. The previous fatal
Matplotlib backend problem is absent in this run. However, the `sitecustomize`
warning for missing `wrapt` remains in the controller and setup logs. The earlier
environment cleanup therefore fixed the fatal backend conflict without proving
complete target-host startup isolation.

Fixing the two configuration values alone removes this particular stop. It does
not address the defects found in the later workflow. Before research execution,
repair the P0/P1 items below, deliver one matching notebook/source/wheel package,
and exercise only the affected lightweight checks. Keep the current run as
evidence. Do not erase it, edit its source binding, manufacture session allowance,
or reinterpret its unknown outcomes as failures.

No code review can guarantee that an unexecuted GPU/model path will never fail.
The objective is to eliminate demonstrated implementation errors, detect
remaining compatibility problems at the right stage, stop safely, preserve
spending/evidence, and provide a precise recovery action. Actual 9B T4 capability,
memory headroom, latency, pilots, and main outcomes remain empirical questions.

## 2. Authority, scope and evidence

[PROJECT_SPECIFICATION.md §12](../../PROJECT_SPECIFICATION.md#12-adopted-i-01-course-regime)
governs scientific behavior. The
[implementation WBS](../plans/i01-course-implementation-wbs.md),
[living handoff](../IMPLEMENTATION_PLAN.md),
[natural notebook workflow](../plans/i01-notebook-natural-workflow.md),
[reviewed I-01 design](silo-bench-course-redesign-review.md), and
[existing implementation evidence](../validation/i01-implementation.md)
provide the relevant engineering and prerequisite context. Historical proposal
settings do not override the adopted specification.

The proposed changes preserve the pinned 9B model/revision, runtime lock,
direct/thinking conditions, private views, literal retain/clear transformation,
fixed inputs/orders/seeds, phase-final submissions, three-call-per-agent bounds,
500 physical attempts, 28 contingency, historical 45 separation, durable raw
output before effects, and twenty intended main worlds. There is no additional
model, new treatment, automatic fallback, scientific resampling, or new status
database. Research logic stays in reusable modules; operator cells remain
ordinary named commands.

### 2.1 Evidence inventory

All six supplied files were inspected without modification. Full input hashes,
archive checks, and seven focused scripted reproductions are recorded in
[course-1-audit-probes.json](../validation/course-1-audit-probes.json).

| Supplied file | Size | What it establishes |
|---|---:|---|
| [notebook-exec.ipynb](../../notebooks/run/course-1/notebook-exec.ipynb) | 165,548 bytes | Executed cells 1–6, exact window error, successful preceding outputs; later cells unexecuted |
| [latest.zip](../../notebooks/run/course-1/latest.zip) | 1,238,884 bytes | Valid self-check-boundary source, receipts, two canonical DB snapshots and reports |
| [worlds.csv](../../notebooks/run/course-1/worlds.csv) | 1,518 bytes | Matches archived CSV byte-for-byte; all twenty main outcomes unknown |
| [conversations.txt](../../notebooks/run/course-1/conversations.txt) | 0 bytes | No recorded agent calls/conversations; consistent with the databases |
| [research report MHTML](<../../notebooks/run/course-1/I-01 research report.mhtml>) | 239,418 bytes | Browser capture of partial evidence, 0/20 known pairs and 0/500 attempts |
| [conversation MHTML](<../../notebooks/run/course-1/I-01 conversations.mhtml>) | 19,827 bytes | Audit inputs/truth without call traces; consistent with no inference |

The notebook has 52 cells, including 25 code cells. Joining each cell's source
lines shows that its source matches the notebook preserved in the archive;
Kaggle's JSON source representation differs, but the executed code does not.
Archived I-01 modules also match the reviewed working-tree files byte-for-byte.
This incident is not explained by an old notebook attachment or an unreviewed
code edit.

The archive contains 113 members, including 112 inventory entries. ZIP CRC,
every inventory size/SHA256, and both SQLite integrity checks pass. Fresh
read-only analysis of copied manifest/DB snapshots equals the archived complete
analysis. Archive SHA256:

```text
b5d2df95fcb1238dfac849af0795a691a36307937691914bf36a6bde92b3f68c
```

### 2.2 Actual progression

Evidence timestamps below are recorded UTC; on this date Budapest is UTC+02:00.
For example, the archive's 18:07:30 UTC is 20:07:30 Budapest time. No provider
allocation duration is inferred from these observations.

| Stage / cell ID | Execution | Observed result |
|---|---:|---|
| `workspace` | 1 | Linux x86_64 Python 3.13.15; two distinct Tesla T4 UUIDs, 15,360 MiB each; scratch about 1,069.91 GiB free and working about 19.5 GiB free |
| `setup` | 2 | Pinned runtime installation, pip check and installed-source inventory accepted; receipt records 179.005697 seconds, zero model attempts |
| `open-study` | 3 | Study `4e0a35fb-2b52-4e06-8303-7dbabdb6a98e` created at 18:07:20.369932 UTC; controller attached |
| `selfcheck` | 4 | Native tokenizer and scripted checks pass at 18:07:28.658012 UTC; input bound 6,885 ≤ 8,192; checkpoint created at 18:07:30.126927 UTC |
| `weights` | 5 | Twelve pinned files verified; native total 19,329,302,519 bytes; zero inference; fetch completed and hashing continued afterward |
| `load` | 6 | `set_session_window(None, "")` raises `ValueError`; no model load |
| `readiness` onward | not executed | No GPU/model qualification, pilot, freeze, main, final report cell, final archive cell or finish-session cell executed in this notebook |

Each canonical DB has zero `calls`, `attempts`, `episodes`, `sessions`, and
`annotations`. Worker 0 stores the passing self-check and last completed action;
there is no session-window record, loaded-session record, qualification,
envelope, freeze, or main scope. Twenty main worlds remain unknown; paired
contrast and intervals are unavailable; missingness bounds are [-1, 1].

The MHTML reports and downloaded CSV come from the automatic self-check export,
not from execution of the final report stage. Empty conversations are expected.
The zero-attempt count applies to this saved boundary and the visible execution;
it is not evidence of provider deallocation or unused GPU quota.

## 3. Exact immediate failure and present-session recovery

The call chain is:

```text
notebook cell "load" (execution_count=6)
  → Study.set_session_window(None, "")
  → Operator.run("window")
  → Operator.set_window()
  → type / nonempty-evidence validation fails
```

See [named notebook API](../../recovery/i01/notebook.py),
[window validation](../../recovery/i01/ui.py), and
[generated cell design](../../scripts/build_i01_course_notebook.py).
No controller action or inference admission occurs for this failed call.

Three usability choices explain why this recurred:

1. The initial workspace cell mixes source/bootstrap configuration with required
   later-session facts, leaves those facts unset, and proceeds through a long
   successful setup/download sequence without a visible pending-window summary.
2. The load cell combines configuring the window and loading models. Its title
   suggests a model action while its actual first failure is configuration.
3. Rerunning the workspace cell resets both facts to their defaults while it
   retains an existing `study` object. Rerunning the load cell then tries to
   replace even a previously valid window with `None`/empty evidence.

For an intact, still-active controller from this exact run, fill the two globals
with the **current** provider facts, then execute these existing commands:

```python
# First assign SESSION_DEADLINE_UTC to the actual future deadline with UTC offset.
# Assign SESSION_ALLOWANCE_EVIDENCE to actual current Kaggle allowance evidence.
study.set_session_window(SESSION_DEADLINE_UTC, SESSION_ALLOWANCE_EVIDENCE)
study.show_status()
study.save_checkpoint(verify=True)
```

This records the window and creates a fresh zero-generation checkpoint including
the weight receipt copied into the study after download. It is preparation, not
model acceptance. In this proposal's scope, loading/inference is left for the
operator after the implementation defects are repaired.

If the controller exited but files remain intact, use the matching `659c056…`
source and `START_MODE = "reopen"`; prepare/install the same runtime as needed,
reopen the study, and record fresh session facts. Do not create a second owner
while the old controller is alive. If restoring the supplied archive in another
session, select it explicitly, use a fresh destination and the matching source,
and record whether it is the latest safe boundary or an uncertain earlier tail.
Reuse/verify cached weights when present. The saved ZIP excludes weights by
design and predates their successful retrieval; it cannot prove that a new
Kaggle session has those files.

Do not reuse the earlier conversation's example deadline or illustrative quota.
Do not bypass the clock check with an arbitrary far-future time. Current
configured bounds require approximately 730 seconds remaining before each
bounded load plus cleanup/export; new direct and thinking admissions require
more than 310 and 1,030 seconds respectively. Those values derive from the
configured operation bound, two five-second cleanup graces and 120-second export
reserve. They are not claims about the account's actual allowance, or promises
that a whole study fits.

## 4. Findings and repair priorities

**Observed** means present in supplied run evidence. **Reproduced** means a
temporary scripted fixture reached the behavior in current production code.
**Source-confirmed risk** means an identified code path, not a failed Kaggle
model stage. **Policy clarification** requires an explicit interpretation of an
existing gate rather than silently adding a scientific criterion.

| ID | Priority | Finding | Evidence class |
|---|---|---|---|
| F01 | P1 | Missing session facts produce a late, confusing load-cell traceback | Observed |
| F02 | P1 | Startup hook still executes despite environment cleanup and some `-I` launches | Observed; exact hook origin unavailable |
| F03 | P0 | Reopening can recreate a missing canonical DB and forget spending/evidence | Reproduced |
| F04 | P1 | Repeated same-controller replacement can reuse a previous reload envelope | Reproduced |
| F05 | P1 | Correct original-input controls receive false wrong-submission labels | Reproduced |
| F06 | P1 | Failure of the second main future does not promptly pause new admissions | Reproduced |
| F07 | P1 | Dead workers can appear resident; inspection fails when its controller exited | Two reproductions |
| F08 | P1 | Latest archive predates successful weight retrieval and the window error | Observed plus source-confirmed failure-reporting gap |
| F09 | P1 | Periodic checkpoint logic applies to collaborative episodes but omits controls/diagnostics | Source-confirmed risk |
| F10 | P1 | Explicit verified snapshot is not passed to the actual model loader | Source-confirmed integration risk |
| F11 | P2 | Cached setup receipt is accepted without a fresh inventory at setup reuse | Source-confirmed risk; load already has a later inventory guard |
| F12 | P1 | Notebook scope checks accept unset configuration without exercising real validation | Source-confirmed coverage gap |
| F13 | P1 | `ABA_equal` can be false while readiness is reported passed | Reproduced; gate-policy clarification |
| F14 | P2 | Blank conversations, bulky receipt displays and terminal batch behavior obscure progress | Observed / source-confirmed UX gaps |

### F01 — Make session configuration an explicit ordinary stage

Split the current load cell into **Record this session's actual allowance** and
**Load both T4 workers**. Place the small configuration beside its setter rather
than inside the source-extraction cell. Display a concise window state from the
first workspace inspection: preparation permitted, model loading pending actual
facts. Keep setup, self-check, and verified retrieval independently executable.

The session cell should offer one default ordinary-code route using an actual
remaining duration observed in the Kaggle UI and evidence. A small named module
helper may convert that observed duration to an aware UTC deadline and record
the observation time. Retain the existing absolute-deadline command as the
explicit alternative. Require exactly one source of deadline information,
finite positive duration if used, nonempty real evidence, and sufficient margin.
There is no reviewed provider-deadline API in this repository to substitute for
operator evidence; do not invent an automatic provider reading.

Do not make each cell rerun add the same duration to a later clock time. Reuse
the recorded deadline for the current controller, show its decreasing remainder,
and require an explicit fresh observation for a change. A new controller must
never inherit an old window automatically. Workspace reruns must preserve
operator inputs and not overwrite the authoritative current window.

Expected missing/expired facts should raise a concise operational exception
showing which field is missing, that no model was loaded/admitted, and the exact
named correction command. Retain the real validation and stop the cell. Do not
return a success-shaped payload for invalid facts.

**Affected files:** `notebook.py`, `ui.py`, `workflow.py` if the duration helper
belongs there, notebook builder, verifier, runbook. **Acceptance:** default
preparation succeeds with zero model calls; missing facts stop before load;
valid observed facts lead to a fake resident loader; expired/stale windows still
refuse; workspace/load reruns neither reset nor extend a recorded window.

### F02 — Diagnose the remaining host hook instead of assuming isolation

Eight archived logs contain `ModuleNotFoundError: No module named 'wrapt'`:
controller startup, verified pip bootstrap, pip isolation, dependencies, project,
pip check, installed inventory, and metadata retrieval. The venv-creation log
does not. The bootstrap/probe commands use `-I`, so adding that flag alone cannot
honestly be promised to remove this particular warning.

Python processes site configuration separately from environment variables.
`-I` excludes unsafe current/user paths and ignores `PYTHON*`, while `-S` disables
site processing; `.pth` entries and `sitecustomize` are distinct startup paths.
[Python 3.13 site documentation](https://docs.python.org/3.13/library/site.html),
[Python interpreter options](https://docs.python.org/3.13/using/cmdline.html).

Add one bounded zero-generation startup diagnostic in the isolated interpreter:
capture `sys.executable`, prefix/base prefix, startup flags, cwd, `sys.path`,
resolved hook origin, relevant `.pth` paths, and the complete hook traceback.
Use an allowlist of diagnostic environment names; never print HF credentials or
proxy secrets. Compare ordinary and isolated startup from a neutral directory.
Store the result under existing setup receipts and carry it into checkpoints.

Use the existing sanitized environment consistently for setup, metadata,
weights, controller and resident children. For installed-runtime commands,
prefer `-I -X utf8` plus a neutral cwd after proving imports resolve to the
installed wheel; do not depend on checkout cwd to make package imports pass.
Continue selecting `MPLBACKEND=Agg` before import in the controller and plotting
process. The backend variable selects Matplotlib's renderer.
[Matplotlib environment documentation](https://matplotlib.org/stable/install/environment_variables_faq.html).

Resolve the hook according to its measured origin: exclude an unintended
current/user path; remove an unapproved path injection only from a verified
isolated environment; or, if it comes from retained host startup machinery,
implement a narrowly scoped launcher only after proving that native venv
prefixes, dependency imports and multiprocessing spawn are preserved. A blanket
`-S` change is unsuitable because it also changes dependency discovery. If a
retained host hook cannot yet be isolated safely, stop with its exact origin
and required repair instead of concealing the warning or marking isolation
accepted. Do not install `wrapt` blindly, loosen dependency pins, delete host
files, or monkeypatch scientific inference.

**Acceptance:** a real installed subprocess starts from outside the source tree
under hostile notebook settings; parent environment stays unchanged; no
unapproved hook executes; all dependency/source checks pass; both spawned
worker entry points import correctly without loading models. The target hook
origin and Linux behavior need Kaggle evidence; the Windows PYTHONPATH fixture
does not establish those facts.

### F03 — Refuse missing or incomplete canonical databases

[Session opening](../../recovery/i01/workflow.py) constructs writable `Store`s;
[Store construction](../../recovery/i01/store.py) opens SQLite in create mode,
creates tables and binds a new store. A fixture with one recorded attempt in
worker 1, followed by moving that fixture DB aside, reopened successfully,
created an empty worker 1 DB and reported zero attempts. The original fixture DB
was retained; no supplied run file was moved. This can violate both exact resume
and the whole-study ceiling after actual data loss.

Before acquiring writable stores for an existing run, require the manifest,
both explicitly named DBs, required tables/schema/binding and readable integrity.
Open existing DBs with SQLite `mode=rw`, not create mode. Schema creation belongs
only to explicit fresh initialization. Missing tables or metadata must not be
silently repaired into an empty ledger. Release partially acquired connections
and ownership if validation fails.

Make fresh initialization complete before publishing its run manifest, using a
small staging directory or equivalent explicit completion boundary. This avoids
having to interpret interrupted initialization as permission to recreate stores
for an established experiment. Reuse existing identity/binding records.

Recovery is a verified complete checkpoint into a fresh destination, or explicit
unknown-spending/evidence handling; it is never inferred zero. Preserve missing
world outcomes and prevent regeneration of lost prefixes. **Acceptance:** either
missing DB, missing ledger table, corrupt DB or binding mismatch refuses before
any creation/admission; the existing good files stay byte-for-byte unchanged;
fresh initialization and exact verified restore still work.

### F04 — Bind reload probes to the actual replica load records

`Session.envelope()` uses `/reload-<controller-session-id>` for both probe IDs.
Two separate replacements inside the same controller therefore have identical
requests/IDs. The second replacement reuses durable old outcomes through the
normal exact-resume path, reports `passed=True`, and clears `reload_required`
without new probes. The scripted reproduction produced **zero** new provider
calls instead of the required two. Exact reply reuse is correct for a completed
logical call; identifying a new replica check as that same call is the defect.

Use the existing per-worker successful load-record IDs to bind the envelope to
the currently loaded pair. A replacement gets a new load ID even if controller
session and physical UUID are unchanged. New load pairs require distinct probe
calls, charged to contingency; rerunning the same accepted pair reuses its
recorded probes with zero generation. Include mode/runtime and current load
references in the receipt; `qualified()` verifies those references. No separate
generation counter or parallel store is needed.

**Acceptance:** initial envelope uses two hardware first attempts; first and
second replacements each use two new contingency probes; unchanged-pair reruns
use zero; interrupted probes use exact persisted outcomes and at most the
already approved eligible retry. Insufficient contingency refuses before
dispatch. A frozen mode cannot change.

### F05 — Select the correct truth for failure annotations

[Failure analysis](../../recovery/i01/report.py) chooses original truth only for
`phase == "prefix"`, and revised truth for every other episode. That includes
`control-original-direct` and `control-original-thinking`. A correct original
control submitting 950 is correctly scored 1 by the control evaluator, but the
failure audit compares it to revised truth 921 and labels `wrong_submission`.

Resolve the episode type/input phase explicitly: prefix and original control
use original truth; retain, clear and revised control use revised truth. Keep
single-control and two-agent submissions separate. Recovery-only labels such
as obsolete-value repetition stay restricted to recovery phases. Unknown or
unsupported episode identity must be reported explicitly, not defaulted to a
truth population.

**Acceptance:** correct original/revised controls in both modes have no false
wrong-submission label; actual wrong controls retain it; team/recovery labels,
unknown states, paired estimates, and intended populations remain unchanged.
Rebuild reports from canonical raw evidence; never alter model submissions.

### F06 — Notice either main worker's failure promptly

`Session.main()` waits for futures in submission order. A quickly failed second
world is not observed while the first world's future remains active. In the
scripted fixture, the second failure occurred but `pause` remained false until
the first world completed. Further calls can continue during that interval.

Process results in completion order (`as_completed`) or set the shared pause
flag in a completion callback. On the first failure, stop new admissions and
retain the prepared batch scope. Let already admitted calls settle and persist
their outcomes/effects; do not declare them cancelled merely because a future
or notebook wait was cancelled. Collect both outcomes before producing the
quiescent checkpoint. No automatic new batch or retry.

**Acceptance:** a failure on either slot prevents the healthy slot's next
admission while its already admitted work settles; the unchanged saved batch
resumes completed calls without generation and preserves failed/unknown states.

### F07 — Keep status and inspection useful after process loss

`Session.status()` reports a resident model if its process object exists,
without checking liveness. A dead-process fixture therefore displayed resident
true. Separately, `Operator.inspect()` reconstructs canonical saved records,
then calls the live controller for status; an exited client aborts inspection
although read-only analysis still works. This contradicts the error message
promising saved evidence through `study.inspect()`.

Derive resident state from liveness and termination confirmation. Distinguish
loaded/alive, absent/confirmed exited, and exit unconfirmed; an old load report
does not establish current residency. Render saved analysis and conversations
even if transport status is unavailable. Label current session/worker state
unavailable and show the existing log and exact reopen recipe. Do not start a
replacement or load models during inspection. Apply the same rule to offline
reporting when a stale client handle exists.

**Acceptance:** dead workers cannot appear resident; controller loss still
allows complete saved conversations, costs and downloads; unknown termination
does not permit replacement. Inspection never admits a call.

### F08 — Make archive freshness and operational errors durable

The supplied latest ZIP is explicitly `action/selfcheck`; it precedes successful
weights retrieval and has no `weights.json` or weight-command log. The local
window error never reaches `Session.run_action()`, so it also has no durable
controller-stage receipt. Showing the old ZIP after those actions is valid, but
it should not look like a checkpoint of the latest attempted stage.

After successful zero-generation setup/download/window changes, create an
explicit checkpoint at a quiescent boundary and show its action/time. For local
operational failures, record the requested stage, failure type/cause, source,
observation time, attempt count when known and remedy under existing receipts.
Save full traceback for unexpected defects while presenting concise expected
errors. Best-effort failure export must not overwrite or obscure the original
failure, and it must not snapshot active generators.

Display both the last valid archive boundary and the newest unsaved receipt.
Preserve the last good ZIP on export failure. Do not announce a newer checkpoint
unless export actually succeeds. Weight files and credentials stay excluded;
only their verification/progress receipts are included. Report process/session
closure evidence without claiming provider deallocation.

**Acceptance:** the post-weight/window checkpoint contains their receipts; a
bad-window receipt is recoverable; a failed export retains the prior SHA256 and
shows the failed boundary; no inferred zero spending or implicit model call.

### F09 — Apply the checkpoint interval across long control stages

The five-minute `checkpoint_seconds` check exists in `Session.episode()`, after
committed effects. `control()`, readiness and envelope do not perform that
periodic-boundary check. Twelve thinking controls can therefore leave an old
downloadable archive throughout a long qualification action even though each
raw reply is durable in the live DB.

Use one small existing-session helper to check elapsed time after **settled**
control/diagnostic/episode calls and create a quiescent checkpoint when due.
Keep stage-end and per-world exports. Do not call it while the current call is
still in `active_calls`, which would deadlock waiting for itself. A wall-clock
timer cannot guarantee a five-minute archive during a single 900-second call;
state the guarantee as the next safe settled boundary after the interval.

**Acceptance:** a synthetic expired interval produces a checkpoint after a
control or diagnostic; no checkpoint occurs during its active call; concurrent
writers quiesce, complete outcomes reconstruct exactly, and failure preserves
the last valid archive. No new scheduler or background model execution.

### F10 — Load the exact snapshot already verified

`Session.load()` loads its controller tokenizer from the explicit snapshot.
`recovery/i01/inference.py:ModelFactory` stores that snapshot argument but invokes
the reviewed loader using the Hub model ID/revision instead. Offline cache
lookup will often resolve the same files, but the verified argument is not the
actual loader boundary. A relocated valid snapshot can fail unnecessarily, or
the controller and worker can resolve different locations.

Extend the reviewed loader narrowly with an optional verified local directory,
keeping existing thesis/course defaults. Pass the same selected snapshot to
both model and worker tokenizer with local-only loading. Preserve all current
NF4/double/FP16, attention, tensor/load audit, no-offload and fresh-cache logic.
Record the native snapshot/revision receipt in load evidence; refuse mismatch
before any generation. Do not replace the loader or serving stack.

Local-directory loading and local-only options are supported API concepts;
their behavior must still be checked against the actual pinned 5.12.0 package,
not assumed from the latest documentation.
[Transformers model-loading reference](https://huggingface.co/docs/transformers/main/en/main_classes/model).
Hub cache files remain verified immutable inputs; avoid editing them while
reusing pinned revision downloads.
[Hub download/cache documentation](https://huggingface.co/docs/huggingface_hub/main/en/guides/download).

**Acceptance:** a lightweight loader spy confirms one explicit path for both
replicas and tokenizers; moved-cache path and source mismatch behave correctly;
no network fallback or GPU work in the check. Actual native T4 load remains an
operator stage with unchanged scientific settings.

### F11 — Revalidate cached environments without reinstalling them

`install()` returns an existing matching environment receipt without checking
actual installed packages/source again. `Session.load()` already checks the
inventory before model loading, so this is a late-error risk rather than an
unprotected generation path. A missing or modified package may fail metadata
work first with less useful context.

Reuse the existing bounded inventory command when accepting a cached receipt,
plus interpreter/pip isolation checks appropriate to that path. Diagnose any
binary import compatibility needed before large retrieval in a disposable CPU
process with GPU visibility disabled; do not initialize CUDA in setup or add an
uncounted warmup. Require only checks affected by this incident. Refuse a
mismatching completed environment and give a preserved/fresh-environment route;
no in-place upgrades to a study-bound or frozen runtime.

**Acceptance:** matching cached setup reuses bytes without reinstalling; missing
or modified packages/source produce an early receipt; existing logs/artifacts
remain; runtime pins and default thesis behavior are unchanged.

### F12 — Check real stage behavior as well as notebook call names

The release verifier's recording stub accepts every named method and records
`set_session_window(None, "")` as a successful scope check. It verifies routing,
cell order and empty outputs; it cannot establish usable configuration behavior.
The real-controller integration test exercises opening/status/snapshot/window,
but not the normal configured sequence reaching a fake model loader. Those
checks are useful and their claims should stay limited to what they execute.

Retain the scope verifier and add one lightweight integrated ordinary-cell
scenario using the real `Study` window/error path and a fake resident loader:
default preparation, missing facts, actual-shaped valid facts, load rerun,
workspace rerun, controller restart, and read-only inspection after exit. Assert
that no skipped prerequisite launches work, no deadline is silently extended,
and no model-call counter changes. Exercise the installed wheel from outside the
checkout with the same entry flags/cwd used on Kaggle. Add targeted regressions
for F03–F10; reuse unchanged mathematical/protocol evidence.

**Acceptance:** documentation separates source scope checks, integrated scripted
behavior and actual-host/model evidence. No new broad CPU verification campaign,
download of models for testing, or model qualification masquerading as a check.

### F13 — Make A/B/A readiness interpretation explicit

The scripted fixture returned unequal A1/A2 token sequences on both slots while
finite/cache metadata passed. `readiness()` recorded `ABA_equal=[False, False]`
and `passed=True`; equality is calculated but excluded from the pass expression.
The operator presentation does not make that discrepancy prominent.

The approved design calls for six A/B/A state checks and isolation; it does not
spell out every token-equality acceptance rule. Establish whether equality is a
required readiness criterion or a diagnostic alongside fresh-cache checks. If
required, enforce it using those same six calls. If diagnostic, display both
results, document the accepted interpretation and require explicit resolution
of unexpected discrepancies before treating isolation as established. Do not
silently add repeated samples, different seeds, deterministic kernels or new
decoding settings to obtain equality.

Identical seeds alone do not guarantee identical outputs across runtimes/devices;
numerical nondeterminism and stale state need to be distinguished.
[Pinned-generation PyTorch 2.11 reproducibility guidance](https://docs.pytorch.org/docs/2.11/notes/randomness.html).
This finding is a gate-policy omission, not proof that the supplied model leaked
state: the supplied run executed no A/B/A model calls.

**Acceptance:** passing/unequal cases expose the declared decision clearly,
without extra calls or changing scientific assumptions. Preserve raw requests,
tokens and cache/finite-score diagnostics for every probe.

### F14 — Make empty, partial and complete states readable

Add a short header to empty conversation exports explaining that no calls are
recorded, with study identity, boundary and coverage. A blank file currently
looks broken despite being correct. Distinguish zero observed spending from
unknown unexecuted outcomes. Show compact archive boundary/time/SHA256 in normal
output, with full inventories inside the downloadable archive; avoid repeating
the entire source inventory and native chat template after every cell.

When no main worlds remain, persist or explicitly return a terminal batch state
that the named run/review methods understand. `prepare_batch()` currently returns
`main-complete` without replacing the previous batch metadata, so later cells
can keep presenting the last completed batch. This is a progress/interaction
problem, not permission to add worlds. Keep useful conversations and all raw
audits downloadable; ordinary cells must not launch later stages automatically.
Show study identity, writable destination and whether opening created a new
study or attached existing matching files. Restore into an explicit fresh path
using the existing `Study(..., run=...)` parameter when the default destination
is occupied; do not replace its files or guess a checkpoint by timestamp.

**Acceptance:** the zero-call case explains itself; partial reports retain 20
unknowns; the final prepared state cannot request another main world; completed
batch reruns use zero model calls and show current overall coverage.

## 5. Natural operator progression after repair

The regenerated notebook should follow this ordinary-cell sequence:

```text
workspace/source inventory → install/reuse pinned runtime → open/reopen/restore
→ native implementation check → verified weight retrieval
→ record actual session window → load both resident replicas
→ six readiness calls → twelve direct controls → inspect qualification
→ conditional thinking controls only when permitted → selected-mode envelope
→ pilot 1 → inspect/download/review
→ pilot 2 → inspect/download/review
→ pilot 3 → inspect/download/review
→ inspect measured forecast/configuration → explicit freeze/download
→ prepare fixed main batch → run/resume that batch → inspect/download/acknowledge
→ repeat the fixed batch loop only by operator choice
→ final/partial report → verify/export archive → close processes → stop provider
```

The window is the one additional explicit stage. Routine mode, saved batch,
world IDs, receipts and progress derive from canonical records. Human pilot
findings and allowance evidence remain actual human inputs. There are no widget
forms, action menus, global arming flags, or hidden run-all dispatcher. Load,
inspection and reporting preserve weights while the controller is healthy.
Recovery commands remain in an appendix and have explicit ordinary-call forms.

Before every expensive stage show its scope, prerequisites, current attempt and
contingency remainder, session margin, and last safe archive. For sequential
two-replica loading, check the remaining margin again before the second load.
Label the existing whole-main forecast as a conservative serial bound; do not
quietly halve it because there are two T4s. Any improved parallel forecast must
use the fixed per-slot schedule and observed costs, retain cleanup/export
reserves, and be reviewed as a resource-admission change before relying on it.

## 6. Failure handling and recovery contract

| Trigger | Required behavior | Permitted recovery |
|---|---|---|
| Missing/expired window | No model load or admission; concise receipt and existing evidence | Record actual current facts; rerun only that preparation stage |
| Incompatible host/runtime or unresolved startup hook | Stop before weight/model work where detectable; preserve origin/version/log evidence | Correct a scoped environment issue or prepare a fresh matching package/runtime; no automatic unpinned upgrades |
| Interrupted pinned download | Preserve partial verified native bytes; bounded transport retry and progress | Resume identical revision download; no attempt-ledger forgiveness needed |
| Load failure or wrong physical UUID | Preserve load-only elapsed/termination evidence; close both partial replicas within bounds | Explicit compatible reload after confirmed exit; no inference attempt fabricated for a load |
| Wrong/malformed/truncated action | Persist raw result; consume the declared attempt and turn; preserve exact scoring | Continue only the remaining legal phase; never retry the answer |
| Known generation timeout | Persist terminal failure before termination acknowledgement; spend attempt/turn | Confirm exit, explicitly reload, obtain new required envelope evidence, resume remaining scope; never regenerate the timed-out call |
| Infrastructure loss without durable output | Preserve admission as spent/unresolved until confirmed termination | At most one identical permitted retry, charged to contingency; no changed request/settings/seed |
| Controller/kernel loss | Stop descendants through existing ownership/sentinel mechanism; preserve canonical records | Confirm old owner exit; exact matching-source reopen/restore and fresh actual window/load evidence |
| Missing/corrupt DB or unknown tail spending | Refuse new writers/admission; unknown is not zero | Verified complete checkpoint in a fresh destination, or explicit bounded/unknown evidence handling; do not regenerate lost worlds |
| Snapshot/report failure | Preserve last valid archive and original action error | Repair output/storage issue, wait for quiescence, export again; reporting performs no inference |
| Finished main population | No extra worlds or attempts; report all intended coverage | Read-only report/export and session closure |

Preserve the distinction between model residency, confirmed process termination,
observed elapsed allocation, and provider deallocation. Notebook interruption is
a pause request, not immediate proof that all children are dead. Resource refusal
or an honest scientific gate failure should produce a useful stopped state,
not a cascade of unrelated exceptions or an automatic retry.

## 7. Implementation sequence and concrete deliverables

All items here are proposed work. Keep changes small and make a clean commit at
each logical checkpoint. Do not package an uncommitted mixture under an older
release label.

| Checkpoint | Changes | Deliverable and acceptance |
|---|---|---|
| C1 — operator/session correctness | F01, F07, F08, F14 | Named window stage, concise operational errors, truthful status, independent saved inspection, fresh setup/window archives, clear zero/complete output; real ordinary-cell scenario passes |
| C2 — canonical recovery protection | F03, F04, F06, F09 | Existing DBs opened without create semantics, atomic fresh initialization, load-record-bound envelopes, immediate cross-slot pause and settled-boundary exports; targeted scripted counterexamples repaired |
| C3 — inference/environment/report correctness | F02, F05, F10, F11, F13 | Actual hook-origin diagnostic and scoped launcher decision, correct control truth, explicit local snapshot, cached inventory recheck and declared readiness policy; no dependency/scientific changes smuggled in |
| C4 — coherent complete delivery | F12 and all integration | Regenerated notebook, complete wheel/source ZIP, runbook, WBS/handoff and focused receipts agree; installed outside-cwd entry points and ZIP/expanded restore paths pass; old packet preserved |
| C5 — later operator Kaggle acceptance | Target-only behavior | Preparation/startup receipt, actual native T4 loads, original bounded readiness/qualification/envelope/pilots, explicit freeze, incremental main, report/export/restore/closure; each stage remains separate |

Implementation targets are existing `recovery/i01/` modules, narrowly extended
`recovery/inference.py` loading support if necessary, the two notebook/release
builders and verifier, focused existing tests, runbook, and the living handoff.
Reuse existing SQLite metadata, successful load IDs, receipts and archive
primitives. A new server, execution framework, database, migration subsystem or
parallel scientific ledger is unnecessary.

Generate a new source package only after code and focused checks are committed,
then record package identity/verification in a receipt-only checkpoint. Preserve
the currently used `659c056…` packet and all course-1 evidence for exact restore.
An existing study intentionally rejects changed source; do not rewrite its
manifest/source binding to make a patched wheel look identical. For this saved
zero-inference run, the simplest post-repair experiment route is a clearly
identified fresh study with the same adopted fixed design/seed and the original
zero-call preparation archived separately. If any later unseen inference exists,
its evidence/spending must be reconciled first; the older snapshot is not proof
of a globally zero tail. This proposal does not introduce a migration exception
for populated or frozen studies.

## 8. Focused verification and remaining Kaggle acceptance

The audit executed seven small scripted reproductions, not a broad CPU suite.
No production code was changed. Fixture attempts are temporary SQLite test
records, not real model calls or additions to the saved study's ledger.

| Probe | Current observed behavior | Required repair result |
|---|---|---|
| Missing canonical worker DB after one fixture attempt | Reopen creates an empty DB and reports 0 attempts | Refuse before creation; preserved ledger remains authoritative |
| Second same-controller replica reload | Gate passes with 0 new scripted calls | Two fresh contingency probes bound to new successful loads |
| Correct original control | Correct score 1 but `wrong_submission` label | Correct score 1 with no false failure label |
| Failure in second main future | Pause false while first future still running | Stop new admissions promptly on either failure |
| Dead process object | Resident reported true | Truthful dead/unconfirmed state |
| Saved inspection after controller exit | Raises transport error despite available canonical analysis | Complete saved inspection without restarting workers |
| Unequal A/B/A replies | `passed=True`, both equality flags false | Explicit declared readiness interpretation; no hidden criterion or extra samples |

Add these focused regression cases during repair, plus one ordinary-cell flow,
one expired/stale-window case, one safe periodic-control checkpoint case, and
one loader-path spy. Reuse existing raw-before-effects/replay, private-view,
500/28 admission, native-token capacity, ZIP/expanded restore and paired-analysis
evidence unless changed code affects those guarantees. Do not repeat an entire
legacy CPU campaign or run GPU inference during implementation preparation.

On Kaggle, first validate the repaired zero-generation preparation and exact
hook-origin/entry-point behavior. Reuse the already demonstrated native check
where its inputs/affected code remain applicable. Subsequent actual loading,
six readiness calls, twelve direct controls, conditional twelve thinking
controls when permitted, two full envelopes, three individual pilots, freeze
and fixed main batches remain distinct later operator executions. Every new
diagnostic/reload/retry stays within the original 500/28 allocation; failed
hardware/model gates produce partial evidence rather than extra candidates or
undocumented qualification attempts.

Target-only uncertainties remain: native Torch/CUDA/bitsandbytes/attention
compatibility, actual 9B replica loading, headroom at the declared full envelope,
finite/fresh generation and framing, direct/thinking competence and latency,
useful pilot communication, notebook interrupt/download behavior during real
work, restored-session load/reload behavior and provider quota availability.
The notebook/archive from this run cannot settle them. Each should have one
clear next stage, bounded failure path and evidence export, rather than a
promise that no future operational or scientific gate can fail.

## 9. Audit completion and preservation

Observed preparation/controller/native-self-check acceptance is established for
this course-1 evidence. Archive integrity and fresh read-only reconstruction are
verified locally. F03–F07 and the F13 readiness omission are demonstrated by
focused fixtures; other proposed mitigations retain their stated evidence class.
Research outcomes remain unknown. The six supplied run files and preexisting
root logs are preserved; no GPU inference, actual qualification, pilot, freeze,
main, model download or runtime upgrade occurred during this audit.

The proposal is complete enough to implement in the checkpoints above. Its
repairs are pending. The WBS and handoff should link this audit and distinguish
the newly observed target-host preparation evidence from the open correctness
repairs and unexecuted research stages.
