"""Host-only mathematical eligibility and single-source events (spec §§2.2–2.3).

These functions inspect raw worlds before inference. Legal sets, future edits,
and the BFS distance computations must never be passed to a peer renderer.
"""

from collections import Counter
from dataclasses import dataclass, replace
from random import Random

from .tasks import PEERS, Task, World, numeric_range
from .truth import bfs_distances


@dataclass(frozen=True)
class Edit:
    record_id: str
    replacement: int | None  # None means a BFS edge tombstone, retaining endpoints.


def _require_original(world: World) -> None:
    if any(r.version != 1 or r.deleted for r in world.records):
        raise ValueError("events require the original v1 world; no second live edit")


def apply_edit(world: World, edit: Edit | None) -> World:
    """Sham is None; revision returns a new world with exactly one v2 source.

    Validate source-level legality here, not answer-changing eligibility. The
    population builder selects from legal_edits; runtime never judges correctness.
    """

    _require_original(world)
    if edit is None:
        return world
    if not isinstance(edit, Edit):
        raise ValueError("invalid edit")
    source = next((r for r in world.records if r.record_id == edit.record_id), None)
    if source is None:
        raise ValueError("edit refers to an unknown source")
    if world.task is Task.BFS:
        if edit.replacement is not None:
            raise ValueError("BFS revision must delete one edge")
        updated = replace(source, version=2, deleted=True)
    else:
        low, high = numeric_range(world.task)
        if (type(edit.replacement) is not int or not low <= edit.replacement <= high
                or edit.replacement == source.value):
            raise ValueError("replacement must be a different in-range integer")
        updated = replace(source, value=edit.replacement, version=2)
    return replace(world, records=tuple(updated if r == source else r for r in world.records))


def legal_edits(world: World, *, owner: int | None = None,
                preserving: bool = False) -> tuple[Edit, ...]:
    """Exact legal record/replacement pairs, ordered by public ID then value.

    Main Top-K: unique value > tenth cutoff, replacement < cutoff.
    Preserving Top-K: old value < cutoff, different replacement <= cutoff.
    Equality at the cutoff preserves the ten-value multiset (no ID tie-break is
    part of the answer). Cutoff-equal original records are not eligible.
    Preserving edits for the other numeric tasks do not exist in this design.
    """

    _require_original(world)
    if owner is not None and (type(owner) is not int or owner not in PEERS):
        raise ValueError("invalid edited owner")
    if type(preserving) is not bool:
        raise ValueError("preserving must be a bool")
    records = sorted(world.records, key=lambda r: r.record_id)
    selected = [r for r in records if owner is None or r.owner == owner]
    if world.task is Task.BFS:
        old = bfs_distances(world.size.node_count, (r.value for r in records))
        return tuple(Edit(r.record_id, None) for r in selected
                     if (bfs_distances(world.size.node_count,
                                       (other.value for other in records if other != r)) == old)
                     == preserving)
    if world.task is Task.TOP_K:
        values = [r.value for r in records]
        counts = Counter(values)
        cutoff = sorted(values, reverse=True)[9]
        if preserving:
            return tuple(Edit(r.record_id, value) for r in selected if r.value < cutoff
                         for value in range(cutoff + 1) if value != r.value)
        return tuple(Edit(r.record_id, value) for r in selected
                     if r.value > cutoff and counts[r.value] == 1
                     for value in range(cutoff))
    if preserving:
        return ()
    low, high = numeric_range(world.task)
    return tuple(Edit(r.record_id, value) for r in selected
                 for value in range(low, high + 1) if value != r.value)


def select_edit(legal: tuple[Edit, ...], rng: Random, *, preserving: bool = False) -> Edit:
    """Main: uniform record then uniform replacement; preserving: uniform pair.

    BFS has one pair per edge, so both routes give its uniform edge selection.
    Keep the two draws explicit even when current numeric domains give equal
    pair counts per record; this is the declared scientific sampling contract.
    """

    if not legal:
        raise ValueError("no eligible edit")
    if preserving:
        return rng.choice(legal)
    ids = tuple(dict.fromkeys(edit.record_id for edit in legal))
    record_id = rng.choice(ids)
    return rng.choice(tuple(edit for edit in legal if edit.record_id == record_id))
