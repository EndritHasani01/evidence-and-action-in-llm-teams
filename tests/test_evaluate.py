"""Hand-calculated exact, coordinate and trajectory fixtures for spec §7.1."""

import copy
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recovery.evaluate import (ANNOTATIONS, aggregate_diagnostics, annotation_counts, candidate_payload,
                               evaluate_records, evaluate_run, identical_wrong_agreement,
                               score_candidate, score_coordinates, trajectory, write_evaluation)
from recovery.tasks import Size, Task
from recovery.truth import Truth
from tests.outcome_fixture import ROOT, encode, saved_records, selection, write_worker


def metric(rows, name):
    return next(r for r in rows if r["metric"] == name)


class ExactOutcomeTests(unittest.TestCase):
    def test_saved_bfs_pair_encoding_is_decoded_without_losing_keys(self):
        state = {"status": "valid", "value": [[str(j), j] for j in range(8)]}
        self.assertEqual(candidate_payload(Task.BFS, Size.FALLBACK, 0, state), {str(j): j for j in range(8)})
        for pairs in (state["value"][:-1], state["value"] + [["0", 0]], list(reversed(state["value"]))):
            with self.assertRaises(ValueError):
                candidate_payload(Task.BFS, Size.FALLBACK, 0, dict(state, value=pairs))
    def test_order_and_duplicate_multiplicity(self):
        gold = Truth(Task.TOP_K, Size.TARGET, (9, 9, 8, 8, 7, 7, 6, 6, 5, 5))
        for peer in range(4):
            self.assertEqual(score_candidate(gold, "valid", gold.candidate(peer), peer), 1)
            wrong = [9, 8, 7, 6, 5] * 2
            self.assertEqual(score_candidate(gold, "valid", wrong, peer), 0)
            self.assertEqual(score_candidate(gold, "valid", list(reversed(gold.values)), peer), 0)
            for status, expected in (("invalid", 0), ("failed", 0), ("unknown", None)):
                self.assertEqual(score_candidate(gold, status, gold.candidate(peer), peer), expected)
        with self.assertRaises(ValueError):
            score_candidate(gold, "valid", [True] * 10, 0)

    def test_bfs_full_dictionary_and_unreachable_node(self):
        gold = Truth(Task.BFS, Size.FALLBACK, (0, 1, 2, 3, 4, 5, 6, -1))
        answer = dict(reversed(list(gold.candidate().items())))
        self.assertEqual(score_candidate(gold, "valid", answer, 2), 1)
        answer["7"] = 7
        self.assertEqual(score_candidate(gold, "valid", answer, 2), 0)
        del answer["7"]
        with self.assertRaises(ValueError):
            score_candidate(gold, "valid", answer, 2)

    def test_segment_assignments_and_full_information_control(self):
        for task in (Task.PREFIX, Task.SORT):
            gold = Truth(task, Size.TARGET, tuple(range(32)))
            for peer in range(4):
                self.assertEqual(score_candidate(gold, "valid", list(range(8 * peer, 8 * peer + 8)), peer), 1)
            self.assertEqual(score_candidate(gold, "valid", list(range(32)), None), 1)


class CoordinateOutcomeTests(unittest.TestCase):
    def setUp(self):
        self.old = Truth(Task.DIFFERENCE, Size.FALLBACK, tuple(range(1, 24)))
        self.new = Truth(Task.DIFFERENCE, Size.FALLBACK, (101, 102, *range(3, 24)))

    def test_repair_old_errors_and_collateral_damage_are_distinct(self):
        old_answer = self.old.candidate(0)
        old_answer[3] = -4  # Coordinate 4 was an old U error, eligible for repair only.
        answer = self.new.candidate(0)
        answer[0] = 1  # Coordinate 1 explicitly persists at old gold.
        answer[2] = -3  # Coordinate 3 was old-correct U, now collateral damage.
        coordinates, rates = score_coordinates(self.old, self.new, 0, "valid", answer, "valid", old_answer)
        self.assertEqual(coordinates[0]["coordinate"], 1)
        self.assertEqual([r["set"] for r in coordinates[:3]], ["D", "D", "U"])
        self.assertEqual(metric(rates, "changed_accuracy")["rate"], 1 / 2)
        self.assertEqual(metric(rates, "old_value_persistence")["rate"], 1 / 2)
        self.assertEqual(metric(rates, "preservation")["denominator"], 20)
        self.assertEqual(metric(rates, "preservation")["rate"], 19 / 20)
        self.assertEqual(metric(rates, "collateral_damage")["rate"], 1 / 20)
        self.assertEqual(metric(rates, "old_error_repair")["rate"], 1)
        self.assertTrue(coordinates[3]["old_error_eligible"])
        self.assertFalse(coordinates[3]["preservation_eligible"])
        self.assertTrue(coordinates[3]["changed_from_prefix"])

    def test_invalid_current_is_incorrect_and_explicitly_malformed(self):
        coordinates, rates = score_coordinates(self.old, self.new, 0, "invalid", self.old.candidate(),
                                                "valid", self.old.candidate())
        self.assertEqual(metric(rates, "changed_accuracy")["rate"], 0)
        self.assertEqual(metric(rates, "old_value_persistence")["rate"], 0)
        self.assertEqual(metric(rates, "changed_malformed_or_missing")["rate"], 1)
        self.assertEqual(metric(rates, "preservation")["rate"], 0)
        self.assertEqual(metric(rates, "collateral_damage")["rate"], 1)
        self.assertTrue(all(r["value"] is None for r in coordinates))

    def test_final_invalid_prefix_never_backfills_an_earlier_answer(self):
        for prefix_status in ("invalid", "failed"):
            _, rates = score_coordinates(self.old, self.new, 0, "valid", self.new.candidate(),
                                        prefix_status, self.old.candidate())
            for name in ("preservation", "collateral_damage", "old_error_repair"):
                row = metric(rates, name)
                self.assertEqual(row["denominator"], 0)
                self.assertIsNone(row["rate"])
                self.assertEqual(row["reason"], "prefix_round_four_not_protocol_valid")

    def test_empty_D_empty_U_and_no_eligible_old_correct_coordinate(self):
        _, rates = score_coordinates(self.old, self.old, 0, "valid", self.old.candidate(),
                                    "valid", self.old.candidate())
        self.assertEqual(metric(rates, "changed_accuracy")["reason"], "no_changed_coordinates")
        self.assertIsNone(metric(rates, "old_value_persistence")["rate"])
        self.assertEqual(metric(rates, "preservation")["rate"], 1)
        all_changed = Truth(self.old.task, self.old.size, tuple(v + 1 for v in self.old.values))
        _, rates = score_coordinates(self.old, all_changed, 0, "valid", all_changed.candidate(),
                                    "valid", self.old.candidate())
        self.assertEqual(metric(rates, "preservation")["reason"], "no_unchanged_coordinates")
        _, rates = score_coordinates(self.old, self.new, 0, "valid", self.new.candidate(),
                                    "valid", [-999] * 23)
        self.assertEqual(metric(rates, "preservation")["reason"], "no_correct_prefix_U_coordinates")
        self.assertEqual(metric(rates, "old_error_repair")["denominator"], 21)

    def test_unknown_slot_and_unknown_prefix_eligibility(self):
        _, rates = score_coordinates(self.old, self.new, 0, "unknown", None, "valid", self.old.candidate())
        self.assertEqual(metric(rates, "changed_accuracy")["denominator"], 2)
        self.assertIsNone(metric(rates, "changed_accuracy")["numerator"])
        self.assertEqual(metric(rates, "preservation")["denominator"], 21)
        self.assertIsNone(metric(rates, "preservation")["rate"])
        _, rates = score_coordinates(self.old, self.new, 0, "valid", self.new.candidate(), "unknown", None)
        self.assertEqual(metric(rates, "changed_accuracy")["rate"], 1)
        self.assertIsNone(metric(rates, "preservation")["denominator"])
        self.assertEqual(metric(rates, "preservation")["reason"], "prefix_round_four_unknown")

    def test_unique_global_coordinates_for_segments(self):
        old = Truth(Task.PREFIX, Size.TARGET, tuple(range(32)))
        new = Truth(Task.PREFIX, Size.TARGET, (*range(16), *range(116, 132)))
        for peer in range(4):
            coordinates, rates = score_coordinates(old, new, peer, "valid", new.candidate(peer),
                                                    "valid", old.candidate(peer))
            self.assertEqual([r["coordinate"] for r in coordinates], list(range(peer * 8, peer * 8 + 8)))
            self.assertEqual(metric(rates, "changed_accuracy")["denominator"], 0 if peer < 2 else 8)


class TrajectoryTests(unittest.TestCase):
    def test_four_complete_categories_times_auc_and_regression(self):
        examples = [
            ([1, 1, 1, 1], "continuously_correct", 1, 1, False, 1),
            ([0, 0, 1, 1], "correct_at_end_after_delay_or_regression", 3, 3, False, 1 / 2),
            ([1, 0, 0, 1], "correct_at_end_after_delay_or_regression", 1, 4, True, 1 / 2),
            ([0, 1, 0, 0], "temporarily_correct_but_incorrect_at_end", 2, None, True, 1 / 4),
            ([0, 0, 0, 0], "never_jointly_correct", None, None, False, 0),
        ]
        for rounds, category, first, stable, regression, auc in examples:
            with self.subTest(rounds=rounds):
                result = trajectory([[c] * 4 for c in rounds])
                self.assertEqual(result["category"], category)
                self.assertEqual(result["first_joint_round"], first)
                self.assertEqual(result["first_stable_joint_round"], stable)
                self.assertEqual(result["regression"], regression)
                self.assertEqual(result["auc"], auc)
                self.assertEqual(result["final_joint"], rounds[-1])

    def test_fragmentation_does_not_splice_best_answers(self):
        result = trajectory([[int(peer == r) for peer in range(4)] for r in range(4)])
        self.assertEqual(result["individual_ever"], [True] * 4)
        self.assertFalse(result["joint_ever"])
        self.assertTrue(result["fragmented"])
        self.assertEqual(result["auc"], 1 / 4)
        self.assertEqual(result["final_joint"], 0)
        self.assertIsNone(result["first_joint_round"])

    def test_incomplete_is_separate_from_never_correct(self):
        result = trajectory([[None] * 4] * 4)
        self.assertEqual(result["category"], "incomplete")
        for name in ("auc", "final_joint", "first_joint_round", "first_stable_joint_round", "fragmented", "regression"):
            self.assertIsNone(result[name])
        result = trajectory([[1] * 4, [0] * 4, [None] * 4, [1] * 4])
        self.assertEqual(result["observed_first_joint_round"], 1)
        self.assertTrue(result["regression"])
        self.assertIsNone(result["first_stable_joint_round"])
        self.assertEqual(result["category"], "incomplete")

    def test_identical_wrong_only_for_replicated_outputs(self):
        outcomes = [{"protocol_outcome": "valid", "correct": 0, "candidate": [4] * 10}] * 4
        for task in (Task.TOP_K, Task.DIFFERENCE, Task.BFS):
            self.assertTrue(identical_wrong_agreement(task, outcomes))
        for task in (Task.PREFIX, Task.SORT):
            self.assertIsNone(identical_wrong_agreement(task, outcomes))
        self.assertFalse(identical_wrong_agreement(Task.TOP_K, [*outcomes[:3], dict(outcomes[3], protocol_outcome="invalid")]))
        self.assertIsNone(identical_wrong_agreement(Task.TOP_K, [*outcomes[:3], dict(outcomes[3], protocol_outcome="unknown")]))


class OfflineRecordTests(unittest.TestCase):
    def test_saved_numeric_and_bfs_candidates_and_original_attempt_joins(self):
        for task in Task:
            worlds, branches = selection(task)
            records, inputs, attempts = saved_records(worlds, branches)
            result = evaluate_records(worlds, branches, records, inputs, attempts)
            self.assertEqual(result["coverage"], {"scheduled": 32, "recorded": 32, "unknown": 0,
                                               "protocol_outcomes": {"valid": 32}})
            self.assertTrue(all(r["correct"] == 1 and r["attempt_numbers"] == [1] for r in result["outcomes"]))
            self.assertTrue(all(r["auc"] == 1 for r in result["trajectories"]))
            if task in (Task.PREFIX, Task.SORT):
                self.assertTrue(all(r["identical_wrong_agreement"] is None for r in result["rounds"]))

    def test_invalid_failed_unknown_and_raw_validation_defect_are_distinct(self):
        worlds, branches = selection()
        records, inputs, attempts = saved_records(worlds, branches)
        branch = next(b for b in branches if b.phase == "continuation")
        invalid, failed, unknown = (records[c.call_id] for c in branch.calls[:3])
        validation = json.loads(invalid["validation_json"])
        validation["candidate"].update(status="invalid", value=None)
        invalid["validation_json"] = encode(validation)
        validation = json.loads(failed["validation_json"])
        validation["candidate"].update(status="failed", value=None)
        validation["generated"] = None
        failed.update(status="timeout", raw_json=None, failure_json='{"status":"timeout","reason":"fixture"}',
                      validation_json=encode(validation))
        unknown.update(status="running", raw_json=None, validation_json=None)
        result = evaluate_records(worlds, branches, records, inputs, attempts)
        outcomes = {r["call_id"]: r for r in result["outcomes"]}
        self.assertEqual([outcomes[r["call_id"]]["correct"] for r in (invalid, failed, unknown)], [0, 0, None])
        self.assertEqual(result["coverage"]["unknown"], 1)
        self.assertEqual(next(r for r in result["trajectories"] if r["phase"] == "continuation")["category"], "incomplete")
        raw = records[branch.calls[3].call_id]
        raw["validation_json"] = None
        with self.assertRaisesRegex(ValueError, "resume validation"):
            evaluate_records(worlds, branches, records, inputs, attempts)

    def test_literal_replay_and_unexecuted_replay_do_not_copy_parent_outcomes(self):
        worlds, branches = selection(Task.BFS, ("B", "Q_B"))
        records, inputs, attempts = saved_records(worlds, branches)
        result = evaluate_records(worlds, branches, records, inputs, attempts)
        replay = next(r for r in result["outcomes"] if r["replay_parent"])
        self.assertEqual(replay["correct"], 1)
        self.assertEqual(replay["attempt_numbers"], [1])
        self.assertEqual(len(result["attempts"]), 44)
        record = records[replay["call_id"]]
        record.update(status="pending", validation_json=None)
        result = evaluate_records(worlds, branches, records, inputs, attempts)
        self.assertIsNone(next(r for r in result["outcomes"] if r["call_id"] == replay["call_id"])["correct"])
        record.update(status="replay", validation_json=records[replay["generation_id"]]["validation_json"])
        barrier = inputs[replay["branch_id"], replay["round"]]
        barrier["settings_json"] = '{"drift":true}'
        with self.assertRaisesRegex(ValueError, "settings differs"):
            evaluate_records(worlds, branches, records, inputs, attempts)

    def test_failure_annotations_overlap_and_keep_archived_provenance(self):
        worlds, branches = selection()
        records, inputs, attempts = saved_records(worlds, branches)
        branch = next(b for b in branches if b.phase == "continuation")
        from recovery.truth import solve_world
        old = solve_world(worlds[0].world)
        row = records[branch.calls[0].call_id]
        validation = json.loads(row["validation_json"])
        validation["candidate"]["value"] = old.candidate(0)
        validation["generated"]["text"] = json.dumps({"candidate": old.candidate(0), "send": []})
        row.update(validation_json=encode(validation), raw_json=encode(validation["generated"]))
        row = records[next(c.call_id for c in branch.calls if c.round_number == 4 and c.peer == 0)]
        validation = json.loads(row["validation_json"])
        validation["candidate"].update(status="invalid", value=None)
        row["validation_json"] = encode(validation)
        # Peer 1 has a pending replacement at the first call boundary, despite a correct answer.
        barrier = inputs[branch.branch_id, 1]
        state = json.loads(barrier["requests"]["before"])
        state["peers"] = copy.deepcopy(state["peers"])
        for source in state["peers"][1]["sources"]:
            if source["version"] == 2:
                del source["value"]
                del source["deleted"]
        barrier["requests"]["before"] = encode(state)
        result = evaluate_records(worlds, branches, records, inputs, attempts)
        rows = [r for r in result["annotations"] if r["branch_id"] == branch.branch_id]
        first = next(r for r in rows if r["round"] == 1 and r["peer"] == 0)
        self.assertTrue(first["labels"]["incorrect_after_v2"])
        self.assertTrue(first["labels"]["explicit_old_value_persistence"])
        self.assertTrue(first["v2_delivery_ids"])
        pending = next(r for r in rows if r["round"] == 1 and r["peer"] == 1)
        self.assertTrue(pending["labels"]["v2_unavailable"])
        self.assertFalse(pending["labels"]["incorrect_after_v2"])
        last = next(r for r in rows if r["round"] == 4 and r["peer"] == 0)
        for label in ("protocol_inference_failure", "incorrect_after_v2", "collateral_error", "regression"):
            self.assertTrue(last["labels"][label])
        counts = next(r for r in result["annotation_counts"] if r["branch_id"] == branch.branch_id)
        overlap = next(r for r in counts["intersections"] if r["labels"] == ["protocol_inference_failure", "regression"])
        self.assertEqual(overlap["positive"], 1)
        self.assertEqual(sum(r["count"] for r in counts["patterns"]), 16)

    def test_reader_is_read_only_missing_files_are_unknown_and_duplicates_fail(self):
        worlds, branches = selection()
        records, inputs, attempts = saved_records(worlds, branches)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "worker.sqlite"
            write_worker(path, records, inputs, attempts)
            before = path.read_bytes()
            self.assertEqual(evaluate_run(worlds, branches, [path])["coverage"]["recorded"], 32)
            self.assertEqual(path.read_bytes(), before)
            missing = path.with_name("missing.sqlite")
            self.assertEqual(evaluate_run(worlds, branches, [missing])["coverage"]["unknown"], 32)
            self.assertFalse(missing.exists())
            with self.assertRaisesRegex(ValueError, "once"):
                evaluate_run(worlds, branches, [path, path])
            backup = path.with_name("backup.sqlite")
            backup.write_bytes(before)
            with self.assertRaisesRegex(ValueError, "duplicate"):
                evaluate_run(worlds, branches, [path, backup])

    def test_offline_imports_exclude_runtime_and_inference_dependencies(self):
        code = '''
import sys, importlib.abc
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in ("torch", "transformers", "pydantic", "langgraph"):
            raise AssertionError(fullname)
sys.meta_path.insert(0, Block())
from tests.outcome_fixture import selection, saved_records
from recovery.evaluate import evaluate_records
w, b = selection()
evaluate_records(w, b, *saved_records(w, b))
forbidden = ('torch', 'transformers', 'pydantic', 'langgraph', 'recovery.runner',
             'recovery.accounting', 'recovery.workers', 'recovery.protocol', 'recovery.rounds')
assert all(n not in sys.modules for n in forbidden)
'''
        result = subprocess.run([sys.executable, "-S", "-c", code], cwd=ROOT, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_export_is_exclusive_and_plain_and_gzip_tables_agree(self):
        worlds, branches = selection()
        result = evaluate_records(worlds, branches, *saved_records(worlds, branches))
        with tempfile.TemporaryDirectory() as directory:
            plain, compressed = Path(directory) / "tables.json", Path(directory) / "tables.json.gz"
            write_evaluation(plain, result)
            write_evaluation(compressed, result)
            self.assertEqual(plain.read_bytes(), gzip.decompress(compressed.read_bytes()))
            with self.assertRaises(FileExistsError):
                write_evaluation(plain, result)

    def test_cli_joins_entire_development_manifest_offline_and_protects_export(self):
        with tempfile.TemporaryDirectory() as directory:
            output, missing = Path(directory) / "tables.json.gz", Path(directory) / "missing.sqlite"
            command = [sys.executable, "-S", "-m", "recovery", "analyze", "--stage", "development",
                "--manifest", str(ROOT / "tests/fixtures/population_target.json"),
                "--schedule", str(ROOT / "tests/fixtures/schedules_target.json"),
                "--worker", str(missing), "--output", str(output)]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            tables = json.loads(gzip.decompress(output.read_bytes()))
            self.assertEqual(tables["coverage"]["scheduled"], 1178)
            self.assertEqual(tables["coverage"]["unknown"], 1178)
            self.assertTrue(all(r["category"] == "incomplete" for r in tables["trajectories"]))
            self.assertFalse(missing.exists())
            before = output.read_bytes()
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_bytes(), before)


class DiagnosticAggregationTests(unittest.TestCase):
    def test_average_peers_then_worlds_then_equal_eligible_families(self):
        base = dict(size="target", phase="continuation", event="revision", policy="B", replicate=0,
                    round=1, metric="preservation", reason=None)
        rows = []
        for family, world, peer, numerator, denominator in (
                ("difference_array", "a", 0, 1, 1), ("difference_array", "a", 1, 0, 9),
                ("difference_array", "b", 0, 0, 100), ("prefix_sum", "c", 0, 1, 1),
                ("bfs_distance", "d", 0, 0, 0)):
            rows.append(dict(base, family=family, world_id=world, branch_id=world + "/B", peer=peer,
                numerator=numerator, denominator=denominator, rate=numerator / denominator if denominator else None,
                eligible_coordinates=list(range(denominator))))
        result = aggregate_diagnostics(rows)
        pooled = next(r for r in result if r["level"] == "all_families")
        self.assertEqual(pooled["rate"], 5 / 8)
        self.assertEqual((pooled["eligible_peers"], pooled["eligible_worlds"], pooled["eligible_families"]), (4, 3, 2))
        self.assertEqual(pooled["scheduled_families"], 3)
        self.assertEqual(pooled["unique_coordinate_count"], 110)
        self.assertEqual(pooled["peer_copy_count"], 111)
        rows[0].update(numerator=None, rate=None, reason="slot_unknown")
        self.assertIsNone(next(r for r in aggregate_diagnostics(rows) if r["level"] == "all_families")["rate"])

    def test_annotation_unknowns_and_inapplicable_denominators_are_explicit(self):
        labels = {k: None for k in ANNOTATIONS}
        base = dict(size="target", phase="continuation", event="sham", policy="B", replicate=0,
                    family="top_k", world_id="a", branch_id="a/B", labels=labels,
                    reasons={k: "not_applicable" if k != "protocol_inference_failure" else "slot_unknown" for k in ANNOTATIONS})
        result = annotation_counts([base])[0]
        self.assertEqual(result["counts"]["protocol_inference_failure"]["unknown"], 1)
        self.assertEqual(result["counts"]["v2_unavailable"]["not_applicable"], 1)
        self.assertEqual(result["counts"]["v2_unavailable"]["applicable"], 0)


if __name__ == "__main__":
    unittest.main()
