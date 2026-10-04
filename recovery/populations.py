"""Prepared host populations, not an accepted M5 freeze (spec §§2.2–2.3, 6).

No model outcomes are accepted by this API. Target/fallback WORLD COUNTS are
views of one 60-world preparation, independent of the declared mathematical
Size (m=8/6). Full raw worlds and future edits stay host-side, never in views.
"""

from dataclasses import dataclass
from random import Random

from .edits import Edit, apply_edit, legal_edits, select_edit
from .tasks import PEERS, Size, Task, World, generate_world

MAX_ATTEMPTS = 1_000
FAMILIES = tuple(Task)
PARTITIONS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def _root(master_seed: int) -> int:
    if type(master_seed) is not int or master_seed < 0:
        raise ValueError("master_seed must be a nonnegative integer")
    # Disjoint integer slots, not process hashes, mutable RNG spawning, or IDs
    # derived from content. 65 worlds * 4096 fits within each 2**20 root block.
    return master_seed * 2**20


def owner_seed(master_seed: int, task: Task, *, development: bool = False) -> int:
    return _root(master_seed) + 1 + FAMILIES.index(task) + (5 if development else 0)


def owner_order(master_seed: int, task: Task) -> tuple[int, ...]:
    rng = Random(owner_seed(master_seed, task))
    result = []
    for _ in range(3):
        block = list(PEERS)
        rng.shuffle(block)
        result.extend(block)
    return tuple(result)


def draw_partition(rng: Random) -> tuple[tuple[int, int], tuple[int, int]]:
    """Uniform unordered two-pair partition; G is always the pair with peer 0."""

    return rng.choice(PARTITIONS)


SeedRounds = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class Streams:
    generation: int
    ownership: int
    main_edit: int
    preserving_edit: int
    partition: int
    prefix: SeedRounds
    continuation: tuple[SeedRounds, ...]
    controls: tuple[int, int]

    def prefix_seed(self, round_number: int, peer: int) -> int:
        _check_slot(round_number, peer)
        return self.prefix[round_number - 1][peer]

    def continuation_seed(self, replicate: int, round_number: int, peer: int) -> int:
        # Event/policy are intentionally absent: all siblings match this seed.
        _check_slot(round_number, peer)
        if type(replicate) is not int or not 0 <= replicate < len(self.continuation):
            raise ValueError("continuation replicate is not assigned for this world")
        return self.continuation[replicate][round_number - 1][peer]


def _check_slot(round_number: int, peer: int) -> None:
    if (type(round_number) is not int or not 1 <= round_number <= 4
            or type(peer) is not int or peer not in PEERS):
        raise ValueError("invalid round/peer")


def streams_for(master_seed: int, task: Task, index: int, *, development: bool = False) -> Streams:
    if not isinstance(task, Task) or type(development) is not bool:
        raise ValueError("invalid task/development domain")
    if type(index) is not int or not 1 <= index <= (1 if development else 12):
        raise ValueError("world index outside the prepared population")
    slot = 60 + FAMILIES.index(task) if development else FAMILIES.index(task) * 12 + index - 1
    base = _root(master_seed) + (slot + 1) * 4096
    prefix = tuple(tuple(base + 16 + 4 * r + p for p in PEERS) for r in range(4))
    replicates = 1 if development or index > 2 else 2
    continuation = tuple(tuple(tuple(base + 32 + 16 * k + 4 * r + p for p in PEERS)
                               for r in range(4)) for k in range(replicates))
    return Streams(base, base + 1, base + 2, base + 3, base + 4,
                   prefix, continuation, (base + 64, base + 65))


@dataclass(frozen=True)
class Rejection:
    attempt: int
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Eligibility:
    main_records: tuple[str, ...]
    preserving_pairs: int


@dataclass(frozen=True)
class PreparedWorld:
    world_id: str
    index: int
    development: bool
    edited_owner: int
    world: World
    main_edit: Edit
    preserving_edit: Edit | None
    partition: tuple[tuple[int, int], tuple[int, int]]
    streams: Streams
    eligibility: Eligibility
    rejections: tuple[Rejection, ...]

    @property
    def attempts(self) -> int:
        return len(self.rejections) + 1

    def event_world(self, event: str) -> World:
        """All event siblings use this immutable original, never another event."""

        if event == "revision":
            return apply_edit(self.world, self.main_edit)
        if event == "sham":
            return apply_edit(self.world, None)
        if event == "preserving" and self.preserving_edit is not None:
            return apply_edit(self.world, self.preserving_edit)
        raise ValueError("event not available for this world")


class PopulationExhausted(ValueError):
    """Keep the exhausted world's ID/owner and every failed attempt available."""

    def __init__(self, world_id: str, owner: int, rejections: tuple[Rejection, ...]):
        self.world_id, self.owner, self.rejections = world_id, owner, rejections
        super().__init__(f"{world_id}: exhausted {MAX_ATTEMPTS} generation attempts for owner {owner}")


def prepare_world(master_seed: int, task: Task, size: Size, index: int,
                  edited_owner: int, *, development: bool = False) -> PreparedWorld:
    if type(edited_owner) is not int or edited_owner not in PEERS:
        raise ValueError("invalid edited owner")
    streams = streams_for(master_seed, task, index, development=development)
    domain = "dev" if development else "main"
    world_id = f"{domain}-{task.value}-{index:02d}"
    generation, ownership = Random(streams.generation), Random(streams.ownership)
    rejections = []
    for attempt in range(1, MAX_ATTEMPTS + 1):
        world = generate_world(task, size, generation_rng=generation, ownership_rng=ownership)
        main = legal_edits(world, owner=edited_owner)
        preserving = legal_edits(world, preserving=True)
        reasons = []
        if not main:
            reasons.append("no_owner_changing_edit")
        if task in (Task.TOP_K, Task.BFS) and not preserving:
            reasons.append("no_preserving_edit")
        if reasons:
            rejections.append(Rejection(attempt, tuple(reasons)))
            continue
        return PreparedWorld(world_id, index, development, edited_owner, world,
                             select_edit(main, Random(streams.main_edit)),
                             select_edit(preserving, Random(streams.preserving_edit), preserving=True)
                             if preserving else None,
                             draw_partition(Random(streams.partition)), streams,
                             Eligibility(tuple(dict.fromkeys(e.record_id for e in main)), len(preserving)),
                             tuple(rejections))
    raise PopulationExhausted(world_id, edited_owner, tuple(rejections))


@dataclass(frozen=True)
class Population:
    format_version: int
    master_seed: int
    size: Size
    owner_seeds: tuple[int, ...]
    development_owner_seeds: tuple[int, ...]
    main: tuple[PreparedWorld, ...]
    development: tuple[PreparedWorld, ...]

    def worlds(self, count: int = 60) -> tuple[PreparedWorld, ...]:
        if type(count) is not int or count not in (60, 40):
            raise ValueError("world count must be 60 or the nested 40")
        return tuple(w for w in self.main if w.index <= count // 5)

    def subsets(self, count: int = 60) -> dict[str, tuple[str, ...]]:
        worlds = self.worlds(count)
        return {
            "main": tuple(w.world_id for w in worlds),
            "receipt": tuple(w.world_id for w in worlds if w.world.task in (Task.PREFIX, Task.SORT)),
            "q": tuple(w.world_id for w in worlds if w.world.task in (Task.SORT, Task.BFS)),
            "preserving": tuple(w.world_id for w in worlds
                                if w.world.task in (Task.TOP_K, Task.BFS) and w.index <= 8),
            "repeat": tuple(w.world_id for w in worlds if w.index <= 2),
        }


def prepare_population(master_seed: int, size: Size) -> Population:
    """Prepare all 60 + five disjoint development worlds; 40 is a saved view."""

    _root(master_seed)
    if not isinstance(size, Size):
        raise ValueError("invalid mathematical size")
    # Owner orders are fixed before any eligibility-conditioned world generation.
    orders = {task: owner_order(master_seed, task) for task in FAMILIES}
    main = tuple(prepare_world(master_seed, task, size, index, owner)
                 for task in FAMILIES for index, owner in enumerate(orders[task], 1))
    development = tuple(prepare_world(master_seed, task, size, 1,
                                     Random(owner_seed(master_seed, task, development=True)).randrange(4),
                                     development=True) for task in FAMILIES)
    return Population(1, master_seed, size,
                      tuple(owner_seed(master_seed, task) for task in FAMILIES),
                      tuple(owner_seed(master_seed, task, development=True) for task in FAMILIES),
                      main, development)


def validate_population(population: Population) -> None:
    """Check loaded structure/math/assigned streams, without generating any world.

    Detect changed valid inputs by comparison with the saved authoritative
    manifest (manifests.assert_matches). Mathematical validity alone cannot prove
    an input is unchanged, nor can seeds replace the saved actual inputs.
    """

    p = population
    if type(p.format_version) is not int or p.format_version != 1 or not isinstance(p.size, Size):
        raise ValueError("unsupported population configuration")
    _root(p.master_seed)
    if (any(type(values) is not tuple for values in
            (p.owner_seeds, p.development_owner_seeds, p.main, p.development))
            or any(type(seed) is not int for seed in p.owner_seeds + p.development_owner_seeds)):
        raise ValueError("population collections/seeds must have exact immutable types")
    if (p.owner_seeds != tuple(owner_seed(p.master_seed, t) for t in FAMILIES)
            or p.development_owner_seeds != tuple(owner_seed(p.master_seed, t, development=True) for t in FAMILIES)):
        raise ValueError("owner seed assignments differ")
    if len(p.main) != 60 or len(p.development) != 5:
        raise ValueError("population must contain 60 main and five development worlds")
    expected = [(False, t, i) for t in FAMILIES for i in range(1, 13)]
    expected += [(True, t, 1) for t in FAMILIES]
    for w, (development, task, index) in zip(p.main + p.development, expected):
        domain = "dev" if development else "main"
        owner = (Random(owner_seed(p.master_seed, task, development=True)).randrange(4)
                 if development else owner_order(p.master_seed, task)[index - 1])
        if (type(w.index) is not int or type(w.development) is not bool
                or type(w.edited_owner) is not int or type(w.world_id) is not str
                or w.world_id != f"{domain}-{task.value}-{index:02d}" or w.index != index
                or w.development != development or w.world.task is not task
                or w.world.size is not p.size or w.edited_owner != owner):
            raise ValueError("world identity/configuration/edited owner differs")
        if w.streams != streams_for(p.master_seed, task, index, development=development):
            raise ValueError("world random stream assignments differ")
        scalar_seeds = (w.streams.generation, w.streams.ownership, w.streams.main_edit,
                        w.streams.preserving_edit, w.streams.partition)
        all_seeds = scalar_seeds + w.streams.controls
        all_seeds += tuple(seed for row in w.streams.prefix for seed in row)
        all_seeds += tuple(seed for repeat in w.streams.continuation for row in repeat for seed in row)
        if any(type(seed) is not int for seed in all_seeds):
            raise ValueError("random seeds must be exact integers")
        if w.partition != draw_partition(Random(w.streams.partition)):
            raise ValueError("world partition differs")
        if any(type(peer) is not int for pair in w.partition for peer in pair):
            raise ValueError("partition peers must be exact integers")
        main = legal_edits(w.world, owner=owner)
        preserving = legal_edits(w.world, preserving=True)
        if not main or (task in (Task.TOP_K, Task.BFS) and not preserving):
            raise ValueError("world violates eligibility conditioning")
        if (type(w.eligibility.preserving_pairs) is not int
                or w.eligibility != Eligibility(tuple(dict.fromkeys(e.record_id for e in main)), len(preserving))):
            raise ValueError("saved eligibility differs from actual inputs")
        if (w.main_edit != select_edit(main, Random(w.streams.main_edit))
                or (task is not Task.BFS and type(w.main_edit.replacement) is not int)):
            raise ValueError("main edit differs from assigned selection")
        expected_preserving = (select_edit(preserving, Random(w.streams.preserving_edit), preserving=True)
                               if preserving else None)
        if (w.preserving_edit != expected_preserving
                or (task is Task.TOP_K and type(w.preserving_edit.replacement) is not int)):
            raise ValueError("preserving edit differs from assigned selection")
        if w.attempts > MAX_ATTEMPTS:
            raise ValueError("generation attempts exceed ceiling")
        for attempt, rejection in enumerate(w.rejections, 1):
            if (type(rejection.attempt) is not int or rejection.attempt != attempt or not rejection.reasons
                    or rejection.reasons not in (("no_owner_changing_edit",),
                                                ("no_preserving_edit",),
                                                ("no_owner_changing_edit", "no_preserving_edit"))
                    or task not in (Task.TOP_K, Task.BFS)):
                raise ValueError("invalid rejection accounting")
