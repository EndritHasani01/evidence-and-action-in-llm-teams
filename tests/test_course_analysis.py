"""Independent course formulas/cohorts and literal offline record failure cases."""

import copy
from dataclasses import asdict
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recovery.analysis import analyze_estimands, analyze_run, population_table
from recovery.evaluate import evaluate_records, evaluate_run
from recovery.prompts import COURSE_LIMITS
from recovery.tasks import Task
from tests.estimand_fixture import constant, correct_rounds, group_matrix, prepared, selection, tables, zeros
from tests.outcome_fixture import ROOT, encode, saved_records, write_worker
from tests.test_analysis import find


def course_selection(task=None, index=3, *, worlds=None):
    return selection(task, index, size="course", worlds=worlds)


def formula_case(matrices, task=Task.DIFFERENCE, index=3, *, uniform_preservation=False):
    worlds, branches = course_selection(task, index)
    mapping = {(worlds[0].world_id, *key): value for key, value in matrices.items()}
    data = tables(worlds, branches, mapping)
    if uniform_preservation:
        # Explicit abstract eligibility: one old-correct U coordinate per peer.
        # Actual event-specific coordinates are checked on original workers.
        for row in data["peer_diagnostics"]:
            row.update(denominator=1, numerator=row["correct"], rate=row["correct"],
                       eligible_coordinates=[0])
    return analyze_estimands(worlds, branches, data)


class CourseFormulaTests(unittest.TestCase):
    def test_saved_cohorts_and_streams_define_twenty_eight_and_five(self):
        population, schedules = prepared("course")
        cohorts = {r["population"]: r for r in population_table(population.main)}
        for name, count in (("main", 20), ("receipts", 8), ("prose_delay", 8), ("preserving", 8), ("repeat", 5)):
            self.assertEqual(len(cohorts[name]["world_ids"]), count)
            if name != "main":
                subset = {"receipts": "receipt", "prose_delay": "q"}.get(name, name)
                self.assertEqual(set(cohorts[name]["world_ids"]), set(population.subsets(20)[subset]))
        overlap = set(cohorts["receipts"]["world_ids"]) & set(cohorts["prose_delay"]["world_ids"])
        self.assertEqual(len(overlap), 4)
        self.assertTrue(all("distributed_sort" in name for name in overlap))
        repeated = {b.world_id for b in schedules.main if b.replicate == 1}
        self.assertEqual(set(cohorts["repeat"]["world_ids"]), repeated)
        for world in cohorts["repeat"]["worlds"]:
            self.assertEqual(world["index"], 1)
            a, b = world["continuation_seeds"]
            self.assertFalse(set(sum(a, [])) & set(sum(b, [])))
        self.assertFalse(next(p for p in population_table(population.development) if p["population"] == "repeat")["world_ids"])

    def test_complete_contract_rows_fixed_denominators_and_companion_endpoints(self):
        p, s = prepared("course")
        result = analyze_estimands(p.main, s.main, tables(p.main, s.main))
        # Contract arithmetic: 262 main rows/world; 112 receipt, 44 Q and
        # 42 preserving rows/eligible world. Repeated main matrix has 248.
        self.assertEqual(len(result["world_contrasts"]), 20 * 262 + 8 * (112 + 44 + 42))
        self.assertEqual(len(result["repeat_contrasts"]), 5 * 248)
        self.assertEqual(len(result["repeatability"]), 5 * 16)
        self.assertEqual(len(result["trajectory_changes"]), 5 * 10)
        self.assertEqual(sum(r["primary"] for r in result["world_contrasts"]), 40)
        signatures = [(r["world_id"], r["population"], r["estimand"], r["event"], r["endpoint"], r["round"])
                      for r in result["world_contrasts"]]
        self.assertEqual(len(signatures), len(set(signatures)))
        for row in result["summaries"]:
            if row["endpoint"] == "preservation":
                continue  # Actual empty U populations remain N/A, not accuracy exclusions.
            self.assertEqual(set(row["family_denominators"].values()), {4})
            expected = 4 if row["level"] == "family" else 20 if row["population"] == "main" else 8
            self.assertEqual(row["scheduled_worlds"], expected)
            self.assertEqual(row["observed_worlds"], expected)
            self.assertEqual(row["value"], 0)
        by_world = {w.world_id: w for w in p.main}
        for row in result["world_contrasts"]:
            if row["population"] != "main":
                subset = {"receipts": "receipt", "prose_delay": "q"}.get(row["population"], row["population"])
                self.assertIn(row["world_id"], p.subsets(20)[subset])
            for term in row["components"]:
                for atom in term["atoms"]:
                    self.assertEqual(atom["seed"], by_world[row["world_id"]].streams.continuation_seed(0, atom["round"], atom["peer"]))

    def test_theta_equal_revised_sham_null_and_both_signs(self):
        for sham, expected in ((constant([1, 1, 0, 0]), 0), (zeros(), .5), (constant([1] * 4), -.5)):
            result = formula_case({("revision", "B", 0): constant([1, 0, 0, 0]),
                ("revision", "C", 0): constant([1, 1, 1, 0]), ("sham", "C", 0): sham})
            self.assertEqual(find(result, "theta", "revision_minus_sham")["value"], expected)
            self.assertEqual(find(result, "C-B")["value"], .5)
            self.assertEqual(find(result, "C-B", "sham")["value"], .5 - expected)

    def test_focal_peer_null_benefit_harm_equal_event_effect_and_round_one(self):
        world = course_selection(Task.DIFFERENCE)[0][0]
        for baseline, retained, effect in ((0, 0, 0), (0, 1, 1), (1, 0, -1)):
            result = formula_case({(event, policy, 0): matrix for event in ("revision", "sham")
                for policy, matrix in (("B", constant([baseline] * 4)),
                    ("P_G", group_matrix(world, [0, 0], [retained] * 2)),
                    ("P_H", group_matrix(world, [retained] * 2, [0, 0])))})
            self.assertEqual(find(result, "E_keep", endpoint="collaborator_accuracy")["value"], effect)
            self.assertEqual(find(result, "E_keep", "sham", "collaborator_accuracy")["value"], effect)
            self.assertEqual(find(result, "phi_corr", "revision_minus_sham", "collaborator_accuracy")["value"], 0)
            phi = find(result, "E_keep", endpoint="collaborator_accuracy")
            for term, peers in zip(phi["components"], (world.partition[0],) * 2 + (world.partition[1],) * 2):
                self.assertEqual(term["peers"], list(peers))
                self.assertEqual(term["rounds"], [2, 3, 4])
                self.assertEqual(term["scheduled_calls"], 6)
            reference = find(result, "E_keep", endpoint="accuracy", number=1)
            self.assertEqual(reference["value"], 0)
            self.assertTrue(reference["construction_reference"])

    def test_cleared_peers_complementary_own_effects_and_masks(self):
        world = course_selection(Task.DIFFERENCE)[0][0]
        result = formula_case({("revision", policy, 0): group_matrix(world, G, H) for policy, G, H in (
            ("B", [1, 0], [1, 1]), ("P_G", [0, 0], [1, 0]),
            ("P_H", [1, 1], [0, 0]), ("C", [1, 0], [1, 0]))})
        for name, value in (("E_keep", 0), ("E_clear", .5),
                           ("own_reset_other_retained", -.75), ("own_reset_other_cleared", -.25)):
            self.assertEqual(find(result, name, endpoint="collaborator_accuracy")["value"], value)
        for group, values in (("G", (.5, 0, 1, .5)), ("H", (1, .5, 0, .5))):
            for mask, value in zip(("00", "10", "01", "11"), values):
                self.assertEqual(find(result, f"M_{group}_{mask}", endpoint="collaborator_accuracy")["value"], value)
        for number in (1, 2, 3, 4):
            cells = [find(result, "cell_" + policy, endpoint="accuracy", number=number)["value"] for policy in ("P_G", "P_H")]
            self.assertEqual(find(result, "mixed_mean", endpoint="accuracy", number=number)["value"], sum(cells) / 2)

    def test_retention_compact_delivery_evidence_and_preservation_companions(self):
        matrices = {("revision", policy, 0): correct_rounds(n) for policy, n in (("L", 0), ("B", 1), ("C", 2), ("K", 3), ("F", 4))}
        matrices.update({("sham", policy, 0): correct_rounds(n) for policy, n in (("B", 2), ("C", 1), ("K", 0))})
        result = formula_case(matrices)
        for name, auc, final in (("C-B", .25, 0), ("K-C", .25, 0), ("K-B", .5, 0), ("B-L", .25, 0), ("C-F", -.5, -1)):
            for endpoint in ("auc", "preservation"):
                self.assertEqual(find(result, name, endpoint=endpoint)["value"], auc)
            self.assertEqual(find(result, name, endpoint="final_joint")["value"], final)
            self.assertEqual(find(result, name, endpoint="preservation", number=4)["value"], final)
            self.assertEqual(find(result, name)["components"][0]["scheduled_calls"], 16)
        for name, sham, correction in (("K-C", -.25, .5), ("K-B", -.5, 1)):
            self.assertEqual(find(result, name, "sham")["value"], sham)
            self.assertEqual(find(result, name + "_corr", "revision_minus_sham")["value"], correction)

    def test_all_receipt_cells_effects_and_companions_with_equal_benefit_null(self):
        for task in (Task.PREFIX, Task.SORT):
            result = formula_case({("revision", p, 0): constant(v) for p, v in (
                ("B", [1, 0, 0, 0]), ("C", [1, 1, 0, 0]), ("K", [1, 1, 1, 0]),
                ("B_delta", [1, 1, 0, 0]), ("C_delta", [1, 0, 0, 0]), ("K_delta", [1] * 4))},
                task, uniform_preservation=True)
            for p, value in (("B", .25), ("C", .5), ("K", .75), ("B_delta", .5), ("C_delta", .25), ("K_delta", 1)):
                self.assertEqual(find(result, "receipt_cell_" + p, endpoint="accuracy", number=1)["value"], value)
            for name, value in (("eta", .5), ("B_delta-B", .25), ("C_delta-C", -.25), ("K_delta-K", .25),
                                ("B-C", -.25), ("B-K", -.5), ("B_delta-C_delta", .25), ("B_delta-K_delta", -.5)):
                for endpoint, number in (("accuracy", 1), ("auc", None), ("preservation", None), *(("preservation", r) for r in (1, 2, 3, 4))):
                    self.assertEqual(find(result, name, endpoint=endpoint, number=number)["value"], value)
            self.assertEqual(find(result, "eta", endpoint="final_joint")["value"], 1)
            null = formula_case({("revision", p, 0): constant(v) for p, v in (
                ("C", [0] * 4), ("K", [1, 0, 0, 0]), ("C_delta", [1, 1, 0, 0]), ("K_delta", [1, 1, 1, 0]))}, task)
            self.assertEqual(find(null, "eta", endpoint="accuracy", number=1)["value"], 0)
            for name in ("C_delta-C", "K_delta-K"):
                self.assertEqual(find(null, name, endpoint="accuracy", number=1)["value"], .5)

    def test_q_both_events_round_two_and_later_auc_final_preservation(self):
        for task in (Task.SORT, Task.BFS):
            result = formula_case({(event, p, 0): constant(v) for event, p, v in (
                ("revision", "B", [1, 0, 0, 0]), ("revision", "Q_B", [1, 1, 1, 0]),
                ("revision", "C", [1, 1, 0, 0]), ("revision", "Q_C", [0] * 4),
                ("sham", "B", [1, 0, 0, 0]), ("sham", "Q_B", [0] * 4),
                ("sham", "C", [1, 1, 0, 0]), ("sham", "Q_C", [1] * 4))}, task, uniform_preservation=True)
            for event, name, value, final in (("revision", "Q_B-B", .5, 0), ("revision", "Q_C-C", -.5, 0),
                                            ("sham", "Q_B-B", -.25, 0), ("sham", "Q_C-C", .5, 1)):
                self.assertEqual(find(result, name, event, "accuracy", 1)["value"], 0)
                for number in (2, 3, 4):
                    self.assertEqual(find(result, name, event, "accuracy", number)["value"], value)
                    self.assertEqual(find(result, name, event, "preservation", number)["value"], value)
                self.assertEqual(find(result, name, event)["value"], .75 * value)
                self.assertEqual(find(result, name, event, "preservation")["value"], .75 * value)
                self.assertEqual(find(result, name, event, "final_joint")["value"], final)

    def test_preserving_nonzero_cells_and_contrasts(self):
        for task in (Task.TOP_K, Task.BFS):
            result = formula_case({("preserving", p, 0): correct_rounds(n) for p, n in (("B", 1), ("C", 2), ("K", 4))}, task)
            for name, value, final in (("preserving_cell_B", .25, 0), ("preserving_cell_C", .5, 0),
                                     ("preserving_cell_K", 1, 1), ("C-B", .25, 0), ("K-C", .5, 1), ("K-B", .75, 1)):
                self.assertEqual(find(result, name, "preserving")["value"], value)
                self.assertEqual(find(result, name, "preserving", "preservation")["value"], value)
                self.assertEqual(find(result, name, "preserving", "final_joint")["value"], final)

    def test_equal_five_and_named_two_family_weights(self):
        p, _ = prepared("course")
        worlds = [w for w in p.main if w.index == 3 or w.world.task is Task.TOP_K and w.index in (2, 4)]
        worlds, branches = course_selection(worlds=worlds)
        matrices = {(w.world_id, "revision", "C", 0): constant([1] * 4) for w in worlds if w.world.task is Task.TOP_K}
        result = analyze_estimands(worlds, branches, tables(worlds, branches, matrices))
        row = next(r for r in result["summaries"] if r["primary"] and r["estimand"] == "theta" and r["level"] == "all_families")
        self.assertEqual(row["value"], 1 / 5)
        self.assertNotEqual(row["value"], 3 / 7)
        worlds = [w for w in p.main if w.world.task is Task.PREFIX and w.index in (2, 3, 4) or w.world.task is Task.SORT and w.index == 3]
        worlds, branches = course_selection(worlds=worlds)
        matrices = {(w.world_id, "revision", "K_delta", 0): constant([1] * 4) for w in worlds if w.world.task is Task.PREFIX}
        result = analyze_estimands(worlds, branches, tables(worlds, branches, matrices))
        row = next(r for r in result["summaries"] if r["estimand"] == "eta" and r["endpoint"] == "accuracy" and r["level"] == "all_families")
        self.assertEqual(row["value"], .5)
        self.assertNotEqual(row["value"], .75)
        self.assertEqual(sorted(row["family_denominators"].values()), [1, 3])

    def test_fixed_unknown_population_and_peer_preservation_weights(self):
        p, s = prepared("course")
        matrices = {(w.world_id, "revision", "C", 0): constant([1] * 4) for w in p.main}
        matrices[p.main[0].world_id, "revision", "B", 0] = constant([None] * 4)
        result = analyze_estimands(p.main, s.main, tables(p.main, s.main, matrices))
        row = next(r for r in result["summaries"] if r["primary"] and r["estimand"] == "theta" and r["level"] == "all_families")
        self.assertIsNone(row["value"])
        self.assertEqual(row["scheduled_worlds"], 20)
        self.assertEqual(row["observed_worlds"], 19)
        self.assertEqual(set(row["family_denominators"].values()), {4})
        self.assertEqual(row["complete_case_description"]["value"], 1)
        worlds, branches = course_selection(Task.DIFFERENCE)
        data = tables(worlds, branches)
        for metric in data["peer_diagnostics"]:
            if metric["policy"] == "C" and metric["event"] == "revision":
                peer = metric["peer"]
                metric.update(denominator=10 if peer == 0 else 1 if peer == 1 else 0,
                    numerator=9 if peer == 0 else 0, rate=.9 if peer == 0 else 0 if peer == 1 else None,
                    eligible_coordinates=list(range(10)) if peer == 0 else [0] if peer == 1 else [])
        result = analyze_estimands(worlds, branches, data)
        term = find(result, "C-B", endpoint="preservation")["components"][0]
        self.assertEqual(term["exact"], {"numerator": 9, "denominator": 20})
        self.assertEqual((term["unique_coordinate_count"], term["peer_copy_count"]), (10, 11))
        for metric in data["peer_diagnostics"]:
            if metric["policy"] == "C" and metric["event"] == "revision" and metric["peer"] == 0:
                metric.update(denominator=None, numerator=None, rate=None)
        self.assertEqual(find(analyze_estimands(worlds, branches, data), "C-B", endpoint="preservation")["eligibility"], "unknown")

    def test_only_five_repeats_ties_signs_trajectories_and_primary_separation(self):
        p, s = prepared("course")
        zero = analyze_estimands(p.main, s.main, tables(p.main, s.main))
        world = next(w for w in p.main if w.world.task is Task.DIFFERENCE and w.index == 1)
        data = tables(p.main, s.main, {(world.world_id, "revision", "C", 0): constant([1] * 4),
            (world.world_id, "revision", "B", 1): constant([1] * 4)})
        before = analyze_estimands(p.main, s.main, data)
        theta = next(r for r in before["repeatability"] if r["world_id"] == world.world_id and r["estimand"] == "theta" and r["endpoint"] == "auc")
        self.assertEqual(theta["classification"], "sign_reversal")
        self.assertEqual((theta["replicate_zero"], theta["replicate_one"]), (1, -1))
        self.assertTrue(any(r["classification"] == "both_ties" for r in before["repeatability"]))
        self.assertTrue(any(r["category_changed"] for r in before["trajectory_changes"]))
        for row in data["outcomes"]:
            if row["replicate"] == 1:
                row.update(correct=None, protocol_outcome="unknown")
        for row in data["peer_diagnostics"]:
            if row["replicate"] == 1:
                row.update(numerator=None, rate=None)
        after = analyze_estimands(p.main, s.main, data)
        self.assertEqual(before["world_contrasts"], after["world_contrasts"])
        self.assertEqual(before["summaries"], after["summaries"])
        self.assertTrue(all(r["classification"] == "unknown" for r in after["repeatability"]))
        self.assertTrue(all(r["category_changed"] is None for r in after["trajectory_changes"]))
        self.assertEqual(len(zero["populations"][0]["world_ids"]), 20)
        self.assertEqual(len({r["world_id"] for r in after["repeat_contrasts"]}), 5)
        self.assertTrue(all(r["replicate"] == 1 and r["population"] == "main" for r in after["repeat_contrasts"]))
        self.assertFalse(any(r["estimand"].startswith(("receipt", "Q_", "preserving")) for r in after["repeat_contrasts"]))


class CourseOfflineRecordTests(unittest.TestCase):
    def fixture(self, task=Task.DIFFERENCE, policies=("B",)):
        worlds, branches = course_selection(task)
        branches = tuple(b for b in branches if b.phase == "prefix" or
                         b.phase == "continuation" and b.event == "revision" and b.policy in policies)
        records, inputs, attempts = saved_records(worlds, branches)
        for saved in inputs.values():
            saved["settings_json"] = encode({"protocol_limits": asdict(COURSE_LIMITS)})
        return worlds, branches, records, inputs, attempts

    def test_later_invalid_timeout_and_unexecuted_never_inherit_correct_answers(self):
        for status in ("invalid", "timeout", "unknown"):
            worlds, branches, records, inputs, attempts = self.fixture()
            branch = next(b for b in branches if b.phase == "continuation")
            call = next(c for c in branch.calls if c.round_number == 4 and c.peer == 0)
            saved = records[call.call_id]
            if status == "unknown":
                del records[call.call_id]
                attempts = [r for r in attempts if r["call_id"] != call.call_id]
            elif status == "timeout":
                saved.update(status="timeout", raw_json=None, validation_json=None,
                             failure_json=encode({"status": "timeout"}))
            else:
                validation = json.loads(saved["validation_json"])
                validation.update(json_valid=False, schema_valid=False, permissions_valid=False)
                validation["candidate"].update(status="invalid", value=None)
                saved["validation_json"] = encode(validation)
            result = evaluate_records(worlds, branches, records, inputs, attempts)
            row = next(r for r in result["outcomes"] if r["call_id"] == call.call_id)
            self.assertEqual(row["correct"], None if status == "unknown" else 0)
            trajectory = next(r for r in result["trajectories"] if r["branch_id"] == branch.branch_id)
            self.assertEqual(trajectory["auc"], None if status == "unknown" else 15 / 16)
            self.assertEqual(trajectory["final_joint"], None if status == "unknown" else 0)

    def test_course_output_cap_and_contradictory_settings_are_not_thesis_defaults(self):
        worlds, branches, records, inputs, attempts = self.fixture()
        saved = next(iter(records.values()))
        for length in (256, 257):
            raw = json.loads(saved["raw_json"])
            raw["token_ids"] = [1] * length
            validation = json.loads(saved["validation_json"])
            validation["generated"] = raw
            saved.update(raw_json=encode(raw), validation_json=encode(validation))
            if length == 256:
                self.assertEqual(evaluate_records(worlds, branches, records, inputs, attempts)["coverage"]["unknown"], 0)
            else:
                with self.assertRaises(ValueError):
                    evaluate_records(worlds, branches, records, inputs, attempts)
        inputs[saved["branch_id"], saved["round_number"]]["settings_json"] = '{"max_new_tokens":256}'
        with self.assertRaises(ValueError):
            evaluate_records(worlds, branches, records, inputs, attempts)

    def test_missing_replay_parent_and_literal_candidate_key_defects_fail(self):
        worlds, branches, records, inputs, attempts = self.fixture(Task.BFS, ("B", "C", "P_G", "P_H", "Q_B", "Q_C"))
        replay = next(r for r in records.values() if r["replay_parent"])
        parent = records.pop(replay["generation_id"])
        without_parent_attempt = [r for r in attempts if r["call_id"] != parent["call_id"]]
        with self.assertRaisesRegex(ValueError, "original physical outcome"):
            evaluate_records(worlds, branches, records, inputs, without_parent_attempt)
        records[parent["call_id"]] = parent
        physical = next(r for r in records.values() if not r["replay_parent"] and r["round_number"] == 4)
        original = physical["validation_json"]
        for change in ("missing", "duplicate", "order"):
            validation = json.loads(original)
            pairs = validation["candidate"]["value"]
            if change == "missing": pairs.pop()
            elif change == "duplicate": pairs.append(pairs[0])
            else: pairs.reverse()
            physical["validation_json"] = encode(validation)
            with self.assertRaises(ValueError):
                evaluate_records(worlds, branches, records, inputs, attempts)

    def test_sqlite_read_only_duplicate_and_manifest_drift_fail(self):
        worlds, branches, records, inputs, attempts = self.fixture()
        with tempfile.TemporaryDirectory() as directory:
            worker = Path(directory) / "worker.sqlite"
            write_worker(worker, records, inputs, attempts)
            original = worker.read_bytes()
            actual = analyze_run(worlds, branches, [worker])
            self.assertEqual(actual["coverage"]["recorded"], 32)
            self.assertEqual(worker.read_bytes(), original)
            with self.assertRaises(ValueError): analyze_run(worlds, branches, [worker, worker])
            missing = Path(directory) / "absent.sqlite"
            self.assertEqual(evaluate_run(worlds, branches, [missing])["coverage"]["unknown"], 32)
            self.assertFalse(missing.exists())
        altered = copy.deepcopy(tables(worlds, branches))
        altered["outcomes"][0]["seed"] += 1
        with self.assertRaises(ValueError): analyze_estimands(worlds, branches, altered)


class CourseAnalysisCLITests(unittest.TestCase):
    def test_manifest_default_explicit_twenty_and_cross_regime_refusal(self):
        with tempfile.TemporaryDirectory() as directory:
            absent = Path(directory) / "absent.sqlite"
            base = [sys.executable, "-S", "-m", "recovery", "analyze", "--manifest", str(ROOT / "tests/fixtures/population_course.json"),
                    "--schedule", str(ROOT / "tests/fixtures/schedules_course.json"), "--worker", str(absent)]
            results = []
            for label, extra, expected in (("default", ["--estimands"], 6280), ("explicit", ["--estimands", "--count", "20"], 6280),
                                           ("outcomes", [], 6280), ("development", ["--estimands", "--stage", "development"], 1178)):
                output = Path(directory) / (label + ".json.gz")
                result = subprocess.run(base + extra + ["--output", str(output)], cwd=ROOT, capture_output=True, text=True, timeout=90)
                self.assertEqual(result.returncode, 0, result.stderr)
                with gzip.open(output, "rt", encoding="utf-8") as source: actual = json.load(source)
                self.assertEqual(actual["coverage"]["unknown"], expected)
                self.assertFalse(absent.exists())
                if "estimands" in actual:
                    cohort = next(r for r in actual["estimands"]["populations"] if r["population"] == "repeat")
                    self.assertEqual(len(cohort["world_ids"]), 0 if label == "development" else 5)
                results.append(actual)
            self.assertEqual(results[0], results[1])
            for count in (40, 60):
                output = Path(directory) / (str(count) + ".json")
                result = subprocess.run(base + ["--count", str(count), "--output", str(output)], cwd=ROOT, capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(output.exists())
            for regime, count in (("target", 60), ("fallback", 40)):
                # Preserve default thesis 60; its nested 40 remains explicit.
                output = Path(directory) / (regime + ".json")
                schedule = ROOT / "tests/fixtures/schedules_target.json"
                manifest = ROOT / "tests/fixtures/population_target.json"
                extra = [] if count == 60 else ["--count", "40"]
                result = subprocess.run([*base[:5], "--manifest", str(manifest), "--schedule", str(schedule), "--worker", str(absent),
                    *extra, "--output", str(output)], cwd=ROOT, capture_output=True, text=True, timeout=90)
                self.assertEqual(result.returncode, 0, result.stderr)
                actual = json.loads(output.read_bytes())
                self.assertEqual(actual["coverage"]["scheduled"], 17656 if count == 60 else 12560)


if __name__ == "__main__":
    unittest.main()
