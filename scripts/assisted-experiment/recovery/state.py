"""Explicit permitted peer data (spec §§3.1, 4.3–4.4).

Worlds enter only the initial-view projection. Rendering and source lookup take
PeerView, which has no evaluator, branch, event, reset mask or delayed queue.
Round delivery lives in rounds.py; event/retention transformations in events.py.
"""

from dataclasses import dataclass, field, replace
from types import MappingProxyType

from .tasks import (PEERS, PublicSource, Size, SourceRecord, Task, World,
                    candidate_contract, numeric_range, source_manifest)


@dataclass(frozen=True, slots=True)
class Slot:
    phase: str
    round_number: int

    def __post_init__(self) -> None:
        if (type(self.phase) is not str or self.phase not in ("prefix", "recovery", "control")
                or type(self.round_number) is not int
                or not 1 <= self.round_number <= (1 if self.phase == "control" else 4)):
            raise ValueError("invalid public phase/round")

    @property
    def order(self) -> int:
        return self.round_number + (4 if self.phase == "recovery" else 0)


@dataclass(frozen=True, slots=True)
class DeliveryBoundary:
    """Availability after the last recovery call, without a fifth opportunity.

    Ordinary availability uses Slot. Final messages are still drained/audited,
    but their next-round boundary is never rendered or scheduled as a call.
    """

    phase: str = "recovery"
    round_number: int = 5

    def __post_init__(self) -> None:
        if (self.phase != "recovery" or type(self.phase) is not str
                or type(self.round_number) is not int or self.round_number != 5):
            raise ValueError("terminal delivery boundary is recovery round five")

    @property
    def order(self) -> int:
        return 9


@dataclass(frozen=True, slots=True)
class PendingSource:
    """Known current identity/version, with no usable payload or old value."""

    record_id: str
    owner: int
    position: int | None
    version: int


@dataclass(frozen=True, slots=True)
class OwnReply:
    slot: Slot
    text: str


@dataclass(frozen=True, slots=True)
class ReceivedProse:
    """Append at release time, retaining the sender's generation label."""

    slot: Slot
    sender: int
    text: str


# Fixed public descriptions prevent library errors/hidden payloads becoming
# feedback. Tokenizer admission of their 32-token cap is checked at encoding.
PUBLIC_FEEDBACK = MappingProxyType({
    "json": "Reply must be one complete strict JSON object.",
    "reply_schema": "Use exactly the declared candidate and send fields.",
    "candidate_shape": "Candidate must match the assigned integer shape.",
    "message_schema": "Use only the declared message and source-reference fields.",
    "recipient": "Send at most one message to each other peer.",
    "control_send": "Full-information controls require an empty send list.",
    "source_reference": "Source references must name currently held IDs and versions.",
    "reference_limit": "Use at most eight distinct source references per recipient.",
    "prose_limit": "Combined message texts must fit the 128-token prose limit.",
    "output_limit": "Reply exceeds the 384-token output limit.",
})


@dataclass(frozen=True, slots=True)
class Feedback:
    slot: Slot
    code: str

    def __post_init__(self) -> None:
        if type(self.code) is not str or self.code not in PUBLIC_FEEDBACK:
            raise ValueError("feedback must describe a declared public violation")

    @property
    def text(self) -> str:
        return PUBLIC_FEEDBACK[self.code]


@dataclass(frozen=True, slots=True)
class CandidateState:
    """Latest slot outcome, never an automatically inherited earlier answer.

Valid values are immutable integer tuples or canonical BFS key/value tuples.
`historical` describes K's actual retained result/absence, not correctness.
"""

    status: str = "unexecuted"
    slot: Slot | None = None
    value: tuple | None = None
    historical: bool = False

    def __post_init__(self) -> None:
        if (type(self.status) is not str or self.status not in ("unexecuted", "valid", "invalid", "failed")
                or type(self.historical) is not bool):
            raise ValueError("invalid candidate status")
        if self.status == "unexecuted":
            if self.slot is not None or self.value is not None or self.historical:
                raise ValueError("unexecuted candidate must be absent")
        elif type(self.slot) is not Slot:
            raise ValueError("completed candidate requires its slot")
        if self.status == "valid":
            if type(self.value) is not tuple:
                raise ValueError("candidate must be immutable")
        elif self.value is not None:
            raise ValueError("invalid/failed slots have no candidate")
        if self.historical and self.slot != Slot("prefix", 4):
            raise ValueError("historical result must be the prefix-round-four outcome")

    @classmethod
    def valid(cls, task: Task, size: Size, peer: int | None, slot: Slot,
              value: object, *, historical: bool = False) -> "CandidateState":
        contract = candidate_contract(task, size, peer)
        if contract.error(value) is not None:
            raise ValueError("candidate does not match public shape")
        frozen = (tuple((str(j), value[str(j)]) for j in contract.coordinates)
                  if task is Task.BFS else tuple(value))
        return cls("valid", slot, frozen, historical)

    def payload(self, task: Task) -> list[int] | dict[str, int] | None:
        if self.value is None:
            return None
        # No coercion: even wrong integers remain the actual submitted values.
        return dict(self.value) if task is Task.BFS else list(self.value)


@dataclass(frozen=True, slots=True)
class RevisionNotice:
    source: PublicSource
    previous_version: int
    new_version: int

    def __post_init__(self) -> None:
        if (type(self.source) is not PublicSource
                or type(self.source.record_id) is not str or type(self.source.owner) is not int
                or (self.source.position is not None and type(self.source.position) is not int)
                or type(self.previous_version) is not int
                or type(self.new_version) is not int
                or self.previous_version < 1
                or self.new_version != self.previous_version + 1):
            raise ValueError("invalid public revision notice")


@dataclass(frozen=True, slots=True)
class ContinueNotice:
    """The same neutral continue-solving notice for every sham peer."""


@dataclass(frozen=True, slots=True)
class HistoricalReceipt:
    source: PublicSource
    previous_version: int
    new_version: int
    before_value: int | None = None


@dataclass(frozen=True, slots=True)
class SourceDelivery:
    """First usable acquisition of a current record; full attempts stay offline.

No message/branch IDs, payloads, prose flags or queue/release internals enter
this layout. Source-bearing Q/parent siblings can share it exactly.
"""

    record_id: str
    version: int
    origin: str
    sender: int | None
    generated: Slot | None
    first_usable: Slot | DeliveryBoundary


@dataclass(frozen=True, slots=True)
class PeerView:
    task: Task
    size: Size
    peer: int | None
    slot: Slot
    manifest: tuple[PublicSource, ...]
    sources: tuple[SourceRecord | PendingSource, ...]
    history: tuple[OwnReply | ReceivedProse | CandidateState, ...] = ()
    candidate: CandidateState = field(default_factory=CandidateState)
    feedback: tuple[Feedback, ...] = ()
    notice: RevisionNotice | ContinueNotice | None = None
    receipt: HistoricalReceipt | None = None
    source_deliveries: tuple[SourceDelivery, ...] = ()

    def __post_init__(self) -> None:
        contract = candidate_contract(self.task, self.size, self.peer)
        if type(self.slot) is not Slot or (self.peer is None) != (self.slot.phase == "control"):
            raise ValueError("peer/control phase mismatch")
        for name in ("manifest", "sources", "history", "feedback", "source_deliveries"):
            if type(getattr(self, name)) is not tuple:
                raise ValueError("peer data collections must be immutable tuples")
        bfs = self.task is Task.BFS
        count = self.size.edge_count if bfs else self.size.numeric_length
        expected_ids = {f"{'e' if bfs else 'x'}{i:03d}" for i in range(count)}
        public = {}
        owners = [0] * 4
        for source in self.manifest:
            if (type(source) is not PublicSource or type(source.record_id) is not str
                    or source.record_id in public or source.record_id not in expected_ids
                    or type(source.owner) is not int or source.owner not in PEERS):
                raise ValueError("invalid public source identity/owner")
            position = None if bfs else int(source.record_id[1:])
            if (source.position != position or (not bfs and type(source.position) is not int)
                    or (self.task in (Task.PREFIX, Task.DIFFERENCE)
                        and source.owner != position // self.size.shard_size)):
                raise ValueError("invalid public position/owner")
            public[source.record_id] = source
            owners[source.owner] += 1
        if set(public) != expected_ids or owners != [count // 4] * 4:
            raise ValueError("incomplete public manifest")
        current = {}
        for source in self.sources:
            if type(source) not in (SourceRecord, PendingSource):
                raise ValueError("invalid current source")
            identity = PublicSource(source.record_id, source.owner, source.position)
            if (type(source.record_id) is not str or source.record_id in current
                    or public.get(source.record_id) != identity
                    or type(source.owner) is not int
                    or (not bfs and type(source.position) is not int)
                    or type(source.version) is not int or source.version < 1):
                raise ValueError("current source disagrees with public identity")
            if type(source) is SourceRecord:
                if type(source.deleted) is not bool:
                    raise ValueError("invalid source deletion status")
                if bfs:
                    edge = source.value
                    if (type(edge) is not tuple or len(edge) != 2
                            or any(type(v) is not int for v in edge)
                            or not 0 <= edge[0] < edge[1] < self.size.node_count
                            or (source.deleted and source.version == 1)):
                        raise ValueError("invalid held edge/tombstone")
                else:
                    low, high = numeric_range(self.task)
                    if (source.deleted or type(source.value) is not int
                            or not low <= source.value <= high):
                        raise ValueError("invalid held numeric source")
            current[source.record_id] = source
        if type(self.notice) is RevisionNotice:
            notice = self.notice
            changed = current.get(notice.source.record_id)
            if (public.get(notice.source.record_id) != notice.source or changed is None
                    or changed.version != notice.new_version):
                raise ValueError("revision requires known or pending current replacement")
        elif self.notice is not None and type(self.notice) is not ContinueNotice:
            raise ValueError("notice must use the public layout")
        if self.receipt is not None:
            receipt = self.receipt
            if (type(receipt) is not HistoricalReceipt or type(self.notice) is not RevisionNotice
                    or self.task not in (Task.PREFIX, Task.SORT)
                    or type(receipt.source) is not PublicSource
                    or type(receipt.source.owner) is not int
                    or type(receipt.source.position) is not int
                    or receipt.source != self.notice.source
                    or type(receipt.previous_version) is not int
                    or type(receipt.new_version) is not int
                    or (receipt.previous_version, receipt.new_version)
                        != (self.notice.previous_version, self.notice.new_version)
                    or (receipt.before_value is not None
                        and type(current[receipt.source.record_id]) is not SourceRecord)):
                raise ValueError("receipt requires the matching numeric revision; disclosure requires delivery")
            low, high = numeric_range(self.task)
            if receipt.before_value is not None and (type(receipt.before_value) is not int
                                                     or not low <= receipt.before_value <= high):
                raise ValueError("invalid historical receipt value")
        own_slots = set()
        prose_slots = set()
        historical_slots = set()
        for entry in self.history:
            if type(entry) is CandidateState:
                if not entry.historical or entry.slot in historical_slots:
                    raise ValueError("history keeps only one literal historical fourth-slot outcome")
                self._past_slot(entry.slot)
                self._candidate_shape(entry, contract)
                historical_slots.add(entry.slot)
                continue
            if type(entry) not in (OwnReply, ReceivedProse) or type(entry.text) is not str:
                raise ValueError("history contains only literal replies/prose or the retained result")
            self._past_slot(entry.slot)
            if type(entry) is OwnReply:
                if entry.slot in own_slots:
                    raise ValueError("duplicate own reply slot")
                own_slots.add(entry.slot)
            else:
                if (type(entry.sender) is not int or entry.sender not in PEERS
                        or entry.sender == self.peer or (entry.slot, entry.sender) in prose_slots):
                    raise ValueError("invalid/duplicate received prose")
                prose_slots.add((entry.slot, entry.sender))
        if historical_slots & own_slots:
            raise ValueError("historical result must not duplicate its complete own reply")
        feedback_slots = set()
        for entry in self.feedback:
            if type(entry) is not Feedback or entry.slot in feedback_slots:
                raise ValueError("invalid/duplicate public feedback")
            self._past_slot(entry.slot)
            feedback_slots.add(entry.slot)
        if type(self.candidate) is not CandidateState:
            raise ValueError("invalid candidate state")
        if self.candidate.slot is not None:
            self._past_slot(self.candidate.slot)
        latest_recorded = max(own_slots | feedback_slots, key=lambda s: s.order, default=None)
        if latest_recorded is not None and (self.candidate.slot is None
                                            or self.candidate.slot.order < latest_recorded.order):
            raise ValueError("candidate must describe the latest recorded own slot")
        if historical_slots and (self.candidate.slot is None or self.candidate.slot.order <= 4):
            raise ValueError("archived compact result requires a separate new-slot outcome")
        self._candidate_shape(self.candidate, contract)
        delivered = set()
        for delivery in self.source_deliveries:
            if (type(delivery) is not SourceDelivery or type(delivery.record_id) is not str
                    or delivery.record_id in delivered or type(delivery.version) is not int):
                raise ValueError("invalid/duplicate current source delivery")
            source = current.get(delivery.record_id)
            if type(source) is not SourceRecord or source.version != delivery.version:
                raise ValueError("delivery metadata requires a held current source")
            if (type(delivery.first_usable) is not Slot or delivery.first_usable.order > self.slot.order
                    or (delivery.first_usable.phase == "control") != (self.slot.phase == "control")):
                raise ValueError("source delivery is not yet usable")
            if delivery.origin == "host":
                if delivery.sender is not None or delivery.generated is not None:
                    raise ValueError("host delivery cannot include peer/queue metadata")
            elif delivery.origin == "peer":
                if (type(delivery.sender) is not int or delivery.sender not in PEERS
                        or delivery.sender == self.peer or type(delivery.generated) is not Slot
                        or delivery.generated.phase == "control" or self.peer is None
                        or delivery.generated.order >= delivery.first_usable.order):
                    raise ValueError("invalid peer source-delivery label")
            else:
                raise ValueError("unknown source-delivery origin")
            delivered.add(delivery.record_id)
        # Only public identity controls these orders. History stays in actual
        # append/release order, including Q's later release of an earlier slot.
        for name in ("manifest", "sources", "source_deliveries"):
            object.__setattr__(self, name, tuple(sorted(getattr(self, name), key=lambda r: r.record_id)))

    def _past_slot(self, slot: Slot) -> None:
        if (type(slot) is not Slot or slot.phase == "control"
                or slot.order >= self.slot.order or self.slot.phase == "control"):
            raise ValueError("derived history/candidate must precede this call")

    def _candidate_shape(self, candidate: CandidateState, contract) -> None:
        if candidate.status == "valid":
            value = candidate.value
            if self.task is Task.BFS and (
                    any(type(pair) is not tuple or len(pair) != 2 for pair in value)
                    or tuple(pair[0] for pair in value) != tuple(str(j) for j in contract.coordinates)):
                raise ValueError("immutable BFS candidate must use canonical node keys")
            if contract.error(candidate.payload(self.task)) is not None:
                raise ValueError("candidate disagrees with public output shape")


def initial_view(world: World, peer: int | None) -> PeerView:
    """Host projection: private v1 shard, or all inputs for an empty-send control.

No prepared-world/event/evaluator record is accepted. The control may receive
an already revised World, but gets no edit labels or before-values.
"""

    if type(world) is not World:
        raise ValueError("initial projection requires a mathematical World")
    candidate_contract(world.task, world.size, peer)
    slot = Slot("control" if peer is None else "prefix", 1)
    sources = tuple(r for r in world.records if peer is None or r.owner == peer)
    deliveries = tuple(SourceDelivery(r.record_id, r.version, "host", None, None, slot)
                       for r in sources)
    return PeerView(world.task, world.size, peer, slot, source_manifest(world), sources,
                    source_deliveries=deliveries)


def held_source(view: PeerView, record_id: str, version: int) -> SourceRecord | None:
    """Resolve only a held current payload, including a known tombstone.

Pending updates, stale/unheld references and historical receipts reveal nothing.
The later protocol validates permission before staging any delivery.
"""

    if type(view) is not PeerView:
        raise ValueError("source lookup requires a permitted PeerView")
    if type(record_id) is not str or type(version) is not int:
        return None
    return next((source for source in view.sources
                 if type(source) is SourceRecord and source.record_id == record_id
                 and source.version == version), None)


def revise_source(view: PeerView, notice: RevisionNotice,
                  replacement: SourceRecord | None) -> PeerView:
    """Invalidate one current version, then deliver content or retain a pending ID.

    This source-authority primitive never edits derived work. CPU v3 checks use
    it directly; the live event entry point permits only a single v1 -> v2 cut.
    The caller supplies the upcoming slot; no old receipt carries into a new
    notice. Host delivery attempts are recorded by the branch transformation.
    """

    if type(view) is not PeerView or type(notice) is not RevisionNotice:
        raise ValueError("revision requires a permitted view and public notice")
    if view.peer is None or view.slot.phase != "recovery" or notice.source not in view.manifest:
        raise ValueError("revision requires a recovery peer and matching public identity")
    key = notice.source.record_id
    current = {s.record_id: s for s in view.sources}
    previous = current.get(key)
    if previous is not None and previous.version != notice.previous_version:
        raise ValueError("revision does not follow current source authority")
    if replacement is not None:
        if (type(replacement) is not SourceRecord
                or PublicSource(replacement.record_id, replacement.owner, replacement.position) != notice.source
                or replacement.version != notice.new_version):
            raise ValueError("replacement must match the announced identity/version")
        current[key] = replacement
    else:
        current[key] = PendingSource(key, notice.source.owner, notice.source.position, notice.new_version)
    deliveries = tuple(d for d in view.source_deliveries if d.record_id != key)
    if replacement is not None:
        deliveries += (SourceDelivery(key, notice.new_version, "host", None, None, view.slot),)
    return replace(view, sources=tuple(current.values()), notice=notice, receipt=None,
                   source_deliveries=deliveries)
