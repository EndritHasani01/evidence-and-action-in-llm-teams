"""Native mathematics, fixed schedules, permitted views and phase-final actions."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import random

from . import REGIME, ASSISTED_REGIME, assisted

SYSTEM = '''Find the global maximum across two agents' current private integer shards.
Your current shard is authoritative. Coordinate using ordinary messages; claims are
not certified. Your submission is private unless you explicitly message it.
Return exactly one JSON object with keys message, submit, wait:
{"message": "text or null", "submit": null, "wait": false}
message is a string or null, submit an integer or null, wait a boolean.
You may message, submit, message and submit, or wait (without message/submission).
Submission is FINAL for this phase. Share necessary information before finishing.
Messages received after submission cannot cancel it. Only a factual revision
starts a new phase. Both agents must submit, with at most three calls each in a
phase. Unused turns cannot be transferred. Waiting wakes on a new message.
You receive no correctness feedback. Do not include reasoning outside the JSON.'''
CONTROL_SYSTEM = '''Find the maximum of the complete integer input below.
Return exactly {"message":null,"submit":INTEGER,"wait":false}.
No communication. A submission is final. No text outside the JSON.'''

ASSISTED_SYSTEM = '''You are one of two agents finding the global maximum across your current
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

An ENVIRONMENT SOURCE NOTICE is not a partner message, a partner maximum or
a partner submission. Its record index identifies a location, not an answer.
At a source-change boundary only the named record changes. The replacement
value is supplied only to that record's owner. Earlier-phase history records
what was visible then; current values come from your current shard.

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
Only an environment source change starts a new phase and reopens both agents.

Each agent has at most three calls per phase. Unused calls cannot be transferred.
Waiting wakes only on a delivered message. If both agents wait, neither can
send a waking message. Invalid replies use a call and deliver nothing.
There is no correctness feedback. Put no text outside the JSON object.'''

REJECTION_FEEDBACK = {
    "provider_failure": "Call failed; no action was delivered.",
    "truncated_action": "Invalid: output was truncated. Nothing was delivered.",
    "schema": "Invalid: output one JSON object with the required fields and types. Nothing was delivered.",
    "wait_requires_null_message_and_submit": "Invalid: wait requires null message and null submit. Nothing was delivered.",
    "empty_nonwaiting_action": "Invalid: choose message, submit, both, or wait. Nothing was delivered.",
}


def rejection_feedback(reason):
    return REJECTION_FEEDBACK.get(reason, REJECTION_FEEDBACK["schema"])


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                      separators=(",", ":"))


def seed_for(master, *parts):
    # Stable independent streams, never derived from execution order.
    return int.from_bytes(hashlib.sha256(canonical([master, *parts]).encode()).digest()[:8], "big") % 2**63


def oracle(shards):
    return max(value for shard in shards for value in shard)


def eligible(shards):
    values = [v for s in shards for v in s]
    winner = max(values)
    return values.count(winner) == 1 and max(v for v in values if v != winner) > -1000


def make_world(master, group, index, owner, first):
    identity = f"{group}-{index:02d}"
    rng = random.Random(seed_for(master, identity, "world"))
    rejections=dict(nonunique_maximum=0,remaining_at_floor=0,owner_block=0)
    for proposal in range(1, 1001):
        shards = [[rng.randint(-1000, 1000) for _ in range(20)] for _ in range(2)]
        values=[v for shard in shards for v in shard]
        winner=oracle(shards)
        if values.count(winner)!=1:
            rejections["nonunique_maximum"]+=1
            continue
        if max(v for v in values if v!=winner)<=-1000:
            rejections["remaining_at_floor"]+=1
            continue
        if winner not in shards[owner]:
            rejections["owner_block"]+=1
            continue
        row = shards[owner].index(oracle(shards))
        remaining = [v for a, s in enumerate(shards) for j, v in enumerate(s) if (a, j) != (owner, row)]
        second = max(remaining)
        replacement = rng.randint(-1000, second - 1)
        revised = deepcopy(shards)
        revised[owner][row] = replacement
        world = dict(id=identity, group=group, index=index, original=shards, revised=revised,
                     owner=owner, row=row, before=shards[owner][row], after=replacement,
                     original_truth=oracle(shards), revised_truth=oracle(revised), proposals=proposal,
                     rejections=rejections,
                     first=first, device=index % 2, treatments=["retain", "clear"] if index % 2 == 0 else ["clear", "retain"])
        world["seeds"] = {phase: [[seed_for(master, identity, phase, a, k) for k in range(3)]
                                  for a in range(2)] for phase in ("prefix", "recovery")}
        world["control_seeds"] = {p: seed_for(master, identity, "control", p) for p in ("original", "revised")}
        return world
    raise ValueError(f"mathematical proposal limit exhausted: {identity}")


def manifests(config):
    if assisted(config):
        if (config["main_worlds"] != 20 or config["attempt_limit"] != 500 or
            config["qualification_worlds"] != 4 or config["pilot_worlds"] != 4 or
            config["diagnostic_calls"] != 4 or config["contingency_limit"] != 20):
            raise ValueError("use the adopted assisted I-01 configuration")
        master = config["master_seed"]
        worlds = []
        combinations = [(0, "retain"), (0, "clear"), (1, "retain"), (1, "clear")]
        assignments = {}
        for s in range(4):
            choices = combinations + [combinations[s]]
            random.Random(seed_for(master, "assignment", s // 2, s % 2)).shuffle(choices)
            assignments[s] = choices
        pilots = [(0, "retain"), (1, "retain"), (0, "clear"), (1, "clear")]
        for group, count in (("qualification", 4), ("pilot", 4), ("main", 20)):
            for i in range(count):
                s = i % 4
                w = make_world(master, group, i, s // 2, s % 2)
                w["regime"] = ASSISTED_REGIME
                if group == "qualification":
                    w["device"] = s % 2
                    w["treatments"] = []
                else:
                    device, first_policy = assignments[s][i // 4] if group == "main" else pilots[s]
                    w["device"] = device
                    w["treatments"] = [first_policy, "clear" if first_policy == "retain" else "retain"]
                worlds.append(w)
        return dict(regime=ASSISTED_REGIME, config=config, worlds=worlds,
                    planned_first_attempts=480, direct_first_attempts=480,
                    stage_first_limits=dict(hardware=8, direct=8, diagnostic=4, pilot=80, main=380),
                    historical_attempts_separate=45)
    if config["regime"] != REGIME or config["main_worlds"] != 20 or config["attempt_limit"] != 500:
        raise ValueError("use the adopted I-01 configuration")
    worlds = []
    for group, count in (("qualification", 6), ("pilot", 3), ("main", 20)):
        for i in range(count):
            owner, first = ((i // 5) // 2, (i // 5) % 2) if group == "main" else (i % 2, (i // 2) % 2)
            worlds.append(make_world(config["master_seed"], group, i, owner, first))
    return dict(regime=REGIME, config=config, worlds=worlds, planned_first_attempts=472,
                direct_first_attempts=460, historical_attempts_separate=45)


def validate_action(text, *, truncated=False, control=False):
    if truncated:
        return None, "truncated_action"
    def no_duplicates(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise ValueError("duplicate key")
            result[k] = v
        return result
    try:
        value = json.loads(text, object_pairs_hook=no_duplicates)
        if type(value) is not dict or set(value) != {"message", "submit", "wait"}:
            raise ValueError("shape")
        m, s, w = value["message"], value["submit"], value["wait"]
        if (m is not None and (type(m) is not str or not m.strip()) or
            s is not None and type(s) is not int or type(w) is not bool or
            w and (m is not None or s is not None) or not w and m is None and s is None or
            control and (m is not None or s is None or w)):
            raise ValueError("types or action")
        return value, None
    except (ValueError, TypeError, RecursionError):
        return None, "malformed_action"


def check_disjoint_inputs(worlds, exposed):
    """Exact ordered whole-input overlap; diagnostics deliberately reuse qualification."""
    historical = {}
    for record in exposed:
        for phase in ("original", "revised"):
            historical.setdefault(canonical(record[phase]), record.get("id", "historical input"))
    seen = {}
    for world in worlds:
        for phase in ("original", "revised"):
            key = canonical(world[phase])
            if key in historical:
                raise ValueError(f"Exposed input overlap: {world['id']}/{phase} and {historical[key]}")
            if key in seen:
                raise ValueError(f"New input overlap: {world['id']}/{phase} and {seen[key]}")
            seen[key] = world["id"] + "/" + phase
    return dict(passed=True, checked_new_inputs=len(seen), distinct_exposed_inputs=len(historical))


def initial_episode(world, phase, prefix=None):
    if phase not in ("prefix", "retain", "clear"):
        raise ValueError("unknown phase")
    history = deepcopy(prefix["history"]) if phase == "retain" else [[], []]
    state = dict(world=world["id"], phase=phase, history=history, turns=[0, 0], submissions=[None, None],
                 waiting=[False, False], next=world["first"], events=[], terminal=None, unused=None)
    if assisted(world):
        state.update(regime=ASSISTED_REGIME,
                     earlier_history_lengths=[len(h) for h in history] if phase == "retain" else [0, 0])
    return state


def next_agent(state):
    if state["terminal"]:
        return None
    available = [a for a in range(2) if state["submissions"][a] is None and state["turns"][a] < 3 and not state["waiting"][a]]
    if not available:
        return None
    return state["next"] if state["next"] in available else available[0]


def finish(state):
    if all(v is not None for v in state["submissions"]):
        state["terminal"] = "both_submitted"
    elif next_agent(state) is None:
        state["terminal"] = ("waiting_deadlock" if any(state["waiting"][a] and state["submissions"][a] is None and state["turns"][a] < 3
                                                      for a in range(2)) else "horizon_exhausted")
    if state["terminal"]:
        state["unused"] = [3 - t for t in state["turns"]]
    return state


def apply_outcome(state, agent, action, error, call_id, *, feedback=None):
    state = deepcopy(state)
    if next_agent(state) != agent:
        raise ValueError("call differs from saved eligible turn")
    state["turns"][agent] += 1
    state["next"] = 1 - agent
    event = dict(call=call_id, agent=agent, action=action, error=error)
    state["events"].append(event)
    if action is None:
        text = (feedback or rejection_feedback(error)) if assisted(state) else "Previous action invalid; no action delivered."
        state["history"][agent].append(dict(kind="feedback", text=text))
    else:
        state["history"][agent].append(dict(kind="own_action", action=action))
        if action["message"] is not None:
            partner = 1 - agent
            state["history"][partner].append(dict(kind="received_message", sender=agent, text=action["message"]))
            state["waiting"][partner] = False
        if action["submit"] is not None:
            state["submissions"][agent] = action["submit"]
        state["waiting"][agent] = action["wait"]
    return finish(state)


def permitted_view(world, state, agent):
    revised = state["phase"] != "prefix"
    view = dict(agent=agent, current_shard=world["revised" if revised else "original"][agent],
                visible_history=deepcopy(state["history"][agent]), own_invocation=state["turns"][agent] + 1,
                partner_finished=state["submissions"][1-agent] is not None)
    if assisted(world):
        view.update(reopened=revised, earlier_history_length=state["earlier_history_lengths"][agent])
    if revised:
        view["revision_notice"] = dict(owner=world["owner"], record=world["row"])
        if agent == world["owner"]:
            view["revision_notice"]["new_value"] = world["after"]
    return view


def messages(view, *, control=False, regime=REGIME):
    if control:
        body = "Complete input: " + str(view["complete_input"])
    elif regime == ASSISTED_REGIME:
        def entries(history):
            rendered = []
            for entry in history:
                if entry["kind"] == "own_action":
                    a = entry["action"]
                    m = a["message"] if a["message"] is not None else "null"
                    s = str(a["submit"]) if a["submit"] is not None else "null"
                    content = f"Your action:\nmessage={m}\nsubmit={s}; wait={str(a['wait']).lower()}"
                elif entry["kind"] == "received_message":
                    content = f"From agent {entry['sender']}:\n{entry['text']}"
                else:
                    content = "Environment feedback:\n" + entry["text"]
                rendered.append("BEGIN VISIBLE ENTRY\n" + content + "\nEND VISIBLE ENTRY")
            return "\n".join(rendered) or "(no visible entries)"
        boundary = view["earlier_history_length"]
        history = view["visible_history"]
        if type(boundary) is not int or not 0 <= boundary <= len(history):
            raise ValueError("invalid literal earlier-phase boundary")
        notice = view.get("revision_notice")
        notice_text = "No source-change notice in this phase."
        if notice is not None:
            notice_text = ("Environment event: the following record changed before this phase began.\n"
                           f"Changed owner (agent identity): {notice['owner']}\n"
                           f"Changed record (index only): {notice['record']}")
            if "new_value" in notice:
                notice_text += f"\nReplacement value for your record: {notice['new_value']}"
        phase = "reopened after an environment source change" if view["reopened"] else "initial"
        body = (f"You are agent {view['agent']}. Your partner is agent {1-view['agent']}.\n"
                f"This phase: {phase}.\nYour invocation: {view['own_invocation']}/3.\n"
                f"Partner finished: {str(view['partner_finished']).lower()}. This is status only; no value is disclosed.\n\n"
                "VISIBLE HISTORY: EARLIER PHASE\n" + entries(history[:boundary]) + "\n\n"
                "VISIBLE HISTORY: THIS PHASE\n" + entries(history[boundary:]) + "\n\n"
                "ENVIRONMENT SOURCE NOTICE\n" + notice_text + "\n\n"
                "CURRENT AUTHORITATIVE PRIVATE SHARD\n" +
                "\n".join(f"record {i}: {v}" for i, v in enumerate(view["current_shard"])) +
                "\n\nChoose one legal action for the current phase. Return only the JSON object.")
        if view.get("diagnostic_directive"):
            body += "\n" + view["diagnostic_directive"]
    else:
        body = (f"You are agent {view['agent']}. Current private shard: {view['current_shard']}\n"
                f"Your invocation: {view['own_invocation']}/3. Partner finished: {view['partner_finished']}\n")
        if "revision_notice" in view:
            body += "Revision notice (new phase): " + canonical(view["revision_notice"]) + "\n"
        body += "Your visible history (literal actions/messages; not certified):\n"
        for entry in view["visible_history"]:
            if entry["kind"] == "received_message":
                body += f"From agent {entry['sender']}:\n{entry['text']}\n"
            elif entry["kind"] == "own_action":
                # Do not JSON-escape message content into a different token envelope.
                a = entry["action"]
                body += f"Your action: message={a['message']}\nsubmit={a['submit']}; wait={a['wait']}\n"
            else:
                body += entry["text"] + "\n"
    return [{"role": "system", "content": CONTROL_SYSTEM if control else ASSISTED_SYSTEM if regime == ASSISTED_REGIME else SYSTEM},
            {"role": "user", "content": body}]


def success(state, truth):
    return None if state is None or not state.get("terminal") else int(state["submissions"] == [truth, truth])


def diagnostic_fixture(manifest, label):
    """Four declared single-call views; scripted actions are never model-call rows."""
    if not assisted(manifest["config"]) or label not in ("D00", "D01", "D02", "D03"):
        raise ValueError("Unknown assisted diagnostic")
    index = {"D00": 0, "D01": 1, "D02": 3, "D03": 2}[label]
    world = next(w for w in manifest["worlds"] if w["id"] == f"qualification-{index:02d}")
    actor = 1 if label in ("D01", "D02") else 0
    state = initial_episode(world, "prefix")
    local = [max(shard) for shard in world["original"]]
    def scripted(agent, message=None, submit=None):
        nonlocal state
        state = apply_outcome(state, agent, dict(message=message, submit=submit, wait=False),
                              None, f"scripted/{label}/{len(state['events'])}")
    directive = None
    if label == "D00":
        directive = "Interface check: send only the message ready. Do not submit or wait."
        expected = "ready"
    elif label in ("D01", "D02"):
        scripted(1, f"My local maximum is {local[1]}.")
        scripted(0, f"My local maximum is {local[0]}.", world["original_truth"])
        if label == "D02":
            scripted(1, submit=world["original_truth"])
            state = initial_episode(world, "retain", state)
        expected = world["revised_truth" if label == "D02" else "original_truth"]
    else:
        state = initial_episode(world, "clear")
        directive = "Local-source check: send only your current shard's maximum as decimal message text. Do not submit or wait."
        expected = str(max(world["revised"][actor]))
    view = permitted_view(world, state, actor)
    if directive is not None:
        view["diagnostic_directive"] = directive
    return dict(id=world["id"]+"/diagnostic-"+label, label=label, world=world,
                actor=actor, state=state, view=view, expected=expected,
                seed=seed_for(manifest["config"]["master_seed"], world["id"], "diagnostic", label))


def diagnostic_pass(fixture, action):
    if action is None or validate_action(canonical(action))[0] is None:
        return False
    if fixture["label"] in ("D00", "D03"):
        return (action["message"] is not None and action["message"].strip() == fixture["expected"]
                and action["submit"] is None and not action["wait"])
    return action["submit"] == fixture["expected"] and not action["wait"]
