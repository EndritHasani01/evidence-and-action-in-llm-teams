"""Read-only course-7 audit; no model imports, calls, or modification of inputs.

Run from the repository root: python scripts/audit_i01_course7.py
Outputs are derived evidence, never replacements for the two canonical stores.
"""
import argparse
from collections import Counter
import csv
from datetime import datetime
import json
from pathlib import Path
import random
import statistics
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from recovery.i01.archive import extract_selected, verify, digest
from recovery.i01.core import (apply_outcome, initial_episode, manifests, messages,
                               next_agent, permitted_view)
from recovery.i01.policy import outcome_action, validation_detail
from recovery.i01.report import analysis, read_run
from recovery.i01.workflow import source_files


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows({k: json.dumps(v) if isinstance(v, (list, dict)) else v
                         for k, v in row.items()} for row in rows)


def interval(rows, key, config):
    strata = {}
    for row in rows:
        strata.setdefault((row['owner'], row['first']), []).append(row[key])
    rng = random.Random(config['bootstrap_seed'])
    values = sorted(sum(rng.choice(v) for v in strata.values() for _ in v) / len(rows)
                    for _ in range(config['bootstrap_draws']))
    return [values[int(len(values) * .025)], values[int(len(values) * .975)]]


def audit(run, notebook):
    integrity = verify(run)
    manifest, tables, meta = read_run(run)
    assert source_files(ROOT) == manifest['source_identity'], 'Scientific source drift'
    assert source_files(run / 'source') == manifest['source_identity']
    release = json.loads((run / 'source/source-release.json').read_text())
    for name, expected in release['files'].items():
        path = run / 'source' / name
        assert path.stat().st_size == expected['bytes'] and digest(path) == expected['sha256']
    wheel_members = 0
    with zipfile.ZipFile(next((run / 'source').glob('*.whl'))) as wheel:
        for name in wheel.namelist():
            if name.startswith('recovery/') and name.endswith('.py'):
                assert wheel.read(name) == (run / 'source' / name).read_bytes()
                wheel_members += 1
    assert manifests(manifest['config'])['worlds'] == manifest['worlds']
    result = analysis(run)
    assert result == json.loads((run / 'reports/analysis.json').read_text())
    episodes = {row['id']: json.loads(row['state']) for row in tables['episodes']}
    calls = {row['id']: row for row in tables['calls']}
    attempts = {row['call_id']: row for row in tables['attempts']}
    assert len(calls) == len(attempts) == 252
    assert all(row['status'] == 'completed' and row['number'] == 1 for row in attempts.values())
    assert all(row['evidence'] == calls[cid]['outcome'] for cid, row in attempts.items())
    call_rows, world_rows = [], []
    replayed = controls = 0
    for world in manifest['worlds']:
        wid = world['id']
        original = [v for shard in world['original'] for v in shard]
        revised = [v for shard in world['revised'] for v in shard]
        assert all(len(shard) == 20 for shard in world['original'] + world['revised'])
        assert all(type(v) is int and -1000 <= v <= 1000 for v in original + revised)
        assert world['original_truth'] == max(original) and original.count(max(original)) == 1
        assert world['revised_truth'] == max(revised) < max(original)
        assert world['after'] < world['revised_truth']
        assert [(i,j) for i in range(2) for j in range(20) if world['original'][i][j] != world['revised'][i][j]] == [(world['owner'],world['row'])]
        if world['group'] != 'qualification':
            for phase in ['prefix'] + world['treatments']:
                final = episodes[wid + '/' + phase]
                state = initial_episode(world, phase, episodes[wid + '/prefix'] if phase != 'prefix' else None)
                for event in final['events']:
                    agent = next_agent(state)
                    invocation = state['turns'][agent]
                    cid = f'{wid}/{phase}/agent-{agent}/invocation-{invocation}'
                    assert event['call'] == cid and event['agent'] == agent
                    call = calls[cid]
                    request, outcome = json.loads(call['request']), json.loads(call['outcome'])
                    view = permitted_view(world, state, agent)
                    assert request['view'] == view and request['messages'] == messages(view)
                    assert request['seed'] == world['seeds']['prefix' if phase == 'prefix' else 'recovery'][agent][invocation]
                    assert call['slot'] == world['device'] and call['effect_committed'] == 1
                    assert request['settings'] == meta['freeze']['settings']
                    assert len(request['input_ids']) == outcome['input_tokens']
                    assert len(outcome['token_ids']) == outcome['generated_tokens']
                    action, error = outcome_action(outcome)
                    assert action == event['action'] and error == event['error']
                    state = apply_outcome(state, agent, action, error, cid)
                    call_rows.append(dict(call=cid, group=world['group'], phase=phase,
                        agent=agent, invocation=invocation, slot=call['slot'],
                        seed=request['seed'], **validation_detail(outcome),
                        raw_action=outcome['visible_text'], ready_seconds=outcome['ready_seconds'],
                        input_tokens=outcome['input_tokens'], generated_tokens=outcome['generated_tokens']))
                    replayed += 1
                assert state == final, 'Literal saved state does not replay: ' + wid + '/' + phase
        for phase in ['original', 'revised']:
            cid = f'{wid}/control-{phase}-direct'
            if cid not in calls:
                assert world['group'] == 'main' and phase == 'original'
                continue
            call = calls[cid]
            request, outcome = json.loads(call['request']), json.loads(call['outcome'])
            view = dict(complete_input=[v for shard in world[phase] for v in shard])
            assert request['view'] == view and request['messages'] == messages(view, control=True)
            assert request['seed'] == world['control_seeds'][phase]
            assert call['slot'] == world['device'] and call['effect_committed'] == 1
            assert request['settings'] == meta['freeze']['settings']
            action, error = outcome_action(outcome, control=True)
            expected = dict(terminal='control_completed', submissions=[action['submit']] if action else [],
                correct=int(not error and action['submit'] == world[phase + '_truth']), error=error)
            assert episodes[cid] == expected
            controls += 1
        if world['group'] == 'main':
            row = {k: world[k] for k in ['id', 'owner', 'first', 'device', 'before', 'after', 'original_truth', 'revised_truth']}
            row['treatment_order'] = world['treatments']
            row['local_maxima_revised'] = [max(shard) for shard in world['revised']]
            for phase in ['prefix', 'retain', 'clear']:
                state = episodes[wid + '/' + phase]
                truth = world['original_truth' if phase == 'prefix' else 'revised_truth']
                rows = [r for r in call_rows if r['call'].startswith(wid + '/' + phase + '/')]
                row.update({phase + '_submissions': state['submissions'], phase + '_terminal': state['terminal'],
                    phase + '_success': int(state['submissions'] == [truth, truth]),
                    phase + '_correct_agents': sum(v == truth for v in state['submissions']),
                    phase + '_illegal_actions': sum(not r['legal_action'] for r in rows),
                    phase + '_old_winner_submissions': sum(v == world['before'] for v in state['submissions']),
                    phase + '_local_max_submissions': sum(v == max(world['original' if phase == 'prefix' else 'revised'][i])
                                                         for i, v in enumerate(state['submissions']))})
            row['control_revised_submit'] = episodes[wid + '/control-revised-direct']['submissions'][0]
            row['control_revised_correct'] = episodes[wid + '/control-revised-direct']['correct']
            row['clear_minus_retain'] = row['clear_success'] - row['retain_success']
            row['winner_changes_agent'] = max(world['revised'][1-world['owner']]) == world['revised_truth']
            for phase in ['retain', 'clear']:
                state = episodes[wid + '/' + phase]
                first_action = state['events'][0]['action']
                row[phase + '_first_call_submits'] = bool(first_action and first_action['submit'] is not None)
                row[phase + '_below_own_max'] = sum(v is not None and v < max(world['revised'][i]) for i,v in enumerate(state['submissions']))
                row[phase + '_replacement_submissions'] = sum(v == world['after'] for v in state['submissions'])
                row[phase + '_wrong_consensus'] = state['submissions'][0] is not None and state['submissions'][0] == state['submissions'][1] != world['revised_truth']
            world_rows.append(row)
    assert replayed == 206 and controls == 38
    assert all(r['json_valid'] and r['schema_valid'] for r in result['validation_details'])
    pairs = Counter(('both' if r['retain_success'] and r['clear_success'] else 'retain_only' if r['retain_success']
                     else 'clear_only' if r['clear_success'] else 'neither') for r in world_rows)
    assert dict(pairs) == result['summary']['paired_counts']
    assert interval(world_rows, 'clear_minus_retain', manifest['config']) == [result['summary']['interval'][k] for k in ['low', 'high']]
    assert interval(result['paired_costs'], 'clear_minus_retain_ready_seconds', manifest['config']) == [result['summary']['principal_effort_interval'][k] for k in ['low', 'high']]
    costs = []
    for phase in ['prefix', 'retain', 'clear']:
        rows = [r for r in result['costs'] if r['world'].startswith('main-') and r['phase'] == phase]
        cost = dict(phase=phase)
        for key in ['calls', 'input_tokens', 'generated_tokens', 'ready_seconds', 'messages']:
            cost[key + '_total'] = sum(r[key] for r in rows)
            cost[key + '_mean'] = statistics.mean(r[key] for r in rows)
            cost[key + '_median'] = statistics.median(r[key] for r in rows)
        costs.append(cost)
    sessions = [json.loads(row['evidence']) for row in tables['sessions']]
    notebook_json = json.loads(notebook.read_text(encoding='utf-8'))
    code = [c for c in notebook_json['cells'] if c['cell_type'] == 'code']
    assert [c['execution_count'] for c in code] == list(range(1, 34))
    assert not any(o.get('output_type') == 'error' for c in code for o in c.get('outputs', []))
    cell_timing = []
    for cell in code:
        timing = cell['metadata']['execution']
        start, end = [datetime.fromisoformat(timing[key].replace('Z', '+00:00'))
                      for key in ['iopub.status.busy', 'iopub.status.idle']]
        cell_timing.append(dict(cell=cell['execution_count'], stage=''.join(cell['source']).splitlines()[0],
                                start=start.isoformat(), end=end.isoformat(), seconds=(end-start).total_seconds()))
    outcomes = [json.loads(row['outcome']) for row in calls.values()]
    scientific = [json.loads(c['outcome']) for c in calls.values() if not c['id'].startswith('hardware/')]
    assert all(o['failure'] is None and not o['framing_error'] for o in outcomes)
    assert not any(o['truncated'] for o in scientific)
    assert all(o['backend']['cache']['initial_empty'] and o['backend']['cache']['disposed_after_call'] for o in outcomes)
    load_pids = {s['slot']:s['load']['pid'] for s in sessions}
    for call in calls.values():
        request, outcome = json.loads(call['request']), json.loads(call['outcome'])
        assert all(outcome['backend'][key] == request['seed'] for key in ['seed','cpu_seed','cuda_seed'])
        assert outcome['backend']['pid'] == load_pids[call['slot']]
        assert outcome['backend']['finite_score_steps'] > 0
    elapsed = (datetime.fromisoformat(integrity['created_at']) - datetime.fromisoformat(manifest['created_at'])).total_seconds()
    return dict(study_id=manifest['study_id'], source_sha256=manifest['source_identity'],
        source_release_commit=release['git_head'], archive=integrity | {'files': len(integrity['files'])},
        checks=dict(source_identity_members=len(manifest['source_identity']), release_members=len(release['files']),
            wheel_python_members=wheel_members, regenerated_worlds=29, team_calls_replayed=replayed,
            controls_replayed=controls, committed_scientific_calls=244, saved_analysis_equal=True,
            primary_and_effort_bootstrap_equal=True, executed_code_cells=len(code), notebook_errors=0,
            provider_failures=0, framing_failures=0, scientific_truncated=0,
            deliberate_envelope_length_terminations=sum(o['truncated'] for o in outcomes),
            retries=0, annotations=len(tables['annotations'])),
        summary={k:v for k,v in result['summary'].items() if k not in ['gates']},
        main_worlds=world_rows, main_costs=costs, protocol_compliance=result['protocol_compliance'],
        reasons=dict(Counter(r['reason'] for r in result['validation_details'] if not r['legal_action'])),
        stages=dict(Counter(r['stage'] for r in attempts.values())),
        physical_calls_by_slot=dict(Counter(r['slot'] for r in calls.values())),
        episode_terminals_by_group_phase={g+'/'+p:dict(Counter(episodes[w['id']+'/'+p]['terminal'] for w in manifest['worlds'] if w['group']==g))
                                       for g in ['pilot','main'] for p in ['prefix','retain','clear']},
        all_slots_close=[dict(slot=s['slot'],process_close=s.get('process_close')) for s in sessions],
        timing=dict(study_created_at=manifest['created_at'], final_checkpoint_at=integrity['created_at'],
                    study_to_final_checkpoint_seconds=elapsed,
                    notebook_elapsed_seconds=(datetime.fromisoformat(cell_timing[-1]['end'])-datetime.fromisoformat(cell_timing[0]['start'])).total_seconds(),
                    cells=cell_timing),
        hardware=dict(min_observed_free_bytes=min(o['backend']['observed_free_min_bytes'] for o in outcomes),
            min_peak_free_lower_bytes=min(o['backend']['observed_peak_free_lower_bytes'] for o in outcomes),
            max_peak_reserved_bytes=max(o['backend']['peak_reserved_bytes'] for o in outcomes),
            max_scientific_input_tokens=max(o['input_tokens'] for o in scientific),
            max_generated_tokens=max(o['generated_tokens'] for o in outcomes),
            worker_loads=[{k:s['load'].get(k) for k in ['pid','cuda_visible_devices','cuda_device_uuid','load_seconds','packages','recurrent_fast_path']} for s in sessions])), call_rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=ROOT/'notebooks/run/course-7-working/latest.zip')
    parser.add_argument('--notebook', type=Path, default=ROOT/'notebooks/run/course-7-working/multi-agents-course-v5nb.ipynb')
    parser.add_argument('--output', type=Path, default=ROOT/'notebooks/validation/i01-course7-analysis')
    args = parser.parse_args()
    # Prevent derived output from overwriting supplied evidence, including extracted directories.
    out = args.output.resolve()
    assert not out.is_relative_to(args.archive.resolve().parent), 'Output must be outside the original evidence folder'
    hashes = {str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p): digest(p) for p in [args.archive, args.notebook]}
    with tempfile.TemporaryDirectory(prefix='i01-course7-readonly-') as name:
        run = Path(name)/'run'
        extract_selected(args.archive, run)
        result, calls = audit(run, args.notebook)
        result['input_sha256'] = hashes
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output/'audit.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
        write_csv(args.output/'main-worlds.csv', result['main_worlds'])
        write_csv(args.output/'team-call-audit.csv', calls)
        write_csv(args.output/'main-costs.csv', result['main_costs'])
        # Preserve selected original figures byte for byte; no new experiment or plotting dependency.
        figure_dir = args.output/'figures'
        figure_dir.mkdir(exist_ok=True)
        for stem in ['paired-outcomes', 'recovery-ready_seconds', 'termination-coverage']:
            for suffix in ['png','svg']:
                name = stem + '.' + suffix
                (figure_dir/name).write_bytes((run/'reports/figures'/name).read_bytes())
    assert hashes == {str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p): digest(p) for p in [args.archive, args.notebook]}
    print(json.dumps(dict(output=str(args.output),checks=result['checks'],paired_counts=result['summary']['paired_counts']), indent=2))


if __name__ == '__main__':
    main()
