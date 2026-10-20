"""Literal single-event continuation starts (spec §§2.3, 4.1–4.3).

Each call deserializes the original drained prefix. The saved schedule owns
event/subset/replicate eligibility; no model outcome selects or repairs a start.
No evaluator, inference, checkpoint backend or generalized policy language.
"""

from dataclasses import replace

from .populations import PreparedWorld
from .rounds import BranchState, Delivery, PeerState, fork_prefix
from .schedule import Branch, _prepare_branches
from .state import (CandidateState, ContinueNotice, HistoricalReceipt,
                    RevisionNotice, Slot, revise_source)
from .tasks import PEERS, SourceRecord, Task, source_manifest


def start_continuation(prefix: bytes, world: PreparedWorld, branch: Branch) -> BranchState:
    """Return one complete boundary, using existing saved branch/parent IDs.

    `world` and `branch` come from the validated population/schedule. Checking
    the small existing schedule enumeration avoids a second definition of
    subset, replicate and complementary-mask eligibility. Q starts exactly as
    its B/C parent; replay.py owns its subsequent reply reuse and delivery rule.
    """

    if (type(world) is not PreparedWorld or type(branch) is not Branch
            or branch.phase != "continuation" or branch not in _prepare_branches((world,))):
        raise ValueError("boundary requires a scheduled continuation of this saved world")
    state = fork_prefix(prefix, branch.branch_id)
    original = world.world
    if (state.prefix_parent != branch.prefix_parent or state.task is not original.task
            or state.size is not original.size or state.manifest != source_manifest(original)):
        raise ValueError("prefix does not match the scheduled original world/parent")
    sources = {s.record_id: s for s in original.records}
    if any(s.version != 1 or s.deleted for s in original.records):
        raise ValueError("live events require the original v1 world")
    for p, peer in enumerate(state.peers):
        if (peer.notice is not None or peer.receipt is not None
                or peer.candidate.slot != Slot("prefix", 4) or peer.candidate.historical
                or any(type(s) is not SourceRecord or sources.get(s.record_id) != s for s in peer.sources)
                or not all(s in peer.sources for s in original.records if s.owner == p)):
            raise ValueError("prefix must retain its original private/current sources and actual fourth slot")

    # Read genuine archived before-values from this deserialized prefix, after
    # checking its records against the saved original. Never infer from prose.
    revised = world.event_world(branch.event)
    updated = next((s for s in revised.records if s.version == 2), None)
    before = (None if updated is None else next(s for s in state.peers[updated.owner].sources
                                               if s.record_id == updated.record_id))
    identity = (None if updated is None else next(s for s in state.manifest
                                                 if s.record_id == updated.record_id))
    notice = ContinueNotice() if updated is None else RevisionNotice(identity, 1, 2)
    policy = branch.policy
    base = {"B_delta": "B", "C_delta": "C", "K_delta": "K", "Q_B": "B", "Q_C": "C"}.get(policy, policy)
    reset_group = (world.partition[0] if base == "P_G" else
                   world.partition[1] if base == "P_H" else ())
    peers, deliveries = [], list(state.deliveries)
    for p in PEERS:
        view = state.peers[p].view(state.task, state.size, p, Slot("recovery", 1), state.manifest)
        if updated is None:
            view = replace(view, notice=notice)
        else:
            content = updated if base != "L" or p == updated.owner else None
            # Copy the host record too: no shared nested identity across siblings.
            content = None if content is None else replace(content)
            view = revise_source(view, notice, content)
            if content is not None:
                message_id = f"{state.branch_id}/host/revision/p{p}"
                deliveries.append(Delivery(f"{message_id}/{content.record_id}/v2", message_id,
                    None, p, "host", None, source=content, first_usable=view.slot, acquired=True))
            if state.task in (Task.PREFIX, Task.SORT):
                # Keep the ordinary layout in L/F/masks as well: delivery and
                # retention contrasts must not accidentally change the receipt.
                view = replace(view, receipt=HistoricalReceipt(identity, 1, 2,
                    before.value if policy in ("B_delta", "C_delta", "K_delta") else None))
        if base in ("C", "F") or p in reset_group:
            view = replace(view, history=(), candidate=CandidateState(), feedback=())
        elif base == "K":
            view = replace(view, history=(), feedback=(),
                           candidate=replace(view.candidate, historical=True))
        if base == "F":
            kept = tuple(s for s in view.sources if s.owner == p or s.record_id == updated.record_id)
            kept_ids = {s.record_id for s in kept}
            view = replace(view, sources=kept,
                           source_deliveries=tuple(d for d in view.source_deliveries if d.record_id in kept_ids))
        peers.append(PeerState.from_view(view))
    return replace(state, peers=tuple(peers), deliveries=tuple(deliveries))
