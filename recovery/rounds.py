"""Scripted synchronous barriers and branch-owned delivery (spec §§3, 9).

Prepare every request before obtaining replies. Validate all replies before
staging effects; drain sources/prose together before the next opportunity.
The separate pure steps are also the later persistence/replay integration seam.
No inference, evaluator, event policy or persistence framework is imported.
"""

from dataclasses import asdict, dataclass, field, replace
import json

from .prompts import (ProtocolLimits, THESIS_LIMITS, RenderedRequest, TokenizedRequest,
                      render_request, rendered_data, tokenize_request)
from .protocol import GeneratedReply, ReplyValidation, StagedMessage, failed_reply, validate_reply
from .state import (CandidateState, ContinueNotice, DeliveryBoundary, Feedback,
                    HistoricalReceipt, OwnReply, PeerView, PendingSource,
                    ReceivedProse, RevisionNotice, Slot, SourceDelivery, initial_view)
from .tasks import PEERS, PublicSource, Size, SourceRecord, Task, World


@dataclass(frozen=True, slots=True)
class PeerState:
    """Committed permitted data, including the final scheduled slot's outcome."""

    sources: tuple[SourceRecord | PendingSource, ...]
    history: tuple[OwnReply | ReceivedProse | CandidateState, ...] = ()
    candidate: CandidateState = field(default_factory=CandidateState)
    feedback: tuple[Feedback, ...] = ()
    notice: RevisionNotice | ContinueNotice | None = None
    receipt: HistoricalReceipt | None = None
    source_deliveries: tuple[SourceDelivery, ...] = ()

    def __post_init__(self) -> None:
        for name in ("sources", "history", "feedback", "source_deliveries"):
            if type(getattr(self, name)) is not tuple:
                raise ValueError("committed peer collections must be immutable")

    @classmethod
    def from_view(cls, view: PeerView) -> "PeerState":
        return cls(view.sources, view.history, view.candidate, view.feedback,
                   view.notice, view.receipt, view.source_deliveries)

    def view(self, task: Task, size: Size, peer: int, slot: Slot,
             manifest: tuple[PublicSource, ...]) -> PeerView:
        return PeerView(task, size, peer, slot, manifest, self.sources, self.history,
                        self.candidate, self.feedback, self.notice, self.receipt,
                        self.source_deliveries)


@dataclass(frozen=True, slots=True)
class Delivery:
    """One reference attempt or literal text component, kept offline.

    Repeated references have separate IDs under the same message. acquired is
    true only for the first newly known record/version; text has no acquisition.
    An unreleased queue entry has neither first_usable nor acquired.
    """

    delivery_id: str
    message_id: str
    sender: int | None
    recipient: int
    origin: str
    generated: Slot | None
    source: SourceRecord | None = None
    text: str | None = None
    first_usable: Slot | DeliveryBoundary | None = None
    acquired: bool | None = None

    def __post_init__(self) -> None:
        if (type(self.delivery_id) is not str or not self.delivery_id
                or type(self.message_id) is not str or not self.message_id
                or type(self.recipient) is not int or self.recipient not in PEERS
                or (self.source is None) == (self.text is None)
                or (self.source is not None and type(self.source) is not SourceRecord)
                or (self.text is not None and type(self.text) is not str)):
            raise ValueError("delivery must identify one source attempt or text component")
        if self.origin == "host":
            if self.sender is not None or self.generated is not None or self.source is None:
                raise ValueError("host delivery supplies only a source, without a peer slot")
        elif self.origin == "peer":
            if (type(self.sender) is not int or self.sender not in PEERS
                    or self.sender == self.recipient or type(self.generated) is not Slot
                    or self.generated.phase == "control"):
                raise ValueError("peer delivery requires its generating sender/slot")
        else:
            raise ValueError("unknown delivery origin")
        if self.first_usable is not None:
            if (type(self.first_usable) not in (Slot, DeliveryBoundary)
                    or (self.generated is not None
                        and self.first_usable.order <= self.generated.order)):
                raise ValueError("delivery cannot be usable inside its generating round")
            if self.source is not None and type(self.acquired) is not bool:
                raise ValueError("released source attempt requires acquisition outcome")
        elif self.acquired is not None:
            raise ValueError("pending delivery has no acquisition outcome")
        if self.text is not None and self.acquired is not None:
            raise ValueError("text is derived work, not raw-source acquisition")


@dataclass(frozen=True, slots=True)
class BranchState:
    branch_id: str
    phase: str
    task: Task
    size: Size
    manifest: tuple[PublicSource, ...]
    peers: tuple[PeerState, ...]
    last_slot: Slot | None = None
    prefix_parent: str | None = None
    pending: tuple[Delivery, ...] = ()
    deliveries: tuple[Delivery, ...] = ()
    committed: bool = True

    def __post_init__(self) -> None:
        if (type(self.branch_id) is not str or not self.branch_id
                or self.phase not in ("prefix", "recovery")
                or type(self.task) is not Task or type(self.size) is not Size
                or type(self.manifest) is not tuple or type(self.peers) is not tuple
                or len(self.peers) != 4 or any(type(p) is not PeerState for p in self.peers)
                or type(self.pending) is not tuple or type(self.deliveries) is not tuple
                or type(self.committed) is not bool
                or (self.last_slot is not None and type(self.last_slot) is not Slot)):
            raise ValueError("branch requires four immutable peers and host identity")
        if self.phase == "prefix":
            if self.prefix_parent is not None or (self.last_slot is not None
                                                  and self.last_slot.phase != "prefix"):
                raise ValueError("prefix cannot inherit a continuation")
        elif (type(self.prefix_parent) is not str or not self.prefix_parent
              or type(self.last_slot) is not Slot
              or (self.last_slot.phase == "prefix" and self.last_slot.round_number != 4)
              or self.last_slot.phase == "control"):
            raise ValueError("continuation must follow its original complete prefix")
        ids = [d.delivery_id for d in self.pending + self.deliveries]
        if (len(ids) != len(set(ids)) or any(d.first_usable is not None for d in self.pending)
                or any(d.first_usable is None for d in self.deliveries)):
            raise ValueError("delivery IDs and pending/released states must be distinct")

    @property
    def boundary_applied(self) -> bool:
        """Persistent notices identify the cut, including sham, without a new ID.

        M3 can inspect this in the serialized checkpoint before resuming. A raw
        prefix fork has no notices; every event assigns one to all four peers.
        This is an in-memory marker, not a claim of crash-safe persistence.
        """

        return self.phase == "recovery" and all(p.notice is not None for p in self.peers)

    @property
    def next_slot(self) -> Slot | None:
        if self.last_slot is None or self.last_slot.phase != self.phase:
            return Slot(self.phase, 1)
        return (None if self.last_slot.round_number == 4
                else Slot(self.phase, self.last_slot.round_number + 1))


def initial_branch(world: World, branch_id: str) -> BranchState:
    if type(world) is not World or any(s.version != 1 or s.deleted for s in world.records):
        raise ValueError("a shared prefix starts only from original v1 records")
    views = tuple(initial_view(world, peer) for peer in PEERS)
    deliveries = []
    for view in views:
        message_id = f"{branch_id}/host/initial/p{view.peer}"
        for source in view.sources:
            deliveries.append(Delivery(f"{message_id}/{source.record_id}/v{source.version}",
                                       message_id, None, view.peer, "host", None,
                                       source=source, first_usable=view.slot, acquired=True))
    return BranchState(branch_id, "prefix", world.task, world.size, views[0].manifest,
                       tuple(PeerState.from_view(v) for v in views), deliveries=tuple(deliveries))


@dataclass(frozen=True, slots=True)
class RoundRequests:
    before: BranchState
    slot: Slot
    views: tuple[PeerView, ...]
    rendered: tuple[RenderedRequest, ...]
    tokenized: tuple[TokenizedRequest, ...]


@dataclass(frozen=True, slots=True)
class RoundBarrier:
    requests: RoundRequests
    replies: tuple[ReplyValidation, ...]
    messages: tuple[StagedMessage, ...]


@dataclass(frozen=True, slots=True)
class RoundResult:
    barrier: RoundBarrier
    committed: BranchState


def prepare_round(state: BranchState, tokenizer, *, limits: ProtocolLimits = THESIS_LIMITS) -> RoundRequests:
    if not state.committed:
        raise ValueError("commit the preceding delivery barrier before another call")
    slot = state.next_slot
    if slot is None:
        raise ValueError("all four scheduled rounds are complete")
    views = tuple(p.view(state.task, state.size, i, slot, state.manifest)
                  for i, p in enumerate(state.peers))
    rendered = tuple(render_request(view, limits=limits) for view in views)
    tokenized = tuple(tokenize_request(request, tokenizer, limits=limits) for request in rendered)
    return RoundRequests(state, slot, views, rendered, tokenized)


def validate_round(requests: RoundRequests, generated: tuple[GeneratedReply | None, ...],
                   tokenizer, *, limits: ProtocolLimits = THESIS_LIMITS) -> RoundBarrier:
    """None is an explicitly recorded failed slot; empty text is invalid output."""

    if type(generated) is not tuple or len(generated) != 4:
        raise ValueError("record all four scheduled replies/failures before validation")
    replies = tuple(failed_reply(view) if raw is None else validate_reply(view, raw, tokenizer, limits=limits)
                    for view, raw in zip(requests.views, generated))
    # Canonical sender/recipient order, independent of invocation and send-list order.
    messages = tuple(sorted((m for reply in replies for m in reply.messages),
                            key=lambda m: (m.sender, m.recipient)))
    return RoundBarrier(requests, replies, messages)


def stage_effects(barrier: RoundBarrier) -> BranchState:
    """Apply own outcomes and enqueue components without exposing recipient effects.

    The returned state is a pre-delivery checkpoint, not a next-call state.
    Later delivery rules can release source/text component IDs independently.
    """

    state = barrier.requests.before
    peers = tuple(replace(peer, candidate=reply.candidate,
                          # K's boundary result becomes ordinary labeled history
                          # once a new slot replaces latest_candidate. Preserve
                          # even absence, without fabricating a complete reply.
                          history=peer.history + ((peer.candidate,) if peer.candidate.historical else ())
                          + (() if reply.own_reply is None else (reply.own_reply,)),
                          feedback=peer.feedback + (() if reply.feedback is None else (reply.feedback,)))
                  for peer, reply in zip(state.peers, barrier.replies))
    pending = list(state.pending)
    for message in barrier.messages:
        call_id = f"{state.branch_id}/r{message.slot.round_number}/p{message.sender}"
        message_id = f"{call_id}/to{message.recipient}"
        for attempt, source in enumerate(message.sources):
            pending.append(Delivery(f"{message_id}/source{attempt}", message_id,
                                    message.sender, message.recipient, "peer", message.slot,
                                    source=source))
        if message.text is not None:
            pending.append(Delivery(f"{message_id}/text", message_id, message.sender,
                                    message.recipient, "peer", message.slot, text=message.text))
    return replace(state, peers=peers, last_slot=barrier.requests.slot,
                   pending=tuple(pending), committed=False)


def _following(slot: Slot) -> Slot | DeliveryBoundary:
    if slot.round_number < 4:
        return Slot(slot.phase, slot.round_number + 1)
    return Slot("recovery", 1) if slot.phase == "prefix" else DeliveryBoundary()


def drain_deliveries(state: BranchState, delivery_ids: tuple[str, ...] | None = None) -> BranchState:
    """Release queued components at the next boundary, exactly once.

    Selecting component IDs supplies the narrow seam needed by later prose
    delay. Already released IDs are idempotent; unknown IDs are an error.
    Sources arrive before prose; prose appends in generation/sender order.
    """

    if state.last_slot is None:
        if state.pending:
            raise ValueError("peer deliveries require a completed generating round")
        return state
    known = {d.delivery_id for d in state.pending + state.deliveries}
    selected = {d.delivery_id for d in state.pending} if delivery_ids is None else set(delivery_ids)
    if not selected <= known:
        raise ValueError("cannot release an unknown delivery")
    if any(d.source is not None and d.delivery_id not in selected for d in state.pending):
        raise ValueError("every validated source must be delivered at this barrier")
    usable = _following(state.last_slot)
    peers = list(state.peers)
    released = []
    queue = sorted((d for d in state.pending if d.delivery_id in selected),
                   key=lambda d: (d.source is None, d.generated.order, d.sender, d.recipient))
    for delivery in queue:
        peer = peers[delivery.recipient]
        if delivery.source is not None:
            source = delivery.source
            current = {s.record_id: s for s in peer.sources}
            previous = current.get(source.record_id)
            if (previous is not None and (previous.version > source.version
                    or (type(previous) is SourceRecord and previous.version == source.version
                        and previous != source))):
                raise ValueError("delivery conflicts with recipient current source authority")
            acquired = type(previous) is not SourceRecord or previous.version != source.version
            current[source.record_id] = source
            metadata = {d.record_id: d for d in peer.source_deliveries}
            if acquired:
                metadata[source.record_id] = SourceDelivery(source.record_id, source.version,
                    delivery.origin, delivery.sender, delivery.generated, usable)
            peer = replace(peer, sources=tuple(current[k] for k in sorted(current)),
                           source_deliveries=tuple(metadata[k] for k in sorted(metadata)))
            delivery = replace(delivery, first_usable=usable, acquired=acquired)
        else:
            peer = replace(peer, history=peer.history + (
                ReceivedProse(delivery.generated, delivery.sender, delivery.text),))
            delivery = replace(delivery, first_usable=usable)
        peers[delivery.recipient] = peer
        released.append(delivery)
    return replace(state, peers=tuple(peers),
                   pending=tuple(d for d in state.pending if d.delivery_id not in selected),
                   deliveries=state.deliveries + tuple(released), committed=True)


def commit_round(barrier: RoundBarrier) -> RoundResult:
    return RoundResult(barrier, drain_deliveries(stage_effects(barrier)))


def run_round(state: BranchState, tokenizer, reply_provider, *, invocation_order=PEERS,
              limits: ProtocolLimits = THESIS_LIMITS) -> RoundResult:
    """The provider sees only its frozen view and exact rendered/tokenized request.

    It returns recorded output or an explicit failure. Provider exceptions leave
    the whole round uncommitted; retry/persistence belongs to M3.
    """

    order = tuple(invocation_order)
    if len(order) != 4 or any(type(i) is not int for i in order) or set(order) != set(PEERS):
        raise ValueError("invoke every peer exactly once")
    requests = prepare_round(state, tokenizer, limits=limits)
    generated = [None] * 4
    for peer in order:
        generated[peer] = reply_provider(requests.views[peer], requests.rendered[peer],
                                         requests.tokenized[peer])
    return commit_round(validate_round(requests, tuple(generated), tokenizer, limits=limits))


def snapshot_bytes(state: BranchState) -> bytes:
    """One ordinary JSON state record, with no hashes or secondary stores."""

    return json.dumps(asdict(state), ensure_ascii=True, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")


def _read_slot(data) -> Slot | DeliveryBoundary | None:
    if data is None:
        return None
    return DeliveryBoundary(**data) if data["round_number"] == 5 else Slot(**data)


def _read_source(data) -> SourceRecord | PendingSource:
    data = dict(data)
    if "value" not in data:
        return PendingSource(**data)
    if type(data["value"]) is list:
        data["value"] = tuple(data["value"])
    return SourceRecord(**data)


def _read_candidate(data) -> CandidateState:
    candidate = dict(data)
    candidate["slot"] = _read_slot(candidate["slot"])
    if candidate["value"] is not None:
        candidate["value"] = tuple(tuple(v) if type(v) is list else v for v in candidate["value"])
    return CandidateState(**candidate)


def _read_peer(data) -> PeerState:
    data = dict(data)
    data["sources"] = tuple(_read_source(s) for s in data["sources"])
    data["history"] = tuple(_read_candidate(e) if "status" in e else
        (ReceivedProse if "sender" in e else OwnReply)(**dict(e, slot=_read_slot(e["slot"])))
        for e in data["history"])
    data["candidate"] = _read_candidate(data["candidate"])
    data["feedback"] = tuple(Feedback(**dict(e, slot=_read_slot(e["slot"]))) for e in data["feedback"])
    notice = data["notice"]
    data["notice"] = (None if notice is None else ContinueNotice() if not notice else
                      RevisionNotice(**dict(notice, source=PublicSource(**notice["source"]))))
    receipt = data["receipt"]
    if receipt is not None:
        data["receipt"] = HistoricalReceipt(**dict(receipt, source=PublicSource(**receipt["source"])))
    data["source_deliveries"] = tuple(SourceDelivery(**dict(
        e, generated=_read_slot(e["generated"]), first_usable=_read_slot(e["first_usable"])))
        for e in data["source_deliveries"])
    return PeerState(**data)


def _read_delivery(data) -> Delivery:
    return Delivery(**dict(data, source=None if data["source"] is None else _read_source(data["source"]),
                           generated=_read_slot(data["generated"]),
                           first_usable=_read_slot(data["first_usable"])))


def deserialize_state(payload: bytes) -> BranchState:
    """Rebuild every nested record; no parent/thread/backend state is reused."""

    data = json.loads(payload)
    data.update(task=Task(data["task"]), size=Size(data["size"]),
                manifest=tuple(PublicSource(**s) for s in data["manifest"]),
                peers=tuple(_read_peer(p) for p in data["peers"]),
                last_slot=_read_slot(data["last_slot"]),
                pending=tuple(_read_delivery(d) for d in data["pending"]),
                deliveries=tuple(_read_delivery(d) for d in data["deliveries"]))
    state = BranchState(**data)
    # Validate full public source/history contracts where a future view exists.
    # Terminal recovery state has no fifth model view; it still round-trips all
    # final outcomes/deliveries for the later offline audit.
    slot = state.next_slot
    if slot is None and state.phase == "prefix":
        slot = Slot("recovery", 1)
    if slot is not None:
        for peer, p in enumerate(state.peers):
            p.view(state.task, state.size, peer, slot, state.manifest)
    return state


def prefix_snapshot(state: BranchState) -> bytes:
    if (state.phase != "prefix" or state.last_slot != Slot("prefix", 4)
            or state.pending or not state.committed):
        raise ValueError("freeze only a committed, completely drained four-round prefix")
    return snapshot_bytes(state)


def fork_prefix(payload: bytes, branch_id: str) -> BranchState:
    state = deserialize_state(payload)
    prefix_snapshot(state)  # Reject partial/queued/continuation snapshots.
    if branch_id == state.branch_id:
        raise ValueError("a continuation requires a new branch identity")
    return replace(state, branch_id=branch_id, phase="recovery", prefix_parent=state.branch_id)


@dataclass(frozen=True, slots=True)
class ScriptedPrefix:
    rounds: tuple[RoundResult, ...]
    snapshot: bytes

    def owner_v1_exposure(self, source: PublicSource) -> tuple[Slot, ...]:
        """Factual check of actual rendered owner requests, never outcome selection."""

        exposed = []
        for result in self.rounds:
            requests = result.barrier.requests
            rendered = requests.rendered[source.owner]
            data = rendered_data(rendered)
            if any(s["record_id"] == source.record_id and s["owner"] == source.owner
                   and s["version"] == 1 and s["status"] == "known"
                   for s in data["current_sources"]):
                exposed.append(requests.slot)
        return tuple(exposed)


def run_prefix(world: World, branch_id: str, tokenizer, reply_provider, *, invocation_order=PEERS) -> ScriptedPrefix:
    state = initial_branch(world, branch_id)
    order = tuple(invocation_order)
    rounds = []
    for _ in range(4):
        result = run_round(state, tokenizer, reply_provider, invocation_order=order)
        rounds.append(result)
        state = result.committed
    return ScriptedPrefix(tuple(rounds), prefix_snapshot(state))
