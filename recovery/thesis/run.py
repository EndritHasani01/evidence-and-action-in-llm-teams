"""Study controller: open or restore, admission, readiness, development, gates,
freeze and main execution (specification sections 4 and 6-7).

One canonical SQLite store per study (the unchanged I-01 Store). One resident
model process per GPU (the unchanged I-01 Resident). Raw replies are persisted
before effects; a completed call is never regenerated.
"""

from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import json
import math
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import threading
from time import monotonic

from ..i01.archive import atomic_json, digest
from ..i01.core import canonical, next_agent
from ..i01.policy import outcome_action, outcome_feedback
from ..i01.process import InfrastructureLost, Resident
from ..i01.store import Store
from . import (CELLS, CONFIG_PATH, LOCK_PATH, MODELS, REGIME, SCOPES, SEPARATION_PATH, SOURCE_ROOT,
               WORLDS_PATH, digest_file, load_config)
from . import checkpoint as ckpt
from . import protocol
from .models import Factory, ScriptedFactory, ScriptedTokenizer, load_tokenizer, prepare

EXIT_DONE, EXIT_ERROR, EXIT_STOPPED = 0, 1, 3
SCOPE_RANK = {s: i for i, s in enumerate(SCOPES)}


class Stop(Exception):
    """An expected, recorded stop: time, ceiling, gate, integrity or operator request."""


class WorkerLost(Exception):
    """The resident model process must be (re)loaded before the next call."""


def utc_now():
    return datetime.now(timezone.utc)


def iso(value):
    return value.isoformat()


@dataclass
class Profile:
    name: str = "study"
    scripted: bool = False
    development: tuple = ()
    main_limit: int | None = None
    behaviors: dict = field(default_factory=dict)
    gates_informational: bool = False
    call_timeout: int | None = None
    heartbeat_seconds: int = 60


def profile_for(scope, config, manifest):
    dev = tuple(w["id"] for w in manifest["worlds"] if w["group"] == "development")
    if scope == "rehearsal":
        return Profile("rehearsal", scripted=True, development=dev[:2], main_limit=2, gates_informational=True)
    return Profile("study", development=dev)


def pid_alive(pid):
    if type(pid) is not int or pid <= 0:
        return False
    if os.name == "nt":
        import ctypes
        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            return False
        code = ctypes.c_ulong()
        ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
        ctypes.windll.kernel32.CloseHandle(handle)
        return code.value == 259  # STILL_ACTIVE
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def host_gpus():
    try:
        text = subprocess.check_output(["nvidia-smi", "--query-gpu=index,name,uuid,driver_version,memory.total",
                                        "--format=csv,noheader,nounits"], text=True, timeout=20)
    except (FileNotFoundError, subprocess.SubprocessError):
        return []
    gpus = []
    for line in text.strip().splitlines():
        index, name, uuid, driver, memory = [v.strip() for v in line.split(",")]
        gpus.append(dict(index=int(index), name=name, uuid=uuid, driver=driver, memory_mib=int(memory)))
    return gpus


def source_binding(source, study, profile, source_commit):
    source = Path(source)
    return dict(regime=REGIME, study=study, profile=profile.name, source_commit=source_commit,
                config_sha256=digest_file(source / CONFIG_PATH), worlds_sha256=digest_file(source / WORLDS_PATH),
                runtime_lock_sha256=digest_file(source / LOCK_PATH))


class Controller:
    def __init__(self, run, store, *, source, config, manifest, profile, scope, session, session_start,
                 deadline, scratch, mirror=None, progress=print, clock=utc_now):
        self.run, self.store, self.source = Path(run), store, Path(source)
        self.config, self.manifest, self.profile, self.scope = config, manifest, profile, scope
        self.session, self.session_start, self.deadline = session, session_start, deadline
        self.scratch, self.mirror, self._print, self.clock = Path(scratch), mirror, progress, clock
        self.worlds = {w["id"]: w for w in manifest["worlds"]}
        self.study = store.meta("binding")["study"]
        self.slots = [None, None]
        self.slot_model = None
        self.tokenizers = {}
        self.print_lock = threading.Lock()
        self.checkpoint_lock = threading.Lock()
        self.stop_event = threading.Event()
        self.stop_reason = None
        self.last_checkpoint = monotonic()
        self.counts = self._attempt_counts()
        self.session_calls = 0
        self.pace = None  # worlds finished by the current run_worlds call, for the time-left estimate
        self.call_timeout = profile.call_timeout or config["call_timeout_seconds"]

    # ---------------------------------------------------------------- basics
    def say(self, text):
        with self.print_lock:
            stamp = self.clock().strftime("%H:%M:%S")
            line = f"[{stamp}] {text}"
            self._print(line)
            with (self.run / "progress.log").open("a", encoding="utf-8") as stream:
                stream.write(line + "\n")

    @contextmanager
    def db(self):
        with self.store.lock:
            yield self.store

    def meta(self, key, default=None):
        with self.db() as s:
            return s.meta(key, default)

    def put(self, key, value):
        with self.db() as s:
            s.put_meta(key, value)

    def bind(self, key, value):
        """Write once; a later different value is an integrity error."""
        with self.db() as s:
            saved = s.meta(key)
            if saved is not None and canonical(saved) != canonical(value):
                raise Stop(f"immutable record {key} differs from the saved value")
            if saved is None:
                s.put_meta(key, value)
        return value

    def remaining(self):
        return (self.deadline - self.clock()).total_seconds()

    def stop(self, reason):
        if not self.stop_event.is_set():
            self.stop_reason = reason
            self.stop_event.set()
        raise Stop(reason)

    def require_scope(self, needed):
        if SCOPE_RANK[self.scope] < SCOPE_RANK[needed] and not (needed in ("development", "main") and self.scope == "rehearsal"):
            raise Stop(f"skipped: scope {self.scope} does not include {needed}")

    # ---------------------------------------------------------------- sessions
    def touch_session(self, **extra):
        key = f"session/{self.session}"
        with self.db() as s:
            row = s.db.execute("SELECT evidence FROM sessions WHERE id=?", (key,)).fetchone()
            evidence = json.loads(row[0]) if row else dict(
                session=self.session, start=iso(self.session_start), deadline=iso(self.deadline), scope=self.scope,
                scripted=self.profile.scripted, host=socket.gethostname(), python=sys.version.split()[0],
                gpu=False, closed=False, commands=[])
            evidence.update(extra, last_seen=iso(self.clock()), deadline=iso(self.deadline))
            with s.transaction():
                s.db.execute("INSERT OR REPLACE INTO sessions VALUES (?,?)", (key, canonical(evidence)))
        return evidence

    def sessions(self):
        with self.db() as s:
            return [json.loads(e) for (i, e) in s.db.execute("SELECT id, evidence FROM sessions") if i.startswith("session/")]

    def aggregate_hours(self):
        """2 x wall time of GPU sessions; an unclosed earlier session counts to its deadline."""
        total = 0.0
        for e in self.sessions():
            if not e.get("gpu") or e.get("scripted"):
                continue
            start = datetime.fromisoformat(e["start"])
            if e["session"] == self.session:
                end = self.clock()
            elif e.get("closed"):
                end = datetime.fromisoformat(e["last_seen"])
            else:
                end = datetime.fromisoformat(e["deadline"])
            total += 2 * max(0.0, (end - start).total_seconds()) / 3600
        return total

    def lost_sessions(self):
        return [e["session"] for e in self.sessions()
                if e["session"] != self.session and e.get("gpu") and not e.get("scripted") and not e.get("closed")]

    # ---------------------------------------------------------------- admission
    def _attempt_counts(self):
        counts = {}
        with self.db() as s:
            for stage, contingency, n in s.db.execute(
                    "SELECT stage, contingency, COUNT(*) FROM attempts GROUP BY stage, contingency"):
                counts[(stage, contingency)] = n
        return counts

    def ceiling(self, stage):
        c = self.config["ceilings"]
        if stage in ("readiness", "reload"):
            return c[stage]
        if stage == "development":
            return len(self.profile.development) * c["main_per_model_per_world"] * len(MODELS)
        if stage == "main":
            freeze = self.meta("freeze")
            return 0 if not freeze else freeze["n"] * c["main_per_model_per_world"] * len(freeze["models"])
        raise ValueError("unknown stage")

    def admit(self, call_id, stage):
        with self.db() as s:
            rows = s.db.execute("SELECT number, status FROM attempts WHERE call_id=? ORDER BY number",
                                (call_id,)).fetchall()
            contingency = 0
            if rows:
                if len(rows) >= 2 or rows[-1][1] not in ("interrupted", "lost"):
                    self.stop(f"{call_id}: no durable reply and its single identical retry is used; stop and ask")
                contingency = 1
            if contingency:
                used = sum(n for (st, cg), n in self.counts.items() if cg == 1)
                if used >= self.config["ceilings"]["contingency"]:
                    self.stop("contingency ceiling reached; stop and ask")
            elif self.counts.get((stage, 0), 0) >= self.ceiling(stage):
                self.stop(f"{stage} first-attempt ceiling {self.ceiling(stage)} reached; stop and ask")
            with s.transaction():
                cur = s.db.execute("INSERT INTO attempts(call_id,number,stage,contingency,admitted_at,status) "
                                   "VALUES (?,?,?,?,?,?)", (call_id, len(rows) + 1, stage, contingency,
                                                            iso(self.clock()), "admitted"))
            self.counts[(stage, contingency)] = self.counts.get((stage, contingency), 0) + 1
            return cur.lastrowid

    def mark_attempt(self, attempt, status, evidence):
        with self.db() as s, s.transaction():
            s.db.execute("UPDATE attempts SET status=?, finished_at=?, evidence=? WHERE id=?",
                         (status, iso(self.clock()), canonical(evidence), attempt))

    def reconcile_unfinished(self, status, reason):
        """Attempts admitted by a process that no longer exists can never return."""
        with self.db() as s:
            ids = [i for (i,) in s.db.execute("SELECT id FROM attempts WHERE status='admitted'")]
        for attempt in ids:
            self.mark_attempt(attempt, status, dict(reason=reason, detected_by=self.session))
        return len(ids)

    # ---------------------------------------------------------------- calls
    def check_call_time(self):
        reserve = self.call_timeout + self.config["termination_seconds"] + 60 * self.config["export_reserve_minutes"]
        if self.remaining() < reserve:
            self.stop("time: not enough session time left for one bounded call, termination and export")

    def call(self, slot, call_id, episode, request, stage, model):
        if self.stop_event.is_set():
            raise Stop(self.stop_reason)
        with self.db() as s:
            s.register(call_id, episode, request)
            row = s.call(call_id)
        if row["outcome"] is not None:
            return json.loads(row["outcome"])
        self.check_call_time()
        worker = self.slots[slot]
        if worker is None or worker.process is None or not worker.process.is_alive():
            raise WorkerLost(f"slot {slot} needs a load before {call_id}")
        attempt = self.admit(call_id, stage)
        try:
            outcome = worker.obtain(request, self.call_timeout)
        except InfrastructureLost as error:
            self.mark_attempt(attempt, "interrupted", dict(error.evidence, reason="model process ended without a reply"))
            self.slots[slot] = None
            raise WorkerLost(f"slot {slot} process ended during {call_id}") from error
        outcome = dict(outcome, dispatch=dict(session=self.session, slot=slot, model=model, stage=stage,
                                              attempt=attempt, admitted_remaining_seconds=round(self.remaining())))
        with self.db() as s:
            s.raw(call_id, attempt, outcome)
        self.session_calls += 1
        if outcome.get("termination_pending"):
            try:
                evidence = worker.close()
            except ValueError:
                self.put(f"unconfirmed_termination/{call_id}", dict(session=self.session))
                self.stop("integrity: timed-out model process termination is unconfirmed")
            self.put(f"timeout_termination/{call_id}", evidence)
            self.slots[slot] = None
        elif outcome.get("failure") == "provider_defect":
            self.slots[slot] = None
            failures = self.provider_failures(model, stage)
            limit = dict(readiness=0, reload=0, development=self.config["gates"]["development_provider_failures_max"],
                         main=self.config["gates"]["main_provider_failures_max"])[stage]
            self.say(f"WARNING {model}: provider failure on {call_id} ({failures} in {stage})")
            if failures > limit:
                self.put(f"provider_stop/{model}/{stage}", dict(failures=failures, session=self.session))
                self.stop(f"integrity: {model} exceeded {limit} provider failures in {stage}")
        return outcome

    def provider_failures(self, model, stage):
        with self.db() as s:
            rows = s.db.execute("SELECT evidence FROM attempts WHERE stage=? AND call_id LIKE ? AND status='failed'",
                                (stage, model + "/%")).fetchall()
        return sum(json.loads(e).get("failure") == "provider_defect" for (e,) in rows if e)

    # ---------------------------------------------------------------- models
    def tokenizer(self, model):
        if model not in self.tokenizers:
            if self.profile.scripted:
                self.tokenizers[model] = ScriptedTokenizer()
            else:
                receipt = self.meta(f"assets/{model}")
                if not receipt:
                    raise Stop(f"{model}: verified model files are required first")
                self.tokenizers[model] = load_tokenizer(self.config, model, receipt["snapshot"])
        return self.tokenizers[model]

    def input_limit(self):
        limit = self.meta("input_limit")
        if limit is None:
            raise Stop("CPU checks have not fixed the input limit; run the CPU checks cell first")
        return limit

    def prepare_assets(self, model):
        if self.profile.scripted:
            return
        from .assets import download
        receipt = download(model, self.scratch, self.run / "receipts", weights=True, config=self.config,
                           progress=self.say)
        self.put(f"assets/{model}", dict(receipt, session=self.session))
        self.tokenizers.pop(model, None)

    def factory(self, model, slot):
        if self.profile.scripted:
            return ScriptedFactory(model, tuple(sorted(self.profile.behaviors.get(model, {}).items())))
        receipt = self.meta(f"assets/{model}")
        return Factory(self.config, model, str(slot), receipt["snapshot"], self.input_limit())

    def load_slot(self, slot, model):
        if self.slots[slot] is not None:
            try:
                self.slots[slot].close()
            except ValueError:
                self.stop("integrity: previous model process termination unconfirmed")
        loads = self.meta(f"loads/{self.session}", 0) + 1
        self.put(f"loads/{self.session}", loads)
        reload_calls = sum(n for (st, cg), n in self.counts.items() if st == "reload")
        if self.meta(f"readiness/{model}") and reload_calls >= self.config["ceilings"]["reload"]:
            self.stop("reload readiness ceiling reached; stop and ask")
        worker = Resident(self.factory(model, slot), self.config["termination_seconds"])
        started = monotonic()
        self.say(f"loading {model} on GPU{slot} (load {loads} of this session)")
        try:
            report = worker.load(self.config["load_timeout_seconds"])
        except ValueError as error:
            self.record_load(model, slot, loads, dict(failed=str(error)))
            self.stop(f"integrity: {model} failed to load on GPU{slot}: {error}")
        self.record_load(model, slot, loads, dict(report=report, seconds=round(monotonic() - started, 1)))
        self.slots[slot], self.slot_model = worker, model
        return loads

    def record_load(self, model, slot, number, evidence):
        key = f"load/{self.session}/{model}/gpu-{slot}/{number}"
        with self.db() as s, s.transaction():
            s.db.execute("INSERT OR REPLACE INTO sessions VALUES (?,?)", (key, canonical(dict(evidence, at=iso(self.clock())))))

    def close_slots(self):
        evidence = []
        for slot, worker in enumerate(self.slots):
            if worker is not None:
                try:
                    evidence.append(worker.close())
                except ValueError:
                    self.put(f"unconfirmed_termination/slot-{slot}", dict(session=self.session))
                    evidence.append(dict(termination_confirmed=False))
                self.slots[slot] = None
        self.slot_model = None
        return evidence

    def check_host(self):
        if self.profile.scripted:
            return
        gpus = host_gpus()
        if len(gpus) != 2 or len({g["uuid"] for g in gpus}) != 2 or any("T4" not in g["name"] for g in gpus):
            self.stop("hardware: two distinct T4 GPUs are required for GPU stages")
        self.put(f"host/{self.session}", dict(gpus=gpus))

    # ---------------------------------------------------------------- readiness
    def readiness_request(self, model, probe):
        seed_label = "A" if probe in ("A1", "A2") else probe
        from ..i01.core import seed_for
        seed = seed_for(self.config["master_seed"], model, "readiness", seed_label)
        values = {"A1": [-7, 3], "A2": [-7, 3], "B": [100, -9]}.get(probe, [0, 1])
        return prepare(dict(complete_input=values), seed, self.config, model, self.tokenizer(model),
                       self.input_limit(), control=True, envelope=probe == "envelope")

    def probe_ok(self, outcome, envelope):
        backend = outcome.get("backend") or {}
        cache = backend.get("cache") or {}
        ok = (not outcome.get("failure") and backend.get("finite_score_steps", 0) > 0
              and cache.get("initial_empty") and cache.get("same_call_cache"))
        if envelope:
            ok = ok and outcome.get("generated_tokens") == self.config["output_tokens"] and \
                backend.get("observed_peak_free_lower_bytes", 0) >= self.config["headroom_bytes"]
        return bool(ok)

    def readiness(self, model, slots=(0, 1), *, load_number):
        """First load of a model: A/B/A + envelope per GPU; later loads: envelope only."""
        first = self.meta(f"readiness/{model}") is None
        results, passed = [], True
        for slot in slots:
            probes = ("A1", "B", "A2", "envelope") if first else ("envelope",)
            for probe in probes:
                if first:
                    call_id = f"{model}/readiness/first/gpu-{slot}/{probe}"
                    stage = "readiness"
                else:
                    call_id = f"{model}/readiness/{self.session}-load-{load_number}/gpu-{slot}/{probe}"
                    stage = "reload"
                request = self.readiness_request(model, probe)
                outcome = self.call(slot, call_id, call_id, request, stage, model)
                ok = self.probe_ok(outcome, probe == "envelope")
                passed = passed and ok
                results.append(dict(call=call_id, ok=ok, generated_tokens=outcome.get("generated_tokens"),
                                    free_bytes=(outcome.get("backend") or {}).get("observed_peak_free_lower_bytes"),
                                    token_ids_digest=canonical(outcome.get("token_ids"))[:64]))
                if not ok:
                    break
        receipt = dict(passed=passed, first=first, session=self.session, results=results)
        if first:
            aba = [r["token_ids_digest"] for r in results if r["call"].endswith(("/A1", "/A2"))]
            receipt["aba_equal_for_review"] = [aba[i] == aba[i + 1] for i in range(0, len(aba) - 1, 2)]
            self.put(f"readiness/{model}", receipt)
        else:
            self.put(f"reload/{model}/{self.session}-{load_number}", receipt)
        if not passed:
            self.say(f"{model}: readiness FAILED on this load: {results[-1]}")
        return passed

    # ---------------------------------------------------------------- episodes
    def episode_id(self, model, world, cell):
        return f"{model}/{world['id']}/{cell}"

    def stage_of(self, world):
        return "development" if world["group"] == "development" else "main"

    def run_episode(self, slot, model, world, cell):
        eid = self.episode_id(model, world, cell)
        stage = self.stage_of(world)
        with self.db() as s:
            state = s.state(eid)
        if state is not None and state.get("terminal"):
            return state
        if self.remaining() < 60 * self.config["dispatch_cutoff_minutes"] and state is None:
            self.stop("time: dispatch cutoff reached; no new episode starts")
        if state is None:
            if cell == "prefix":
                start = protocol.start(world, model, "prefix")
            else:
                with self.db() as s:
                    prefix = s.state(self.episode_id(model, world, "prefix"))
                start = protocol.start(world, model, cell, prefix)
            with self.db() as s:
                state = s.start(eid, start)
        while (agent := next_agent(state)) is not None:
            k = state["turns"][agent]
            call_id = f"{eid}/agent-{agent}/invocation-{k}"
            seed = world["seeds"][model]["prefix" if cell == "prefix" else "continuation"][agent][k]
            request = prepare(protocol.view(world, state, agent), seed, self.config, model,
                              self.tokenizer(model), self.input_limit())
            outcome = self.call(slot, call_id, eid, request, stage, model)
            action, error = outcome_action(outcome)
            state = protocol.apply(state, agent, action, error, call_id,
                                   outcome_feedback(outcome) if action is None else None)
            with self.db() as s:
                s.effects(call_id, eid, state)
            self.maybe_checkpoint()
        return state

    def run_control(self, slot, model, world, phase):
        eid = f"{model}/{world['id']}/control-{phase}"
        with self.db() as s:
            state = s.state(eid)
        if state is not None and state.get("terminal"):
            return state
        request = prepare(protocol.control_view(world, phase), world["seeds"][model]["control"][phase],
                          self.config, model, self.tokenizer(model), self.input_limit(), control=True)
        outcome = self.call(slot, eid, eid, request, self.stage_of(world), model)
        action, error = outcome_action(outcome, control=True)
        truth = world[phase + "_truth"]
        result = dict(regime=REGIME, world=world["id"], model=model, cell="control-" + phase,
                      terminal="control_completed", submission=action["submit"] if action else None,
                      error=error, correct=int(action is not None and action["submit"] == truth))
        with self.db() as s:
            s.start(eid, dict(regime=REGIME, world=world["id"], model=model, cell="control-" + phase, terminal=None))
            s.effects(eid, eid, result)
        self.maybe_checkpoint()
        return result

    def world_complete(self, model, world):
        with self.db() as s:
            ids = [self.episode_id(model, world, c) for c in ("prefix",) + tuple(world["order"])]
            ids += [f"{model}/{world['id']}/control-{p}" for p in ("original", "revised")]
            states = [s.state(i) for i in ids]
        return all(st is not None and st.get("terminal") for st in states)

    def run_world(self, slot, model, world):
        started = monotonic()
        prefix = self.run_episode(slot, model, world, "prefix")
        states = {"prefix": prefix}
        for cell in world["order"]:
            states[cell] = self.run_episode(slot, model, world, cell)
        controls = [self.run_control(slot, model, world, p) for p in ("original", "revised")]
        code = dict(both_submitted="B", horizon_exhausted="H", waiting_deadlock="W")
        parts = [f"{c} {code.get(states[c]['terminal'], '?')}" for c in ("prefix",) + CELLS]
        line = f"{world['id']} done on GPU{slot}: " + " . ".join(parts) + f" . {monotonic() - started:.0f} s"
        if world["group"] == "development":
            ys = {c: protocol.score(world, states[c]) for c in states}
            line += " | dev outcomes " + " ".join(f"{c}={ys[c]}" for c in ("prefix",) + CELLS)
            line += f" controls={controls[0]['correct']}{controls[1]['correct']}"
        self.say(line)

    def run_worlds(self, model, ids):
        queue = deque(i for i in ids if not self.world_complete(model, self.worlds[i]))
        lock, errors = threading.Lock(), []
        self.pace = dict(started=monotonic(), done=0, todo=len(queue))

        def worker(slot):
            current = None
            while not self.stop_event.is_set():
                if current is None:
                    with lock:
                        if not queue:
                            return
                        current = queue.popleft()
                try:
                    if self.slots[slot] is None:
                        loads = self.load_slot(slot, model)
                        if not self.readiness(model, (slot,), load_number=loads):
                            self.stop(f"integrity: {model} reload readiness failed on GPU{slot}")
                    self.run_world(slot, model, self.worlds[current])
                    current = None
                    with lock:
                        self.pace["done"] += 1
                except WorkerLost as error:
                    self.say(f"{error}; reloading GPU{slot}")
                    self.slots[slot] = None
                except Stop as error:
                    if not self.stop_event.is_set():
                        self.stop_reason = str(error)
                        self.stop_event.set()
                    return
                except BaseException as error:  # unexpected: stop the stage and keep evidence
                    errors.append(error)
                    if not self.stop_event.is_set():
                        self.stop_reason = f"error: {type(error).__name__}: {error}"
                        self.stop_event.set()
                    return

        threads = [threading.Thread(target=worker, args=(slot,), daemon=True) for slot in (0, 1)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        if errors:
            raise errors[0]
        if self.stop_event.is_set():
            raise Stop(self.stop_reason)

    # ---------------------------------------------------------------- checkpoints
    def maybe_checkpoint(self, force=False, reason="periodic"):
        if not force and monotonic() - self.last_checkpoint < 60 * self.config["checkpoint_minutes"]:
            return None
        with self.checkpoint_lock:
            if not force and monotonic() - self.last_checkpoint < 60 * self.config["checkpoint_minutes"]:
                return None
            self.touch_session()
            receipt = ckpt.export(self.run, self.store, study=self.study, session=self.session, reason=reason,
                                  mirror=self.mirror, progress=self.say)
            self.last_checkpoint = monotonic()
            mirrored = receipt["mirror"]
            note = ("mirror uploaded" if mirrored and mirrored.get("uploaded") else
                    "mirror FAILED" if mirrored else "no mirror configured")
            self.say(f"checkpoint seq {receipt['seq']} ({receipt['bytes'] / 2**20:.1f} MiB, {note}) {receipt['path']}")
            return receipt

    # ---------------------------------------------------------------- heartbeat
    @contextmanager
    def heartbeat(self, label, model_ids):
        done = threading.Event()

        def beat():
            while not done.wait(self.profile.heartbeat_seconds):
                self.say(self.status_line(label, model_ids))

        thread = threading.Thread(target=beat, daemon=True)
        thread.start()
        try:
            yield
        finally:
            done.set()
            thread.join(timeout=2)

    def status_line(self, label, ids):
        model = self.slot_model or "-"
        complete = sum(self.world_complete(model, self.worlds[i]) for i in ids) if model != "-" else 0
        attempts = sum(self.counts.values())
        contingency = sum(n for (st, cg), n in self.counts.items() if cg == 1)
        left = timedelta(seconds=max(0, int(self.remaining())))
        pace, estimate = self.pace, ""
        if pace and pace["done"] >= 2:  # measured in this session; never shown before two worlds finish
            seconds = (monotonic() - pace["started"]) / pace["done"] * (pace["todo"] - pace["done"])
            estimate = f" . about {timedelta(seconds=int(seconds))} left for {model} at this session's measured pace"
        return (f"{label} {model} . worlds {complete}/{len(ids)} complete . calls this session {self.session_calls} . "
                f"attempts {attempts} (contingency {contingency}/{self.config['ceilings']['contingency']}) . "
                f"aggregate GPU-h {self.aggregate_hours():.1f}/{self.config['ceilings']['aggregate_gpu_hours']} . "
                f"deadline in {left}{estimate}")

    # ---------------------------------------------------------------- stages
    def require_checks(self):
        checks = self.meta("checks")
        if not checks or not checks.get("passed") or checks.get("binding") != self.store.meta("binding"):
            raise Stop("CPU checks have not passed for this source; run the CPU checks cell first")

    def guard_gpu_stage(self):
        if self.aggregate_hours() >= self.config["ceilings"]["aggregate_gpu_hours"]:
            raise Stop("aggregate GPU-hour ceiling reached; stop and ask")
        lost = self.lost_sessions()
        if len(lost) > self.config["ceilings"]["lost_sessions"]:
            raise Stop(f"more than {self.config['ceilings']['lost_sessions']} lost GPU sessions ({lost}); stop and ask")
        if any(k.startswith("unconfirmed_termination/") for k in self.meta_keys()):
            raise Stop("integrity: an earlier model process termination is unconfirmed")

    def meta_keys(self):
        with self.db() as s:
            return [k for (k,) in s.db.execute("SELECT key FROM meta")]

    def develop(self):
        self.require_scope("development")
        self.require_checks()
        if self.meta("freeze"):
            self.say("development: complete (the study is frozen; no development calls remain)")
            return self.meta("gate_report")
        if self.gate_report() is not None:
            self.say("development: complete for both models")
            self.print_gate_report(self.meta("gate_report"))
            return self.meta("gate_report")
        self.guard_gpu_stage()
        self.check_host()
        for model in MODELS:
            if self.meta(f"gates/{model}") is not None:
                self.say(f"development {model}: already complete")
                continue
            self.prepare_assets(model)
            loads = None
            try:
                for slot in (0, 1):
                    loads = self.load_slot(slot, model)
                readiness_done = self.meta(f"readiness/{model}") is not None
                if not self.readiness(model, (0, 1), load_number=loads):
                    if not readiness_done:
                        self.bind(f"gates/{model}", self.gate_record(model, readiness_failed=True))
                        self.say(f"development {model}: first-load readiness failed; G1 fails, model excluded")
                        continue
                    self.stop(f"integrity: {model} reload readiness failed")
                with self.heartbeat("DEVELOPMENT", self.profile.development):
                    self.run_worlds(model, self.profile.development)
            finally:
                self.close_slots()
            record = self.gate_record(model)
            if record is not None:
                self.bind(f"gates/{model}", record)
                self.say(f"development {model}: complete; admitted={record['admitted']}")
        report = self.gate_report()
        if report:
            self.print_gate_report(report)
        return report

    def gate_record(self, model, readiness_failed=False):
        gates = self.config["gates"]
        dev = [self.worlds[i] for i in self.profile.development]
        if readiness_failed:
            return dict(model=model, complete=False, admitted=False, G1=dict(passed=False, reason="first-load readiness failed"),
                        g_seconds=None, informational=self.profile.gates_informational)
        if not all(self.world_complete(model, w) for w in dev):
            return None
        with self.db() as s:
            controls = [s.state(f"{model}/{w['id']}/control-{p}")["correct"] for w in dev for p in ("original", "revised")]
            prefixes = [(w, s.state(self.episode_id(model, w, "prefix"))) for w in dev]
            prefix_calls = s.db.execute("SELECT outcome FROM calls WHERE id LIKE ? AND outcome IS NOT NULL",
                                        (f"{model}/dev-%/prefix/%",)).fetchall()
        legal = sum(outcome_action(json.loads(o))[0] is not None for (o,) in prefix_calls)
        failures = self.provider_failures(model, "development")
        readiness = self.meta(f"readiness/{model}") or {}
        unconfirmed = any(k.startswith("unconfirmed_termination/") for k in self.meta_keys())
        g1 = dict(passed=bool(readiness.get("passed")) and failures <= gates["development_provider_failures_max"]
                  and not unconfirmed, readiness=readiness.get("passed"), provider_failures=failures,
                  unconfirmed_termination=unconfirmed)
        n = len(dev)
        scale = n / 16
        g2 = dict(correct=sum(controls), total=2 * n, minimum=math.ceil(gates["controls_min"] * scale - 1e-9))
        g2["passed"] = g2["correct"] >= g2["minimum"]
        g3 = dict(legal=legal, total=len(prefix_calls), fraction=round(legal / max(1, len(prefix_calls)), 4),
                  minimum=gates["legal_fraction_min"])
        g3["passed"] = g3["fraction"] >= gates["legal_fraction_min"]
        g4 = dict(correct=sum(protocol.score(w, st) == 1 for w, st in prefixes), total=n,
                  minimum=math.ceil(gates["original_min"] * scale - 1e-9))
        g4["passed"] = g4["correct"] >= g4["minimum"]
        passed = all(g["passed"] for g in (g1, g2, g3, g4))
        return dict(model=model, complete=True, G1=g1, G2=g2, G3=g3, G4=g4, passed=passed,
                    admitted=passed or self.profile.gates_informational,
                    informational=self.profile.gates_informational, g_seconds=self.throughput(model),
                    development_outcomes=self.development_outcomes(model))

    def throughput(self, model):
        with self.db() as s:
            rows = s.db.execute("SELECT admitted_at, finished_at, evidence FROM attempts WHERE stage='development' "
                                "AND call_id LIKE ? AND finished_at IS NOT NULL", (model + "/%",)).fetchall()
        spans = {}
        for admitted, finished, evidence in rows:
            session = json.loads(evidence).get("dispatch", {}).get("session") if evidence else None
            a, f = datetime.fromisoformat(admitted), datetime.fromisoformat(finished)
            lo, hi = spans.get(session, (a, f))
            spans[session] = (min(lo, a), max(hi, f))
        if not rows:
            return None
        return round(2 * sum((hi - lo).total_seconds() for lo, hi in spans.values()) / len(rows), 3)

    def development_outcomes(self, model):
        result = {}
        with self.db() as s:
            for cell in ("prefix",) + tuple(protocol.CELLS):
                ys = [protocol.score(self.worlds[i], s.state(f"{model}/{i}/{cell}")) for i in self.profile.development]
                result[cell] = dict(success=sum(y == 1 for y in ys), total=len(ys))
        return result

    def gate_report(self):
        records = {m: self.meta(f"gates/{m}") for m in MODELS}
        if any(r is None for r in records.values()):
            return None
        core = dict(regime=REGIME, study=self.study, profile=self.profile.name,
                    models={m: {k: v for k, v in r.items()} for m, r in records.items()})
        report_id = "dev-" + digest_bytes_canon(core)[:12]
        report = dict(core, id=report_id)
        saved = self.meta("gate_report")
        if saved is None:
            self.put("gate_report", report)
        elif saved["id"] != report_id:
            raise Stop("integrity: the gate report differs from its saved version")
        atomic_json(self.run / "receipts" / "gate-report.json", dict(report, forecast=self.forecast()))
        return report

    def forecast(self):
        records = {m: self.meta(f"gates/{m}") for m in MODELS}
        admitted = [m for m, r in records.items() if r and r.get("admitted")]
        g = [records[m]["g_seconds"] or 0 for m in admitted]
        fc = self.config["forecast"]
        spent = self.aggregate_hours()
        result = dict(spent_hours=round(spent, 2), admitted=admitted, g_seconds={m: records[m]["g_seconds"] for m in admitted})
        n = self.config["main_worlds"]
        per = (self.config["ceilings"]["main_per_model_per_world"] * n * sum(g) +
               self.config["ceilings"]["contingency"] * (max(g) if g else 0))
        result[f"F{n}"] = round(spent + fc["fixed_hours"] + fc["margin"] * per / 3600, 2)
        # No fallback main size: above the ceiling the campaign stops and asks.
        result["chosen_n"] = n if result[f"F{n}"] <= self.config["ceilings"]["aggregate_gpu_hours"] else None
        if self.profile.main_limit and result["chosen_n"]:
            result["chosen_n"] = min(result["chosen_n"], self.profile.main_limit)
        return result

    def print_gate_report(self, report):
        self.say("DEVELOPMENT GATE REPORT  id=" + report["id"] +
                 ("  (rehearsal: informational only)" if self.profile.gates_informational else
                  "  -> paste into MAIN_AUTHORIZATION to authorize main"))
        for m in MODELS:
            r = report["models"][m]
            if not r.get("complete"):
                self.say(f"  {m:8s} G1 FAIL ({r['G1'].get('reason')}) -> excluded")
                continue
            self.say(f"  {m:8s} G1 {'pass' if r['G1']['passed'] else 'FAIL'}  "
                     f"G2 {r['G2']['correct']}/{r['G2']['total']}  G3 {r['G3']['fraction']:.1%}  "
                     f"G4 {r['G4']['correct']}/{r['G4']['total']}  -> {'admitted' if r['admitted'] else 'excluded'}  "
                     f"g={r['g_seconds']} s/call")
            outcomes = r["development_outcomes"]
            self.say("           development outcomes (descriptive): " +
                     " ".join(f"{c} {outcomes[c]['success']}/{outcomes[c]['total']}"
                              for c in ("prefix",) + CELLS if c in outcomes))
        f = self.forecast()
        n = self.config["main_worlds"]
        self.say(f"  forecast: spent {f['spent_hours']} h; F({n})={f[f'F{n}']} h; "
                 f"main size if frozen now: {f['chosen_n']}")

    def freeze(self, authorization):
        self.require_scope("main")
        report = self.meta("gate_report")
        if report is None:
            raise Stop("development is incomplete; no gate report exists")
        saved = self.meta("freeze")
        if saved:
            if saved["authorization"] != authorization:
                raise Stop("the study is already frozen under a different authorization")
            self.say(f"frozen: {saved['n']} worlds for {', '.join(saved['models'])} (authorization {saved['authorization']})")
            return saved
        if authorization != report["id"]:
            raise Stop(f"MAIN_AUTHORIZATION {authorization!r} does not match the gate report {report['id']}")
        forecast = self.forecast()
        if not forecast["admitted"]:
            raise Stop("no model passed the development gates; feasibility report only, no main")
        if forecast["chosen_n"] is None:
            raise Stop("the forecast exceeds the aggregate GPU-hour ceiling; stop and ask")
        n = forecast["chosen_n"]
        ids = [w["id"] for w in self.manifest["worlds"] if w["group"] == "main" and w["index"] < n]
        record = dict(authorization=authorization, gate_report=report["id"], models=forecast["admitted"], n=n,
                      worlds=ids, input_limit=self.input_limit(), binding=self.store.meta("binding"),
                      assets={m: (self.meta(f"assets/{m}") or {}).get("files") for m in forecast["admitted"]},
                      templates=(self.meta("checks") or {}).get("templates"), forecast=forecast,
                      at=iso(self.clock()), session=self.session)
        self.bind("freeze", record)
        self.say(f"FROZEN: {n} main worlds for {', '.join(record['models'])}; main ceiling {self.ceiling('main')} first attempts")
        return record

    def main(self):
        self.require_scope("main")
        self.require_checks()
        freeze = self.meta("freeze")
        if not freeze:
            raise Stop("main is not authorized or not frozen")
        if freeze["binding"] != self.store.meta("binding") or freeze["input_limit"] != self.input_limit():
            raise Stop("integrity: frozen settings differ from this session")
        self.guard_gpu_stage()
        self.check_host()
        for model in freeze["models"]:
            if self.meta(f"provider_stop/{model}/main"):
                self.say(f"main {model}: stopped earlier by the provider-failure rule; skipped")
                continue
            if all(self.world_complete(model, self.worlds[i]) for i in freeze["worlds"]):
                self.say(f"main {model}: complete")
                continue
            self.prepare_assets(model)
            if not self.profile.scripted and (self.meta(f"assets/{model}") or {}).get("files") != freeze["assets"][model]:
                raise Stop(f"integrity: {model} files differ from the frozen files")
            try:
                for slot in (0, 1):
                    loads = self.load_slot(slot, model)
                if not self.readiness(model, (0, 1), load_number=loads):
                    self.stop(f"integrity: {model} readiness failed on this load")
                with self.heartbeat("MAIN", freeze["worlds"]):
                    self.run_worlds(model, freeze["worlds"])
            except Stop as stop:
                if not self.stop_reason or not self.stop_reason.startswith(f"integrity: {model} exceeded"):
                    raise
                self.say(f"main {model}: {stop}; continuing with the next model")
                self.stop_event.clear()
                self.stop_reason = None
            finally:
                self.close_slots()
            self.say(f"main {model}: {'complete' if all(self.world_complete(model, self.worlds[i]) for i in freeze['worlds']) else 'incomplete'}")
        return self.main_status()

    def main_status(self):
        freeze = self.meta("freeze")
        if not freeze:
            return None
        return {m: dict(complete=sum(self.world_complete(m, self.worlds[i]) for i in freeze["worlds"]),
                        intended=len(freeze["worlds"])) for m in freeze["models"]}

    def declare_stopped(self, reason):
        if not reason.strip():
            raise Stop("a reason is required")
        return self.bind("declared_stopped", dict(reason=reason, at=iso(self.clock()), session=self.session))


def digest_bytes_canon(value):
    import hashlib
    return hashlib.sha256(canonical(value).encode()).hexdigest()


# ---------------------------------------------------------------- opening
class Ownership:
    def __init__(self, run, session, command):
        self.path = Path(run) / "lock.json"
        if self.path.exists():
            try:
                held = json.loads(self.path.read_text(encoding="utf-8"))
            except ValueError:
                held = {}
            if held.get("host") == socket.gethostname() and pid_alive(held.get("pid")) and held.get("pid") != os.getpid():
                raise Stop(f"another process (pid {held.get('pid')}, command {held.get('command')}) owns this study; "
                           "wait for it or use stop_running()")
            self.previous = held
        else:
            self.previous = None
        atomic_json(self.path, dict(pid=os.getpid(), host=socket.gethostname(), session=session, command=command,
                                    since=iso(utc_now())))

    def close(self):
        try:
            held = json.loads(self.path.read_text(encoding="utf-8"))
            if held.get("pid") == os.getpid():
                self.path.unlink()
        except (OSError, ValueError):
            pass


def open_controller(run, *, study, source=None, source_commit, scope, session, session_start, deadline,
                    scratch, start_new=False, roots=(), mirror=None, command="open", progress=print,
                    clock=utc_now, profile=None, restore_allowed=True):
    """Open the local study, restore the newest checkpoint, or create a new study."""
    if scope not in SCOPES:
        raise Stop(f"unknown scope {scope}")
    source = Path(source or SOURCE_ROOT)
    run = Path(run)
    run.mkdir(parents=True, exist_ok=True)
    config = load_config(source)
    from .worlds import load_manifest
    manifest, _ = load_manifest(source)
    profile = profile or profile_for(scope, config, manifest)
    if (scope == "rehearsal") != study.endswith("-rehearsal"):
        raise Stop("rehearsal studies must be named <STUDY_ID>-rehearsal and real studies must not")
    binding = source_binding(source, study, profile, source_commit)
    ownership = Ownership(run, session, command)
    restored = None
    try:
        db_path = run / "study.sqlite"
        candidates = ckpt.find(study, [r for r in roots if Path(r).resolve() != (run / "checkpoints").resolve()], mirror)
        local_seq = None
        if db_path.exists():
            try:
                store = Store(db_path, binding)
            except ValueError as error:
                raise Stop(f"this run directory belongs to different source/config/inputs ({error}); "
                           "reports can still be built read-only") from error
            local_seq = store.meta("checkpoint_seq", 0)
            newer = [c for c in candidates if c["seq"] > local_seq]
            if newer:
                store.close()
                raise Stop(f"a newer checkpoint (seq {max(c['seq'] for c in newer)}) exists than this local study "
                           f"(seq {local_seq}); move the local run directory aside explicitly before restoring")
        elif candidates and restore_allowed:
            chosen = ckpt.select(candidates)
            path = Path(chosen["location"])
            if chosen["origin"] == "mirror":
                path = mirror.fetch(chosen["location"], run / ".mirror-download")
            manifest_ckpt = ckpt.verify(path)
            if manifest_ckpt["binding"] != binding:
                raise Stop("the newest checkpoint was made with a different source/config/inputs; "
                           "use the matching SOURCE_COMMIT (reports can still be built read-only)")
            # A running session exports at least every checkpoint interval. A recent checkpoint from a
            # session that has not finished may mean a concurrent writer on another host.
            written = datetime.fromisoformat(manifest_ckpt["created_at"])
            quiet = written + timedelta(minutes=config["checkpoint_minutes"] + 10)
            if manifest_ckpt["session"] != session and manifest_ckpt.get("session_closed") is not True and clock() < quiet:
                raise Stop(f"the newest checkpoint (seq {manifest_ckpt['seq']}) was written at {written:%H:%M} UTC by "
                           f"session {manifest_ckpt['session'][:8]}, which has not finished; another session may still "
                           f"be running this study. Stop it (or let it finish), or run this cell again after "
                           f"{quiet:%H:%M} UTC")
            ckpt.restore(path, run)
            store = Store(db_path, binding)
            store.put_meta("checkpoint_seq", manifest_ckpt["seq"])
            restored = dict(seq=manifest_ckpt["seq"], session=manifest_ckpt["session"], location=chosen["location"])
        elif start_new and restore_allowed:
            store = Store(db_path, binding, create=True)
            inputs = run / "inputs"
            inputs.mkdir(exist_ok=True)
            for rel in (CONFIG_PATH, WORLDS_PATH, SEPARATION_PATH):
                shutil.copy2(source / rel, inputs / Path(rel).name)
            store.put_meta("created", dict(at=iso(clock()), session=session, source_commit=source_commit))
        else:
            raise Stop("no study or checkpoint found: attach the latest checkpoint (or configure the mirror), "
                       "or set START_NEW_STUDY=True for the very first run")
    except BaseException:
        ownership.close()
        raise
    ctl = Controller(run, store, source=source, config=config, manifest=manifest, profile=profile, scope=scope,
                     session=session, session_start=session_start, deadline=deadline, scratch=scratch,
                     mirror=mirror, progress=progress, clock=clock)
    ctl.ownership = ownership
    stale = ownership.previous is not None
    status = "interrupted" if stale and ownership.previous.get("session") == session else "lost"
    n = ctl.reconcile_unfinished(status, "process or session ended before a durable reply")
    if n:
        ctl.say(f"{n} admitted attempt(s) without a durable reply marked {status}; each may be retried once")
    if restored:
        ctl.say(f"restored checkpoint seq {restored['seq']} from {restored['location']}")
        ctl.put(f"restored/{session}", restored)
    gpu_scope = scope in ("development", "main") and not profile.scripted
    previous = ctl.touch_session()
    ctl.touch_session(commands=[*previous.get("commands", []), command], gpu=previous.get("gpu") or gpu_scope)
    return ctl


def close_controller(ctl):
    try:
        ctl.close_slots()
        ctl.touch_session()
    finally:
        ctl.store.close()
        ctl.ownership.close()


def install_stop_handler(ctl):
    def handler(signum, frame):
        ctl.stop_reason = "operator stop request"
        ctl.stop_event.set()
    for name in ("SIGTERM", "SIGINT", "SIGBREAK"):
        if hasattr(signal, name):
            try:
                signal.signal(getattr(signal, name), handler)
            except ValueError:
                pass
