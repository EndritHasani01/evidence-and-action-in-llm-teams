"""Pinned 4B CPU/native course intervention traces; never loads model weights."""

import argparse
from dataclasses import asdict
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import unittest

from recovery.prompts import COURSE_LIMITS
from recovery.replay import commit_continuation_round, obtain_continuation_round
from recovery.rounds import deserialize_state, snapshot_bytes
from tests.course_intervention_cases import branches, course_inputs
from tests.course_intervention_checks import CourseInterventionTests
from tests.replay_checks import replay_provider
from tests.tokenizer_replay import round_record

FIXTURE = Path(__file__).resolve().parent / "fixtures/course_interventions.json.gz"


def canonical(value):
    return json.loads(json.dumps(value, ensure_ascii=True))


def archive():
    cases = []
    for world, prefix, records in CourseInterventionTests.cases:
        parents = tuple(s for s in records.values() if s.branch.policy in ("B", "C"))
        rounds = []
        for saved in records.values():
            rounds.append(round_record(saved, parents))
            if saved.branch.policy in ("Q_B", "Q_C") or (
                    not world.development and world.index == 1 and saved.branch.policy in ("K", "K_delta")):
                state = commit_continuation_round(saved).committed
                for _ in range(3):
                    current = obtain_continuation_round(state, saved.branch, CourseInterventionTests.tokenizer,
                        replay_provider(CourseInterventionTests.tokenizer), settings=CourseInterventionTests.settings)
                    rounds.append(round_record(current))
                    state = commit_continuation_round(current).committed
        branch = next(b for b in branches(world) if b.phase == "prefix")
        cases.append(dict(world_id=world.world_id, development=world.development,
            prefix_snapshot=json.loads(prefix.snapshot), prefix_calls=[asdict(c) for c in branch.calls],
            prefix_rounds=[asdict(r) for r in prefix.rounds], rounds=rounds))
    return canonical(dict(model="Qwen/Qwen3.5-4B", revision="851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a",
        scope="Scripted course interventions/replay; no model, capacity proof or empirical result",
        limits=asdict(COURSE_LIMITS), settings=CourseInterventionTests.settings, cases=cases))


class NativeArchiveTests(unittest.TestCase):
    current = expected = tokenizer = None

    def test_archive_reproduces_literal_prefixes_boundaries_parents_tokens_and_queues(self):
        self.assertEqual({k: v for k, v in self.current.items() if k != "cases"},
                         {k: v for k, v in self.expected.items() if k != "cases"})
        self.assertEqual([c["world_id"] for c in self.current["cases"]], [c["world_id"] for c in self.expected["cases"]])
        for actual, expected in zip(self.current["cases"], self.expected["cases"]):
            self.assertEqual(actual["prefix_snapshot"], expected["prefix_snapshot"], actual["world_id"])
            self.assertEqual(actual["prefix_calls"], expected["prefix_calls"])
            self.assertEqual(actual["prefix_rounds"], expected["prefix_rounds"], actual["world_id"])
            self.assertEqual(len(actual["rounds"]), len(expected["rounds"]))
            for a, b in zip(actual["rounds"], expected["rounds"]):
                self.assertEqual(a, b, (a["branch_id"], a["slot"]))

    def test_all_course_starts_and_prescribed_parent_joins_are_present_and_exact(self):
        _, schedules = course_inputs()
        expected = {b.branch_id for b in schedules.main + schedules.development if b.phase == "continuation"}
        starts = {r["branch_id"] for c in self.current["cases"] for r in c["rounds"] if r["slot"]["round_number"] == 1}
        self.assertEqual(starts, expected)
        outcomes = {}
        comparisons = []
        for case in self.current["cases"]:
            for row in case["rounds"]:
                self.assertEqual(json.loads(row["settings_json"]), self.current["settings"])
                for call, outcome in zip(row["calls"], row["replies"]):
                    self.assertNotIn(call["call_id"], outcomes)
                    outcomes[call["call_id"]] = outcome
                comparisons.extend(row["parent_comparisons"])
        self.assertEqual({c["call_id"] for c in comparisons},
                         {c.call_id for b in schedules.main + schedules.development for c in b.calls if c.replay_parent})
        for comparison in comparisons:
            self.assertTrue(all(comparison["equal"].values()), comparison)
            self.assertEqual(outcomes[comparison["call_id"]], outcomes[comparison["parent"]])

    def test_native_counts_and_roundtrip_metadata_cover_receipts_exposure_and_source_prose_timing(self):
        for case in self.current["cases"]:
            state = deserialize_state(json.dumps(case["prefix_snapshot"]).encode())
            self.assertEqual(json.loads(snapshot_bytes(state)), case["prefix_snapshot"])
            rows = [(r["barrier"]["requests"], r["barrier"]["replies"]) for r in case["prefix_rounds"]]
            rows += [(r, r["replies"]) for r in case["rounds"]]
            for row, replies in rows:
                requests = row.get("requests")
                if requests is None:
                    requests = [dict(view=v, rendered=r, tokenized=t) for v, r, t in zip(row["views"], row["rendered"], row["tokenized"])]
                for request, outcome in zip(requests, replies):
                    self.assertLessEqual(len(request["tokenized"]["input_ids"]) + 256, COURSE_LIMITS.context_tokens)
                    self.assertEqual(len(request["tokenized"]["input_ids"]), len(request["tokenized"]["attention_mask"]))
                    if outcome["generated"] is not None:
                        raw = outcome["generated"]
                        self.assertLessEqual(len(raw["token_ids"]), 256)
                        self.assertEqual(self.tokenizer.decode(raw["token_ids"], skip_special_tokens=False,
                            clean_up_tokenization_spaces=False), raw["text"])
                    if outcome["prose_tokens"] is not None:
                        self.assertLessEqual(outcome["prose_tokens"], 64)
            for row in case["rounds"]:
                state = deserialize_state(json.dumps(row["committed"]).encode())
                self.assertEqual(json.loads(snapshot_bytes(state)), row["committed"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", required=True, type=Path)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    parser.add_argument("--environment", type=Path)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    CourseInterventionTests.tokenizer = tokenizer
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CourseInterventionTests))
    if not result.wasSuccessful():
        return 1
    current = archive()
    expected = current if args.write_fixture else json.loads(gzip.decompress(args.fixture.read_bytes()))
    NativeArchiveTests.current, NativeArchiveTests.expected, NativeArchiveTests.tokenizer = current, expected, tokenizer
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeArchiveTests))
    if not result.wasSuccessful():
        return 1
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            output.write(gzip.compress((json.dumps(current, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode(), mtime=0))
    environment = dict(python=sys.version.split()[0], tokenizer_directory=str(args.tokenizer),
        model=current["model"], revision=current["revision"],
        packages={name: importlib.metadata.version(name) for name in ("pydantic", "transformers", "tokenizers", "jinja2", "huggingface-hub")},
        files={p.name: dict(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in args.tokenizer.iterdir() if p.is_file()},
        model_weights_loaded=False)
    if args.environment:
        with args.environment.open("x", encoding="utf-8", newline="\n") as output:
            json.dump(environment, output, indent=2)
            output.write("\n")
    rounds = [r for c in current["cases"] for r in c["rounds"]]
    print(json.dumps(dict(worlds=len(current["cases"]), prefix_rounds=sum(len(c["prefix_rounds"]) for c in current["cases"]),
        continuation_starts=sum(r["slot"]["round_number"] == 1 for r in rounds), retained_continuation_rounds=len(rounds),
        parent_comparisons=sum(len(r["parent_comparisons"]) for r in rounds),
        largest_retained_input=max(len(t["tokenized"]["input_ids"]) for r in rounds for t in r["requests"]),
        largest_retained_output=max(len(o["generated"]["token_ids"]) for r in rounds for o in r["replies"] if o["generated"]),
        complete_context_capacity="unaccepted", model_calls=0)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
