"""Hand-calculated estimands, scope/denominators and conditional repeatability."""

import copy
from fractions import Fraction
import subprocess
import sys
import unittest

from recovery.analysis import analyze_estimands, compare_replicates, population_table
from recovery.tasks import Task
from tests.estimand_fixture import selection, tables, constant, correct_rounds, group_matrix, zeros, prepared
from tests.outcome_fixture import ROOT


def find(result, name, event="revision", endpoint="auc", number=None, *, table="world_contrasts", world=None):
    return next(r for r in result[table] if r["estimand"] == name and r["event"] == event and
        r["endpoint"] == endpoint and r["round"] == number and (world is None or r.get("world_id") == world))


class EstimandTests(unittest.TestCase):
    def run_case(self, matrices, task=Task.DIFFERENCE, index=3):
        worlds, branches = selection(task, index)
        mappings = {(worlds[0].world_id, *key): value for key, value in matrices.items()}
        return analyze_estimands(worlds, branches, tables(worlds, branches, mappings))

    def test_theta_equal_effect_null_positive_and_negative(self):
        for sham, expected in ((constant([1, 1, 0, 0]), 0), (zeros(), .5), (constant([1, 1, 1, 1]), -.5)):
            result = self.run_case({("revision", "B", 0): constant([1, 0, 0, 0]),
                ("revision", "C", 0): constant([1, 1, 1, 0]), ("sham", "C", 0): sham})
            self.assertEqual(find(result, "theta", "revision_minus_sham")["value"], expected)
            self.assertEqual(find(result, "C-B")["value"], .5)
            self.assertEqual(find(result, "theta", "revision_minus_sham")["range"], [-2, 2])

    def test_retained_collaborator_null_benefit_harm_and_same_event_effect(self):
        worlds, _ = selection(Task.DIFFERENCE)
        world = worlds[0]
        for baseline, retained, expected in ((0, 0, 0), (0, 1, 1), (1, 0, -1)):
            result = self.run_case({(event, policy, 0): matrix for event in ("revision", "sham")
                for policy, matrix in (("B", constant([baseline] * 4)),
                    ("P_G", group_matrix(world, [0, 0], [retained, retained])),
                    ("P_H", group_matrix(world, [retained, retained], [0, 0])))})
            self.assertEqual(find(result, "E_keep", endpoint="collaborator_accuracy")["value"], expected)
            self.assertEqual(find(result, "E_keep", "sham", "collaborator_accuracy")["value"], expected)
            self.assertEqual(find(result, "phi_corr", "revision_minus_sham", "collaborator_accuracy")["value"], 0)

    def test_focal_peers_match_and_round_one_is_excluded(self):
        world = selection(Task.DIFFERENCE)[0][0]
        B = correct_rounds(1)
        result = self.run_case({("revision", "B", 0): B,
            ("revision", "P_G", 0): group_matrix(world, [0, 0], [1, 1]),
            ("revision", "P_H", 0): group_matrix(world, [1, 1], [0, 0])})
        phi = find(result, "E_keep", endpoint="collaborator_accuracy")
        self.assertEqual(phi["value"], 1)
        self.assertTrue(phi["primary"])
        for term, peers in zip(phi["components"], (world.partition[0], world.partition[0], world.partition[1], world.partition[1])):
            self.assertEqual(term["peers"], list(peers))
            self.assertEqual(term["rounds"], [2, 3, 4])
            self.assertEqual(len(term["atoms"]), 6)
        reference = find(result, "E_keep", endpoint="accuracy", number=1)
        self.assertEqual(reference["value"], 0)
        self.assertTrue(reference["construction_reference"])
        self.assertFalse(reference["primary"])

    def test_clear_and_complementary_own_group_signs(self):
        world = selection(Task.DIFFERENCE)[0][0]
        result = self.run_case({("revision", policy, 0): group_matrix(world, G, H) for policy, G, H in (
            ("B", [1, 0], [1, 1]), ("P_G", [0, 0], [1, 0]),
            ("P_H", [1, 1], [0, 0]), ("C", [1, 0], [1, 0]))})
        for name, expected in (("E_keep", 0), ("E_clear", .5),
                ("own_reset_other_retained", -.75), ("own_reset_other_cleared", -.25)):
            self.assertEqual(find(result, name, endpoint="collaborator_accuracy")["value"], expected)
        for group in ("G", "H"):
            for mask in ("00", "10", "01", "11"):
                self.assertIsNotNone(find(result, f"M_{group}_{mask}", endpoint="collaborator_accuracy")["value"])

    def test_every_retention_delivery_evidence_and_compact_endpoint(self):
        mappings = {("revision", p, 0): correct_rounds(n) for p, n in (("L", 0), ("B", 1), ("C", 2), ("K", 3), ("F", 4))}
        mappings.update({("sham", p, 0): correct_rounds(n) for p, n in (("B", 2), ("C", 1), ("K", 0))})
        result = self.run_case(mappings)
        for name, auc, final in (("C-B", .25, 0), ("K-C", .25, 0), ("K-B", .5, 0),
                                ("B-L", .25, 0), ("C-F", -.5, -1)):
            self.assertEqual(find(result, name)["value"], auc)
            self.assertEqual(find(result, name, endpoint="final_joint")["value"], final)
            self.assertEqual(find(result, name, endpoint="preservation")["value"], auc)
            self.assertEqual(find(result, name, endpoint="preservation", number=4)["value"], final)
        for name, values in (("C-B", [0, 1, 0, 0]), ("K-C", [0, 0, 1, 0]), ("K-B", [0, 1, 1, 0]),
                             ("B-L", [1, 0, 0, 0]), ("C-F", [0, 0, -1, -1])):
            for number, value in enumerate(values, 1):
                self.assertEqual(find(result, name, endpoint="preservation", number=number)["value"], value)
        for name, sham, interaction in (("K-C", -.25, .5), ("K-B", -.5, 1)):
            self.assertEqual(find(result, name, "sham")["value"], sham)
            self.assertEqual(find(result, name + "_corr", "revision_minus_sham")["value"], interaction)
            self.assertEqual(find(result, name + "_corr", "revision_minus_sham", "final_joint")["value"], 0)
            self.assertEqual(find(result, name, "sham", "preservation")["value"], sham)
            self.assertEqual(find(result, name + "_corr", "revision_minus_sham", "preservation")["value"], interaction)
        for event in ("revision", "sham"):
            for number in (1, 2, 3, 4):
                for p in ("B", "C", "P_G", "P_H"):
                    find(result, "cell_" + p, event, "accuracy", number)
                mean = find(result, "mixed_mean", event, "accuracy", number)
                cells = [find(result, "cell_" + p, event, "accuracy", number)["value"] for p in ("P_G", "P_H")]
                self.assertEqual(mean["value"], sum(cells) / 2)

    def test_six_receipt_cells_eta_direct_effects_and_representation_signs(self):
        result = self.run_case({("revision", p, 0): constant(v) for p, v in (
            ("B", [1, 0, 0, 0]), ("C", [1, 1, 0, 0]), ("K", [1, 1, 1, 0]),
            ("B_delta", [1, 1, 0, 0]), ("C_delta", [1, 0, 0, 0]), ("K_delta", [1, 1, 1, 1]))}, task=Task.PREFIX)
        for p, value in (("B", .25), ("C", .5), ("K", .75), ("B_delta", .5), ("C_delta", .25), ("K_delta", 1)):
            self.assertEqual(find(result, "receipt_cell_" + p, endpoint="accuracy", number=1)["value"], value)
        for name, value in (("eta", .5), ("B_delta-B", .25), ("C_delta-C", -.25), ("K_delta-K", .25),
                            ("B-C", -.25), ("B-K", -.5), ("B_delta-C_delta", .25), ("B_delta-K_delta", -.5)):
            self.assertEqual(find(result, name, endpoint="accuracy", number=1)["value"], value)
            find(result, name, endpoint="auc")
            find(result, name, endpoint="final_joint")
            find(result, name, endpoint="preservation")
            for number in (1, 2, 3, 4):
                find(result, name, endpoint="preservation", number=number)
        self.assertEqual(find(result, "eta")["value"], .5)
        self.assertEqual(find(result, "eta", endpoint="final_joint")["value"], 1)
        self.assertEqual(find(result, "eta", endpoint="accuracy", number=1)["range"], [-2, 2])
        # This fixed Prefix edit leaves eligible U only in peers 0,1,2.
        # The receipt gains in peer 3 contribute to exact accuracy, not U preservation.
        for name, value in (("eta", 1/3), ("B_delta-B", 1/3), ("C_delta-C", -1/3), ("K_delta-K", 0),
                            ("B-C", -1/3), ("B-K", -2/3), ("B_delta-C_delta", 1/3), ("B_delta-K_delta", -1/3)):
            self.assertEqual(find(result, name, endpoint="preservation")["value"], value)
            for number in (1, 2, 3, 4):
                self.assertEqual(find(result, name, endpoint="preservation", number=number)["value"], value)

    def test_receipt_equal_large_benefits_have_zero_eta(self):
        result = self.run_case({("revision", p, 0): constant(v) for p, v in (
            ("C", [0, 0, 0, 0]), ("K", [1, 0, 0, 0]),
            ("C_delta", [1, 1, 0, 0]), ("K_delta", [1, 1, 1, 0]))}, task=Task.SORT)
        self.assertEqual(find(result, "eta", endpoint="accuracy", number=1)["value"], 0)
        for name in ("C_delta-C", "K_delta-K"):
            self.assertEqual(find(result, name, endpoint="accuracy", number=1)["value"], .5)

    def test_prose_round_two_event_effects_trajectories_and_preservation(self):
        result = self.run_case({(event, p, 0): constant(v) for event, p, v in (
            ("revision", "B", [1, 0, 0, 0]), ("revision", "Q_B", [1, 1, 1, 0]),
            ("revision", "C", [1, 1, 0, 0]), ("revision", "Q_C", [0, 0, 0, 0]),
            ("sham", "B", [1, 0, 0, 0]), ("sham", "Q_B", [0, 0, 0, 0]),
            ("sham", "C", [1, 1, 0, 0]), ("sham", "Q_C", [1, 1, 1, 1]))}, task=Task.BFS)
        for event, name, expected in (("revision", "Q_B-B", .5), ("revision", "Q_C-C", -.5),
                                      ("sham", "Q_B-B", -.25), ("sham", "Q_C-C", .5)):
            self.assertEqual(find(result, name, event, "accuracy", 2)["value"], expected)
            self.assertEqual(find(result, name, event, "accuracy", 1)["value"], 0)
            self.assertEqual(find(result, name, event)["value"], .75 * expected)
            for number in (3, 4):
                self.assertEqual(find(result, name, event, "accuracy", number)["value"], expected)
                self.assertEqual(find(result, name, event, "preservation", number)["value"], expected)
            self.assertEqual(find(result, name, event, "preservation")["value"], .75 * expected)
        for event, name, expected in (("revision", "Q_B-B", 0), ("revision", "Q_C-C", 0),
                                    ("sham", "Q_B-B", 0), ("sham", "Q_C-C", 1)):
            self.assertEqual(find(result, name, event, "final_joint")["value"], expected)


class PopulationAndMissingnessTests(unittest.TestCase):
    def test_fixed_subsets_overlapping_ids_and_original_repeat_seeds(self):
        worlds = prepared("target")[0].main
        cohorts = {r["population"]: r for r in population_table(worlds)}
        for p, expected in (("main", 60), ("receipts", 24), ("prose_delay", 24), ("preserving", 16), ("repeat", 10)):
            self.assertEqual(len(cohorts[p]["world_ids"]), expected)
        overlap = set(cohorts["receipts"]["world_ids"]) & set(cohorts["prose_delay"]["world_ids"])
        self.assertEqual(len(overlap), 12)
        self.assertTrue(all("sort" in w for w in overlap))
        for world in cohorts["repeat"]["worlds"]:
            zero, one = world["continuation_seeds"]
            self.assertFalse(set(sum(zero, [])) & set(sum(one, [])))
            self.assertIn(0, world["partition"][0])
        fallback = prepared("fallback")[0].worlds(40)
        fallback_cohorts = {r["population"]: r for r in population_table(fallback)}
        for p, expected in (("main", 40), ("receipts", 16), ("prose_delay", 16), ("preserving", 16), ("repeat", 10)):
            self.assertEqual(len(fallback_cohorts[p]["world_ids"]), expected)

    def test_equal_five_family_weighting_rather_than_pooled_worlds(self):
        population = prepared("fallback")[0]
        worlds = [w for w in population.main if w.index == 3 or w.world.task is Task.TOP_K and w.index in (4, 5)]
        worlds, branches = selection(worlds=worlds)
        matrices = {(w.world_id, "revision", "C", 0): constant([1] * 4) for w in worlds if w.world.task is Task.TOP_K}
        result = analyze_estimands(worlds, branches, tables(worlds, branches, matrices))
        summary = next(r for r in result["summaries"] if r["estimand"] == "theta" and r["endpoint"] == "auc" and r["level"] == "all_families")
        self.assertEqual(summary["value"], .2)
        self.assertNotEqual(summary["value"], 3 / 7)
        self.assertEqual(sorted(summary["family_denominators"].values()), [1, 1, 1, 1, 3])

    def test_unknown_components_and_complete_cases_do_not_redefine_population(self):
        population = prepared("fallback")[0]
        worlds = [w for w in population.main if w.index in (3, 4)]
        worlds, branches = selection(worlds=worlds)
        matrices = {(w.world_id, "revision", "C", 0): constant([1] * 4) for w in worlds}
        matrices[worlds[0].world_id, "revision", "B", 0] = constant([None] * 4)
        result = analyze_estimands(worlds, branches, tables(worlds, branches, matrices))
        unknown = find(result, "theta", "revision_minus_sham", world=worlds[0].world_id)
        self.assertIsNone(unknown["value"])
        self.assertEqual(unknown["known_components"], 3)
        self.assertTrue(any(a["correct"] is None for c in unknown["components"] for a in c["atoms"]))
        summary = next(r for r in result["summaries"] if r["estimand"] == "theta" and r["endpoint"] == "auc" and r["level"] == "all_families")
        self.assertIsNone(summary["value"])
        self.assertEqual(summary["scheduled_worlds"], 10)
        self.assertEqual(summary["observed_worlds"], 9)
        self.assertEqual(summary["complete_case_description"]["value"], 1)

    def test_preservation_averages_peers_then_rounds_and_keeps_unknown_eligibility(self):
        worlds, branches = selection(Task.DIFFERENCE)
        data = tables(worlds, branches)
        for metric in data["peer_diagnostics"]:
            if metric["policy"] == "C" and metric["event"] == "revision":
                p = metric["peer"]
                metric.update(denominator=10 if p == 0 else 1 if p == 1 else 0,
                    numerator=9 if p == 0 else 0, rate=.9 if p == 0 else 0 if p == 1 else None,
                    eligible_coordinates=list(range(10)) if p == 0 else [0] if p == 1 else [])
        result = analyze_estimands(worlds, branches, data)
        component = find(result, "C-B", endpoint="preservation")["components"][0]
        self.assertEqual(component["value"], .45)
        self.assertEqual(component["unique_coordinate_count"], 10)
        self.assertEqual(component["peer_copy_count"], 11)
        self.assertEqual(component["eligible_peers"], 2)
        for metric in data["peer_diagnostics"]:
            if metric["policy"] == "C" and metric["event"] == "revision" and metric["peer"] == 0:
                metric.update(denominator=None, numerator=None, rate=None)
        result = analyze_estimands(worlds, branches, data)
        row = find(result, "C-B", endpoint="preservation")
        self.assertIsNone(row["value"])
        self.assertEqual(row["eligibility"], "unknown")
        self.assertEqual(row["reason"], "prefix_round_four_unknown")

    def test_empty_preservation_is_na_and_does_not_remove_main_outcomes(self):
        worlds, branches = selection(Task.DIFFERENCE)
        data = tables(worlds, branches)
        for metric in data["peer_diagnostics"]:
            metric.update(denominator=0, numerator=0, rate=None, eligible_coordinates=[])
        result = analyze_estimands(worlds, branches, data)
        self.assertEqual(find(result, "C-B", endpoint="preservation")["eligibility"], "ineligible")
        self.assertEqual(find(result, "theta", "revision_minus_sham")["value"], 0)

    def test_preserving_cells_and_companions_stay_on_fixed_eligible_worlds(self):
        for task in Task:
            for index in (3, 9):
                worlds, branches = selection(task, index)
                result = analyze_estimands(worlds, branches, tables(worlds, branches))
                rows = [r for r in result["world_contrasts"] if r["population"] == "preserving"]
                self.assertEqual(bool(rows), task in (Task.TOP_K, Task.BFS) and index <= 8)
                if rows:
                    for p in ("B", "C", "K"):
                        for endpoint in ("auc", "final_joint", "preservation"):
                            find(result, "preserving_cell_" + p, "preserving", endpoint)
        worlds, branches = selection(Task.TOP_K, 3)
        data = tables(worlds, branches, {(worlds[0].world_id, "preserving", p, 0): correct_rounds(n)
            for p, n in (("B", 2), ("C", 4), ("K", 3))})
        result = analyze_estimands(worlds, branches, data)
        for p, mean, final in (("B", .5, 0), ("C", 1, 1), ("K", .75, 0)):
            self.assertEqual(find(result, "preserving_cell_" + p, "preserving")["value"], mean)
            self.assertEqual(find(result, "preserving_cell_" + p, "preserving", "preservation")["value"], mean)
            self.assertEqual(find(result, "preserving_cell_" + p, "preserving", "final_joint")["value"], final)
            self.assertEqual(find(result, "preserving_cell_" + p, "preserving", "preservation", 4)["value"], final)

    def test_missing_sibling_and_missing_family_are_explicit(self):
        worlds, branches = selection(Task.DIFFERENCE)
        branches = tuple(b for b in branches if b.policy not in ("K",))
        result = analyze_estimands(worlds, branches, tables(worlds, branches))
        row = find(result, "K-C")
        self.assertIsNone(row["value"])
        self.assertEqual(row["components"][0]["reason"], "branch_not_in_supplied_schedule")
        summary = next(r for r in result["summaries"] if r["estimand"] == "theta" and r["endpoint"] == "auc" and r["level"] == "all_families")
        self.assertIsNone(summary["value"])
        self.assertEqual(len(summary["missing_families"]), 4)

    def test_unexecuted_logical_replay_retains_parent_identity_and_unknown_value(self):
        worlds, branches = selection(Task.DIFFERENCE)
        data = tables(worlds, branches, {(worlds[0].world_id, "revision", "B", 0): constant([1] * 4)})
        child = next(r for r in data["outcomes"] if r["policy"] == "P_G" and r["event"] == "revision" and r["round"] == 1
                     and r["peer"] in worlds[0].partition[1])
        child.update(correct=None, protocol_outcome="unknown")
        result = analyze_estimands(worlds, branches, data)
        row = find(result, "E_keep", endpoint="accuracy", number=1)
        self.assertIsNone(row["value"])
        atom = next(a for c in row["components"] for a in c["atoms"] if a["call_id"] == child["call_id"])
        self.assertEqual(atom["generation_id"], child["replay_parent"])
        self.assertIsNone(atom["correct"])

    def test_duplicate_drifted_or_incomplete_tables_fail(self):
        worlds, branches = selection(Task.DIFFERENCE)
        original = tables(worlds, branches)
        mutations = [lambda d: d["outcomes"].append(d["outcomes"][0]), lambda d: d["outcomes"].pop(),
            lambda d: d["outcomes"][0].update(seed=-1), lambda d: d["outcomes"][0].update(correct=True),
            lambda d: d["outcomes"][0].update(prefix_call_id="another-prefix"),
            lambda d: d["outcomes"][0].update(family=Task.SORT.value),
            lambda d: d["peer_diagnostics"][0].update(branch_id="another-branch"),
            lambda d: d["peer_diagnostics"].clear(), lambda d: d["peer_diagnostics"].append(d["peer_diagnostics"][0])]
        for mutate in mutations:
            data = copy.deepcopy(original)
            mutate(data)
            with self.assertRaises(ValueError):
                analyze_estimands(worlds, branches, data)


class RepeatabilityTests(unittest.TestCase):
    def test_exact_ties_are_distinct_from_strict_sign_reversals(self):
        def row(n):
            return {"value": float(n), "exact": {"numerator": n.numerator, "denominator": n.denominator}}
        for left, right, expected in ((0, 0, "both_ties"), (0, 1, "replicate_zero_tie"),
                (-1, 0, "replicate_one_tie"), (1, -1, "sign_reversal"), (-1, 1, "sign_reversal"), (1, 2, "same_sign")):
            self.assertEqual(compare_replicates(row(Fraction(left)), row(Fraction(right)))["classification"], expected)
        self.assertEqual(compare_replicates(row(Fraction(1, 3)), row(Fraction(1, 3)))["exact_difference"], {"numerator": 0, "denominator": 1})
        self.assertEqual(compare_replicates(row(Fraction(0)), {"value": None, "exact": None})["classification"], "unknown")

    def test_replicate_zero_unchanged_and_no_receipt_q_or_new_world_repeats(self):
        worlds, branches = selection(Task.SORT, 1)
        before = analyze_estimands(worlds, branches, tables(worlds, branches))
        data = tables(worlds, branches, {(worlds[0].world_id, "revision", "C", 1): constant([1] * 4)})
        after = analyze_estimands(worlds, branches, data)
        self.assertEqual(before["world_contrasts"], after["world_contrasts"])
        self.assertEqual(before["summaries"], after["summaries"])
        self.assertTrue(all(r["replicate"] == 0 for r in after["world_contrasts"]))
        self.assertTrue(all(r["replicate"] == 1 for r in after["repeat_contrasts"]))
        self.assertFalse(any(r["population"] != "main" for r in after["repeat_contrasts"]))
        self.assertEqual({r["world_id"] for r in after["repeatability"]}, {worlds[0].world_id})
        theta = next(r for r in after["repeatability"] if r["estimand"] == "theta" and r["endpoint"] == "auc")
        self.assertEqual(theta["classification"], "replicate_zero_tie")
        self.assertEqual(theta["replicate_zero"], 0)
        self.assertEqual(theta["replicate_one"], 1)

    def test_trajectory_category_changes_and_incomplete_pairs(self):
        worlds, branches = selection(Task.DIFFERENCE, 1)
        data = tables(worlds, branches, {(worlds[0].world_id, "revision", "B", 0): correct_rounds(4),
            (worlds[0].world_id, "revision", "B", 1): correct_rounds(1)})
        for row in data["trajectories"]:
            row.update(category="stale_export", complete=False)
        result = analyze_estimands(worlds, branches, data)
        change = next(r for r in result["trajectory_changes"] if r["event"] == "revision" and r["policy"] == "B")
        self.assertEqual(change["replicate_zero_category"], "continuously_correct")
        self.assertEqual(change["replicate_one_category"], "temporarily_correct_but_incorrect_at_end")
        self.assertTrue(change["category_changed"])
        data = tables(worlds, branches, {(worlds[0].world_id, "revision", "B", 1): constant([None] * 4)})
        result = analyze_estimands(worlds, branches, data)
        change = next(r for r in result["trajectory_changes"] if r["event"] == "revision" and r["policy"] == "B")
        self.assertIsNone(change["category_changed"])
        self.assertFalse(change["complete_pair"])

    def test_analysis_imports_no_runtime_or_statistics_dependencies(self):
        script = '''
import importlib.abc, sys
blocked = {"torch", "transformers", "pydantic", "langgraph", "langchain", "numpy", "scipy", "pandas", "matplotlib"}
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in blocked or fullname in {"recovery.runner", "recovery.protocol", "recovery.replay"}:
            raise AssertionError(fullname)
sys.meta_path.insert(0, Block())
import recovery.analysis
'''
        result = subprocess.run([sys.executable, "-S", "-c", script], cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
