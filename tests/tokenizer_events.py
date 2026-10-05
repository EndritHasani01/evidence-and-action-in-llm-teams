"""Native-tokenizer boundary snapshots, paired receipt renders and token costs.

Uses pinned local metadata only; no inference, model weights or capacity gate.
"""

import argparse
from dataclasses import asdict
import importlib.metadata
import json
from pathlib import Path
import unittest

from recovery.events import start_continuation
from recovery.prompts import MAX_CONTEXT_TOKENS, RenderedRequest, render_request, rendered_data
from recovery.protocol import token_count
from recovery.rounds import deserialize_state, prepare_round, run_round, snapshot_bytes
from recovery.schedule import _prepare_branches
from recovery.state import CandidateState, Slot
from recovery.tasks import PEERS, Size, Task
from tests.event_checks import build_prefix, case_world, data, event_provider, start

FIXTURE = Path(__file__).resolve().parent / "fixtures/event_boundaries.json"


def request_records(state, tokenizer):
    requests = prepare_round(state, tokenizer)
    return [{"peer": p, "rendered": asdict(requests.rendered[p]),
             "tokenized": asdict(requests.tokenized[p]),
             "input_tokens": requests.tokenized[p].input_tokens,
             # This is the serialized receipt field's token cost. Whole-input
             # pair differences below include actual neighboring tokenization.
             "receipt_tokens": (0 if view.receipt is None else token_count(
                 json.dumps(data(view)["historical_receipt"], ensure_ascii=True, separators=(",", ":")), tokenizer))}
            for p, view in enumerate(requests.views)]


def boundary_archive(tokenizer):
    cases = []
    for task, size in ((Task.PREFIX, Size.TARGET), (Task.SORT, Size.FALLBACK),
                       (Task.BFS, Size.TARGET), (Task.TOP_K, Size.FALLBACK)):
        world = case_world(task, size)
        prefix = build_prefix(world, tokenizer)
        pairs = ([("revision", p) for p in ("B", "B_delta", "C", "C_delta", "K", "K_delta")]
                 if task in (Task.PREFIX, Task.SORT) else
                 [("revision", "L"), ("revision", "B")] if task is Task.BFS else [("preserving", "B")])
        boundaries = []
        for event, policy in pairs:
            state = start(world, prefix, policy, event)
            boundaries.append({"event": event, "policy": policy,
                "snapshot": json.loads(snapshot_bytes(state)), "requests": request_records(state, tokenizer)})
        contrasts = []
        if task in (Task.PREFIX, Task.SORT):
            for ordinary, disclosed in zip(boundaries[::2], boundaries[1::2]):
                contrasts.append({"ordinary": ordinary["policy"], "disclosed": disclosed["policy"],
                    "input_token_difference_per_peer": [b["input_tokens"] - a["input_tokens"]
                        for a, b in zip(ordinary["requests"], disclosed["requests"])]})
        cases.append({"world_id": world.world_id, "task": task.value, "size": size.value,
                      "prefix_snapshot": json.loads(prefix.snapshot),
                      "boundaries": boundaries, "receipt_contrasts": contrasts})
    return {"provenance": {
        "tokenizer": "Qwen/Qwen3.5-9B", "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
        "packages": {name: importlib.metadata.version(name) for name in
                     ("pydantic", "transformers", "tokenizers", "jinja2", "huggingface-hub")},
        "scope": "Scripted original-prefix boundaries and actual receipt token costs; no model or capacity admission.",
    }, "cases": cases}


class TokenizerEventTests(unittest.TestCase):
    tokenizer = None
    current = None
    expected = None

    def test_saved_boundaries_exact_snapshots_requests_native_ids_and_receipt_costs(self):
        self.assertEqual(self.current["cases"], self.expected["cases"])
        for key in ("tokenizer", "revision"):
            self.assertEqual(self.current["provenance"][key], self.expected["provenance"][key])
        for case in self.current["cases"]:
            for boundary in case["boundaries"]:
                state = deserialize_state(json.dumps(boundary["snapshot"]).encode())
                self.assertTrue(state.boundary_applied)
                self.assertEqual(json.loads(snapshot_bytes(state)), boundary["snapshot"])
                self.assertEqual(state.next_slot, Slot("recovery", 1))
                for request in boundary["requests"]:
                    self.assertEqual(request["input_tokens"], len(request["tokenized"]["input_ids"]))
                    self.assertLessEqual(request["input_tokens"] + 384, MAX_CONTEXT_TOKENS)

    def test_native_receipt_pairs_change_only_before_value_with_real_unpadded_cost(self):
        for case in self.current["cases"][:2]:
            for ordinary, disclosed in zip(case["boundaries"][::2], case["boundaries"][1::2]):
                for left, right in zip(ordinary["requests"], disclosed["requests"]):
                    a = rendered_data(RenderedRequest(**left["rendered"]))
                    b = rendered_data(RenderedRequest(**right["rendered"]))
                    self.assertEqual(a["historical_receipt"]["before_value"], "not included in this receipt")
                    self.assertIs(type(b["historical_receipt"]["before_value"]), int)
                    a["historical_receipt"]["before_value"] = b["historical_receipt"]["before_value"]
                    self.assertEqual(a, b)
                    self.assertNotEqual(left["tokenized"]["input_ids"], right["tokenized"]["input_ids"])
                    self.assertGreater(left["receipt_tokens"], 0)
                    self.assertGreater(right["receipt_tokens"], 0)

    def test_all_families_sizes_event_boundaries_and_exact_mixed_parent_requests(self):
        inputs, outputs = [], []
        for size in Size:
            for task in Task:
                world = case_world(task, size)
                prefix = build_prefix(world, self.tokenizer)
                for result in prefix.rounds:
                    expected = {1: ("valid",) * 4, 2: ("valid",) * 3 + ("invalid",),
                                3: ("valid",) * 4, 4: ("valid", "invalid", "failed", "valid")}
                    self.assertEqual(tuple(r.candidate.status for r in result.barrier.replies),
                                     expected[result.barrier.requests.slot.round_number])
                    outputs.extend(len(r.generated.token_ids) for r in result.barrier.replies if r.generated)
                starts = {}
                for branch in _prepare_branches((world,)):
                    if branch.phase != "continuation" or branch.policy in ("Q_B", "Q_C"):
                        continue
                    state = start_continuation(prefix.snapshot, world, branch)
                    requests = prepare_round(state, self.tokenizer)
                    starts[(branch.event, branch.policy, branch.replicate)] = requests
                    for p, request in enumerate(requests.tokenized):
                        inputs.append(request.input_tokens)
                        self.assertNotIn(state.branch_id, request.text)
                        self.assertNotIn("reset_group", request.text)
                        self.assertEqual(requests.rendered[p], render_request(requests.views[p]))
                for (event, policy, replicate), requests in starts.items():
                    if policy not in ("P_G", "P_H"):
                        continue
                    group = world.partition[0 if policy == "P_G" else 1]
                    for p in PEERS:
                        parent = starts[(event, "C" if p in group else "B", replicate)]
                        self.assertEqual(requests.views[p], parent.views[p])
                        self.assertEqual(requests.rendered[p], parent.rendered[p])
                        self.assertEqual(requests.tokenized[p], parent.tokenized[p])
        print(f"All-family native boundary inputs: {min(inputs)}-{max(inputs)} tokens; "
              f"scripted prefix outputs: {min(outputs)}-{max(outputs)}; output reserve=384.")

    def test_native_continuations_accumulate_history_preserve_notices_and_do_not_recompact(self):
        for task, policy in ((Task.PREFIX, "K_delta"), (Task.SORT, "C_delta"),
                             (Task.BFS, "L"), (Task.BFS, "F")):
            world = case_world(task)
            prefix = build_prefix(world, self.tokenizer)
            state = start(world, prefix, policy)
            persistent = tuple((p.notice, p.receipt) for p in state.peers)
            retained = tuple(p.candidate for p in state.peers)
            for r in range(1, 5):
                result = run_round(state, self.tokenizer, event_provider(self.tokenizer))
                state = result.committed
                self.assertTrue(all(reply.protocol_valid for reply in result.barrier.replies))
                self.assertEqual(tuple((p.notice, p.receipt) for p in state.peers), persistent)
                self.assertTrue(all(p.candidate.slot == Slot("recovery", r) and not p.candidate.historical
                                    for p in state.peers))
                if policy == "K_delta":
                    for p, peer in enumerate(state.peers):
                        self.assertEqual([e for e in peer.history if type(e) is CandidateState], [retained[p]])
                self.assertEqual(deserialize_state(snapshot_bytes(state)), state)
            self.assertIsNone(state.next_slot)
            self.assertFalse(state.pending)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True, help="local pinned metadata only")
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create a new boundary archive")
    args = parser.parse_args()
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    current = json.loads(json.dumps(boundary_archive(tokenizer)))
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            output.write((json.dumps(current, ensure_ascii=True, sort_keys=True,
                                     separators=(",", ":")) + "\n").encode("utf-8"))
    TokenizerEventTests.tokenizer = tokenizer
    TokenizerEventTests.current = current
    TokenizerEventTests.expected = json.loads((args.write_fixture or args.fixture).read_bytes())
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TokenizerEventTests))
    for case in current["cases"]:
        for pair in case["receipt_contrasts"]:
            print(f"{case['task']}/{case['size']} {pair['disclosed']} minus {pair['ordinary']}: "
                  f"{pair['input_token_difference_per_peer']} input tokens per peer.")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
