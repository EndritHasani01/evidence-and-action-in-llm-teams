"""Reproducible ordinary-cell notebook; each research cell has one finite scope."""

import json
from pathlib import Path


BOOTSTRAP = '''from pathlib import Path
import hashlib, json, shutil, sys, tempfile, zipfile

# Select one exact small source attachment. ZIP and Kaggle-expanded roots work.
SOURCE_BUNDLE = None  # Set only if more than one candidate is attached.
source_candidates = list(Path('/kaggle/input').rglob('i01-source.zip'))
source_candidates += [p.parent for p in Path('/kaggle/input').rglob('source-release.json')]
if SOURCE_BUNDLE is None:
    if len(source_candidates) != 1:
        raise RuntimeError(f'Select SOURCE_BUNDLE explicitly; candidates: {source_candidates}')
    SOURCE_BUNDLE = source_candidates[0]
selected_source = Path(SOURCE_BUNDLE)
source_root = Path('/kaggle/working/i01-source')
with tempfile.TemporaryDirectory(prefix='i01-source-', dir='/kaggle/working') as staging_name:
    staging = Path(staging_name)
    if selected_source.is_file():
        with zipfile.ZipFile(selected_source) as source_zip:
            infos = source_zip.infolist()
            if sum(p.file_size for p in infos) > 64 * 2**20 or len({p.filename for p in infos}) != len(infos):
                raise RuntimeError('Source attachment size or duplicate member violation')
            for item in infos:
                p = Path(item.filename)
                if p.is_absolute() or '..' in p.parts or '\\\\' in item.filename or ':' in item.filename or ((item.external_attr >> 16) & 0o170000) == 0o120000:
                    raise RuntimeError('Unsafe source archive member')
            if source_zip.testzip() is not None:
                raise RuntimeError('Source ZIP integrity failed')
            source_zip.extractall(staging)
    elif selected_source.is_dir():
        if any(p.is_symlink() for p in selected_source.rglob('*')):
            raise RuntimeError('Select an ordinary verified expanded source directory')
        shutil.copytree(selected_source, staging, dirs_exist_ok=True)
    else:
        raise RuntimeError('Missing exact selected source attachment')
    release = json.loads((staging/'source-release.json').read_text())
    if release['format'] != 'i01-online-source-v1':
        raise RuntimeError('Wrong source release format')
    for relative, wanted in release['files'].items():
        path = staging/relative
        if not path.is_file() or path.stat().st_size != wanted['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != wanted['sha256']:
            raise RuntimeError(f'Source identity failed: {relative}')
        if source_root.exists() and (not (source_root/relative).is_file() or hashlib.sha256((source_root/relative).read_bytes()).hexdigest() != wanted['sha256']):
            raise RuntimeError('Existing source differs; select a fresh session/source directory')
    if not source_root.exists():
        shutil.copytree(staging, source_root)
sys.path.insert(0, str(source_root))
from recovery.i01.ui import Operator
if 'ui' not in globals():
    ui = Operator(source_root)
ui.bootstrap_status()
'''


def notebook():
    cells=[]
    def markdown(text):
        cells.append(dict(cell_type="markdown",id=f"i01-text-{len(cells):02d}",metadata={},source=text.splitlines(keepends=True)))
    def stage(identity,title,description,body,action=None,generation=False):
        markdown(f"## {title}\n\n{description}\n")
        cells.append(dict(cell_type="code",id=identity,metadata=dict(i01=dict(action=action,generation=generation)),
                          execution_count=None,outputs=[],source=body.splitlines(keepends=True)))

    markdown("""# I-01: recovery after a changed winning value

Two agents collaborate on a maximum. After one value changes, compare retaining
their conversation with clearing it. This is a controlled recovery extension of
SILO-BENCH I-01: six qualification worlds, three pilots, twenty main worlds.

**Run one stage cell at a time. Pressing Run performs the named stage.**
No widget forms or extra action buttons. **Do not use Run All / Save & Run All:**
those commands can execute inference and multiple stages. Each research cell
requests only its displayed bounded scope; successful work starts no later stage.

Attach the matching **private source dataset**, select **GPU T4 ×2** and enable
**Internet**. Actual host/runtime compatibility is checked before installation.
Model qualification and research outcomes remain unverified until executed.

Setup → qualification → pilot 1/review → pilot 2/review → pilot 3/review →
freeze → prepare/run/review main batches → report → portable archive.

The whole study has a **500-new-physical-attempt ceiling**. Diagnostics, failures
and eligible retries count. Historical 45 are separate. First-attempt ceilings
exclude eligible retries, which consume shared 28 contingency and study allowance.

Models stay resident during inspection and between stages. Interrupt requests
pause; an admitted call must settle within its bound. Recovery recipes are below.
""")
    configuration="""# Supply facts from the CURRENT Kaggle session; no duration or quota is guessed.
START_MODE = "new"  # "reopen" for intact files; "restore" for a selected archive.
SESSION_DEADLINE_UTC = None  # Actual future ISO time: YYYY-MM-DDTHH:MM:SS+00:00.
SESSION_ALLOWANCE_EVIDENCE = ""  # Describe the actual allowance shown by Kaggle.

# Only for restoration: uncomment and supply exact checkpoint/tail evidence.
# RESTORE_CHECKPOINT = "/kaggle/input/EXACT-DOWNLOADED-CHECKPOINT"
# RESTORE_TAIL = "latest"  # "unknown" if the latest safe boundary is uncertain.
# RESTORE_EVIDENCE = "Actual evidence about the saved boundary and prior session."

"""
    stages=[
      ("workspace","1. Configure and inspect the workspace","Edit actual session facts here. A unique verified source ZIP/expanded directory is selected automatically; set SOURCE_BUNDLE only when ambiguous. Inventory only; no installation or generation.",configuration+BOOTSTRAP,None,False),
      ("setup","2. Install the pinned runtime","Install/reuse the isolated pinned environment and fetch metadata/tokenizer. Live progress and /kaggle/working/i01-setup/ logs. No model loading or generation.",'ui.run("setup");\n',"setup",False),
      ("open-study","3. Open the study","Create fixed inputs, reopen intact files or explicitly restore into a fresh writable directory. Record this session's actual allowance/deadline. Missing facts stop here; conflicting studies are never overwritten.",
       'ui.open_study(START_MODE, deadline=SESSION_DEADLINE_UTC,\n    allowance_evidence=SESSION_ALLOWANCE_EVIDENCE,\n    selected=globals().get("RESTORE_CHECKPOINT"),\n    tail=globals().get("RESTORE_TAIL"), evidence=globals().get("RESTORE_EVIDENCE", ""));\n',"initialize",False),
      ("selfcheck","4. Check the implementation","Lightweight mathematics/private-view/lifecycle/durability/accounting/archive/restore and native-tokenizer checks. Temporary scripted records, zero model attempts.",'ui.run("selfcheck");\n',"selfcheck",False),
      ("weights","5. Download verified weights","Retrieve/reuse the pinned Qwen3.5-9B files; verify native identities and actual available space. Progress appears below. No inference.",'ui.run("weights");\n',"weights",False),
      ("load","6. Load both T4 workers","Load/attach the two resident replicas and show device/load receipts. No hidden warmup. Inspection does not unload them.",'ui.run("load");\n',"load",False),
      ("readiness","7. Check fresh-state readiness","Exactly six short A/B/A diagnostics across both workers: ≤6 first attempts plus eligible contingency. A failed gate stops the cell with saved evidence.",'ui.run("readiness");\n',"readiness",True),
      ("direct-screen","8. Check direct-mode competence","Twelve original/revised controls, ≤12 first attempts plus eligible contingency. Require ≥11/12 correct and zero malformed/truncated actions. Failure stops here; inspect it below.",'ui.run("screen", mode="direct");\n',"screen",True),
      ("qualification","9. Inspect qualification","Read-only control outcomes and complete saved evidence. If direct passed, proceed to headroom. A protocol defect blocks research; only a documented competence limitation enables the optional thinking screen.",'ui.inspect(worlds=[f"qualification-{i:02d}" for i in range(6)]);\n',None,False),
      ("thinking-screen","Optional: thinking qualification","Skip if direct passed; running this cell then makes zero calls. Otherwise supply your evidence-based competence reason only after direct failure without protocol errors. ≤12 first attempts; no automatic fallback or extra model candidate.",
       'THINKING_COMPETENCE_REASON = None\nui.thinking_screen(THINKING_COMPETENCE_REASON);\n',"screen",True),
      ("envelope","10. Check selected-mode headroom","The passing recorded mode is derived automatically. Two full-input/full-output probes, ≤2 first attempts. Require ≥1.5 GiB measured free headroom on each T4. Output forcing applies only to diagnostics. Restored/reloaded sessions use the separately charged reload recipe.",'ui.envelope();\n',"envelope",True)
    ]
    for args in stages: stage(*args)
    for n in (1,2,3):
        stage(f"pilot-{n}",f"{10+n}. Run pilot {n}",
              f"Run **pilot {n} only**, including original team, literal retain/clear siblings and original/revised controls. ≤20 first attempts plus eligible contingency. Conversation, outcomes, costs and cumulative checkpoint appear automatically. Inspect/download before review; recovery errors alone do not fail the gate.",
              f'ui.run("pilot", number={n});\n',"pilot",True)
        stage(f"review-pilot-{n}",f"Review pilot {n}",
              "Replace the None findings with actual True/False conclusions and write trace-based notes. Useful original communication is a human finding, not inferred from correct answers. Records only this review; no next pilot/freeze. Unreviewed never means approved.",
              f'ui.review_pilot({n},\n    useful_communication=None,\n    usable=None,\n    notes="");\n',"review")
    for args in [
      ("pre-freeze","14. Review the main configuration","Read qualification, three pilot reviews, exact configuration and measured attempt/time forecast. This cell neither freezes nor generates.",'ui.preview_freeze();\n',None,False),
      ("freeze","15. Freeze for main","Write actual review notes, then run to freeze accepted configuration. Gates require correct original teams/controls, valid protocol, documented communication/usability and adequate resources. Download the pre-main checkpoint. No main calls.",'FREEZE_NOTES = ""\nui.run("freeze", notes=FREEZE_NOTES);\n',"freeze",False),
      ("prepare-batch","16. Prepare the next main batch","Prepare the next fixed two worlds, or return the existing incomplete scope. Change count to 1 explicitly for a one-world batch. Show IDs, remaining work, ≤19/38 first-attempt ceiling, eligible retry allowance and forecast. No generation. Repeat sections 16–18 only by choice.",'ui.run("prepare_batch", count=2);\n',"prepare_batch",False),
      ("main-batch","17. Run the prepared main batch","Execute/resume only the saved scope: ≤19/38 first attempts plus eligible contingency. No next-batch preparation/execution. A completed saved batch displays results with zero calls. Interrupt requests pause; wait for settlement before export/closure.",'ui.run_batch();\n',"main",True),
      ("review-batch","18. Inspect and acknowledge the batch","Inspect the previous output and complete conversation files; download the checkpoint, then run this acknowledgement. Saved batch ID is derived automatically; extra notes are optional. No claim of verified understanding/download. Return to section 16 or continue to reporting when all intended work is recorded.",'ui.review_batch(notes="");\n',"review",False),
      ("report","19. Build the final or partial report","Read-only canonical reconstruction: twenty intended worlds, exact paired outcomes, unknown bounds, correct-prefix descriptive stratum, costs, failures, figures and limitations. No inference/reload. Download HTML/text/JSONL, CSV/plotting data and SVG/PNG.",'ui.final_report();\n',"report",False),
      ("archive","20. Save and verify the final archive","Quiescent snapshot and exact fresh-directory analysis comparison, zero model calls. Save ZIP outside Kaggle. Save/download the executed notebook separately **without Save & Run All**. Links do not prove backup.",'ui.run("snapshot");\nui.verify_checkpoint();\n',"snapshot",False),
      ("close","Finish the session","Run after saving the checkpoint and executed notebook. Close models/controller, then stop Kaggle through its UI. Process exit does not establish provider deallocation; partial outcomes remain partial.",'ui.run("close_models");\nui.run("shutdown");\n',"shutdown",False)
    ]: stage(*args)
    markdown("""## Recovery and support

Copy the needed ordinary commands into a cell. These recipes do not execute
merely by opening this appendix. Use the action matching saved state; never reset
a study to work around a blocked gate.

### Status, pause and a safe checkpoint

    ui.run("status");
    ui.run("pause");  # Request only; an admitted call may still be active.
    # Wait for settlement / confirmed bounded termination, then:
    ui.run("snapshot");

Interrupting a generation cell already requests pause. Do not infer process death
from a stale PID or claim interrupt immediately produced a safe checkpoint.

### Reopen or restore

For intact files after kernel restart, rerun workspace/runtime setup as needed,
set START_MODE = "reopen" and fresh actual session deadline/evidence, then Open
the study. The ownership lock refuses a second live controller.

For another session, attach the **matching source release** and exact downloaded
checkpoint. Set START_MODE = "restore"; uncomment the restore values in the
configuration cell and record genuine latest-boundary or unknown-tail evidence.
Restore into a fresh writable directory. ZIP and expanded roots both work.
No archive is chosen by timestamp; a missing ZIP never silently creates a study.

After reopening/restoring: self-check, reuse/download weights, then load workers.
New session/replacement workers need **two contingency-charged probes**:

    ui.envelope(reload=True);
    ui.run_batch();  # Resume only a saved interrupted main scope.

Do not redo already accepted readiness/qualification just to restore the study.
Completed calls reuse durable raw replies without generation. Load/reload evidence
remains recorded; diagnostics, retries and warmups never disappear from accounting.

### Reconcile missing outcomes or termination evidence

Only after observed prior process/session exit, supply exact identifiers/evidence:

    ui.client.command("reconcile", slot=0, attempt=EXACT_ATTEMPT_ID,
        evidence={"termination_confirmed": True, "reason": "Actual observed exit"});
    ui.client.command("confirm_timeout_termination", slot=0, call="EXACT_CALL_ID",
        evidence={"termination_confirmed": True, "reason": "Actual observed exit"});

Admitted calls without durable output stay spent/unknown. Only one identical
pre-persistence infrastructure retry is eligible after confirmed termination.
Recorded timeouts, wrong, malformed or truncated replies never retry.

If saved bytes predate lost work, report partial recovery. Provide a defensible
spending bound and affected worlds; unbounded unknown spending blocks generation
while allowing reports:

    ui.client.command("lost_spending",
        gap={"resolved": True, "upper": ACTUAL_UPPER_BOUND, "evidence": "Actual evidence"},
        affected_worlds=["main-XX"]);
    # For unbounded loss: resolved=False, upper=None. Never assume zero.

### Complete inspection, annotation and read-only reporting

    ui.inspect(world="pilot-00", phase="retain", agent=0, audit_limit=None);
    ui.links(all_files=True);
    ui.annotate("unique-review-id", "ambiguous", ["exact/call/id"], "Trace-based notes");

Filtering changes only this view. Private submissions, truth and thinking are
audit material, never partner input. Thinking is not a faithful explanation.
No LLM judge is used.

With an initialized controller use ui.final_report(). With only intact files,
the same method reconstructs reports read-only without creating workers/CUDA.
Outside the notebook, use its exact saved source:

    python scripts/i01_course.py --source SOURCE --run EXTRACTED status
    python scripts/i01_course.py --source SOURCE --run EXTRACTED report --output REPORT_DIR

A previous checkpoint uses its exact saved source release for inference.
Reports remain readable; a UI update cannot replace its scientific evidence.
""")
    return dict(nbformat=4,nbformat_minor=5,cells=cells,
                metadata=dict(kernelspec=dict(display_name="Python 3",language="python",name="python3"),
                              language_info=dict(name="python"),kaggle=dict(accelerator="gpu",isInternetEnabled=True),
                              i01=dict(regime="i01-course-v1",research_execution="ordinary cells; one explicit bounded stage",
                                       run_all_can_execute_inference=True,kaggle_verified=False)))


def build(path):
    value=notebook()
    for cell in value["cells"]:
        if cell["cell_type"]=="code": compile("".join(cell["source"]),cell["id"],"exec")
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return path


if __name__=="__main__":
    print(build(Path(__file__).resolve().parents[1]/"notebooks/i01_course_kaggle.ipynb"))
