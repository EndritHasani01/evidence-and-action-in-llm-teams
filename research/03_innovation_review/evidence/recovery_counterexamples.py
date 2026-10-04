"""Three deterministic counterexamples; no inference and no benchmark mutation."""
from collections import deque
import json
from pathlib import Path


def shortest(edges, start, goal):
    neighbors = {}
    for a, b in edges:
        neighbors.setdefault(a, set()).add(b)
        neighbors.setdefault(b, set()).add(a)
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        node, depth = queue.popleft()
        if node == goal:
            return depth
        for other in neighbors.get(node, set()) - seen:
            seen.add(other)
            queue.append((other, depth + 1))
    return None


def path_feasible(path, edges):
    return all((a, b) in edges or (b, a) in edges for a, b in zip(path, path[1:]))


def main():
    # Historical proof expires, proposition survives via independent current proof.
    before = {("s", "a"), ("a", "t"), ("s", "b"), ("b", "t")}
    after = before - {("a", "t")}
    old_witness = ["s", "a", "t"]
    alternate = ["s", "b", "t"]
    first = {
        "name": "expired_support_with_surviving_result",
        "old_witness_currently_valid": path_feasible(old_witness, after),
        "old_distance": shortest(before, "s", "t"),
        "new_distance": shortest(after, "s", "t"),
        "alternate_witness_currently_valid": path_feasible(alternate, after),
    }
    assert first == {"name": "expired_support_with_surviving_result", "old_witness_currently_valid": False,
                     "old_distance": 2, "new_distance": 2, "alternate_witness_currently_valid": True}

    # Every historical edge remains, yet insertion changes optimality.
    before = {("s", "a"), ("a", "b"), ("b", "t")}
    after = before | {("s", "t")}
    old_witness = ["s", "a", "b", "t"]
    second = {
        "name": "feasibility_survives_but_optimality_expires",
        "all_historical_edge_dependencies_unchanged": before <= after,
        "old_path_currently_feasible": path_feasible(old_witness, after),
        "old_distance": shortest(before, "s", "t"),
        "new_distance": shortest(after, "s", "t"),
        "need_current_edge_domain_coverage": True,
    }
    assert second["old_path_currently_feasible"] and second["old_distance"] == 3 and second["new_distance"] == 1

    # Updating a selected item lowers the threshold; untouched rejected work matters.
    before = {"A": 10, "B": 9, "C": 8, "D": 2}
    after = dict(before, A=6)
    top = lambda values: sorted(values, key=lambda key: (-values[key], key))[:2]
    old_selected = top(before)
    repaired_selected_only = sorted(old_selected, key=lambda key: -after[key])
    third = {
        "name": "old_pruning_threshold_expires",
        "before_top2": old_selected,
        "after_top2": top(after),
        "repair_selected_only": repaired_selected_only,
        "all_repaired_items_and_scores_currently_valid": all(key in after for key in repaired_selected_only),
        "retained_positive_B_unchanged": before["B"] == after["B"],
        "previously_pruned_C_unchanged": before["C"] == after["C"],
        "pruning_witness": {"old_cutoff": 9, "C_score": 8},
        "missed_new_winner": list(set(top(after)) - set(repaired_selected_only)),
    }
    assert third["before_top2"] == ["A", "B"] and third["after_top2"] == ["B", "C"]
    assert third["repair_selected_only"] == ["B", "A"] and third["missed_new_winner"] == ["C"]
    results = {"status": "3 deterministic counterexamples passed", "claims": [first, second, third],
               "limits": "Constructed mathematical cases; no evidence of LLM prevalence, benefit, or novelty."}
    destination = Path(__file__).with_name("counterexample_results.json")
    destination.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
