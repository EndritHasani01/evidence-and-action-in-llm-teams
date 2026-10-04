"""Exact scheduled continuation replies and Q delivery (spec §§4.2, 4.4, 9).

SavedRound is the in-memory pre-delivery record, not a cache or a durable ledger.
Its branch comes from the validated schedule. Obtain/save it before committing
effects; M3 will persist the same evidence before advancing a checkpoint.
"""

from copy import deepcopy
from dataclasses import dataclass
import json

from .rounds import (BranchState, RoundBarrier, RoundResult, drain_deliveries,
                     prepare_round, stage_effects, validate_round)
from .schedule import Branch, CallSlot, _call_id
from .state import Slot
from .tasks import PEERS


def _calls(branch: Branch, state: BranchState) -> tuple[CallSlot, ...]:
    if (type(branch) is not Branch or branch.phase != "continuation"
            or branch.branch_id != state.branch_id or branch.task is not state.task
            or branch.prefix_parent != state.prefix_parent or not state.boundary_applied
            or not state.committed or state.next_slot is None):
        raise ValueError("continuation requires its scheduled branch and committed event boundary")
    calls = tuple(c for c in branch.calls if c.round_number == state.next_slot.round_number)
    replay = state.next_slot.round_number == 1 and branch.policy in ("P_G", "P_H", "Q_B", "Q_C")
    if (len(calls) != 4 or tuple(c.peer for c in calls) != PEERS
            or any(c.call_id != _call_id(branch.branch_id, c.round_number, c.peer)
                   or type(c.seed) is not int or c.seed < 0
                   or (c.replay_parent is not None) != replay for c in calls)):
        raise ValueError("scheduled continuation slots or required replay parents differ")
    return calls


@dataclass(frozen=True, slots=True)
class SavedRound:
    branch: Branch
    settings_json: str
    barrier: RoundBarrier

    @property
    def calls(self) -> tuple[CallSlot, ...]:
        return _calls(self.branch, self.barrier.requests.before)


def obtain_continuation_round(state: BranchState, branch: Branch, tokenizer,
                              reply_provider=None, *, settings: dict,
                              parents: tuple[SavedRound, ...] = (),
                              invocation_order=PEERS) -> SavedRound:
    """Obtain four literal outputs without effects, or consume prescribed parents.

    For new calls the provider receives only (view, rendered, tokenized), plus
    keyword seed and a fresh settings dictionary. It returns GeneratedReply or
    an explicitly recorded failure (None). Required replays never call it, even
    when the parent is absent/invalid/failed. A missing record is not a failure.
    Settings are captured as ordinary immutable JSON, without an M5 freeze.
    """

    calls = _calls(branch, state)
    if type(settings) is not dict:
        raise ValueError("record the complete generation settings as a JSON object")
    settings_json = json.dumps(settings, sort_keys=True, ensure_ascii=True,
                               allow_nan=False, separators=(",", ":"))
    order = tuple(invocation_order)
    if len(order) != 4 or any(type(p) is not int for p in order) or set(order) != set(PEERS):
        raise ValueError("invoke every peer exactly once")
    requests = prepare_round(state, tokenizer)
    available = {}
    for parent in parents:
        if type(parent) is not SavedRound:
            raise ValueError("reuse requires saved pre-delivery rounds")
        for p, call in enumerate(parent.calls):
            if call.call_id in available:
                raise ValueError("duplicate saved parent call")
            available[call.call_id] = (parent, p, call)

    selected = {}
    # Check every dependency before any generation, validation or branch effect.
    for p, call in enumerate(calls):
        if call.replay_parent is None:
            continue
        if call.replay_parent not in available:
            raise ValueError(f"missing prescribed replay parent: {call.replay_parent}")
        parent, parent_peer, parent_call = available[call.replay_parent]
        identity = parent.branch
        expected_policies = (branch.policy[2:],) if branch.policy in ("Q_B", "Q_C") else ("B", "C")
        if (identity.policy not in expected_policies or identity.world_id != branch.world_id
                or identity.task is not branch.task or identity.event != branch.event
                or identity.replicate != branch.replicate or identity.prefix_parent != branch.prefix_parent
                or parent.barrier.requests.slot != Slot("recovery", 1)
                or parent_call.replay_parent is not None or parent_peer != p):
            raise ValueError("replay parent differs in world/event/replicate/policy/peer/round")
        prior = parent.barrier.requests
        if (parent_call.seed != call.seed or parent.settings_json != settings_json
                or prior.views[p] != requests.views[p]
                or prior.rendered[p] != requests.rendered[p]
                or prior.tokenized[p] != requests.tokenized[p]):
            raise ValueError("replay request/settings/seed/permitted-state equality failed")
        selected[p] = parent.barrier.replies[p]

    generated = [None] * 4
    for p in order:
        if p in selected:
            generated[p] = deepcopy(selected[p].generated)
        else:
            if reply_provider is None:
                raise ValueError("a new scheduled generation needs a reply provider")
            generated[p] = reply_provider(requests.views[p], requests.rendered[p], requests.tokenized[p],
                                           seed=calls[p].seed, settings=json.loads(settings_json))
    barrier = validate_round(requests, tuple(generated), tokenizer)
    for p, recorded in selected.items():
        # Revalidation binds sources to this branch, and must preserve even the
        # parent's invalid/failed outcome, raw tokens, feedback and termination.
        if barrier.replies[p] != recorded:
            raise ValueError("replayed validation differs from the recorded parent outcome")
    return SavedRound(branch, settings_json, barrier)


def commit_continuation_round(saved: SavedRound) -> RoundResult:
    """Reconstruct this branch's deliveries solely from its pre-delivery record.

    Q round one releases all source attempts and retains own replies normally.
    The next ordinary drain appends held round-one prose before round-two prose
    at the round-three boundary. Existing history never moves. No queue data is
    part of PeerView, and no placeholder or source metadata is added for prose.
    """

    saved.calls  # Check the scheduled start, including mandatory first-round replay.
    staged = stage_effects(saved.barrier)
    selected = None
    if saved.branch.policy in ("Q_B", "Q_C") and saved.barrier.requests.slot.round_number == 1:
        selected = tuple(d.delivery_id for d in staged.pending if d.source is not None)
    return RoundResult(saved.barrier, drain_deliveries(staged, selected))


def held_prose_counts(state: BranchState) -> tuple[int, ...]:
    """Host-only nonempty held texts per recipient, including zero/inactive Q.

    Derive from existing pending/released IDs so counts survive release and JSON
    round trips without another counter. Explicit empty text still traverses the
    literal queue, but contributes no prose exposure. Ordinary branches yield 0.
    """

    if not state.committed:
        raise ValueError("count held prose only after the branch delivery rule commits")
    held = [d for d in state.pending + state.deliveries
            if d.generated == Slot("recovery", 1) and d.text
            and (d.first_usable is None or d.first_usable.order > Slot("recovery", 2).order)]
    return tuple(sum(d.recipient == p for d in held) for p in PEERS)
