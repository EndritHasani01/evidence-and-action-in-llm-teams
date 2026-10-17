"""I-01 interpreter entry: venv packages without host sitecustomize/.pth hooks.

Launched with -I -S. Restore the Python 3.13 venv prefix explicitly; only the
ordinary wheel directory is added. No site.main/addsitedir or hook executes.
"""
import importlib.util
import json
import os
from pathlib import Path
import runpy
import sys


def configure():
    os.environ['MPLBACKEND']='Agg'
    prefix=Path(sys.executable).absolute().parent.parent  # Do not resolve venv executable symlinks.
    config=prefix/'pyvenv.cfg'
    if config.exists():
        if 'include-system-site-packages = false' not in config.read_text(encoding='utf-8').lower():
            raise ValueError('I-01 requires an isolated venv')
        sys.prefix=sys.exec_prefix=str(prefix)
    else:
        prefix=Path(sys.base_prefix)
    sites=[prefix/'Lib/site-packages'] if os.name=='nt' else [prefix/'lib'/f'python{sys.version_info.major}.{sys.version_info.minor}'/'site-packages']
    for path in sites:
        if path.exists() and str(path) not in sys.path:sys.path.append(str(path))
    source=Path(__file__).resolve().parents[2]
    if not config.exists() or not (source/'source-release.json').exists():
        # Development-only source checks; actual setup/load validates the pinned
        # installed interpreter, packages and source before any model work.
        if str(source) not in sys.path:sys.path.insert(0,str(source))
    return dict(prefix=str(prefix),venv=config.exists(),site_directories=[str(p) for p in sites])


def inventory():
    info=configure()
    spec=importlib.util.find_spec('sitecustomize')
    return dict(info,interpreter=sys.executable,base_prefix=sys.base_prefix,
                isolated=bool(sys.flags.isolated),site_processing_disabled=bool(sys.flags.no_site),
                hook_automatically_imported='sitecustomize' in sys.modules,
                discoverable_hook_origin=spec.origin if spec else None,
                pth_files=[str(p) for d in info['site_directories'] for p in Path(d).glob('*.pth')],
                cwd=str(Path.cwd()),sys_path=list(sys.path),model_attempts=0)


def command(python,source,*args):
    return [str(python),'-I','-S','-X','utf8','-u',str(Path(source).resolve()/'recovery/i01/runtime.py'),*map(str,args)]


def main():
    configure()
    if len(sys.argv)<3 or sys.argv[1] not in ('-m','-c'):
        raise ValueError('Use the explicit I-01 module or code entry')
    mode,target=sys.argv[1:3];sys.argv=[target,*sys.argv[3:]]
    if mode=='-m':runpy.run_module(target,run_name='__main__',alter_sys=True)
    else:exec(compile(target,'<i01-runtime>','exec'),{'__name__':'__main__'})


if __name__=='__main__':main()
