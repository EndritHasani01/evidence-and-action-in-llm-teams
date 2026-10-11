"""Explicit 0/1/unknown formula fixtures, independent of runner/model behavior."""

from recovery.evaluate import trajectory
from functools import cache

from recovery.manifests import load_population, load_schedules
from recovery.schedule import prepare_schedules
from recovery.tasks import candidate_contract
from recovery.truth import changed_coordinates, solve_world
from tests.outcome_fixture import ROOT, prepared as target_prepared


@cache
def prepared(size="target"):
    if size == "target":
        return target_prepared(size)
    population = load_population(ROOT / f"tests/fixtures/population_{size}.json")
    if size == "course":
        return population, load_schedules(ROOT / "tests/fixtures/schedules_course.json", population)
    return population, prepare_schedules(population)


def selection(task=None, index=3, size="fallback", worlds=None):
    population, schedules = prepared(size)
    worlds = tuple(worlds) if worlds is not None else tuple(w for w in population.main
        if w.world.task is task and w.index == index)
    ids = {w.world_id for w in worlds}
    return worlds, tuple(b for b in schedules.main if b.world_id in ids)


def tables(worlds, branches, matrices=None):
    """Matrices keyed by (world ID, event, policy, replicate); default all zero.

    Required round-one replay follows the scheduled parent. Preservation is a
    separate synthetic coordinate rate, with a valid fully correct old prefix.
    Saved-record scoring and real source/prose are exercised in integration tests.
    """
    matrices = matrices or {}
    by_world, by_branch = {w.world_id: w for w in worlds}, {b.branch_id: b for b in branches}
    values = {}
    for branch in branches:
        matrix = matrices.get((branch.world_id, branch.event, branch.policy, branch.replicate), zeros())
        for call in branch.calls:
            values[call.call_id] = (1 if branch.phase in ("prefix", "control") else
                                   matrix[call.round_number - 1][call.peer])
    for branch in branches:
        for call in branch.calls:
            if call.replay_parent:
                values[call.call_id] = values[call.replay_parent]
    outcomes, diagnostics, trajectories = [], [], []
    for branch in branches:
        world = by_world[branch.world_id]
        prefix = by_branch.get(branch.prefix_parent)
        old = solve_world(world.world)
        new = old if branch.event == "original" else solve_world(world.event_world(branch.event))
        U = changed_coordinates(old, new).unchanged
        base = {"world_id": world.world_id, "branch_id": branch.branch_id, "family": branch.task.value,
            "size": world.world.size.value, "phase": branch.phase, "event": branch.event, "policy": branch.policy,
            "replicate": branch.replicate, "prefix_parent": branch.prefix_parent}
        for call in branch.calls:
            correct = values[call.call_id]
            prefix_id = next(c.call_id for c in prefix.calls if c.peer == call.peer and c.round_number == 4) if prefix else None
            row = dict(base, call_id=call.call_id, generation_id=call.generation_id, replay_parent=call.replay_parent,
                round=call.round_number, peer=call.peer, seed=call.seed, prefix_call_id=prefix_id, correct=correct,
                protocol_outcome="unknown" if correct is None else "valid")
            outcomes.append(row)
            if branch.phase == "continuation":
                coordinates = [j for j in candidate_contract(new.task, new.size, call.peer).coordinates if j in U]
                d = len(coordinates)
                diagnostics.append(dict(row, metric="preservation", denominator=d,
                    numerator=None if correct is None else correct * d, rate=None if correct is None or not d else correct,
                    eligible_coordinates=coordinates, reason="slot_unknown" if correct is None else
                        "no_unchanged_coordinates" if not d else None))
        if branch.phase != "control":
            matrix = [[values[c.call_id] for c in branch.calls if c.round_number == r] for r in range(1, 5)]
            trajectories.append(dict(base, **trajectory(matrix)))
    return {"outcomes": outcomes, "peer_diagnostics": diagnostics, "trajectories": trajectories}


def zeros():
    return [[0] * 4 for _ in range(4)]


def constant(peers):
    return [list(peers) for _ in range(4)]


def correct_rounds(count):
    return [[int(r < count)] * 4 for r in range(4)]


def group_matrix(world, G, H):
    row = [0] * 4
    for peers, values in zip(world.partition, (G, H)):
        for peer, value in zip(peers, values):
            row[peer] = value
    return constant(row)
