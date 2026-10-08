"""Reproduce the isolated local pinned-pip check without candidate/model downloads.

Run once from the repository root with Python 3.10+; use a new evidence directory
for repetition because the owned command logs deliberately refuse overwrites.
"""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts import m5_kaggle_preflight as preflight


def main():
    output = Path(__file__).resolve().parent
    scratch = ROOT/'build'/('m5-pip-bootstrap-'+uuid.uuid4().hex)
    scratch.mkdir(parents=True, exist_ok=False)
    env = preflight.candidate_environment(scratch)
    candidate = scratch/'venv'
    interpreter = candidate/('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    tools_path = ROOT/'notebooks/validation/m5-full-preparation/build-tool-metadata.json'
    tool = json.loads(tools_path.read_text())['pip']
    metadata = tool['wheels'][0]
    baseline_script = (
        "import json;from importlib.metadata import distributions;"
        "print(json.dumps(sorted((d.metadata['Name'],d.version) for d in distributions())))")
    before = subprocess.check_output([sys.executable,'-c',baseline_script],env=env)
    deadline = time.monotonic()+600

    def invoke(name, args, timeout):
        return preflight.command(output,name,args,deadline=deadline,timeout=timeout,
                                 cwd=scratch,env=env)

    invoke('create-venv',[sys.executable,'-m','venv','--without-pip',candidate],60)
    assert 'include-system-site-packages = false' in (candidate/'pyvenv.cfg').read_text().lower()
    empty = preflight.json_stdout(output,invoke('empty-venv-probe',[interpreter,'-I','-c',
        "import importlib.util,json,site,sys;assert importlib.util.find_spec('pip') is None;"
        "assert sys.prefix!=sys.base_prefix and site.ENABLE_USER_SITE is False;"
        "print(json.dumps({'pip_absent':True,'user_site':site.ENABLE_USER_SITE,'prefix':sys.prefix}))"],30))
    wheel_directory = scratch/'pip-bootstrap'
    wheel_directory.mkdir()
    wheel = wheel_directory/metadata['filename']
    download = preflight.json_stdout(output,invoke('download-pip-wheel',[interpreter,'-I','-c',
        preflight.pip_wheel_download_script(metadata,wheel)],60))
    assert download == dict(metadata,verified=True)
    assert wheel.stat().st_size == metadata['bytes'] and preflight.sha256_file(wheel) == metadata['sha256']
    preflight.save_json(output/'pip-bootstrap-wheel.json',download)
    lock = scratch/'pip-bootstrap.lock'
    lock.write_text(f"pip=={tool['version']} --hash=sha256:{metadata['sha256']}\n")
    invoke('bootstrap-pip',[interpreter,'-I','-c',preflight.PIP_WHEEL_RUNNER,wheel,
        '--isolated','--disable-pip-version-check','install','--no-cache-dir','--no-deps',
        '--require-hashes','--report',output/'pip-bootstrap.json','--no-index',
        '--find-links',wheel_directory,'-r',lock],120)
    probe = preflight.json_stdout(output,invoke('installed-pip-probe',[interpreter,'-I','-c',
        "import json,pip,site,sys;from pathlib import Path;"
        f"assert pip.__version__=={tool['version']!r};"
        "assert sys.prefix!=sys.base_prefix and site.ENABLE_USER_SITE is False;"
        "assert Path(pip.__file__).resolve().is_relative_to(Path(sys.prefix).resolve());"
        "print(json.dumps({'version':pip.__version__,'module':pip.__file__,"
        "'prefix':sys.prefix,'base_prefix':sys.base_prefix,'user_site':site.ENABLE_USER_SITE}))"],30))
    invoke('pip-check',[interpreter,'-I','-m','pip','--isolated','--disable-pip-version-check','check'],30)
    install = json.loads((output/'pip-bootstrap.json').read_text())['install']
    assert len(install) == 1 and install[0]['metadata']['version'] == tool['version']
    assert install[0]['download_info']['archive_info']['hashes']['sha256'] == metadata['sha256']
    after = subprocess.check_output([sys.executable,'-c',baseline_script],env=env)
    assert before == after, 'base packages changed'
    result = {'checked_utc':datetime.now(timezone.utc).isoformat(),'status':'passed',
        'python':platform.python_version(),'os':platform.platform(),'scope':'Local isolated pip bootstrap only',
        'source_helper_sha256':preflight.sha256_file(ROOT/'scripts/m5_kaggle_preflight.py'),
        'metadata_sha256':preflight.sha256_file(tools_path),'empty_venv':empty,
        'verified_download':download,'installed_probe':probe,'base_packages_unchanged':True,
        'candidate_packages_installed':False,'model_generations':0,'gpu_acceptance':None,
        'linux_python313_bootstrap_acceptance':None}
    preflight.save_json(output/'bootstrap-validation.json',result)
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
