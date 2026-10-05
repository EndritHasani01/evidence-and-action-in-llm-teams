"""Native exact replay and queue traces, using pinned local tokenizer metadata only."""

import argparse
from dataclasses import asdict
import importlib.metadata
import json
from pathlib import Path
import unittest

from recovery.prompts import MAX_CONTEXT_TOKENS

from recovery.replay import (commit_continuation_round, held_prose_counts,
                             obtain_continuation_round)
from recovery.rounds import deserialize_state, snapshot_bytes
from recovery.state import Slot
from recovery.tasks import PEERS, Size, Task
from tests.event_checks import build_prefix, case_world, population
from tests.replay_checks import SETTINGS, parent_records, replay_provider, replay_start

FIXTURE = Path(__file__).resolve().parent / "fixtures/replay_traces.json"


def round_record(saved, parents=()):
    result = commit_continuation_round(saved)
    barrier = saved.barrier
    by_call = {call.call_id: (parent, p) for parent in parents for p, call in enumerate(parent.calls)}
    comparisons = []
    for p, call in enumerate(saved.calls):
        if call.replay_parent is not None:
            parent, i = by_call[call.replay_parent]
            prior = parent.barrier.requests
            current = barrier.requests
            comparisons.append({"call_id": call.call_id, "parent": call.replay_parent,
                "equal": {"permitted_view": current.views[p] == prior.views[i],
                          "rendered_request": current.rendered[p] == prior.rendered[i],
                          "native_input": current.tokenized[p] == prior.tokenized[i],
                          "settings": saved.settings_json == parent.settings_json,
                          "seed": call.seed == parent.calls[i].seed,
                          "recorded_reply": barrier.replies[p] == parent.barrier.replies[i]}})
    return {"branch_id": saved.branch.branch_id, "slot": asdict(barrier.requests.slot),
            "calls": [asdict(c) for c in saved.calls], "settings_json": saved.settings_json,
            "parent_comparisons": comparisons,
            "requests": [{"view": asdict(barrier.requests.views[p]),
                          "rendered": asdict(barrier.requests.rendered[p]),
                          "tokenized": asdict(barrier.requests.tokenized[p])} for p in PEERS],
            "replies": [asdict(r) for r in barrier.replies],
            "committed": json.loads(snapshot_bytes(result.committed)),
            "held_prose_counts": held_prose_counts(result.committed)}


def replay_archive(tokenizer):
    cases = []
    for task, size, traffic in ((Task.SORT, Size.TARGET, "rich"),
                                (Task.BFS, Size.FALLBACK, "rich"),
                                (Task.SORT, Size.TARGET, "unicode")):
        world = (case_world(task, size) if traffic == "rich" else
                 next(w for w in population(size).main if w.world.task is task and w.index == 3))
        prefix = build_prefix(world, tokenizer)
        rounds = []
        for event in ("revision", "sham"):
            parents = parent_records(world, prefix, tokenizer, event, mode=traffic)
            rounds.extend(round_record(p) for p in parents)
            for policy in ("P_G", "P_H", "Q_B", "Q_C"):
                saved = replay_start(world, prefix, parents, policy, event, tokenizer=tokenizer)
                rounds.append(round_record(saved, parents))
                # Retain each full Q horizon to audit actual append/release order.
                if policy.startswith("Q_"):
                    state = commit_continuation_round(saved).committed
                    for _ in range(3):
                        current = obtain_continuation_round(state, saved.branch, tokenizer,
                            replay_provider(tokenizer), settings=SETTINGS)
                        rounds.append(round_record(current))
                        state = commit_continuation_round(current).committed
        cases.append({"world_id": world.world_id, "task": task.value, "size": size.value,
                      "traffic": traffic, "prefix_snapshot": json.loads(prefix.snapshot), "rounds": rounds})
        if traffic != "rich":
            continue
        # Use a different predeclared saved world, not another response for the
        # same call ID. Retain its parents too so every archive join is auditable.
        silent_world = next(w for w in population(size).main if w.world.task is task and w.index == 2)
        silent_prefix = build_prefix(silent_world, tokenizer)
        parents = parent_records(silent_world, silent_prefix, tokenizer, "sham", mode="silent")
        inactive = replay_start(silent_world, silent_prefix, parents, "Q_C", "sham", tokenizer=tokenizer)
        cases.append({"world_id": silent_world.world_id, "task": task.value, "size": size.value,
                      "traffic": "source_only", "prefix_snapshot": json.loads(silent_prefix.snapshot),
                      "rounds": [*(round_record(p) for p in parents), round_record(inactive, parents)]})
    return {"provenance": {
        "tokenizer": "Qwen/Qwen3.5-9B", "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
        "packages": {name: importlib.metadata.version(name) for name in
                     ("pydantic", "transformers", "tokenizers", "jinja2", "huggingface-hub")},
        "scope": "Scripted exact-parent and Q queue traces; no inference, complete capacity or empirical result.",
    }, "cases": cases}


class TokenizerReplayTests(unittest.TestCase):
    tokenizer = None
    current = None
    expected = None

    def test_saved_unicode_invalid_parents_are_literal_schema_failures_with_no_effects(self):
        cases = [case for case in self.current["cases"] if case["traffic"] == "unicode"]
        self.assertEqual(len(cases), 1)
        for row in cases[0]["rounds"]:
            if row["slot"]["round_number"] != 1:
                continue
            invalid = row["replies"][2]
            self.assertTrue(invalid["json_valid"])
            self.assertFalse(invalid["schema_valid"])
            self.assertIsNone(invalid["prose_tokens"])
            self.assertEqual(invalid["feedback"]["code"], "message_schema")
            self.assertEqual(invalid["candidate"]["status"], "invalid")
            self.assertEqual(invalid["messages"], [])
            self.assertIn('\\ud800', invalid["generated"]["text"])
            self.assertTrue(all(d["sender"] != 2 for d in row["committed"]["pending"]))
            self.assertTrue(all(d["sender"] != 2 for d in row["committed"]["deliveries"]
                                if d["generated"] == {"phase": "recovery", "round_number": 1}))

    def test_archive_reproduces_exact_requests_tokens_replies_committed_queues_and_counts(self):
        self.assertEqual(self.current["cases"], self.expected["cases"])
        for field in ("tokenizer", "revision"):
            self.assertEqual(self.current["provenance"][field], self.expected["provenance"][field])
        for case in self.current["cases"]:
            for row in case["rounds"]:
                if case["traffic"] == "source_only":
                    self.assertEqual(row["held_prose_counts"], [0] * 4)
                for comparison in row["parent_comparisons"]:
                    self.assertTrue(all(comparison["equal"].values()))
                state = deserialize_state(json.dumps(row["committed"]).encode())
                self.assertEqual(json.loads(snapshot_bytes(state)), row["committed"])
                self.assertEqual(list(held_prose_counts(state)), row["held_prose_counts"])
                for request, outcome in zip(row["requests"], row["replies"]):
                    self.assertLessEqual(len(request["tokenized"]["input_ids"]) + 384, MAX_CONTEXT_TOKENS)
                    if outcome["generated"] is not None:
                        generated = outcome["generated"]
                        self.assertLessEqual(len(generated["token_ids"]), 384)
                        self.assertEqual(self.tokenizer.decode(generated["token_ids"], skip_special_tokens=False,
                            clean_up_tokenization_spaces=False), generated["text"])

    def test_native_q_round_two_source_metadata_and_own_reply_equality_then_round_three_release(self):
        for case in self.current["cases"]:
            if case["traffic"] == "source_only":
                continue  # Inactive first-round joins/counts are checked separately.
            rows = {(row["branch_id"], row["slot"]["round_number"]): row for row in case["rounds"]}
            for row in case["rounds"]:
                if "/Q_" not in row["branch_id"] or row["slot"]["round_number"] != 1:
                    continue
                parent_id = row["calls"][0]["replay_parent"].rsplit("/r", 1)[0]
                parent = rows[(parent_id, 1)]
                for p, (a, b) in enumerate(zip(row["committed"]["peers"], parent["committed"]["peers"])):
                    for key in ("sources", "source_deliveries", "candidate", "feedback"):
                        self.assertEqual(a[key], b[key])
                    self.assertEqual(a["history"], [e for e in b["history"] if not (
                        "sender" in e and e["slot"] == {"phase": "recovery", "round_number": 1})])
                    text = rows[(row["branch_id"], 2)]["requests"][p]["tokenized"]["text"]
                    for sender in (0, 1):
                        if sender != p:
                            self.assertNotIn(f"UNSEEN_{sender}_", text)
                held = row["committed"]["pending"]
                self.assertEqual(len(held), 4)
                released = rows[(row["branch_id"], 2)]["committed"]
                self.assertEqual(released["pending"], [])
                ids = {d["delivery_id"] for d in held}
                self.assertEqual([d["delivery_id"] for d in released["deliveries"] if d["delivery_id"] in ids],
                                 [d["delivery_id"] for d in sorted(held, key=lambda d: (d["sender"], d["recipient"]))])
                for d in released["deliveries"]:
                    if d["delivery_id"] in ids:
                        self.assertEqual(d["first_usable"], {"phase": "recovery", "round_number": 3})
                final = rows[(row["branch_id"], 4)]["committed"]
                self.assertFalse(final["pending"])
                self.assertIsNone(deserialize_state(json.dumps(final).encode()).next_slot)
                self.assertEqual(len([d for d in final["deliveries"] if d["delivery_id"] in ids]), 4)

    def test_every_archive_replay_joins_one_exact_record_with_no_duplicate_call_ids(self):
        rows = [row for case in self.current["cases"] for row in case["rounds"]]
        by_call = {}
        for row in rows:
            for p, call in enumerate(row["calls"]):
                self.assertNotIn(call["call_id"], by_call)
                by_call[call["call_id"]] = (row, p)
        for row in rows:
            for p, call in enumerate(row["calls"]):
                if call["replay_parent"] is None:
                    continue
                self.assertIn(call["replay_parent"], by_call)
                parent, i = by_call[call["replay_parent"]]
                self.assertIsNone(parent["calls"][i]["replay_parent"])
                self.assertEqual(call["seed"], parent["calls"][i]["seed"])
                self.assertEqual(row["settings_json"], parent["settings_json"])
                self.assertEqual(row["requests"][p], parent["requests"][i])
                self.assertEqual(row["replies"][p], parent["replies"][i])

    def test_native_both_masks_all_families_sizes_events_and_repeat_scoping(self):
        for size in Size:
            for task in Task:
                world = case_world(task, size)
                prefix = build_prefix(world, self.tokenizer)
                for event in ("revision", "sham"):
                    for replicate in (0, 1):
                        parents = parent_records(world, prefix, self.tokenizer, event, replicate)
                        for policy in ("P_G", "P_H"):
                            saved = replay_start(world, prefix, parents, policy, event, replicate, self.tokenizer)
                            group = world.partition[0 if policy == "P_G" else 1]
                            for p, call in enumerate(saved.calls):
                                parent = parents[1 if p in group else 0]
                                self.assertEqual(call.replay_parent, parent.calls[p].call_id)
                                self.assertEqual(saved.barrier.requests.tokenized[p], parent.barrier.requests.tokenized[p])
                                self.assertEqual(saved.barrier.replies[p], parent.barrier.replies[p])
                            self.assertEqual(tuple(r.candidate.status for r in saved.barrier.replies),
                                             ("valid", "valid", "invalid", "failed"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True, help="local pinned metadata only")
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path, help="exclusively create a new replay archive")
    args = parser.parse_args()
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    current = json.loads(json.dumps(replay_archive(tokenizer)))
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            output.write((json.dumps(current, ensure_ascii=True, sort_keys=True,
                                     separators=(",", ":")) + "\n").encode("utf-8"))
    TokenizerReplayTests.tokenizer = tokenizer
    TokenizerReplayTests.current = current
    TokenizerReplayTests.expected = json.loads((args.write_fixture or args.fixture).read_bytes())
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TokenizerReplayTests))
    rows = [row for case in current["cases"] for row in case["rounds"]]
    inputs = [len(request["tokenized"]["input_ids"]) for row in rows for request in row["requests"]]
    outputs = [len(reply["generated"]["token_ids"]) for row in rows for reply in row["replies"] if reply["generated"]]
    print(f"Replay archive: {len(rows)} rounds, {len(inputs)} requests, "
          f"{sum(len(row['parent_comparisons']) for row in rows)} exact parent comparisons; "
          f"input={min(inputs)}-{max(inputs)}, output={min(outputs)}-{max(outputs)} tokens; output reserve=384.")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
