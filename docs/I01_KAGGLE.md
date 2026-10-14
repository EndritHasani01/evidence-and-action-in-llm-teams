# I-01 Kaggle: ordinary notebook cells

Press **Run** to perform the cell's named stage. No widget forms or extra action
buttons. Run **one stage cell at a time**. **Run All / Save & Run All can execute
inference and multiple stages and is not a supported study execution method.**

This is implementation delivery, not empirical acceptance. Actual Kaggle
installation, native framing/capacity, T4 residency/cleanup, headroom, competence,
pilots, freeze and main results still need operator execution. No model/GPU
inference or experiment was run during this redesign.

## First execution

1. Upload **dist/i01-course/i01-source.zip** as a **private Kaggle dataset** and
   attach it. Kaggle may expose the ZIP or expanded files; both work.
2. Upload **notebooks/i01_course_kaggle.ipynb**, also copied into dist/i01-course.
   Select **GPU T4 ×2**, enable **Internet**, and keep the study private.
3. In **Configure and inspect the workspace**, supply SESSION_DEADLINE_UTC as
   the actual future ISO time with UTC offset, and SESSION_ALLOWANCE_EVIDENCE
   from the current Kaggle UI. Leave START_MODE = "new" for a fresh study.
   Source selection is automatic only when one verified candidate exists;
   otherwise set SOURCE_BUNDLE exactly.
4. Run **Install the pinned runtime**, then **Open the study**. The reviewed
   Linux x86_64 Python 3.13 candidate is installed in a separate environment;
   the kernel's Torch stack is not replaced. Actual incompatibility stops.
   Setup/download logs are in /kaggle/working/i01-setup/.
5. Separately run **Check the implementation**, **Download verified weights**,
   and **Load both T4 workers**. Lightweight native/scripted checks must pass.
   Downloads reuse verified cached/partial bytes, verify Git/LFS identities and
   measured storage. Loading performs no hidden warmup.
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

    ui.inspect(world="pilot-00", audit_limit=None);
    ui.inspect(world="pilot-00", phase="retain", agent=0, audit_limit=None);
    ui.links(all_files=True);
    ui.annotate("unique-review-id", "ambiguous", ["exact/call/id"], "Trace-based notes");

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

    ui.run("status");
    ui.run("pause");  # Request only.
    # Wait for settlement/confirmed bounded termination, then:
    ui.run("snapshot");

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

    ui.envelope(reload=True);
    ui.run_batch();  # Only for a saved interrupted main scope.

Already accepted readiness/competence need not be rerun just for restore.
Completed calls reuse raw outcomes; raw-persisted calls apply effects without
generation. An older checkpoint uses its exact saved source for resumed inference,
not a silently upgraded UI/runtime. Older checkpoints remain readable for reports.

Only after observing prior process/session exit, reconcile exact identifiers:

    ui.client.command("reconcile", slot=0, attempt=EXACT_ATTEMPT_ID,
        evidence={"termination_confirmed": True, "reason": "Actual observed exit"});
    ui.client.command("confirm_timeout_termination", slot=0, call="EXACT_CALL_ID",
        evidence={"termination_confirmed": True, "reason": "Actual observed exit"});

Only one identical pre-persistence infrastructure retry is eligible after
confirmed termination. Wrong/malformed/truncated replies and recorded timeouts
never retry. A stale PID is not proof of death.

If saved bytes predate lost work, record partial recovery, a defensible missing-
spending bound and affected worlds. Lost prefixes cannot silently regenerate:

    ui.client.command("lost_spending",
        gap={"resolved": True, "upper": ACTUAL_UPPER_BOUND, "evidence": "Actual evidence"},
        affected_worlds=["main-XX"]);

Unbounded loss uses resolved=False, upper=None. Unknown is never assumed zero.
Generation can be blocked while reporting remains available.

## Read-only reconstruction and package maintenance

With a controller, use ui.final_report(). With intact files and no controller,
that same method reconstructs reports without workers/CUDA. Outside the notebook,
extract the checkpoint and use its exact saved source:

    python scripts/i01_course.py --source SOURCE --run EXTRACTED status
    python scripts/i01_course.py --source SOURCE --run EXTRACTED report --output REPORT_DIR

The wheel also provides i01-course and python -m recovery.i01.cli.
Read-only analysis creates no workers and infers no missing outcomes.

Development rebuild and focused verification, zero model calls:

    python scripts/build_i01_course_notebook.py
    python -m unittest tests.test_i01_notebook_ui tests.test_i01_integration
    python scripts/build_i01_course_release.py
    python scripts/verify_i01_course_release.py

See the [workflow plan/completion record](plans/i01-notebook-natural-workflow.md),
[WBS handoff](plans/i01-course-implementation-wbs.md#15-requested-notebook-usability-follow-up)
and [focused evidence](validation/i01-implementation.md).
Actual output layout, interrupt responsiveness, downloads and Linux/T4
qualification remain target-host acceptance; historical probes are not I-01 results.
