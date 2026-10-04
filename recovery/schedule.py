"""CPU call opportunities and required sharing (spec §§2.3, 4, 6, 8.1–8.3).

Schedules are host-only, derived from the saved Population, with no outcomes or
inference settings. A null replay parent means a new generation, even if another
call has the same seed. Replay points to a raw B/C reply, never recipient state.
Request/state/settings equality and branch-local delivery remain M2/M3 checks.
"""

from collections import defaultdict
from dataclasses import dataclass
import heapq
from typing import Iterator

from .populations import Population, PreparedWorld, validate_population
from .tasks import PEERS, CandidateContract, Size, Task, candidate_contract

CAPABILITY_CALLS = 90
SMOKE_MAX_CALLS = 24


def _branch_id(world_id: str, phase: str, event: str, policy: str | None, replicate: int) -> str:
    return f"{world_id}/{phase}/{event}/{policy or 'none'}/rep{replicate}"


def _call_id(branch_id: str, round_number: int, peer: int | None) -> str:
    return f"{branch_id}/r{round_number}/{'full' if peer is None else f'p{peer}'}"


def _prefix_id(world_id: str) -> str:
    return _branch_id(world_id, "prefix", "original", None, 0)


@dataclass(frozen=True)
class CallSlot:
    call_id: str
    round_number: int
    peer: int | None
    seed: int
    replay_parent: str | None

    @property
    def generation_id(self) -> str:
        """Required physical-response join; attempts are recorded later in M3."""
        return self.replay_parent or self.call_id


@dataclass(frozen=True)
class Branch:
    world_id: str
    task: Task
    phase: str
    event: str
    policy: str | None
    replicate: int
    prefix_parent: str | None
    calls: tuple[CallSlot, ...]

    @property
    def branch_id(self) -> str:
        return _branch_id(self.world_id, self.phase, self.event, self.policy, self.replicate)

    @property
    def empty_send(self) -> bool:
        """Full-information controls require the outer reply's send=[] contract."""
        return self.phase == "control"

    def output_contract(self, call: CallSlot, size: Size) -> CandidateContract:
        # Controls have peer=None and thus the complete-world candidate shape.
        return candidate_contract(self.task, size, call.peer)

    @property
    def component(self) -> str:
        if self.phase == "prefix":
            return "prefix"
        if self.phase == "control":
            return "controls"
        if self.replicate == 1:
            return "repeat"
        if self.event == "preserving":
            return "preserving"
        if self.policy in ("P_G", "P_H"):
            return "masks"
        if self.policy in ("B_delta", "C_delta", "K_delta"):
            return "receipts"
        if self.policy in ("Q_B", "Q_C"):
            return "prose_delay"
        return "revised" if self.event == "revision" else "sham"


@dataclass(frozen=True)
class Schedules:
    format_version: int
    master_seed: int
    size: Size
    main: tuple[Branch, ...]
    development: tuple[Branch, ...]

    def main_for(self, population: Population, count: int = 60) -> tuple[Branch, ...]:
        """The nested 40 keeps the same IDs/parents/seeds; no second slot store."""
        if self.master_seed != population.master_seed or self.size is not population.size:
            raise ValueError("schedule population/configuration differs")
        selected = {w.world_id for w in population.worlds(count)}
        return tuple(b for b in self.main if b.world_id in selected)

    @property
    def capability(self) -> tuple[tuple[Branch, CallSlot], ...]:
        """Select the first 80 prefix plus ten control opportunities, before recovery."""
        return tuple((b, c) for b, c in iter_calls(self.development) if b.phase != "continuation")


def iter_calls(branches: tuple[Branch, ...]) -> Iterator[tuple[Branch, CallSlot]]:
    for branch in branches:
        for call in branch.calls:
            yield branch, call


def component_counts(branches: tuple[Branch, ...]) -> dict[str, tuple[int, int]]:
    """Component -> (distinct generation slots, logical opportunities), no attempts."""
    counts: dict[str, list[int]] = {}
    for branch, call in iter_calls(branches):
        row = counts.setdefault(branch.component, [0, 0])
        row[0] += call.replay_parent is None
        row[1] += 1
    return {component: tuple(row) for component, row in counts.items()}


def _branch_keys(world: PreparedWorld) -> Iterator[tuple[str, str, str | None, int]]:
    """The declared matrix, shared by preparation and structural validation.

    Acceptance tests independently enumerate the matrix and component arithmetic.
    Development deliberately has fewer masks, no extra replicate, and two
    preserving worlds rather than the sixteen main worlds.
    """
    yield "prefix", "original", None, 0
    yield "control", "original", None, 0
    yield "control", "revision", None, 0
    for event, policies in (("revision", ("L", "B", "C", "K", "F")),
                            ("sham", ("B", "C", "K"))):
        for policy in policies:
            yield "continuation", event, policy, 0
    if not world.development or world.world.task in (Task.PREFIX, Task.BFS):
        for event in ("revision", "sham"):
            for policy in ("P_G", "P_H"):
                yield "continuation", event, policy, 0
    if world.world.task in (Task.PREFIX, Task.SORT):
        for policy in ("B_delta", "C_delta", "K_delta"):
            yield "continuation", "revision", policy, 0
    if world.world.task in (Task.SORT, Task.BFS):
        for event in ("revision", "sham"):
            for policy in ("Q_B", "Q_C"):
                yield "continuation", event, policy, 0
    if world.world.task in (Task.TOP_K, Task.BFS) and world.index <= 8:
        for policy in ("B", "C", "K"):
            yield "continuation", "preserving", policy, 0
    if not world.development and world.index <= 2:
        for event in ("revision", "sham"):
            for policy in ("B", "C", "K", "P_G", "P_H"):
                yield "continuation", event, policy, 1


def _replay_parent(world: PreparedWorld, event: str, policy: str | None,
                   replicate: int, round_number: int, peer: int | None) -> str | None:
    if round_number != 1:
        return None
    if policy in ("P_G", "P_H"):
        reset_group = world.partition[0 if policy == "P_G" else 1]
        parent_policy = "C" if peer in reset_group else "B"
    elif policy in ("Q_B", "Q_C"):
        parent_policy = policy[2:]
    else:
        return None
    return _call_id(_branch_id(world.world_id, "continuation", event, parent_policy, replicate), 1, peer)


def _seed(world: PreparedWorld, phase: str, event: str,
          replicate: int, round_number: int, peer: int | None) -> int:
    if phase == "control":
        return world.streams.controls[0 if event == "original" else 1]
    if phase == "prefix":
        return world.streams.prefix_seed(round_number, peer)
    return world.streams.continuation_seed(replicate, round_number, peer)


def _prepare_branches(worlds: tuple[PreparedWorld, ...]) -> tuple[Branch, ...]:
    branches = []
    # All prefixes/controls come first. This makes the development capability
    # block exactly the first 90 slots, without adding an execution worker.
    for phase_group in (("prefix",), ("control",), ("continuation",)):
        for world in worlds:
            for phase, event, policy, replicate in _branch_keys(world):
                if phase not in phase_group:
                    continue
                branch_id = _branch_id(world.world_id, phase, event, policy, replicate)
                positions = ((1, None),) if phase == "control" else tuple(
                    (r, p) for r in range(1, 5) for p in PEERS)
                calls = tuple(CallSlot(_call_id(branch_id, r, p), r, p,
                                       _seed(world, phase, event, replicate, r, p),
                                       _replay_parent(world, event, policy, replicate, r, p))
                              for r, p in positions)
                branches.append(Branch(world.world_id, world.world.task, phase, event, policy,
                                       replicate, _prefix_id(world.world_id) if phase == "continuation" else None,
                                       calls))
    return tuple(branches)


def prepare_schedules(population: Population) -> Schedules:
    validate_population(population)
    return Schedules(1, population.master_seed, population.size,
                     _prepare_branches(population.main), _prepare_branches(population.development))


def dependency_order(branches: tuple[Branch, ...]) -> tuple[tuple[Branch, CallSlot], ...]:
    """CPU topological order of calls, previous-round barriers and prefix parents.

    This is an admissible dry order, not a worker/device assignment. Replay
    requires only its saved first-round reply, not completion of the B/C branch.
    The runner must additionally commit delivery barriers before advancing.
    """
    by_branch = {b.branch_id: b for b in branches}
    calls = tuple(iter_calls(branches))
    by_call = {c.call_id: i for i, (_, c) in enumerate(calls)}
    if len(by_branch) != len(branches) or len(by_call) != len(calls):
        raise ValueError("duplicate branch/call identity")
    remaining = []
    children: dict[int, list[int]] = defaultdict(list)
    for i, (branch, call) in enumerate(calls):
        parents = set()
        if call.round_number > 1:
            parents.update(_call_id(branch.branch_id, call.round_number - 1, p) for p in PEERS)
        elif branch.prefix_parent is not None:
            if branch.prefix_parent not in by_branch:
                raise ValueError("missing prefix parent")
            parents.update(_call_id(branch.prefix_parent, 4, p) for p in PEERS)
        if call.replay_parent is not None:
            parents.add(call.replay_parent)
        remaining.append(len(parents))
        for parent in parents:
            if parent not in by_call:
                raise ValueError("missing call/replay parent")
            children[by_call[parent]].append(i)
    ready = [i for i, count in enumerate(remaining) if not count]
    heapq.heapify(ready)
    ordered = []
    while ready:
        i = heapq.heappop(ready)
        ordered.append(calls[i])
        for child in children[i]:
            remaining[child] -= 1
            if not remaining[child]:
                heapq.heappush(ready, child)
    if len(ordered) != len(calls):
        raise ValueError("cyclic call dependencies")
    return tuple(ordered)


def _validate_branches(branches: tuple[Branch, ...], worlds: tuple[PreparedWorld, ...]) -> None:
    if type(branches) is not tuple:
        raise ValueError("schedule branches must be an immutable tuple")
    by_world = {w.world_id: w for w in worlds}
    expected = {(w.world_id, *key) for w in worlds for key in _branch_keys(w)}
    seen = set()
    for branch in branches:
        if (type(branch) is not Branch or type(branch.world_id) is not str
                or not isinstance(branch.task, Task) or type(branch.phase) is not str
                or type(branch.event) is not str or type(branch.replicate) is not int
                or (branch.policy is not None and type(branch.policy) is not str)):
            raise ValueError("invalid branch fields")
        key = (branch.world_id, branch.phase, branch.event, branch.policy, branch.replicate)
        if key not in expected or key in seen:
            raise ValueError("duplicate or unprescribed branch")
        seen.add(key)
        world = by_world[branch.world_id]
        prefix = _prefix_id(world.world_id) if branch.phase == "continuation" else None
        if branch.task is not world.world.task or branch.prefix_parent != prefix:
            raise ValueError("branch task/original prefix parent differs")
        positions = ((1, None),) if branch.phase == "control" else tuple(
            (r, p) for r in range(1, 5) for p in PEERS)
        if type(branch.calls) is not tuple or len(branch.calls) != len(positions):
            raise ValueError("branch lacks the complete fixed opportunities")
        for call, (r, peer) in zip(branch.calls, positions):
            if (type(call) is not CallSlot or type(call.call_id) is not str
                    or type(call.round_number) is not int or type(call.seed) is not int
                    or (call.peer is not None and type(call.peer) is not int)
                    or (call.replay_parent is not None and type(call.replay_parent) is not str)):
                raise ValueError("invalid call fields")
            if (call.round_number != r or call.peer != peer
                    or call.call_id != _call_id(branch.branch_id, r, peer)
                    or call.seed != _seed(world, branch.phase, branch.event, branch.replicate, r, peer)):
                raise ValueError("call identity/opportunity/seed differs")
            if call.replay_parent != _replay_parent(world, branch.event, branch.policy,
                                                   branch.replicate, r, peer):
                raise ValueError("required replay parent differs in world/event/replicate/peer/policy")
    if seen != expected:
        raise ValueError("schedule is missing required branches")
    dependency_order(branches)


def validate_schedules(schedules: Schedules, population: Population) -> None:
    """Validate both complete main counts and exact pilot without building again."""
    validate_population(population)
    if (type(schedules.format_version) is not int or schedules.format_version != 1
            or type(schedules.master_seed) is not int or schedules.master_seed != population.master_seed
            or schedules.size is not population.size):
        raise ValueError("schedule population/configuration differs")
    _validate_branches(schedules.main, population.main)
    _validate_branches(schedules.main_for(population, 40), population.worlds(40))
    _validate_branches(schedules.development, population.development)
    first = tuple(iter_calls(schedules.development))[:CAPABILITY_CALLS]
    if (len(schedules.capability) != CAPABILITY_CALLS or first != schedules.capability
            or any(c.replay_parent is not None for _, c in first)):
        raise ValueError("development must begin with exactly the 90 prefix/control calls")
