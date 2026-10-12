"""Build the current committed course source plus a guarded CPU/GPU notebook."""

import argparse
import json
from pathlib import Path
from pprint import pformat

from scripts.build_course_smoke_packet import build


def hardware_notebook(expected, helper, launch):
    def cell(kind,text,identifier):
        value = dict(cell_type=kind,id=identifier,metadata={},source=text.splitlines(keepends=True))
        if kind == "code":
            value.update(execution_count=None,outputs=[])
        return value
    instructions = """# Course M5-T02: one launch, T4 x2 from the start

This local packet is unpublished. Attach the exact new course source payload
as a private input. You may select **T4 x2 before starting**. Set
`COURSE_M5_PAYLOAD` and `COURSE_M5_HW_OUTPUT` when reviewing
locally; use fresh output paths and preserve all previous results.

Both execution flags default **False**. Edit the visible `LAUNCH` dictionary at
the top of the source cell once, setting both flags True for the authorized run,
using supported prior
allocation/smoke bounds and the separately authorized concrete action. Available
quota is independent of study spending; accounts do not reset the 30-hour course
or cumulative 24-attempt / 1,800-device-second smoke ceilings. Unknowns stop
admission. No pilot/main/freeze is authorized by this notebook.

Record the actual UTC GPU assignment clock in LAUNCH before the first cell,
with remaining provider allowance and release instructions. Run the source,
asset preparation, model smoke and export cells in order. No accelerator switch
or second launch configuration is needed. Asset preparation uses CPU operations
while both GPUs are assigned; installation/downloads/idle time count against
the same cumulative smoke allowance. Preparation and inference use independent
bounded process-group controllers and retain the original assignment clock.
Insufficient time stops work and preserves evidence; it does not extend limits.
The installed candidate is checked before weights and model work.

Download the result ZIP and this executed notebook, then **Stop Session** and
confirm provider deallocation within the reserved release time. Kernel exit is
not provider release. Do not use Save & Run All to retrieve evidence. Retain
actual release time/receipt for off-host allocation reconciliation; open allocation
and unresolved physical R7 coverage withhold hardware acceptance. A short
successful model run cannot establish the complete-envelope memory/headroom gate.
"""
    bootstrap = ("import hashlib,json,os,sys,time\nfrom pathlib import Path\n"
        f"LAUNCH={pformat(launch,sort_dicts=False)}\n"
        f"EXPECTED=json.loads({json.dumps(expected,sort_keys=True)!r})\n"
        f"HELPER={helper!r}\n"
        "assert hashlib.sha256(HELPER.encode()).hexdigest()==EXPECTED['review_helper_sha256']\n"
        "helpers={'__name__':'course_hardware_helper'}\n"
        "exec(compile(HELPER,'m5_kaggle_preflight.py','exec'),helpers)\n"
        "configured=os.environ.get('COURSE_M5_PAYLOAD')\n"
        "matches=[Path(configured)] if configured else list(Path('/kaggle/input').rglob(EXPECTED['payload_filename']))\n"
        "assert len(matches)==1,'Attach the one exact current source payload'\n"
        "output=Path(os.environ.get('COURSE_M5_HW_OUTPUT','/kaggle/working/course-m5-hardware')).resolve()\n"
        "assert not output.exists(),'Fresh output required; preserve previous evidence'\n"
        "output.mkdir(parents=True)\nsource=output/'source'\n"
        "source_facts=helpers['admit_source'](matches[0].resolve(),source,EXPECTED)\n"
        "manifest_path=output/'source-manifest.json'\n"
        "helpers['save_json'](manifest_path,EXPECTED)\n"
        "LAUNCH['source_manifest']=str(manifest_path)\n")
    cpu = """cpu_output=output/'cpu-assets'
launch_path=output/'launch.json'
helpers['save_json'](launch_path,LAUNCH)
scratch=Path(os.environ.get('COURSE_M5_ASSET_SCRATCH','/kaggle/working/course-m5-assets')).resolve()
if not LAUNCH['stage_weights']:
    cpu_output.mkdir()
    helpers['save_json'](cpu_output/'report.json',dict(status='blocked',reason='CPU staging disabled pending authorization/resources',gpu_execution=False,weights_staged=False))
else:
    try:
        import runpy
        asset_helpers=runpy.run_path(str(source/'scripts/m5_course_smoke_assets.py'))
        assigned=bool(asset_helpers['assigned_device_count']() or LAUNCH.get('allocated_at'))
        if assigned:
            wall=asset_helpers['assigned_preparation_window'](LAUNCH)
            deadline=time.monotonic()+wall-LAUNCH['budget']['shutdown_seconds']-124
            timeout=int(deadline-time.monotonic()-helpers['EXPORT_SECONDS']-8)
            assert timeout>0,'Insufficient allowance: export and stop the GPU session'
        else:
            deadline=time.monotonic()+2100
            timeout=1800
        helpers['command'](output,'cpu-asset-preparation',[sys.executable,'-I',str(source/'scripts/m5_course_smoke_assets.py'),
            'prepare','--root',str(source),'--manifest',str(manifest_path),'--launch',str(launch_path),
            '--scratch',str(scratch),'--output',str(cpu_output),'--workflow-seconds',str(timeout)],deadline=deadline,
            timeout=timeout,cwd=output,env=dict(os.environ))
    except (Exception,KeyboardInterrupt) as error:
        cpu_output.mkdir(exist_ok=True)
        helpers['save_json'](cpu_output/'report.json',dict(status='blocked',reason=str(error),gpu_execution=False,
            weights_staged=None,provider_assignment_utc=LAUNCH.get('allocated_at'),provider_release_confirmed=False))
assets_path=cpu_output/'prepared-assets.json'
print(json.loads((cpu_output/'report.json').read_bytes()))
"""
    gpu = """gpu_output=output/'gpu-smoke'
if not LAUNCH['execute_gpu']:
    gpu_output.mkdir()
    helpers['save_json'](gpu_output/'report.json',dict(status='blocked',reason='GPU execution disabled',gpu_admission=False,model_generations=0,physical_memory_accepted=False,provider_release_confirmed=False))
else:
    try:
        assert assets_path.exists(),'Asset preparation must pass before model loading; stop if missing'
        assets=json.loads(assets_path.read_bytes())
        LAUNCH.update(assets_receipt=str(assets_path),hf_cache=assets['hf_cache'])
        helpers['save_json'](launch_path,LAUNCH)
        assert LAUNCH['allocated_at'],'Record actual UTC GPU assignment before running this cell'
        from datetime import datetime,timezone
        assigned=datetime.fromisoformat(LAUNCH['allocated_at'])
        assert assigned.tzinfo is not None
        elapsed=(datetime.now(timezone.utc)-assigned).total_seconds()
        assert elapsed>=0
        prior=LAUNCH['budget']['prior_smoke_gpu_hours']
        assert prior is not None,'Prior smoke use is unknown'
        wall=(1800-3600*prior[1])/2-elapsed
        wall=min(wall,LAUNCH['provider_session_seconds']-elapsed)
        stop_reserve=LAUNCH['budget']['shutdown_seconds']
        timeout=int(wall-stop_reserve-helpers['EXPORT_SECONDS']-8)
        assert timeout>0,'Insufficient allowance: stop the GPU session'
        helpers['command'](output,'bounded-model-smoke',[assets['interpreter'],'-I',str(source/'scripts/m5_course_smoke.py'),
            '--root',str(source),'--launch',str(launch_path),'--output',str(gpu_output)],
            deadline=time.monotonic()+wall-stop_reserve,timeout=timeout,cwd=output,env=dict(os.environ))
    except (Exception,KeyboardInterrupt) as error:
        helpers['save_json'](output/'controller-stop.json',dict(reason=str(error),provider_release_confirmed=False,
            physical_memory_accepted=False,incomplete=True))
    print('Download evidence and Stop Session now. Provider release and R7 acceptance remain to be reviewed.')
"""
    export = """EXPORTED=helpers['export_evidence'](output)
from IPython.display import FileLink,display
display(FileLink(EXPORTED['zip_path']))
print(json.dumps(EXPORTED,indent=2))
print('Retain the actual executed notebook and ZIP. Confirm provider release; do not rerun model calls to save evidence.')
"""
    return dict(nbformat=4,nbformat_minor=5,metadata=dict(kernelspec=dict(display_name="Python 3",language="python",name="python3"),
        language_info=dict(name="python")),cells=[cell("markdown",instructions,"hardware-instructions"),
        cell("code",bootstrap,"hardware-source"),cell("code",cpu,"hardware-cpu-assets"),
        cell("code",gpu,"hardware-gpu-smoke"),cell("code",export,"hardware-export")])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path.cwd())
    for name in ("tokenizer","prepared","inspection","output"):
        parser.add_argument("--"+name,type=Path,required=True)
    args = parser.parse_args()
    root, output = args.root.resolve(),args.output.resolve()
    manifest = build(root,args.tokenizer,args.prepared,args.inspection,output)
    helper = (root/"scripts/m5_kaggle_preflight.py").read_text(encoding="utf-8")
    launch = json.loads((root/"configs/course-smoke-launch.json").read_bytes())
    if launch["execute_gpu"] is not False or launch["stage_weights"] is not False:
        raise ValueError("deliver guarded defaults; authorization remains an external action")
    (output/"course_m5_hardware_smoke.ipynb").write_text(json.dumps(hardware_notebook(manifest,helper,launch),indent=1)+"\n",encoding="utf-8")
    (output/"launch-template.json").write_text(json.dumps(launch,indent=2)+"\n",encoding="utf-8")


if __name__ == "__main__":
    main()
