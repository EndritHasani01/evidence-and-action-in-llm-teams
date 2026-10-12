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
SOURCE_PATHS = ("recovery", "scripts", "tests", "configs", "pyproject.toml", "AGENTS.md", "PROJECT_SPECIFICATION.md", "README.md",
    "docs/IMPLEMENTATION_PLAN.md", "docs/todos/course", "docs/validation/course-kaggle-workflow.md",
    "docs/KAGGLE_COURSE.md", "docs/implementation-research/course-m5-r7-capacity-proof.md",
    "notebooks/validation/course-m5-preparation/inputs",
    "notebooks/validation/course-m5-preparation/candidate-inspection-accepted.json",
    "notebooks/validation/course-m5-r7",
    "notebooks/validation/m5-t4-compatibility-run-6/validation.json")
FIXTURES = {"population_course.json", "schedules_course.json", "course_capacity.json.gz",
            "native_silo_cases.json", "population_target.json", "population_fallback.json",
            "schedules_target.json", "schedules_fallback.json"}


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
    introduction = """# Course research · Kaggle T4 ×2

One interface for the existing course runner, feasibility gates, restartable experiments and offline results.
**Default: inspect only.** Each invocation performs one action. GPU calls, weight staging, freeze and main execution need their own explicit authorization below.

| Action | Accelerator | Internet | Result |
|---|---|---|---|
| `inspect` | None | Off | Verify this exact source package; show saved scope |
| `setup` | None | On | Install pinned candidate and stage the reviewed checkpoint; export reusable assets |
| `restore` | None | Off | Restore attached portable assets before assigning GPUs in a new session |
| `hardware` | T4 ×2 | Off | Native smoke, two 110,107-token resident-envelope diagnostics, bounded timeout, original evidence |
| `capability` | T4 ×2 | Off | First 90 development slots only |
| `pilot` | T4 ×2 | Off | Finish the same 1,114-generation / 1,178-use pilot |
| `freeze` | None | Off* | Audit pilot, review R7/timeout/family failures, forecast all 20 worlds; freeze if admitted |
| `main` | T4 ×2 | Off | Continue the fixed 5,752-generation / 6,280-use schedule for a bounded session |
| `status`, `analyze`, `export` | None | Off* | Monitor, independently audit/reproduce the report, or export without inference |

*A new CPU environment needs Internet for its first install; model weights are unnecessary for analysis.

Upload **course-kaggle-dataset.zip** as a private dataset, attach it and import this notebook.
In later sessions also attach **course-resume.zip**; GPU sessions reuse **course-assets.zip**.
Read `source/docs/KAGGLE_COURSE.md` for the short runbook and memory-review requirements.
The candidate requires Linux x86_64 Python 3.13 for GPU work. A different Kaggle image is a gate failure, not an automatic package upgrade.
"""
    select = """# Edit this cell for the action you have authorized. Run All is safe with these defaults.
ACTION = "inspect"
ENABLE_GPU = False
PACKAGE_DIR = None  # Optional explicit directory containing source-manifest.json
RESUME_ZIP = None   # Otherwise finds the single attached course-resume.zip
ASSETS_ZIP = None   # Otherwise finds the single attached course-assets.zip
"""
    bootstrap = f"""import hashlib,json,os,shutil,stat,sys,time,zipfile
from pathlib import Path,PurePosixPath
from IPython.display import display,FileLink,HTML
EXPECTED_MANIFEST_SHA256={manifest_sha!r}
EXPECTED_SOURCE_COMMIT={commit!r}
workspace=Path(os.environ.get('COURSE_WORKSPACE','/kaggle/working/course-workspace')).resolve()
workspace.mkdir(parents=True,exist_ok=True)
bundle=workspace/'bundle'
inputs=Path(os.environ.get('COURSE_INPUT','/kaggle/input'))
def attached(name,explicit=None):
    if explicit: return Path(explicit).resolve()
    matches=list(inputs.rglob(name))
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
if not bundle.exists():
    if resume: extract_fresh(resume,bundle)
    else: bundle.mkdir()
source=bundle/'source'
if not source.exists():
    options=[Path(PACKAGE_DIR)/'source-manifest.json'] if PACKAGE_DIR else list(inputs.rglob('source-manifest.json'))
    matches=[p for p in options if hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED_MANIFEST_SHA256]
    if len(matches)!=1: raise ValueError('Attach the exact course dataset ZIP (Kaggle extracts it), or set PACKAGE_DIR')
    package=matches[0].parent
    manifest=json.loads(matches[0].read_bytes())
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
display(FileLink(str(source/'docs/KAGGLE_COURSE.md')))
"""
    settings = """# Restore prior bounds/reviews/authorizations; edit only current provider facts.
saved_config=bundle/'operator-config.json'
CONFIG=json.loads((saved_config if saved_config.exists() else source/'configs/course-kaggle.json').read_bytes())
CONFIG.update(execute_gpu=ENABLE_GPU,
    allocated_at=None,                  # Actual UTC provider assignment, e.g. YYYY-MM-DDTHH:MM:SS+00:00
    provider_quota_gpu_hours=None,       # Current provider allowance, independent of scientific spending
    provider_session_seconds=None,      # Current provider maximum session duration; verify it
    prior_sessions_released=CONFIG.get('prior_sessions_released',False),
    max_work_seconds=1800,
)
# Fill these overrides when first known. Empty dictionaries preserve saved values.
CONFIG['authorizations'].update({})  # keys: weights, hardware, pilot, freeze, main; explicit scope text
CONFIG['budget'].update({})         # all six prior_*_gpu_hours=[lower,upper], prior_smoke_attempts, prior_evidence
CONFIG['previous_session_release'].update({})  # released_at='...+00:00', evidence='actual provider deallocation receipt'
CONFIG['hardware_review'].update({})  # accepted, complete_live_memory_upper_bound_bytes, supported justification
CONFIG['pilot_review'].update({})     # family_condition_failures_reviewed, timeout_120_seconds_adequate
# Keep these same prior bounds on all resumes; hardware and pilot ledgers are added once by the runner.
config_path=bundle/'operator-config.json'
config_path.write_text(json.dumps(CONFIG,indent=2)+'\\n')
"""
    run = """import queue,threading,subprocess,signal
def bounded_child(arguments,limit):
    # The repo owns scientific work; this cell only streams its process output.
    log=workspace/('action-'+time.strftime('%Y%m%dT%H%M%S',time.gmtime())+'.log')
    process=subprocess.Popen([str(a) for a in arguments],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
        text=True,bufsize=1,start_new_session=(os.name!='nt'),cwd=workspace)
    lines=queue.Queue()
    def collect():
        for line in process.stdout: lines.put(line)
    reader=threading.Thread(target=collect,daemon=True); reader.start()
    deadline=time.monotonic()+limit
    try:
        with log.open('w',encoding='utf-8') as output:
            while process.poll() is None or not lines.empty():
                if time.monotonic()>=deadline: raise TimeoutError('Notebook controller deadline; preserve/export and Stop Session')
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
    return process.returncode

if ACTION=='inspect':
    print('Verified upload package. GPU and weight staging remain disabled. Choose setup when resource evidence and weight staging authorization are ready.')
else:
    gpu_action=ACTION in ('hardware','capability','pilot','main')
    if gpu_action and not ENABLE_GPU: raise ValueError('Set ENABLE_GPU only for the separately authorized GPU action')
    if not gpu_action and Path('/proc/driver/nvidia/gpus').is_dir() and list(Path('/proc/driver/nvidia/gpus').iterdir()):
        raise ValueError('Use Accelerator None for CPU/setup/review/analysis actions; assigned GPU idle time remains chargeable')
    gpu_receipt=workspace/'gpu-environment'/'bootstrap'/'bootstrap.json'
    kind='setup' if ACTION=='setup' else 'gpu-environment' if ACTION=='restore' or gpu_action or gpu_receipt.exists() else 'cpu-environment'
    environment=workspace/kind
    receipt=environment/'bootstrap'/'bootstrap.json'
    if not receipt.exists():
        arguments=[sys.executable,'-I',source/'scripts/course_kaggle_bootstrap.py']
        if ACTION=='setup':
            arguments+=['setup','--config',config_path]
        elif ACTION=='restore':
            assets=attached('course-assets.zip',ASSETS_ZIP)
            if assets is None:
                options=[p.parent for p in inputs.rglob('prepared-assets.json') if (p.parent/'checkpoint').is_dir() and (p.parent/'wheels').is_dir()]
                if len(options)!=1: raise ValueError('Attach exactly one extracted course-assets dataset, or set ASSETS_ZIP to its directory/ZIP')
                assets=options[0]
            if assets is None: raise ValueError('Attach course-assets.zip from the CPU setup; use the same source package')
            arguments+=['restore','--assets',assets]
        elif gpu_action:
            raise ValueError('Run ACTION=restore with Accelerator None before assigning T4 x2, then change ACTION and record actual assignment time. This avoids spending GPU allowance on environment installation.')
        else:
            arguments+=['cpu']
        arguments+=['--root',source,'--scratch',environment/'scratch','--output',environment/'bootstrap']
        limit=2100
        if bounded_child(arguments,limit)!=0: raise RuntimeError('Environment setup/restore failed; evidence is retained in bootstrap.json and the action log')
    runtime=json.loads(receipt.read_bytes())
    if runtime.get('status')=='blocked': raise RuntimeError(runtime['reason'])
    if runtime.get('assets_receipt') and not runtime.get('requires_dataset_restore'):
        CONFIG.update(assets_receipt=runtime['assets_receipt'],hf_cache=runtime['hf_cache'])
        shutil.copyfile(runtime['assets_receipt'],bundle/'asset-receipt.json')
    elif (bundle/'asset-receipt.json').exists():
        CONFIG['assets_receipt']=str(bundle/'asset-receipt.json')
    config_path.write_text(json.dumps(CONFIG,indent=2)+'\\n')
    if ACTION not in ('setup','restore'):
        arguments=[runtime['interpreter'],'-I',source/'scripts/course_kaggle_workflow.py',
            '--root',source,'--bundle',bundle,'--config',config_path,'--action',ACTION]
        limit=CONFIG['max_work_seconds']+180 if gpu_action else 2100
        code=bounded_child(arguments,limit)
        print('Action returned',code,'· inspect last-action.json for the exact gate/stop reason.')
    else:
        print('Pinned assets ready. Setup packs and consumes staging copies; download course-assets.zip and restore its private input in a new CPU session. Hardware acceptance remains open.')
"""
    export = """# Run this cell after an action finishes/fails. It never invokes inference.
# Stdlib fallback also exports setup/refusal evidence before project installation.
import sqlite3,tempfile
from contextlib import closing
resume_export=workspace/'course-resume.zip'
partial=resume_export.with_suffix('.tmp')
with tempfile.TemporaryDirectory() as temporary:
    with zipfile.ZipFile(partial,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
        for p in sorted(bundle.rglob('*')):
            if not p.is_file() or p.is_symlink() or p.name.endswith(('-wal','-shm','.owner','.tmp','.pyc')) or '__pycache__' in p.parts: continue
            target=p
            if p.name in ('worker-0.sqlite','worker-1.sqlite'):
                target=Path(temporary)/(p.parent.name+'-'+p.name)
                with closing(sqlite3.connect(p.as_uri()+'?mode=ro',uri=True)) as original,closing(sqlite3.connect(target)) as copy:
                    original.backup(copy)
                    if copy.execute('PRAGMA integrity_check').fetchone()[0]!='ok': raise ValueError('SQLite backup failed')
            z.write(target,p.relative_to(bundle).as_posix())
partial.replace(resume_export)
for p in (workspace/'course-resume.zip',workspace/'setup'/'course-assets.zip'):
    if p.exists(): display(FileLink(str(p)))
if (bundle/'last-action.json').exists():
    display(FileLink(str(bundle/'last-action.json')))
if (bundle/'analysis-receipt.json').exists():
    analysis=json.loads((bundle/'analysis-receipt.json').read_bytes())
    display(FileLink(str(bundle/analysis['report'])))
    print(analysis['status'],analysis['coverage'])
print('Retain the ZIP(s) and actual executed notebook. For GPU actions: Stop Session now and verify provider deallocation. Record its UTC release and evidence for the next session.')
"""
    return dict(nbformat=4, nbformat_minor=5,
        metadata=dict(kernelspec=dict(display_name="Python 3", language="python", name="python3"), language_info=dict(name="python")),
        cells=[cell("markdown", introduction, "welcome"), cell("code", select, "action"),
            cell("code", bootstrap, "source"), cell("markdown", "## Configure the authorized action\nUse `[lower, upper]` GPU-hour bounds supported by evidence. Zero also requires evidence. Preserve the same base bounds on every resume. Available account quota does not reset study spending.\n", "config-notes"),
            cell("code", settings, "configuration"), cell("markdown", "## Execute and monitor\nThe package streams progress every 15 seconds and exports quiescent SQLite backups at ten-minute boundaries. Interrupted/invalid replies remain recorded. A failed gate stops subsequent work.\n", "execution-notes"),
            cell("code", run, "execute"), cell("markdown", "## Save evidence and release the session\nDownload the current ZIP and this executed notebook before stopping. Quick Save saves the notebook without a fresh execution; downloading exported evidence is the durable resume path. Save & Run All would start a new invocation.\n", "export-notes"), cell("code", export, "export")])


def build(root, output, *, base_manifest=None, extra_report_wheels=None):
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
            if name.startswith("tests/fixtures/") and Path(name).name not in FIXTURES:
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
    manifest.update(kind="course-kaggle-complete-workflow", candidate_wheels=wheels,
        build_tools=candidate["build_tools"], candidate_lock_sha256=hashlib.sha256(lock.encode()).hexdigest(),
        preparation=preparation_review(root), inference_wheels_unchanged=True,
        rendering_additions=extras, planned_main=dict(worlds=20, distinct_generations=5752, logical_uses=6280),
        planned_development=dict(worlds=5, distinct_generations=1114, logical_uses=1178, capability_first=90),
        gpu_execution_performed=False, model_acceptance=False, main_freeze=False)
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True)+"\n").encode()
    (output/"source-manifest.json").write_bytes(manifest_bytes)
    dataset = output/"course-kaggle-dataset.zip"
    with zipfile.ZipFile(dataset, "x", zipfile.ZIP_DEFLATED) as archive:
        for name,data in sorted(dict(members, **{"source-manifest.json":manifest_bytes}).items()):
            item = zipfile.ZipInfo(name, (2026,10,12,0,0,0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            archive.writestr(item, data)
    document = notebook(hashlib.sha256(manifest_bytes).hexdigest(), commit)
    (output/"course_kaggle.ipynb").write_text(json.dumps(document, indent=1, ensure_ascii=False)+"\n", encoding="utf-8")
    shutil_path = root/"docs/KAGGLE_COURSE.md"
    (output/"START_HERE.md").write_bytes(shutil_path.read_bytes())
    summary = dict(source_commit=commit, dataset=str(dataset), dataset_bytes=dataset.stat().st_size,
        dataset_sha256=hashlib.sha256(dataset.read_bytes()).hexdigest(), notebook="course_kaggle.ipynb",
        source_members=len(members), pinned_candidate_packages=len(wheels), gpu_execution=False)
    (output/"package-summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.root, args.output)


if __name__ == "__main__":
    main()
