"""Permitted course protocol fixtures derived from the saved actual inputs."""

from dataclasses import replace
from pathlib import Path

from recovery.manifests import load_population
from recovery.state import (CandidateState, Feedback, HistoricalReceipt, OwnReply,
                            ReceivedProse, RevisionNotice, Slot, initial_view, revise_source)
from tests.peer_view_cases import SPECIAL_TEXT

ROOT = Path(__file__).resolve().parents[1]


def course_population():
    return load_population(ROOT / "tests/fixtures/population_course.json")


def course_renderer_cases():
    worlds = {w.world.task.value: w.world for w in course_population().main if w.index == 1}
    cases = {name: initial_view(world, 0) for name, world in worlds.items()}
    base = cases["prefix_sum"]
    old = next(r for r in worlds["prefix_sum"].records if r.owner != 0)
    public = next(r for r in base.manifest if r.record_id == old.record_id)
    new = replace(old, version=2, value=1 if old.value != 1 else 9)
    ordinary = revise_source(replace(base, slot=Slot("recovery", 1)),
                             RevisionNotice(public, 1, 2), replacement=new)
    # Genuine archived before-values remain outside clearable history.
    ordinary = replace(ordinary, slot=Slot("recovery", 1),
        receipt=HistoricalReceipt(public, 1, 2),
        history=(OwnReply(Slot("prefix", 4), SPECIAL_TEXT),
                 ReceivedProse(Slot("prefix", 4), 1, SPECIAL_TEXT.replace("\ud800", ""))),
        feedback=(Feedback(Slot("prefix", 4), "json"),),
        candidate=CandidateState("invalid", Slot("prefix", 4)))
    cases["ordinary_receipt"] = ordinary
    disclosed = replace(ordinary, receipt=HistoricalReceipt(public, 1, 2, old.value))
    cases["disclosed_receipt"] = disclosed
    cases["compact_wrong"] = replace(disclosed, history=(), feedback=(),
        candidate=CandidateState.valid(base.task, base.size, 0, Slot("prefix", 4),
                                       [-999] * 6, historical=True))
    cases["compact_absence"] = replace(cases["compact_wrong"],
        candidate=CandidateState("failed", Slot("prefix", 4), historical=True))
    graph = worlds["bfs_distance"]
    old = next(r for r in graph.records if r.owner != 0)
    public = next(r for r in cases["bfs_distance"].manifest if r.record_id == old.record_id)
    base = replace(cases["bfs_distance"], slot=Slot("recovery", 1))
    notice = RevisionNotice(public, 1, 2)
    cases["pending_edge"] = revise_source(base, notice, replacement=None)
    cases["known_tombstone"] = revise_source(base, notice,
        replacement=replace(old, version=2, deleted=True))
    return cases
