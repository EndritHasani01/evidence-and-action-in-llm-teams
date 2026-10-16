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
        return manifest if manifest.get('execution_policy') == 'i01-recorded-outcomes-run-all-2026-10-15' and all('recovery/i01/'+name+'.py' in manifest['files'] for name in ('policy','continuation')) else None
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
    if release.get('execution_policy') != 'i01-recorded-outcomes-run-all-2026-10-15' or not all('recovery/i01/'+name+'.py' in release['files'] for name in ('policy','continuation')):
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



def notebook(*, assisted=False):
    """One whole-study Run All, with ordinary finite cells and stable scopes."""
    if assisted:return assisted_notebook()
    cells=[]
    def markdown(text):
        cells.append(dict(cell_type='markdown',id=f'i01-text-{len(cells):02d}',metadata={},source=text.splitlines(keepends=True)))
    def stage(identity,title,description,body,action=None,generation=False):
        markdown(f'## {title}\n\n{description}\n')
        cells.append(dict(cell_type='code',id=identity,metadata=dict(i01=dict(action=action,generation=generation)),
                          execution_count=None,outputs=[],source=body.splitlines(keepends=True)))
    markdown("""# I-01: the complete experiment with Run All

Start a **fresh online T4 x2 session**, attach only the matching **i01-source.zip**,
enable Internet and press **Run All**. No old checkpoint, forms, pilot approval
buttons or batch acknowledgements are required. Each ordinary cell performs its
named finite stage and can be run individually.

Run setup, lock the execution plan, qualify the runtime and direct model, then
run three pilots, measured main admission and all ten fixed main batches
(twenty worlds), followed by reports, verified export and worker shutdown.
Models stay resident throughout the research stages. Thinking is not selected.

The fresh study starts at **0/500 physical attempts**; direct-only first attempts
are at most **460**, with at most **28 contingency** attempts. Wrong mathematics
is measured, never an admission threshold. The twelve scalar qualification
controls must be legal. After qualification, ordinary pilot errors, including
prefix, recovery and later controls, remain measured outcomes. Original-team
noncompletion does not veto admission. Invalid actions still deliver nothing.
Durable evidence, runtime and resource gates stop safely.
Every pilot, batch and settled error exports a
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
         'RUN_DIR = "/kaggle/working/i01-outcomes-study"\nSESSION_REMAINING_MINUTES = 700  # Conservative fresh-session estimate; reduce to actual time left.\nSESSION_ALLOWANCE_EVIDENCE = "User reports an approximately 12-hour session; 700-minute fresh-session planning bound, provider quota/deadline not independently verified."\n'),
        ('workspace','2. Verify source and inspect the workspace','Only the matching whole-study source release is accepted. Inventory only; no model loading or inference.',BOOTSTRAP),
        ('session-window','3. Record the fixed execution window','Record BEFORE installation and downloads. Reruns retain this deadline. No provider assignment, quota or release is inferred from the configured planning window.',
         'study.configure_session(remaining_minutes=SESSION_REMAINING_MINUTES,\n    evidence=SESSION_ALLOWANCE_EVIDENCE, basis="planning_estimate");\n','window'),
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
              'Require every scheduled episode/control to have terminal committed evidence, reconciled spending and intact runtime/export evidence. All ordinary prefix/recovery/control mistakes and terminal noncompletion are measured outcomes after scalar qualification. Compliance and original-team completion are shown separately. Useful communication remains unreviewed.',
              f'study.check_pilot({number});\n','check_pilot')
    stage('admit-main','Admit the unchanged main experiment',
          'All three objective pilot checks must pass. Record measured attempt/time feasibility under the already locked configuration. No human approval is invented and no pilot-driven tuning occurs. An inadequate forecast stops with a partial checkpoint.',
          'study.admit_main();\n','admit_main')
    for number in range(1,11):
        first=(number-1)*2
        stage(f'main-{number:02d}',f'Main batch {number}/10: worlds {first:02d} and {first+1:02d}',
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

The cumulative checkpoint is **/kaggle/working/i01-outcomes-study/exports/latest.zip**;
reports, all conversations/raw outcomes, CSV tables and figures are under
**/kaggle/working/i01-outcomes-study/reports/**. Download them and the executed
notebook outside the session. Save existing output without another inference run.

A real prerequisite failure stops further admission, attempts a settled partial export, closes workers with recorded acknowledgements and keeps the last valid
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
                                       execution_policy='i01-recorded-outcomes-run-all-2026-10-15',attempt_scope='independent-study',
                                       run_all_supported=True,run_all_scope='whole-study',run_all_can_execute_inference=True,
                                       first_attempt_ceiling=460,hard_attempt_limit=500,contingency_limit=28,
                                       human_review='retrospective_pending',kaggle_verified=False)))


def assisted_notebook():
    """Reuse the complete finite notebook with explicit assisted stage replacements."""
    value=notebook();cells=value['cells']
    policy='i01-assisted-feasibility-2026-10-16'
    def replace_text(cell,text):cell['source']=text.splitlines(keepends=True)
    replace_text(cells[0],'''# I-01: assisted recovery with one fixed Run All

Use a fresh online **T4 x2** session and the matching assisted **i01-source.zip**.
This notebook executes one precommitted condition: eight scalar qualification
controls, four single-call diagnostics, four balanced live pilots, then (only
if eligible) twenty fixed main worlds in ten batches. The two agents receive
one openly disclosed strategy/interface package; retain and clear share it.

The maximum is **480 ordinary physical attempts +20 contingency =500**. All
warmups, failures, diagnostics and eligible retries count. Main eligibility
requires complete pilot evidence, at least **3/4 correct original teams** and
**7/8 correct pilot controls**, current health and an adequate measured forecast.
There is no recovery-success, effect-direction, all-actions-legal or qualitative
message veto. If usefulness fails, preserve a complete feasibility report and
leave main unexecuted. No prompt/model tuning or repeat-until-pass is allowed.

Ordinary main mistakes stay in the fixed population. Scalar/probe success does
not certify live collaboration. Each cell has one finite, idempotent scope;
completed stages spend zero on rerun. Models remain resident through the work.
Setup/downloads consume the same fixed window. The 700-minute planning estimate
is not a provider allowance guarantee; reduce it to the actual time remaining.

Running this notebook is a separate explicit execution request. The software's
CPU checks and design approval alone authorize no inference. Human trace review
remains retrospective and visibly pending. Download every checkpoint and the
executed notebook; a provider may end the session before the final export.
''')
    workspace=BOOTSTRAP.replace('i01-recorded-outcomes-run-all-2026-10-15',policy)
    workspace=workspace.replace('Study(source_root, run=RUN_DIR)','Study(source_root, run=RUN_DIR, assisted=True)')
    workspace=workspace.replace('Path(RUN_DIR).resolve():','Path(RUN_DIR).resolve() or not study.assisted:')
    descriptions={
        'direct-screen':('Qualify the eight direct controls','All eight fixed qualification actions must be legal and committed. Scalar accuracy here is diagnostic; no resampling.'),
        'qualification':('Inspect qualification','Four qualification worlds, eight planned controls; complete raw evidence, accuracy, legality and unknown coverage.'),
        'admit-main':('Make the one fixed feasibility decision','All four pilot scopes must be settled; require 3/4 correct original teams and 7/8 correct pilot scalar controls plus current health/resources. No recovery-effect or qualitative veto. Failure stops scientific admission with all main outcomes unknown.'),
        'report':('Build the complete or truthful feasibility/partial report','All twenty intended main worlds, unknown bounds, stratified paired uncertainty, effort coverage, physical/logical validity denominators, exact process tables, fixed casebook, diagnostics and eight figure pairs. Human annotations remain pending unless supplied.')}
    for i,cell in enumerate(cells):
        if cell['cell_type']!='code':continue
        identity=cell['id']
        if identity=='configuration':replace_text(cell,''.join(cell['source']).replace('i01-outcomes-study','i01-assisted-study'))
        if identity=='workspace':replace_text(cell,workspace)
        if identity in descriptions:
            title,description=descriptions[identity];replace_text(cells[i-1],f'## {title}\n\n{description}\n')
        if identity.startswith('main-'):
            number=int(identity.split('-')[1]);first=(number-1)*2
            replace_text(cells[i-1],f'## Main batch {number}/10: worlds {first:02d} and {first+1:02d}\n\nExecute these fixed worlds, at most 38 first attempts. Different devices may overlap; same-device worlds serialize by index. All ordinary failures remain outcomes. Export before the next batch; reruns reuse exact saved data.\n')
    def pair(identity,title,description,body,action,generation=False):
        return [dict(cell_type='markdown',id='assisted-text-'+identity,metadata={},source=f'## {title}\n\n{description}\n'.splitlines(keepends=True)),
                dict(cell_type='code',id=identity,metadata=dict(i01=dict(action=action,generation=generation)),
                     execution_count=None,outputs=[],source=body.splitlines(keepends=True))]
    position=next(i for i,c in enumerate(cells) if c.get('id')=='envelope')+1
    cells[position:position]=pair('diagnostics','Run four supplied-view diagnostics','D00–D03 once each. Record actual target actions; nonpasses do not veto main or tune the fixed candidate. Scripted histories are diagnostic fixtures, not naturally generated collaboration.',
        'study.run_diagnostics();\n','diagnostics',True)+pair('prepared-checkpoint','Verify the preparation checkpoint','Quiescent portable export after diagnostics; actual measured export cost is required before admitting pilots.',
        'study.save_checkpoint(verify=True);\n','snapshot')
    position=next(i for i,c in enumerate(cells) if c.get('id')=='check-pilot-3')+1
    cells[position:position]=pair('pilot-4','Run pilot 4','Fourth owner/first-speaker cell; execute prefix, both siblings and two controls once, despite ordinary model mistakes.',
        'study.run_pilot(4);\n','pilot',True)+pair('check-pilot-4','Check pilot 4 evidence','Terminal committed scopes, spending and export/health checks. The separate main decision applies the fixed 3/4 and 7/8 thresholds.',
        'study.check_pilot(4);\n','check_pilot')
    for cell in cells:
        if cell['cell_type']=='markdown':
            text=''.join(cell['source']).replace('i01-outcomes-study','i01-assisted-study')
            text=text.replace('two charged reload probes','six current-load state checks and two envelopes, all charged to the 20-attempt reserve')
            replace_text(cell,text)
    value['metadata']['i01'].update(regime='i01-course-assisted-v2',execution_policy=policy,
        first_attempt_ceiling=480,contingency_limit=20,qualification_worlds=4,diagnostic_calls=4,pilot_worlds=4,
        main_usefulness='3/4 correct originals and 7/8 correct pilot scalar controls; intact health/evidence/resources')
    return value


def research_notebook(*, assisted=False):
    # Compatibility filename: both names deliver the same complete notebook.
    return notebook(assisted=assisted)


def build(path, *, research=False, assisted=False):
    value=notebook(assisted=assisted)
    for cell in value['cells']:
        if cell['cell_type']=='code':compile(''.join(cell['source']),cell['id'],'exec')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return path


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--assisted',action='store_true')
    args=parser.parse_args()
    for name in ('i01_course_kaggle.ipynb','i01_course_research.ipynb'):
        print(build(Path(__file__).resolve().parents[1]/'notebooks'/name,assisted=args.assisted))
