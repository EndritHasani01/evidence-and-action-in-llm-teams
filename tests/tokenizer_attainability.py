"""Retain/reproduce the native local-view witness; CPU only, no inference."""

import argparse
from dataclasses import asdict, replace
import gzip
import importlib.metadata
import json
from pathlib import Path
import unittest

from recovery.prompts import render_request, tokenize_request
from recovery.protocol import GeneratedReply, validate_reply
from recovery.replay import commit_continuation_round, held_prose_counts
from recovery.schedule import _prepare_branches
from recovery.state import ReceivedProse, Slot, initial_view
from recovery.tasks import PEERS, Size, SourceRecord, Task
from recovery.truth import exact_candidate, solve_world
from recovery.witness import local_candidate, witness_reply
from tests.attainability_checks import execute_witness
from tests.event_checks import case_world

FIXTURE = Path(__file__).resolve().parent / "fixtures/attainability_traces.json.gz"
REVISION = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"


def provenance():
    return {"tokenizer": "Qwen/Qwen3.5-9B", "revision": REVISION,
            "packages": {name: importlib.metadata.version(name) for name in
                         ("pydantic", "transformers", "tokenizers", "jinja2", "huggingface-hub")},
            "scope": "Local-view scripted attainability and output contracts; no capacity or model-capability admission."}


def call_record(call, view, encoded, outcome):
    return {"call": asdict(call), "slot": asdict(view.slot),
            "local_sources": [asdict(s) for s in view.sources],
            "source_deliveries": [asdict(s) for s in view.source_deliveries],
            "solver": "complete_local_evidence" if local_candidate(view) is not None else "placeholder",
            "request_tokens": encoded.input_tokens, "generated": asdict(outcome.generated),
            "protocol_valid": outcome.protocol_valid}


def output_shapes(tokenizer):
    """Actual outer serialization, reference spellings and correct-value ranges.

    Wrong integers have no added mathematical cap. The 384 generated-token
    contract limits those outputs; retained large mistakes are capacity fixtures.
    """

    rows = []
    for size in Size:
        for task in Task:
            world = case_world(task, size).world
            for peer in (*PEERS, None):
                view = initial_view(world, peer)
                complete = witness_reply(initial_view(world, None), tokenizer)
                candidate = json.loads(complete.text)["candidate"]
                if task in (Task.PREFIX, Task.SORT) and peer is not None:
                    m = size.shard_size
                    candidate = candidate[peer*m:(peer+1)*m]
                # Bound correct integer widths (including signed differences
                # and unreachable BFS); deliberately allow unattainable mixes.
                if task is Task.BFS:
                    candidate = {str(j): -1 for j in range(size.node_count)}
                else:
                    maximum = (9 * size.numeric_length if task is Task.PREFIX else
                               -30 if task is Task.DIFFERENCE else 99)
                    candidate = [maximum] * len(candidate)
                forward = witness_reply(view, tokenizer)
                sends = [[], json.loads(forward.text)["send"]] if peer is not None else [[]]
                for send in sends:
                    text = json.dumps({"candidate": candidate, "send": send}, separators=(",", ":"))
                    raw = GeneratedReply(text, tuple(tokenizer.encode(text, add_special_tokens=False)), "scripted")
                    outcome = validate_reply(view, raw, tokenizer)
                    rows.append({"task": task.value, "size": size.value, "peer": peer,
                                 "shape": "candidate_empty_send" if not send else "candidate_own_shard",
                                 "text": text, "token_ids": list(raw.token_ids),
                                 "output_tokens": outcome.output_tokens,
                                 "prose_tokens": outcome.prose_tokens, "protocol_valid": outcome.protocol_valid})
    return rows


def witness_archive(tokenizer):
    cases = []
    for size in Size:
        for task in Task:
            world = case_world(task, size)
            prefix, continuations, controls = execute_witness(world, tokenizer)
            prefix_calls = next(b.calls for b in _prepare_branches((world,)) if b.phase == "prefix")
            rows, parents = [], {}
            for r, result in enumerate(prefix.rounds):
                req = result.barrier.requests
                rows.append({"branch_id": req.before.branch_id, "event": "original", "policy": None,
                             "replicate": 0, "slot": asdict(req.slot),
                             "calls": [call_record(prefix_calls[4*r+p], req.views[p], req.tokenized[p],
                                                   result.barrier.replies[p]) for p in PEERS]})
            for branch, rounds, state in continuations:
                for saved in rounds:
                    req = saved.barrier.requests
                    comparisons = []
                    for p, call in enumerate(saved.calls):
                        if call.replay_parent is not None:
                            parent, i = parents[call.replay_parent]
                            old = parent.barrier.requests
                            comparisons.append({"call_id": call.call_id, "parent": call.replay_parent,
                                "equal": {"view": req.views[p] == old.views[i],
                                          "rendered": req.rendered[p] == old.rendered[i],
                                          "native_input": req.tokenized[p] == old.tokenized[i],
                                          "settings": saved.settings_json == parent.settings_json,
                                          "seed": call.seed == parent.calls[i].seed,
                                          "reply": saved.barrier.replies[p] == parent.barrier.replies[i]}})
                        parents[call.call_id] = (saved, p)
                    committed = commit_continuation_round(saved).committed
                    rows.append({"branch_id": branch.branch_id, "event": branch.event,
                                 "policy": branch.policy, "replicate": branch.replicate,
                                 "slot": asdict(req.slot), "parent_comparisons": comparisons,
                                 "calls": [call_record(saved.calls[p], req.views[p], req.tokenized[p],
                                                       saved.barrier.replies[p]) for p in PEERS],
                                 "held_prose_counts": list(held_prose_counts(committed)),
                                 "pending_prose_ids": [d.delivery_id for d in committed.pending if d.text is not None],
                                 "received_prose": [[asdict(h) for h in peer.history if type(h) is ReceivedProse]
                                                    for peer in committed.peers]})
                assert not state.pending and state.next_slot is None
            for branch, view, encoded, outcome in controls:
                rows.append({"branch_id": branch.branch_id, "event": branch.event, "policy": None,
                             "replicate": 0, "slot": asdict(view.slot),
                             "calls": [call_record(branch.calls[0], view, encoded, outcome)]})
            cases.append({"world_id": world.world_id, "task": task.value, "size": size.value,
                          "manifest": [asdict(s) for s in prefix.rounds[0].barrier.requests.views[0].manifest],
                          "rounds": rows})
    return json.loads(json.dumps({"provenance": provenance(), "output_shapes": output_shapes(tokenizer),
                                  "cases": cases}, ensure_ascii=True))


class NativeAttainabilityTests(unittest.TestCase):
    current = None
    expected = None
    tokenizer = None

    def test_exact_local_view_trace_and_output_table_reproduce(self):
        for field in ("cases", "output_shapes"):
            self.assertEqual(self.current[field], self.expected[field])
        for field in ("tokenizer", "revision"):
            self.assertEqual(self.current["provenance"][field], self.expected["provenance"][field])

    def test_every_recorded_native_reply_and_correct_width_contract_fits(self):
        for shape in self.current["output_shapes"]:
            self.assertTrue(shape["protocol_valid"], shape)
            self.assertLessEqual(shape["output_tokens"], 384)
        for case in self.current["cases"]:
            for row in case["rounds"]:
                for call in row["calls"]:
                    self.assertTrue(call["protocol_valid"])
                    self.assertLessEqual(len(call["generated"]["token_ids"]), 384)
                    self.assertLessEqual(call["request_tokens"] + 384, 8192)

    def test_final_answers_match_independent_host_evaluation_and_local_inputs(self):
        for case in self.current["cases"]:
            task, size = Task(case["task"]), Size(case["size"])
            world = case_world(task, size)
            for row in case["rounds"]:
                if row["slot"]["round_number"] != 4 and row["slot"]["phase"] != "control":
                    continue
                gold = solve_world(world.world if row["event"] == "original" else world.event_world(row["event"]))
                for call in row["calls"]:
                    peer = call["call"]["peer"]
                    self.assertEqual(call["solver"], "complete_local_evidence")
                    values = json.loads(call["generated"]["text"])["candidate"]
                    self.assertTrue(exact_candidate(gold, values, peer))
                    # Replay the solver solely from the recorded local inputs.
                    base = initial_view(world.world, peer)
                    sources = tuple(SourceRecord(**dict(s, value=tuple(s["value"]) if type(s["value"]) is list
                                                        else s["value"])) for s in call["local_sources"])
                    local = replace(base, sources=sources, source_deliveries=())
                    self.assertEqual(local_candidate(local), values)

    def test_exact_parent_joins_and_q_release_preserve_sources_and_prose_once(self):
        for case in self.current["cases"]:
            calls = {}
            for row in case["rounds"]:
                for call in row["calls"]:
                    key = call["call"]["call_id"]
                    self.assertNotIn(key, calls)
                    calls[key] = call
                for comparison in row.get("parent_comparisons", []):
                    self.assertTrue(all(comparison["equal"].values()))
                    current, parent = calls[comparison["call_id"]], calls[comparison["parent"]]
                    self.assertEqual(current["local_sources"], parent["local_sources"])
                    self.assertEqual(current["generated"], parent["generated"])
                if row["policy"] in ("Q_B", "Q_C"):
                    self.assertEqual(row["held_prose_counts"], [1]*4)
                    self.assertEqual(len(row["pending_prose_ids"]), 4 if row["slot"]["round_number"] == 1 else 0)
                    for history in row["received_prose"]:
                        labels = [(h["slot"]["phase"], h["slot"]["round_number"], h["sender"]) for h in history]
                        self.assertEqual(len(labels), len(set(labels)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create a new CPU witness archive")
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    current = witness_archive(tokenizer)
    fixture = args.write_fixture or args.fixture
    if args.write_fixture:
        with fixture.open("xb") as output:
            payload = (json.dumps(current, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode()
            output.write(gzip.compress(payload, mtime=0) if fixture.suffix == ".gz" else payload)
    NativeAttainabilityTests.current = current
    payload = fixture.read_bytes()
    NativeAttainabilityTests.expected = json.loads(gzip.decompress(payload) if fixture.suffix == ".gz" else payload)
    NativeAttainabilityTests.tokenizer = tokenizer
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeAttainabilityTests))
    for size in Size:
        rows = [r for r in current["output_shapes"] if r["size"] == size.value]
        print(f"{size.value}: max candidate/control/own-shard reply {max(r['output_tokens'] for r in rows)} / 384 tokens")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
