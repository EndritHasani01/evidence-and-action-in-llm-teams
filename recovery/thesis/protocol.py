"""Permitted views, exact prompts, phase starts, scoring and the failure funnel.

Specification sections 3.4-3.7 and 3.9. Action legality, alternation, delivery,
finality and termination are the unchanged I-01 functions in recovery.i01.core.
"""

from copy import deepcopy
import re

from ..i01.core import CONTROL_SYSTEM, apply_outcome, finish, next_agent  # noqa: F401 (re-exported)
from . import CELLS, REGIME, REVISION_CELLS, RETAIN_CELLS

THESIS_SYSTEM = '''You are one of two agents finding the global maximum across your current
private integer shards. Both agents must separately submit that same GLOBAL
maximum. Submitting only your own local maximum is insufficient when the
other shard contains a larger value.

Your CURRENT AUTHORITATIVE PRIVATE SHARD is your source for current local
values. The other agent's shard is private. You can exchange ordinary text
messages. A message is a claim, not a certified source or a private submission.
The partner-finished flag reveals only whether that agent has finished.

A useful strategy is to establish the relevant maximum of each shard, compare
them, and send your partner any information needed before you finish. Choose
your messages and timing. Reuse earlier reports when justified; obtain new
information when needed. You do not have to repeat an exchange merely because
a new phase starts. Check what a source change invalidates and what remains
useful. An earlier final answer is not automatically a current answer.

Every record is named by its owner and position, for example "agent 0 record 13".
An ENVIRONMENT NOTICE is not a partner message, a partner maximum or a partner
submission. A record name identifies a location, not an answer. A notice either
reports that no record changed, or names the single record that changed; the
replacement value is supplied only to that record's owner. Earlier-phase
history records what was visible then; current values come from your current
shard.

Return exactly one JSON object with exactly these keys:
message: a string containing non-whitespace text or null
submit: an integer or null
wait: true or false

Legal choices are message only, submit only, message and submit together, or
wait alone. Waiting requires BOTH message and submit to be null. With wait
false, at least one of message or submit must be non-null.
Message-only example: {"message":"example message","submit":null,"wait":false}
Wait-only example: {"message":null,"submit":null,"wait":true}
These are action-form examples, not messages to copy for the task.

Your submission is private unless you explicitly message it. Submission is
FINAL for this phase: you cannot adjust it after another message arrives.
Sending and submitting together delivers your message and then finishes you.
A new phase reopens both agents: submissions from an earlier phase do not
count, and both agents must submit again in the new phase.

Each agent has at most three calls per phase. Unused calls cannot be transferred.
Waiting wakes only on a delivered message. If both agents wait, neither can
send a waking message. Invalid replies use a call and deliver nothing.
There is no correctness feedback. Put no text outside the JSON object.'''

NOTICE_INITIAL = "No environment notice in the initial phase."
NOTICE_NONE = "Environment event: no source record changed. A new phase began."
NOTICE_CHANGE = "Environment event: one source record changed before this phase began."


def cell_shards(world, cell):
    return world["revised"] if cell in REVISION_CELLS else world["original"]


def cell_truth(world, cell):
    return world["revised_truth"] if cell in REVISION_CELLS else world["original_truth"]


def start(world, model, cell, prefix=None):
    """Initial state of the prefix or of one isolated continuation (section 3.6)."""
    if cell == "prefix":
        if prefix is not None:
            raise ValueError("the prefix has no parent")
        history = [[], []]
    else:
        if cell not in CELLS:
            raise ValueError("unknown cell")
        if prefix is None or not prefix.get("terminal") or prefix.get("cell") != "prefix":
            raise ValueError("a terminal shared prefix is required before any continuation")
        if prefix.get("world") != world["id"] or prefix.get("model") != model:
            raise ValueError("prefix belongs to another world or model")
        history = deepcopy(prefix["history"]) if cell in RETAIN_CELLS else [[], []]
    return dict(regime=REGIME, world=world["id"], model=model, cell=cell, history=history,
                earlier=[len(h) for h in history], turns=[0, 0], submissions=[None, None],
                waiting=[False, False], next=world["first"], events=[], terminal=None, unused=None)


def apply(state, agent, action, error, call_id, feedback=None):
    """Unchanged I-01 transition; an invalid call gets its public-rule feedback text."""
    if state.get("regime") != REGIME:
        raise ValueError("thesis state required")
    new = apply_outcome(state, agent, action, error, call_id)
    if action is None:
        entry = new["history"][agent][-1]
        if entry.get("kind") != "feedback" or not feedback:
            raise ValueError("an invalid call requires its public feedback text")
        entry["text"] = feedback
    return new


def view(world, state, agent):
    """Everything this agent may see now, and nothing else."""
    cell = state["cell"]
    if cell == "prefix":
        notice = dict(kind="initial")
    elif cell in REVISION_CELLS:
        notice = dict(kind="change", owner=world["owner"], record=world["row"])
        if agent == world["owner"]:
            notice["value"] = world["after"]
    else:
        notice = dict(kind="none")
    return dict(agent=agent, phase="initial" if cell == "prefix" else "new",
                invocation=state["turns"][agent] + 1,
                partner_finished=state["submissions"][1 - agent] is not None,
                history=deepcopy(state["history"][agent]), earlier=state["earlier"][agent],
                notice=notice, shard=list(cell_shards(world, cell)[agent]))


def _entries(history):
    rendered = []
    for entry in history:
        if entry["kind"] == "own_action":
            a = entry["action"]
            m = a["message"] if a["message"] is not None else "null"
            s = str(a["submit"]) if a["submit"] is not None else "null"
            content = f"Your action:\nmessage={m}\nsubmit={s}; wait={str(a['wait']).lower()}"
        elif entry["kind"] == "received_message":
            content = f"From agent {entry['sender']}:\n{entry['text']}"
        elif entry["kind"] == "feedback":
            content = "Environment feedback:\n" + entry["text"]
        else:
            raise ValueError("unknown history entry")
        rendered.append("BEGIN VISIBLE ENTRY\n" + content + "\nEND VISIBLE ENTRY")
    return "\n".join(rendered) or "(no visible entries)"


def notice_text(notice):
    if notice["kind"] == "initial":
        return NOTICE_INITIAL
    if notice["kind"] == "none":
        return NOTICE_NONE
    if notice["kind"] != "change":
        raise ValueError("unknown notice")
    text = NOTICE_CHANGE + f"\nChanged record: agent {notice['owner']} record {notice['record']}"
    if "value" in notice:
        text += (f"\nReplacement value for your record agent {notice['owner']} "
                 f"record {notice['record']}: {notice['value']}")
    return text


def messages(view, *, control=False):
    """Exact system and user messages for one call (section 3.4 and 3.7)."""
    if control:
        return [{"role": "system", "content": CONTROL_SYSTEM},
                {"role": "user", "content": "Complete input: " + str(view["complete_input"])}]
    a, history, boundary = view["agent"], view["history"], view["earlier"]
    if type(boundary) is not int or not 0 <= boundary <= len(history):
        raise ValueError("invalid earlier-phase boundary")
    phase = "initial" if view["phase"] == "initial" else "new phase after an earlier phase"
    body = (f"You are agent {a}. Your partner is agent {1 - a}.\n"
            f"This phase: {phase}.\n"
            f"Your invocation: {view['invocation']}/3.\n"
            f"Partner finished: {str(view['partner_finished']).lower()}. "
            "This is status only; no value is disclosed.\n\n"
            "VISIBLE HISTORY: EARLIER PHASE\n" + _entries(history[:boundary]) + "\n\n"
            "VISIBLE HISTORY: THIS PHASE\n" + _entries(history[boundary:]) + "\n\n"
            "ENVIRONMENT NOTICE\n" + notice_text(view["notice"]) + "\n\n"
            "CURRENT AUTHORITATIVE PRIVATE SHARD\n" +
            "\n".join(f"agent {a} record {i}: {v}" for i, v in enumerate(view["shard"])) +
            "\n\nChoose one legal action for the current phase. Return only the JSON object.")
    return [{"role": "system", "content": THESIS_SYSTEM}, {"role": "user", "content": body}]


def control_view(world, phase):
    shards = world[phase]
    return dict(complete_input=list(shards[0]) + list(shards[1]))


def score(world, state):
    """1: both submissions equal the current answer; 0: other terminal; None: unknown."""
    if state is None or not state.get("terminal"):
        return None
    truth = world["original_truth"] if state["cell"] == "prefix" else cell_truth(world, state["cell"])
    return int(state["submissions"] == [truth, truth])


NUMBER = re.compile(r"(?<![\d.])-?\d+(?![\d.])")


def funnel(world, state):
    """Deterministic evaluator-side descriptors of one terminal episode (section 3.9)."""
    if state is None or not state.get("terminal"):
        return None
    cell = state["cell"]
    shards = world["original"] if cell == "prefix" else cell_shards(world, cell)
    truth = world["original_truth"] if cell == "prefix" else cell_truth(world, cell)
    holders = [a for a in (0, 1) if truth in shards[a]]
    needers = [a for a in (0, 1) if a not in holders]

    def classify(agent):
        value = state["submissions"][agent]
        if value is None:
            return "absent"
        if value == truth:
            return "correct"
        if cell in REVISION_CELLS and value == world["original_truth"]:
            return "old_answer"
        if value == max(shards[agent]):
            return "own_local_max"
        if value in shards[agent]:
            return "other_own"
        if value in shards[1 - agent]:
            return "partner_value"
        return "neither_shard"

    delivered = {}
    for agent in needers:
        texts = [e["text"] for e in state["history"][agent] if e["kind"] == "received_message"]
        delivered[agent] = any(int(n) == truth for t in texts for n in NUMBER.findall(t))
    classes = [classify(a) for a in (0, 1)]
    both = all(v is not None for v in state["submissions"])
    return dict(holders=holders, needers=needers, delivered_to_needer=delivered,
                submissions=list(state["submissions"]), classes=classes,
                holder_correct=[classes[a] == "correct" for a in holders],
                needer_correct=[classes[a] == "correct" for a in needers],
                completed=both, success=int(state["submissions"] == [truth, truth]),
                wrong_agreement=both and state["submissions"][0] == state["submissions"][1] != truth,
                wrong_disagreement=both and state["submissions"][0] != state["submissions"][1],
                terminal=state["terminal"])
