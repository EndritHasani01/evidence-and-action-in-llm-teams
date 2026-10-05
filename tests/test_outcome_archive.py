"""Offline reconstruction of retained complete, interrupted and stopped M3 inputs."""

import gzip
import json
import unittest

from tests.outcome_archive import FIXTURE, reconstruct


class OutcomeArchiveTests(unittest.TestCase):
    def test_every_table_reproduces_and_full_manifests_retain_unknown_worlds(self):
        actual = reconstruct()
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
            expected = json.load(source)
        self.assertEqual(actual, expected)
        cases = actual["cases"]
        self.assertEqual(len(cases), 16)
        complete = [case for name, case in cases.items() if name.startswith("test_every_family_")]
        self.assertEqual(sum(c["coverage"]["scheduled"] for c in complete), 4340)
        self.assertEqual(sum(len(c["attempts"]) for c in complete), 3956)
        replays = [r for c in complete for r in c["outcomes"] if r["replay_parent"]]
        self.assertEqual(len(replays), 384)
        self.assertTrue(all(r["generation_id"] == r["replay_parent"] and r["attempt_numbers"] == [1] for r in replays))
        for size, count, scheduled in (("target", 60, 17656), ("fallback", 40, 12560)):
            case = cases[f"full-main-{size}-{count}"]
            self.assertEqual(case["coverage"]["scheduled"], scheduled)
            self.assertEqual(case["coverage"]["unknown"], scheduled - 2170)
            self.assertEqual(len({r["world_id"] for r in case["outcomes"]}), count)
            self.assertTrue(all(r["correct"] == 0 for r in case["outcomes"]
                                if r["protocol_outcome"] in ("invalid", "failed")))
            self.assertTrue(all(r["correct"] is None for r in case["outcomes"] if r["protocol_outcome"] == "unknown"))
        stopped = next(c for name, c in cases.items() if name.endswith("/stopped"))
        self.assertEqual(stopped["coverage"]["unknown"], 16)
        self.assertEqual(stopped["coverage"]["recorded"], 0)
        self.assertEqual(stopped["trajectories"][0]["category"], "incomplete")
        self.assertEqual(sum(a["uncertain_completion"] for a in stopped["attempts"]), 1)


if __name__ == "__main__":
    unittest.main()
