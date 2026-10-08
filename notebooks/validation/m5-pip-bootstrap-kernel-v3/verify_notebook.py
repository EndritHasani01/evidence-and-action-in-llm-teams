"""Execute the exact v3 notebook locally; Windows host refusal is expected.

No installation outcome is controlled or inferred. Both returned exports and
copied SQLite snapshots are checked after real Jupyter execution.
"""

import asyncio
from contextlib import closing
import copy
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sqlite3
import sys
import uuid
import zipfile

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from scripts import m5_kaggle_preflight as preflight


def main():
    evidence = Path(__file__).resolve().parent/'final'
    evidence.mkdir(exist_ok=False)
    original = ROOT/'notebooks/recovery_m5_kaggle_preflight_v3.ipynb'
    shipped = nbformat.read(original,as_version=4)
    nbformat.validate(shipped)
    namespace = {}
    exec(''.join(shipped.cells[1].source),namespace)
    expected = namespace['EXPECTED']
    assert expected['helper_sha256'] == preflight.sha256_file(ROOT/'scripts/m5_kaggle_preflight.py')
    assert all(c.execution_count is None and not c.outputs for c in shipped.cells if c.cell_type=='code')
    scratch = ROOT/'build'/('m5-kernel-v3-'+uuid.uuid4().hex)
    scratch.mkdir(parents=True,exist_ok=False)
    if sys.platform=='win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = {'status':'passed','notebook_sha256':preflight.sha256_file(original),
              'build_commit':expected['build_commit'],'helper_sha256':expected['helper_sha256'],
              'scope':'Real local Windows Jupyter entrypoint; candidate host is correctly refused',
              'linux_candidate_acceptance':None,'model_generations':0,'cases':{}}
    for name in ['valid-source','missing-source']:
        case = evidence/name
        case.mkdir(exist_ok=False)
        inputs = scratch/name/'inputs'
        inputs.mkdir(parents=True)
        if name=='valid-source':
            shutil.copyfile(ROOT/'dist/m5-kaggle-preflight.zip',inputs/expected['payload_filename'])
        overrides = {'M5_PREFLIGHT_INPUT_ROOT':str(inputs),'M5_PREFLIGHT_OUTPUT_ROOT':str(case/'output'),
                     'M5_PREFLIGHT_SCRATCH_ROOT':str(scratch/name/'scratch')}
        prior = {key:os.environ.get(key) for key in overrides}
        try:
            os.environ.update(overrides)
            notebook = NotebookClient(copy.deepcopy(shipped),timeout=180,kernel_name='python3',
                resources={'metadata':{'path':str(ROOT)}}).execute()
        finally:
            for key,value in prior.items():
                if value is None: os.environ.pop(key,None)
                else: os.environ[key]=value
        nbformat.write(notebook,case/'executed.ipynb')
        assert [c.source for c in notebook.cells] == [c.source for c in shipped.cells]
        code = [c for c in notebook.cells if c.cell_type=='code']
        assert [c.execution_count for c in code] == [1,2,3]
        assert not any(o.output_type=='error' for c in code for o in c.outputs)
        archives = list((case/'output').glob('*/preflight-results.zip'))
        assert len(archives)==1
        archive_path = archives[0]
        with zipfile.ZipFile(archive_path) as archive:
            assert archive.testzip() is None
            members = archive.namelist()
            assert len(members)==len(set(members))
            assert all(not p.startswith('/') and '..' not in PurePosixPath(p).parts for p in members)
            summary = json.loads(archive.read('summary.json'))
            report = json.loads(archive.read('preflight-report.json'))
            assert summary == report['summary']
            assert summary['tests_passed']==0 and summary['model_generations']==0
            assert summary['preparation_checks_passed'] is False and summary['model_smoke_ready'] is False
            assert report['stages']['environment']['status']=='blocked'
            assert report['stages']['filesystem_backup']['status']=='passed'
            if name=='valid-source':
                source = report['stages']['source']
                assert source['status']=='passed' and source['result']['verified_members']==143
                assert 'candidate_host_requires_linux_x86_64_python313' in summary['root_blocker']
            else:
                assert 'payload_missing' in summary['root_blocker']
            snapshots = {}
            for member in ['filesystem.sqlite','filesystem-backup.sqlite']:
                copied = case/('reopened-'+member)
                copied.write_bytes(archive.read(member))
                with closing(sqlite3.connect(copied.resolve().as_uri()+'?mode=ro&immutable=1',uri=True)) as connection:
                    assert connection.execute('PRAGMA integrity_check').fetchone()==('ok',)
                    assert connection.execute('SELECT value FROM probe').fetchall()==[(7,)]
                    try: connection.execute('INSERT INTO probe VALUES (8)')
                    except sqlite3.OperationalError: pass
                    else: raise AssertionError('read-only copy permits writes')
                snapshots[member] = preflight.sha256_file(copied)
        output_text = ''.join(o.get('text','') for c in code for o in c.outputs)
        receipts = re.findall(r'Result ZIP SHA-256: ([0-9a-f]{64})',output_text)
        assert receipts == [preflight.sha256_file(archive_path)]
        result['cases'][name] = {'executed':True,'execution_counts':[1,2,3],'cell_sources_unchanged':True,
            'root_blocker':summary['root_blocker'],'zip_path':archive_path.relative_to(ROOT).as_posix(),
            'zip_sha256':receipts[0],'zip_members':len(members),'tests_passed':0,
            'snapshot_sha256':snapshots,'snapshot_integrity':'ok','read_only_enforced':True,
            'model_generations':0}
    assert preflight.sha256_file(original)==result['notebook_sha256']
    preflight.save_json(evidence/'validation.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
