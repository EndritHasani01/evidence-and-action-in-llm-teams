"""Read-only course-3/direct-versus-thinking evidence audit; no model calls."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import statistics
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from recovery.i01.archive import extract_selected
from recovery.i01.core import canonical, manifests, messages, validate_action
from recovery.i01.report import analysis


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_identity(path):
    return dict(bytes=path.stat().st_size, sha256=digest(path))


def summarize(rows):
    return dict(calls=len(rows), generated_tokens=sum(o['generated_tokens'] for o in rows),
                input_tokens=sum(o['input_tokens'] for o in rows),
                ready_seconds=sum(o['ready_seconds'] for o in rows),
                median_ready_seconds=statistics.median(o['ready_seconds'] for o in rows),
                min_ready_seconds=min(o['ready_seconds'] for o in rows),
                max_ready_seconds=max(o['ready_seconds'] for o in rows),
                min_observed_headroom_bytes=min(o['backend']['observed_peak_free_lower_bytes'] for o in rows))


def audit():
    inputs = [ROOT/f'notebooks/run/{course}/{name}' for course in ['course-2','course-3']
              for name in ['latest.zip','multi-agents-course-v1nb.ipynb']]
    before = {p.relative_to(ROOT).as_posix(): file_identity(p) for p in inputs}
    runs, inventories = {}, {}
    with tempfile.TemporaryDirectory(prefix='i01-course3-review-') as name:
        temp = Path(name)
        for course in ['course-2','course-3']:
            run = temp/course
            integrity = extract_selected(ROOT/f'notebooks/run/{course}/latest.zip',run)
            result = analysis(run)
            assert canonical(result) == canonical(json.loads((run/'reports/analysis.json').read_text()))
            release = json.loads((run/'source/source-release.json').read_text())
            for rel, wanted in release['files'].items():
                p = run/'source'/rel
                assert file_identity(p) == wanted, rel
                if rel.startswith('recovery/') and rel.endswith('.py'):
                    assert p.read_bytes() == (ROOT/rel).read_bytes(), rel
            with zipfile.ZipFile(next((run/'source').glob('*.whl'))) as wheel:
                modules = [p for p in wheel.namelist() if p.startswith('recovery/') and p.endswith('.py')]
                assert all(wheel.read(p)==(run/'source'/p).read_bytes() for p in modules)
            assert manifests(result['manifest']['config'])['worlds'] == result['manifest']['worlds']
            with zipfile.ZipFile(ROOT/f'notebooks/run/{course}/latest.zip') as archive:
                members = archive.infolist()
                assert len(members) == len(integrity['files'])+1
            runs[course] = result
            inventories[course] = dict(source_head=release['git_head'],
                integrity_entries=len(integrity['files']), zip_members=len(members),
                zip_uncompressed_bytes=sum(m.file_size for m in members),
                verified_source_files=len(release['files']), verified_wheel_python_files=len(modules),
                boundary=integrity['boundary'], created_at=integrity['created_at'])
        old, current = runs['course-2'], runs['course-3']
        assert old['manifest']['study_id'] != current['manifest']['study_id']
        assert old['manifest']['worlds'] == current['manifest']['worlds']
        assert old['manifest']['config'] == current['manifest']['config']
        calls = {t['id']:(json.loads(t['request']), json.loads(t['outcome'])) for t in current['traces']}
        old_calls = {t['id']:(json.loads(t['request']), json.loads(t['outcome'])) for t in old['traces']}
        repeated = sorted(set(old_calls)&set(calls))
        assert len(repeated)==18
        assert all(canonical(old_calls[id][0])==canonical(calls[id][0]) for id in repeated)
        assert all(old_calls[id][1]['token_ids']==calls[id][1]['token_ids'] for id in repeated)
        worlds = {w['id']:w for w in current['manifest']['worlds']}
        attempt_order = {r['call_id']:r['admitted_at'] for r in current['attempts']}
        matched, direct_results = [], []
        for id in sorted(calls,key=lambda id:attempt_order[id]):
            request, outcome = calls[id]
            assert request['messages'] == messages(request['view'],control=True)
            assert outcome['input_tokens'] == len(request['input_ids']) == len(request['attention_mask'])
            assert all(v==1 for v in request['attention_mask'])
            assert outcome['generated_tokens'] == len(outcome['token_ids'])
            assert request['seed'] == outcome['backend']['seed'] == outcome['backend']['cpu_seed'] == outcome['backend']['cuda_seed']
            assert outcome['backend']['finite_score_steps']==outcome['generated_tokens']
            assert all(outcome['backend']['cache'][key] for key in ['initial_empty','same_call_cache','disposed_after_call'])
            if id.startswith('qualification-'):
                world = worlds[id.split('/')[0]]
                phase = 'revised' if 'revised' in id else 'original'
                assert request['view']['complete_input'] == [v for shard in world[phase] for v in shard]
                assert request['seed'] == world['control_seeds'][phase]
                if id.endswith('-direct'):
                    action, error = validate_action(outcome['visible_text'],truncated=outcome['truncated'],control=True)
                    assert not error and not outcome['framing_error'] and not outcome['failure']
                    direct_results.append(dict(call=id,truth=world[phase+'_truth'],submission=action['submit'],
                                               correct=int(action['submit']==world[phase+'_truth'])))
            if not id.endswith('-thinking'):
                continue
            direct_id = id.removesuffix('-thinking')+'-direct'
            dr, do = calls[direct_id]
            assert dr['view']==request['view'] and dr['seed']==request['seed']
            action, error = validate_action(outcome['visible_text'],truncated=outcome['truncated'],control=True)
            phase = 'revised' if 'revised' in id else 'original'
            truth = worlds[id.split('/')[0]][phase+'_truth']
            matched.append(dict(call=id,direct_call=direct_id,truth=truth,
                direct_submission=json.loads(do['visible_text'])['submit'],
                thinking_submission=action['submit'] if action else None,
                thinking_valid=not error and not outcome.get('framing_error') and not outcome.get('failure'),
                thinking_correct=int(bool(action) and not error and action['submit']==truth),
                validation_error=error,framing_error=outcome['framing_error'],
                termination=outcome['termination'],truncated=outcome['truncated'],
                direct_tokens=do['generated_tokens'],thinking_tokens=outcome['generated_tokens'],
                direct_seconds=do['ready_seconds'],thinking_seconds=outcome['ready_seconds'],
                latency_ratio=outcome['ready_seconds']/do['ready_seconds'],
                direct_input_tokens=do['input_tokens'],thinking_input_tokens=outcome['input_tokens'],
                thinking_close_delimiters=outcome['raw_text'].count('</think>'),
                private_reasoning_characters=len(outcome['thinking'] or ''),
                visible_characters=len(outcome['visible_text'])))
        assert len(matched)==5 and sum(r['thinking_valid'] for r in matched)==4
        assert sum(r['thinking_correct'] for r in matched)==4
        assert len(direct_results)==12 and sum(r['correct'] for r in direct_results)==10
        assert 'screen/thinking' not in current['summary']['gates']
        assert current['summary']['gates']['model_defect']['call']==matched[-1]['call']
        notebook=json.loads((ROOT/'notebooks/run/course-3/multi-agents-course-v1nb.ipynb').read_text(encoding='utf-8'))
        baseline=json.loads((temp/'course-3/source/notebooks/i01_course_kaggle.ipynb').read_text())
        edited=[c['id'] for c,b in zip(notebook['cells'],baseline['cells']) if ''.join(c['source'])!=''.join(b['source'])]
        assert edited==['session-window','thinking-screen']
        timing=[]
        for c in notebook['cells']:
            if c['cell_type']!='code' or c.get('execution_count') is None:continue
            e=c['metadata']['execution']
            start,stop=map(datetime.fromisoformat,[e['iopub.status.busy'],e['iopub.status.idle']])
            timing.append(dict(cell=c['id'],execution=c['execution_count'],start=start.isoformat(),stop=stop.isoformat(),
                wall_seconds=(stop-start).total_seconds(),
                errors=[o['evalue'] for o in c['outputs'] if o.get('output_type')=='error']))
        groups={key:summarize([o for id,(r,o) in calls.items() if predicate(id)]) for key,predicate in {
            'readiness':lambda id:id.startswith('hardware/'),
            'direct':lambda id:id.endswith('-direct'),
            'thinking':lambda id:id.endswith('-thinking')}.items()}
        receipt=dict(audit_only=True,files=before,archives=inventories,
            exact_read_only_reconstruction=True,shipped_python_modules_match_checkout=True,
            course_2_study=old['manifest']['study_id'],course_3_study=current['manifest']['study_id'],
            same_worlds_and_config=True,repeated_physical_call_ids=repeated,
            repeated_requests_exact=True,repeated_output_tokens_exact=True,
            course_2_attempts=old['summary']['attempts'],course_3_attempts=current['summary']['attempts'],
            distinct_physical_attempts_across_runs=old['summary']['attempts']+current['summary']['attempts'],
            groups=groups,direct_control_results=direct_results,matched_controls=matched,
            matched_latency_ratio=sum(r['thinking_seconds'] for r in matched)/sum(r['direct_seconds'] for r in matched),
            matched_generated_token_ratio=sum(r['thinking_tokens'] for r in matched)/sum(r['direct_tokens'] for r in matched),
            valid_final_latency_ratio=sum(r['thinking_seconds'] for r in matched if r['thinking_valid'])/sum(r['direct_seconds'] for r in matched if r['thinking_valid']),
            thinking_planned=12,thinking_recorded=5,thinking_correct_final=4,thinking_invalid=1,thinking_unexecuted=7,
            thinking_aggregate_receipt_present=False,
            truncated_control_in_failure_analysis=any(r['episode']==matched[-1]['call'] for r in current['failure_analysis']),
            summary={k:v for k,v in current['summary'].items() if k!='gates'},
            changed_notebook_cells=edited,executed_cells=timing,
            new_real_model_attempts=0,gpu_inference_executed=False)
    assert before=={p.relative_to(ROOT).as_posix():file_identity(p) for p in inputs}
    output=ROOT/'docs/validation/course-3-audit.json'
    output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:receipt[k] for k in ['course_3_attempts','distinct_physical_attempts_across_runs','groups',
        'matched_latency_ratio','matched_generated_token_ratio','thinking_correct_final','thinking_invalid','thinking_unexecuted',
        'truncated_control_in_failure_analysis','new_real_model_attempts']},indent=2))


if __name__=='__main__':audit()
