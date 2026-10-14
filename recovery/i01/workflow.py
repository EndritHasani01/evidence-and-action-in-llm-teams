"""Finite operator stages. No successful stage automatically starts another."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import threading
from time import monotonic
import uuid
import tempfile
import traceback

from .archive import atomic_json, digest, export, extract_selected, inventory
from .core import (apply_outcome, canonical, initial_episode, manifests, messages,
                   next_agent, permitted_view, seed_for, validate_action)
from .store import Admission, Store, utc


def source_files(root):
    root = Path(root)
    files = list((root/"recovery").rglob("*.py"))
    files += [root/"configs/i01-course.json", root/"configs/i01-runtime.lock", root/"pyproject.toml"]
    return {p.relative_to(root).as_posix():digest(p) for p in sorted(files) if p.is_file()}


def initialize(run, source, config):
    run=Path(run)
    if (run/'run.json').exists():
        manifest=_initialize(run,source,config)
        for slot in range(2): Store.validate(run/f'worker-{slot}.sqlite',{'manifest':manifest})
        return manifest
    if run.exists() and any(run.iterdir()): raise ValueError('fresh run directory required')
    run.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='i01-initialize-',dir=run.parent) as name:
        staging=Path(name)/'study'
        manifest=_initialize(staging,source,config)
        if run.exists(): run.rmdir()  # Only the previously checked empty destination.
        staging.replace(run)
    return manifest


def _initialize(run, source, config):
    run, source = Path(run), Path(source)
    if config != json.loads((source/"configs/i01-course.json").read_text()):
        raise ValueError("configuration differs from adopted release")
    if (run/"run.json").exists():
        old = json.loads((run/"run.json").read_text())
        if old["config"] != config or old["source_identity"] != source_files(source):
            raise ValueError("existing study differs; do not overwrite")
        return old
    if run.exists() and any(run.iterdir()):
        raise ValueError("fresh run directory required")
    run.mkdir(parents=True, exist_ok=True)
    manifest = dict(manifests(config), study_id=str(uuid.uuid4()), created_at=utc(),
                    source_identity=source_files(source))
    for relative in manifest["source_identity"]:
        target = run/"source"/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source/relative, target)
    for relative in ("docs/I01_KAGGLE.md", "PROJECT_SPECIFICATION.md", "scripts/i01_course.py",
                     "scripts/build_i01_course_notebook.py", "notebooks/i01_course_kaggle.ipynb"):
        if (source/relative).exists():
            target = run/"source"/relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source/relative,target)
    for p in list(source.glob("*.whl"))+list(source.glob("source-release.json")):
        shutil.copy2(p,run/"source"/p.name)
    release_path=source/"source-release.json"
    if release_path.exists():
        release=json.loads(release_path.read_text())
        for relative,wanted in release["files"].items():
            rel=Path(relative)
            if rel.is_absolute() or ".." in rel.parts:
                raise ValueError("unsafe source-release member")
            original=source/rel
            if original.stat().st_size!=wanted["bytes"] or digest(original)!=wanted["sha256"]:
                raise ValueError("exact source-release member differs: "+relative)
            target=run/"source"/rel; target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(original,target)
    atomic_json(run/"run.json", manifest)
    binding = {"manifest":manifest}
    for slot in range(2):
        Store(run/f"worker-{slot}.sqlite",binding,create=True).close()
    return manifest


class Ownership:
    """OS file lock survives cell reruns and releases on actual owner exit."""
    def __init__(self, path):
        self.stream = open(path, "a+b")
        self.stream.seek(0)
        if os.name == "nt":
            import msvcrt
            if self.stream.read(1) == b"":
                self.stream.write(b"0")
                self.stream.flush()
            self.stream.seek(0)
            msvcrt.locking(self.stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(self.stream, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def close(self):
        self.stream.close()


class Session:
    def __init__(self, run, source=None, *, providers=None, prepare_request=None, progress=None):
        self.run = Path(run)
        self.manifest = json.loads((self.run/"run.json").read_text())
        if source is not None and self.manifest["source_identity"] != source_files(source):
            raise ValueError("source differs; reporting remains available read-only")
        self.config = self.manifest["config"]
        binding={'manifest':self.manifest}
        for slot in range(2): Store.validate(self.run/f'worker-{slot}.sqlite',binding)
        self.ownership = Ownership(self.run/"controller.lock")
        self.stores=[]
        try:
            for slot in range(2): self.stores.append(Store(self.run/f'worker-{slot}.sqlite',binding))
        except BaseException:
            for store in self.stores: store.close()
            self.ownership.close()
            raise
        self.admission = Admission(self.stores)
        self.workers = providers or [None, None]
        self.prepare_request = prepare_request
        self.progress = progress or (lambda event: None)
        self.pause = threading.Event()
        self.action_lock = threading.RLock()
        self.checkpoint_lock = threading.RLock()
        self.quiescence = threading.Condition()
        self.active_calls = set()
        self.snapshot_requested = False
        self.last_checkpoint = monotonic()
        self.session_id = str(uuid.uuid4())
        self.tokenizer = None
        self.emit("session", study=self.manifest["study_id"], session=self.session_id)

    @property
    def meta(self):
        return self.stores[0]

    def emit(self, kind, **values):
        self.progress(dict(kind=kind, at=utc(), **values))

    def require(self, key):
        if not self.meta.meta(key):
            raise ValueError("prerequisite missing: " + key)

    def window(self, deadline, evidence):
        value = datetime.fromisoformat(deadline)
        if value.tzinfo is None or value <= datetime.now(timezone.utc) or not evidence.strip():
            raise ValueError("actual future session deadline and operator allowance evidence required")
        previous=self.meta.meta("window",{})
        observed_start=previous.get("observed_start") if previous.get("session")==self.session_id else utc()
        self.meta.put_meta("window", dict(deadline=deadline, evidence=evidence, observed_start=observed_start, session=self.session_id))
        return self.meta.meta("window")

    def remaining_time(self):
        w = self.meta.meta("window")
        if not w or w["session"] != self.session_id:
            return None
        return (datetime.fromisoformat(w["deadline"])-datetime.now(timezone.utc)).total_seconds()

    def status(self):
        from .report import analysis
        s = analysis(self.run)["summary"]
        return dict(s, study_id=self.manifest['study_id'],run_dir=str(self.run),usage=self.admission.usage(), session=self.session_id, remaining_session_seconds=self.remaining_time(),
                    models=[dict(resident=w is not None and getattr(w,"process",None) is not None and w.process.is_alive() and not getattr(w,'unconfirmed',False),
                                 termination_unconfirmed=getattr(w,'unconfirmed',False),
                                 load_report=getattr(w,"load_report",None)) for w in self.workers],
                    observed_idle_allocation_note="Observed session time is separate from provider assignment/release; those may be unknown.")

    def selfcheck(self, metadata_path=None):
        from .checks import run_checks
        receipt = run_checks(metadata_path, self.config)
        atomic_json(self.run/"receipts/selfcheck.json", receipt)
        # Native check is mandatory on Kaggle, development-only scripted receipt is insufficient.
        if receipt["passed"] and receipt["native_tokenizer"]:
            self.meta.put_meta("selfcheck", receipt)
        return receipt

    def load(self, snapshot, host):
        self.require("selfcheck")
        from .setup import runtime_inventory
        runtime_inventory(self.run/"source")
        if any(r["status"]=="admitted" for s in self.stores for r in s.rows("attempts")):
            raise ValueError("reconcile prior admitted attempts and confirm old process exit before loading replacements")
        for s in self.stores:
            for c in s.rows("calls"):
                if c["outcome"] and json.loads(c["outcome"]).get("termination_pending") and not s.meta("timeout_termination/"+c["id"],{}).get("termination_confirmed"):
                    raise ValueError("prior timeout termination must be confirmed before replacement loading")
        if self.remaining_time() is None or self.remaining_time() < 600 + self.config["export_reserve_seconds"]:
            raise ValueError("set current observed session deadline before load")
        from .inference import ModelFactory
        from .process import Resident
        from transformers import AutoTokenizer
        if len(host.get("gpus",[])) != 2 or len({g["uuid"] for g in host["gpus"]}) != 2 or any("T4" not in g["name"] for g in host["gpus"]):
            raise ValueError("two distinct actual T4s required")
        self.tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True, trust_remote_code=False)
        reports = []
        replacing = self.meta.meta("loaded_session") is not None and any(w is None or getattr(w,"process",None) is None for w in self.workers)
        try:
            for slot in range(2):
                if self.remaining_time()<self.config["load_timeout_seconds"]+2*self.config["termination_seconds"]+self.config["export_reserve_seconds"]:
                    raise ValueError("insufficient session time for next bounded load and export")
                if self.workers[slot] is None:
                    self.workers[slot] = Resident(ModelFactory(self.config,str(slot),str(snapshot)),self.config["termination_seconds"])
                prior_process=self.workers[slot].process
                already_resident=prior_process is not None and prior_process.is_alive()
                reports.append(self.workers[slot].load(self.config["load_timeout_seconds"]))
                actual=reports[-1]["cuda_device_uuid"].lower().removeprefix("gpu-")
                expected=host["gpus"][slot]["uuid"].lower().removeprefix("gpu-")
                if actual!=expected:
                    raise ValueError("resident replica UUID differs from selected physical T4 slot")
                if not already_resident:
                    evidence = dict(slot=slot, host=host, load=reports[-1], session=self.session_id,
                                    controller_pid=os.getpid(),window=self.meta.meta("window"))
                    n=sum(json.loads(r["evidence"]).get("session")==self.session_id for r in self.stores[slot].rows("sessions"))
                    with self.stores[slot].transaction():
                        load_id=f"{self.session_id}/load-{n}"
                        self.stores[slot].db.execute("INSERT INTO sessions VALUES (?,?)",(load_id,canonical(evidence)))
                        self.stores[slot].db.execute("INSERT OR REPLACE INTO meta VALUES (?,?)",('resident_load',canonical(load_id)))
        except BaseException as error:
            w=self.workers[slot]
            if w is not None:
                value=dict(session=self.session_id,slot=slot,host=host,load_failure=str(error),
                           load_seconds=getattr(w,"load_seconds",None),termination=getattr(w,"last_stop",None))
                n=len(self.stores[slot].rows("sessions"))
                with self.stores[slot].transaction():
                    self.stores[slot].db.execute("INSERT INTO sessions VALUES (?,?)",(f"{self.session_id}/load-failure-{n}",canonical(value)))
            self.close_models()
            raise
        self.meta.put_meta("loaded_session", self.session_id)
        if replacing and self.meta.meta("envelope"):
            self.meta.put_meta("reload_required",True)
        return reports

    def request(self, view, seed, mode, **flags):
        if self.prepare_request:
            return self.prepare_request(view, seed, mode, **flags)
        from .inference import prepare
        if self.tokenizer is None:
            raise ValueError("explicit resident load required")
        return prepare(view, seed, self.config, mode, self.tokenizer, **flags)

    def call(self, slot, identity, episode, request, stage, *, contingency=False):
        from .process import InfrastructureLost
        store = self.stores[slot]
        with self.quiescence:
            while self.snapshot_requested:
                self.quiescence.wait()
            self.active_calls.add(identity)
            self.meta.put_meta("active_generation", True)
        returned = False
        try:
            store.register(identity,episode,request)
            row = store.call(identity)
            if row["outcome"] is not None:
                returned=True
                return json.loads(row["outcome"])
            if self.pause.is_set():
                raise Paused("pause requested before new admission")
            if self.meta.meta("model_defect"):
                raise ValueError("recorded model/runtime defect requires diagnosis before any generation")
            worker = self.workers[slot]
            if worker is None:
                raise ValueError("resident worker required")
            if hasattr(worker,"process") and (worker.process is None or not worker.process.is_alive() or worker.unconfirmed):
                raise ValueError("explicit resident reload required before any further admission")
            if any(r["status"]=="admitted" and r["call_id"] not in self.active_calls for s in self.stores for r in s.rows("attempts")):
                raise ValueError("unresolved prior attempt blocks dispatch until confirmed reconciliation")
            for s in self.stores:
                for c in s.rows("calls"):
                    if c["outcome"] and json.loads(c["outcome"]).get("termination_pending") and not s.meta("timeout_termination/"+c["id"],{}).get("termination_confirmed"):
                        raise ValueError("preceding timeout termination remains unconfirmed")
            mode = request["settings"]["mode"]
            timeout = self.config[mode+"_timeout_seconds"]
            if self.remaining_time() is None or self.remaining_time() <= timeout+2*self.config["termination_seconds"]+self.config["export_reserve_seconds"]:
                raise ValueError("insufficient session time for bounded call, termination and export")
            if self.meta.meta("blocked_worlds") and episode.split("/")[0] in self.meta.meta("blocked_worlds"):
                raise ValueError("lost evidence in this world; automatic regeneration prohibited")
            attempt = self.admission.admit(store,identity,stage,contingency=contingency)
            self.emit("admitted", call=identity, slot=slot, attempt=attempt, usage=self.admission.usage())
            try:
                outcome = worker.obtain(request,timeout)
            except InfrastructureLost as error:
                self.admission.reconcile(store,attempt,dict(error.evidence,reason="confirmed infrastructure interruption"))
                raise ValueError("interrupted attempt retained; explicitly reload then resume exact scope") from error
            store.raw(identity,attempt,outcome)
            if outcome.get("termination_pending"):
                evidence = worker.close()
                store.put_meta("timeout_termination/"+identity,evidence)
            if outcome.get("failure") == "provider_defect" or outcome.get("framing_error"):
                self.meta.put_meta("model_defect", dict(call=identity,outcome=outcome))
            self.emit("raw_persisted",call=identity,outcome=outcome)
            returned = True
            return outcome
        finally:
            if not returned:
                self.settled(identity)

    def settled(self, identity):
        with self.quiescence:
            self.active_calls.discard(identity)
            self.meta.put_meta("active_generation",bool(self.active_calls))
            self.quiescence.notify_all()

    def episode(self, world, phase, mode):
        slot = world["device"]
        store = self.stores[slot]
        identity = world["id"]+"/"+phase
        prefix = store.state(world["id"]+"/prefix")
        if phase != "prefix" and (not prefix or not prefix["terminal"]):
            raise ValueError("terminal shared prefix required before sibling starts")
        with self.quiescence:
            while self.snapshot_requested:
                self.quiescence.wait()
            state = store.state(identity) or store.start(identity,initial_episode(world,phase,prefix))
        while next_agent(state) is not None:
            agent = next_agent(state)
            invocation = state["turns"][agent]
            call_id = f"{identity}/agent-{agent}/invocation-{invocation}"
            view = permitted_view(world,state,agent)
            seed = world["seeds"]["prefix" if phase == "prefix" else "recovery"][agent][invocation]
            request = self.request(view,seed,mode)
            try:
                outcome = self.call(slot,call_id,identity,request,world["group"])
                action,error = validate_action(outcome.get("visible_text",""),truncated=outcome.get("truncated",False))
                if outcome.get("failure") or outcome.get("framing_error"):
                    action,error = None,outcome.get("failure") or outcome["framing_error"]
                state = apply_outcome(state,agent,action,error,call_id)
                store.effects(call_id,identity,state)
            finally:
                self.settled(call_id)
            self.emit("effect_committed",world=world["id"],phase=phase,agent=agent,action=action,error=error,
                      terminal=state["terminal"])
            if self.meta.meta("model_defect"):
                raise ValueError("provider/cache/framing defect; dispatch stopped after persisting evidence")
            self.periodic_checkpoint()
            if self.pause.is_set() and not state["terminal"]:
                raise Paused("paused at committed call boundary")
        return state

    def control(self, world, input_phase, mode, stage=None):
        identity = f"{world['id']}/control-{input_phase}-{mode}"
        request = self.request(dict(complete_input=[v for shard in world[input_phase] for v in shard]),
                               world["control_seeds"][input_phase],mode,control=True)
        try:
            outcome = self.call(world["device"],identity,identity,request,stage or world["group"])
            act,error = validate_action(outcome.get("visible_text",""),truncated=outcome.get("truncated",False),control=True)
            result = dict(terminal="control_completed", submissions=[act["submit"]] if act else [],
                          correct=int(not error and not outcome.get("failure") and not outcome.get("framing_error") and act["submit"]==world[input_phase+"_truth"]),
                          error=error or outcome.get("failure") or outcome.get("framing_error"))
            store = self.stores[world["device"]]
            store.start(identity,dict(terminal=None))
            store.effects(identity,identity,result)
        finally:
            self.settled(identity)
        if self.meta.meta("model_defect"):
            raise ValueError("control provider/framing defect recorded")
        self.periodic_checkpoint()
        return result

    def readiness(self):
        self.require("loaded_session")
        results = []
        for slot in range(2):
            for label,values in (("A1",[-7,3]),("B",[100,-9]),("A2",[-7,3])):
                request = self.request(dict(complete_input=values),seed_for(self.config["master_seed"],"state",slot,"A" if label != "B" else "B"),"direct",control=True)
                identity = f"hardware/state-{slot}-{label}"
                try:
                    outcome = self.call(slot,identity,identity,request,"hardware")
                finally:
                    self.settled(identity)
                self.periodic_checkpoint()
                results.append(dict(slot=slot,label=label,outcome=outcome))
        passed = all(not r["outcome"].get("failure") and r["outcome"].get("backend",{}).get("finite_score_steps",0)>0 and
                     r["outcome"].get("backend",{}).get("cache",{}).get("initial_empty") and
                     r["outcome"].get("backend",{}).get("cache",{}).get("same_call_cache") for r in results)
        equal=[results[s*3]['outcome'].get('token_ids')==results[s*3+2]['outcome'].get('token_ids') for s in range(2)]
        receipt = dict(passed=passed,results=results, ABA_equal=equal,needs_review=not all(equal),
                       equality_policy='Diagnostic: unexpected differences require explicit state-isolation review before qualification; no extra samples or decoding changes.')
        self.meta.put_meta("readiness",receipt)
        if not passed:
            raise ValueError("readiness cache/finite-output gate failed")
        return receipt

    def screen(self, mode, reason=""):
        if not self.meta.meta("readiness",{}).get("passed"):
            raise ValueError("passing readiness required")
        if self.meta.meta('readiness',{}).get('needs_review') and not self.meta.meta('review/readiness'):
            raise ValueError('A/B/A differs: inspect saved cache/token evidence and record_state_review(notes) before qualification')
        if mode == "thinking":
            direct = self.meta.meta("screen/direct")
            if not direct or direct["passed"] or direct["protocol_errors"] or not reason.strip():
                raise ValueError("thinking needs documented direct competence failure without protocol defects")
        rows = [self.control(w,p,mode,mode) for w in self.manifest["worlds"] if w["group"]=="qualification" for p in ("original","revised")]
        receipt = dict(correct=sum(r["correct"] for r in rows),total=12,protocol_errors=sum(bool(r["error"]) for r in rows),reason=reason)
        receipt["passed"] = receipt["correct"]>=11 and receipt["protocol_errors"]==0
        self.meta.put_meta("screen/"+mode,receipt)
        return receipt

    def envelope(self, mode, *, reload=False):
        if not self.meta.meta("screen/"+mode,{}).get("passed"):
            raise ValueError("passing selected competence screen required")
        frozen = self.meta.meta("freeze")
        if frozen and frozen["mode"] != mode:
            raise ValueError("selected frozen mode cannot change")
        prior=self.meta.meta("envelope",{})
        if prior and (prior.get("session")!=self.session_id or self.meta.meta("reload_required")) and not reload:
            raise ValueError("new/reloaded session requires explicit two contingency-charged reload probes")
        loads=self.load_references()
        results = []
        for slot in range(2):
            identity = f"hardware/envelope-{mode}-{slot}" + ("/reload-"+'+'.join(loads) if reload else "")
            req = self.request(dict(complete_input=[0,1]),seed_for(self.config["master_seed"],identity),mode,control=True,envelope=True)
            try:
                outcome = self.call(slot,identity,identity,req,"hardware",contingency=reload)
            finally:
                self.settled(identity)
            self.periodic_checkpoint()
            results.append(outcome)
        passed = all(not o.get("failure") and o.get("backend",{}).get("finite_score_steps",0)>0 and
                     o.get("backend",{}).get("cache",{}).get("initial_empty") and o.get("backend",{}).get("cache",{}).get("same_call_cache") and
                     o.get("generated_tokens")== (512 if mode=="direct" else 4096) and
                     o.get("backend",{}).get("observed_peak_free_lower_bytes",0)>=self.config["headroom_bytes"] for o in results)
        receipt = dict(passed=passed,mode=mode,session=self.session_id,loads=loads,reload=reload,results=results)
        self.meta.put_meta("envelope",receipt)
        if passed:
            self.meta.put_meta("selected_mode",mode)
            self.meta.put_meta("reload_required",False)
        return receipt

    def qualified(self):
        receipt = self.meta.meta("envelope",{})
        if not receipt.get("passed") or receipt.get("session") != self.session_id or self.meta.meta("reload_required"):
            raise ValueError("selected envelope required in current session; restored sessions need two budgeted reload probes")
        if receipt.get('loads')!=self.load_references():
            raise ValueError('Current replica loads require fresh contingency-charged envelope probes')
        return self.meta.meta("selected_mode")

    def load_references(self):
        if any(w is None or hasattr(w,'process') and (w.process is None or not w.process.is_alive() or w.unconfirmed) for w in self.workers):
            raise ValueError('Both resident replicas must be alive with confirmed load evidence')
        refs=[s.meta('resident_load') for s in self.stores]
        if not all(refs): raise ValueError('Both successful replica load records are required')
        return refs

    def world(self, w, mode):
        self.episode(w,"prefix",mode)
        for phase in w["treatments"]:
            self.episode(w,phase,mode)
        if w["group"] == "pilot":
            self.control(w,"original",mode)
        self.control(w,"revised",mode)
        self.checkpoint("world/"+w["id"])

    def pilot(self, number):
        mode = self.qualified()
        if type(number) is not int or number not in (1,2,3):
            raise ValueError("one pilot number 1..3 required")
        if number>1:
            self.require("review/pilot-"+str(number-1))
        w = next(w for w in self.manifest["worlds"] if w["group"]=="pilot" and w["index"]==number-1)
        self.world(w,mode)
        return dict(pilot=number,world=w["id"])

    def review(self, scope, notes, *, useful_communication=None, usable=None):
        if not notes.strip() or not (self.run/"exports/latest.zip").is_file():
            raise ValueError("inspect/export checkpoint and review notes required")
        if scope=='readiness' and (not self.meta.meta('readiness',{}).get('passed') or self.meta.meta('model_defect')):
            raise ValueError('State review cannot bypass a cache, finite-score or provider defect')
        if scope.startswith("pilot-"):
            number = int(scope.split("-")[-1])
            w = next(w for w in self.manifest["worlds"] if w["group"]=="pilot" and w["index"]==number-1)
            store = self.stores[w["device"]]
            mode = self.meta.meta("selected_mode")
            required = [w["id"]+"/"+p for p in ("prefix","retain","clear")]+[f"{w['id']}/control-{p}-{mode}" for p in ("original","revised")]
            if not all(store.state(k) and store.state(k).get("terminal") for k in required):
                raise ValueError("complete pilot evidence required before review acknowledgement")
            if type(useful_communication) is not bool or type(usable) is not bool:
                raise ValueError("pilot requires explicit original communication and usability review")
        value = dict(notes=notes,at=utc(),useful_communication=useful_communication,usable=usable,
                     archive_sha256=digest(self.run/"exports/latest.zip"),human_understanding_verified=False,
                     external_download_verified=False)
        self.meta.put_meta("review/"+scope,value)
        return value

    def forecast(self):
        from .report import analysis
        result = analysis(self.run)
        mode = self.meta.meta("selected_mode","direct")
        observed = [a["ready_seconds"] for a in result["attempts"] if a["ready_seconds"] is not None and a["status"]=="completed" and a["stage"] in ("pilot",mode)]
        remaining=0
        for w in self.manifest["worlds"]:
            if w["group"]!="main": continue
            for p in ("prefix","retain","clear"):
                state=self.stores[w["device"]].state(w["id"]+"/"+p)
                if not state: remaining+=6
                elif not state.get("terminal"):
                    remaining+=sum(3-state["turns"][a] for a in range(2) if state["submissions"][a] is None)
        remaining += sum(r.get("control_revised_"+mode) is None for r in result["worlds"] if r["group"]=="main")
        usage = self.admission.usage()
        return dict(worst_remaining_first_attempts=remaining,remaining_attempt_allowance=usage["remaining"],
                    observed_max_ready_seconds=max(observed) if observed else None,
                    conservative_wall_seconds=(remaining*(max(observed)*1.25+5)+self.config["export_reserve_seconds"] if observed else None),
                    timeout_worst_case_seconds=remaining*self.config[mode+"_timeout_seconds"]+self.config["export_reserve_seconds"],
                    remaining_session_seconds=self.remaining_time(), includes_idle_inspection=False,
                    caveat="Observed maximum with 25% margin is a forecast, not a runtime guarantee; two allocated GPUs also consume idle time.")

    def freeze(self, notes):
        mode = self.qualified()
        from .report import analysis
        result = analysis(self.run)
        for number in (1,2,3):
            r = next(w for w in result["worlds"] if w["id"]==f"pilot-{number-1:02d}")
            review = self.meta.meta("review/pilot-"+str(number),{})
            if (r["prefix"]!=1 or r.get("control_original_"+mode)!=1 or r.get("control_revised_"+mode)!=1 or
                not review.get("useful_communication") or not review.get("usable")):
                raise ValueError("three original teams/controls and documented communication/usability reviews required")
        pilot_calls = [t for t in result["traces"] if t["episode"].startswith("pilot-")]
        if any(json.loads(t["outcome"]).get("truncated") or json.loads(t["outcome"]).get("failure") for t in pilot_calls if t["outcome"]):
            raise ValueError("pilot truncation/provider defects not accepted")
        if any(ev.get("error") for s in self.stores for ep in s.rows("episodes") if ep["id"].startswith("pilot-") for ev in json.loads(ep["state"]).get("events",[])):
            raise ValueError("pilot malformed actions not accepted")
        forecast = self.forecast()
        if (not notes.strip() or forecast["remaining_attempt_allowance"] is None or
            forecast["remaining_attempt_allowance"] < forecast["worst_remaining_first_attempts"] or
            forecast["conservative_wall_seconds"] is None or self.remaining_time() < forecast["conservative_wall_seconds"] or
            forecast["observed_max_ready_seconds"]*1.25+5 > self.config[mode+"_timeout_seconds"]):
            raise ValueError("documented adequate attempt/time forecast and selected deadline required")
        old = self.meta.meta("freeze")
        if old:
            return old
        value = dict(mode=mode,at=utc(),notes=notes,forecast=forecast,manifest=self.manifest,
                     settings=self.request(dict(complete_input=[0]),0,mode,control=True)["settings"],
                     rubric=self.config["rubric"],prompt_system=messages(permitted_view(self.manifest["worlds"][0],initial_episode(self.manifest["worlds"][0],"prefix"),0))[0],
                     sessions=[s.rows("sessions") for s in self.stores])
        self.meta.bind("freeze",value)
        return value

    def prepare_batch(self, count=2):
        self.require("freeze")
        self.qualified()
        if count not in (1,2):
            raise ValueError("one or two fixed worlds only")
        current = self.meta.meta("batch")
        if current and not current.get("complete"):
            return current
        if current and not self.meta.meta("review/"+current["id"]):
            raise ValueError("inspect/export previous main batch before preparing another")
        from .report import analysis
        result = analysis(self.run)
        mode = self.meta.meta("selected_mode")
        pending = [w["id"] for w in result["worlds"] if w["group"]=="main" and
                   (any(w[p] is None for p in ("prefix","retain","clear")) or w.get("control_revised_"+mode) is None)]
        ids = pending[:count]
        if not ids:
            value=dict(complete=True,worlds=[],id='main-complete')
            self.meta.put_meta('batch',value)
            return value
        # A two-world action uses opposite logical slots; fixed parity guarantees it.
        value = dict(id="batch/"+"+".join(ids),worlds=ids,complete=False,first_ceiling=19*len(ids),
                     eligible_retry_allowance=self.config["contingency_limit"]-self.admission.usage()["contingency"],
                     forecast=self.forecast(),prepared_at=utc())
        self.meta.put_meta("batch",value)
        return value

    def main(self):
        mode = self.qualified()
        self.require("freeze")
        self.require("batch")
        batch = self.meta.meta("batch")
        if batch["complete"]:
            return batch
        with ThreadPoolExecutor(max_workers=len(batch["worlds"])) as pool:
            futures=[pool.submit(self.world,next(w for w in self.manifest["worlds"] if w["id"]==identity),mode) for identity in batch["worlds"]]
            failures=[]
            for future in as_completed(futures):
                try: future.result()
                except Exception as error:
                    self.pause.set(); failures.append(error)
            if failures:
                raise failures[0]
        batch["complete"] = True
        self.meta.put_meta("batch",batch)
        return batch

    def periodic_checkpoint(self):
        if monotonic()-self.last_checkpoint>=self.config['checkpoint_seconds']:
            self.checkpoint('periodic-settled-call-boundary')

    def checkpoint(self,boundary):
        with self.checkpoint_lock:
            with self.quiescence:
                self.snapshot_requested=True
                while self.active_calls:
                    self.quiescence.wait()
            try:
                receipt = export(self.run,self.stores,boundary=boundary)
                self.last_checkpoint=monotonic()
                self.emit("checkpoint",**receipt)
                return receipt
            finally:
                with self.quiescence:
                    self.snapshot_requested=False
                    self.quiescence.notify_all()

    def run_action(self, action, **args):
        # Controller allows one active action, including repeated widget requests.
        with self.action_lock:
            self.pause.clear()
            self.meta.put_meta("action",dict(name=action,args=args,status="running",at=utc()))
            result, error = None, None
            try:
                methods = {"readiness":self.readiness,"screen":self.screen,"envelope":self.envelope,
                           "pilot":self.pilot,"freeze":self.freeze,"prepare_batch":self.prepare_batch,
                           "main":self.main,"review":self.review,"selfcheck":self.selfcheck,"load":self.load,
                           "window":self.window,"snapshot":lambda boundary='operator-snapshot':dict(boundary_requested=boundary)}
                if action=="report":
                    from .report import analysis
                    methods["report"]=lambda:analysis(self.run)["summary"]
                if action not in methods:
                    raise ValueError("unknown finite action")
                result = methods[action](**args)
            except (Exception,KeyboardInterrupt) as exc:
                error = f"{type(exc).__name__}: {exc}"
                atomic_json(self.run/'receipts'/'stage-error.json',dict(action=action,args=args,at=utc(),error=error,traceback=traceback.format_exc()))
                self.emit("action_stopped",action=action,error=error)
            finally:
                self.meta.put_meta("action",dict(name=action,args=args,status="stopped" if error else "complete",error=error,at=utc()))
                try:
                    checkpoint=self.checkpoint(args.get('boundary','action/snapshot') if action=='snapshot' else 'action/'+action)
                except Exception as exc:
                    checkpoint=dict(error=f"{type(exc).__name__}: {exc}",last_valid_preserved=True)
                self.emit("action_finished",action=action,error=error,result=result,checkpoint=checkpoint)
            return dict(result=result,error=error,checkpoint=checkpoint)

    def close_models(self):
        if not self.action_lock.acquire(blocking=False):
            self.pause.set()
            raise ValueError("pause requested; wait for call-boundary acknowledgement before close")
        try:
            evidence=[]
            for slot,w in enumerate(self.workers):
                if w is not None:
                    row=w.close()
                    evidence.append(row)
                    prior=self.stores[slot].db.execute("SELECT id,evidence FROM sessions WHERE id LIKE ? ORDER BY rowid DESC LIMIT 1",(self.session_id+"/load-%",)).fetchone()
                    if prior:
                        value=json.loads(prior["evidence"]); value["process_close"]=row
                        with self.stores[slot].transaction():
                            self.stores[slot].db.execute("UPDATE sessions SET evidence=? WHERE id=?",(canonical(value),prior["id"]))
            return evidence
        finally:
            self.action_lock.release()

    def close(self):
        self.pause.set()
        self.close_models()
        for s in self.stores:
            s.close()
        self.ownership.close()


class Paused(RuntimeError):
    pass
