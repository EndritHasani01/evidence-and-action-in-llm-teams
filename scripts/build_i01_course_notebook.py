"""Reproducible thin N00–N24 notebook; rendering never starts research calls."""

import json
from pathlib import Path


BOOTSTRAP = '''from pathlib import Path
import hashlib, json, shutil, sys, tempfile, zipfile

# Select one exact small source attachment. ZIP and Kaggle-expanded roots work.
SOURCE_BUNDLE = None  # Set only if more than one candidate is attached.
source_candidates = list(Path('/kaggle/input').rglob('i01-source.zip'))
source_candidates += [p.parent for p in Path('/kaggle/input').rglob('source-release.json')]
if SOURCE_BUNDLE is None:
    if len(source_candidates) != 1:
        raise RuntimeError(f'Select SOURCE_BUNDLE explicitly; candidates: {source_candidates}')
    SOURCE_BUNDLE = source_candidates[0]
selected_source = Path(SOURCE_BUNDLE)
source_root = Path('/kaggle/working/i01-source')
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
    for relative, wanted in release['files'].items():
        path = staging/relative
        if not path.is_file() or path.stat().st_size != wanted['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != wanted['sha256']:
            raise RuntimeError(f'Source identity failed: {relative}')
        if source_root.exists() and (not (source_root/relative).is_file() or hashlib.sha256((source_root/relative).read_bytes()).hexdigest() != wanted['sha256']):
            raise RuntimeError('Existing source differs; select a fresh session/source directory')
    if not source_root.exists():
        shutil.copytree(staging, source_root)
sys.path.insert(0, str(source_root))
from recovery.i01.ui import Operator
if 'ui' not in globals():
    ui = Operator(source_root)
ui.bootstrap_status()
'''


def notebook():
    cells=[]
    def markdown(text): cells.append(dict(cell_type="markdown",id=f"i01-text-{len(cells):02d}",metadata={},source=text.splitlines(True)))
    def code(text,cell_id): cells.append(dict(cell_type="code",id=cell_id,metadata={"i01_stage":cell_id},execution_count=None,outputs=[],source=text.splitlines(True)))
    markdown('''# N00 · I-01 distributed-team recovery study

**Prepared implementation; Kaggle acceptance and research execution pending.**
This is a controlled recovery extension of SILO-BENCH I-01: two agents, twenty
integers each, a withdrawn unique winner, and paired retain/clear continuations
over twenty independent worlds. Maximum **500 new physical attempts**, including
all diagnostics, failures and eligible retries; prior historical attempts stay separate.

`shared prefix → factual revision → isolated retain / clear → revised control`

Use **Internet On**, **T4 ×2**, and a private source input. Run All renders
controls only. Each button/explicit command requests one bounded stage; passing
a gate starts no later stage. No agent sees evaluator truth or the other private
shard. Submissions are final within a phase; only the revision reopens both agents.
Keep the latest checkpoint downloaded off session. See `START_HERE.md` for recovery.
''')
    stages=[
      ("N01", "Workspace, exact source and actual host", "This cell performs only small source/UI initialization and read-only inventory. If several source inputs are attached, set `SOURCE_BUNDLE` to one exact path. Scratch/cache and writable evidence are separate.", BOOTSTRAP),
      ("N02", "Online setup", "Click once to install the pinned isolated Python environment and pinned metadata/tokenizer. Logs are in `/kaggle/working/i01-setup/`. No weights or model calls. An incompatible host stops before inference.", "ui.panel('setup', 'Online setup', ceiling=0)\n"),
      ("N03", "Initialize, restore, or reopen; current session allowance", "Choose the mode explicitly. Restore accepts one exact ZIP or expanded bundle in a fresh run directory. `tail='latest'` needs evidence that the snapshot is current and the old session stopped; `unknown` blocks generation. Set the actual UTC deadline/allowance seen in Kaggle before loading models. New worlds and schedules are saved before any generation.", "ui.panel('initialize', 'Initialize / restore / reopen', ceiling=0, mode='new', selected='', tail='latest', evidence='')\nui.panel('window', 'Set actual session allowance', ceiling=0, deadline='', evidence='')\n"),
      ("N04", "Lightweight self-check", "Run packaged mathematical, view/finality, admission, persistence, snapshot/restore and native-tokenizer checks. Uses temporary scripted stores and **zero model attempts**. A passing native receipt is required before weight staging.", "ui.panel('selfcheck', 'Lightweight self-check', ceiling=0)\n"),
      ("N05", "Pinned online weights", "Download or reuse exactly the pinned 9B revision. Native Git/LFS file inventory, hashes, partial-cache reuse and measured space are checked; no fallback model or weight upload bundle.", "ui.panel('weights', 'Pinned weights', ceiling=0)\n"),
      ("N06", "Load two resident replicas", "Load/attach one replica per actual T4 with no hidden warmup. Inspect device/process identity, load time and VRAM. The retained controller uses the isolated interpreter; models stay resident when this cell returns.", "ui.panel('load', 'Load two replicas', ceiling=0)\nui.panel('status', 'Resident status', ceiling=0)\n"),
      ("N07", "Six fresh-state readiness calls", "Fixed A/B/A checks on each GPU. All six calls count. Empty fresh cache and finite-score instrumentation govern readiness; repeated-output equality is supporting evidence.", "ui.panel('readiness', 'Run six readiness checks', ceiling=6)\n"),
      ("N08", "Direct competence screen", "Twelve complete-input controls: original/revised pairs over six separate worlds. Require ≥11/12 correct and no malformed/truncated actions. This is not a main-world filter.", "ui.panel('screen', 'Direct screen', ceiling=12, mode='direct')\n"),
      ("N09", "Qualification inspection and download", "Inspect every request/reply and the cumulative checkpoint. Direct failure does not automatically enable thinking. Diagnose malformed/framing/provider failures first; thinking is conditional on a documented competence limitation.", "ui.inspect_panel(default_world='qualification-00')\n"),
      ("N10", "Conditional thinking screen", "This action refuses if direct passed, a protocol defect exists, or no competence justification is supplied. It is never automatic. Thinking tokens/time count and remain separate audit material.", "ui.panel('screen', 'Conditional thinking screen', ceiling=12, mode='thinking', reason='')\n"),
      ("N11", "Select mode and measure full envelope", "Select a passing declared mode. Two diagnostics use 8,192 input tokens plus the full 512/4,096 output reserve and require ≥1.5 GiB observed free headroom on each GPU. Output forcing belongs only here. In a new/restored/reloaded session set `reload=True`; the two probes consume contingency.", "ui.panel('envelope', 'Selected-mode envelope', ceiling=2, mode='direct', reload=False)\nui.inspect_panel()\n"),
      ("N12", "Pilot 1 only", "Execute exactly pilot 1: shared original team, isolated siblings and both full-information controls. Stop at its boundary; no next pilot starts. Maximum twenty first attempts plus separately counted eligible retries.", "ui.panel('pilot', 'Execute pilot 1', ceiling=20, number=1)\n"),
      ("N13", "Pilot 1 · inspect, download, review", "Review the complete original/recovery/control conversations, outcomes, costs and errors. Download the cumulative checkpoint off session. Record original communication usefulness and operational usability, with trace references; recovery wrong answers alone do not fail the gate. The review does not claim browser-download success.", "ui.inspect_panel(default_world='pilot-00')\nui.panel('review', 'Record pilot 1 review', ceiling=0, scope='pilot-1', notes='', useful_communication=False, usable=False)\n"),
      ("N14", "Pilot 2 only", "Requires pilot 1's completed inspection/export review. Executes only the second fixed pilot, including both controls.", "ui.panel('pilot', 'Execute pilot 2', ceiling=20, number=2)\n"),
      ("N15", "Pilot 2 · inspect, download, review", "Inspect every agent turn and download the complete cumulative archive, including failures. Record the second pilot's review before proceeding.", "ui.inspect_panel(default_world='pilot-01')\nui.panel('review', 'Record pilot 2 review', ceiling=0, scope='pilot-2', notes='', useful_communication=False, usable=False)\n"),
      ("N16", "Pilot 3 only", "Requires pilot 2's completed inspection/export review. Covers the third fixed structural pilot without selecting by outcomes.", "ui.panel('pilot', 'Execute pilot 3', ceiling=20, number=3)\n"),
      ("N17", "Pilot 3 · inspect, download, review", "Review original teamwork and six total pilot controls. Assess conversation usability and resource costs; do not select for treatment significance or direction.", "ui.inspect_panel(default_world='pilot-02')\nui.panel('review', 'Record pilot 3 review', ceiling=0, scope='pilot-3', notes='', useful_communication=False, usable=False)\n"),
      ("N18", "Pilot gate, forecast and explicit freeze", "Status includes the measured conservative forecast, actual remaining allowance and gate evidence. Freeze binds mode/settings/runtime, inputs/orders/seeds, prompts, deadlines/endpoints and the review rubric. It makes zero main calls; download the pre-main checkpoint.", "ui.panel('status', 'Gate and resource status', ceiling=0)\nui.panel('freeze', 'Explicit freeze', ceiling=0, notes='')\n"),
      ("N19", "Prepare the next fixed main batch", "Prepare one/two next predetermined incomplete IDs; a pending scope resumes exactly. The preview shows planned first attempts (≤19/38), eligible contingency, remaining study allowance and deadline margin. Prior batch review/export is required.", "ui.panel('prepare_batch', 'Prepare next fixed batch', ceiling=0, count=2)\n"),
      ("N20", "Execute the prepared batch once", "This action uses the saved N19 scope only. One serial model child per T4; two-world scopes can dispatch concurrently with one global admission owner. Pause stops new dispatch and settles bounded in-flight work. Completed raw outcomes never regenerate.", "ui.panel('main', 'Execute prepared batch', ceiling=38)\nui.panel('pause', 'Request pause', ceiling=0)\n"),
      ("N21", "Main batch · inspect, download, review", "Inspect all world/phase/agent traces and cumulative paired results with intended denominators. Download the archive and record the displayed batch ID's review before preparing another scope. Repeat N19–N21 deliberately.", "ui.inspect_panel()\nui.panel('status', 'Show current batch ID', ceiling=0)\nui.panel('review', 'Record main batch review', ceiling=0, scope='', notes='')\n"),
      ("N22", "Session controls and exact pending-scope resume", "Pause → wait for quiescence → checkpoint/download → close models/controller → stop Kaggle UI. For restored sessions, load then explicitly run two reload probes before pending-scope resume. Process exit does not prove provider release. See the runbook for unresolved attempt and lost-tail reconciliation commands.", "ui.panel('status', 'Session status', ceiling=0)\nui.panel('pause', 'Request safe pause', ceiling=0)\nui.panel('snapshot', 'Checkpoint / export', ceiling=0)\nui.panel('close_models', 'Close resident models', ceiling=0)\nui.panel('envelope', 'Budgeted reload validation', ceiling=2, mode='direct', reload=True)\nui.panel('main', 'Resume saved pending scope', ceiling=38)\nui.panel('shutdown', 'Close controller', ceiling=0)\n"),
      ("N23", "Read-only final or partial analysis", "Reconstruct intended coverage, exact paired success, correct-prefix stratum, exploratory intervals and missingness bounds, ready-model seconds, token/call costs and observable failures. Reporting makes no inference call and works without loaded models. All plots export SVG/PNG with plotting data. Add human rubric annotations through the explicit command below; ambiguous mechanisms stay ambiguous.", "ui.panel('report', 'Reconstruct reports and figures', ceiling=0)\nui.inspect_panel()\nprint(\"Annotation: ui.annotate('unique-review-id', 'ambiguous', ['exact/call/id'], 'Trace-based notes')\")\n"),
      ("N24", "Final reproducibility archive and session end", "Create the final/partial archive and inspect its integrity inventory and complete source/evidence/report contents. Use `ui.verify_checkpoint()` to restore into a fresh temporary directory and compare outcomes/costs/traces with archived analysis; it makes zero model calls. Save/download the **executed notebook** separately through Kaggle (without Save & Run All). Download the archive off session; close models/controller, then stop Kaggle via its UI. Partial coverage stays partial.", "ui.panel('snapshot', 'Final portable archive', ceiling=0)\nui.links()\nprint('Fresh-directory reconstruction: ui.verify_checkpoint()')\nui.panel('close_models', 'Final close models', ceiling=0)\nui.panel('shutdown', 'Final close controller', ceiling=0)\n")
    ]
    for stage,title,description,body in stages:
        markdown(f"## {stage} · {title}\n\n{description}\n")
        code(body,stage.lower())
    return dict(nbformat=4,nbformat_minor=5,cells=cells,
                metadata=dict(kernelspec=dict(display_name="Python 3",language="python",name="python3"),
                              language_info=dict(name="python"),
                              kaggle=dict(accelerator="gpu",isInternetEnabled=True),
                              i01=dict(regime="i01-course-v1",research_execution="explicit controls only",kaggle_verified=False)))


def build(path):
    value=notebook()
    for cell in value["cells"]:
        if cell["cell_type"]=="code": compile("".join(cell["source"]),cell["id"],"exec")
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return path


if __name__=="__main__":
    print(build(Path(__file__).resolve().parents[1]/"notebooks/i01_course_kaggle.ipynb"))
