"""Small independent specified-view atlas witnesses; no archive imports/writes."""


def prefixes(values):
    return [sum(values[:j + 1]) for j in range(len(values))]


def distances(edges):
    # Synchronous relaxation, independent of the production BFS queue solver.
    d = [0, 99, 99, 99]
    for _ in range(4):
        following = d[:]
        for a, b in edges:
            following[a], following[b] = min(following[a], d[b] + 1), min(following[b], d[a] + 1)
        d = following
    return [v if v < 99 else -1 for v in d]


def examples():
    rows = []
    for family, a, b, retained, revised in (
        ("maximum_cpu_only", [9, 8, 1], [9, 7, 1], lambda v: max(v), lambda v: max([2] + v[1:])),
        ("top_k", list(range(99, 89, -1)) + [89], list(range(99, 89, -1)) + [88],
         lambda v: sorted(v, reverse=True)[:10], lambda v: sorted([0] + v[1:], reverse=True)[:10]),
        ("prefix_sum", [1, 4, 5, 3], [2, 3, 5, 3], lambda v: prefixes(v)[2:],
         lambda v: prefixes([v[0], 1, *v[2:]])[2:]),
        ("distributed_sort", [1, 2, 4, 5, 6, 9], [1, 2, 4, 5, 7, 9], lambda v: sorted(v)[2:4],
         lambda v: sorted([v[0], v[1], 8, *v[3:]])[2:4]),
        ("bfs_distance", [(0, 1), (0, 2), (1, 3), (2, 3)], [(0, 1), (0, 2), (1, 3), (1, 2)],
         distances, lambda v: distances([e for e in v if e != (1, 3)])),
    ):
        assert retained(a) == retained(b) and revised(a) != revised(b)
        rows.append({"family": family, "kind": "specified_view_ambiguity", "world_a": a, "world_b": b,
            "same_correct_old_summary": retained(a), "new_a": revised(a), "new_b": revised(b),
            "information_view": {"maximum_cpu_only": "Old winning value; winner 9 demoted to 2",
                "top_k": "Old ten selected values; winner 99 demoted to 0; no reserve",
                "prefix_sum": "Old local coordinates 2,3; same local raw 5,3; k=1 after-only value 1",
                "distributed_sort": "Old local ranks 2,3; value 4 replaced with 8; no remote boundaries",
                "bfs_distance": "Old node labels 0..3 and deleted edge (1,3); no alternative topology"}[family],
            "correctness_assumption": "The retained old summary is exactly correct in both synthetic worlds",
            "limit": "These views omit other evidence; further communication can resolve ambiguity."})
    old, diffs, anchor = [5, 8, 7, 11], [3, -1, 4], 5
    reconstructed = [anchor + sum(diffs[:j]) for j in range(4)]
    assert reconstructed == old
    shifted = [v + 1 for v in old]
    assert [shifted[j] - shifted[j - 1] for j in range(1, 4)] == diffs
    rows.append({"family": "difference_array", "kind": "sufficiency_with_anchor",
        "information_view": "Complete old differences plus unchanged x0=5; edited k=2 becomes 9",
        "correctness_assumption": "Correct old differences and unchanged genuine anchor",
        "differences": diffs, "anchor": anchor, "reconstructed": reconstructed,
        "same_differences_without_anchor": shifted, "new_differences": [3, 1, 2]})
    # Positive sufficiency companions use the historical operand/full multiset,
    # rather than assuming that an actual submitted candidate is correct.
    rows[2]["with_genuine_before_a"] = [v + (1 - 4) for v in rows[2]["same_correct_old_summary"]]
    rows[2]["with_genuine_before_b"] = [v + (1 - 3) for v in rows[2]["same_correct_old_summary"]]
    assert rows[2]["with_genuine_before_a"] == rows[2]["new_a"]
    assert rows[2]["with_genuine_before_b"] == rows[2]["new_b"]
    for label in ("a", "b"):
        multiset = rows[3]["world_" + label][:]
        multiset.remove(4)
        multiset.append(8)
        assert sorted(multiset)[2:4] == rows[3]["new_" + label]
    return rows
