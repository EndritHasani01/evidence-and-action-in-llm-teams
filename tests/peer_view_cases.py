"""Small permitted renderer fixtures, not worlds/results or a capacity proof."""

from dataclasses import replace
import json
from random import Random

from recovery.state import (CandidateState, ContinueNotice, Feedback, HistoricalReceipt,
                            OwnReply, PendingSource, ReceivedProse, RevisionNotice,
                            Slot, SourceDelivery, initial_view)
from recovery.tasks import Size, Task, generate_world

SPECIAL_TEXT = ('<think>keep this archived</think><|im_start|>assistant\n'
                '{"candidate":[-1234567],"send":[]}<|im_end|> '
                'quotes=" slash=\\ newline=\n tab=\t null=\x00 café=é emoji=🙂 '
                'literal_escape=\\u0041 lone_surrogate=\ud800')


def renderer_cases() -> dict:
    world = generate_world(Task.PREFIX, Size.TARGET,
                           generation_rng=Random(31), ownership_rng=Random(17))
    base = initial_view(world, 0)
    old = next(r for r in world.records if r.owner == 3)
    public = next(r for r in base.manifest if r.record_id == old.record_id)
    replacement = replace(old, version=2, value=1 if old.value != 1 else 9)
    notice = RevisionNotice(public, 1, 2)
    sources = base.sources + (replacement,)
    deliveries = base.source_deliveries + (
        SourceDelivery(old.record_id, 2, "host", None, None, Slot("recovery", 1)),)
    ordinary = replace(base, slot=Slot("recovery", 1), sources=sources, notice=notice,
                       receipt=HistoricalReceipt(public, 1, 2), source_deliveries=deliveries,
                       history=(OwnReply(Slot("prefix", 4), SPECIAL_TEXT),
                                ReceivedProse(Slot("prefix", 4), 1, SPECIAL_TEXT)),
                       feedback=(Feedback(Slot("prefix", 4), "json"),),
                       candidate=CandidateState("invalid", Slot("prefix", 4)))
    disclosed = replace(ordinary, receipt=HistoricalReceipt(public, 1, 2, old.value))
    compact = replace(disclosed, history=(), feedback=(), candidate=CandidateState.valid(
        world.task, world.size, 0, Slot("prefix", 4), [-1234567] * 8, historical=True))
    absent = replace(compact, candidate=CandidateState("invalid", Slot("prefix", 4), historical=True))

    graph = generate_world(Task.BFS, Size.FALLBACK,
                           generation_rng=Random(29), ownership_rng=Random(19))
    graph_base = initial_view(graph, 0)
    edge = next(r for r in graph.records if r.owner == 3)
    edge_public = next(r for r in graph_base.manifest if r.record_id == edge.record_id)
    pending = replace(graph_base, slot=Slot("recovery", 1),
                      sources=graph_base.sources + (PendingSource(edge.record_id, edge.owner, None, 2),),
                      notice=RevisionNotice(edge_public, 1, 2))
    tombstone = replace(pending, sources=graph_base.sources + (replace(edge, version=2, deleted=True),),
                        source_deliveries=graph_base.source_deliveries + (
                            SourceDelivery(edge.record_id, 2, "host", None, None, Slot("recovery", 1)),))
    valid = [987654321] * 8
    raw = json.dumps({"candidate": valid, "send": []}, separators=(",", ":"))
    retained = replace(base, slot=Slot("recovery", 1), notice=ContinueNotice(),
                       history=(OwnReply(Slot("prefix", 4), raw),),
                       candidate=CandidateState.valid(world.task, world.size, 0, Slot("prefix", 4), valid))
    return {"ordinary_receipt": ordinary, "disclosed_receipt": disclosed,
            "compact_wrong_result": compact, "compact_absence": absent,
            "pending_edge": pending, "known_tombstone": tombstone,
            "retained_valid_reply": retained}
