"""Reproducible ordinary-cell notebook; each research cell has one finite scope."""

import json
from pathlib import Path


BOOTSTRAP = '''from pathlib import Path
import hashlib, json, shutil, sys, tempfile, zipfile

# Select one exact small source attachment. ZIP and Kaggle-expanded roots work.
SOURCE_BUNDLE = None  # Set only if more than one candidate is attached.
source_candidates = list(Path('/kaggle/input').rglob('i01-source.zip'))
source_candidates += [p.parent for p in Path('/kaggle/input').rglob('source-release.json')]
# Expanded old checkpoints carry their own historical source. They are evidence,
# not candidates for this repaired notebook's active source attachment.
def repaired_source_manifest(path):
    try:
        if path.is_dir():
            manifest = json.loads((path/'source-release.json').read_text())
        else:
            with zipfile.ZipFile(path) as archive:
                manifest = json.loads(archive.read('source-release.json'))
        return manifest if all('recovery/i01/'+name+'.py' in manifest['files'] for name in ('policy','continuation')) else None
    except (OSError, ValueError, KeyError, zipfile.BadZipFile):
        return None
unique_sources = {}
for candidate in source_candidates:
    manifest = repaired_source_manifest(candidate)
    if manifest:
        identity = (manifest.get('git_head'), json.dumps(manifest['files'], sort_keys=True))
        unique_sources.setdefault(identity, candidate)  # Same ZIP/expanded release is one choice.
source_candidates = list(unique_sources.values())
if SOURCE_BUNDLE is None:
    if len(source_candidates) != 1:
        raise RuntimeError(f'Select SOURCE_BUNDLE explicitly; candidates: {source_candidates}')
    SOURCE_BUNDLE = source_candidates[0]
selected_source = Path(SOURCE_BUNDLE)
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
    if not all('recovery/i01/'+name+'.py' in release['files'] for name in ('policy','continuation')):
        raise RuntimeError('This notebook requires the repaired direct-protocol source packet; preserve old checkpoints and replace the active source attachment.')
    head = release.get('git_head', '')
    if len(head) != 40 or any(c not in '0123456789abcdef' for c in head):
        raise RuntimeError('Invalid source release commit')
    source_root = Path('/kaggle/working') / ('i01-source-' + head[:12])
    for relative, wanted in release['files'].items():
        path = staging/relative
        if not path.is_file() or path.stat().st_size != wanted['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != wanted['sha256']:
            raise RuntimeError(f'Source identity failed: {relative}')
        if source_root.exists() and (not (source_root/relative).is_file() or hashlib.sha256((source_root/relative).read_bytes()).hexdigest() != wanted['sha256']):
            raise RuntimeError('Existing source differs; select a fresh session/source directory')
    if not source_root.exists():
        shutil.copytree(staging, source_root)
loaded_source = sys.modules.get('recovery')
if loaded_source is not None and not Path(loaded_source.__file__).resolve().is_relative_to(source_root.resolve()):
    raise RuntimeError('Restart the notebook kernel before using this source release; saved study files are preserved.')
sys.path.insert(0, str(source_root))
from recovery.i01.notebook import Study
if 'study' not in globals():
    study = Study(source_root, run=RUN_DIR)
elif study.source.resolve()!=source_root.resolve() or study.run_dir.resolve()!=Path(RUN_DIR).resolve():
    raise RuntimeError('Finish the current study and restart the kernel before changing source or RUN_DIR; existing study files are preserved.')
study.bootstrap_status()
'''


def research_notebook():
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
This is the complete stage-by-stage research notebook. For a fresh diagnostic
Run All, use **i01_course_kaggle.ipynb** instead. This notebook also starts from
scratch by default; restore only your NEW study's checkpoint when continuing it.
Direct controls qualify on valid protocol; mathematical accuracy is reported.

Setup → qualification → pilot 1/review → pilot 2/review → pilot 3/review →
freeze → prepare/run/review main batches → report → portable archive.

The explicitly requested independent rerun has its own **500-physical-attempt
ceiling**, starting at zero. No previous study's result or checkpoint is imported.
Its own retries, diagnostics, restores and reloads all count. Prior studies remain
historical evidence and are not pooled with these new outcomes.

Models stay resident during inspection and between stages. Interrupt requests
pause; an admitted call must settle within its bound. Recovery recipes are below.
""")
    configuration="""# Current source and exact study destination. Session facts have their own later cell.
START_MODE = "new"  # Or "restore" for this NEW study's checkpoint; "reopen" for intact files.
RUN_DIR = "/kaggle/working/i01-fresh-study"

# Only for restore of this new study; leave unset when starting from scratch.
RESTORE_CHECKPOINT = None
PRIOR_CHECKPOINTS = None
# Set these two facts before Open the study:
RESTORE_TAIL = None  # "latest" only if no later generation occurred; otherwise "unknown".
RESTORE_EVIDENCE = ""  # Actual evidence about the boundary and old session exit.

"""
    stages=[
      ("workspace","1. Configure and inspect the workspace","Choose the start mode and study destination here. A unique verified source ZIP/expanded directory is selected automatically; set SOURCE_BUNDLE only when ambiguous. Inventory only; no installation or generation. Record current session facts later in stage 6.",configuration+BOOTSTRAP,None,False),
      ("setup","2. Install the pinned runtime","Create/recover the isolated environment without ensurepip, bootstrap verified pinned pip and install the unchanged runtime lock; fetch metadata/tokenizer. Live progress and release-labelled i01-setup-<source> logs under /kaggle/working. No model loading or generation.",'study.install_runtime();\n',"setup",False),
      ("open-study","3. Open the study","New creates this explicitly independent study at zero attempts. Rerunning reuses the same study and never resets accounting. Restore/reopen preserve every attempt and outcome from this new study. No model loading or generation.",
       'study.open(START_MODE,\n    selected=globals().get("RESTORE_CHECKPOINT"),\n    tail=globals().get("RESTORE_TAIL"), evidence=globals().get("RESTORE_EVIDENCE", ""),\n    prior_checkpoints=globals().get("PRIOR_CHECKPOINTS"), independent=(START_MODE == "new"));\n',"initialize",False),
      ("selfcheck","4. Check the implementation","Lightweight mathematics/private-view/lifecycle/durability/accounting/archive/restore and native-tokenizer checks. Temporary scripted records, zero model attempts.",'study.check_implementation();\n',"selfcheck",False),
      ("weights","5. Download verified weights","Retrieve/reuse the pinned Qwen3.5-9B files; verify native identities and actual available space. Progress appears below. No inference.",'study.download_weights();\n',"weights",False),
      ("session-window","6. Record this session window","Read the CURRENT remaining session duration and allowance from Kaggle. Replace None and the empty evidence below with those actual facts. No default quota is assumed. Rerunning reuses the recorded fixed deadline; loading is a separate next cell. Absolute UTC and explicit refresh alternatives are in the appendix.",'SESSION_REMAINING_MINUTES = None  # Actual remaining minutes observed now.\nSESSION_ALLOWANCE_EVIDENCE = ""  # Actual current provider allowance evidence.\nstudy.configure_session(remaining_minutes=SESSION_REMAINING_MINUTES,\n    evidence=SESSION_ALLOWANCE_EVIDENCE);\n',"window",False),
      ("load","7. Load both T4 workers","Use the recorded current window, load/attach two resident replicas from the verified local snapshot, and show device/load receipts. No hidden warmup. Inspection does not unload them.",'study.load_models();\n',"load",False),
      ("readiness","8. Inspect or check fresh-state readiness","Six fresh A/B/A diagnostics, three per worker. Completed outcomes are reused on rerun with zero new calls. Cache/finite defects block work; unequal A/B/A requires review. The later full envelope validates the current loaded replicas.",'study.check_readiness();\n',"readiness",True),
      ("direct-screen","9. Check direct protocol qualification","Twelve original/revised controls must be committed and protocol-valid. Mathematical accuracy is diagnostic, not a cutoff. A fresh study makes twelve new calls. Completed controls are reused on rerun without resampling; earlier studies are not imported.",'study.qualify_direct();\n',"screen",True),
      ("qualification","10. Inspect qualification","Read-only per-mode scope, every control truth/submission, validity, correctness, tokens/time and failure-first raw inspection. Direct eligibility follows the adopted policy; old failed gates are preserved. Complete direct protocol qualification is required before headroom.",'study.inspect_qualification();\n',None,False),
      ("thinking-history","Optional: inspect saved thinking","Zero-generation inspection of this study only. All thinking controls remain unexecuted for the fresh direct-only run. This cell requests no thinking qualification.",
       'study.inspect_thinking();\n',None,False),
      ("envelope","11. Check selected-mode headroom","The passing recorded mode is derived automatically. Two full-input/full-output probes, ≤2 first attempts. Require ≥1.5 GiB measured free headroom on each T4. Output forcing applies only to diagnostics. Restored/reloaded sessions use the separately charged reload recipe.",'RELOAD_HEADROOM = False  # True only after restoring/reloading an already accepted envelope.\nstudy.check_headroom(reload=RELOAD_HEADROOM);\n',"envelope",True)
    ]
    for args in stages: stage(*args)
    for n in (1,2,3):
        stage(f"pilot-{n}",f"{11+n}. Run pilot {n}",
              f"Run **pilot {n} only**, including original team, literal retain/clear siblings and original/revised controls. ≤20 first attempts plus eligible contingency. Conversation, outcomes, costs and cumulative checkpoint appear automatically. Inspect/download before review; recovery errors alone do not fail the gate.",
              f'study.run_pilot({n});\n',"pilot",True)
        stage(f"review-pilot-{n}",f"Review pilot {n}",
              "Replace the None findings with actual True/False conclusions and write trace-based notes. Useful original communication is a human finding, not inferred from correct answers. Records only this review; no next pilot/freeze. Unreviewed never means approved.",
              f'study.record_pilot_review({n},\n    useful_communication=None,\n    usable=None,\n    notes="");\n',"review")
    for args in [
      ("pre-freeze","15. Review the main configuration","Read qualification, three pilot reviews, exact configuration and measured attempt/time forecast. This cell neither freezes nor generates.",'study.review_configuration();\n',None,False),
      ("freeze","16. Freeze for main","Write actual review notes, then freeze the direct condition and protocol-first policy. Require complete pilot teams/controls, valid protocol, documented useful original communication/usability and adequate resources; mathematical mistakes alone do not disqualify. Keep all twenty main worlds. Download the pre-main checkpoint. No main calls.",'FREEZE_NOTES = ""\nstudy.freeze_configuration(FREEZE_NOTES);\n',"freeze",False),
      ("prepare-batch","17. Prepare the next main batch","Prepare the next fixed two worlds, or return the existing incomplete scope. Change count to 1 explicitly for a one-world batch. Show IDs, remaining work, ≤19/38 first-attempt ceiling, eligible retry allowance and forecast. No generation. Repeat sections 17–19 only by choice.",'study.prepare_main_batch(count=2);\n',"prepare_batch",False),
      ("main-batch","18. Run the prepared main batch","Execute/resume only the saved scope: ≤19/38 first attempts plus eligible contingency. No next-batch preparation/execution. A completed saved batch displays results with zero calls. Interrupt requests pause; wait for settlement before export/closure.",'study.run_main_batch();\n',"main",True),
      ("review-batch","19. Inspect and acknowledge the batch","Inspect the previous output and complete conversation files; download the checkpoint, then run this acknowledgement. Saved batch ID is derived automatically; extra notes are optional. No claim of verified understanding/download. Return to section 17 or continue to reporting when all intended work is recorded.",'study.record_batch_review(notes="");\n',"review",False),
      ("report","20. Build the final or partial report","Read-only canonical reconstruction: twenty intended worlds, exact paired outcomes, unknown bounds, correct-prefix descriptive stratum, costs, failures, figures and limitations. No inference/reload. Download HTML/text/JSONL, CSV/plotting data and SVG/PNG.",'study.build_report();\n',"report",False),
      ("archive","21. Save and verify the final archive","Quiescent snapshot and exact fresh-directory analysis comparison, zero model calls. Save ZIP outside Kaggle. Save/download the executed notebook separately **without Save & Run All**. Links do not prove backup.",'study.save_checkpoint(verify=True);\n',"snapshot",False),
      ("close","Finish the session","Run after saving the checkpoint and executed notebook. Close models/controller, then stop Kaggle through its UI. Process exit does not establish provider deallocation; partial outcomes remain partial.",'study.finish_session();\n',"shutdown",False)
    ]: stage(*args)
    markdown("""## Recovery and support

Copy the needed ordinary commands into a cell. These recipes do not execute
merely by opening this appendix. Use the action matching saved state; never reset
a study to work around a blocked gate.

### Session facts and unexpected A/B/A differences

    study.configure_session(deadline="ACTUAL-FUTURE-ISO-TIME-WITH-OFFSET",
        evidence="Actual current provider allowance")
    # After a fresh provider observation only; duration is never extended by rerun:
    study.configure_session(remaining_minutes=ACTUAL_CURRENT_MINUTES,
        evidence="Actual fresh observation", refresh=True)
    # Only if readiness reports unequal A/B/A: inspect saved tokens/cache evidence,
    # then document the isolation interpretation; no extra probes/changed decoding:
    study.record_state_review("Actual trace-based findings")

### Status, pause and a safe checkpoint

    study.show_status();
    study.pause();  # Request only; an admitted call may still be active.
    # Wait for settlement / confirmed bounded termination, then:
    study.save_checkpoint();

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
If an envelope already passed, new session/replacement workers need **two contingency-charged probes**. For a fresh study no envelope has run: first use study.check_headroom() for its two ordinary probes. After an accepted envelope, use:

    study.check_headroom(reload=True);
    study.run_main_batch();  # Resume only a saved interrupted main scope.

Do not redo already accepted readiness/qualification just to restore the study.
Completed calls reuse durable raw replies without generation. Load/reload evidence
remains recorded; diagnostics, retries and warmups never disappear from accounting.

### Reconcile missing outcomes or termination evidence

Only after observed prior process/session exit, supply exact identifiers/evidence:

    study.reconcile_attempt( slot=0, attempt=EXACT_ATTEMPT_ID,
        evidence={"termination_confirmed": True, "reason": "Actual observed exit"});
    study.confirm_timeout_termination( slot=0, call="EXACT_CALL_ID",
        evidence={"termination_confirmed": True, "reason": "Actual observed exit"});

Admitted calls without durable output stay spent/unknown. Only one identical
pre-persistence infrastructure retry is eligible after confirmed termination.
Recorded timeouts, wrong, malformed or truncated replies never retry.

If saved bytes predate lost work, report partial recovery. Provide a defensible
spending bound and affected worlds; unbounded unknown spending blocks generation
while allowing reports:

    study.record_lost_spending(
        gap={"resolved": True, "upper": ACTUAL_UPPER_BOUND, "evidence": "Actual evidence"},
        affected_worlds=["main-XX"]);
    # For unbounded loss: resolved=False, upper=None. Never assume zero.

If restore used an unknown tail, bound only the ADDITIONAL exposure after that
boundary once old processes/session exit is confirmed. This retains older gap
charges and affected worlds; a later latest-tail choice never erases them:

    study.resolve_restore_tail(upper=ACTUAL_ADDITIONAL_BOUND,
        evidence="Actual confirmed exit and bounded tail evidence",
        affected_worlds=["EXACT-AFFECTED-WORLD"]);
    study.save_checkpoint(verify=True);

### Complete inspection, annotation and read-only reporting

    study.inspect(world="pilot-00", phase="retain", agent=0, audit_limit=None);
    study.links(all_files=True);
    study.annotate("unique-review-id", "ambiguous", ["exact/call/id"], "Trace-based notes");

Filtering changes only this view. Private submissions, truth and thinking are
audit material, never partner input. Thinking is not a faithful explanation.
No LLM judge is used.

With an initialized controller use study.build_report(). With only intact files,
the same method reconstructs reports read-only without creating workers/CUDA.
Outside the notebook, use its exact saved source:

    python scripts/i01_course.py --source SOURCE --run EXTRACTED status
    python scripts/i01_course.py --source SOURCE --run EXTRACTED report --output REPORT_DIR

A previous checkpoint uses its exact saved source for inference unless the reviewed pre-main continuation is explicitly requested. The repaired archive preserves both original and active source packets plus historical gates and prior-spending proof. Unknown tails/earlier gaps block admission until reconciled. Only the explicitly authorized independent rerun starts a separate budget; restoration never resets its accounting.
""")
    return dict(nbformat=4,nbformat_minor=5,cells=cells,
                metadata=dict(kernelspec=dict(display_name="Python 3",language="python",name="python3"),
                              language_info=dict(name="python"),kaggle=dict(accelerator="gpu",isInternetEnabled=True),
                              i01=dict(regime="i01-course-v1",research_execution="ordinary cells; one explicit bounded stage",
                                       qualification_policy="i01-direct-protocol-2026-10-15",
                                       run_all_can_execute_inference=True,kaggle_verified=False)))


def notebook():
    """Fresh, bounded Run All preparation; never imports an older experiment."""
    cells=[]
    def markdown(text):
        cells.append(dict(cell_type='markdown',id=f'i01-text-{len(cells):02d}',metadata={},source=text.splitlines(keepends=True)))
    def stage(identity,title,description,body,action=None,generation=False):
        markdown(f'## {title}\n\n{description}\n')
        cells.append(dict(cell_type='code',id=identity,metadata=dict(i01=dict(action=action,generation=generation)),
                          execution_count=None,outputs=[],source=body.splitlines(keepends=True)))
    markdown('''# I-01: fresh Run All

Start from the beginning with the repaired direct/nonthinking workflow.
Attach **only the matching i01-source.zip**, choose **GPU T4 ×2**, enable
**Internet**, fill in the two actual session facts in the first cell, then
**Run All**. No course-2/course-3 checkpoint or result is needed.

This notebook runs setup → self-check → weights → both resident workers → six
state checks → twelve new direct controls → two headroom probes → report and
verified downloadable checkpoint. **At most 20 first model attempts**, plus
eligible bounded infrastructure retries, within this new study's 500-attempt
limit. Wrong mathematical answers are measured; valid protocol is required.
Thinking inference, pilots, freeze and main experiments are separate stages.

Ordinary cells show each stage and can be rerun individually. Saved outcomes
are never resampled. A refusal preserves evidence and blocks generation at the
failed prerequisite; inspect the receipt before retrying. Models stay resident
after successful completion. Stop Kaggle when finished to release the allocation.
''')
    stages=[
        ('configuration','1. Set the session facts once',
         'Read the actual remaining session time and GPU allowance from Kaggle now. Enter the remaining session minutes and a short truthful allowance note. These are provider facts, not experiment settings; no quota or deadline is guessed. RUN_DIR needs changing only for a separate new study.',
         'RUN_DIR = "/kaggle/working/i01-fresh-study"\nSESSION_REMAINING_MINUTES = None  # Replace with the minutes actually remaining now.\nSESSION_ALLOWANCE_EVIDENCE = ""  # Describe the current allowance shown by Kaggle.\n'),
        ('workspace','2. Inspect the workspace','Select and verify the small source attachment. Inventory only; no installation or inference.',BOOTSTRAP),
        ('session-window','3. Record the fixed deadline','Record the observation BEFORE installation/downloads. Their elapsed time counts against this deadline. Rerunning this cell keeps the same deadline; use an explicit fresh observation to refresh it.',
         'study.configure_session(remaining_minutes=SESSION_REMAINING_MINUTES,\n    evidence=SESSION_ALLOWANCE_EVIDENCE);\n','window'),
        ('setup','4. Install the pinned runtime','Create the isolated environment without ensurepip. Verified pip bootstrap, pinned dependencies, project installation and import checks have visible progress/logs. The controller uses an isolated headless environment.',
         'study.install_runtime();\n','setup'),
        ('open-study','5. Start the new study','Explicit independent rerun: new study ID, zero prior attempts, no checkpoint import and no previous result reuse. Repeating this cell in the same destination retains its existing calls and budget. A different existing campaign is refused.',
         'study.start_new();\n','initialize'),
        ('selfcheck','6. Check implementation and tokenizer','Lightweight scripted mathematics, private views, persistence, accounting and archive checks, plus the native tokenizer. Zero model generations.',
         'study.check_implementation();\n','selfcheck'),
        ('weights','7. Download verified weights','Download/reuse the pinned model snapshot in scratch and verify its native files. No model inference.',
         'study.download_weights();\n','weights'),
        ('load','8. Load both workers','Load the pinned replicas once, one per T4. Actual inventory, current session deadline and fresh-state accounting must pass. Loading does not generate a reply.',
         'study.load_models();\n','load'),
        ('readiness','9. Check fresh-state readiness','Six A/B/A checks, three per worker. Real numerical/cache/provider defects block. Unequal A/B/A needs trace-based human review before proceeding; no automatic waiver or extra samples.',
         'study.check_readiness();\n','readiness',True),
        ('direct-screen','10. Run direct protocol qualification','Twelve fresh original/revised full-information controls. All twelve must be committed, valid JSON and legal protocol. Accuracy is diagnostic; a wrong answer alone does not reject the model. Completed replies are reused on cell rerun.',
         'study.qualify_direct();\n','screen',True),
        ('qualification','11. Inspect every direct control','Read-only truth/submission, correctness, validity, cost and failure-first raw inspection. Complete traces and raw replies are in the report/checkpoint. No thinking generation.',
         'study.inspect_qualification(mode="direct");\n'),
        ('envelope','12. Check full headroom','Two full-input/full-output probes, one per current replica. Require at least 1.5 GiB measured free memory on both T4s. Success starts no pilot or main work.',
         'study.check_headroom();\n','envelope',True),
        ('report','13. Build the report','Export qualification, failures, resources, all raw traces, tables and figures. All twenty main worlds stay explicitly unknown until their experiments are executed. Report generation keeps models resident.',
         'study.build_report();\n','report'),
        ('archive','14. Download and verify the checkpoint','Create the cumulative portable archive and verify read-only reconstruction. Download latest.zip and the executed notebook. Save this output without scheduling another Run All just to save it.',
         'study.save_checkpoint(verify=True);\n','snapshot')]
    for args in stages:stage(*args)
    markdown('''## After Run All

Expected on successful first attempts: **20 attempts here, zero prior charges**,
no thinking/pilot/main calls. Mathematical accuracy can be below 12/12 and is
reported without failing protocol qualification. Real protocol, resource and
isolation failures still stop execution and retain their evidence.

Download **/kaggle/working/i01-fresh-study/exports/latest.zip** and follow the
displayed links for reports, all conversations/raw replies, figures and receipts.
Every completed stage also publishes its cumulative checkpoint.

For the complete pilot/review/freeze/main workflow use the accompanying
**i01_course_research.ipynb**, whose research stages run individually. To keep
these loaded models, copy its pilot 1 and review cells into this notebook and
continue with the existing `study` object; do not repeat setup or loading.
Otherwise finish this controller before restoring the NEW checkpoint in the
research notebook, using its matching source and actual tail/exit evidence.
Newly loaded replicas need the separately charged two-probe reload validation.

Support commands (copy only the needed command into a new cell):

    study.show_status();
    study.inspect_qualification(mode="direct");
    study.inspect(audit_limit=None);  # Every raw call, no display limit.
    study.links(all_files=True);
    study.pause();  # Wait for an admitted call to settle before checkpoint/close.
    study.save_checkpoint(verify=True);
    study.record_state_review("Actual trace-based findings");  # Only if A/B/A needs review.
    study.configure_session(remaining_minutes=ACTUAL_CURRENT_MINUTES,
        evidence="Actual fresh provider observation", refresh=True);
    study.finish_session();  # Then stop Kaggle through its UI to release resources.

Do not replace failed gates, invent session facts or start another study to
bypass an error. Correct the demonstrated infrastructure error and resume its
saved scope. Wrong/malformed/truncated recorded model outcomes never retry.
''')
    return dict(nbformat=4,nbformat_minor=5,cells=cells,
                metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),
                              language_info=dict(name='python'),kaggle=dict(accelerator='gpu',isInternetEnabled=True),
                              i01=dict(regime='i01-course-v1',research_execution='fresh bounded preparation; Run All supported',
                                       qualification_policy='i01-direct-protocol-2026-10-15',attempt_scope='independent-study',
                                       run_all_supported=True,run_all_can_execute_inference=True,
                                       first_attempt_ceiling=20,kaggle_verified=False)))


def build(path, *, research=False):
    value=research_notebook() if research else notebook()
    for cell in value["cells"]:
        if cell["cell_type"]=="code": compile("".join(cell["source"]),cell["id"],"exec")
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return path


if __name__=="__main__":
    print(build(Path(__file__).resolve().parents[1]/"notebooks/i01_course_kaggle.ipynb"))
    print(build(Path(__file__).resolve().parents[1]/"notebooks/i01_course_research.ipynb",research=True))
