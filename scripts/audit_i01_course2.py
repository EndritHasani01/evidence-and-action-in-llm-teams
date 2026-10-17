"""Read-only course-2 audit and small temporary counterexamples; no inference.

Run from the checkout: python -X utf8 scripts/audit_i01_course2.py
Only the audit receipt is written in the checkout. Supplied evidence is hashed
before and after; archive extraction and all synthetic writers use temp dirs.
"""
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from recovery.i01.archive import export, extract_selected, verify
from recovery.i01.core import canonical, manifests, messages
from recovery.i01.inference import split_visible
from recovery.i01.report import analysis
from recovery.i01.workflow import Session, initialize


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(view, seed, mode, **flags):
    return dict(view=view, seed=seed, settings={'mode': mode}, input_ids=[1],
                rendered=canonical(view), **flags)


class Scripted:
    def __init__(self, reply=None):
        self.calls = 0
        self.reply = reply

    def obtain(self, request, timeout):
        self.calls += 1
        if self.reply:
            return self.reply(request)
        return dict(failure=None, visible_text='', ready_seconds=.001,
                    input_tokens=1, generated_tokens=512, token_ids=[request['seed']],
                    backend=dict(finite_score_steps=1,
                                 cache=dict(initial_empty=True, same_call_cache=True),
                                 observed_peak_free_lower_bytes=2**31))

    def close(self):
        return dict(termination_confirmed=True)


def fixture(parent, name):
    run = parent/name
    initialize(run, ROOT, json.loads((ROOT/'configs/i01-course.json').read_text()))
    workers = [Scripted(), Scripted()]
    s = Session(run, providers=workers, prepare_request=prepare)
    s.window((datetime.now(timezone.utc)+timedelta(hours=2)).isoformat(),
             'Synthetic fixture only; not provider allowance evidence')
    return s, workers


def audit():
    supplied = ROOT/'notebooks/run/course-2'
    hashes = {p.name: dict(bytes=p.stat().st_size, sha256=digest(p))
              for p in supplied.iterdir() if p.is_file()}
    cases = {}
    with tempfile.TemporaryDirectory(prefix='i01-course2-review-') as name:
        temp = Path(name)
        run = temp/'observed'
        integrity = extract_selected(supplied/'latest.zip', run)
        verify(run)
        archived = json.loads((run/'reports/analysis.json').read_text())
        rebuilt = analysis(run)
        assert canonical(rebuilt) == canonical(archived)
        release = json.loads((run/'source/source-release.json').read_text())
        for rel, wanted in release['files'].items():
            p = run/'source'/rel
            assert p.stat().st_size == wanted['bytes'] and digest(p) == wanted['sha256'], rel
            if rel.startswith('recovery/') and rel.endswith('.py'):
                assert p.read_bytes() == (ROOT/rel).read_bytes(), 'Audit source differs: '+rel
        with zipfile.ZipFile(next((run/'source').glob('*.whl'))) as wheel:
            wheel_members = [p for p in wheel.namelist()
                             if p.startswith('recovery/') and p.endswith('.py')]
            assert all(wheel.read(p) == (run/'source'/p).read_bytes() for p in wheel_members)
        notebook = json.loads((supplied/'multi-agents-course-v1nb.ipynb').read_text())
        baseline = json.loads((run/'source/notebooks/i01_course_kaggle.ipynb').read_text())
        changed = [a.get('id') for a, b in zip(notebook['cells'], baseline['cells'])
                   if ''.join(a['source']) != ''.join(b['source'])]
        assert changed == ['session-window']
        assert manifests(rebuilt['manifest']['config'])['worlds'] == rebuilt['manifest']['worlds']
        worlds = {w['id']: w for w in rebuilt['manifest']['worlds']}
        controls, timing = [], []
        requests = []
        for trace in rebuilt['traces']:
            r, o = json.loads(trace['request']), json.loads(trace['outcome'])
            requests.append(r)
            assert r['messages'] == messages(r['view'], control=True)
            assert all(v == 1 for v in r['attention_mask'])
            assert o['input_tokens'] == len(r['input_ids'])
            assert o['generated_tokens'] == len(o['token_ids'])
            assert r['seed'] == o['backend']['seed'] == o['backend']['cpu_seed'] == o['backend']['cuda_seed']
            assert o['termination'] == 'eos' and not any(o.get(k) for k in ['failure','framing_error','truncated'])
            if trace['episode'].startswith('qualification-'):
                wid, phase = trace['episode'].split('/')
                input_phase = 'revised' if 'revised' in phase else 'original'
                truth = max(r['view']['complete_input'])
                assert truth == worlds[wid][input_phase+'_truth']
                controls.append(dict(call=trace['id'], slot=trace['slot'], truth=truth,
                                     answer=json.loads(o['visible_text'])['submit'],
                                     ready_seconds=o['ready_seconds'], input_tokens=o['input_tokens'],
                                     generated_tokens=o['generated_tokens']))
        for c in notebook['cells']:
            if c.get('execution_count') is None or c['cell_type'] != 'code':
                continue
            e = c['metadata']['execution']
            start = datetime.fromisoformat(e['iopub.status.busy'])
            stop = datetime.fromisoformat(e['iopub.status.idle'])
            timing.append(dict(cell=c['id'], execution=c['execution_count'], start=start.isoformat(),
                               stop=stop.isoformat(), seconds=(stop-start).total_seconds(),
                               serialized_output_characters=sum(len(json.dumps(o)) for o in c['outputs'])))
        # Replay the exact already-recorded direct screen with no provider call.
        def replay_prepare(view, seed, mode, **flags):
            return next(r for r in requests if r['view'] == view and r['seed'] == seed
                        and r['settings']['mode'] == mode)
        workers = [Scripted(), Scripted()]
        s = Session(run, providers=workers, prepare_request=replay_prepare)
        try:
            receipt = s.screen('direct')
            assert receipt['correct'] == 10 and receipt['protocol_errors'] == 0
            assert sum(w.calls for w in workers) == 0
            assert s.admission.usage()['attempts'] == 18
            cases['recorded_direct_screen_exact_replay'] = dict(**receipt, new_provider_calls=0, attempts=18)
        finally:
            s.close()
        # Current load references alone do not force the initial envelope IDs to change.
        s, workers = fixture(temp, 'stale-envelope')
        try:
            s.meta.put_meta('screen/direct', dict(passed=True))
            for slot, store in enumerate(s.stores):
                store.put_meta('resident_load', f'{s.session_id}/original-{slot}')
            s.envelope('direct')
            before = s.admission.usage()['attempts']
            s.stores[1].put_meta('resident_load', f'{s.session_id}/replacement-1')
            receipt = s.envelope('direct')
            mode = s.qualified()
            cases['changed_load_without_reload_flag'] = dict(passed=receipt['passed'], qualified_mode=mode,
                new_scripted_probes=s.admission.usage()['attempts']-before,
                adopted_current_load_refs=receipt['loads']==s.load_references())
            assert receipt['passed'] and s.admission.usage()['attempts'] == before
        finally:
            s.close()
        # A model hitting its thinking cap is classified as a global runtime defect.
        s, workers = fixture(temp, 'thinking-framing')
        try:
            tokenizer = SimpleNamespace(encode=lambda text, **kw: list(text))
            thinking_text = 'x'*4096  # Synthetic one-character tokens at the total cap.
            _, _, framing = split_visible(tokenizer, SimpleNamespace(text=thinking_text), 'thinking')
            for w in workers:
                w.reply = lambda req: dict(failure=None, raw_text=thinking_text, visible_text='',
                    token_ids=[120]*4096, generated_tokens=4096, ready_seconds=.001, input_tokens=1,
                    truncated=True, termination='length', framing_error=framing)
            world = next(w for w in s.manifest['worlds'] if w['id'] == 'pilot-00')
            try:
                s.episode(world, 'prefix', 'thinking')
            except ValueError as error:
                reason = str(error)
            else:
                raise AssertionError('Expected current global defect classification')
            cases['thinking_truncation_global_defect'] = dict(framing_error=framing,
                global_model_defect=bool(s.meta.meta('model_defect')), error=reason,
                state=s.stores[0].state('pilot-00/prefix'))
        finally:
            s.close()
        # Slot identity is absent from the shared manifest binding.
        s, workers = fixture(temp, 'duplicated-slot')
        try:
            world = s.manifest['worlds'][0]
            workers[0].reply = lambda req: dict(failure=None, visible_text=canonical(
                dict(message=None, submit=world['original_truth'], wait=False)), ready_seconds=.001,
                input_tokens=1, generated_tokens=1)
            s.control(world, 'original', 'direct', stage='direct')
        finally:
            s.close()
        shutil.copy2(temp/'duplicated-slot/worker-0.sqlite', temp/'duplicated-slot/worker-1.sqlite')
        s = Session(temp/'duplicated-slot')
        try:
            traces = analysis(s.run)['traces']
            cases['duplicated_canonical_slot_accepted'] = dict(open_accepted=True,
                reported_attempts=s.admission.usage()['attempts'], distinct_calls=len({r['id'] for r in traces}))
        finally:
            s.close()
        # Restoring the latest safe boundary erases an already recorded earlier gap.
        s, _ = fixture(temp, 'saved-gap')
        try:
            s.meta.put_meta('lost_spending', dict(upper=3, resolved=True, evidence='Earlier bounded lost calls'))
            s.meta.put_meta('blocked_worlds', ['main-00'])
            before = s.admission.usage()['remaining']
            packet = export(s.run, s.stores, boundary='synthetic-earlier-gap', reports=False)
        finally:
            s.close()
        from recovery.i01.cli import main
        with redirect_stdout(io.StringIO()):
            main(['--source',str(ROOT),'--run',str(temp/'restored-gap'),'restore',packet['path'],
                  '--tail','latest','--evidence','No additional tail after the supplied snapshot'])
        s = Session(temp/'restored-gap')
        try:
            cases['restore_clears_prior_lost_spending'] = dict(before_remaining=before,
                after_remaining=s.admission.usage()['remaining'], lost_spending=s.meta.meta('lost_spending'),
                blocked_worlds=s.meta.meta('blocked_worlds'))
            assert s.admission.usage()['remaining'] == before+3
        finally:
            s.close()
        # A real commit between SELECT calls and SELECT attempts breaks live analysis.
        s, _ = fixture(temp, 'read-race')
        from recovery.i01.store import connection
        injected = False
        class Reader:
            def __init__(self, path, *args, **kwargs):
                self.db = connection(path,*args,**kwargs)
                self.slot0 = Path(path).name == 'worker-0.sqlite'
            def execute(self, sql, *args):
                nonlocal injected
                if self.slot0 and sql == 'SELECT * FROM attempts' and not injected:
                    injected = True
                    s.stores[0].register('race-call','race-episode',prepare({},1,'direct'))
                    s.admission.admit(s.stores[0],'race-call','direct')
                return self.db.execute(sql,*args)
            def close(self):
                self.db.close()
        try:
            with patch('recovery.i01.report.connection', Reader):
                try:
                    analysis(s.run)
                except KeyError as error:
                    cases['live_read_without_transaction'] = dict(error=repr(error),
                        write_committed_between_tables=True, saved_call_and_attempt_intact=True)
                else:
                    raise AssertionError('Expected current read consistency failure')
        finally:
            s.close()
    assert hashes == {p.name: dict(bytes=p.stat().st_size,sha256=digest(p))
                      for p in supplied.iterdir() if p.is_file()}
    receipt = dict(audit_only=True, supplied_files_unchanged=True, files=hashes,
        source_head=release['git_head'], zip_members=1+len(integrity['files']),
        verified_integrity_entries=len(integrity['files']), verified_source_files=len(release['files']),
        verified_wheel_python_files=len(wheel_members), exact_read_only_reconstruction=True,
        shipped_python_modules_match_checkout=True,
        changed_notebook_cells=changed, executed_cell_timing=timing,
        controls=sorted(controls,key=lambda r:r['call']),
        observed_failure_analysis=archived['failure_analysis'],
        summary={k:v for k,v in archived['summary'].items() if k!='gates'},
        counterexamples=cases, new_real_model_attempts=0, gpu_inference_executed=False)
    output = ROOT/'docs/validation/course-2-audit.json'
    output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(output)
    print(json.dumps(cases,indent=2))


if __name__ == '__main__':
    audit()
