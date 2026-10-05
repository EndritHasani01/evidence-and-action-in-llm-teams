"""Small local scheduler over saved branches and exclusive worker databases.

One controller and one bounded resident generation process per worker. Only
the latter loads a model. Parent files are read-only; no replies, attempts or
delivery effects are copied. Placement/order never assign scientific seeds.
M5 supplies the accepted factories and authorization; M3 tests use CPU scripts.
"""

from dataclasses import asdict, dataclass
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
from .runner import DurableRunner, WorkerReader
from .schedule import _prepare_branches, dependency_order
from .storage import record_json, seconds, settings_json
from .tasks import PEERS


@dataclass(frozen=True)
class WorkerSpec:
    database: Path
    provider_factory: object
    cuda_visible_devices: str | None = None


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
        with DurableRunner(spec.database, tokenizer, provider, dependencies=dependencies,
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
                 timeout_seconds=120, termination_seconds=1, heartbeat_seconds=1):
        self.specs = tuple(workers)
        self.paths = tuple(Path(w.database).resolve() for w in workers)
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
                if path.exists():
                    self._confirm_provider_exit(path)
                with DurableRunner(path, None) as runner:
                    runner.store.bind_run(self.worlds, self.branches, self.settings, self.bounds)
            self.readers = [WorkerReader(path) for path in self.paths]
            self.status()  # Reject old drift/duplicate ownership before providers can run.
            for index in range(len(self.specs)):
                self._launch(index)
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
        if not wait([connection, process.sentinel], timeout=self.bounds["timeout_seconds"]):
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
        """Read-only runnable/waiting/active/done work from existing records.

        This scheduling view supplies M3-T04; it is not resource accounting or a
        persisted progress store. It never reads candidate correctness.
        """
        if not self.readers:
            raise ValueError("open the scheduler before reading its worker records")
        owned, completed = {}, {}
        for index, reader in enumerate(self.readers):
            recorded = {r[0] for r in reader.store.connection.execute("SELECT DISTINCT branch_id FROM round_inputs")}
            recorded.update(r[0] for r in reader.store.connection.execute("SELECT DISTINCT thread_id FROM checkpoints"))
            if recorded - self.by_branch.keys():
                raise ValueError("worker contains work outside the saved run schedule")
            for branch_id in recorded:
                if branch_id in owned:
                    raise ValueError("duplicate branch ownership across workers")
                branch = self.by_branch[branch_id]
                values = reader.values(branch_id) if branch.phase != "control" else None
                if values is not None:
                    if (values["branch_json"] != record_json(asdict(branch))
                            or values["settings_json"] != settings_json(self.settings)):
                        raise ValueError("worker checkpoint schedule/settings differ")
                    state = reader.state(branch_id)
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
        active = {b: i for i, (b, _) in self.inflight.items()}
        incomplete = [b for b in self.ordered if completed.get(b.branch_id, 0) < (1 if b.phase == "control" else 4)]
        first_block = min((self.block[b.branch_id] for b in incomplete), default=None)
        prelude = tuple(b.branch_id for b in incomplete if self.block[b.branch_id] == first_block
                        and b.phase in ("prefix", "control"))
        work = []
        for branch in self.ordered:
            branch_id = branch.branch_id
            r = completed.get(branch_id, 0)
            done = r == (1 if branch.phase == "control" else 4)
            waiting = []
            if not done and branch_id not in active:
                if self.block[branch_id] != first_block:
                    waiting.append("earlier balanced world block")
                if branch.phase == "continuation" and prelude:
                    waiting.extend(prelude)
                if branch.prefix_parent is not None and completed.get(branch.prefix_parent, 0) != 4:
                    waiting.append(branch.prefix_parent)
                if r == 0:
                    waiting.extend(c.replay_parent for c in branch.calls if c.replay_parent is not None
                                   and completed.get(c.replay_parent.rsplit("/r", 1)[0], 0) < 1)
            status = "active" if branch_id in active else "done" if done else "dependency_waiting" if waiting else "runnable"
            work.append(Work(branch_id, owned.get(branch_id, active.get(branch_id)), r,
                             None if done else r + 1, status, tuple(dict.fromkeys(waiting))))
        return tuple(work)

    def dispatch(self):
        for index, process in self.processes.items():
            if not process.is_alive():
                raise WorkerInterrupted(f"worker {index} exited; restart its assigned work")
        idle = [(self.cursor + i) % len(self.specs) for i in range(len(self.specs))
                if (self.cursor + i) % len(self.specs) not in self.inflight]
        ready = sorted((w for w in self.status() if w.status == "runnable"),
                       key=lambda w: (w.next_round, self.rank[w.branch_id]))
        admitted = []
        for work in ready:
            eligible = idle if work.worker is None else [i for i in idle if i == work.worker]
            if not eligible:
                continue
            index = eligible[0]
            command = work.branch_id, work.next_round
            self.connections[index].send(command)
            self.inflight[index] = command
            idle.remove(index)
            self.cursor = (index + 1) % len(self.specs)
            admitted.append((index, *command))
        return tuple(admitted)

    def advance(self, timeout=0.1):
        """Dispatch ready work and wait briefly for explicit round acknowledgments."""
        self.dispatch()
        handles = [h for i in self.inflight for h in (self.connections[i], self.processes[i].sentinel)]
        if not handles:
            if any(w.status != "done" for w in self.status()):
                raise ValueError("no runnable work: missing/inconsistent dependency")
            return ()
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
        return tuple(finished)

    def run(self):
        while self.inflight or any(w.status != "done" for w in self.status()):
            self.advance()
