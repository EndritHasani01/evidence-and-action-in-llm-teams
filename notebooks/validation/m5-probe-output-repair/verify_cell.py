"""Real Jupyter wiring of the exact continuation cell, with candidate calls controlled."""

import asyncio
import hashlib
import json
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
legacy=nbformat.read(ROOT/'notebooks/recovery_m5_kaggle_preflight_v3.ipynb',as_version=4)
cell_path=ROOT/'notebooks/recovery_m5_kaggle_continue_run4.py'
cell=cell_path.read_text(encoding='utf-8')
seed=f'''
from contextlib import ExitStack
from unittest.mock import patch
from tests.test_kaggle_preflight import PreflightTests
import platform,sys,inspect
testcase=PreflightTests();testcase.setUp()
testcase.expected['helper_sha256']=hashlib.sha256(PREFLIGHT_PROGRAM.encode()).hexdigest()
EXPECTED=testcase.expected
testcase.output=Path({str(OUT/'controlled-case')!r})
scope=ExitStack()
scope.enter_context(patch.object(platform,'system',return_value='Linux'))
scope.enter_context(patch.object(platform,'machine',return_value='x86_64'))
scope.enter_context(patch.object(sys,'version_info',(3,13,15,'final',0)))
preflight_namespace['command']=testcase.controlled_command
preflight_namespace['process_tree_diagnostic']=lambda *args:{{'scope':'controlled host diagnostic'}}
PREFLIGHT_RESULT=preflight_namespace['run_preflight'](testcase.inputs,testcase.output,testcase.scratch,EXPECTED,testcase.lock)
assert PREFLIGHT_RESULT['report']['stages']['environment']['status']=='passed'
assert PREFLIGHT_RESULT['summary']['root_blocker'].startswith('JSONDecodeError:')
original_zip_hash=preflight_namespace['sha256_file'](Path(PREFLIGHT_RESULT['zip_path']))
scratch=Path(PREFLIGHT_RESULT['report']['scratch_directory'])
interpreter=scratch/'venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
interpreter.parent.mkdir(exist_ok=True);interpreter.touch()
testcase.command_calls.clear()
'''
verify=f'''
assert CONTINUATION_RESULT['summary']['continuation_checks_passed']
assert CONTINUATION_RESULT['summary']['tests_passed']==97
assert CONTINUATION_RESULT['summary']['model_generations']==0
assert preflight_namespace['sha256_file'](Path(PREFLIGHT_RESULT['zip_path']))==original_zip_hash
assert len(inspect.signature(preflight_namespace['installed_probe_script']).parameters)==2
assert continuation_namespace is not preflight_namespace
assert not any(n.startswith(('download-','install-','create-venv')) for n,_,_ in testcase.command_calls)
scope.close()
data={{'status':'passed','scope':'Real Jupyter cell wiring; candidate/import/test outcomes controlled',
       'cell_sha256':hashlib.sha256(Path({str(cell_path)!r}).read_bytes()).hexdigest(),
       'original_namespace_and_failed_export_preserved':True,'controlled_test_count':97,
       'model_generations':0,'actual_linux_continuation_acceptance':None,
       'continuation_zip':CONTINUATION_RESULT['zip_path'],'original_zip':PREFLIGHT_RESULT['zip_path']}}
Path({str(OUT/'kernel-validation.json')!r}).write_text(json.dumps(data,indent=2)+'\\n')
print(json.dumps(data,indent=2))
'''
notebook=nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(legacy.cells[1].source),
    nbformat.v4.new_code_cell(seed),nbformat.v4.new_code_cell(cell),nbformat.v4.new_code_cell(verify)])
if sys.platform=='win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
executed=NotebookClient(notebook,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(ROOT)}}).execute()
assert executed.cells[2].source==cell
assert [c.execution_count for c in executed.cells]==[1,2,3,4]
assert not any(o.output_type=='error' for c in executed.cells for o in c.outputs)
nbformat.write(executed,OUT/'executed-cell.ipynb')
print((OUT/'kernel-validation.json').read_text())
