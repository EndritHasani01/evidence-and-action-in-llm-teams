"""Course execution interface over the accepted M1--M4 records and runner.

GPU operations are opt-in. This module imports no CUDA or pretrained weights.
The source manifest, frozen run packet and worker SQLite files are authoritative;
gate summaries, reports and portable exports are derived from them.
"""

import argparse
from collections import Counter, defaultdict
from contextlib import ExitStack, closing
from dataclasses import asdict, replace
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sqlite3
import sys
import traceback
import tempfile
from time import monotonic
import zipfile

if not __package__:
    import types
    for name in ("scripts", "tests"):
        namespace = types.ModuleType(name)
        namespace.__path__ = [str(Path(__file__).resolve().parents[1]/name)]
        sys.modules.setdefault(name, namespace)

from recovery.accounting import (BudgetStop, CourseBudget, MonitoringCourseBudget, FINAL, course_admission,
    budget_from_record, format_status, progress_snapshot, timestamp)
from recovery.evaluate import evaluate_run, read_records
from recovery.inference import TokenizerFactory, course_candidate
from recovery.manifests import load_population, load_schedules
from recovery.prompts import COURSE_LIMITS, prompt_profile, render_request, tokenize_request
from recovery.protocol import GeneratedReply, failed_reply, validate_reply
from recovery.rounds import deserialize_state, prepare_round, snapshot_bytes
from recovery.runner import DurableRunner, WorkerReader
from recovery.schedule import component_counts, dependency_order
from recovery.storage import RecordedFailure, WorkerStore, record_json, settings_json, utc_now
from recovery.truth import solve_world
from recovery.workers import LocalScheduler, WorkerInterrupted, WorkerSpec, _own_file
from scripts.m5_course_smoke import CANDIDATE, SmokeFactory, resources as smoke_resources
from scripts.m5_course_preparation import read, preparation_files

BOUNDS = dict(timeout_seconds=120., termination_seconds=1., heartbeat_seconds=1.)
AS_OF_SEED = 20261006
MIN_HEADROOM = 1610612736


def course_budget(config, values=None):
    cls = MonitoringCourseBudget if config.get("resource_policy") == "observe" else CourseBudget
    return cls(**(values if values is not None else config["budget"]))


def end_observations(bundle, current_assignment=None, *, through=None):
    """Keep measured intervals and unknown gaps; never fabricate GPU release."""
    for path in all_workers(bundle):
        with _own_file(path), closing(WorkerStore(path)) as store:
            for row in store.connection.execute("SELECT * FROM allocations WHERE stopped_at IS NULL").fetchall():
                billing = json.loads(row["billing_json"] or "{}")
                if billing.get("provider_assignment_at") == current_assignment:
                    continue
                if billing.get("measurement_scope") != "observed_notebook_interval":
                    raise ValueError("previous physical allocation still needs actual release evidence")
                observed = [row["started_at"]]
                if through:
                    observed.append(through)
                for table,fields in (("attempts",("started_at","finished_at","recovered_at")),
                        ("provider_processes",("started_at","ready_at","last_observed_at","stopped_at","recovered_at"))):
                    for record in store.connection.execute("SELECT * FROM "+table):
                        observed.extend(record[field] for field in fields if field in record.keys() and record[field])
                store.allocation_observation_ended(row["number"],at=max(observed,key=timestamp),
                    reason="saved notebook observation ended; time outside recorded activity remains unknown")


def save(path, value):
    """Atomic replacement of derived views; canonical evidence is never removed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    temporary.replace(path)


def require_authorization(config, action):
    text = config.get("authorizations", {}).get(action, "")
    if type(text) is not str or not text.strip():
        raise BudgetStop(f"explicit_{action}_authorization_missing")
    return text


def safe_extract(archive, destination):
    """Fresh destination, no traversal, duplicate members or symbolic links."""
    destination = Path(destination).resolve()
    if destination.exists():
        raise FileExistsError(destination)
    with zipfile.ZipFile(archive) as source:
        names = set()
        for item in source.infolist():
            path = PurePosixPath(item.filename)
            if (item.filename in names or path.is_absolute() or ".." in path.parts
                    or "\\" in item.filename or ":" in item.filename
                    or (item.external_attr >> 16) & 0o170000 == 0o120000):
                raise ValueError("unsafe or duplicated portable archive member")
            names.add(item.filename)
        destination.mkdir(parents=True)
        source.extractall(destination)


def worker_paths(bundle, stage):
    return tuple(Path(bundle)/stage/f"worker-{i}.sqlite" for i in range(2))

def current_assignment(bundle, stage, config, physical_devices=None):
    """Recognize only two persisted segments of this still-assigned session."""
    if not config.get("continuous_assignment"):
        return False
    rows = []
    for path in worker_paths(bundle, stage):
        if not path.exists():
            continue
        with closing(WorkerStore(path, readonly=True)) as store:
            rows.extend(dict(r) for r in store.connection.execute("SELECT * FROM allocations WHERE stopped_at IS NULL"))
    if not rows:
        return False
    if len(rows) != 2:
        raise BudgetStop("partial_continuous_assignment_requires_provider_release")
    for index, row in enumerate(rows):
        billing = json.loads(row["billing_json"] or "{}")
        if (row["device"] != f"kaggle-t4-slot-{index}" or row["stage"] != stage
                or billing.get("provider") != "kaggle"
                or billing.get("provider_assignment_at") != config.get("allocated_at")
                or not billing.get("physical_gpu_uuid")
                or physical_devices and billing["physical_gpu_uuid"] != physical_devices[index]):
            raise BudgetStop("open_allocation_belongs_to_another_session_or_device")
    return True


def transfer_assignment(bundle, source_stage, target_stage, config, *, budget=None):
    """Partition a continuous assignment at a quiescent scientific stage boundary."""
    authorization = require_authorization(config, "main" if target_stage == "main" else "pilot")
    # Hardware rows have development accounting, but their directory is hardware.
    sources = worker_paths(bundle, source_stage)
    targets = worker_paths(bundle, target_stage)
    targets[0].parent.mkdir(parents=True, exist_ok=True)
    at = utc_now()
    with ExitStack() as stack:
        pairs = []
        for index, (source, target) in enumerate(zip(sources, targets)):
            stack.enter_context(_own_file(source))
            stack.enter_context(_own_file(target))
            previous = WorkerStore(source)
            following = stack.enter_context(DurableRunner(target,None)).store
            stack.callback(previous.close)
            rows = previous.connection.execute("SELECT * FROM allocations WHERE stopped_at IS NULL").fetchall()
            if (len(rows) != 1
                    or previous.connection.execute("SELECT COUNT(*) FROM provider_processes WHERE stopped_at IS NULL").fetchone()[0]
                    or previous.connection.execute("SELECT COUNT(*) FROM attempts WHERE status='running'").fetchone()[0]):
                raise BudgetStop("stage_transfer_requires_quiescent_original_workers")
            row = rows[0]
            billing = json.loads(row["billing_json"] or "{}")
            if (billing.get("provider_assignment_at") != config.get("allocated_at")
                    or row["device"] != f"kaggle-t4-slot-{index}" or not billing.get("physical_gpu_uuid")):
                raise BudgetStop("stage_transfer_must_preserve_the_current_physical_assignment")
            if following.connection.execute("SELECT 1 FROM allocations WHERE stopped_at IS NULL").fetchone():
                raise BudgetStop("successor_assignment_already_open")
            pairs.append((previous, following, row, billing))
        # Write successors first. A crash leaves visible overlapping/partial
        # intervals and admission refuses; it never silently loses paid time.
        successors = []
        for previous, following, row, billing in pairs:
            billing = {k:v for k,v in billing.items() if k not in ("segment_end", "successor_stage")}
            billing.update(authorization=authorization, provider_release_confirmed=False)
            number = following.allocation_started(row["device"], target_stage, started_at=at,
                budget=budget or course_budget(config), billing=billing)
            successors.append(dict(following.connection.execute("SELECT * FROM allocations WHERE number=?", (number,)).fetchone()))
        for (previous, following, row, billing), successor in zip(pairs, successors):
            previous.allocation_transferred(row["number"], successor, at=at)
    return dict(at=at, from_stage=source_stage, to_stage=target_stage, provider_release_confirmed=False)


def start_assignment(bundle, stage, config, budget):
    """Charge a resumed session from its actual assignment, including setup."""
    import subprocess
    inventory = subprocess.check_output(["nvidia-smi", "--query-gpu=uuid,name", "--format=csv,noheader"], text=True, timeout=5)
    rows = [line.split(",") for line in inventory.splitlines()]
    if len(rows) != 2 or any("T4" not in r[1] for r in rows) or rows[0][0] == rows[1][0]:
        raise BudgetStop("two_actual_T4_replicas_required")
    if current_assignment(bundle, stage, config, tuple(r[0].strip() for r in rows)):
        return
    for path in all_workers(bundle):
        with closing(WorkerStore(path, readonly=True)) as store:
            if store.connection.execute("SELECT 1 FROM allocations WHERE stopped_at IS NULL").fetchone():
                raise BudgetStop("previous_session_provider_release_receipt_required")
    authorization = require_authorization(config, "main" if stage == "main" else "pilot")
    worker_paths(bundle, stage)[0].parent.mkdir(parents=True, exist_ok=True)
    for index, path in enumerate(worker_paths(bundle, stage)):
        with _own_file(path), DurableRunner(path,None) as runner:
            store = runner.store
            store.allocation_started(f"kaggle-t4-slot-{index}", stage, started_at=config["allocated_at"],
                budget=budget, billing=dict(provider="kaggle", provider_assignment_at=config["allocated_at"],
                    physical_gpu_uuid=rows[index][0].strip(), authorization=authorization,
                    measurement_scope="observed_notebook_interval" if config.get("resource_policy") == "observe" else "provider_assignment",
                    release_instructions=config["release_instructions"]))


def all_workers(bundle):
    ordinary = tuple(p for stage in ("hardware", "development", "main") for p in worker_paths(bundle, stage) if p.exists())
    children = tuple(p for child in sorted((Path(bundle)/"candidates").glob("*")) if child.is_dir() for p in all_workers(child))
    return ordinary + refused_workers(bundle) + children


def refused_workers(bundle):
    return tuple(sorted((Path(bundle)/"refusals").glob("*/worker-*.sqlite")))


def record_refused_allocation(root, bundle, config, action, reason, *, devices=None):
    """Already assigned Kaggle GPUs stay chargeable when an early gate refuses.

    Use ordinary allocation-only worker ledgers; no call/checkpoint/provider is
    created. Their costs enter subsequent status/admission as historical files.
    """
    if action not in ("hardware", "capability", "pilot", "main") or config.get("execute_gpu") is not True or not config.get("allocated_at"):
        return
    assigned = config["allocated_at"]
    if timestamp(assigned) > timestamp(utc_now()):
        return
    # Existing scheduler/smoke allocations already cover the assignment.
    for path in all_workers(bundle):
        store = WorkerStore(path, readonly=True)
        try:
            if store.connection.execute("SELECT 1 FROM allocations WHERE started_at=?", (assigned,)).fetchone():
                return
        finally:
            store.close()
    if devices is None:
        import subprocess
        inventory = subprocess.check_output(["nvidia-smi", "--query-gpu=uuid", "--format=csv,noheader"], text=True, timeout=5)
        devices = tuple(line.strip() for line in inventory.splitlines() if line.strip())
    if not devices:
        return
    stage = "main" if action == "main" else "development"
    worlds, branches = scope(root, bundle, stage)
    settings = read(preparation_files(root,CANDIDATE)["packet"])["settings"]
    saved = read(Path(bundle)/"run.json") if (Path(bundle)/"run.json").exists() else None
    budget = course_budget(config,saved["budget"] if saved else config["budget"])
    label = datetime.fromisoformat(assigned).astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    directory = Path(bundle)/"refusals"/label
    directory.mkdir(parents=True, exist_ok=False)
    for i, physical in enumerate(devices):
        with DurableRunner(directory/f"worker-{i}.sqlite", None) as runner:
            store = runner.store
            store.bind_run(worlds, branches, settings, BOUNDS, budget=budget, regime="course")
            number = store.allocation_started(f"kaggle-t4-slot-{i}", stage, budget=budget, started_at=assigned,
                billing=dict(provider="kaggle", physical_gpu_uuid=physical, unadmitted_action=action,
                    measurement_scope="observed_notebook_interval" if config.get("resource_policy") == "observe" else "provider_assignment",
                    provider_assignment_at=assigned))
            store.allocation_stop_requested(number, "gate refusal; provider release pending: "+reason)

def recover_bootstrap_refusals(root, bundle, current_config):
    """Materialize pre-install assignment receipts into the ordinary ledgers."""
    for path in sorted((Path(bundle)/"bootstrap-refusals").glob("*.json")):
        receipt = read(path)
        correction = current_config.get("bootstrap_refusal_assignments", {}).get(path.name, {})
        if correction:
            if not correction.get("evidence", "").strip():
                raise BudgetStop("bootstrap_assignment_correction_requires_provider_evidence")
            if correction.get("allocated_at"):
                if timestamp(correction["allocated_at"]) > timestamp(receipt["observed_at"]):
                    raise ValueError("corrected assignment cannot follow its observed refusal")
                receipt["allocated_at"] = correction["allocated_at"]
            if correction.get("physical_devices"):
                receipt["physical_devices"] = correction["physical_devices"]
        if not receipt.get("allocated_at") or not receipt.get("physical_devices"):
            raise BudgetStop("earlier_bootstrap_assignment_interval_unknown; reconcile it before GPU work")
        config = receipt["config"]
        config.update(execute_gpu=True,allocated_at=receipt["allocated_at"])
        record_refused_allocation(root,bundle,config,receipt.get("stage","hardware"),
            receipt["reason"],devices=tuple(receipt["physical_devices"]))


def initialize(root, bundle):
    root, bundle = Path(root).resolve(), Path(bundle).resolve()
    bundle.mkdir(parents=True, exist_ok=True)
    for name, fixture in (("population.json", "population_course.json"), ("schedules.json", "schedules_course.json")):
        source, target = root/"tests/fixtures"/fixture, bundle/"inputs"/name
        target.parent.mkdir(exist_ok=True)
        if target.exists():
            if target.read_bytes() != source.read_bytes():
                raise ValueError("course saved inputs differ from the uploaded source")
        else:
            shutil.copyfile(source, target)
    population = load_population(bundle/"inputs/population.json")
    schedules = load_schedules(bundle/"inputs/schedules.json", population)
    if population.regime != "course":
        raise ValueError("this workflow executes only the adopted course regime")
    totals = [tuple(sum(row[i] for row in component_counts(branches).values()) for i in (0, 1))
              for branches in (schedules.development, schedules.main_for(population, 20))]
    if totals != [(1114, 1178), (5752, 6280)] or len(schedules.capability) != 90:
        raise ValueError("complete course schedule/counts differ")
    return population, schedules


def scope(root, bundle, stage):
    population, schedules = initialize(root, bundle)
    return ((population.development, schedules.development) if stage == "development" else
            (population.worlds(20), schedules.main_for(population, 20)))


def confirm_previous_release(bundle, receipt, *, now=None):
    """Record a real provider release, preserving unknown completion around crashes.

    Call only on a restored/stopped session. A local worker exit never supplies
    this acknowledgement, and a future/current-session receipt is rejected.
    """
    if not receipt or not receipt.get("released_at") or not receipt.get("evidence", "").strip():
        return 0
    at, now = receipt["released_at"], now or utc_now()
    if timestamp(at) > timestamp(now):
        raise ValueError("provider release cannot be in the future")
    updates = 0
    for path in all_workers(bundle):
        with _own_file(path):
            store = WorkerStore(path)
            try:
                for row in store.connection.execute("SELECT * FROM allocations WHERE stopped_at IS NULL").fetchall():
                    if timestamp(at) < timestamp(row["started_at"]):
                        raise ValueError("release receipt precedes an open allocation")
                    observed = store.connection.execute("SELECT MAX(last_observed_at) FROM provider_processes").fetchone()[0]
                    finished = store.connection.execute("SELECT MAX(finished_at) FROM attempts").fetchone()[0]
                    if any(value and timestamp(value) > timestamp(at) for value in (observed, finished)):
                        raise ValueError("release receipt precedes observed model work")
                    # On a different VM, old PIDs are meaningless. The provider
                    # receipt bounds their exit without inventing exact timing.
                    with store.connection:
                        store.connection.execute("""UPDATE provider_processes SET stopped_at=?,
                            uncertain_stop=1,recovered_at=?,termination_reason=? WHERE stopped_at IS NULL""",
                            (at, at, "provider release receipt: "+receipt["evidence"]))
                    for call in store.connection.execute("SELECT call_id FROM calls WHERE status='running'").fetchall():
                        attempts = store.attempts(call[0])
                        if attempts and attempts[-1]["status"] == "running":
                            store.interrupt_attempt(call[0], "provider release confirmed; unobserved completion retained")
                    store.allocation_stopped(row["number"], "provider release: "+receipt["evidence"], released_at=at)
                    updates += 1
            finally:
                store.close()
    if updates:
        save(Path(bundle)/"provider-release.json", receipt)
    return updates


def backup_bundle(bundle, destination):
    """Export quiescent canonical evidence using ordinary SQLite backups.

    The caller drains rounds/stops workers first. Do not zip live WAL files.
    Previously downloaded ZIPs remain valid immutable session snapshots.
    """
    bundle, destination = Path(bundle).resolve(), Path(destination).resolve()
    if destination.is_relative_to(bundle):
        raise ValueError("put exports outside the canonical bundle")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_zip = destination.with_suffix(".tmp")
    paths = all_workers(bundle)
    with tempfile.TemporaryDirectory() as directory:
        backups = {}
        for i, path in enumerate(paths):
            target = Path(directory)/f"worker-{i}.sqlite"
            store = WorkerStore(path, readonly=True)
            try:
                store.backup(target)
            finally:
                store.close()
            with closing(sqlite3.connect(target)) as db:
                if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                    raise ValueError("portable SQLite integrity check failed")
            backups[path] = target
        with zipfile.ZipFile(temporary_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=3) as archive:
            for path in sorted(bundle.rglob("*")):
                if not path.is_file() or path.is_symlink() or path.name.endswith(("-wal", "-shm", ".owner", ".tmp")):
                    continue
                if "__pycache__" in path.parts or path.suffix == ".pyc":
                    continue
                archive.write(backups.get(path, path), path.relative_to(bundle).as_posix())
    try:
        temporary_zip.replace(destination)
    except PermissionError:
        destination = destination.with_name("course-resume-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")+".zip")
        temporary_zip.replace(destination)
    return dict(path=str(destination), bytes=destination.stat().st_size,
                canonical_workers=len(paths), provider_release_confirmed=False)


def capability_gate(worlds, branches, paths):
    tables = evaluate_run(worlds, branches, paths)
    rows = [r for r in tables["outcomes"] if r["phase"] in ("prefix", "control")]
    controls = [r for r in rows if r["phase"] == "control"]
    final = [r for r in rows if r["phase"] == "prefix" and r["round"] == 4]
    families = sorted({w.world.task.value for w in worlds})
    by_family = {family:dict(controls_correct=sum(r["correct"] == 1 for r in controls if r["family"] == family),
        final_peers_correct=sum(r["correct"] == 1 for r in final if r["family"] == family),
        invalid_or_failed=sum(r["protocol_outcome"] in ("invalid", "failed") for r in rows if r["family"] == family))
        for family in families}
    counts = dict(scheduled=len(rows), recorded=sum(r["correct"] is not None for r in rows),
        controls_correct=sum(r["correct"] == 1 for r in controls),
        final_peers_correct=sum(r["correct"] == 1 for r in final),
        jointly_correct_prefixes=sum(all(r["correct"] == 1 for r in final if r["world_id"] == w.world_id)
                                     for w in worlds))
    passed = (len(worlds) == 5 and counts["scheduled"] == counts["recorded"] == 90
        and counts["controls_correct"] >= 9 and counts["final_peers_correct"] >= 14
        and counts["jointly_correct_prefixes"] >= 3 and all(r["controls_correct"] >= 1 for r in by_family.values()))
    return dict(passed=passed, status="passed" if passed else "incomplete" if counts["recorded"] < 90 else "failed",
        counts=counts, by_family=by_family, rows=rows,
        interpretation="Operational development screen; no main treatment effects or added independent worlds")


def audit_records(worlds, branches, paths, tokenizer, settings):
    """Re-render, revalidate, recompute independent gold and replay committed effects.

    Archived replies are the sole provider in the scratch reconstruction. This
    audit never invokes a model and never changes the original worker files.
    Partial raw rounds are checked without fabricating their missing peers.
    """
    from tests.references import numeric_reference, relaxation_distances
    records, inputs, attempts, committed = read_records(worlds, branches, paths, include_committed=True)
    tables = evaluate_run(worlds, branches, paths)
    by_world = {w.world_id:w for w in worlds}
    scheduled = {c.call_id:(b, c) for b in branches for c in b.calls}
    last_rounds = {}
    for branch in branches:
        if branch.phase == "control":
            row = records.get(branch.calls[0].call_id)
            last_rounds[branch.branch_id] = int(bool(row and row["status"] in FINAL and row["validation_json"]))
        elif branch.branch_id in committed:
            state = deserialize_state(record_json(committed[branch.branch_id]["state"]))
            last_rounds[branch.branch_id] = state.last_slot.round_number if state.last_slot and state.last_slot.phase == state.phase else 0
        else:
            last_rounds[branch.branch_id] = 0
            if any(bid == branch.branch_id for bid,r in inputs):
                raise ValueError("saved branch requests lack their committed boundary")
        if any(bid == branch.branch_id and r > last_rounds[branch.branch_id]+1 for bid,r in inputs):
            raise ValueError("future round requests lack an intervening committed boundary")
    committed_complete = all(last_rounds[b.branch_id] == (1 if b.phase == "control" else 4) for b in branches)
    completed_raw = [r for r in records.values() if r["replay_parent"] is None and r["status"] == "completed"]
    native = [a for a in attempts if a.get("backend_json") and a["status"] == "completed" and
        (lambda f:f.get("cache", {}).get("initial_empty") is True and f.get("finite_score_steps",0) > 0 and
         f.get("device") == "cuda:0" and not f.get("hardware_diagnostic"))(json.loads(a["backend_json"]))]
    native_ids = {a["call_id"] for a in native}
    actual_model_evidence = bool(completed_raw) and all(r["call_id"] in native_ids for r in completed_raw)
    gold_checked = 0
    for world in worlds:
        for event in ("original", "revision", "preserving"):
            if event == "preserving" and world.preserving_edit is None:
                continue
            native = world.world if event == "original" else world.event_world(event)
            truth = solve_world(native)
            raw = [r.value for r in sorted(native.records, key=lambda r:r.position if r.position is not None else r.record_id)
                   if not r.deleted]
            reference = (relaxation_distances(native.size.node_count, raw) if native.task.value == "bfs_distance"
                         else numeric_reference(native.task.value, raw))
            actual = truth.candidate(None)
            if actual != reference:
                raise ValueError("independent gold differs: "+world.world_id)
            gold_checked += 1
    with ExitStack() as stack:
        stores = []
        for path in paths:
            if Path(path).exists():
                store = WorkerStore(path, readonly=True)
                stack.callback(store.close)
                if store.connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                    raise ValueError("worker integrity check failed")
                stores.append(store)
        for store in stores:
            store.parents = tuple(other for other in stores if other is not store)
        owners = {r["call_id"]:s for s in stores for r in s.connection.execute("SELECT call_id FROM calls")}
        for call_id, saved in records.items():
            branch, call = scheduled[call_id]
            if tuple(saved[k] for k in ("branch_id", "seed", "generation_id", "replay_parent", "round_number", "peer")) != (
                    branch.branch_id, call.seed, call.generation_id, call.replay_parent, call.round_number,
                    -1 if call.peer is None else call.peer):
                raise ValueError("saved call identity/seed/replay parent differs from schedule")
        for row in inputs.values():
            if row["settings_json"] != settings_json(settings):
                raise ValueError("audited candidate/template/settings differ")
            data = row["requests"]
            if "view" in data:
                from scripts.m5_course_preparation import peer_view
                views = [peer_view(data["view"])]
                rendered, tokens = [data["rendered"]], [data["tokenized"]]
            else:
                before = deserialize_state(data["before"])
                prepared = prepare_round(before, tokenizer, limits=COURSE_LIMITS, profile=prompt_profile(settings))
                # Include permitted views, exact native requests and pre-delivery state.
                re_rendered = dict(before=snapshot_bytes(prepared.before).decode("utf-8"), slot=asdict(prepared.slot),
                    rendered=[asdict(r) for r in prepared.rendered], tokenized=[asdict(t) for t in prepared.tokenized])
                if record_json(re_rendered) != record_json(data):
                    raise ValueError("saved native request/state differs from re-rendering")
                views, rendered, tokens = prepared.views, data["rendered"], data["tokenized"]
            for i, view in enumerate(views):
                rendered_now = render_request(view, limits=COURSE_LIMITS, profile=prompt_profile(settings))
                if (record_json(asdict(rendered_now)) != record_json(rendered[i]) or
                        record_json(asdict(tokenize_request(rendered_now, tokenizer, limits=COURSE_LIMITS))) != record_json(tokens[i])):
                    raise ValueError("native rendering/tokenization audit failed")
                bid, number = row["branch_id"], row["round_number"]
                calls = [c for b in branches if b.branch_id == bid for c in b.calls
                         if c.round_number == number and c.peer == view.peer]
                call = calls[0]
                if call.call_id not in owners:
                    continue
                store = owners[call.call_id]
                saved = store.call(call.call_id)
                if saved["status"] not in FINAL:
                    continue
                raw = store.response(call.call_id)
                validation = (validate_reply(view, raw, tokenizer, limits=COURSE_LIMITS)
                              if type(raw) is GeneratedReply else failed_reply(view))
                if saved["validation_json"] and saved["validation_json"] != record_json(asdict(validation)):
                    raise ValueError("raw reply independent validation differs")
        comparisons = 0
        with tempfile.TemporaryDirectory() as directory:
            ordered = dict.fromkeys(b.branch_id for b,c in dependency_order(branches))
            by_branch = {b.branch_id:b for b in branches}
            for branch_id in ordered:
                branch = by_branch[branch_id]
                if branch.branch_id not in committed and branch.phase != "control":
                    continue
                if branch.phase == "control" and (branch.calls[0].call_id not in records or
                        records[branch.calls[0].call_id]["validation_json"] is None):
                    continue
                def archived(view, rendered, tokenized, *, seed, settings, branch=branch):
                    call = next(c for c in branch.calls if c.peer == view.peer and c.round_number == view.slot.round_number)
                    if call.call_id not in owners or records[call.call_id]["status"] not in FINAL:
                        raise ValueError("committed checkpoint depends on missing raw reply")
                    return owners[call.call_id].response(call.call_id)
                # Audit each branch against original read-only parents. No full
                # second run accumulates on disk; every prefix is independently
                # reconstructed too, and each child's boundary is compared.
                with tempfile.TemporaryDirectory(dir=directory) as branch_directory, DurableRunner(
                        Path(branch_directory)/"reconstructed.sqlite", tokenizer, archived, scripted=True,
                        dependencies=tuple(Path(p) for p in paths if Path(p).exists())) as runner:
                    # The scratch branch owns its current calls. Original files
                    # supply only its parents, avoiding duplicate current IDs.
                    # URI mode=ro still forbids every main-database write; TEMP
                    # views are private to these disposable audit connections.
                    for parent in runner.dependencies:
                        con = parent.store.connection
                        con.execute("PRAGMA query_only=OFF")
                        con.execute("CREATE TEMP TABLE audit_branch(branch_id TEXT)")
                        con.execute("INSERT INTO audit_branch VALUES (?)", (branch.branch_id,))
                        for table in ("calls", "round_inputs"):
                            con.execute(f"CREATE TEMP VIEW {table} AS SELECT * FROM main.{table} WHERE branch_id NOT IN (SELECT branch_id FROM audit_branch)")
                        con.commit()
                        con.execute("PRAGMA query_only=ON")
                    from recovery.manifests import _branch, _prepared
                    binding = stores[0].run_inputs
                    if binding is None:
                        raise ValueError("course audit requires the original bound worker inputs")
                    runner.store.bind_run(tuple(_prepared(w) for w in binding["worlds"]),
                        tuple(_branch(b) for b in binding["branches"]), binding["settings"], binding["bounds"],
                        budget=budget_from_record(binding["budget"]) if binding.get("budget") else None,
                        regime="course")
                    if branch.phase == "control":
                        call = branch.calls[0]
                        if call.call_id in records and records[call.call_id]["validation_json"] is not None:
                            runner.run_control(by_world[branch.world_id], branch, settings=settings)
                            expected = runner.store.connection.execute("SELECT requests_json FROM round_inputs WHERE branch_id=?", (branch.branch_id,)).fetchone()[0]
                            if expected != record_json(inputs[(branch.branch_id, 1)]["requests"]):
                                raise ValueError("control exposes a changed full-information view")
                        continue
                    runner.start(by_world[branch.world_id], branch, settings=settings)
                    target = deserialize_state(record_json(committed[branch.branch_id]["state"]))
                    last = target.last_slot.round_number if target.last_slot and target.last_slot.phase == target.phase else 0
                    for number in range(1, last+1):
                        runner.run_round(branch.branch_id, number)
                        expected = runner.store.connection.execute("SELECT requests_json FROM round_inputs WHERE branch_id=? AND round_number=?", (branch.branch_id, number)).fetchone()[0]
                        if expected != record_json(inputs[(branch.branch_id, number)]["requests"]):
                            raise ValueError("reconstructed branch boundary differs from original saved requests")
                    if snapshot_bytes(runner.state(branch.branch_id)) != snapshot_bytes(target):
                        raise ValueError("archived reply replay differs from committed sources/history/queues/deliveries")
                    pending = inputs.get((branch.branch_id, last+1))
                    if pending and pending["requests"]["before"] != snapshot_bytes(target).decode("utf-8"):
                        raise ValueError("unfinished round view differs from its last committed boundary")
                    comparisons += 1
    return dict(passed=True, gold_cases=gold_checked, raw_calls_checked=len(records),
        committed_branches_reconstructed=comparisons, coverage=tables["coverage"],
        committed_schedule_complete=committed_complete, actual_model_evidence=actual_model_evidence,
        inference_calls=0, missing_slots="unknown", note="Independent gold; literal raw reply validation and branch-local effect reconstruction")


def pilot_gate(worlds, branches, paths, *, audit=None):
    tables = evaluate_run(worlds, branches, paths)
    rows = [r for r in tables["outcomes"] if r["replay_parent"] is None]
    valid = sum(r["protocol_outcome"] == "valid" for r in rows)
    recorded = sum(r["correct"] is not None for r in rows)
    failures = defaultdict(Counter)
    for r in rows:
        failures[(r["family"], r["phase"], r["policy"] or "none", r["event"])][r["protocol_outcome"]] += 1
    group_rows = [dict(family=k[0], phase=k[1], policy=k[2], event=k[3], outcomes=dict(v)) for k,v in sorted(failures.items())]
    capability = capability_gate(worlds, branches, paths)
    complete = (len(rows) == recorded == 1114 and tables["coverage"]["recorded"] == 1178
                and bool(audit and audit.get("committed_schedule_complete")))
    passed = complete and valid*100 >= 98*1114 and capability["passed"] and bool(audit and audit["passed"])
    return dict(passed=passed, complete=complete, distinct_scheduled=len(rows), distinct_recorded=recorded,
        protocol_valid=valid, validity_denominator=1114, minimum_valid=1092, capability=capability,
        family_condition_failures=group_rows, audit=audit,
        status="passed" if passed else "incomplete" if not complete else "failed")


def hardware_gate(bundle, review, *, assignment=None):
    report = read(Path(bundle)/"hardware/report.json")
    paths = worker_paths(bundle, "hardware")
    probes, ordinary, loads, all_attempts = [], [], [], []
    segment_closed, released, quiescent, same_assignment = True, True, True, True
    for path in paths:
        store = WorkerStore(path, readonly=True)
        try:
            allocations = store.connection.execute("SELECT * FROM allocations").fetchall()
            segment_closed &= all(r["stopped_at"] is not None for r in allocations)
            released &= all(r["stopped_at"] is not None and
                json.loads(r["billing_json"] or "{}").get("segment_end") not in ("stage_transfer","observation_end") and
                json.loads(r["billing_json"] or "{}").get("measurement_scope") != "observed_notebook_interval" for r in allocations)
            quiescent &= (store.connection.execute("SELECT COUNT(*) FROM provider_processes WHERE stopped_at IS NULL").fetchone()[0] == 0
                and store.connection.execute("SELECT COUNT(*) FROM attempts WHERE status='running'").fetchone()[0] == 0)
            same_assignment &= bool(allocations) and all(r["stopped_at"] is not None or
                json.loads(r["billing_json"] or "{}").get("provider_assignment_at") == assignment for r in allocations)
            loads.extend(json.loads(r[0]) for r in store.connection.execute("SELECT backend_json FROM provider_processes WHERE backend_json IS NOT NULL"))
            for row in store.connection.execute("SELECT * FROM attempts"):
                all_attempts.append(dict(row))
                facts = json.loads(row["backend_json"]) if row["backend_json"] else {}
                if facts.get("hardware_diagnostic"):
                    probes.append(facts)
                elif row["status"] == "completed":
                    ordinary.append(facts)
        finally:
            store.close()
    bound_input = review.get("complete_input_tokens_upper",109851)
    complete_probes = (len(probes) == 2 and all(p.get("input_tokens") == bound_input and p.get("forced_output_tokens") == 256
        and p.get("finite_score_steps") == 256 and p.get("cache", {}).get("initial_empty") is True for p in probes))
    samples = [s for p in ordinary+probes for s in p.get("observed_model_edge_memory", [])]
    observed_peak = max((s["total_bytes"]-s["free_bytes"] for s in samples), default=0)
    free_min = min((s["free_bytes"] for s in samples), default=0)
    total_min = min((s["total_bytes"] for s in samples), default=0)
    bound = review.get("complete_live_memory_upper_bound_bytes")
    supported = (review.get("accepted") is True and type(bound) is int and bound >= observed_peak
        and bound >= 7400914336 and bound+MIN_HEADROOM <= total_min
        and bool(review.get("justification", "").strip()))
    measured = review.get("acceptance") == "measured_stress"
    host_receipt = read(Path(bundle)/"hardware/host-checks.json") if (Path(bundle)/"hardware/host-checks.json").exists() else {}
    host_passed = host_receipt.get("tests") == 3 and host_receipt.get("skipped") == 0
    native_loads = [l for l in loads if l.get("model") == CANDIDATE.model]
    valid_loads = bool(native_loads) and all(l.get("revision") == CANDIDATE.revision and
        len(l.get("candidate_attention", [])) == 3 for l in native_loads)
    cache_passed = len(ordinary) == 21 and all(p.get("cache", {}).get("initial_empty") is True and
        p.get("cache", {}).get("same_call_cache") is True and p.get("finite_score_steps", 0) > 0 for p in ordinary)
    passed = (report.get("root_blocker") is None and report.get("smoke", {}).get("stop_reason") is None
        and complete_probes and len(ordinary) == 21 and valid_loads
        and (segment_closed or assignment is not None and same_assignment and quiescent)
        and free_min >= MIN_HEADROOM and (measured or supported) and host_passed and cache_passed)
    return dict(passed=passed, status="passed" if passed else "review_required" if complete_probes and free_min >= MIN_HEADROOM else "incomplete_or_failed",
        complete_resident_tokens_upper=bound_input+256, complete_envelope_probes=len(probes),
        full_envelope_minimum_free_bytes=min((s["free_bytes"] for p in probes for s in p.get("observed_model_edge_memory",[])),default=None),
        memory_scope="completed model-edge samples; full-envelope acceptance requires both completed probes",
        ordinary_completed=len(ordinary), actual_minimum_free_bytes=free_min if samples else None,
        observed_device_peak_bytes=observed_peak if samples else None,
        complete_live_memory_upper_bound_bytes=bound, review=review, host_checks=host_receipt,
        native_load_checks_passed=valid_loads, provider_release_confirmed=released,
        accounting_segment_closed=segment_closed, inference_processes_quiescent=quiescent,
        terminal_attempts=[{k:r[k] for k in ("call_id","number","status","reason","timeout_seconds","elapsed_seconds","worker_pid")}
            for r in all_attempts if r["status"] in ("timeout","infrastructure_failure") and r["call_id"] != "smoke/course-m5/24"],
        acceptance="measured_stress" if measured else "supported_memory_bound",
        note="Measured complete-input stress/headroom acceptance; no formal memory proof claimed" if measured else
            "Physical shape diagnostics alone do not prove a complete allocator/workspace bound; a supported R7 review is required")


def accepted_budget(bundle, base, *, observe=False):
    """Derive prior hardware charges once; pilot/main ledgers stay explicit."""
    if observe:
        return MonitoringCourseBudget(**base)  # Hardware stays in the canonical ledgers.
    original = CourseBudget(**base)
    stores = []
    try:
        for path in worker_paths(bundle, "hardware"):
            stores.append(WorkerStore(path, readonly=True))
        used = smoke_resources(stores, original, utc_now())
        if any(d["stopped_at"] is None for d in used["devices"]):
            raise BudgetStop("hardware_provider_release_pending")
        if not used["admission_available"]:
            raise BudgetStop(used["admission_reason"])
        values = asdict(original)
        for name in ("development", "setup", "interruption", "other_course", "other_overall"):
            values["prior_"+name+"_gpu_hours"] = used["spending_bounds_gpu_hours"][name]
        allocated = used["allocated_gpu_hours"]
        values["prior_smoke_gpu_hours"] = [v+allocated for v in original.prior_smoke_gpu_hours]
        # Refused hardware assignments also consumed the same smoke envelope;
        # their monetary costs enter status as prior ledgers, not these bounds.
        for path in refused_workers(bundle):
            prior = WorkerStore(path, readonly=True)
            try:
                for row in prior.connection.execute("SELECT * FROM allocations"):
                    billing = json.loads(row["billing_json"] or "{}")
                    if billing.get("unadmitted_action") == "hardware":
                        if row["stopped_at"] is None:
                            raise BudgetStop("refused_hardware_assignment_release_pending")
                        hours = (timestamp(row["stopped_at"])-timestamp(row["started_at"]))/3600
                        values["prior_smoke_gpu_hours"] = [v+hours for v in values["prior_smoke_gpu_hours"]]
            finally:
                prior.close()
        values["prior_smoke_attempts"] += sum(s.connection.execute("SELECT COUNT(*) FROM attempts").fetchone()[0] for s in stores)
        values["prior_evidence"] += "; original released hardware worker allocations (included once)"
        return CourseBudget(**values)
    finally:
        for store in stores:
            store.close()


def bind_candidate(root, bundle, config, *, verify_environment=True):
    path = Path(bundle)/"run.json"
    manifest = read(Path(root)/"source-manifest.json")
    from scripts.m5_course_smoke_assets import source_identity
    source_identity(Path(root), manifest)
    prepared = read(preparation_files(root,CANDIDATE)["packet"])
    budget = accepted_budget(bundle, config["budget"],observe=config.get("resource_policy") == "observe")
    assets = read(config["assets_receipt"])
    for name, version in assets["versions"].items():
        if verify_environment and importlib.metadata.version(name) != version:
            raise ValueError("candidate environment differs from prepared assets: "+name)
    candidate = dict(source_commit=manifest["source_baseline_commit"], source_members=manifest["members"],
        settings=prepared["settings"], bounds=BOUNDS, budget=asdict(budget), environment=assets["versions"],
        analysis=dict(regime="course", resampling_seed=AS_OF_SEED, bootstrap_draws=10000,
            primaries_interval=.975, secondary_interval=.95, replicate_zero_primary=True),
        source_manifest="source/source-manifest.json", model_revision=CANDIDATE.revision,
        freeze=None)
    if config.get("resource_policy") == "observe":
        candidate["resource_policy"] = "observe"
        candidate["hardware_acceptance"] = config.get("hardware_review", {}).get("acceptance")
        candidate["smoke_attempt_limit"] = config.get("smoke_attempt_limit",24)
        candidate["smoke_attempt_allowance"] = config.get("smoke_attempt_allowance")
    if path.exists():
        saved = read(path)
        if record_json({k:v for k,v in saved.items() if k != "freeze"}) != record_json({k:v for k,v in candidate.items() if k != "freeze"}):
            raise ValueError("candidate source/settings/environment/resource binding differs; resume exact inputs")
        return saved
    save(path, candidate)
    return candidate


def snapshot(root, bundle, stage, run=None, *, now=None, devices=()):
    worlds, branches = scope(root, bundle, stage)
    return progress_snapshot(worlds, branches, worker_paths(bundle, stage), now=now,
        budget=course_budget(run) if run else None,
        settings=run["settings"] if run else None, regime="course",
        prior_paths=(tuple(p for p in worker_paths(bundle, "development") if p.exists()) if stage == "main" else ()) +
            (tuple(p for p in worker_paths(bundle,"hardware") if p.exists()) if run and run.get("resource_policy") == "observe" else ()) + refused_workers(bundle),
        planned_devices=devices)


def session_window(config):
    assigned = config.get("allocated_at")
    if not assigned or not config.get("release_instructions", "").strip():
        raise BudgetStop("actual_assignment_and_provider_release_instructions_required")
    elapsed = timestamp(utc_now())-timestamp(assigned)
    if config.get("resource_policy") == "observe":
        if elapsed < 0:
            raise ValueError("observed session start is in the future")
        return config.get("max_work_seconds",36000)-elapsed
    quota, duration = config.get("provider_quota_gpu_hours"), config.get("provider_session_seconds")
    if (elapsed < 0 or type(quota) not in (int,float) or quota <= 0 or
            type(duration) not in (int,float) or duration <= 0):
        raise BudgetStop("verify_current_quota_session_duration_and_assignment_clock")
    return min(duration-elapsed, quota*3600/2-elapsed, config.get("max_work_seconds", 3600))


def disk_admission(bundle, stage, *, complete_forecast=False):
    current = sum(p.stat().st_size for p in all_workers(bundle))
    pilot = sum(p.stat().st_size for p in worker_paths(bundle, "development") if p.exists())
    main = sum(p.stat().st_size for p in worker_paths(bundle, "main") if p.exists())
    projection = int(1.5*pilot*6280/1178) if stage == "main" and pilot else current
    # Ordinary backup + uncompressed ZIP upper allowance; reports/branch audit
    # have separate scratch. Projection is pilot-based, not a disk guarantee.
    target = max(current, projection) if complete_forecast else current
    required = (max(0, projection-main) if complete_forecast else 0)+2*target+512*1024**2
    free = shutil.disk_usage(bundle).free
    if free < required:
        raise BudgetStop("insufficient_disk_for_raw_records_backup_export_and_offline_report")
    return dict(free_bytes=free, required_free_bytes=required, observed_worker_bytes=current,
        pilot_based_main_projection_bytes=projection if stage == "main" else None,
        rule="1.5 pilot byte-rate main projection; two portable-copy allowances and 512 MiB report/branch scratch; monitor actual growth")


def hardware(root, bundle, config):
    require_authorization(config, "hardware")
    if config.get("execute_gpu") is not True:
        raise BudgetStop("gpu_execution_disabled")
    from scripts.m5_course_smoke import run as run_smoke
    launch = dict(execute_gpu=True, stage_weights=False, authorization=config["authorizations"]["hardware"],
        provider="kaggle", reported_quota_gpu_hours=config["provider_quota_gpu_hours"],
        provider_session_seconds=config["provider_session_seconds"], allocated_at=config["allocated_at"],
        prior_sessions_released=config.get("prior_sessions_released", False),
        release_instructions=config["release_instructions"], budget=config["budget"],
        hf_cache=config["hf_cache"], assets_receipt=config["assets_receipt"],
        source_manifest=str(Path(root)/"source-manifest.json"), resume_workers=[], complete_envelope_diagnostics=True)
    launch["continuous_assignment"] = config.get("continuous_assignment", False)
    if config.get("candidate"):
        launch.update(candidate=config["candidate"],envelope_timeout_seconds=config.get("envelope_timeout_seconds",600))
    launch.update(resource_policy=config.get("resource_policy"),session_limit_seconds=config.get("max_work_seconds",36000),
        smoke_attempt_limit=config.get("smoke_attempt_limit",24),smoke_attempt_allowance=config.get("smoke_attempt_allowance"))
    launch["prior_allocation_workers"] = [str(p) for p in refused_workers(bundle)]
    if (Path(bundle)/"hardware").exists():
        if not all(p.exists() for p in worker_paths(bundle, "hardware")):
            raise BudgetStop("partial_hardware_controller_setup_requires_review; no new probe identities are created")
        launch.update(resume_workers=[str(p) for p in worker_paths(bundle, "hardware")], resume_in_place=True)
    return run_smoke(Path(root), launch, Path(bundle)/"hardware")


def execute(root, bundle, config, action):
    authorization = require_authorization(config, "main" if action == "main" else "pilot")
    if config.get("execute_gpu") is not True:
        raise BudgetStop("gpu_execution_disabled")
    gate = hardware_gate(bundle, config.get("hardware_review", {}),
        assignment=config.get("allocated_at") if config.get("continuous_assignment") else None)
    save(Path(bundle)/"hardware-gate.json", gate)
    if not gate["passed"]:
        raise BudgetStop("complete_hardware_resource_release_and_R7_gate_not_passed")
    from scripts.m5_course_smoke_assets import verify_assets
    verify_assets(Path(root), dict(source_manifest=str(Path(root)/"source-manifest.json"),
        assets_receipt=config["assets_receipt"], hf_cache=config["hf_cache"],candidate=config.get("candidate")))
    run = bind_candidate(root, bundle, config)
    if action == "main" and not run["freeze"]:
        raise BudgetStop("explicit_frozen_main_admission_missing")
    stage = "main" if action == "main" else "development"
    disk_admission(Path(bundle), stage, complete_forecast=stage == "main")
    worlds, branches = scope(root, bundle, stage)
    tokenizer = TokenizerFactory(CANDIDATE, str(Path(root)/"metadata/4B"), COURSE_LIMITS)()
    if action == "pilot":
        capability = capability_gate(worlds, branches, worker_paths(bundle, stage))
        if not capability["passed"]:
            raise BudgetStop("first_90_capability_gate_not_passed")
    import subprocess
    inventory = subprocess.check_output(["nvidia-smi", "--query-gpu=uuid,name,driver_version,memory.total", "--format=csv,noheader"], text=True, timeout=5)
    device_rows = [line.split(",") for line in inventory.splitlines()]
    if len(device_rows) != 2 or any("T4" not in row[1] for row in device_rows):
        raise BudgetStop("two_actual_T4_replicas_required")
    physical_devices = tuple(row[0].strip() for row in device_rows)
    if len(set(physical_devices)) != 2:
        raise ValueError("two distinct GPUs required")
    # Stable replica positions allow measured phase/condition forecasts to
    # survive Kaggle VM replacement. Each allocation still archives the actual
    # physical UUID, host facts and model device visibility; these are not a
    # claim that the same physical card returns in the next session.
    devices = ("kaggle-t4-slot-0", "kaggle-t4-slot-1")
    budget = course_budget(run)
    wall = session_window(config)
    session_deadline = monotonic()+wall-budget.shutdown_seconds-config.get("finalization_seconds", 60)
    initial = snapshot(root, bundle, stage, run, devices=devices)
    reason, allowed = course_admission(initial["resources"], initial["forecast"], budget, stage, 2)
    if reason:
        raise BudgetStop(reason)
    continuing = current_assignment(bundle, stage, config, physical_devices)
    if initial["resources"]["active_devices"] and not continuing:
        raise BudgetStop("previous_session_provider_release_receipt_required")
    if wall <= budget.shutdown_seconds+1050:
        raise BudgetStop("insufficient_session_time_for_a_complete_bounded_round_backup_and_release")
    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", HF_HUB_CACHE=config["hf_cache"])
    paths = worker_paths(bundle, stage)
    specs = [WorkerSpec(path, SmokeFactory(physical,CANDIDATE), cuda_visible_devices=physical, allocated_device=device,
        allocated_at=utc_now() if config.get("continuous_assignment") else config["allocated_at"],
        continuing_assignment=continuing, provider_billing=dict(provider="kaggle", authorization=authorization,
            measurement_scope="observed_notebook_interval" if config.get("resource_policy") == "observe" else "provider_assignment",
            physical_gpu_uuid=physical, host_inventory=inventory,
            provider_assignment_at=config["allocated_at"],
            release_instructions=config["release_instructions"])) for path,device,physical in zip(paths,devices,physical_devices)]
    last_print, last_backup = [0.], monotonic()
    def report(progress):
        disk_admission(Path(bundle), stage)
        if monotonic()-last_print[0] >= 15 or progress["counts"]["remaining_logical"] == 0:
            save(Path(bundle)/"progress.json", progress)
            c = progress["counts"]
            print(f"{stage}: {c['finished_logical']}/{c['scheduled_logical']} recorded; "
                  f"{c['attempts']} attempts; {c['replay_uses']} replay uses; "
                  f"{c['recorded_failures']} invalid/failed; {c['unknown_logical']} unknown", flush=True)
            estimate=progress["forecast"]
            print("  "+utc_now()+"; measured remaining-time forecast: "+str(estimate.get("elapsed_seconds"))+" seconds",flush=True)
            last_print[0] = monotonic()
        # Raw replies have already been saved. Stop subsequent work on any
        # physical headroom/finite/cache defect without resampling those slots.
        for path in paths:
            if not path.exists():
                continue
            store = WorkerStore(path, readonly=True)
            try:
                for row in store.connection.execute("SELECT backend_json FROM attempts WHERE backend_json IS NOT NULL"):
                    facts = json.loads(row[0])
                    samples = facts.get("observed_model_edge_memory", [])
                    if samples and min(s["free_bytes"] for s in samples) < MIN_HEADROOM:
                        raise BudgetStop("recorded_actual_headroom_failure")
            finally:
                store.close()
    scheduler = LocalScheduler(specs, worlds, branches, TokenizerFactory(CANDIDATE, str(Path(root)/"metadata/4B"), COURSE_LIMITS),
        settings=run["settings"], budget=budget, release_device=lambda *unused:False,
        prior_paths=(tuple(p for p in worker_paths(bundle, "development") if p.exists()) if stage == "main" else ()) +
            (tuple(p for p in worker_paths(bundle,"hardware") if p.exists()) if config.get("resource_policy") == "observe" else ()) + refused_workers(bundle),
        regime="course", report=report)
    stopped = None
    try:
        scheduler.__enter__()
        scheduler.deadline = min(scheduler.deadline, session_deadline)
        if action == "capability":
            scheduler.run(capability_only=True)
        else:
            while scheduler.inflight or any(w.status != "done" for w in scheduler.status()):
                if monotonic()-last_backup >= config.get("backup_every_seconds", 600):
                    while scheduler.inflight:
                        scheduler.advance(dispatch=False)
                    exported = backup_bundle(bundle, Path(bundle).parent/("course-resume.payload" if config.get("resource_policy") == "observe" else "course-resume.zip"))
                    last_backup = monotonic()
                    print("Portable round-boundary backup updated: "+exported["path"], flush=True)
                scheduler.advance()
    except (Exception, KeyboardInterrupt) as error:
        stopped = f"{type(error).__name__}: {error}"
    finally:
        try:
            scheduler.close()
        except WorkerInterrupted:
            pass  # Kaggle provider release is deliberately deferred to a real receipt.
    progress = snapshot(root, bundle, stage, run)
    save(Path(bundle)/"progress.json", progress)
    if stage == "development":
        capability = capability_gate(worlds, branches, paths)
        save(Path(bundle)/"capability-gate.json", capability)
        if capability["status"] == "failed":
            stopped = "capability screen failed; no recovery spending admitted"
    result = dict(action=action, stop_reason=stopped, counts=progress["counts"], provider_release_confirmed=False,
        instruction=("Download course-resume.payload and executed notebook; stop the interactive Kaggle session normally."
            if config.get("resource_policy") == "observe" else
            "Download course-resume.zip and executed notebook; stop the session and retain actual provider release evidence."))
    save(Path(bundle)/"last-execution.json", result)
    return result


def freeze(root, bundle, config):
    authorization = require_authorization(config, "freeze")
    run = bind_candidate(root, bundle, config, verify_environment=False)
    if run["freeze"]:
        return run["freeze"]
    if any(p.exists() for p in worker_paths(bundle, "main")):
        raise ValueError("main records already exist before freeze")
    hardware = hardware_gate(bundle, config.get("hardware_review", {}))
    if not hardware["passed"]:
        raise BudgetStop("hardware_gate_not_passed")
    worlds, branches = scope(root, bundle, "development")
    tokenizer = TokenizerFactory(CANDIDATE, str(Path(root)/"metadata/4B"), COURSE_LIMITS)()
    audit = audit_records(worlds, branches, worker_paths(bundle, "development"), tokenizer, run["settings"])
    pilot = pilot_gate(worlds, branches, worker_paths(bundle, "development"), audit=audit)
    save(Path(bundle)/"pilot-gate.json", pilot)
    if not pilot["passed"]:
        raise BudgetStop("complete_pilot_acceptance_not_passed")
    if not audit["actual_model_evidence"]:
        raise BudgetStop("pilot_rows_lack_actual_finite_fresh_cache_GPU_diagnostics")
    progress = snapshot(root, bundle, "development", run)
    if progress["resources"]["active_devices"] and not (
            config.get("continuous_assignment") and current_assignment(bundle, "development", config)):
        raise BudgetStop("pilot_provider_release_required_before_freeze")
    review = config.get("pilot_review", {})
    if config.get("automatic_pilot_review") and not (
            review.get("family_condition_failures_reviewed") and review.get("timeout_120_seconds_adequate")):
        # A completely clean pilot can be inspected mechanically. Any invalid,
        # failed, uncertain or near-timeout call still needs an explicit review.
        attempts = []
        for path in worker_paths(bundle, "development"):
            with closing(WorkerStore(path, readonly=True)) as store:
                attempts.extend(dict(r) for r in store.connection.execute("SELECT * FROM attempts"))
        clean = (pilot["protocol_valid"] == 1114 and all(r["status"] == "completed"
            and not r["uncertain_completion"] and r["elapsed_seconds"] is not None
            and r["elapsed_seconds"] < .8*BOUNDS["timeout_seconds"] for r in attempts))
        review = dict(family_condition_failures_reviewed=clean, timeout_120_seconds_adequate=clean,
            method="independent raw/effect audit; inspect every family/phase/policy/event group; "
                   "automatic acceptance only with no failures/uncertainty and every attempt below 96 seconds",
            maximum_attempt_seconds=max((r["elapsed_seconds"] or 0 for r in attempts), default=None))
        save(Path(bundle)/"automatic-pilot-review.json", review)
    if config.get("resource_policy") == "observe" and config.get("automatic_pilot_review"):
        review.update(family_condition_failures_reviewed=audit["passed"],timeout_120_seconds_adequate=pilot["passed"],
            method="automatic independent raw/effect audit and complete 98% validity gate; all failure groups retained")
        save(Path(bundle)/"automatic-pilot-review.json",review)
    if not review.get("family_condition_failures_reviewed") or not review.get("timeout_120_seconds_adequate"):
        raise BudgetStop("review_pilot_family_failures_and_120_second_timeout_before_freeze")
    devices = tuple(sorted({d["device"] for d in progress["resources"]["devices"]}))
    forecast = snapshot(root, bundle, "main", run, devices=devices)
    reason, available = course_admission(forecast["resources"], forecast["forecast"], course_budget(run), "main", 2)
    if reason:
        raise BudgetStop(reason)
    # Existing forecast includes slower-device/idle allocation and the 25% margin.
    resources = forecast["resources"]
    freeze_receipt = dict(at=utc_now(), authorization=authorization, hardware=hardware, pilot=pilot, pilot_review=review,
        storage=disk_admission(Path(bundle), "main", complete_forecast=True),
        forecast=forecast["forecast"], resources=resources, planned_devices=list(devices),
        course_admission_lhs_upper_gpu_hours=None if config.get("resource_policy") == "observe" else
            resources["course_gpu_hours"][1]+sum(resources["remaining_reserves_gpu_hours"].values())+forecast["forecast"]["remaining_gpu_hours"][1],
        complete_main_distinct=5752, complete_main_logical=6280,
        provider_session_terms=dict(duration_seconds=config.get("provider_session_seconds"),
            release_instructions=config.get("release_instructions")),
        main_authorization_granted=False)
    run["freeze"] = freeze_receipt
    save(Path(bundle)/"run.json", run)
    return freeze_receipt


def analyze(root, bundle, config):
    from recovery.report import report_run, write_report
    run_path = Path(bundle)/"run.json"
    run = read(run_path) if run_path.exists() else None
    settings = run["settings"] if run else read(preparation_files(root,CANDIDATE)["packet"])["settings"]
    if (Path(bundle)/"hardware/report.json").exists() and all(p.exists() for p in worker_paths(bundle, "hardware")):
        save(Path(bundle)/"hardware-gate.json", hardware_gate(bundle, config.get("hardware_review", {})))
    tokenizer = TokenizerFactory(CANDIDATE, str(Path(root)/"metadata/4B"), COURSE_LIMITS)()
    worlds, branches = scope(root, bundle, "main")
    audit = audit_records(worlds, branches, worker_paths(bundle, "main"), tokenizer, settings)
    save(Path(bundle)/"main-audit.json", audit)
    recorded = audit["coverage"]["recorded"]
    if recorded and not (run and run["freeze"]):
        raise ValueError("main evidence has no accepted frozen configuration")
    if recorded and not audit["actual_model_evidence"]:
        raise ValueError("main raw generations lack actual finite/fresh-cache GPU diagnostics")
    now = config.get("analysis_as_of") or utc_now()
    accounting_context = read(Path(bundle)/"provider-release.json") if (Path(bundle)/"provider-release.json").exists() else None
    # Persist the first analysis clock: subsequent CPU reproductions use it.
    receipt_path = Path(bundle)/"analysis-receipt.json"
    if receipt_path.exists():
        receipt = read(receipt_path)
        if receipt["coverage"] == audit["coverage"] and receipt.get("accounting_context") == accounting_context:
            now = receipt["as_of"]
    evidence = dict(audit_passed=True, committed_schedule_complete=audit["committed_schedule_complete"],
        status="model_complete" if recorded == 6280 and audit["committed_schedule_complete"] else "model_incomplete" if recorded else "feasibility",
        accepted_main_freeze=("run.json; frozen at "+run["freeze"]["at"]) if run and run["freeze"] else None,
        model_capability=read(Path(bundle)/"capability-gate.json")["counts"] if (Path(bundle)/"capability-gate.json").exists() else None,
        gpu_memory_headroom={k:read(Path(bundle)/"hardware-gate.json")[k] for k in ("passed", "actual_minimum_free_bytes", "complete_live_memory_upper_bound_bytes")} if (Path(bundle)/"hardware-gate.json").exists() else None,
        cumulative_allocation=snapshot(root, bundle, "main", run, now=now)["resources"] if run else None,
        source_commit=run["source_commit"] if run else (Path(root)/"SOURCE_COMMIT.txt").read_text().strip())
    name = datetime.fromisoformat(now).astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = Path(bundle)/"analyses"/name
    result = report_run(worlds, branches, worker_paths(bundle, "main"), now=now, seed=AS_OF_SEED,
        tokenizer=tokenizer, regime="course", execution_evidence=evidence,
        provenance=dict(manifest="inputs/population.json", schedule="inputs/schedules.json",
            workers=[p.relative_to(bundle).as_posix() for p in worker_paths(bundle, "main")], stage="main", count=20))
    # Reproduce bytes on two fresh paths, then compare the retained canonical
    # export. No CPU regeneration of raw model replies is permitted.
    with tempfile.TemporaryDirectory() as directory:
        first, second = Path(directory)/"first", Path(directory)/"second"
        write_report(first, result, figures=config.get("figures", True))
        repeated = report_run(worlds, branches, worker_paths(bundle, "main"), now=now, seed=AS_OF_SEED,
            tokenizer=tokenizer, regime="course", execution_evidence=evidence, provenance=result["report"]["provenance"])
        write_report(second, repeated, figures=config.get("figures", True))
        files = [p.relative_to(first) for p in first.rglob("*") if p.is_file()]
        if any((first/p).read_bytes() != (second/p).read_bytes() for p in files):
            raise ValueError("clean offline report reproduction differs")
        if target.exists():
            if any(not (target/p).exists() or (target/p).read_bytes() != (first/p).read_bytes() for p in files):
                raise ValueError("retained report differs; preserve it and use a new derived output for updated evidence")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(first, target)
    if run:
        dev_worlds, dev_branches = scope(root, bundle, "development")
        dev_audit = audit_records(dev_worlds, dev_branches, worker_paths(bundle, "development"), tokenizer, settings)
        save(Path(bundle)/"development-audit.json", dev_audit)
        save(Path(bundle)/"pilot-gate.json", pilot_gate(dev_worlds, dev_branches, worker_paths(bundle, "development"), audit=dev_audit))
    receipt = dict(as_of=now, resampling_seed=AS_OF_SEED, report=(target/"report.html").relative_to(bundle).as_posix(),
        status=evidence["status"], coverage=audit["coverage"], byte_identical_reproductions=2,
        inference_calls=0, external_delivery=False, accounting_context=accounting_context)
    save(receipt_path, receipt)
    return receipt


def run_all(root, bundle, config):
    """Advance the existing gates in order, always finish with retained results."""
    config = dict(config, continuous_assignment=True)
    events, reason, action = [], None, "hardware"
    def record(stage, result):
        events.append(dict(stage=stage, at=utc_now(), result=result))
        save(Path(bundle)/"automatic-run.json", dict(status="running", stages=events))
        backup_bundle(bundle, Path(bundle).parent/("course-resume.payload" if config.get("resource_policy") == "observe" else "course-resume.zip"))
        outcome = result.get("status", "recorded")
        print("Run All: "+stage+" | "+outcome+" | portable evidence updated", flush=True)
    def inference(stage):
        last_count = -1
        while True:
            result = execute(root, bundle, config, stage)
            record(stage, result)
            count = result["counts"]["finished_logical"]
            stop = result.get("stop_reason")
            if not stop:
                return result
            # A scientific/resource failure is terminal for this invocation.
            # Only the runner's conservative time window may be re-admitted
            # in the same still-assigned session, with fresh derived spending.
            if "BudgetStop: allocation_deadline" not in stop or count <= last_count:
                raise BudgetStop(stop)
            last_count = count
    try:
        if config.get("execute_gpu") is not True:
            raise BudgetStop("GPU authorization disabled; limited CPU report only")
        if config.get("resource_policy") != "observe" and config.get("prior_sessions_released") is not True:
            raise BudgetStop("prior_provider_release_unconfirmed")
        session_window(config)
        hardware_report = Path(bundle)/"hardware/report.json"
        resume_hardware = not hardware_report.exists()
        if hardware_report.exists():
            previous = read(hardware_report)
            stop = previous.get("root_blocker") or previous.get("smoke", {}).get("stop_reason")
            if stop:
                # Resume only an interrupted controller window, never a diagnosed
                # provider defect, a final model failure or a failed science gate.
                recoverable = str(stop).startswith(("KeyboardInterrupt:", "BudgetStop: allocation_deadline"))
                paths = worker_paths(bundle,"hardware")
                if recoverable and all(p.exists() for p in paths):
                    plan=Path(bundle)/"hardware/executed-plan.json"
                    hang_ids={row["smoke_call_id"] for row in read(plan).get("rows",[]) if row.get("controlled_hang")} if plan.exists() else set()
                    with ExitStack() as stack:
                        stores = [WorkerStore(p,readonly=True) for p in paths]
                        for store in stores: stack.callback(store.close)
                        recoverable = not any(store.connection.execute(
                            "SELECT 1 FROM attempts WHERE status IN ('blocked','infrastructure_failure') LIMIT 1").fetchone()
                            for store in stores)
                        recoverable &= not any(row["call_id"] not in hang_ids for store in stores
                            for row in store.connection.execute("SELECT call_id FROM calls WHERE status IN ('timeout','infrastructure_failure')"))
                else:
                    recoverable = False
                if not recoverable:
                    raise BudgetStop(str(stop))
                resume_hardware = True
                print("Run All: hardware | resuming original interrupted work",flush=True)
        if resume_hardware:
            result = hardware(root, bundle, config)
            record("hardware", result)
            if result.get("root_blocker") or result.get("smoke", {}).get("stop_reason"):
                terminal = result.get("smoke",{}).get("terminal_failure")
                reason = result.get("root_blocker") or result["smoke"]["stop_reason"]
                if terminal:
                    reason += ": "+terminal["call_id"]+" | "+terminal["reason"]
                raise BudgetStop(reason)
        gate = hardware_gate(bundle, config.get("hardware_review", {}), assignment=config["allocated_at"])
        save(Path(bundle)/"hardware-gate.json", gate)
        if not gate["passed"]:
            raise BudgetStop("complete_hardware_stress_headroom_cache_and_loading_gate_not_passed")
        if not gate["accounting_segment_closed"]:
            record("hardware_to_development", transfer_assignment(bundle, "hardware", "development", config))
        run = bind_candidate(root, bundle, config)
        if not run["freeze"]:
            action = "pilot"
            start_assignment(bundle, "development", config, course_budget(run))
            worlds, branches = scope(root, bundle, "development")
            capability = capability_gate(worlds, branches, worker_paths(bundle, "development"))
            if capability["status"] == "incomplete":
                inference("capability")
                capability = capability_gate(worlds, branches, worker_paths(bundle, "development"))
            save(Path(bundle)/"capability-gate.json", capability)
            if not capability["passed"]:
                raise BudgetStop("first_90_capability_gate_not_passed")
            inference("pilot")
            action = "freeze"
            record("freeze", freeze(root, bundle, config))
            run = read(Path(bundle)/"run.json")
        action = "main"
        require_authorization(config, "main")
        if current_assignment(bundle, "development", config):
            record("development_to_main", transfer_assignment(bundle, "development", "main", config,
                budget=course_budget(run)))
        start_assignment(bundle, "main", config, course_budget(run))
        result = inference("main")
        if result["counts"]["remaining_logical"]:
            raise BudgetStop("fixed_main_schedule_incomplete")
    except (Exception, KeyboardInterrupt) as error:
        reason = f"{type(error).__name__}: {error}"
        save(Path(bundle)/"logs/workflow-error.json",dict(stage=action,exception_type=type(error).__name__,
            reason=str(error),traceback=traceback.format_exc(),at=utc_now()))
        print("Run All stopped at "+action+": "+reason, flush=True)
        try:
            record_refused_allocation(root, bundle, config, "pilot" if action == "freeze" else action, reason)
        except Exception as accounting_error:
            events.append(dict(stage="assignment_accounting", reason=str(accounting_error),
                               assignment_clock=config.get("allocated_at")))
    if config.get("resource_policy") == "observe":
        # Seal measured inference/setup intervals before read-only reporting.
        # Subsequent analysis/export/provider idle is not silently called free;
        # its controller logs survive and unobserved provider time stays unknown.
        end_observations(bundle,through=utc_now())
    # Reporting never invokes a model, and has its own failure receipt. Preserve
    # original evidence even if an audit or provider interruption prevents it.
    analysis = None
    alarm = False
    try:
        if config.get("execute_gpu"):
            run = read(Path(bundle)/"run.json") if (Path(bundle)/"run.json").exists() else None
            budget = course_budget(config,run["budget"] if run else config["budget"])
            if run:
                stage = "main" if run["freeze"] else "development"
                resources = snapshot(root,bundle,stage,run)["resources"]
            else:
                with ExitStack() as stack:
                    stores = [WorkerStore(p,readonly=True) for p in all_workers(bundle)]
                    for store in stores: stack.callback(store.close)
                    resources = smoke_resources(stores,budget,utc_now())
            if config.get("resource_policy") != "observe" and not resources["admission_available"]:
                raise BudgetStop("reporting_on_assigned_GPUs_with_unresolved_resource_bounds")
            hours = config.get("max_work_seconds",36000)/1800 if config.get("resource_policy") == "observe" else resources["remaining_ceiling_gpu_hours"]
            if config.get("resource_policy") != "observe":
                if not run or not run["freeze"]:
                    hours = min(hours,resources["remaining_reserves_gpu_hours"]["development"])
                if not run:
                    hours = min(hours,resources["remaining_smoke_gpu_hours"])
            window = min(session_window(config),hours*3600/2)-budget.shutdown_seconds-30
            if window < 10:
                raise BudgetStop("report_deferred_to_CPU_to_preserve_release_allowance")
            if os.name != "nt":
                import signal
                def stop_report(*unused):
                    raise BudgetStop("report_time_limit; original evidence retained for CPU reproduction")
                signal.signal(signal.SIGALRM,stop_report)
                signal.setitimer(signal.ITIMER_REAL,min(window,config.get("finalization_seconds",900)))
                alarm = True
        analysis = analyze(root, bundle, config)
        record("analysis", analysis)
    except (Exception, KeyboardInterrupt) as error:
        analysis_error = f"{type(error).__name__}: {error}"
        save(Path(bundle)/"logs/analysis-error.json",dict(exception_type=type(error).__name__,
            reason=str(error),traceback=traceback.format_exc(),at=utc_now()))
        events.append(dict(stage="analysis", status="failed", reason=analysis_error))
        reason = reason or analysis_error
    finally:
        if alarm:
            signal.setitimer(signal.ITIMER_REAL,0)
            signal.signal(signal.SIGALRM,signal.SIG_DFL)
    result = dict(action="run_all", status="complete_results" if analysis and
        analysis["status"] == "model_complete" and reason is None else "limited_result",
        reason=reason, analysis=analysis, stages=events, gates_bypassed=False,
        provider_release_confirmed=False,
        instruction=("Download course-resume.payload and course-results.zip; stop the interactive Kaggle session normally. "
                     "Resume with the matching dataset and latest payload; observed time never proves provider deallocation."
                     if config.get("resource_policy") == "observe" else
                     "Download course-resume.zip and course-results.zip. Stop the interactive session and retain actual release evidence."))
    save(Path(bundle)/"automatic-run.json", result)
    return result


def run_qualification(root, bundle, config):
    """Two explicit source-bound bundles; existing pipeline owns every stage."""
    from copy import deepcopy
    from scripts.course_kaggle_bootstrap import qualification_choice
    from scripts.m5_course_smoke_assets import download_weights_stdlib, require_space
    from scripts.m5_course_smoke import check_hardware_plan
    global CANDIDATE
    bundle = Path(bundle)
    summaries = []
    for _ in range(2):
        label, prior = qualification_choice(bundle,config)
        CANDIDATE = course_candidate(label)
        child = bundle/"candidates"/label
        selected = deepcopy(config)
        selected.pop("candidate_order",None)
        selected["candidate"] = label
        selected["budget"].update(prior_smoke_attempts=prior,
            prior_evidence=f"final-online-4 retained 23 original preparation attempts; earlier candidate hardware adds {prior-23} canonical attempts")
        selected["hardware_review"] = read(preparation_files(root,CANDIDATE)["review"])
        initialize(root,child)
        own_assets = child/"asset-receipt.json"
        if own_assets.exists():
            selected["assets_receipt"] = str(own_assets)
        save(child/"operator-config.json",selected)
        if selected.get("execute_gpu"):
            assets = read(selected["assets_receipt"])
            if (assets["model"],assets["revision"]) != (CANDIDATE.model,CANDIDATE.revision):
                # Only the fallback weights change; reuse the verified installed
                # environment. Real native CPU preflight precedes its download.
                tokenizer = TokenizerFactory(CANDIDATE,str(Path(root)/"metadata/4B"),COURSE_LIMITS)()
                packet = read(preparation_files(root,CANDIDATE)["packet"])
                contract = check_hardware_plan(root,packet,tokenizer)
                from tests.generation_checks import check_generation_contract
                contract["generation_contract"] = check_generation_contract(tokenizer,packet["settings"])
                save(child/"environment-receipts/hardware-plan-contract.json",contract)
                require_authorization(selected,"weights")
                from scripts.m5_kaggle_preflight import command
                inspection = read(preparation_files(root,CANDIDATE)["inspection"])
                require_space(Path(selected["hf_cache"]),child,inspection["checkpoint_index"]["total_checkpoint_bytes"]+512*1024**2)
                seconds = min(900, int(session_window(selected))-150)
                if seconds < 1:
                    raise BudgetStop("session_window_exhausted_before_fallback_download")
                receipt = child/"environment-receipts/checkpoint.json"
                command(child/"environment-receipts","stage-fallback-checkpoint",
                    [sys.executable,"-I","-S",Path(root)/"scripts/m5_course_smoke_assets.py","weights",
                     "--root",root,"--manifest",Path(root)/"source-manifest.json","--cache",selected["hf_cache"],
                     "--receipt",receipt,"--stdlib","--range-bytes",str(16*1024**2),"--candidate",label],
                    deadline=monotonic()+seconds+20,timeout=seconds,cwd=child,env=dict(os.environ),stream=True)
                staged = read(receipt)
                assets.update(model=CANDIDATE.model,revision=CANDIDATE.revision,checkpoint_files=staged["checkpoint_files"])
                selected["assets_receipt"] = str(child/"asset-receipt.json")
                save(selected["assets_receipt"],assets)
                save(child/"operator-config.json",selected)
        # Resume the selected fallback's exact asset binding rather than the
        # root setup's first-candidate receipt.
        own_assets = child/"asset-receipt.json"
        if own_assets.exists():
            selected["assets_receipt"] = str(own_assets)
        elif selected.get("assets_receipt"):
            shutil.copyfile(selected["assets_receipt"],own_assets)
            selected["assets_receipt"] = str(own_assets)
        result = run_all(root,child,selected)
        save(child/"last-action.json",result)
        summaries.append(dict(candidate=label,status=result["status"],reason=result.get("reason")))
        # Keep the root's selected model explicit for CPU reporting and resume.
        config["candidate"] = label
        if selected.get("assets_receipt"):
            config["assets_receipt"] = selected["assets_receipt"]
        save(bundle/"operator-config.json",config)
        current_results = child.parent/"course-results.zip"
        if current_results.exists():
            shutil.copyfile(current_results,bundle.parent/"course-results.zip")
        analysis = result.get("analysis")
        if analysis and analysis.get("report"):
            result["report"] = "candidates/"+label+"/"+analysis["report"]
            save(bundle/"analysis-receipt.json",dict(analysis,report=result["report"]))
            result["analysis"] = dict(analysis,report=result["report"])
        physical = 23
        for path in (bundle/"candidates").glob("*/hardware/worker-*.sqlite"):
            with closing(sqlite3.connect(path.resolve().as_uri()+"?mode=ro",uri=True)) as db:
                physical += db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0]
        result.update(selected_candidate=label,candidate_results=summaries,cumulative_preparation_attempts=physical,preparation_attempt_limit=71)
        save(bundle/"last-action.json",result)
        save(bundle/"automatic-run.json",result)
        backup_bundle(bundle,bundle.parent/"course-resume.payload")
        next_label,_ = qualification_choice(bundle,config)
        if next_label == label or not selected.get("execute_gpu"):
            return result
        print("Qualification: retained "+label+" failure; proceeding to the declared "+next_label+" fallback",flush=True)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--action", choices=("run_all", "inspect", "hardware", "capability", "pilot", "freeze", "main", "status", "analyze", "export"), required=True)
    args = parser.parse_args(argv)
    root, bundle = args.root.resolve(), args.bundle.resolve()
    os.environ["MPLBACKEND"] = "Agg"  # Notebook inline backends must not leak into ordinary CPU exports.
    config = read(args.config)
    if config.get("candidate"):
        config["hardware_review"] = read(preparation_files(root,course_candidate(config["candidate"]))["review"])
    global CANDIDATE
    if config.get("candidate"):
        CANDIDATE = course_candidate(config["candidate"])
    result = dict(action=args.action, status="blocked", inference_called=False)
    try:
        if not config.get("candidate_order"):
            initialize(root, bundle)
        if config.get("resource_policy") == "observe":
            end_observations(bundle,current_assignment=config.get("allocated_at"))
        recover_bootstrap_refusals(root,bundle,config)
        confirm_previous_release(bundle, config.get("previous_session_release"))
        if args.action == "run_all":
            result = run_qualification(root,bundle,config) if config.get("candidate_order") else run_all(root, bundle, config)
        elif args.action == "hardware":
            result = hardware(root, bundle, config)
            if result.get("root_blocker"):
                record_refused_allocation(root, bundle, config, args.action, result["root_blocker"])
        elif args.action in ("capability", "pilot", "main"):
            result = execute(root, bundle, config, args.action)
        elif args.action == "freeze":
            result = freeze(root, bundle, config)
        elif args.action == "analyze":
            if config.get("candidate_order"):
                child = bundle/"candidates"/config["candidate"]
                selected = read(child/"operator-config.json") if (child/"operator-config.json").exists() else config
                initialize(root,child)
                result = analyze(root,child,selected)
                result["report"] = "candidates/"+config["candidate"]+"/"+result["report"]
                save(bundle/"analysis-receipt.json",result)
            else:
                result = analyze(root, bundle, config)
        elif args.action in ("inspect", "status"):
            selected_bundle = bundle/"candidates"/config["candidate"] if config.get("candidate_order") else bundle
            run = read(selected_bundle/"run.json") if (selected_bundle/"run.json").exists() else None
            result = {stage:snapshot(root, selected_bundle, stage, run) for stage in ("development", "main")}
            for stage in result:
                print(stage+"\n"+format_status(result[stage]), flush=True)
        elif args.action == "export":
            result = dict(status="exported", gpu_calls=0)
    except (Exception, KeyboardInterrupt) as error:
        result = dict(action=args.action, status="blocked_or_safely_stopped", reason=f"{type(error).__name__}: {error}",
            remaining_outcomes="unknown", gates_bypassed=False)
        save(bundle/"logs/controller-error.json",dict(action=args.action,reason=result["reason"],
            traceback=traceback.format_exc(),at=utc_now()))
        try:
            record_refused_allocation(root, bundle, config, args.action, result["reason"])
        except Exception as accounting_error:
            result["unresolved_assignment_accounting"] = str(accounting_error)
            result["assignment_clock"] = config.get("allocated_at")
    finally:
        save(bundle/"last-action.json", result)
        save(bundle/"actions"/(args.action+"-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")+".json"), result)
        exported = backup_bundle(bundle, bundle.parent/("course-resume.payload" if config.get("resource_policy") == "observe" else "course-resume.zip"))
        brief = {k:result[k] for k in ("action", "status", "passed", "stop_reason", "reason", "counts", "coverage", "report", "instruction") if k in result}
        print(json.dumps(dict(result=brief, export=exported), indent=2), flush=True)
    return 0 if result.get("status") not in ("blocked", "blocked_or_safely_stopped") else 2


if __name__ == "__main__":
    raise SystemExit(main())
