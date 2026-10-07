"""Synthetic saved evaluator inputs; real protocol evidence uses the M3 bundle."""

from dataclasses import asdict, replace
import json

from recovery.prompts import render_request
from recovery.state import CandidateState, HistoricalReceipt, OwnReply, RevisionNotice, Slot, initial_view
from recovery.tasks import Task, source_manifest
from tests.estimand_fixture import prepared
from tests.outcome_fixture import encode, saved_records


class CharacterTokenizer:
    def encode(self, text, *, add_special_tokens=False):
        assert not add_special_tokens
        return list(map(ord, text))


def fixture(task=Task.PREFIX, policies=("B", "C", "F", "K", "B_delta", "C_delta", "K_delta"), size="target", wrong_prefix=False):
    population, schedules = prepared(size)
    world = next(w for w in population.main if w.world.task is task)
    worlds = (world,)
    branches = tuple(b for b in schedules.main if b.world_id == world.world_id and (b.phase == "prefix" or
        b.phase == "continuation" and b.event == "revision" and b.policy in policies and b.replicate == 0))
    records, inputs, attempts = saved_records(worlds, branches)
    if wrong_prefix:
        for branch in branches:
            if branch.phase == "prefix":
                for call in branch.calls:
                    if call.round_number == 4:
                        row = records[call.call_id]
                        raw, validation = json.loads(row["raw_json"]), json.loads(row["validation_json"])
                        reply = json.loads(raw["text"])
                        if task is Task.BFS:
                            reply["candidate"]["0"] += 17
                            validation["candidate"]["value"][0][1] += 17
                        else:
                            reply["candidate"][0] += 17
                            validation["candidate"]["value"][0] += 17
                        raw["text"] = encode(reply)
                        validation["generated"] = raw
                        row.update(raw_json=encode(raw), validation_json=encode(validation))
    world = worlds[0]
    for branch in branches:
        current = world.world if branch.phase == "prefix" else world.event_world(branch.event)
        for number in range(1, 5):
            saved = inputs[branch.branch_id, number]
            state = json.loads(saved["requests"]["before"])
            state.update(manifest=[asdict(s) for s in source_manifest(current)], pending=[], committed=True,
                last_slot=None if number == 1 else {"phase": state["phase"], "round_number": number - 1},
                prefix_parent=branch.prefix_parent)
            peers, rendered, tokenized = [], [], []
            for peer in range(4):
                history = ()
                candidate = CandidateState()
                if number > 1:
                    call_id = f"{branch.branch_id}/r{number - 1}/p{peer}"
                    history = (OwnReply(Slot(state["phase"], number - 1), json.loads(records[call_id]["raw_json"])["text"]),)
                    answer = json.loads(json.loads(records[call_id]["raw_json"])["text"])["candidate"]
                    candidate = CandidateState.valid(task, current.size, peer, Slot(state["phase"], number - 1), answer)
                if branch.policy in ("B", "B_delta"):
                    prefix_id = f"{branch.prefix_parent}/r4/p{peer}"
                    raw_text = json.loads(records[prefix_id]["raw_json"])["text"]
                    history = (OwnReply(Slot("prefix", 4), raw_text), *history)
                    if number == 1:
                        candidate = CandidateState.valid(task, current.size, peer, Slot("prefix", 4), json.loads(raw_text)["candidate"])
                if branch.policy in ("K", "K_delta"):
                    prefix_id = f"{branch.prefix_parent}/r4/p{peer}"
                    answer = json.loads(json.loads(records[prefix_id]["raw_json"])["text"])["candidate"]
                    historical = CandidateState.valid(task, current.size, peer, Slot("prefix", 4), answer, historical=True)
                    if number == 1:
                        candidate = historical
                    else:
                        history = (historical, *history)
                notice, receipt = None, None
                if branch.phase == "continuation":
                    source = next(r for r in current.records if r.version == 2)
                    public = next(r for r in source_manifest(current) if r.record_id == source.record_id)
                    notice = RevisionNotice(public, 1, 2)
                    if task in (Task.PREFIX, Task.SORT):
                        old = next(r.value for r in world.world.records if r.record_id == source.record_id)
                        receipt = HistoricalReceipt(public, 1, 2, old if branch.policy.endswith("_delta") else None)
                view = replace(initial_view(world.world, peer), sources=current.records,
                    slot=Slot(state["phase"], number), history=history, candidate=candidate,
                    notice=notice, receipt=receipt, source_deliveries=())
                peers.append({k: asdict(view)[k] for k in ("sources", "history", "candidate", "feedback", "notice", "receipt", "source_deliveries")})
                request = asdict(render_request(view))
                rendered.append(request)
                tokenized.append({"text": request["content"], "input_ids": list(map(ord, request["content"]))})
            state["peers"] = peers
            for d in state["deliveries"]:
                d.update(message_id=d["delivery_id"].split("/x")[0], text=None, sender=None, generated=None, acquired=True)
            saved["requests"].update(before=encode(state), rendered=rendered, tokenized=tokenized)
    for row in records.values():
        validation = json.loads(row["validation_json"])
        validation.update(messages=[], prose_tokens=0, feedback=None, feedback_tokens=0)
        row["validation_json"] = encode(validation)
    committed = {}
    for branch in branches:
        state = json.loads(inputs[branch.branch_id, 4]["requests"]["before"])
        state["last_slot"] = {"phase": state["phase"], "round_number": 4}
        committed[branch.branch_id] = {"state": state}
    return worlds, branches, records, inputs, attempts, committed


def set_sources(saved, peer, sources):
    """Change synthetic source view and its exact rendering together."""
    state = json.loads(saved["requests"]["before"])
    state["peers"][peer]["sources"] = sources
    content = saved["requests"]["rendered"][peer]["content"]
    from recovery.prompts import DATA_MARKER
    payload = content.split(DATA_MARKER, 1)[1]
    data, offset = json.JSONDecoder().raw_decode(payload)
    data["current_sources"] = [{**{k: s[k] for k in ("record_id", "owner", "version", "position") if s[k] is not None},
        "status": "known", "value": s["value"]} for s in sources]
    content = content.split(DATA_MARKER, 1)[0] + DATA_MARKER + json.dumps(data, separators=(",", ":")) + payload[offset:]
    saved["requests"]["rendered"][peer]["content"] = content
    saved["requests"]["tokenized"][peer] = {"text": content, "input_ids": list(map(ord, content))}
    saved["requests"]["before"] = encode(state)
