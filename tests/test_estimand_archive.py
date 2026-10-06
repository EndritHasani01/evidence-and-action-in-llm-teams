"""Retained complete and incomplete ordinary-worker analysis acceptance."""

import gzip
import json
import unittest

from tests.estimand_archive import FIXTURE, reconstruct


class EstimandArchiveTests(unittest.TestCase):
    def test_all_tables_reproduce_without_redefining_fixed_populations(self):
        actual = reconstruct()
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as source:
            self.assertEqual(actual, json.load(source))
        for size, count, unknown in (("target", 60, 15486), ("fallback", 40, 10390)):
            case = actual["cases"][f"full-main-{size}-{count}"]
            self.assertEqual(case["coverage"]["unknown"], unknown)
            primary = [r for r in case["summaries"] if r["primary"] and r["level"] == "all_families"]
            self.assertEqual(len(primary), 2)
            for row in primary:
                self.assertIsNone(row["value"])
                self.assertEqual(row["scheduled_worlds"], count)
                self.assertEqual(row["observed_worlds"], 5)
                self.assertEqual(set(row["family_denominators"].values()), {count // 5})
                self.assertEqual(row["complete_case_description"]["value"], 0)
            cohorts = {r["population"]: r for r in case["populations"]}
            self.assertEqual(len(cohorts["preserving"]["world_ids"]), 16)
            self.assertEqual(len(cohorts["repeat"]["world_ids"]), 10)
            self.assertEqual(len(case["trajectory_changes"]), 100)
            self.assertEqual(len(case["prose_activity"]), 4 * (2 * count // 5))
            self.assertEqual(sum(r["observed"] for r in case["prose_activity"]), 8)
            self.assertTrue(all(r["population"] == "main" and r["replicate"] == 1 for r in case["repeat_contrasts"]))
            self.assertTrue(all(r["replicate"] == 0 for r in case["world_contrasts"]))


if __name__ == "__main__":
    unittest.main()
