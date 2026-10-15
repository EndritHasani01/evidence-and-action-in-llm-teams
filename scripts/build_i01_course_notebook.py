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
        return manifest if manifest.get('execution_policy') == 'i01-whole-study-run-all-2026-10-15' and all('recovery/i01/'+name+'.py' in manifest['files'] for name in ('policy','continuation')) else None
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
    if release.get('execution_policy') != 'i01-whole-study-run-all-2026-10-15' or not all('recovery/i01/'+name+'.py' in release['files'] for name in ('policy','continuation')):
        raise RuntimeError('This notebook requires the whole-study Run All source packet; preserve old checkpoints and replace the active source attachment.')
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



def notebook():
    """One whole-study Run All, with ordinary finite cells and stable scopes."""
    cells=[]
    def markdown(text):
        cells.append(dict(cell_type='markdown',id=f'i01-text-{len(cells):02d}',metadata={},source=text.splitlines(keepends=True)))
    def stage(identity,title,description,body,action=None,generation=False):
        markdown(f'## {title}\n\n{description}\n')
        cells.append(dict(cell_type='code',id=identity,metadata=dict(i01=dict(action=action,generation=generation)),
                          execution_count=None,outputs=[],source=body.splitlines(keepends=True)))
    markdown("""# I-01: the complete experiment with Run All

Start a **fresh online T4 ?2 session**, attach only the matching **i01-source.zip**,
enable Internet and press **Run All**. No old checkpoint, forms, pilot approval
buttons or batch acknowledgements are required. Each ordinary cell performs its
named finite stage and can be run individually.

Setup ? fixed execution plan ? readiness/direct qualification/headroom ? all
three pilots/objective checks ? measured main admission ? all ten fixed main
batches (twenty worlds) ? full reports/figures ? verified archive ? worker shutdown.
Models stay resident throughout the research stages. Thinking is not selected.

The fresh study starts at **0/500 physical attempts**; direct-only first attempts
are at most **460**, with at most **28 contingency** attempts. Wrong mathematics
is measured, never an admission threshold. Strict protocol/evidence/runtime and
resource gates still stop safely. Every pilot, batch and settled error exports a
cumulative checkpoint. No existing outcome is regenerated on rerun.

The default is a **700-minute planning window** within your reported approximately
12-hour fresh session, leaving a 20-minute margin. This is an estimate, not a
verified provider quota/deadline. Reduce it below if time has already elapsed or
Kaggle shows less remaining. Setup/downloads consume the same fixed window.
Human communication/mechanism review remains retrospective and explicitly pending.
""")
    for args in [
        ('configuration','1. Fresh-session configuration',
         'Defaults assume a new approximately twelve-hour allocation. Check actual GPU allowance; lower the minutes for any time already elapsed. The evidence note describes an estimate truthfully. Do not copy a previous session deadline or extend the window by rerunning.',
         'RUN_DIR = "/kaggle/working/i01-run-all-study"\nSESSION_REMAINING_MINUTES = 700  # Conservative fresh-session estimate; reduce to actual time left.\nSESSION_ALLOWANCE_EVIDENCE = "User reports an approximately 12-hour session; 700-minute fresh-session planning bound, provider quota/deadline not independently verified."\n'),
        ('workspace','2. Verify source and inspect the workspace','Only the matching whole-study source release is accepted. Inventory only; no model loading or inference.',BOOTSTRAP),
        ('session-window','3. Record the fixed execution window','Record BEFORE installation and downloads. Reruns retain this deadline. No provider assignment, quota or release is inferred from the configured planning window.',
         'study.configure_session(remaining_minutes=SESSION_REMAINING_MINUTES,\n    evidence=SESSION_ALLOWANCE_EVIDENCE);\n','window'),
        ('setup','4. Install the pinned runtime','Verified pip bootstrap without ensurepip, unchanged pinned dependencies, isolated/headless controller, visible logs/progress. No host startup hooks or unpinned upgrades.',
         'study.install_runtime();\n','setup'),
        ('open-study','5. Start the independent study','New study at zero, no old checkpoint/result import. Repeating this cell reuses the same destination and preserves spending; an old shared campaign cannot be converted.',
         'study.start_new();\n','initialize'),
        ('selfcheck','6. Check implementation and native tokenizer','Focused scripted math/private-view/lifecycle/accounting/durability/archive checks and native token bounds. Zero model attempts.',
         'study.check_implementation();\n','selfcheck'),
        ('weights','7. Download and verify weights','Pinned model snapshot and actual storage/native file checks. Scratch caches are reused when valid.',
         'study.download_weights();\n','weights'),
        ('load','8. Load both resident T4 workers','Two fixed replicas; concise actual load/device evidence. Loading generates no hidden warmup. Inspection and research stages retain these replicas.',
         'study.load_models();\n','load'),
        ('plan','9. Lock the complete execution plan','Before the first model call, bind the unchanged manifest/settings, objective checks, ten fixed batches and retrospective review policy. Pilots cannot tune this configuration.',
         'study.plan_execution();\n','plan_execution'),
        ('readiness','10. Check fresh-state readiness','Six A/B/A calls. Cache/numerical/provider faults or unexplained unequal A/B/A stop; no automatic waiver or extra samples.',
         'study.check_readiness();\n','readiness',True),
        ('direct-screen','11. Qualify direct protocol','Twelve fixed original/revised controls. All twelve must be committed and protocol-valid. Wrong scalar answers alone pass protocol admission and remain visible outcomes.',
         'study.qualify_direct();\n','screen',True),
        ('qualification','12. Inspect qualification','Every planned direct control, truth/submission, validity, correctness, effort and failure-first raw audit. Complete raw evidence is downloadable.',
         'study.inspect_qualification(mode="direct");\n'),
        ('envelope','13. Check full headroom','Two full-input/full-output diagnostic probes, one per current load. Require at least 1.5 GiB measured free headroom on each T4.',
         'study.check_headroom();\n','envelope',True)
    ]:stage(*args)
    for number in (1,2,3):
        stage(f'pilot-{number}',f'Run pilot {number}',
              f'Pilot {number} only: prefix, literal retain/clear siblings and original/revised controls, at most twenty first attempts. Conversation and cumulative checkpoint appear automatically. No outcome-based replacement or extra seed.',
              f'study.run_pilot({number});\n','pilot',True)
        stage(f'check-pilot-{number}',f'Check pilot {number} automatically',
              'Require complete durable terminal episodes/controls, both original-team submissions, valid protocol, reconciled spending and intact runtime/export evidence. Mathematical errors and message quality do not gate admission. Useful communication remains unreviewed.',
              f'study.check_pilot({number});\n','check_pilot')
    stage('admit-main','Admit the unchanged main experiment',
          'All three objective pilot checks must pass. Record measured attempt/time feasibility under the already locked configuration. No human approval is invented and no pilot-driven tuning occurs. An inadequate forecast stops with a partial checkpoint.',
          'study.admit_main();\n','admit_main')
    for number in range(1,11):
        first=(number-1)*2
        stage(f'main-{number:02d}',f'Main batch {number}/10 ? worlds {first:02d} and {first+1:02d}',
              'Execute these two predetermined worlds, one per logical slot, at most 38 first attempts. Commit all terminal outcomes, show conversations and export before the next cell. Wrong/invalid recorded main replies remain measured failures. Rerunning this numbered cell never advances another batch or resamples.',
              f'study.run_main_batch({number});\n','automatic_main',True)
    stage('report','Build complete or honest partial reports',
          'All twenty intended worlds, paired outcomes/uncertainty, costs, protocol/qualification/pilot checks, full conversations/raw calls, failure analysis, limitations, tables and eight SVG/PNG figure pairs. Retrospective human review is visibly pending.',
          'study.build_report();\n','report')
    stage('archive','Verify the portable checkpoint and download results',
          'Quiescent cumulative ZIP and exact read-only fresh-directory reconstruction. Download latest.zip and the executed notebook. Checkpoints happen automatically even if you ignore their links during execution.',
          'study.save_checkpoint(verify=True);\n','snapshot')
    stage('close','Close model workers and controller',
          'Close after final export; the closing checkpoint retains actual process evidence. Stop Kaggle through its UI to release its allocation. Process closure and a link do not prove provider deallocation or an external download.',
          'study.finish_session();\n','shutdown')
    markdown("""## Results, errors and later restoration

The cumulative checkpoint is **/kaggle/working/i01-run-all-study/exports/latest.zip**;
reports, all conversations/raw outcomes, CSV tables and figures are under
**/kaggle/working/i01-run-all-study/reports/**. Download them and the executed
notebook outside the session. Save existing output without another inference run.

A real prerequisite failure stops further admission and keeps the last valid
archive plus receipts. A provider hard shutdown may occur before a new export;
no missing outcome or unbounded spending is silently assumed zero. Checkpoints
are already present; a convenient restore workflow can be added later without
having to reconstruct unsaved hours of work.

For inspection with intact files (copy only the needed commands into a cell):

    study.show_status();
    study.inspect(audit_limit=None);  # Every raw call, no display limit.
    study.links(all_files=True);
    study.build_report();  # Works read-only after controller closure.

Before closure, interrupt requests pause; wait for admitted calls to settle:

    study.pause();
    study.save_checkpoint(verify=True);
    study.finish_session();

For a later session, use this checkpoint's exact source and the existing explicit
restore/reopen commands in **docs/I01_KAGGLE.md**. Supply actual prior-exit/tail
and current-time facts. New loaded replicas require two charged reload probes;
do not repeat completed controls, pilot outcomes or earlier numbered batches.
Do not rerun the complete notebook to bypass a failed gate or reset its budget.

After execution, inspect all pilot/main conversations and add genuine human
annotations using the frozen rubric and exact call references. Automatic checks
establish evidence/protocol/resource eligibility, not meaningful communication,
human understanding, download completion or a favorable scientific effect.
""")
    return dict(nbformat=4,nbformat_minor=5,cells=cells,
                metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),
                              language_info=dict(name='python'),kaggle=dict(accelerator='gpu',isInternetEnabled=True),
                              i01=dict(regime='i01-course-v1',research_execution='whole-study Run All; finite numbered stages',
                                       qualification_policy='i01-direct-protocol-2026-10-15',
                                       execution_policy='i01-whole-study-run-all-2026-10-15',attempt_scope='independent-study',
                                       run_all_supported=True,run_all_scope='whole-study',run_all_can_execute_inference=True,
                                       first_attempt_ceiling=460,hard_attempt_limit=500,contingency_limit=28,
                                       human_review='retrospective_pending',kaggle_verified=False)))


def research_notebook():
    # Compatibility filename: both names deliver the same complete notebook.
    return notebook()


def build(path, *, research=False):
    value=notebook()
    for cell in value['cells']:
        if cell['cell_type']=='code':compile(''.join(cell['source']),cell['id'],'exec')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return path


if __name__=='__main__':
    for name in ('i01_course_kaggle.ipynb','i01_course_research.ipynb'):
        print(build(Path(__file__).resolve().parents[1]/'notebooks'/name))
