"""Reproduction and independent acceptance counts for the ordinary M3 bundle."""

import gzip
import importlib.util
import json
import unittest


@unittest.skipUnless(importlib.util.find_spec("langgraph"), "ordinary checkpoint decoder needs declared CPU packages")
class UncertaintyArchiveTests(unittest.TestCase):
    def test_all_sixteen_original_worker_cases_reproduce_uncertainty_and_frozen_bounds(self):
        from tests.uncertainty_archive import FIXTURE, reconstruct
        actual = reconstruct()
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
            expected = json.load(source)
        self.assertEqual(actual.keys(), expected.keys())
        self.assertEqual(actual["cases"].keys(), expected["cases"].keys())
        for name, case in actual["cases"].items():
            for key, value in case.items():
                self.assertTrue(value == expected["cases"][name][key], name+"/"+key)
        for size, count, n, unknown in (("target", 60, 12, 15486), ("fallback", 40, 8, 10390)):
            full = actual["cases"][f"full-main-{size}-{count}"]
            self.assertEqual(full["coverage"]["scheduled"], 2170+unknown)
            self.assertEqual(full["coverage"]["unknown"], unknown)
            primaries = [r for r in full["summaries"] if r["primary_interval"]]
            self.assertEqual(len(primaries), 2)
            for row in primaries:
                self.assertEqual(row["eligible_worlds"], count)
                self.assertEqual(list(row["family_denominators"].values()), [n]*5)
                self.assertIsNone(row["intended_population"]["interval"])
                self.assertEqual(row["complete_case_description"]["independent_worlds"], 5)
            self.assertEqual(len(full["populations"][-1]["world_ids"]), 10)
            self.assertTrue(any(not r["execution_observed"] for r in full["world_bounds"]))
            shared_first = [r for r in full["world_bounds"] if r["endpoint"] == "accuracy" and r["round"] == 1
                            and r["estimand"] in ("Q_B-B", "Q_C-C", "E_keep", "E_clear")]
            self.assertTrue(shared_first)
            self.assertTrue(any(not r["execution_observed"] for r in shared_first))
            self.assertTrue(all(r["sensitivity"]["interval"] == [0, 0] for r in shared_first))
            self.assertTrue(any(r["metric"] == "policy_seconds" and r["sensitivity"]["interval"]
                                and r["sensitivity"]["interval"][1] is None for r in full["policy_display_summaries"]))
        for name, case in actual["cases"].items():
            self.assertEqual(case["settings"]["draws"], 10_000)
            if name.endswith("/stopped"):
                self.assertEqual(case["coverage"]["unknown"], 16)
                self.assertTrue(all(r["observed"]["category"] == "incomplete" for r in case["world_trajectories"]))
                self.assertTrue(all(r["exact_binomial"] is None for r in case["family_completion"]))


if __name__ == "__main__":
    unittest.main()
