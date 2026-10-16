"""Host-owned worlds and public coordinate/candidate contracts (spec §2.1).

SILO-derived mathematics: I-09, II-11, II-17, III-21, III-24. See
tests/fixtures/README.md for attribution and the deliberately changed distributions.
No vendor generators, runner, scorer, model stack, or archive code are imported.
Worlds contain raw inputs only; gold and changed coordinates live in truth.py.
"""

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from random import Random

PEERS = (0, 1, 2, 3)


class Task(str, Enum):
    TOP_K = "top_k"
    PREFIX = "prefix_sum"
    DIFFERENCE = "difference_array"
    SORT = "distributed_sort"
    BFS = "bfs_distance"


class Size(str, Enum):
    TARGET = "target"
    FALLBACK = "fallback"

    @property
    def shard_size(self) -> int:
        return 8 if self is Size.TARGET else 6

    @property
    def numeric_length(self) -> int:
        return 4 * self.shard_size

    @property
    def node_count(self) -> int:
        return 12 if self is Size.TARGET else 8

    @property
    def edge_count(self) -> int:
        return self.node_count - 1 + 5


def _check_task_size(task: Task, size: Size) -> None:
    if not isinstance(task, Task) or not isinstance(size, Size):
        raise ValueError("task and size must be declared Task/Size members")


def numeric_range(task: Task) -> tuple[int, int]:
    if task is Task.PREFIX:
        return 1, 9
    if task is Task.DIFFERENCE:
        return 0, 30
    if task in (Task.TOP_K, Task.SORT):
        return 0, 99
    raise ValueError("not a declared numeric task")


@dataclass(frozen=True)
class SourceRecord:
    record_id: str
    owner: int
    position: int | None
    value: int | tuple[int, int]
    version: int = 1
    deleted: bool = False


@dataclass(frozen=True)
class PublicSource:
    """Public identity/ownership, never a value or private edge endpoint."""

    record_id: str
    owner: int
    position: int | None


@dataclass(frozen=True)
class World:
    """Immutable host input, including stable slots for BFS deletion tombstones.

    Construction validates dimensions, raw types/ranges, ownership and identity.
    Connectivity is a generator guarantee, not a constraint on revised worlds.
    Future edit/population information is not part of this mathematical record.
    """

    task: Task
    size: Size
    records: tuple[SourceRecord, ...]

    def __post_init__(self) -> None:
        _check_task_size(self.task, self.size)
        if type(self.records) is not tuple:
            raise ValueError("records must be an immutable tuple")
        bfs = self.task is Task.BFS
        count = self.size.edge_count if bfs else self.size.numeric_length
        if len(self.records) != count:
            raise ValueError("wrong source-record count")
        ids: set[str] = set()
        positions: set[int] = set()
        edges: set[tuple[int, int]] = set()
        owners = [0] * 4
        for record in self.records:
            if not isinstance(record, SourceRecord):
                raise ValueError("invalid source record")
            if type(record.owner) is not int or record.owner not in PEERS:
                raise ValueError("invalid source owner")
            if type(record.version) is not int or record.version < 1:
                raise ValueError("invalid source version")
            if type(record.deleted) is not bool:
                raise ValueError("invalid deletion flag")
            if type(record.record_id) is not str or record.record_id in ids:
                raise ValueError("invalid or duplicate source ID")
            ids.add(record.record_id)
            owners[record.owner] += 1
            if bfs:
                if record.position is not None:
                    raise ValueError("BFS has no public edge position")
                if record.deleted and record.version == 1:
                    raise ValueError("an initial edge cannot be a tombstone")
                edge = record.value
                if (type(edge) is not tuple or len(edge) != 2
                        or any(type(v) is not int for v in edge)
                        or not 0 <= edge[0] < edge[1] < self.size.node_count):
                    raise ValueError("edge must have canonical distinct endpoints")
                if edge in edges:
                    raise ValueError("duplicate undirected edge")
                edges.add(edge)
            else:
                if record.deleted:
                    raise ValueError("numeric records cannot be deleted")
                pos = record.position
                if (type(pos) is not int or not 0 <= pos < count
                        or pos in positions):
                    raise ValueError("invalid or duplicate numeric position")
                positions.add(pos)
                low, high = numeric_range(self.task)
                if type(record.value) is not int or not low <= record.value <= high:
                    raise ValueError("raw value outside the declared integer range")
                if (self.task in (Task.PREFIX, Task.DIFFERENCE)
                        and record.owner != pos // self.size.shard_size):
                    raise ValueError("contiguous task source owner disagrees with position")
                if record.record_id != f"x{pos:03d}":
                    raise ValueError("numeric IDs must identify public positions")
        per_peer = count // 4
        if owners != [per_peer] * 4:
            raise ValueError("source ownership must be equal")
        if bfs and ids != {f"e{i:03d}" for i in range(count)}:
            raise ValueError("BFS IDs must use opaque edge slots")


def source_manifest(world: World) -> tuple[PublicSource, ...]:
    return tuple(PublicSource(r.record_id, r.owner, r.position)
                 for r in sorted(world.records, key=lambda r: r.record_id))


@dataclass(frozen=True)
class CoordinateMap:
    """Unique outputs and ordered assignments; replicas do not add coordinates."""

    coordinates: tuple[int, ...]
    peer_coordinates: tuple[tuple[int, ...], ...]

    @property
    def coordinate_peers(self) -> dict[int, tuple[int, ...]]:
        return {j: tuple(i for i in PEERS if j in self.peer_coordinates[i])
                for j in self.coordinates}


def coordinate_map(task: Task, size: Size) -> CoordinateMap:
    _check_task_size(task, size)
    if task is Task.TOP_K:
        coords = tuple(range(10))
    elif task is Task.DIFFERENCE:
        # d_j has coordinate j, and Python list index j-1.
        coords = tuple(range(1, size.numeric_length))
    elif task is Task.BFS:
        coords = tuple(range(size.node_count))
    else:
        coords = tuple(range(size.numeric_length))
    if task in (Task.PREFIX, Task.SORT):
        m = size.shard_size
        assigned = tuple(coords[i * m:(i + 1) * m] for i in PEERS)
    else:
        assigned = (coords,) * 4
    return CoordinateMap(coords, assigned)


@dataclass(frozen=True)
class CandidateContract:
    """Public shape only. Shape validity never certifies mathematical correctness."""

    task: Task
    coordinates: tuple[int, ...]

    def error(self, candidate: object) -> str | None:
        if self.task is Task.BFS:
            if type(candidate) is not dict:
                return "candidate_object_required"
            if (any(type(key) is not str for key in candidate)
                    or set(candidate) != {str(j) for j in self.coordinates}):
                return "candidate_node_keys"
            values = candidate.values()
        else:
            if type(candidate) is not list:
                return "candidate_list_required"
            if len(candidate) != len(self.coordinates):
                return "candidate_length"
            values = candidate
        if any(type(value) is not int for value in values):
            return "candidate_integer_required"
        return None


def candidate_contract(task: Task, size: Size, peer: int | None = None) -> CandidateContract:
    """peer=None denotes the complete-world full-information control contract."""

    mapping = coordinate_map(task, size)
    if peer is None:
        coords = mapping.coordinates
    else:
        if type(peer) is not int or peer not in PEERS:
            raise ValueError("invalid peer")
        coords = mapping.peer_coordinates[peer]
    return CandidateContract(task, coords)


def _prufer_tree(node_count: int, rng: Random) -> set[tuple[int, int]]:
    """IID uniform Prüfer labels bijectively select a uniform labeled tree."""

    sequence = [rng.randrange(node_count) for _ in range(node_count - 2)]
    degree = [1] * node_count
    for node in sequence:
        degree[node] += 1
    edges = set()
    for node in sequence:
        leaf = next(v for v in range(node_count) if degree[v] == 1)
        edges.add(tuple(sorted((leaf, node))))
        degree[leaf] -= 1
        degree[node] -= 1
    leaves = [v for v in range(node_count) if degree[v] == 1]
    edges.add(tuple(leaves))
    return edges


def generate_world(task: Task, size: Size, *, generation_rng: Random,
                   ownership_rng: Random) -> World:
    """One unconditioned draw. M1-T02 owns eligibility/rejection and saved streams.

    Pass separate caller-owned local RNGs. No global random stream is touched.
    Ownership permutations and BFS ID assignment use only the ownership stream.
    """

    _check_task_size(task, size)
    if (not isinstance(generation_rng, Random) or not isinstance(ownership_rng, Random)
            or generation_rng is ownership_rng):
        raise ValueError("use two separate local Random instances")
    if task is Task.BFS:
        nodes = size.node_count
        tree = _prufer_tree(nodes, generation_rng)
        nonedges = [edge for edge in combinations(range(nodes), 2) if edge not in tree]
        edges = sorted(tree | set(generation_rng.sample(nonedges, 5)))
        # Shuffle BEFORE binding identities/owners: no endpoint-sorted ID rank leaks.
        ownership_rng.shuffle(edges)
        per_peer = size.edge_count // 4
        records = tuple(SourceRecord(f"e{i:03d}", i // per_peer, None, edge)
                        for i, edge in enumerate(edges))
    else:
        n, m = size.numeric_length, size.shard_size
        low, high = numeric_range(task)
        values = [generation_rng.randint(low, high) for _ in range(n)]
        positions = list(range(n))
        if task in (Task.TOP_K, Task.SORT):
            ownership_rng.shuffle(positions)
        owners = {pos: i // m for i, pos in enumerate(positions)}
        records = tuple(SourceRecord(f"x{j:03d}", owners[j], j, value)
                        for j, value in enumerate(values))
    return World(task, size, records)
