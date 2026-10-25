"""Thesis worlds: generator contract, committed manifest and input separation (spec 3.3)."""
import json
from pathlib import Path
import unittest

from recovery.thesis import CELLS, load_config
from recovery.thesis.worlds import (build_manifest, check_world, load_manifest, make_world, manifest_bytes,
                                    stratum, verify_manifest, verify_separation)

ROOT = Path(__file__).parents[1]


class Worlds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(ROOT)
        cls.manifest, cls.sha = load_manifest(ROOT)
        cls.worlds = cls.manifest["worlds"]

    def test_committed_manifest_regenerates_byte_for_byte(self):
        receipt = verify_manifest(ROOT, self.config)
        self.assertEqual(receipt["sha256"], self.sha)
        self.assertEqual(receipt["worlds"], 80)
        self.assertEqual(receipt["strata"], dict(development=[2] * 8, main=[8] * 8))

    def test_main_is_the_first_64_indices_eight_per_stratum(self):
        main = [w for w in self.worlds if w["group"] == "main"]
        self.assertEqual([w["id"] for w in main], [f"main-{i:03d}" for i in range(64)])
        self.assertEqual([sum(w["stratum"] == s for w in main) for s in range(8)], [8] * 8)
        # World content depends only on the master seed and the identifier, so these 64 are the
        # same worlds that indices 0-63 of the earlier 192-world manifest contained.
        self.assertEqual(main[5], make_world(self.config["master_seed"], "main", 5))

    def test_strata_mapping(self):
        self.assertEqual(stratum(0), dict(stratum=0, edit="demote", owner=0, first=0))
        self.assertEqual(stratum(5), dict(stratum=5, edit="keep", owner=0, first=1))
        self.assertEqual(stratum(14), dict(stratum=6, edit="keep", owner=1, first=0))
        main = [w for w in self.worlds if w["group"] == "main"]
        self.assertEqual([w["id"] for w in main[:3]], ["main-000", "main-001", "main-002"])

    def test_every_world_meets_the_mathematical_contract(self):
        for world in self.worlds:
            self.assertTrue(check_world(world))
            values = world["original"][0] + world["original"][1]
            m1, m2 = sorted(values, reverse=True)[:2]
            if world["edit"] == "demote":
                self.assertLess(world["after"], m2)
                self.assertEqual(world["revised_truth"], m2)
            else:
                self.assertGreater(world["after"], m2)
                self.assertNotEqual(world["after"], m1)
                self.assertEqual(world["revised_truth"], world["after"])
            self.assertEqual(world["holders_original"], [world["owner"]])
            self.assertEqual(sorted(world["order"]), sorted(CELLS))

    def test_answer_preserving_change_keeps_answer_and_local_maxima(self):
        for world in self.worlds:
            owner, row, p_row = world["owner"], world["row"], world["preserving_row"]
            original, preserving = world["original"], world["preserving"]
            changed = [(a, j) for a in (0, 1) for j in range(20) if original[a][j] != preserving[a][j]]
            self.assertEqual(changed, [(owner, p_row)])  # same owner as the revision, one record
            self.assertNotEqual(p_row, row)  # never the winning record
            self.assertEqual(world["preserving_before"], original[owner][p_row])
            self.assertEqual(preserving[owner][p_row], world["preserving_after"])
            self.assertLess(world["preserving_after"], world["original_truth"])
            self.assertEqual(max(preserving[0] + preserving[1]), world["original_truth"])
            self.assertEqual([max(s) for s in preserving], [max(s) for s in original])
        broken = json.loads(json.dumps(self.worlds[0]))
        broken["preserving"][broken["owner"]][broken["row"]] = -1000
        with self.assertRaises(ValueError):
            check_world(broken)

    def test_generation_depends_only_on_seed_and_identity(self):
        a = make_world(self.config["master_seed"], "main", 7)
        b = make_world(self.config["master_seed"], "main", 7)
        self.assertEqual(a, b)
        self.assertNotEqual(a["original"], make_world(self.config["master_seed"] + 1, "main", 7)["original"])
        self.assertEqual(manifest_bytes(build_manifest(self.config)), (ROOT / "configs/thesis-worlds.json").read_bytes())

    def test_seeds_are_exact_integers_and_shared_across_continuation_cells(self):
        raw = (ROOT / "configs/thesis-worlds.json").read_text()
        world = self.worlds[0]
        for model in ("qwen", "granite"):
            seeds = world["seeds"][model]
            for value in [s for row in seeds["prefix"] + seeds["continuation"] for s in row] + list(seeds["control"].values()):
                self.assertIs(type(value), int)
                self.assertTrue(0 <= value < 2**63)
                self.assertIn(str(value), raw)
        self.assertNotEqual(world["seeds"]["qwen"]["prefix"], world["seeds"]["granite"]["prefix"])

    def test_separation_receipt_matches_a_fresh_audit(self):
        receipt = verify_separation(ROOT)
        self.assertTrue(receipt["passed"])
        self.assertEqual(receipt["checked_new_inputs"], 240)  # original, revised and preserving inputs of 80 worlds
        self.assertGreaterEqual(receipt["distinct_exposed_inputs"], 114)

    def test_config_ceilings_must_match_the_six_cells(self):
        import tempfile
        self.assertEqual((self.config["ceilings"]["main_per_model_per_world"], self.config["ceilings"]["development"]),
                         (44, 1408))  # 6 prefix + 6 x 6 continuation + 2 controls; 16 worlds x 44 x 2 models
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "configs").mkdir()
            stale = json.loads((ROOT / "configs/thesis.json").read_text())
            stale["ceilings"]["main_per_model_per_world"] = 32  # the pre-amendment four-cell value
            (root / "configs/thesis.json").write_text(json.dumps(stale))
            with self.assertRaises(ValueError):
                load_config(root)

    def test_tampered_manifest_is_refused(self):
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for rel in ("configs/thesis.json", "configs/thesis-worlds.json"):
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, root / rel)
            data = json.loads((root / "configs/thesis-worlds.json").read_text())
            data["worlds"][0]["after"] += 1
            (root / "configs/thesis-worlds.json").write_bytes(manifest_bytes(data))
            with self.assertRaises(ValueError):
                verify_manifest(root, self.config)


if __name__ == "__main__":
    unittest.main()
