"""Build a small committed course dataset ZIP and its orchestration notebook."""

import argparse
import hashlib
import importlib.metadata
import io
import json
from pathlib import Path
import subprocess
from urllib.request import urlopen
import zipfile

from scripts.build_kaggle_bundle import archive_manifest, candidate_lock
from scripts.build_course_smoke_packet import preparation_review

REPORT_PACKAGES = ("matplotlib", "contourpy", "cycler", "fonttools", "kiwisolver", "pillow",
                   "pyparsing", "python-dateutil", "six")
# Explicit execution dependencies, not the whole repository. The existing three
# mandatory host checks require these helper modules and two original populations.
RUNTIME_SCRIPTS = ("course_kaggle_workflow", "course_kaggle_bootstrap", "m5_course_smoke",
    "m5_course_smoke_assets", "m5_course_preparation", "m5_kaggle_preflight", "m5_model_feasibility")
HOST_HELPERS = ("worker_checks", "attempt_checks", "durable_checks", "event_checks",
    "replay_checks", "round_checks", "protocol_checks", "worker_fixture", "references", "loading_checks", "generation_checks")
FIXTURES = ("population_course.json", "schedules_course.json", "course_capacity.json.gz",
    "population_target.json", "population_fallback.json")
SOURCE_PATHS = ("recovery", "pyproject.toml", "PROJECT_SPECIFICATION.md", "tests/__init__.py",
    *("scripts/"+name+".py" for name in RUNTIME_SCRIPTS),
    *("tests/"+name+".py" for name in HOST_HELPERS),
    *("tests/fixtures/"+name for name in FIXTURES),
    "configs/course-kaggle.json", "configs/course-smoke-launch.json", "configs/course-cpu-reproduction.txt",
    "notebooks/validation/course-kaggle/repair-predecessor.json",
    "notebooks/validation/course-kaggle/repair-candidates",
    "notebooks/validation/course-m5-preparation/inputs/smoke-requests.json.gz",
    "notebooks/validation/course-m5-preparation/inputs/memory-review.json",
    "notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json",
    "notebooks/validation/course-m5-r7/native-tightening-source.json",
    "notebooks/validation/course-m5-r7/outside-provenance.json",
    "notebooks/validation/course-m5-r7/offline-memory-review.json",
    "notebooks/validation/course-m5-r7/loading-review-source.json")


def report_wheels(base):
    """Pin only CPU rendering additions; leave the reviewed inference wheels exact."""
    result = []
    existing = {w["name"] for w in base}
    for name in REPORT_PACKAGES:
        if name in existing:
            continue
        version = importlib.metadata.version(name)
        with urlopen(f"https://pypi.org/pypi/{name}/{version}/json", timeout=30) as response:
            metadata = json.load(response)
        options = []
        for item in metadata["urls"]:
            filename = item["filename"]
            if item["packagetype"] != "bdist_wheel" or item.get("yanked"):
                continue
            pure = filename.endswith("-py3-none-any.whl") or filename.endswith("-py2.py3-none-any.whl")
            native = ("-cp313-cp313-" in filename and "x86_64" in filename and "manylinux" in filename
                      and any(tag in filename for tag in ("manylinux_2_17", "manylinux_2_24", "manylinux_2_27", "manylinux_2_28", "manylinux2014")))
            if pure or native:
                options.append((not pure, filename, item))
        if not options:
            raise ValueError("no pinned Linux CPython 3.13 report wheel: "+name)
        item = min(options, key=lambda v:(v[0], v[1]))[2]
        result.append(dict(name=name, version=version, filename=item["filename"], url=item["url"],
            bytes=item["size"], sha256=item["digests"]["sha256"]))
    return result


def notebook(manifest_sha, commit):
    def cell(kind, source, name):
        value = dict(cell_type=kind, id=name, metadata={}, source=source.splitlines(keepends=True))
        if kind == "code":
            value.update(outputs=[], execution_count=None)
        return value
    introduction = """# Course research · Run All on Kaggle T4 ×2

Upload this notebook and the **small research dataset ZIP**, attach the dataset,
select **T4 ×2**, turn Internet **On**, then **Run All**.
The notebook downloads the pinned dependencies and original model checkpoint,
verifies their native hashes and versions, and advances automatically:

The research source is a packed archive and its integrity manifest.
Cell 3 extracts the required files locally after Kaggle starts the session.

**Hardware → first 90 slots → full pilot → audit and freeze → complete main matrix
→ independently reproduced analysis → results and resume exports.**

Progress appears every 15 seconds; portable backups update every ten minutes.
No action switching, separate asset upload, or manual stage restart is needed.

**A complete result depends on every mandatory gate passing and enough session time.**
Failed scientific checks finish with a limited result and preserved evidence.
GPU mode is detected automatically. Running this notebook on T4 ×2 authorizes
the fixed hardware/development/main sequence and a freeze conditional on the
scientific gates. Use Accelerator **None** for CPU reporting. GPU work requires the pinned
Linux x86_64 **Python 3.13** candidate; incompatible images stop safely.

Keep the dataset private. Later sessions also attach **course-resume.payload**;
Run All resumes exact saved inputs without resampling completed calls.
For this final-online-4 repair, attach only the new dataset for the first run.
Do not attach old final-online-3/4/5 resume payloads: this repaired source starts fresh.
Later sessions attach this same dataset and one latest matching resume export.
For durable background execution, use **Save Version → Save & Run All**;
see the [Kaggle notebook guide](https://www.kaggle.com/docs/notebooks).
"""
    select = """# Normally leave these unchanged and select Run All.
ACTION = "run_all"       # alternatives: status, analyze, export
SESSION_HOURS = 10       # controller window; reserves time for a safe export
RESUME_ZIP = None        # automatically detects a single attached resume bundle

# Automatic GPU detection and timing; no budget or approval forms.
import os,time
from pathlib import Path
devices=Path('/proc/driver/nvidia/gpus')
ENABLE_GPU=ACTION=='run_all' and devices.is_dir() and bool(list(devices.iterdir()))
SESSION_STARTED_AT=time.strftime('%Y-%m-%dT%H:%M:%S+00:00',time.gmtime())
PACKAGE_DIR=ASSETS_ZIP=None
RUN_SETTINGS={}         # optional advanced overrides; normal execution needs none
"""
    bootstrap = f"""import hashlib,json,os,shutil,stat,sys,time,zipfile
from pathlib import Path,PurePosixPath
from IPython.display import display,FileLink,HTML
EXPECTED_MANIFEST_SHA256={manifest_sha!r}
EXPECTED_SOURCE_COMMIT={commit!r}
workspace=Path(os.environ.get('COURSE_WORKSPACE','/kaggle/working/course-workspace-{commit[:12]}')).resolve()
workspace.mkdir(parents=True,exist_ok=True)
bundle=workspace/'bundle'
inputs=Path(os.environ.get('COURSE_INPUT','/kaggle/input'))
def attached(name,explicit=None):
    if explicit: return Path(explicit).resolve()
    matches=(list(inputs.rglob('course-resume*.payload'))+list(inputs.rglob('course-resume*.zip'))) if name=='course-resume.zip' else list(inputs.rglob(name))
    if name=='course-resume.zip' and len(matches)>1:
        external=[p for p in matches if not (p.parent/'source-manifest.json').is_file()
            or hashlib.sha256((p.parent/'source-manifest.json').read_bytes()).hexdigest()!=EXPECTED_MANIFEST_SHA256]
        if len(external)==1:
            print('Resume: using the separately attached export instead of the packaged repair seed')
            matches=external
    if len(matches)>1: raise ValueError('Select one exact '+name+' in the options cell')
    return matches[0] if matches else None
def extract_fresh(archive,target):
    if target.exists(): raise FileExistsError(target)
    with zipfile.ZipFile(archive) as z:
        names=set()
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            if p.is_absolute() or '..' in p.parts or '\\\\' in i.filename or ':' in i.filename or i.filename in names or stat.S_ISLNK(i.external_attr>>16):
                raise ValueError('Unsafe/duplicated archive member')
            names.add(i.filename)
        target.mkdir(parents=True)
        z.extractall(target)
resume=attached('course-resume.zip',RESUME_ZIP)
if resume is None:
    # Kaggle normally expands uploaded ZIPs. Recognize the extracted original
    # bundle instead of accidentally starting a new set of worker files.
    options=[p.parent for p in inputs.rglob('operator-config.json')
        if (p.parent/'inputs/population.json').is_file()
        and (p.parent/'source/source-manifest.json').is_file()
        and hashlib.sha256((p.parent/'source/source-manifest.json').read_bytes()).hexdigest()==EXPECTED_MANIFEST_SHA256]
    if len(options)>1: raise ValueError('Select the exact extracted resume directory with RESUME_ZIP')
    resume=options[0] if options else None
if not bundle.exists():
    if resume and resume.is_dir():
        members=list(resume.rglob('*'))
        if any(p.is_symlink() or p.name.endswith(('-wal','-shm','.owner','.tmp')) for p in members):
            raise ValueError('Resume requires the ordinary exported SQLite backups, without live WAL/locks or symlinks')
        shutil.copytree(resume,bundle)
    elif resume: extract_fresh(resume,bundle)
    else: bundle.mkdir()
source=bundle/'source'
if not source.exists():
    options=[Path(PACKAGE_DIR)/'source-manifest.json'] if PACKAGE_DIR else list(inputs.rglob('source-manifest.json'))
    matches=[p for p in options if hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED_MANIFEST_SHA256]
    if len(matches)!=1: raise ValueError('Attach the exact course dataset ZIP (Kaggle extracts it), or set PACKAGE_DIR')
    package=matches[0].parent
    manifest=json.loads(matches[0].read_bytes())
    payload=package/manifest.get('payload_filename','missing.payload')
    if payload.exists():
        if payload.is_symlink() or not payload.is_file() or payload.stat().st_size!=manifest['archive_bytes'] or hashlib.sha256(payload.read_bytes()).hexdigest()!=manifest['archive_sha256']:
            raise ValueError('Packed research archive differs')
        with zipfile.ZipFile(payload) as archive:
            if len(archive.infolist())!=len(manifest['members']) or set(archive.namelist())!=set(manifest['members']):
                raise ValueError('Packed research member set differs')
            for item in archive.infolist():
                expected=manifest['members'][item.filename]
                if item.file_size!=expected['bytes'] or hashlib.sha256(archive.read(item)).hexdigest()!=expected['sha256']:
                    raise ValueError('Packed source bytes differ: '+item.filename)
        extract_fresh(payload,source)
    else:
        # Read previously delivered loose layouts as well as compact datasets.
        source.mkdir()
        for name,expected in manifest['members'].items():
            p=PurePosixPath(name)
            if p.is_absolute() or '..' in p.parts or '\\\\' in name or ':' in name: raise ValueError('Unsafe source member')
            original=package/name
            if not original.is_file() or original.is_symlink() or original.stat().st_size!=expected['bytes'] or hashlib.sha256(original.read_bytes()).hexdigest()!=expected['sha256']:
                raise ValueError('Source bytes differ: '+name)
            target=source/name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(original,target)
    shutil.copyfile(matches[0],source/'source-manifest.json')
manifest_bytes=(source/'source-manifest.json').read_bytes()
if hashlib.sha256(manifest_bytes).hexdigest()!=EXPECTED_MANIFEST_SHA256: raise ValueError('Resume requires the identical source package/notebook')
manifest=json.loads(manifest_bytes)
if (source/'SOURCE_COMMIT.txt').read_text().strip()!=EXPECTED_SOURCE_COMMIT: raise ValueError('Source commit differs')
for name,expected in manifest['members'].items():
    p=source/name
    if p.is_symlink() or not p.is_file() or p.stat().st_size!=expected['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=expected['sha256']:
        raise ValueError('Canonical source changed: '+name)
display(HTML('<div style="padding:16px;background:#e8f3f3;border-radius:10px"><b>Source verified</b> · '+EXPECTED_SOURCE_COMMIT[:12]+'<br>20 main worlds · 6,280 logical main uses · 5 separate development worlds</div>'))
repair_receipt=bundle/'repair/receipt.json'
if repair_receipt.exists():
    repaired=json.loads(repair_receipt.read_bytes())
    print('Repair resume: preserving',repaired['preserved_current_attempts'],'original outcomes;',
          repaired['cumulative_attempts'],'of',repaired['attempt_limit'],'attempts already recorded.',flush=True)
"""
    bootstrap = ("import os,json,traceback\nfrom pathlib import Path\nSOURCE_READY=False\nsource=None\n"
        f"workspace=Path(os.environ.get('COURSE_WORKSPACE','/kaggle/working/course-workspace-{commit[:12]}')).resolve()\n"
        "bundle=workspace/'bundle'\ntry:\n"+
        "".join("    "+line+"\n" for line in bootstrap.splitlines())+
        "    SOURCE_READY=True\nexcept (Exception,KeyboardInterrupt) as error:\n"
        "    bundle.mkdir(parents=True,exist_ok=True)\n"
        "    logs=bundle/'logs'; logs.mkdir(exist_ok=True)\n"
        "    (logs/'source-error.txt').write_text(traceback.format_exc(),encoding='utf-8')\n"
        "    (bundle/'last-action.json').write_text(json.dumps(dict(status='source_setup_failed',reason=str(error),inference_calls=0)))\n"
        "    print('Source setup failed:',error,'; no inference will run. The final cell exports the logs.')\n")
    settings = """# Automatic configuration; no manual budget or memory proof.
if not SOURCE_READY:
    CONFIG=dict(execute_gpu=False,allocated_at=SESSION_STARTED_AT)
    config_path=bundle/'operator-config.json'
    print('Source setup failed; execution will be skipped and evidence exported.')
else:
    saved_config=bundle/'operator-config.json'
    CONFIG=json.loads((saved_config if saved_config.exists() else source/'configs/course-kaggle.json').read_bytes())
    CONFIG.update(execute_gpu=ENABLE_GPU,continuous_assignment=(ACTION=='run_all'),
        automatic_pilot_review=True,max_work_seconds=SESSION_HOURS*3600,finalization_seconds=900,
        resource_policy='observe',allocated_at=SESSION_STARTED_AT,assignment_clock_scope='observed_notebook_interval',
        hardware_review=dict(acceptance='measured_stress'))
    if ENABLE_GPU:
        CONFIG['authorizations']={key:'Operator Run All authorizes the pinned course '+key+' stage; scientific gates must pass'
            for key in ('weights','hardware','pilot','freeze','main')}
    for key,value in RUN_SETTINGS.items():
        if isinstance(value,dict): CONFIG.setdefault(key,{}).update(value)
        else: CONFIG[key]=value
    config_path=bundle/'operator-config.json'
    config_path.write_text(json.dumps(CONFIG,indent=2)+'\\n')
"""
    run = """import queue,threading,subprocess,signal
def bounded_child(arguments,limit):
    # The repo owns scientific work; this cell only streams its process output.
    logs=bundle/'logs'; logs.mkdir(exist_ok=True)
    log=logs/('action-'+time.strftime('%Y%m%dT%H%M%S',time.gmtime())+'-'+str(time.time_ns())+'.log')
    process=subprocess.Popen([str(a) for a in arguments],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
        text=True,bufsize=1,start_new_session=(os.name!='nt'),cwd=workspace,
        env=dict(os.environ,MPLBACKEND='Agg'))
    lines=queue.Queue()
    def collect():
        for line in process.stdout: lines.put(line)
    reader=threading.Thread(target=collect,daemon=True); reader.start()
    deadline=time.monotonic()+limit
    started=time.monotonic(); heartbeat=started
    try:
        with log.open('w',encoding='utf-8') as output:
            while process.poll() is None or reader.is_alive() or not lines.empty():
                if time.monotonic()>=deadline: raise TimeoutError('Notebook controller deadline; preserve/export and Stop Session')
                if time.monotonic()-heartbeat>=15:
                    print(time.strftime('%H:%M:%S UTC',time.gmtime()),'|',Path(str(arguments[2])).name,
                          '| elapsed',round(time.monotonic()-started),'s | log:',log.name,flush=True)
                    heartbeat=time.monotonic()
                try: line=lines.get(timeout=1)
                except queue.Empty: continue
                output.write(line); output.flush(); print(line,end='',flush=True)
    finally:
        if process.poll() is None:
            if os.name!='nt': os.killpg(process.pid,signal.SIGTERM)
            else: process.terminate()
            try: process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                if os.name!='nt': os.killpg(process.pid,signal.SIGKILL)
                else: process.kill()
                process.wait(timeout=5)
        reader.join(timeout=2)
        if not reader.is_alive(): process.stdout.close()
    return process.returncode

receipt=None
bootstrap_output=None
assigned=False
try:
    if not SOURCE_READY:
        raise RuntimeError('Source setup failed; see logs/source-error.txt. No experiment was started.')
    if ACTION=='inspect':
        print('Source verified. Default Run All automatically orchestrates the authorized stages.')
    else:
        gpu_action=ACTION in ('hardware','capability','pilot','main') or ACTION=='run_all' and ENABLE_GPU
        if gpu_action and not ENABLE_GPU: raise ValueError('GPU execution requires explicit scoped authorizations in the setup cell')
        assigned=Path('/proc/driver/nvidia/gpus').is_dir() and bool(list(Path('/proc/driver/nvidia/gpus').iterdir()))
        if assigned and ACTION=='run_all' and (not ENABLE_GPU or not CONFIG.get('allocated_at')):
            raise ValueError('Assigned GPUs are chargeable: complete the authorized setup cell, or select Accelerator None for CPU reporting')
        if assigned and ACTION!='run_all' and not gpu_action and CONFIG.get('resource_policy')!='observe':
            raise ValueError('Use Accelerator None for standalone CPU actions; assigned idle time is chargeable')
        assets=attached('course-assets.zip',ASSETS_ZIP)
        if assets is None:
            options=[p.parent for p in inputs.rglob('prepared-assets.json') if (p.parent/'checkpoint').is_dir() and (p.parent/'wheels').is_dir()]
            if len(options)>1: raise ValueError('Select the exact asset directory with ASSETS_ZIP')
            assets=options[0] if options else None
        gpu_receipt=workspace/'gpu-environment'/'bootstrap'/'bootstrap.json'
        cpu_receipt=workspace/'cpu-environment'/'bootstrap'/'bootstrap.json'
        kind='setup' if ACTION=='setup' else 'gpu-environment' if gpu_action or gpu_receipt.exists() or assets and not cpu_receipt.exists() else 'cpu-environment'
        environment=workspace/kind
        bootstrap_output=environment/'bootstrap'
        receipt=bootstrap_output/'bootstrap.json'
        if receipt.exists():
            previous=json.loads(receipt.read_bytes())
            python=Path(previous.get('interpreter') or '/missing')
            asset_path=CONFIG.get('assets_receipt') or previous.get('assets_receipt')
            reusable=previous.get('status')!='blocked' and python.is_file()
            if asset_path:
                reusable=reusable and Path(asset_path).is_file() and Path(previous.get('hf_cache','/missing')).is_dir()
            if reusable and asset_path:
                # A saved setup receipt is not proof that cached files still match.
                verification=[python,'-I','-c',
                    "import sys,types; from pathlib import Path; scripts=types.ModuleType('scripts'); scripts.__path__=[str(Path(sys.argv[1])/'scripts')]; sys.modules['scripts']=scripts; from scripts.m5_course_smoke_assets import verify_assets; import json; verify_assets(Path(sys.argv[1]),dict(source_manifest=str(Path(sys.argv[1])/'source-manifest.json'),assets_receipt=sys.argv[2],hf_cache=sys.argv[3],candidate=sys.argv[4] if len(sys.argv)>4 else None))",
                    source,asset_path,previous['hf_cache']]+([CONFIG['candidate']] if CONFIG.get('candidate') else [])
                reusable=bounded_child(verification,180)==0
            if not reusable:
                # Preserve small receipts; bootstrap verifies/reuses the installation
                # independently of an interrupted checkpoint download.
                print('Setup: retaining diagnostics; checking installation/download resumption',flush=True)
                report_path=Path(CONFIG.get('setup_resume_report') or previous.get('setup_report') or receipt.parent/'report.json')
                if report_path.is_file(): CONFIG['setup_resume_report']=str(report_path)
                cache=Path(previous.get('hf_cache') or environment/'scratch/hub')
                if cache.is_dir() and previous.get('source_commit')==EXPECTED_SOURCE_COMMIT:
                    CONFIG['hf_cache']=str(cache)
                config_path.write_text(json.dumps(CONFIG,indent=2)+'\\n')
                bootstrap_output=environment/('bootstrap-retry-'+str(time.time_ns()))
                receipt=bootstrap_output/'bootstrap.json'
        if not receipt.exists():
            arguments=[sys.executable,'-I',source/'scripts/course_kaggle_bootstrap.py']
            if ACTION=='setup': arguments+=['setup','--config',config_path]
            elif kind=='gpu-environment':
                if assets is None: arguments+=['online','--config',config_path]
                else: arguments+=['restore','--assets',assets,'--config',config_path]
            else: arguments+=['cpu','--config',config_path]
            arguments+=['--root',source,'--scratch',environment/'scratch','--output',bootstrap_output]
            if bounded_child(arguments,1800)!=0:
                blocked=json.loads(receipt.read_bytes()) if receipt.is_file() else {}
                raise RuntimeError(blocked.get('reason') or 'Bootstrap failed before writing its receipt; see the retained log')
            pointer=workspace/kind/'bootstrap'/'bootstrap.json'
            if pointer!=receipt:
                pointer.parent.mkdir(parents=True,exist_ok=True)
                # Preserve original receipt/logs; the pointer holds the verified current setup.
                if pointer.exists(): shutil.copyfile(pointer,pointer.with_name('bootstrap-before-'+str(time.time_ns())+'.json'))
                shutil.copyfile(receipt,pointer)
        runtime=json.loads(receipt.read_bytes())
        # Bootstrap derives a resumed candidate from its existing gate evidence.
        # Reload that selection before merging runtime paths and saving config.
        CONFIG=json.loads(config_path.read_bytes())
        if CONFIG.get('assets_receipt') and Path(CONFIG['assets_receipt']).is_file():
            runtime['assets_receipt']=CONFIG['assets_receipt']
        if runtime.get('status')=='blocked': raise RuntimeError(runtime['reason'])
        # Preserve setup/hash/version evidence in every portable resume export.
        bootstrap_evidence=bundle/'environment-receipts'/(kind+'-'+bootstrap_output.name)
        bootstrap_evidence.mkdir(parents=True,exist_ok=True)
        for path in bootstrap_output.rglob('*'):
            if path.is_file() and path.name!='source-manifest.json':
                target=bootstrap_evidence/path.relative_to(bootstrap_output)
                target.parent.mkdir(parents=True,exist_ok=True)
                if target.exists() and target.read_bytes()!=path.read_bytes():
                    target=bootstrap_evidence/(str(time.time_ns())+'-'+path.name)
                if not target.exists(): shutil.copyfile(path,target)
        if runtime.get('assets_receipt') and not runtime.get('requires_dataset_restore'):
            CONFIG.update(assets_receipt=runtime['assets_receipt'],hf_cache=runtime['hf_cache'])
            shutil.copyfile(runtime['assets_receipt'],bundle/'asset-receipt.json')
        config_path.write_text(json.dumps(CONFIG,indent=2)+'\\n')
        if ACTION not in ('setup','restore'):
            arguments=[runtime['interpreter'],'-I',source/'scripts/course_kaggle_workflow.py',
                '--root',source,'--bundle',bundle,'--config',config_path,'--action',ACTION]
            limit=(CONFIG.get('provider_session_seconds') or CONFIG['max_work_seconds'])+2100 if gpu_action else 2100
            code=bounded_child(arguments,limit)
            final=json.loads((bundle/'last-action.json').read_bytes()) if (bundle/'last-action.json').exists() else {}
            print('Workflow:',final.get('status','no final receipt'),'| process exit',code,
                  '|',final.get('reason') or 'Final cell exports results and resume evidence.',flush=True)
except (Exception,KeyboardInterrupt) as error:
    (bundle/'logs').mkdir(exist_ok=True)
    (bundle/'logs'/('notebook-error-'+str(time.time_ns())+'.txt')).write_text(traceback.format_exc(),encoding='utf-8')
    failure=dict(action=ACTION,status='blocked_or_safely_stopped',reason=type(error).__name__+': '+str(error),
        gates_bypassed=False,assignment_clock=CONFIG.get('allocated_at'),provider_release_confirmed=False)
    if locals().get('receipt') and Path(receipt).is_file():
        setup=json.loads(Path(receipt).read_bytes())
        if setup.get('status')=='blocked':
            failure.update(reason=setup.get('reason') or failure['reason'],setup_stage=setup.get('stage'),
                setup_report=setup.get('setup_report'),weights_staged=setup.get('weights_staged',False))
            CONFIG['setup_resume_report']=setup.get('setup_report')
            config_path.write_text(json.dumps(CONFIG,indent=2)+'\\n')
    (bundle/'last-action.json').write_text(json.dumps(failure,indent=2)+'\\n')
    if locals().get('bootstrap_output') and bootstrap_output.is_dir():
        evidence=bundle/'environment-receipts'/(kind+'-failed-'+time.strftime('%Y%m%dT%H%M%S',time.gmtime())+'-'+str(time.time_ns()))
        evidence.mkdir(parents=True,exist_ok=True)
        for path in bootstrap_output.rglob('*'):
            if path.is_file() and path.name!='source-manifest.json':
                target=evidence/path.relative_to(bootstrap_output)
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(path,target)
    if locals().get('assigned'):
        try:
            ids=subprocess.check_output(['nvidia-smi','--query-gpu=uuid','--format=csv,noheader'],text=True,timeout=5)
            physical_devices=[line.strip() for line in ids.splitlines() if line.strip()]
        except Exception: physical_devices=[]
        old_run=json.loads((bundle/'run.json').read_bytes()) if (bundle/'run.json').exists() else None
        stage='main' if old_run and old_run['freeze'] else 'pilot' if old_run else 'hardware'
        refusal_receipt=dict(config=CONFIG,allocated_at=CONFIG.get('allocated_at'),physical_devices=physical_devices,
            stage=stage,reason=failure['reason'],observed_at=time.strftime('%Y-%m-%dT%H:%M:%S+00:00',time.gmtime()))
        refusals=bundle/'bootstrap-refusals'; refusals.mkdir(exist_ok=True)
        (refusals/(time.strftime('%Y%m%dT%H%M%S',time.gmtime())+'-'+str(time.time_ns())+'.json')).write_text(json.dumps(refusal_receipt,indent=2)+'\\n')
    print(failure['reason'])

"""
    export = """# Run this cell after an action finishes/fails. It never invokes inference.
# Stdlib fallback also exports setup/refusal evidence before project installation.
import sqlite3,tempfile
from contextlib import closing
# A small results export accompanies the complete reproducibility/resume ZIP.
import html
last=json.loads((bundle/'last-action.json').read_bytes()) if (bundle/'last-action.json').exists() else {}
analysis=json.loads((bundle/'analysis-receipt.json').read_bytes()) if (bundle/'analysis-receipt.json').exists() else last.get('analysis') or {}
status=analysis.get('status') or last.get('status','limited_result')
reason=last.get('reason') or last.get('stop_reason') or ''
coverage=analysis.get('coverage')
summary='<html><meta charset="utf-8"><title>Course research result</title><body style="font:16px system-ui;max-width:900px;margin:40px auto;line-height:1.5">'
summary+='<h1>Course research result</h1><p><b>'+html.escape(status)+'</b></p><p>'+html.escape(reason)+'</p>'
if last.get('setup_stage') and last.get('weights_staged') is False:
    summary+='<p>Setup stopped before weights. No new model attempt was started by this setup action. Stage: '+html.escape(last['setup_stage'])+'</p>'
if coverage: summary+='<p>Fixed main population coverage: '+html.escape(json.dumps(coverage))+'</p>'
summary+='<p>Original replies and failures are retained in course-resume.payload. Unexecuted outcomes remain unknown. No failed scientific check was bypassed.</p>'
if analysis.get('report'): summary+='<p><a href="'+html.escape(analysis['report'],quote=True)+'">Open the independently reproduced analysis</a></p>'
summary+='<p>Retain course-results.zip, course-resume.payload and this executed notebook. Stop the interactive Kaggle session normally.</p></body></html>'
(bundle/'RESULT.html').write_text(summary,encoding='utf-8')
resume_export=workspace/'course-resume.payload'
partial=resume_export.with_suffix('.tmp')
with tempfile.TemporaryDirectory() as temporary:
    with zipfile.ZipFile(partial,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
        for p in sorted(bundle.rglob('*')):
            if not p.is_file() or p.is_symlink() or p.name.endswith(('-wal','-shm','.owner','.tmp','.pyc')) or '__pycache__' in p.parts: continue
            relative=p.relative_to(bundle)
            if 'source' in relative.parts and ('build' in relative.parts or any(part.endswith('.egg-info') for part in relative.parts)): continue
            target=p
            if p.name in ('worker-0.sqlite','worker-1.sqlite'):
                target=Path(temporary)/(str(len(z.infolist()))+'-'+p.name)
                with closing(sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)) as original,closing(sqlite3.connect(target)) as copy:
                    original.backup(copy)
                    if copy.execute('PRAGMA integrity_check').fetchone()[0]!='ok': raise ValueError('SQLite backup failed')
            z.write(target,p.relative_to(bundle).as_posix())
try:
    partial.replace(resume_export)
except PermissionError:
    # An open download/Windows scanner may hold the previous derived ZIP.
    # Keep it intact and publish this complete snapshot under a fresh name.
    resume_export=workspace/('course-resume-'+time.strftime('%Y%m%dT%H%M%S',time.gmtime())+'.payload')
    partial.replace(resume_export)
results_export=workspace/'course-results.zip'
results_partial=results_export.with_suffix('.tmp')
with zipfile.ZipFile(results_partial,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
    for p in sorted(bundle.rglob('*')):
        if p.is_file() and not p.is_symlink() and (p.suffix in ('.html','.csv','.svg','.png') or
                p.suffix=='.json' and p.name!='operator-config.json' and not {'source','inputs'} & set(p.relative_to(bundle).parts)):
            z.write(p,p.relative_to(bundle).as_posix())
with zipfile.ZipFile(results_partial) as z:
    if z.testzip() is not None: raise ValueError('Results export CRC failed; previous export is preserved')
try:
    results_partial.replace(results_export)
except PermissionError:
    results_export=workspace/('course-results-'+str(time.time_ns())+'.zip')
    results_partial.replace(results_export)
display(HTML(summary))
for p in (results_export,resume_export,workspace/'setup'/'course-assets.zip'):
    if p.exists(): display(FileLink(str(p)))
if (bundle/'last-action.json').exists():
    display(FileLink(str(bundle/'last-action.json')))
if (bundle/'analysis-receipt.json').exists():
    analysis=json.loads((bundle/'analysis-receipt.json').read_bytes())
    display(FileLink(str(bundle/analysis['report'])))
    print(analysis['status'],analysis['coverage'])
print('Retain course-results.zip, course-resume.payload and the executed notebook. Stop the interactive Kaggle session normally. Observation timestamps do not prove provider release.')
"""
    return dict(nbformat=4, nbformat_minor=5,
        metadata=dict(kernelspec=dict(display_name="Python 3", language="python", name="python3"), language_info=dict(name="python")),
        cells=[cell("markdown", introduction, "welcome"), cell("code", select, "action"),
            cell("code", bootstrap, "source"), cell("markdown", "## Automatic configuration\nThe notebook detects GPU mode, records observed session timestamps, and saves the same scientific configuration for resumption. No manual budget or memory-proof form is required. Unobserved provider time remains unknown.\n", "config-notes"),
            cell("code", settings, "configuration"), cell("markdown", "## Run and monitor\nThe package measures storage before installation and keeps dependencies/weights in suitable temporary space. Logs show the exact paths and available/required capacity. Verified installations and partial downloads resume within a session. Progress streams every 15 seconds; quiescent SQLite backups update at ten-minute boundaries. A failed gate stops subsequent work and retains its evidence.\n", "execution-notes"),
            cell("code", run, "execute"), cell("markdown", "## Results and safe resume\nDownload course-results.zip, course-resume.payload and this executed notebook. A later Run All with the SAME dataset and latest payload resumes eligible interrupted work without resampling completed calls. A diagnosed adapter defect or failed scientific gate remains a limited result. Stop interactive sessions normally; no manual release form is required.\n", "export-notes"), cell("code", export, "export")])


def build(root, output, *, base_manifest=None, extra_report_wheels=None, assets_cache=None):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output.exists():
        raise FileExistsError(output)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root).decode().strip()
    if subprocess.check_output(["git", "diff", "HEAD", "--name-only", "--", *SOURCE_PATHS], cwd=root).strip():
        raise ValueError("commit task-owned source before packaging")
    candidate = json.loads((base_manifest or root/"dist/course-m5-hardware-v3/source-manifest.json").read_bytes())
    payload = (base_manifest.parent if base_manifest else root/"dist/course-m5-hardware-v3")/candidate["payload_filename"]
    if hashlib.sha256(payload.read_bytes()).hexdigest() != candidate["archive_sha256"]:
        raise ValueError("reviewed metadata source payload differs")
    archive = subprocess.check_output(["git", "archive", "--format=zip", commit, *SOURCE_PATHS], cwd=root)
    members = {}
    with zipfile.ZipFile(io.BytesIO(archive)) as source:
        for item in source.infolist():
            name = item.filename
            if item.is_dir() or name.endswith(".pyc"):
                continue
            members[name] = source.read(item)
    with zipfile.ZipFile(payload) as source:
        for name, expected in candidate["members"].items():
            if not name.startswith("metadata/4B/"):
                continue
            data = source.read(name)
            if len(data) != expected["bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
                raise ValueError("pinned metadata differs")
            members[name] = data
    for name in ("config.json","model.safetensors.index.json"):
        members["metadata/9B/"+name] = (root/"notebooks/validation/course-kaggle/repair-candidates"/name).read_bytes()
    members["SOURCE_COMMIT.txt"] = (commit+"\n").encode()
    base_wheels = candidate["candidate_wheels"]
    extras = report_wheels(base_wheels) if extra_report_wheels is None else extra_report_wheels
    wheels = base_wheels+extras
    lock = candidate_lock(wheels)
    members["candidate-linux313.lock"] = lock.encode()
    output.mkdir(parents=True)
    raw = output/"course-kaggle-source.payload"
    with zipfile.ZipFile(raw, "x", zipfile.ZIP_DEFLATED) as archive:
        for name,data in sorted(members.items()):
            item = zipfile.ZipInfo(name, (2026,10,12,0,0,0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            archive.writestr(item, data)
    manifest = archive_manifest(raw, source_commit=commit, payload_name=raw.name)
    preparation = preparation_review(root)
    renewed = json.loads((root/"notebooks/validation/course-kaggle/repair-candidates/9B/memory-review.json").read_bytes())
    preparation.update(complete_input_tokens_upper=renewed["complete_input_tokens_upper"],
        complete_resident_tokens_upper=renewed["complete_resident_tokens_upper"],
        prompt_profile=renewed["prompt_profile"],candidate_order=["9B","4B"])
    # The previous conditional tensor subtotals describe 4B, not the newly
    # qualified 9B replica. Neither candidate has physical acceptance yet.
    preparation.pop("conditional_tensor_component_sum_bytes",None)
    preparation.pop("conditional_loading_tensor_allowance_bytes",None)
    manifest.update(kind="course-kaggle-complete-workflow", candidate_wheels=wheels,
        build_tools=candidate["build_tools"], candidate_lock_sha256=hashlib.sha256(lock.encode()).hexdigest(),
        preparation=preparation, inference_wheels_unchanged=True,
        rendering_additions=extras, planned_main=dict(worlds=20, distinct_generations=5752, logical_uses=6280),
        planned_development=dict(worlds=5, distinct_generations=1114, logical_uses=1178, capability_first=90),
        gpu_execution_performed=False, model_acceptance=False, main_freeze=False)
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True)+"\n").encode()
    (output/"source-manifest.json").write_bytes(manifest_bytes)
    dataset = output/"course-kaggle-dataset.zip"
    assets = {}
    if assets_cache is not None:
        import tempfile
        from scripts.build_course_kaggle_assets import portable_members
        with tempfile.TemporaryDirectory(dir=assets_cache) as directory:
            installed_source = Path(directory)/"source"
            with zipfile.ZipFile(raw) as source:
                source.extractall(installed_source)
            (installed_source/"source-manifest.json").write_bytes(manifest_bytes)
            assets = portable_members(installed_source,manifest,Path(assets_cache))
    with zipfile.ZipFile(dataset, "x", zipfile.ZIP_DEFLATED) as archive:
        # The .payload suffix preserves one packed file during Kaggle's input
        # preparation. The notebook verifies/extracts it after the session starts.
        archive.write(raw,raw.name,compress_type=zipfile.ZIP_STORED)
        archive.writestr("source-manifest.json",manifest_bytes)
        for name,path in sorted(assets.items()):
            archive.write(path,"assets/"+name,compress_type=zipfile.ZIP_STORED)
    document = notebook(hashlib.sha256(manifest_bytes).hexdigest(), commit)
    (output/"course_kaggle.ipynb").write_text(json.dumps(document, indent=1, ensure_ascii=False)+"\n", encoding="utf-8")
    shutil_path = root/"docs/KAGGLE_COURSE.md"
    (output/"START_HERE.md").write_bytes(shutil_path.read_bytes())
    from scripts.m5_kaggle_preflight import sha256_file
    summary = dict(source_commit=commit, dataset=str(dataset), dataset_bytes=dataset.stat().st_size,
        dataset_sha256=sha256_file(dataset), notebook="course_kaggle.ipynb",
        source_members=len(members), pinned_candidate_packages=len(wheels), gpu_execution=False,
        dataset_input_files=2+len(assets), online_first=True, offline_assets_included=bool(assets), pretrained_model_loaded=False)
    (output/"package-summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--assets-cache", type=Path, help="include verified checkpoint and target wheels for one offline upload")
    args = parser.parse_args()
    build(args.root, args.output, assets_cache=args.assets_cache)


if __name__ == "__main__":
    main()
