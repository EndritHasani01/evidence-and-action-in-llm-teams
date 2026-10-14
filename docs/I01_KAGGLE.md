# I-01 Kaggle: ordinary notebook cells

Press **Run** to perform the cell's named stage. No widget forms or extra action
buttons. Named research methods such as **study.install_runtime()** and
**study.run_pilot(1)** replace string UI dispatch. Run **one stage cell at a time**. **Run All / Save & Run All can execute
inference and multiple stages and is not a supported study execution method.**

This is implementation delivery, not empirical acceptance. The operator reported
successful Kaggle runtime installation; native framing/capacity, T4 residency/cleanup, headroom, competence,
pilots, freeze and main results still need operator execution. No model/GPU
inference or experiment was run during this redesign.

## Recovering the reported ensurepip setup failure

The reported failure was inside Python's default pip bootstrap, before dependency
installation/model loading. Setup now creates the isolated venv with
--without-pip and installs the same verified pip 26.2.1 wheel used by the earlier
accepted Kaggle bootstrap. Scientific/runtime dependency pins are unchanged.

Replace **both the notebook and its source dataset attachment** with the current
delivery, then **restart the notebook kernel**. Run the workspace cell followed
by **study.install_runtime()**. The existing incomplete isolated venv is recovered
without clearing it; previous failure logs and study files are preserved. An
unknown/non-isolated directory or completed mismatching environment is refused.

Source is extracted into a commit-labelled cache directory, so a new release
does not overwrite old source. Cached imports from another release explicitly
require a kernel restart. If multiple source attachments remain, select the exact
current SOURCE_BUNDLE rather than guessing.

Expected subprocess failures now show the actual last log lines and the full log
path instead of an uninformative dispatcher traceback. The full logs append
across attempts. A failed setup does not create model calls or authorize any
later stage. This repair passed a tiny Windows environment test. The operator
subsequently reported Kaggle setup completion in 177.780 seconds with zero model
attempts; controller startup then exposed a separate environment conflict.

## Recovering the reported controller startup failure

The supplied log shows the child inheriting Kaggle's inline MPLBACKEND and a
Python startup hook that imports unavailable wrapt. Matplotlib fails during
import, before the old controller can select Agg. Current subprocesses remove
inherited Python/pip/plotting overrides, retain authentication/proxy settings,
and select Agg before import. Dependency pins are unchanged. An exited child is
detected promptly; startup failures display the new stderr tail, preserve older
logs and confirm bounded process cleanup.

For the already installed 4db263ea25c8 source and intact study, run this recovery
cell after the failed controller has exited. It temporarily cleans the spawn
environment and reopens the same scientific binding; no reinstall is needed:

```python
import os
from unittest.mock import patch

controller_env = {k: v for k, v in os.environ.items()
                  if not k.startswith(("PYTHON", "PIP_", "VIRTUAL_ENV", "MPL"))}
controller_env.update(MPLBACKEND="Agg", PYTHONNOUSERSITE="1",
                      PYTHONUTF8="1", PYTHONUNBUFFERED="1")
with patch.dict(os.environ, controller_env, clear=True):
    study.open("reopen", deadline=SESSION_DEADLINE_UTC,
               allowance_evidence=SESSION_ALLOWANCE_EVIDENCE)
```

The parent environment is restored afterward. For subsequent old-release
metadata/weight subprocesses, use the same temporary context if needed.
Keep the actual configured deadline future and allowance evidence nonempty for
this old API. Then continue with Check the implementation. Do not substitute a
new source release into an existing bound study. Retain its matching attachment
for later restore. The permanent fix is included in the new notebook/source
package for a fresh study; an older package copy is kept under
dist/i01-course-4db263ea25c8.

Current study opening/inspection requires no session window. Before loading,
the ordinary load cell records the actual session deadline/allowance. Backend
checks still reject missing/stale windows before model loading or admitting
generation; the 500-attempt ceiling and export reserve are unchanged.

## First execution

1. Upload **dist/i01-course/i01-source.zip** as a **private Kaggle dataset** and
   attach it. Kaggle may expose the ZIP or expanded files; both work.
2. Upload **notebooks/i01_course_kaggle.ipynb**, also copied into dist/i01-course.
   Select **GPU T4 ×2**, enable **Internet**, and keep the study private.
3. In **Configure and inspect the workspace**, supply SESSION_DEADLINE_UTC as
   the actual future ISO time with UTC offset, and SESSION_ALLOWANCE_EVIDENCE
   from the current Kaggle UI before loading models. Opening and inspection can
   proceed while these facts are unset. Leave START_MODE = "new" for a fresh study.
   Source selection is automatic only when one verified candidate exists;
   otherwise set SOURCE_BUNDLE exactly.
4. Run **Install the pinned runtime**, then **Open the study**. The reviewed
   Linux x86_64 Python 3.13 candidate is installed in a separate environment;
   the kernel's Torch stack is not replaced. Actual incompatibility stops.
   Setup/download logs are in /kaggle/working/i01-setup/.
5. Separately run **Check the implementation**, **Download verified weights**,
   and **Load both T4 workers**. Lightweight native/scripted checks must pass.
   Downloads reuse verified cached/partial bytes, verify Git/LFS identities and
   measured storage. The load cell first records the actual current session
   window; missing facts stop before loading. Loading performs no hidden warmup.
6. Run **Check fresh-state readiness** (six first attempts maximum), then
   **Check direct-mode competence** (twelve). Inspect qualification. Failed
   gates stop the cell after saving evidence and exposing its checkpoint.
   Skip thinking if direct passed. Only a documented competence limitation
   without protocol defects permits the explicitly requested thinking screen,
   after you supply its real reason (twelve first attempts maximum).
7. Run **Check selected-mode headroom**. The passing recorded mode is derived
   automatically. Two full-envelope probes require at least 1.5 GiB measured
   free headroom per T4. Output forcing applies only to diagnostics.
8. Run **pilot 1 only**. Its conversation, private audit, outcomes, costs and
   cumulative checkpoint appear automatically. Inspect and download the ZIP.
   In **Review pilot 1**, replace the two None findings with actual True/False
   conclusions and write trace-based notes, then execute the review. Repeat
   separately for pilots 2 and 3. Each pilot has at most twenty first attempts;
   eligible retries are separately charged. Useful original communication is a
   human finding; recovery errors/effect sign alone do not fail the pilot gate.
9. Run **Review the main configuration**. Read original-team/control results,
   human reviews, exact configuration and measured resource forecast. Write
   actual FREEZE_NOTES and run **Freeze for main**. Download the pre-main ZIP.
   Freeze makes no main calls.
10. Repeat only **Prepare next main batch → Run prepared batch → Inspect and
    acknowledge batch**. Default is the next two fixed worlds (maximum 38 first
    attempts); explicitly change count to one for a one-world scope (maximum
    19). Batch ID/incomplete scope come from saved state. Optional extra review
    notes are available. Completed-scope reruns make no new model calls.
    Models stay resident during inspection and between stages.
11. Run **Build the final or partial report**, then **Save and verify the final
    archive**. Save the ZIP outside Kaggle and download/save the **executed
    notebook** separately, without Save & Run All.
12. Run **Finish the session** after saving. Close models/controller, then stop
    Kaggle through its UI. Process exit alone does not prove deallocation.

Every research cell requests one bounded scope; completion starts no later stage.
All diagnostics/failures/retries count toward 500 new physical attempts and the
shared 28 contingency. Historical 45 remain separate. First-attempt ceilings
do not include or conceal eligible retries.

## Results, conversations and downloads

Readable outcome/cost/device tables and live progress replace routine JSON dumps.
Phase events show exact public messages in order. Private submissions, evaluator
truth, retained history, exact requests, raw replies, tokens and thinking are
labelled audit details and never enter partner inputs.

Complete evidence remains in reports/conversations.html, .jsonl and .txt,
including calls beyond the bounded default detailed display. Ordinary commands:

    study.inspect(world="pilot-00", audit_limit=None);
    study.inspect(world="pilot-00", phase="retain", agent=0, audit_limit=None);
    study.links(all_files=True);
    study.annotate("unique-review-id", "ambiguous", ["exact/call/id"], "Trace-based notes");

Thinking is audit material, not a faithful explanation. Human annotations need
exact trace references and frozen rubric labels; no LLM judge is used.

Reports include all twenty intended main worlds, paired counts/contrasts, unknown
bounds, correct-prefix descriptive stratum, exploratory stratified bootstrap,
physical/logical costs, failures and limitations. Unexecuted/unresolved outcomes
remain unknown; recorded terminal failures score zero. Download CSV/HTML/JSONL/
text, SVG/PNG figures and plotting data.

The prominent download is **i01-study/exports/latest.zip**, a **current cumulative**
checkpoint that advances after later actions. Refresh its boundary/time/hash.
An old link does not promise an immutable historical pilot archive. If links fail,
use Kaggle's Output/Files pane and the exact path. Link creation proves neither
browser download nor off-session durability.

## Pause, reopen and restore

Interrupting a synchronous generation cell requests pause. Stop new admissions;
let an already admitted call finish or terminate within its bound. Status may
still show active/unresolved work; interruption is not an immediate safe snapshot.

    study.show_status();
    study.pause();  # Request only.
    # Wait for settlement/confirmed bounded termination, then:
    study.save_checkpoint();

Quiescent SQLite backup copies, integrity inventory and atomic ZIP replacement
preserve the last valid archive on failure. The ZIP contains both canonical DBs,
exact source/wheel/configuration, fixed inputs/seeds, gate/freeze/session evidence,
raw outputs/tokens and reports. No weights, environments, caches or credentials.

For intact files after kernel restart, use START_MODE = "reopen", fresh actual
session facts and workspace/runtime setup as needed. The ownership lock refuses
a second controller until the old owner exits.

For another session, attach the **matching source release** and exactly selected
checkpoint. Use START_MODE = "restore" and uncomment its configuration values:

    RESTORE_CHECKPOINT = "/kaggle/input/EXACT-DOWNLOADED-CHECKPOINT"
    RESTORE_TAIL = "latest"  # "unknown" if latest-boundary evidence is unavailable.
    RESTORE_EVIDENCE = "Actual evidence about safe boundary and prior session"

Restore into a fresh writable directory. ZIP/expanded inputs work; no timestamp
guessing or silent new study when a ZIP is missing. Reexecuting against an already
restored nonempty destination requires the explicit reopen route. Unknown tail
spending can block admission.

After self-check, weight reuse and loading, run **two contingency-charged**
new-session/replacement-worker envelope probes:

    study.check_headroom(reload=True);
    study.run_main_batch();  # Only for a saved interrupted main scope.

Already accepted readiness/competence need not be rerun just for restore.
Completed calls reuse raw outcomes; raw-persisted calls apply effects without
generation. An older checkpoint uses its exact saved source for resumed inference,
not a silently upgraded UI/runtime. Older checkpoints remain readable for reports.

Only after observing prior process/session exit, reconcile exact identifiers:

    study.reconcile_attempt( slot=0, attempt=EXACT_ATTEMPT_ID,
        evidence={"termination_confirmed": True, "reason": "Actual observed exit"});
    study.confirm_timeout_termination( slot=0, call="EXACT_CALL_ID",
        evidence={"termination_confirmed": True, "reason": "Actual observed exit"});

Only one identical pre-persistence infrastructure retry is eligible after
confirmed termination. Wrong/malformed/truncated replies and recorded timeouts
never retry. A stale PID is not proof of death.

If saved bytes predate lost work, record partial recovery, a defensible missing-
spending bound and affected worlds. Lost prefixes cannot silently regenerate:

    study.record_lost_spending(
        gap={"resolved": True, "upper": ACTUAL_UPPER_BOUND, "evidence": "Actual evidence"},
        affected_worlds=["main-XX"]);

Unbounded loss uses resolved=False, upper=None. Unknown is never assumed zero.
Generation can be blocked while reporting remains available.

## Read-only reconstruction and package maintenance

With a controller, use study.build_report(). With intact files and no controller,
that same method reconstructs reports without workers/CUDA. Outside the notebook,
extract the checkpoint and use its exact saved source:

    python scripts/i01_course.py --source SOURCE --run EXTRACTED status
    python scripts/i01_course.py --source SOURCE --run EXTRACTED report --output REPORT_DIR

The wheel also provides i01-course and python -m recovery.i01.cli.
Read-only analysis creates no workers and infers no missing outcomes.

Development rebuild and focused verification, zero model calls:

    python scripts/build_i01_course_notebook.py
    python -m unittest tests.test_i01_setup tests.test_i01_notebook_ui tests.test_i01_integration
    python scripts/build_i01_course_release.py
    python scripts/verify_i01_course_release.py

See the [workflow plan/completion record](plans/i01-notebook-natural-workflow.md),
[WBS handoff](plans/i01-course-implementation-wbs.md#15-requested-notebook-usability-follow-up)
and [focused evidence](validation/i01-implementation.md).
Actual output layout, interrupt responsiveness, downloads and Linux/T4
qualification remain target-host acceptance; historical probes are not I-01 results.
