"""Bounded online setup in a separate interpreter; never initializes CUDA."""

import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from time import monotonic
from collections import deque
from urllib.request import urlopen

from .archive import atomic_json, digest


# Same installer wheel as the accepted M5 Kaggle bootstrap. Scientific runtime
# dependencies remain in the unchanged i01-runtime.lock.
PIP_BOOTSTRAP = dict(version='26.2.1',filename='pip-26.2.1-py3-none-any.whl',bytes=1816632,
    sha256='71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e',
    url='https://files.pythonhosted.org/packages/f3/6e/1736e5b4ae2b778ef2f81c47d797de9f891d4d8acb047a24ca37a60294dd/pip-26.2.1-py3-none-any.whl')
PIP_WHEEL_RUNNER = "import runpy,sys;sys.path.insert(0,sys.argv.pop(1));runpy.run_module('pip',run_name='__main__',alter_sys=True)"


class SetupFailure(ValueError):
    def __init__(self, stage, log, code, tail):
        self.stage,self.log,self.code,self.tail=stage,str(log),code,tail
        super().__init__(f'{stage} failed ({code}). Full log: {log}')

    def _render_traceback_(self):
        # Expected operational failures show their cause instead of a dispatcher
        # stack. Unexpected Python defects still retain normal tracebacks.
        return [str(self), 'Last log lines:', self.tail]


def host_inventory(scratch, working):
    from .store import utc
    paths={}
    for label,path in (("scratch",scratch),("working",working)):
        path=Path(path); path.mkdir(parents=True,exist_ok=True)
        probe=path/".i01-write-probe"; probe.write_text("ok"); probe.unlink()
        free=shutil.disk_usage(path)
        paths[label]=dict(path=str(path),total=free.total,free=free.free,device=path.stat().st_dev,writable=True)
    gpus=[]
    try:
        text=subprocess.check_output(["nvidia-smi","--query-gpu=index,name,uuid,driver_version,memory.total","--format=csv,noheader,nounits"],text=True,timeout=20)
        for line in text.strip().splitlines():
            idx,name,identity,driver,memory=[v.strip() for v in line.split(",")]
            gpus.append(dict(index=int(idx),name=name,uuid=identity,driver=driver,memory_mib=int(memory)))
    except (FileNotFoundError,subprocess.SubprocessError) as error:
        gpus_error=str(error)
    return dict(observed_at=utc(),python=sys.version,executable=sys.executable,system=platform.system(),machine=platform.machine(),
                python_version=list(sys.version_info[:3]),gpus=gpus,paths=paths,
                gpus_error=locals().get("gpus_error"),internet_required=True)


def invoke(args, log, timeout=1800, *, env=None):
    log=Path(log); log.parent.mkdir(parents=True,exist_ok=True)
    print("Setup: "+log.stem,flush=True)
    with log.open("a",encoding="utf-8") as stream:
        stream.write('\nStarting '+log.stem+'\n'); stream.flush()
        p=subprocess.Popen([str(x) for x in args],stdout=stream,stderr=subprocess.STDOUT,env=env)
        started=monotonic()
        try:
            while True:
                remaining=timeout-(monotonic()-started)
                if remaining<=0: raise subprocess.TimeoutExpired(args,timeout)
                try:
                    code=p.wait(timeout=min(15,remaining)); break
                except subprocess.TimeoutExpired:
                    stream.flush()
                    lines=log.read_text(encoding="utf-8",errors="replace").splitlines()
                    print(f"{log.stem}: {monotonic()-started:.0f}s elapsed; "+(lines[-1][-300:] if lines else "in progress"),flush=True)
        except BaseException:
            p.terminate()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill(); p.wait(timeout=5)
            raise
    if code:
        with log.open(encoding='utf-8',errors='replace') as stream:
            tail=''.join(deque(stream,maxlen=40)).strip()
        raise SetupFailure(log.stem,log,code,tail)


def pip_wheel(scratch, receipts):
    """Retrieve one small pinned installer; no get-pip script or base pip needed."""
    directory=Path(scratch)/'pip-bootstrap'; directory.mkdir(parents=True,exist_ok=True)
    target=directory/PIP_BOOTSTRAP['filename']
    if not (target.is_file() and target.stat().st_size==PIP_BOOTSTRAP['bytes'] and digest(target)==PIP_BOOTSTRAP['sha256']):
        print('Setup: download verified pip bootstrap wheel',flush=True)
        partial=target.with_suffix('.partial')
        with urlopen(PIP_BOOTSTRAP['url'],timeout=30) as response, partial.open('wb') as stream:
            started=monotonic(); total=0
            while True:
                if monotonic()-started>120: raise ValueError('pip bootstrap download deadline')
                block=response.read(256*1024)
                if not block: break
                total+=len(block)
                if total>PIP_BOOTSTRAP['bytes']: raise ValueError('pip bootstrap wheel exceeds pinned size')
                stream.write(block)
        if partial.stat().st_size!=PIP_BOOTSTRAP['bytes'] or digest(partial)!=PIP_BOOTSTRAP['sha256']:
            raise ValueError('pip bootstrap size/hash mismatch; no wheel execution')
        partial.replace(target)
    atomic_json(Path(receipts)/'pip-bootstrap-wheel.json',dict(PIP_BOOTSTRAP,verified=True))
    return target


def create_environment(venv, scratch, receipts, env):
    """Create/recover a plain isolated venv, explicitly bypassing ensurepip."""
    venv,scratch,receipts=Path(venv),Path(scratch),Path(receipts)
    python=venv/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
    config=venv/'pyvenv.cfg'
    if venv.exists() and any(venv.iterdir()) and (not config.is_file() or 'include-system-site-packages = false' not in config.read_text().lower()):
        raise ValueError('Existing environment is not a verified isolated venv; choose a fresh scratch directory. No files were deleted.')
    invoke([sys.executable,'-m','venv','--without-pip',venv],receipts/'venv.log',120,env=env)
    if 'include-system-site-packages = false' not in config.read_text().lower():
        raise ValueError('Environment must not inherit kernel packages')
    wheel=pip_wheel(scratch,receipts)
    lock=scratch/'pip-bootstrap.lock'
    lock.write_text(f"pip=={PIP_BOOTSTRAP['version']} --hash=sha256:{PIP_BOOTSTRAP['sha256']}\n",encoding='utf-8')
    invoke([python,'-I','-c',PIP_WHEEL_RUNNER,wheel,'--isolated','--disable-pip-version-check',
            'install','--no-deps','--no-index','--find-links',wheel.parent,'--require-hashes',
            '-r',lock],receipts/'bootstrap-pip.log',120,env=env)
    probe="import pathlib,pip,sys; assert sys.prefix!=sys.base_prefix; assert pathlib.Path(pip.__file__).resolve().is_relative_to(pathlib.Path(sys.prefix).resolve()); assert pip.__version__=="+repr(PIP_BOOTSTRAP['version'])+"; print('Isolated pinned pip accepted:',pip.__version__)"
    invoke([python,'-I','-c',probe],receipts/'pip-isolation.log',60,env=env)
    return python


def install(source, scratch, working):
    source,scratch,working=Path(source),Path(scratch),Path(working)
    host=host_inventory(scratch,working)
    receipts=working/"i01-setup"; receipts.mkdir(exist_ok=True)
    atomic_json(receipts/"host.json",host)
    if host["system"]!="Linux" or host["machine"]!="x86_64" or host["python_version"][:2]!=[3,13]:
        raise ValueError("reviewed runtime requires Linux x86_64 Python 3.13; stop before installing an incompatible lock")
    if len(host["gpus"])!=2 or any("T4" not in g["name"] for g in host["gpus"]):
        raise ValueError("select T4 x2 before setup")
    if host["paths"]["scratch"]["free"] < 12*2**30 or host["paths"]["working"]["free"] < 2*2**30:
        raise ValueError("insufficient measured setup/output storage")
    venv=scratch/"i01-venv"; python=venv/"bin/python"
    from .workflow import source_files
    wheels=list(source.glob("*.whl"))
    if len(wheels)!=1:
        raise ValueError("exactly one verified source wheel required")
    identity=dict(runtime_lock=digest(source/"configs/i01-runtime.lock"),
                  source_identity=source_files(source),wheel_sha256=digest(wheels[0]))
    receipt_path=receipts/"environment.json"
    if receipt_path.exists():
        saved=json.loads(receipt_path.read_text())
        if saved["identity"]!=identity or not python.exists():
            raise ValueError("environment differs or missing; no mid-session replacement")
        return saved
    started=monotonic()
    (scratch/"tmp").mkdir(exist_ok=True)
    env={k:v for k,v in os.environ.items() if not k.startswith(('PYTHON','PIP_','VIRTUAL_ENV'))}
    env.update(PIP_DEFAULT_TIMEOUT="60",HF_HUB_DOWNLOAD_TIMEOUT="60",HF_HUB_ETAG_TIMEOUT="30",
             HF_HUB_CACHE=str(scratch/"hf-cache"),PYTHONUNBUFFERED="1",TMPDIR=str(scratch/"tmp"),
             TMP=str(scratch/"tmp"),TEMP=str(scratch/"tmp"),PYTHONNOUSERSITE='1',PYTHONUTF8='1',
             PIP_CONFIG_FILE=os.devnull,PIP_DISABLE_PIP_VERSION_CHECK='1')
    python=create_environment(venv,scratch,receipts,env)
    invoke([python,"-m","pip","--isolated","--cache-dir",scratch/"pip-cache","install","--only-binary=:all:","--require-hashes",
            "--retries","2","--index-url","https://pypi.org/simple","--extra-index-url","https://download.pytorch.org/whl/cu128",
            "--report",receipts/"dependency-install.json","-r",source/"configs/i01-runtime.lock"],receipts/"dependencies.log",3600,env=env)
    invoke([python,"-m","pip","--isolated","install","--no-deps","--no-index",wheels[0]],receipts/"project.log",120,env=env)
    invoke([python,"-m","pip","check"],receipts/"pip-check.log",60,env=env)
    probe=receipts/"installed.json"
    invoke([python,"-m","recovery.i01.cli","--source",source,"runtime-inventory","--output",probe],receipts/"installed.log",120,env=env)
    result=dict(identity=identity,interpreter=str(python),source=str(source),scratch=str(scratch),
                working=str(working),hf_cache=str(scratch/"hf-cache"),host=host,setup_seconds=monotonic()-started,
                versions=json.loads(probe.read_text()),model_attempts=0)
    result['pip_bootstrap']=dict(PIP_BOOTSTRAP,ensurepip_used=False)
    atomic_json(receipt_path,result)
    return result


def runtime_inventory(source):
    from .workflow import source_files
    import recovery
    root=Path(recovery.__file__).parent.parent
    expected=source_files(source)
    for relative,sha in expected.items():
        if relative.startswith("recovery/") and digest(root/relative)!=sha:
            raise ValueError("installed source differs: "+relative)
    names=[line.split("==")[0] for line in (Path(source)/"configs/i01-runtime.lock").read_text().splitlines() if "==" in line]
    versions={name:importlib.metadata.version(name) for name in names}
    expected_versions={line.split("==")[0]:line.split("==")[1].split()[0]
                       for line in (Path(source)/"configs/i01-runtime.lock").read_text().splitlines() if "==" in line}
    if versions!=expected_versions:
        raise ValueError("installed packages differ from pinned runtime")
    return dict(python=sys.version,packages=versions,installed_source_matches=True,source_identity=expected)


def download(source, scratch, working, *, weights=False):
    from huggingface_hub import HfApi, snapshot_download
    source,scratch,working=Path(source),Path(scratch),Path(working)
    config=json.loads((source/"configs/i01-course.json").read_text())
    receipts=working/"i01-setup"; receipts.mkdir(parents=True,exist_ok=True)
    info=HfApi().model_info(config["model"],revision=config["revision"],files_metadata=True)
    if info.sha!=config["revision"]:
        raise ValueError("pinned model revision differs")
    metadata={"config.json","generation_config.json","tokenizer.json","tokenizer_config.json","chat_template.jinja","vocab.json","merges.txt","model.safetensors.index.json","preprocessor_config.json","processor_config.json"}
    files=[item for item in info.siblings if item.rfilename in metadata or weights and item.rfilename.endswith(".safetensors")]
    if not any(f.rfilename.endswith(".safetensors") for f in files) and weights:
        raise ValueError("native checkpoint shard inventory missing")
    needed=sum(f.size or 0 for f in files)
    # Hugging Face cache shares verified blobs across metadata and weight stages.
    free=shutil.disk_usage(scratch).free
    already=working/"i01-setup"/("weights.json" if weights else "metadata.json")
    cache=scratch/"hf-cache"/"models--Qwen--Qwen3.5-9B"/"blobs"
    missing=0
    for f in files:
        identity=f.lfs.sha256 if f.lfs is not None else f.blob_id
        present=cache/identity
        partial=cache/(identity+".incomplete")
        available=present.stat().st_size if present.exists() else partial.stat().st_size if partial.exists() else 0
        missing+=max(0,(f.size or 0)-available)
    if free < missing+2*2**30:
        raise ValueError(f"native files still need {missing} bytes plus reserve; scratch free={free}")
    snapshot=None
    for attempt in range(3):
        try:
            snapshot=Path(snapshot_download(config["model"],revision=config["revision"],cache_dir=scratch/"hf-cache",
                                           allow_patterns=[f.rfilename for f in files],max_workers=2,etag_timeout=30))
            break
        except Exception:
            if attempt==2:
                raise
            print(f"Transport retry {attempt+1}/2; reuse partial pinned files",flush=True)
    verified={}
    for f in files:
        path=snapshot/f.rfilename
        if path.stat().st_size!=f.size:
            raise ValueError("native file byte size differs: "+f.rfilename)
        actual=digest(path)
        if f.lfs is not None and actual!=f.lfs.sha256:
            raise ValueError("native LFS hash differs: "+f.rfilename)
        if f.lfs is None:
            import hashlib
            blob=hashlib.sha1(b"blob "+str(f.size).encode()+b"\0"+path.read_bytes()).hexdigest()
            if blob!=f.blob_id:
                raise ValueError("native Git blob hash differs: "+f.rfilename)
        verified[f.rfilename]=dict(bytes=f.size,sha256=actual)
    result=dict(model=config["model"],revision=config["revision"],snapshot=str(snapshot),files=verified,
                native_total_bytes=needed,weights=weights,model_attempts=0)
    atomic_json(already,result)
    return result
