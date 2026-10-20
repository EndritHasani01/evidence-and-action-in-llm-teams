"""Qualification derived from canonical outcomes, with historical gates retained."""
import json

from .core import validate_action, rejection_feedback, success
from . import assisted

PROTOCOL_POLICY = "i01-direct-protocol-2026-10-15"
AUTOMATIC_POLICY = "i01-whole-study-run-all-2026-10-15"
RECOVERY_POLICY = "i01-recovery-admission-run-all-2026-10-15"
OUTCOME_POLICY = "i01-recorded-outcomes-run-all-2026-10-15"
ASSISTED_POLICY = "i01-assisted-feasibility-2026-10-16"
AUTOMATIC_POLICIES = (AUTOMATIC_POLICY, RECOVERY_POLICY, OUTCOME_POLICY, ASSISTED_POLICY)
FAILURE_CLEANUP_POLICIES = (RECOVERY_POLICY, OUTCOME_POLICY, ASSISTED_POLICY)
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


def validation_detail(outcome, *, control=False):
    """Read-only explanation; the strict core validator alone decides effects."""
    action,error=outcome_action(outcome,control=control)
    duplicate=[]
    def pairs(items):
        value={}
        for key,item in items:
            if key in value: duplicate.append(key)
            value[key]=item
        return value
    syntax,schema,reason=False,False,None
    try:
        value=json.loads(outcome.get('visible_text',''),object_pairs_hook=pairs)
        syntax=True
        if duplicate:reason='duplicate_json_keys'
        elif type(value) is not dict or set(value)!={'message','submit','wait'}:reason='required_action_keys'
        elif (value['message'] is not None and (type(value['message']) is not str or not value['message'].strip()) or
              value['submit'] is not None and type(value['submit']) is not int or type(value['wait']) is not bool):
            reason='action_field_types'
        else:
            schema=True
            if value['wait'] and (value['message'] is not None or value['submit'] is not None):reason='wait_requires_null_message_and_submit'
            elif not value['wait'] and value['message'] is None and value['submit'] is None:reason='empty_nonwaiting_action'
            elif control and (value['message'] is not None or value['submit'] is None or value['wait']):reason='control_requires_integer_submission_only'
    except (ValueError,TypeError,RecursionError):reason='invalid_json'
    if outcome.get('failure'):reason='provider_'+str(outcome['failure'])
    elif outcome.get('truncated'):reason='truncated_action'
    elif outcome.get('framing_error'):reason='output_framing_error'
    return dict(json_valid=syntax,schema_valid=schema,legal_action=action is not None and error is None,
                error=error,reason=reason)


def outcome_feedback(outcome):
    if outcome.get("failure"):
        return rejection_feedback("provider_failure")
    if outcome.get("truncated"):
        return rejection_feedback("truncated_action")
    return rejection_feedback(validation_detail(outcome)["reason"])


def runtime_safe(outcome, termination=None):
    """Ordinary output errors are outcomes; unknown death/backend faults block."""
    termination=termination or {}
    if outcome.get('termination_pending') and not termination.get('termination_confirmed'):
        return False
    failure=outcome.get('failure')
    return not failure or failure=='timeout' and bool(termination.get('termination_confirmed') or outcome.get('termination_confirmed'))


def admission_blocks(policy, group, phase, detail, *, safe=True):
    if not safe:return True
    if group=='qualification':return False if policy==ASSISTED_POLICY and phase.startswith('diagnostic-') else not detail['legal_action']
    if group=='pilot':
        if policy in (OUTCOME_POLICY,ASSISTED_POLICY):return False
        return not detail['legal_action'] and (policy!=RECOVERY_POLICY or phase not in ('retain','clear'))
    return False


def qualification(manifest, tables, metadata):
    calls = {r['id']: r for r in tables['calls']}
    states = {r['id']: json.loads(r['state']) for r in tables['episodes']}
    policy = metadata.get('qualification_policy', LEGACY_POLICY)
    result = {}
    selected_assisted = assisted(manifest['config'])
    planned = 8 if selected_assisted else 12
    for mode in (('direct',) if selected_assisted else ('direct', 'thinking')):
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
        protocol_passed = complete==planned and all(r['valid'] is True for r in rows)
        passed = (mode=='direct' and protocol_passed if policy==PROTOCOL_POLICY
                  else protocol_passed and correct>=11)
        result[mode] = dict(mode=mode, policy=policy, planned=planned,
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


def pilot_usefulness(manifest, tables):
    """Reconstruct the one assisted scientific gate from committed pilot records."""
    if not assisted(manifest['config']):
        raise ValueError('Assisted pilot usefulness is a separately scoped decision')
    states = {r['id']:json.loads(r['state']) for r in tables['episodes']}
    calls = {r['id']:r for r in tables['calls']}
    pilots = []
    for world in manifest['worlds']:
        if world['group'] != 'pilot':continue
        scopes = [world['id']+'/'+p for p in ('prefix','retain','clear')]
        controls = [world['id']+'/control-'+p+'-direct' for p in ('original','revised')]
        required = scopes+controls
        rows = [r for r in tables['calls'] if r['episode'] in required]
        complete = (all(states.get(key,{}).get('terminal') for key in required) and
                    all(any(r['episode']==key for r in rows) for key in required) and
                    all(r['outcome'] and r['effect_committed'] for r in rows))
        scores = []
        for phase,key in zip(('original','revised'),controls):
            row = calls.get(key)
            if not row or not row['outcome'] or not row['effect_committed'] or not states.get(key,{}).get('terminal'):
                scores.append(None)
            else:
                action,error = outcome_action(json.loads(row['outcome']),control=True)
                scores.append(int(not error and action['submit']==world[phase+'_truth']))
        pilots.append(dict(world=world['id'],complete=bool(complete),
                           original=success(states.get(scopes[0]),world['original_truth']),controls=scores))
    originals=sum(p['original']==1 for p in pilots)
    controls=sum(c==1 for p in pilots for c in p['controls'])
    checks=dict(complete_pilot_evidence=len(pilots)==4 and all(p['complete'] for p in pilots),
                original_team_usefulness=originals>=3,scalar_usefulness=controls>=7)
    return dict(policy=ASSISTED_POLICY,passed=all(checks.values()),checks=checks,
                correct_originals=originals,intended_originals=4,correct_controls=controls,
                intended_controls=8,pilots=pilots,
                rationale='Fixed course-usefulness decision, not population reliability certification; recovery outcomes do not select admission.')
