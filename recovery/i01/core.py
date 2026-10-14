"""Native mathematics, fixed schedules, permitted views and phase-final actions."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import random

from . import REGIME

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
    for proposal in range(1, 1001):
        shards = [[rng.randint(-1000, 1000) for _ in range(20)] for _ in range(2)]
        if not eligible(shards) or oracle(shards) not in shards[owner]:
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
                     first=first, device=index % 2, treatments=["retain", "clear"] if index % 2 == 0 else ["clear", "retain"])
        world["seeds"] = {phase: [[seed_for(master, identity, phase, a, k) for k in range(3)]
                                  for a in range(2)] for phase in ("prefix", "recovery")}
        world["control_seeds"] = {p: seed_for(master, identity, "control", p) for p in ("original", "revised")}
        return world
    raise ValueError(f"mathematical proposal limit exhausted: {identity}")


def manifests(config):
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


def initial_episode(world, phase, prefix=None):
    if phase not in ("prefix", "retain", "clear"):
        raise ValueError("unknown phase")
    history = deepcopy(prefix["history"]) if phase == "retain" else [[], []]
    return dict(world=world["id"], phase=phase, history=history, turns=[0, 0], submissions=[None, None],
                waiting=[False, False], next=world["first"], events=[], terminal=None, unused=None)


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


def apply_outcome(state, agent, action, error, call_id):
    state = deepcopy(state)
    if next_agent(state) != agent:
        raise ValueError("call differs from saved eligible turn")
    state["turns"][agent] += 1
    state["next"] = 1 - agent
    event = dict(call=call_id, agent=agent, action=action, error=error)
    state["events"].append(event)
    if action is None:
        state["history"][agent].append(dict(kind="feedback", text="Previous action invalid; no action delivered."))
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
    if revised:
        view["revision_notice"] = dict(owner=world["owner"], record=world["row"])
        if agent == world["owner"]:
            view["revision_notice"]["new_value"] = world["after"]
    return view


def messages(view, *, control=False):
    if control:
        body = "Complete input: " + str(view["complete_input"])
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
    return [{"role": "system", "content": CONTROL_SYSTEM if control else SYSTEM}, {"role": "user", "content": body}]


def success(state, truth):
    return None if state is None or not state.get("terminal") else int(state["submissions"] == [truth, truth])
