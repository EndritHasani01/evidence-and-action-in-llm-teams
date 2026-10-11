"""Native course local witness with exact requests/parents and output width proof."""

import argparse
from dataclasses import asdict
import gzip
import json
from pathlib import Path
import unittest

from recovery.prompts import COURSE_LIMITS, rendered_data
from recovery.tasks import PEERS
from recovery.witness import local_candidate
from tests.course_attainability_checks import CourseAttainabilityTests
from tests.course_intervention_cases import branches
from tests.tokenizer_attainability import output_shapes
from tests.tokenizer_course_capacity import canonical, environment, metadata_support
from tests.tokenizer_replay import round_record

FIXTURE = Path(__file__).resolve().parent / "fixtures/course_attainability.json.gz"


def archive():
    cases, shapes = [], []
    tokenizer = CourseAttainabilityTests.tokenizer
    for world, prefix, continuations, controls in CourseAttainabilityTests.cases:
        parents = tuple(saved for b, rounds, _ in continuations if b.policy in ("B", "C") for saved in rounds[:1])
        rows = [round_record(saved, parents) for _, rounds, _ in continuations for saved in rounds]
        prefix_branch = next(b for b in branches(world) if b.phase == "prefix")
        shape_rows = output_shapes(tokenizer, sizes=(world.world.size,), tasks=(world.world.task,),
            limits=COURSE_LIMITS, world_for=lambda *_: world)
        shapes += [dict(world_id=world.world_id, **r) for r in shape_rows]
        cases.append(dict(world_id=world.world_id, development=world.development, task=world.world.task.value,
            prefix_snapshot=json.loads(prefix.snapshot), prefix_calls=[asdict(c) for c in prefix_branch.calls],
            prefix_rounds=[asdict(r) for r in prefix.rounds], rounds=rows,
            controls=[dict(call=asdict(b.calls[0]), view=asdict(view), tokenized=asdict(encoded), outcome=asdict(reply))
                      for b, view, encoded, reply in controls]))
    return canonical(dict(model=CourseAttainabilityTests.settings["model"], revision=CourseAttainabilityTests.settings["revision"],
        scope="Locally informed scripted course strategy; no model competence or GPU result",
        limits=asdict(COURSE_LIMITS), settings=CourseAttainabilityTests.settings, output_shapes=shapes, cases=cases))


class NativeCourseWitnessTests(unittest.TestCase):
    current = expected = tokenizer = None

    def test_exact_raw_local_requests_replies_settings_parents_and_states_reproduce(self):
        for current, expected in zip(self.current["cases"], self.expected["cases"]):
            self.assertEqual(current, expected, current["world_id"])
        self.assertEqual({k: v for k, v in self.current.items() if k != "cases"},
                         {k: v for k, v in self.expected.items() if k != "cases"})
        self.assertEqual(len(self.current["cases"]), len(self.expected["cases"]))

    def test_all_correct_width_candidate_control_and_useful_shard_shapes_fit_without_padding(self):
        self.assertEqual(len(self.current["output_shapes"]), 225)
        for row in self.current["output_shapes"]:
            self.assertTrue(row["protocol_valid"])
            self.assertLessEqual(row["output_tokens"], row["correct_value_token_upper"])
            self.assertLessEqual(row["correct_value_token_upper"], 256)
            self.assertLessEqual(row["prose_tokens"], 64)
            self.assertEqual(self.tokenizer.decode(row["token_ids"], skip_special_tokens=False,
                clean_up_tokenization_spaces=False), row["text"])

    def test_native_calls_stay_scalar_and_lossless_with_local_evidence_and_exact_replay(self):
        outcomes = {}
        for _, prefix, continuations, controls in CourseAttainabilityTests.cases:
            barriers = [r.barrier for r in prefix.rounds]
            barriers += [saved.barrier for _, rounds, _ in continuations for saved in rounds]
            for barrier in barriers:
                for p in PEERS:
                    request, raw = barrier.requests, barrier.replies[p].generated
                    self.assertEqual(self.tokenizer.decode(raw.token_ids, skip_special_tokens=False,
                        clean_up_tokenization_spaces=False), raw.text)
                    self.assertLessEqual(len(raw.token_ids), 256)
                    self.assertLessEqual(request.tokenized[p].input_tokens+256, COURSE_LIMITS.context_tokens)
                    if request.slot.round_number == 4:
                        self.assertEqual(local_candidate(request.views[p]), json.loads(raw.text)["candidate"])
                    self.assertEqual([h["text"] for h in rendered_data(request.rendered[p])["history"]
                                      if "text" in h],
                                     [h.text for h in request.views[p].history if hasattr(h, "text")])
            for branch, rounds, _ in continuations:
                for saved in rounds:
                    for call, outcome in zip(saved.calls, saved.barrier.replies):
                        if call.replay_parent:
                            self.assertEqual(outcome, outcomes[call.replay_parent])
                        outcomes[call.call_id] = outcome
            for _, view, encoded, outcome in controls:
                self.assertEqual(local_candidate(view), json.loads(outcome.generated.text)["candidate"])
                self.assertLessEqual(encoded.input_tokens+256, COURSE_LIMITS.context_tokens)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", required=True, type=Path)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    parser.add_argument("--environment", type=Path)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    metadata_support(args.tokenizer, tokenizer)
    CourseAttainabilityTests.tokenizer = tokenizer
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CourseAttainabilityTests))
    if not result.wasSuccessful():
        return 1
    current = archive()
    expected = current if args.write_fixture else json.loads(gzip.decompress(args.fixture.read_bytes()))
    NativeCourseWitnessTests.current, NativeCourseWitnessTests.expected, NativeCourseWitnessTests.tokenizer = current, expected, tokenizer
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeCourseWitnessTests))
    if not result.wasSuccessful():
        return 1
    if args.write_fixture:
        with args.write_fixture.open("xb") as output:
            output.write(gzip.compress((json.dumps(current, ensure_ascii=True, sort_keys=True, separators=(",", ":"))+"\n").encode(), mtime=0))
    if args.environment:
        with args.environment.open("x", encoding="utf-8", newline="\n") as output:
            json.dump(environment(args.tokenizer, tokenizer), output, indent=2)
            output.write("\n")
    rows = [r for c in current["cases"] for r in c["rounds"]]
    print(json.dumps(dict(worlds=len(current["cases"]), prefix_rounds=sum(len(c["prefix_rounds"]) for c in current["cases"]),
        continuation_rounds=len(rows), parent_comparisons=sum(len(r["parent_comparisons"]) for r in rows),
        largest_shape_output=max(r["output_tokens"] for r in current["output_shapes"]),
        correct_value_output_upper=max(r["correct_value_token_upper"] for r in current["output_shapes"]),
        model_calls=0)), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
