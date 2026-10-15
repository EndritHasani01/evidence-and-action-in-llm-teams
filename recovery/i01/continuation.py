"""Explicit pre-main continuation of the reviewed 8f5bcdb I-01 checkpoints.

Original manifest, source, calls and gates remain intact. A fresh destination
publishes only after validation; ordinary reopen never invents this transition.
"""
from contextlib import closing
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

from .archive import digest, extract_selected, verify
from .core import canonical, manifests
from .policy import PROTOCOL_POLICY
from .store import Store, connection, restore_tail, utc

LEGACY_SOURCE_SHA256 = '1aa0866281d866941ae49bda5436a50e2001d66689c2d39026209bfc142002e2'
COURSE_3_STUDY = 'de1b347e-2cb7-41e5-a8b9-2789abda2da3'
COURSE_2_STUDY = 'c2973855-84fa-411d-9f6c-a08f8acc79d6'
CHANGED_MODULES = {'recovery/i01/'+name+'.py' for name in
                   ('workflow','store','report','ui','notebook','cli','policy','continuation')}


def metadata(run):
    with closing(connection(Path(run)/'worker-0.sqlite', True)) as db:
        return {r['key']:json.loads(r['value']) for r in db.execute('SELECT * FROM meta')}


def active_source(run):
    transition = metadata(run).get('implementation_transition')
    if transition and transition.get('source_path') != 'source/continuation':
        raise ValueError('Unsupported implementation transition path')
    return Path(run)/(transition['source_path'] if transition else 'source')


def validate_active_source(run, source, manifest):
    from .workflow import source_files
    for slot in range(2):
        Store.validate(Path(run)/f'worker-{slot}.sqlite', {'manifest':manifest})
    transition = metadata(run).get('implementation_transition')
    wanted = manifest['source_identity']
    if transition:
        if (transition.get('from_identity') != wanted or transition.get('policy') != PROTOCOL_POLICY or
            source_files(Path(run)/'source') != wanted):
            raise ValueError('Original source/transition binding differs')
        wanted = transition['to_identity']
        if source_files(active_source(run)) != wanted:
            raise ValueError('Preserved active continuation source differs')
    if source_files(source) != wanted:
        raise ValueError('source differs; use the exact packet or explicit reviewed pre-main continuation; reporting remains read-only')


def choose_checkpoint(study_id, root='/kaggle/input'):
    """Select by the declared study ID, never by filename or latest timestamp."""
    root = Path(root)
    candidates = []
    for path in root.rglob('*.zip'):
        try:
            with zipfile.ZipFile(path) as archive:
                if 'run.json' in archive.namelist() and json.loads(archive.read('run.json'))['study_id']==study_id:
                    candidates.append(path)
        except (OSError, ValueError, KeyError, zipfile.BadZipFile):
            continue
    for path in root.rglob('integrity.json'):
        manifest=path.parent/'run.json'
        if manifest.is_file() and json.loads(manifest.read_text())['study_id']==study_id:
            candidates.append(path.parent)
    if len(candidates)!=1:
        raise ValueError(f'Set the exact checkpoint for study {study_id}; found {len(candidates)} candidates. Attach its downloaded ZIP or expanded root; no timestamp selection.')
    return candidates[0]


def _pre_main(result):
    if result['summary']['gates'].get('freeze') or any(
        not (t['id'].startswith('qualification-') or t['id'].startswith('hardware/')) for t in result['traces']):
        raise ValueError('Only pre-main preparation can use this continuation/prior-preparation path')
    if any(a['stage'] not in ('hardware','direct','thinking') for a in result['attempts']):
        raise ValueError('Prior preparation contains a non-preparation attempt stage')
    if result['summary']['in_flight']:
        raise ValueError('Resolve old admitted attempts before compatible continuation')


def _keep_zip(selected, extracted, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if Path(selected).is_file():
        shutil.copy2(selected, target)
    else:
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(Path(extracted).rglob('*')):
                if path.is_file():
                    archive.write(path, path.relative_to(extracted).as_posix())


def record_prior_preparation(run, stores, checkpoints):
    """Known repeated preparation uses reserve, never becomes a retry/loss."""
    from .report import analysis
    run=Path(run)
    if not checkpoints and stores[0].meta('prior_spending_pending'):
        raise ValueError('A failed prior-spending import cannot be cancelled by an empty checkpoint list')
    if checkpoints:
        stores[0].put_meta('prior_spending_pending',dict(checkpoints=[str(p) for p in checkpoints],at=utc()))
    own=json.loads((run/'run.json').read_text())['study_id']
    existing={r['study_id']:r for r in stores[0].meta('prior_spending',[])}
    for selected in checkpoints:
        with tempfile.TemporaryDirectory(prefix='i01-prior-') as name:
            old=Path(name)/'checkpoint'
            extract_selected(selected,old)
            result=analysis(old); _pre_main(result)
            identity=result['manifest']['study_id']
            if identity==own:
                raise ValueError('Prior spending overlaps the current study; do not charge its own calls twice')
            if result['manifest']['config']!=json.loads((run/'run.json').read_text())['config']:
                raise ValueError('Prior preparation belongs to another scientific regime')
            components=list(result['summary'].get('prior_spending',[]))
            relative=f'receipts/prior-studies/{identity}.zip'
            component=dict(study_id=identity, attempts=result['summary']['attempts'],
                contingency_charge=result['summary']['attempts'],
                stages={stage:sum(a['stage']==stage for a in result['attempts']) for stage in ('hardware','direct','thinking')},
                ready_seconds_observed=result['summary']['physical_ready_seconds_observed'],
                generated_tokens_observed=result['summary']['generated_tokens_observed'],
                inventory_sha256=digest(old/'integrity.json'), evidence_path=relative,
                basis='Known repeated I-01 preparation charged to the shared reserve under the 15 October amendment; not a retry or historical-45 spending')
            components.append(component)
            pending={}
            for item in components:
                sid=item['study_id']
                if sid==own:
                    raise ValueError('Nested prior spending overlaps the current study')
                if item['evidence_path']!=f'receipts/prior-studies/{sid}.zip':
                    raise ValueError('Unexpected prior-checkpoint evidence path')
                if sid in existing:
                    if existing[sid]!=item:
                        raise ValueError('Conflicting checkpoints for one prior study; choose one exact boundary')
                    continue  # Identical evidence cannot double-charge.
                if sid in pending:
                    raise ValueError('Duplicated prior-study component')
                pending[sid]=item
            for sid,item in pending.items():
                target=run/item['evidence_path']
                if sid==identity:
                    _keep_zip(selected,old,target)
                else:
                    source=old/item['evidence_path']
                    with tempfile.TemporaryDirectory(prefix='i01-prior-proof-') as proof_name:
                        proof=Path(proof_name)/'proof'; extract_selected(source,proof)
                        proof_result=analysis(proof);_pre_main(proof_result)
                        if (digest(proof/'integrity.json')!=item['inventory_sha256'] or
                            proof_result['manifest']['study_id']!=sid or proof_result['summary']['attempts']!=item['attempts']):
                            raise ValueError('Nested prior-study evidence differs')
                    target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
            existing.update(pending)
    value=[existing[k] for k in sorted(existing)]
    stores[0].put_meta('prior_spending',value)
    stores[0].put_meta('prior_spending_pending',None)
    return value


def _adjudicate_length_flag(stores):
    flag=stores[0].meta('model_defect')
    if not flag:
        return None
    rows=[s.call(flag['call']) for s in stores]
    rows=[r for r in rows if r]
    if len(rows)!=1 or not rows[0]['outcome']:
        raise ValueError('Cannot adjudicate missing/ambiguous runtime defect evidence')
    row=rows[0]; outcome=json.loads(row['outcome']); request=json.loads(row['request'])
    backend=outcome.get('backend',{})
    if (request['settings']['mode']!='thinking' or outcome!=flag['outcome'] or
        outcome.get('failure') or not outcome.get('truncated') or outcome.get('termination')!='length' or
        outcome.get('generated_tokens')!=4096 or len(outcome.get('token_ids',[]))!=4096 or
        outcome.get('framing_error')!='thinking_framing_defect' or outcome.get('visible_text') or
        '</think>' in outcome.get('raw_text','') or backend.get('finite_score_steps')!=4096 or
        not all(backend.get('cache',{}).get(k) for k in ('initial_empty','same_call_cache','disposed_after_call'))):
        raise ValueError('A real or unrecognized runtime defect cannot be cleared by this transition')
    receipt=dict(call=row['id'], at=utc(), original_flag=flag,
        decision='Normal token-limit noncompletion; keep invalid action, raw output and spending; remove only erroneous global runtime classification')
    stores[0].bind('model_defect_adjudication',receipt)
    stores[0].put_meta('model_defect',None)
    return receipt


def continue_checkpoint(selected, target, source, *, prior_checkpoints=(), tail='latest', evidence=''):
    from .workflow import capture_source, source_files
    from .report import analysis
    target, source=Path(target),Path(source)
    if target.exists() and any(target.iterdir()):
        raise ValueError('Compatible continuation requires a fresh writable destination')
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='i01-continue-',dir=target.parent) as name:
        staging=Path(name)/'study'
        receipt=extract_selected(selected,staging)
        before=analysis(staging); manifest=before['manifest']; _pre_main(before)
        old=manifest['source_identity']; current=source_files(source)
        if hashlib.sha256(canonical(old).encode()).hexdigest()!=LEGACY_SOURCE_SHA256:
            raise ValueError('Only the reviewed 8f5bcdb source can use this explicit transition')
        if source_files(staging/'source')!=old:
            raise ValueError('Original source bytes differ')
        release=json.loads((staging/'source/source-release.json').read_text())
        for rel,wanted in release['files'].items():
            if Path(rel).is_absolute() or '..' in Path(rel).parts:
                raise ValueError('Unsafe original source-release member')
            path=staging/'source'/rel
            if path.stat().st_size!=wanted['bytes'] or digest(path)!=wanted['sha256']:
                raise ValueError('Original source release differs: '+rel)
        differences={key for key in old.keys()|current.keys() if old.get(key)!=current.get(key)}
        if not differences<=CHANGED_MODULES:
            raise ValueError('Unreviewed scientific/runtime source difference: '+str(sorted(differences-CHANGED_MODULES)))
        if (manifest['config']!=json.loads((source/'configs/i01-course.json').read_text()) or
            manifest['worlds']!=manifests(manifest['config'])['worlds'] or before['summary']['gates'].get('envelope')):
            raise ValueError('Unchanged fixed inputs/configuration and no prior envelope are required')
        capture_source(source,staging/'source/continuation')
        stores=[Store(staging/f'worker-{slot}.sqlite',{'manifest':manifest}) for slot in range(2)]
        try:
            for slot,store in enumerate(stores):store.bind('logical_slot',slot)
            stores[0].bind('qualification_policy',PROTOCOL_POLICY)
            adjudication=_adjudicate_length_flag(stores)
            priors=record_prior_preparation(staging,stores,prior_checkpoints)
            # The known course-3 run cannot silently forget the audited course-2
            # spending, even if its older archive was omitted by the operator.
            if manifest['study_id']==COURSE_3_STUDY and COURSE_2_STUDY not in {p['study_id'] for p in priors}:
                raise ValueError('Course-3 continuation requires the supplied course-2 checkpoint for its 18 known prior executions')
            transition=dict(at=utc(),policy=PROTOCOL_POLICY,source_path='source/continuation',
                from_identity=old,to_identity=current,original_boundary=receipt['boundary'],
                original_inventory_sha256=digest(staging/'integrity.json'),
                basis='User authorized full repair of the reviewed course-3 direct-mode solution; data-informed pre-main protocol/pilot admission amendment')
            stores[0].bind('implementation_transition',transition)
            restore_tail(stores[0],tail,evidence,boundary=transition['original_inventory_sha256'])
            after=analysis(staging)
            for table in ('traces','attempts','episodes','sessions','annotations'):
                if canonical(before[table])!=canonical(after[table]):
                    raise ValueError('Continuation changed original scientific evidence: '+table)
            if json.loads((staging/'run.json').read_text())!=manifest:
                raise ValueError('Continuation changed the original manifest')
        finally:
            for store in stores:store.close()
        # The old inventory/report is retained as history; the next ordinary
        # controller checkpoint writes a new self-consistent bundle/report.
        history=staging/'receipts/pre-transition'; history.mkdir(parents=True)
        shutil.copy2(staging/'integrity.json',history/'integrity.json')
        shutil.copy2(staging/'reports/analysis.json',history/'analysis.json')
        (staging/'integrity.json').unlink()  # Staging only; never alter the input.
        if target.exists():target.rmdir()  # Only the checked empty destination.
        staging.replace(target)
    return dict(study_id=manifest['study_id'],preserved_attempts=before['summary']['attempts'],
                prior_attempts=after['summary']['prior_attempts'],campaign_attempts=after['summary']['campaign_attempts'],
                policy=PROTOCOL_POLICY,model_defect_adjudicated=bool(adjudication),model_attempts=0)
