"""Offline mathematical solvers and exact grading. Never pass Truth to peer views."""

from collections import deque
from dataclasses import dataclass
from typing import Iterable, Sequence

from .tasks import Size, Task, World, candidate_contract, coordinate_map


def top_k(values: Sequence[int]) -> list[int]:
    if len(values) < 10:
        raise ValueError("Top-K requires at least ten inputs")
    return sorted(values, reverse=True)[:10]


def prefix_sums(values: Sequence[int]) -> list[int]:
    total = 0
    result = []
    for value in values:
        total += value
        result.append(total)
    return result


def differences(values: Sequence[int]) -> list[int]:
    return [values[j] - values[j - 1] for j in range(1, len(values))]


def sorted_values(values: Sequence[int]) -> list[int]:
    return sorted(values)


def bfs_distances(node_count: int, edges: Iterable[tuple[int, int]]) -> dict[str, int]:
    """Unweighted undirected distances from node 0, including unreachable -1."""

    adjacency = [[] for _ in range(node_count)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    distances = [-1] * node_count
    distances[0] = 0
    queue = deque([0])
    while queue:
        node = queue.popleft()
        for neighbor in adjacency[node]:
            if distances[neighbor] == -1:
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)
    return {str(j): value for j, value in enumerate(distances)}


@dataclass(frozen=True)
class Truth:
    task: Task
    size: Size
    values: tuple[int, ...]

    def __post_init__(self) -> None:
        coords = coordinate_map(self.task, self.size).coordinates
        if (type(self.values) is not tuple or len(self.values) != len(coords)
                or any(type(value) is not int for value in self.values)):
            raise ValueError("invalid evaluator truth")

    @property
    def by_coordinate(self) -> dict[int, int]:
        return dict(zip(coordinate_map(self.task, self.size).coordinates, self.values))

    def candidate(self, peer: int | None = None) -> list[int] | dict[str, int]:
        contract = candidate_contract(self.task, self.size, peer)
        values = self.by_coordinate
        if self.task is Task.BFS:
            return {str(j): values[j] for j in contract.coordinates}
        return [values[j] for j in contract.coordinates]


def solve_world(world: World) -> Truth:
    if world.task is Task.BFS:
        distances = bfs_distances(world.size.node_count,
                                  (r.value for r in world.records if not r.deleted))
        values = tuple(distances[str(j)] for j in range(world.size.node_count))
    else:
        raw = [r.value for r in sorted(world.records, key=lambda r: r.position)]
        if world.task is Task.TOP_K:
            result = top_k(raw)
        elif world.task is Task.PREFIX:
            result = prefix_sums(raw)
        elif world.task is Task.DIFFERENCE:
            result = differences(raw)
        else:
            result = sorted_values(raw)
        values = tuple(result)
    return Truth(world.task, world.size, values)


def exact_candidate(truth: Truth, candidate: object, peer: int | None = None,
                    *, protocol_valid: bool = True) -> bool:
    """Grade a recorded candidate; full reply validity comes from the M2 protocol.

    A caller with an invalid reply must pass protocol_valid=False. This function
    neither parses replies nor classifies an unexecuted slot as a failed result.
    """

    contract = candidate_contract(truth.task, truth.size, peer)
    return (protocol_valid is True and contract.error(candidate) is None
            and candidate == truth.candidate(peer))


@dataclass(frozen=True)
class CoordinateChanges:
    changed: frozenset[int]
    unchanged: frozenset[int]


def changed_coordinates(old: Truth, new: Truth) -> CoordinateChanges:
    """Evaluator-only D/U on unique coordinates, independently of peer copies."""

    if old.task is not new.task or old.size is not new.size:
        raise ValueError("old/new truth must have the same task and size")
    old_values, new_values = old.by_coordinate, new.by_coordinate
    changed = frozenset(j for j in old_values if old_values[j] != new_values[j])
    return CoordinateChanges(changed, frozenset(old_values) - changed)
