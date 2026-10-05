"""Native-tokenizer scripted rounds and a reproducible complete trace archive.

Run with --tokenizer <local pinned Qwen metadata>. No model weights, inference,
GPU, event-policy admission, complete worst-context proof or accepted freeze.
"""

import argparse
from dataclasses import asdict
import importlib.metadata
import json
from pathlib import Path
import unittest

from recovery.prompts import MAX_CONTEXT_TOKENS

from recovery.rounds import deserialize_state, fork_prefix, run_prefix, run_round, snapshot_bytes
from recovery.state import Slot
from recovery.tasks import PEERS, Size, Task
from tests.round_checks import PREFIX_ID, mixed_provider, world

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests/fixtures/round_traces.json"


def trace_archive(tokenizer):
    prefix = run_prefix(world(), PREFIX_ID, tokenizer, mixed_provider(tokenizer))
    state = fork_prefix(prefix.snapshot, "scripted/recovery/untransformed/none/rep0")
    traces = list(prefix.rounds)
    for _ in range(4):
        result = run_round(state, tokenizer, mixed_provider(tokenizer))
        traces.append(result)
        state = result.committed
    rounds = []
    for result in traces:
        barrier = result.barrier
        rounds.append({
            "slot": asdict(barrier.requests.slot),
            "requests": [{"peer": p, "rendered": asdict(barrier.requests.rendered[p]),
                          "tokenized": asdict(barrier.requests.tokenized[p])} for p in PEERS],
            "replies": [asdict(reply) for reply in barrier.replies],
            "deliveries": [asdict(d) for d in result.committed.deliveries[len(barrier.requests.before.deliveries):]],
            "committed_peers": [asdict(p) for p in result.committed.peers],
        })
    return {"provenance": {
        "tokenizer": "Qwen/Qwen3.5-9B",
        "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
        "packages": {name: importlib.metadata.version(name) for name in
                     ("pydantic", "transformers", "tokenizers", "jinja2", "huggingface-hub")},
        "scope": "Scripted in-memory prefix and untransformed continuation; no model, event, replay or capacity admission.",
    }, "trace": {
        "rounds": rounds,
        "prefix_snapshot": json.loads(prefix.snapshot),
        "final_snapshot": json.loads(snapshot_bytes(state)),
        "owner_v1_exposure": {s.record_id: [asdict(slot) for slot in prefix.owner_v1_exposure(s)]
                              for s in state.manifest},
    }}


class TokenizerRoundTests(unittest.TestCase):
    tokenizer = None
    expected = None

    def test_saved_trace_exact_requests_native_ids_raw_replies_delivery_and_committed_state(self):
        current = json.loads(json.dumps(trace_archive(self.tokenizer)))
        self.assertEqual(current["trace"], self.expected["trace"])
        for key in ("tokenizer", "revision"):
            self.assertEqual(current["provenance"][key], self.expected["provenance"][key])
        self.assertEqual(len(current["trace"]["rounds"]), 8)
        self.assertEqual(current["trace"]["prefix_snapshot"]["pending"], [])
        self.assertEqual(current["trace"]["final_snapshot"]["pending"], [])

    def test_native_both_sizes_all_families_and_physical_orders_match_for_all_eight_rounds(self):
        inputs, outputs = [], []
        for task in Task:
            for size in Size:
                prefixes = [run_prefix(world(task, size), PREFIX_ID, self.tokenizer,
                                       mixed_provider(self.tokenizer), invocation_order=order)
                            for order in (PEERS, tuple(reversed(PEERS)))]
                self.assertEqual(prefixes[0], prefixes[1])
                states = [fork_prefix(p.snapshot, "scripted/recovery/untransformed/none/rep0") for p in prefixes]
                traces = list(prefixes[0].rounds)
                for _ in range(4):
                    results = [run_round(s, self.tokenizer, mixed_provider(self.tokenizer), invocation_order=order)
                               for s, order in zip(states, (PEERS, tuple(reversed(PEERS))))]
                    self.assertEqual(results[0], results[1])
                    traces.append(results[0])
                    states = [r.committed for r in results]
                self.assertEqual(deserialize_state(snapshot_bytes(states[0])), states[0])
                self.assertIsNone(states[0].next_slot)
                for trace in traces:
                    barrier = trace.barrier
                    for request, validation in zip(barrier.requests.tokenized, barrier.replies):
                        inputs.append(request.input_tokens)
                        self.assertLessEqual(request.input_tokens + 384, MAX_CONTEXT_TOKENS)
                        if validation.generated is not None:
                            generated = validation.generated
                            outputs.append(len(generated.token_ids))
                            self.assertEqual(self.tokenizer.decode(generated.token_ids,
                                skip_special_tokens=False, clean_up_tokenization_spaces=False), generated.text)
                            self.assertLessEqual(len(generated.token_ids), 384)
                    # These scripted invalid/failure outcomes must stay invalid/failed,
                    # never suppress an opportunity or cause token-induced accidents.
                    expected = {1: ("valid", "valid", "valid", "invalid"),
                                2: ("valid",) * 4,
                                3: ("invalid", "failed", "valid", "valid"),
                                4: ("valid", "valid", "invalid", "valid")}[barrier.requests.slot.round_number]
                    self.assertEqual(tuple(v.candidate.status for v in barrier.replies), expected)
        print(f"All-family scripted native requests: {min(inputs)}-{max(inputs)} input tokens; "
              f"{min(outputs)}-{max(outputs)} generated tokens; output reserve=384.")

    def test_actual_rendered_owner_v1_exposure_and_round_four_drain(self):
        prefix = run_prefix(world(), PREFIX_ID, self.tokenizer, mixed_provider(self.tokenizer))
        state = deserialize_state(prefix.snapshot)
        for source in state.manifest:
            self.assertEqual(prefix.owner_v1_exposure(source), tuple(Slot("prefix", r) for r in range(1, 5)))
        final = [d for d in state.deliveries if d.generated == Slot("prefix", 4)]
        self.assertTrue(final)
        self.assertTrue(all(d.first_usable == Slot("recovery", 1) for d in final))
        self.assertFalse(state.pending)
        for trace in prefix.rounds:
            for request in trace.barrier.requests.tokenized:
                self.assertNotIn(PREFIX_ID, request.text)
                self.assertNotIn('"delivery_id"', request.text)
                self.assertNotIn('"message_id"', request.text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True, help="local pinned metadata only")
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create a new scripted trace archive")
    args = parser.parse_args()
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    current = trace_archive(tokenizer)
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            output.write((json.dumps(current, ensure_ascii=True, sort_keys=True,
                                     separators=(",", ":")) + "\n").encode("utf-8"))
        fixture = args.write_fixture
    else:
        fixture = args.fixture
    TokenizerRoundTests.tokenizer = tokenizer
    TokenizerRoundTests.expected = json.loads(fixture.read_bytes())
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(TokenizerRoundTests))
    rows = current["trace"]["rounds"]
    for row in rows:
        inputs = [len(r["tokenized"]["input_ids"]) for r in row["requests"]]
        attempts = sum(d["source"] is not None for d in row["deliveries"])
        acquired = sum(d["acquired"] is True for d in row["deliveries"])
        print(f"{row['slot']['phase']} r{row['slot']['round_number']}: "
              f"input={min(inputs)}-{max(inputs)}, source attempts={attempts}, acquisitions={acquired}, "
              f"outcomes={','.join(v['candidate']['status'] for v in row['replies'])}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
