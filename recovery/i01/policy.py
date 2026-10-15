"""Qualification derived from canonical outcomes, with historical gates retained."""
import json

from .core import validate_action

PROTOCOL_POLICY = "i01-direct-protocol-2026-10-15"
LEGACY_POLICY = "i01-competence-11-of-12"
COURSE_2_STUDY = 'c2973855-84fa-411d-9f6c-a08f8acc79d6'
COURSE_3_STUDY = 'de1b347e-2cb7-41e5-a8b9-2789abda2da3'
CAMPAIGN_STUDIES = (COURSE_2_STUDY, COURSE_3_STUDY)


def outcome_action(outcome, *, control=False):
    action,error=validate_action(outcome.get('visible_text',''),truncated=outcome.get('truncated',False),control=control)
    if outcome.get('failure'):
        return None,'provider_failure'
    if outcome.get('framing_error'):
        return None,error or 'malformed_action'
    return action,error


def qualification(manifest, tables, metadata):
    calls = {r['id']: r for r in tables['calls']}
    states = {r['id']: json.loads(r['state']) for r in tables['episodes']}
    policy = metadata.get('qualification_policy', LEGACY_POLICY)
    result = {}
    for mode in ('direct', 'thinking'):
        rows = []
        for world in manifest['worlds']:
            if world['group'] != 'qualification':
                continue
            for phase in ('original', 'revised'):
                identity = f"{world['id']}/control-{phase}-{mode}"
                call = calls.get(identity)
                outcome = json.loads(call['outcome']) if call and call['outcome'] else None
                attempts = [a for a in tables['attempts'] if a['call_id'] == identity]
                committed = bool(call and call['effect_committed'] and states.get(identity, {}).get('terminal'))
                action, error = (None, None) if outcome is None else outcome_action(outcome,control=True)
                valid = None if outcome is None else bool(action and not error)
                truth = world[phase+'_truth']
                rows.append(dict(call=identity, world=world['id'], phase=phase, mode=mode,
                    slot=world['device'], truth=truth, submission=action['submit'] if action else None,
                    attempts=len(attempts), unresolved=sum(a['status']=='admitted' for a in attempts),
                    recorded=outcome is not None, committed=committed, valid=valid,
                    correct=int(bool(valid) and action['submit']==truth) if committed else None,
                    error=error, framing_error=(outcome or {}).get('framing_error'),provider_failure=(outcome or {}).get('failure'),
                    termination=(outcome or {}).get('termination'),
                    generated_tokens=(outcome or {}).get('generated_tokens'),
                    ready_seconds=(outcome or {}).get('ready_seconds')))
        complete = sum(r['committed'] for r in rows)
        errors = sum(r['valid'] is False for r in rows)
        correct = sum(r['correct']==1 for r in rows)
        protocol_passed = complete==12 and all(r['valid'] is True for r in rows)
        passed = (mode=='direct' and protocol_passed if policy==PROTOCOL_POLICY
                  else protocol_passed and correct>=11)
        result[mode] = dict(mode=mode, policy=policy, planned=12,
            admitted=sum(bool(r['attempts']) for r in rows),
            unresolved=sum(r['unresolved'] for r in rows),
            recorded=sum(r['recorded'] for r in rows), committed=complete,
            valid=sum(r['valid'] is True for r in rows), correct=correct,
            wrong_scalar=sum(r['valid'] is True and r['correct']==0 for r in rows),
            protocol_errors=errors, unexecuted=sum(not r['attempts'] for r in rows),
            protocol_passed=protocol_passed, passed=passed,
            historical_gate=metadata.get('screen/'+mode), controls=rows)
        mode_attempts = [a for a in tables['attempts'] if a['call_id'] in {r['call'] for r in rows}]
        evidence = [json.loads(a['evidence']) if a.get('evidence') else {} for a in mode_attempts]
        result[mode].update(physical_attempts=len(mode_attempts),
            generated_tokens_observed=sum(o.get('generated_tokens') or 0 for o in evidence),
            ready_seconds_observed=sum(o.get('ready_seconds') or 0 for o in evidence),
            attempts_unknown_effort=sum(o.get('ready_seconds') is None for o in evidence))
    return result
