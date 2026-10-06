"""Original-ledger reconciliation, repeated policies, full populations and stops."""

import gzip
import importlib.util
import json
import unittest


@unittest.skipUnless(importlib.util.find_spec("langgraph"), "saved checkpoint decoder needs declared CPU dependencies")
class CostArchiveTests(unittest.TestCase):
    def test_all_original_cases_reconcile_m3_and_reproduce_cost_rule_tables(self):
        from tests.cost_archive import FIXTURE, reconstruct
        actual = reconstruct()
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
            expected = json.load(source)
        self.assertEqual(actual.keys(), expected.keys())
        self.assertEqual(actual["cases"].keys(), expected["cases"].keys())
        for name, case in actual["cases"].items():
            self.assertEqual(case.keys(), expected["cases"][name].keys())
            for key, value in case.items():
                self.assertTrue(value == expected["cases"][name][key], name + "/" + key)
        complete = next(v for k, v in actual["cases"].items() if k.endswith("/target"))
        self.assertEqual(complete["physical"]["attempts"], 1978)
        self.assertEqual(len(complete["boundary_selections"]), 22)
        self.assertTrue(all(r["available"] for r in complete["boundary_selections"]))
        for name, count, unknown in (("full-main-target-60", 60, 15486), ("full-main-fallback-40", 40, 10390)):
            full = actual["cases"][name]
            self.assertEqual(full["coverage"]["unknown"], unknown)
            self.assertEqual(sum(r["frequency_denominator"] for r in full["selection_frequencies"]
                                 if r["level"] == "pooled" and r["event"] == "revision" and r["replicate"] == 0), count)
            self.assertTrue(any(not r["available"] for r in full["boundary_selections"]))
        stopped = next(v for k, v in actual["cases"].items() if k.endswith("/stopped"))
        self.assertEqual(stopped["coverage"]["unknown"], 16)
        self.assertEqual(stopped["physical"]["attempts"], 1)
        self.assertEqual(stopped["physical"]["uncertain_attempts"], 1)
        self.assertTrue(all(r["complete_policy_seconds"] is None for r in stopped["policy_costs"]))


if __name__ == "__main__":
    unittest.main()
