"""Small local scheduler over saved branches and exclusive worker databases.

One controller and one bounded resident generation process per worker. Only
the latter loads a model. Parent files are read-only; no replies, attempts or
delivery effects are copied. Placement/order never assign scientific seeds.
M5 supplies the accepted factories and authorization; M3 tests use CPU scripts.
"""

from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import json
import multiprocessing as mp
from multiprocessing.connection import wait
import os
from pathlib import Path
from threading import Thread
from time import monotonic, sleep
import traceback

from .attempts import ProcessProvider, _die_with_owner
from .manifests import load_population, load_schedules
from .populations import FAMILIES
from .rounds import deserialize_state
from .runner import DurableRunner, WorkerReader
from .schedule import _prepare_branches, dependency_order
from .storage import record_json, seconds, settings_json
from .tasks import PEERS


@dataclass(frozen=True)
class WorkerSpec:
    database: Path
    provider_factory: object
    cuda_visible_devices: str | None = None
    allocated_device: str | None = None
    allocated_at: str | None = None
    provider_billing: dict | None = None


@dataclass(frozen=True)
class Work:
    branch_id: str
    worker: int | None
    completed_round: int
    next_round: int | None
    status: str
    waiting_for: tuple[str, ...]


class WorkerInterrupted(RuntimeError):
    """The exclusive owner stopped; restart it before continuing assigned work."""


@contextmanager
def _own_file(path):
    """An OS lock enforces one writer even after a controller/worker restart.

    This one-byte sidecar stores no status, PID, replies or peer state. The OS
    releases ownership when a killed process exits; no stale lease is guessed.
    """
    with Path(str(path) + ".owner").open("a+b") as lock:
        lock.seek(0, os.SEEK_END)
        if lock.tell() == 0:
            lock.write(b"\0")
            lock.flush()
        lock.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            raise WorkerInterrupted(f"preceding exclusive worker still owns {path}") from error
        try:
            yield
        finally:
            lock.seek(0)
            if os.name == "nt":
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _process_alive(pid):
    if os.name == "nt":
        import ctypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.OpenProcess.argtypes = (ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong)
        kernel.WaitForSingleObject.argtypes = (ctypes.c_void_p, ctypes.c_ulong)
        kernel.CloseHandle.argtypes = (ctypes.c_void_p,)
        handle = kernel.OpenProcess(0x100000, False, pid)
        if not handle:
            return ctypes.get_last_error() == 5  # Access denied cannot establish exit.
        try:
            return kernel.WaitForSingleObject(handle, 0) == 258
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def balanced_order(worlds, branches, *, reverse=False):
    """One world of each family per index block, with rotated eligible siblings.

    Prefix/control opportunities precede recoveries in each balanced block.
    All development worlds have index one, preserving the 90-call capability
    prelude. Dependency checks, not list order, admit mixed/Q first rounds.
    """
    ordered = []
    for index in sorted({w.index for w in worlds}):
        family_order = FAMILIES[index % len(FAMILIES):] + FAMILIES[:index % len(FAMILIES)]
        block = sorted((w for w in worlds if w.index == index),
                       key=lambda w: (family_order.index(w.world.task), w.world_id))
        for phase in ("prefix", "control", "continuation"):
            for world in block:
                siblings = sorted((b for b in branches if b.world_id == world.world_id and b.phase == phase),
                                  key=lambda b: (b.replicate, b.event, b.policy or ""))
                if siblings:
                    rotation = (index + FAMILIES.index(world.world.task)) % len(siblings)
                    siblings = siblings[rotation:] + siblings[:rotation]
                    ordered.extend(reversed(siblings) if reverse else siblings)
    return tuple(ordered)


def _worker(spec, paths, worlds, branches, tokenizer_factory, settings, bounds, order, connection):
    # Visibility was inherited at spawn, before imports in the new interpreter;
    # set it explicitly again before either factory can initialize CUDA.
    if spec.cuda_visible_devices is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = spec.cuda_visible_devices
    Thread(target=_die_with_owner, daemon=True).start()
    try:
        tokenizer = tokenizer_factory()
        provider = ProcessProvider(spec.provider_factory, **bounds)
        dependencies = tuple(p for p in paths if p != Path(spec.database).resolve())
        by_world = {w.world_id: w for w in worlds}
        by_branch = {b.branch_id: b for b in branches}
        with _own_file(spec.database), DurableRunner(spec.database, tokenizer, provider, dependencies=dependencies,
                                                    invocation_order=order) as runner:
            connection.send(("ready", os.getpid()))
            while True:
                command = connection.recv()
                if command is None:
                    return
                branch_id, round_number = command
                branch = by_branch[branch_id]
                world = by_world[branch.world_id]
                if branch.phase == "control":
                    if round_number != 1:
                        raise ValueError("control has one fixed opportunity")
                    runner.run_control(world, branch, settings=settings)
                else:
                    runner.start(world, branch, settings=settings)
                    runner.run_round(branch_id, round_number)
                connection.send(("done", (branch_id, round_number)))
    except (EOFError, BrokenPipeError):
        pass
    except BaseException:
        connection.send(("error", traceback.format_exc()))
    finally:
        connection.close()


class LocalScheduler:
    """One local owner dispatches explicit rounds to isolated serial workers.

    Use as a context manager. Completed raw calls/checkpoints, including invalid
    outcomes, determine resume. An interrupted worker raises WorkerInterrupted;
    restart(index) confirms its exit before reopening its original database.
    A protocol/capacity/provider defect stops instead of choosing new work.
    """

    def __init__(self, workers, worlds, branches, tokenizer_factory, *, settings,
                 reverse=False, worker_rotation=0, invocation_order=PEERS,
                 timeout_seconds=120, termination_seconds=1, heartbeat_seconds=1,
                 budget=None, release_device=None, allocation_stage=None, report=None, prior_paths=()):
        self.specs = tuple(workers)
        self.paths = tuple(Path(w.database).resolve() for w in self.specs)
        self.worlds, self.branches = tuple(worlds), tuple(branches)
        self.settings = json.loads(settings_json(settings))
        self.tokenizer_factory = tokenizer_factory
        self.bounds = dict(timeout_seconds=seconds(timeout_seconds),
                           termination_seconds=seconds(termination_seconds),
                           heartbeat_seconds=seconds(heartbeat_seconds))
        if (not self.specs or len(set(self.paths)) != len(self.paths)
                or any(not callable(w.provider_factory) or
                       w.cuda_visible_devices is not None and type(w.cuda_visible_devices) is not str for w in self.specs)
                or not callable(tokenizer_factory) or min(self.bounds.values()) <= 0
                or self.bounds["heartbeat_seconds"] > 60):
            raise ValueError("use distinct worker files, importable factories and positive bounded timeouts")
        self.order = tuple(invocation_order)
        if (len(self.order) != 4 or set(self.order) != set(PEERS)
                or any(type(p) is not int for p in self.order) or type(worker_rotation) is not int):
            raise ValueError("invalid peer order or worker rotation")
        by_world = {w.world_id: w for w in self.worlds}
        allowed = {b.branch_id: b for b in _prepare_branches(self.worlds)}
        if (len(by_world) != len(self.worlds) or not self.branches
                or any(b.world_id not in by_world or allowed.get(b.branch_id) != b for b in self.branches)):
            raise ValueError("execute exact saved branches/worlds; never reassign seeds or parents")
        dependency_order(self.branches)  # Missing/mis-scoped parents fail before any process/write.
        self.ordered = balanced_order(self.worlds, self.branches, reverse=reverse)
        self.by_branch = {b.branch_id: b for b in self.branches}
        self.rank = {b.branch_id: i for i, b in enumerate(self.ordered)}
        self.block = {b.branch_id: by_world[b.world_id].index for b in self.branches}
        self.cursor = worker_rotation % len(self.specs)
        self.processes, self.connections, self.readers = {}, {}, []
        self.inflight = {}
        self.budget, self.release_device, self.report = budget, release_device, report
        self.prior_paths = tuple(Path(p).resolve() for p in prior_paths)
        self.allocation_stage = allocation_stage or ("development" if all(w.development for w in self.worlds) else "main")
        self.deadline = None
        self.allocations = {}
        self.stop_reason = None
        self._reported_signature = self._last_reported = None
        if budget is not None:
            from .accounting import Budget
            devices = [w.allocated_device for w in self.specs]
            if (not isinstance(budget, Budget) or not callable(release_device) or not all(devices)
                    or len(set(devices)) != len(devices)
                    or budget.shutdown_seconds < len(self.specs) * 5 * self.bounds["termination_seconds"]):
                raise ValueError("budget requires distinct allocated devices, a bounded release acknowledgement and complete shutdown allowance")
        if report is not None and not callable(report):
            raise ValueError("report must consume derived status snapshots")

    @classmethod
    def from_manifests(cls, workers, population_path, schedule_path, tokenizer_factory, *,
                       stage="development", count=60, **kwargs):
        population = load_population(population_path)
        schedules = load_schedules(schedule_path, population)
        if stage == "development":
            worlds, branches = population.development, schedules.development
        elif stage == "main":
            worlds, branches = population.worlds(count), schedules.main_for(population, count)
        else:
            raise ValueError("choose the saved development or complete main schedule")
        return cls(workers, worlds, branches, tokenizer_factory, **kwargs)

    def __enter__(self):
        try:
            for path in self.paths:
                path.parent.mkdir(parents=True, exist_ok=True)
                with _own_file(path):
                    if path.exists():
                        self._confirm_provider_exit(path)
                    with DurableRunner(path, None) as runner:
                        runner.store.bind_run(self.worlds, self.branches, self.settings, self.bounds, budget=self.budget)
            self.readers = [WorkerReader(path) for path in self.paths]
            self.status()  # Reject old drift/duplicate ownership before providers can run.
            if self.budget is not None:
                self._allocate()
            for index in range(len(self.specs)):
                self._launch(index)
            self._report(force=True)
        except BaseException:
            self.close()
            raise
        return self

    def _confirm_provider_exit(self, path):
        # A dead controller's inference child exits via its real owner sentinel.
        # Confirm that exit before admitting replacement inference. PID reuse
        # causes a conservative stop, never a kill of an unrelated process.
        store = WorkerReader(path).store
        try:
            pids = {r[0] for r in store.connection.execute(
                "SELECT pid FROM provider_processes WHERE stopped_at IS NULL")}
            deadline = monotonic() + 2 * self.bounds["termination_seconds"]
            while any(_process_alive(pid) for pid in pids):
                if monotonic() >= deadline:
                    raise WorkerInterrupted("preceding inference process is still live or uncertain; do not restart")
                sleep(0.01)
        finally:
            store.close()

    def __exit__(self, *_):
        self.close()

    def _launch(self, index):
        self._check_deadline()
        context = mp.get_context("spawn")
        connection, child = context.Pipe()
        process = context.Process(target=_worker, args=(self.specs[index], self.paths,
            self.worlds, self.branches, self.tokenizer_factory, self.settings, self.bounds, self.order, child))
        old_visibility = os.environ.get("CUDA_VISIBLE_DEVICES")
        visibility = self.specs[index].cuda_visible_devices
        try:
            if visibility is not None:
                os.environ["CUDA_VISIBLE_DEVICES"] = visibility
            process.start()
        finally:
            child.close()
            if old_visibility is None:
                os.environ.pop("CUDA_VISIBLE_DEVICES", None)
            else:
                os.environ["CUDA_VISIBLE_DEVICES"] = old_visibility
        self.processes[index], self.connections[index] = process, connection
        wait_seconds = self.bounds["timeout_seconds"]
        if self.deadline is not None:
            wait_seconds = min(wait_seconds, max(0, self.deadline - monotonic()))
        if not wait([connection, process.sentinel], timeout=wait_seconds):
            self._check_deadline()
            raise WorkerInterrupted(f"worker {index} did not initialize within its bound")
        try:
            kind, payload = connection.recv()
        except (EOFError, OSError) as error:
            raise WorkerInterrupted(f"worker {index} exited during initialization") from error
        if kind != "ready":
            raise RuntimeError(f"worker {index} initialization defect: {payload}")

    def close(self):
        for index, process in self.processes.items():
            if process.is_alive() and index not in self.inflight:
                try:
                    self.connections[index].send(None)
                except (EOFError, OSError):
                    pass
            process.join(self.bounds["termination_seconds"])
            if process.is_alive():
                process.terminate()
                process.join(self.bounds["termination_seconds"])
            if process.is_alive():
                process.kill()
                process.join(self.bounds["termination_seconds"])
            if process.is_alive():
                raise WorkerInterrupted(f"worker {index} termination is unconfirmed")
            self._confirm_provider_exit(self.paths[index])
            self.connections[index].close()
            process.close()
        self.processes.clear()
        self.connections.clear()
        self.inflight.clear()
        # A local process exit alone never ends paid/physical allocation.
        # Writes happen only after the exclusive worker has exited.
        for index, number in tuple(self.allocations.items()):
            from .storage import WorkerStore
            with _own_file(self.paths[index]):
                store = WorkerStore(self.paths[index])
                try:
                    reason = self.stop_reason or "scheduler_close"
                    store.recover_processes()
                    for row in store.connection.execute("SELECT call_id FROM calls WHERE status='running'").fetchall():
                        attempt = store.attempts(row[0])[-1]
                        if attempt["status"] == "running":
                            store.interrupt_attempt(row[0], "confirmed worker/provider exit at " + reason)
                    store.allocation_stop_requested(number, reason)
                    released = self.release_device(index, self.specs[index].allocated_device)
                    if released is not True and not isinstance(released, str):
                        store.allocation_stop_requested(number, reason + "; provider_release_unconfirmed")
                        raise WorkerInterrupted("provider release is unconfirmed; allocation remains open and chargeable")
                    store.allocation_stopped(number, reason, released_at=released if isinstance(released, str) else None)
                    del self.allocations[index]
                finally:
                    store.close()
        for reader in self.readers:
            reader.close()
        self.readers.clear()

    def restart(self, index):
        process = self.processes[index]
        process.join(0)
        if process.is_alive():
            raise WorkerInterrupted("stop the preceding exclusive worker before restart")
        self._confirm_provider_exit(self.paths[index])
        self.connections[index].close()
        process.close()
        del self.processes[index]
        del self.connections[index]
        self.inflight.pop(index, None)
        self._launch(index)

    def status(self):
        """Read-only runnable/waiting/active/done work from existing records."""
        return scheduled_work(self.worlds, self.branches, self.readers,
                              settings=self.settings, inflight=self.inflight)

    def progress(self):
        from .accounting import progress_snapshot
        return progress_snapshot(self.worlds, self.branches, self.paths, budget=self.budget,
            inflight=self.inflight, settings=self.settings, prior_paths=self.prior_paths,
            gate=self.stop_reason or "M3 CPU verification; M5 inference gate open")

    def _allocate(self):
        from .accounting import BudgetStop, timestamp
        from .storage import WorkerStore
        snapshot = self.progress()
        resources = snapshot["resources"]
        if resources["active_devices"]:
            raise BudgetStop("preceding allocations require confirmed provider release")
        available = (resources["remaining_ceiling_gpu_hours"]
                     - sum(resources["remaining_reserves_gpu_hours"].values())) * 3600 - self.budget.overhead_seconds
        now = datetime.now(timezone.utc)
        previous_idle = sum(now.timestamp() - timestamp(spec.allocated_at) for spec in self.specs if spec.allocated_at)
        if any(spec.allocated_at and timestamp(spec.allocated_at) > now.timestamp() for spec in self.specs):
            raise ValueError("provider allocation cannot start in the future")
        available -= previous_idle
        duration = available / len(self.specs) - self.budget.shutdown_seconds
        if duration <= 0:
            self.stop_reason = "budget_exhausted_before_allocation"
        self.deadline = monotonic() + max(0, duration)
        deadline_at = (now + timedelta(seconds=duration)).isoformat() if duration > 0 else None
        for index, spec in enumerate(self.specs):
            if duration <= 0 and spec.allocated_at is None:
                continue  # No new allocation, but retain already allocated time.
            with _own_file(self.paths[index]):
                store = WorkerStore(self.paths[index])
                try:
                    self.allocations[index] = store.allocation_started(spec.allocated_device, self.allocation_stage,
                        budget=self.budget, deadline_at=deadline_at, started_at=spec.allocated_at,
                        billing=spec.provider_billing)
                finally:
                    store.close()
        if duration <= 0:
            raise BudgetStop(self.stop_reason)

    def _check_deadline(self):
        if self.deadline is not None and monotonic() >= self.deadline:
            from .accounting import BudgetStop
            self.stop_reason = "allocation_deadline"
            raise BudgetStop(self.stop_reason)

    def _admit(self, work):
        self._check_deadline()
        if self.budget is None:
            return
        from .accounting import BudgetStop
        snapshot = self.progress()
        forecast, resources = snapshot["forecast"], snapshot["resources"]
        available = resources["remaining_ceiling_gpu_hours"] - sum(resources["remaining_reserves_gpu_hours"].values())
        shutdown = len(resources["active_devices"]) * self.budget.shutdown_seconds / 3600
        if self.allocation_stage == "main" and not forecast["available"]:
            self.stop_reason = "remaining_forecast_unavailable"
        elif forecast["available"] and forecast["remaining_gpu_hours"][1] + shutdown >= available:
            self.stop_reason = "remaining_forecast_exceeds_budget"
        else:
            # Serial workers can use two attempts only for interrupted calls.
            # Reserve every still-possible attempt in this whole round; idle
            # allocated devices also consume the common deadline horizon.
            bound = 0
            rows = {r["call_id"]: r for r in snapshot["logical_slots"]}
            for call in self.by_branch[work.branch_id].calls:
                if call.round_number == work.next_round and call.replay_parent is None and not rows[call.call_id]["finished"]:
                    attempts = rows[call.call_id]["cost"]["attempts"]
                    bound += max(0, 2 - attempts) * (self.bounds["timeout_seconds"] + 2 * self.bounds["termination_seconds"])
            if self.deadline - monotonic() <= bound + self.budget.overhead_seconds:
                self.stop_reason = "timeout_and_termination_allowance"
        if self.stop_reason:
            self._report(force=True)
            raise BudgetStop(self.stop_reason)

    def _report(self, *, force=False):
        if self.report is None:
            return
        clock = monotonic()
        signature = tuple((reader.store.connection.execute("SELECT count(*) FROM attempts").fetchone()[0],
            reader.store.connection.execute("SELECT count(*) FROM calls WHERE status IN ('completed','timeout','infrastructure_failure','replay')").fetchone()[0])
            for reader in self.readers)
        if not force and self._last_reported is not None and clock - self._last_reported < self.bounds["heartbeat_seconds"]:
            # Cheap ledger counters expose call transitions immediately.
            if signature == self._reported_signature:
                return
        self.report(self.progress())
        self._reported_signature, self._last_reported = signature, clock

    def dispatch(self):
        self._check_deadline()
        for index, process in self.processes.items():
            if not process.is_alive():
                raise WorkerInterrupted(f"worker {index} exited; restart its assigned work")
        idle = [(self.cursor + i) % len(self.specs) for i in range(len(self.specs))
                if (self.cursor + i) % len(self.specs) not in self.inflight]
        if not idle:
            return ()
        ready = sorted((w for w in self.status() if w.status == "runnable"),
                       key=lambda w: (w.next_round, self.rank[w.branch_id]))
        admitted = []
        for work in ready:
            eligible = idle if work.worker is None else [i for i in idle if i == work.worker]
            if not eligible:
                continue
            index = eligible[0]
            self._admit(work)
            command = work.branch_id, work.next_round
            self.connections[index].send(command)
            self.inflight[index] = command
            idle.remove(index)
            self.cursor = (index + 1) % len(self.specs)
            admitted.append((index, *command))
        if admitted:
            self._report(force=True)
        return tuple(admitted)

    def advance(self, timeout=0.1):
        """Dispatch ready work and wait briefly for explicit round acknowledgments."""
        self.dispatch()
        handles = [h for i in self.inflight for h in (self.connections[i], self.processes[i].sentinel)]
        if not handles:
            if any(w.status != "done" for w in self.status()):
                raise ValueError("no runnable work: missing/inconsistent dependency")
            return ()
        timeout = min(seconds(timeout), self.bounds["heartbeat_seconds"], 0.1)
        if self.deadline is not None:
            timeout = min(timeout, max(0, self.deadline - monotonic()))
        readable = wait(handles, timeout=timeout)
        finished = []
        for index in tuple(self.inflight):
            connection, process = self.connections[index], self.processes[index]
            if connection in readable:
                try:
                    kind, payload = connection.recv()
                except (EOFError, OSError) as error:
                    raise WorkerInterrupted(f"worker {index} interrupted; recorded outcomes remain authoritative") from error
                if kind != "done":
                    raise RuntimeError(f"worker {index} stopped for diagnosis:\n{payload}")
                if tuple(payload) != self.inflight[index]:
                    raise ValueError("worker acknowledgement differs from assigned round")
                self.inflight.pop(index)
                finished.append((index, *payload))
            elif process.sentinel in readable:
                raise WorkerInterrupted(f"worker {index} interrupted; restart its assigned work")
        self._check_deadline()
        self._report(force=bool(finished))
        return tuple(finished)

    def run(self):
        from .accounting import BudgetStop
        try:
            while self.inflight or any(w.status != "done" for w in self.status()):
                self.advance()
        except BudgetStop:
            self.close()
            raise


def scheduled_work(worlds, branches, readers, *, settings, inflight=None, reverse=False, recorded_active=False):
    """Read-only dependency/ownership reconstruction shared by status and dispatch."""
    if not readers:
        raise ValueError("open worker records before reading scheduling status")
    by_branch = {b.branch_id: b for b in branches}
    ordered = balanced_order(worlds, branches, reverse=reverse)
    by_world = {w.world_id: w for w in worlds}
    block = {b.branch_id: by_world[b.world_id].index for b in branches}
    inflight = inflight or {}
    owned, completed, running, blocked = {}, {}, {}, set()
    for index, reader in enumerate(readers):
        if reader is None:
            continue
        recorded = {r[0] for r in reader.store.connection.execute("SELECT DISTINCT branch_id FROM round_inputs")}
        recorded.update(r[0] for r in reader.store.connection.execute("SELECT DISTINCT thread_id FROM checkpoints"))
        if recorded - by_branch.keys():
            raise ValueError("worker contains work outside the saved run schedule")
        for branch_id in recorded:
            if branch_id in owned:
                raise ValueError("duplicate branch ownership across workers")
            branch = by_branch[branch_id]
            values = reader.values(branch_id) if branch.phase != "control" else None
            if values is not None:
                if (values["branch_json"] != record_json(asdict(branch))
                        or values["settings_json"] != settings_json(settings)):
                    raise ValueError("worker checkpoint schedule/settings differ")
                # Metadata and peer state come from the same saved checkpoint;
                # a second saver read can observe a newer worker transition.
                state = deserialize_state(values["committed"])
                r = state.last_slot.round_number if state.last_slot is not None and state.last_slot.phase == state.phase else 0
            else:
                r = 0
                if branch.phase != "control":
                    raise ValueError("saved branch inputs lack their original checkpoint")
            rows = {row["call_id"]: dict(row) for row in reader.store.connection.execute(
                "SELECT * FROM calls WHERE branch_id=?", (branch_id,))}
            if rows.keys() - {c.call_id for c in branch.calls}:
                raise ValueError("worker contains an unscheduled logical slot")
            for call in branch.calls:
                row = rows.get(call.call_id)
                if row is not None and row["status"] == "running":
                    attempt = reader.store.attempts(call.call_id)[-1]
                    if attempt["status"] == "blocked":
                        blocked.add(branch_id)
                    else:
                        running[branch_id] = index
                if row is not None and tuple(row[k] for k in ("seed", "generation_id", "replay_parent", "round_number", "peer")) != (
                        call.seed, call.generation_id, call.replay_parent, call.round_number,
                        -1 if call.peer is None else call.peer):
                    raise ValueError("worker slot seed/scope/parent differs")
                if call.round_number <= r and (row is None or row["validation_json"] is None):
                    raise ValueError("missing committed call/validation dependency")
                if call.round_number <= r:
                    if row["status"] not in ("completed", "timeout", "infrastructure_failure", "replay"):
                        raise ValueError("committed slot lacks a durable outcome")
                    if call.replay_parent is None:
                        reader.store.response(call.call_id)
            if branch.phase == "control":
                row = rows.get(branch.calls[0].call_id)
                r = int(row is not None and row["validation_json"] is not None)
            owned[branch_id], completed[branch_id] = index, r
    active = (running if recorded_active else {}) | {b: i for i, (b, _) in inflight.items()}
    incomplete = [b for b in ordered if completed.get(b.branch_id, 0) < (1 if b.phase == "control" else 4)]
    first_block = min((block[b.branch_id] for b in incomplete), default=None)
    prelude = tuple(b.branch_id for b in incomplete if block[b.branch_id] == first_block
                    and b.phase in ("prefix", "control"))
    work = []
    for branch in ordered:
        branch_id = branch.branch_id
        r = completed.get(branch_id, 0)
        done = r == (1 if branch.phase == "control" else 4)
        waiting = []
        if not done and branch_id not in active:
            if block[branch_id] != first_block:
                waiting.append("earlier balanced world block")
            if branch.phase == "continuation" and prelude:
                waiting.extend(prelude)
            if branch.prefix_parent is not None and completed.get(branch.prefix_parent, 0) != 4:
                waiting.append(branch.prefix_parent)
            if r == 0:
                waiting.extend(c.replay_parent for c in branch.calls if c.replay_parent is not None
                               and completed.get(c.replay_parent.rsplit("/r", 1)[0], 0) < 1)
        status = "blocked" if branch_id in blocked else "active" if branch_id in active else "done" if done else "dependency_waiting" if waiting else "runnable"
        work.append(Work(branch_id, owned.get(branch_id, active.get(branch_id)), r,
                         None if done else r + 1, status, tuple(dict.fromkeys(waiting))))
    return tuple(work)
