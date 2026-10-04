"""CPU research probes only: no model, production runtime, or old-file mutation.

Constructive examples use the PS's 32-record / four-peer output assignments.
They test information carried by specified retained representations, not LLM
ability or prevalence in naturally generated collaborative prefixes.
"""
from collections import Counter, deque
from itertools import accumulate, product
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def outputs(task, x):
    if task == "prefix":
        y = list(accumulate(x))
    elif task == "difference":
        y = [b-a for a, b in zip(x, x[1:])]
    elif task == "sort":
        y = sorted(x)
    elif task == "max":
        return [max(x)] * 4
    elif task == "topk":
        return [sorted(x, reverse=True)[:10]] * 4
    else:
        raise ValueError(task)
    return [y[8*p:8*p+8] for p in range(4)] if task in {"prefix", "sort"} else [y] * 4


def array_pair(name, task, left, right, position, replacement, peer):
    before = [outputs(task, x)[peer] for x in (left, right)]
    after_arrays = [x[:position] + [replacement] + x[position+1:] for x in (left, right)]
    own = [x[8*peer:8*peer+8] for x in after_arrays]
    after = [outputs(task, x)[peer] for x in after_arrays]
    assert len(left) == len(right) == 32
    assert before[0] == before[1] and own[0] == own[1] and after[0] != after[1]
    return {
        "name": name, "task": task, "peer": peer,
        "worlds": [left, right], "old_candidate_identical": before[0],
        "current_private_shard_identical": own[0],
        "public_replacement_identical": {"record_position": position, "new_value": replacement},
        "old_values": [left[position], right[position]],
        "new_candidates_differ": after,
        "raw_remote_sources_held": [],
        "meaning": "Same candidate-only retained view, different required new answers; no universally correct update from this view alone."
    }


def distances(edges):
    adj = {i: set() for i in range(12)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    out = [-1] * 12
    out[0] = 0
    q = deque([0])
    while q:
        a = q.popleft()
        for b in sorted(adj[a]):
            if out[b] < 0:
                out[b] = out[a] + 1
                q.append(b)
    return out


def graph_pair():
    tree = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6),
            (5, 7), (6, 8), (7, 9), (8, 10), (9, 11)]
    extra = [(1, 2), (3, 4), (5, 6), (7, 8)]
    left, right = tree + extra + [(2, 3)], tree + extra + [(1, 4)]
    own = [(5, 7), (6, 8), (7, 9), (8, 10)]
    deleted = (0, 1)
    before = [distances(e) for e in (left, right)]
    after = [distances([e for e in es if e != deleted]) for es in (left, right)]
    assert before[0] == before[1] and after[0] != after[1]
    assert all(after[i] != before[i] for i in range(2))
    assert all(set(own) <= set(e) and len(e) == 16 for e in (left, right))
    return {"name": "bfs_old_distances_and_deleted_edge_not_sufficient",
            "worlds": [left, right], "old_candidate_identical": before[0],
            "current_private_edges_identical": own, "deleted_edge_identical": deleted,
            "new_candidates_differ": after, "both_events_answer_changing": True}


def aggregate_only_history_pair(task, left, right, peer, replacement):
    """A contract-shaped scripted trace, not a naturally sampled model prefix.

    Round one exchanges sum or sorted-shard prose without raw source refs;
    round two has enough information for exact answers. Source order/identity
    within a remote shard was intentionally not communicated.
    """
    views = []
    for x in (left, right):
        shards = [x[8*p:8*p+8] for p in range(4)]
        messages = [str(sum(s)) if task == "prefix" else json.dumps(sorted(s)) for s in shards]
        own_reply = {"candidate": [0]*8,
                     "send": [{"to": p, "text": messages[peer]} for p in range(4) if p != peer]}
        histories = [{"round": 1, "own_reply": own_reply}]
        histories.append({"before_round": 2,
                          "received_prose": [{"from": p, "text": messages[p]} for p in range(4) if p != peer]})
        for r in range(2, 5):
            histories.append({"round": r, "own_reply": {"candidate": outputs(task, x)[peer], "send": []}})
        current_table = [{"id": i, "owner": i//8, "version": 1, "value": x[i]}
                         for i in range(8*peer, 8*peer+8)]
        current_table.append({"id": 0, "owner": 0, "version": 2, "value": replacement})
        views.append({"peer": peer, "task": task, "current_source_table": current_table,
                      "history": histories, "notice": {"changed_record": 0, "owner": 0, "version": 2}})
    assert views[0] == views[1]
    after = []
    for x in (left, right):
        y = x.copy()
        y[0] = replacement
        after.append(outputs(task, y)[peer])
    assert after[0] != after[1]
    recovered = []
    # Mathematical sufficiency check only: compute from the retained view plus
    # receipt. This deterministic updater is NOT supplied to model conditions.
    for x in (left, right):
        view = views[0]
        if task == "prefix":
            old_own = view["history"][-1]["own_reply"]["candidate"]
            new_own = [value + replacement-x[0] for value in old_own]
        else:
            own_summary = view["history"][0]["own_reply"]["send"][0]["text"]
            all_values = json.loads(own_summary)
            for msg in view["history"][1]["received_prose"]:
                all_values.extend(json.loads(msg["text"]))
            all_values.remove(x[0])
            all_values.append(replacement)
            new_own = sorted(all_values)[8*peer:8*peer+8]
        recovered.append(new_own)
    assert recovered == after
    return {"task": task, "identical_full_B_boundary_view": views[0],
            "different_required_new_outputs": after,
            "new_outputs_computed_from_common_view_plus_historical_before_value": recovered,
            "limits": "Scripted legal information flow, no LLM sampling or tokenizer execution; not natural frequency evidence."}


def delta_transport_checks():
    count = 0
    # Exhaustive small arrays verify mathematical identities, not PS world frequency.
    for x in product(range(1, 4), repeat=6):
        x = list(x)
        old_prefix = list(accumulate(x))
        old_diff = [b-a for a, b in zip(x, x[1:])]
        old_sort = sorted(x)
        for j in range(6):
            for new in range(1, 4):
                if new == x[j]:
                    continue
                delta = new-x[j]
                changed = x.copy()
                changed[j] = new
                assert [v + (delta if k >= j else 0) for k, v in enumerate(old_prefix)] == list(accumulate(changed))
                repaired = old_diff.copy()
                if j:
                    repaired[j-1] += delta
                if j < 5:
                    repaired[j] -= delta
                assert repaired == [b-a for a, b in zip(changed, changed[1:])]
                repaired = old_sort.copy()
                repaired.remove(x[j])
                repaired.append(new)
                assert sorted(repaired) == sorted(changed)
                # Correct complete differences + one unchanged current anchor
                # reconstruct the old array and hence the unavailable old value.
                anchor = (j+1) % 6
                offset = changed[anchor] - sum(old_diff[:anchor])
                reconstructed = [offset] + [offset+s for s in accumulate(old_diff)]
                assert reconstructed == x
                count += 1
    return {"exhaustive_cases": count, "identities_passed": [
        "prefix update with old/new delta", "difference update with old/new delta",
        "complete sorted multiset update with old/new values",
        "correct full difference output plus unchanged current anchor recovers old values"],
        "limitation": "Correct old outputs assumed; host does not perform these updates for agents."}


def cone(schedule, owner=0):
    # A generated message may depend on every already visible input. The next
    # round sees committed messages; round-four deliveries enter final history.
    exposed = {owner}
    history = []
    for edges in schedule:
        before = set(exposed)
        exposed |= {recipient for sender, recipient in edges if sender in before}
        history.append(sorted(exposed))
    return history


def exposure_checks():
    early = [[(0, 1)], [(1, 2)], [], []]
    late = [[(1, 2)], [(0, 1)], [], []]
    assert set(sum(early, [])) == set(sum(late, []))
    assert cone(early)[-1] == [0, 1, 2] and cone(late)[-1] == [0, 1]
    # Enumerate fixed routings in which each peer sends to at most one other
    # peer per round. This is a combinatorial probe, NOT an agent distribution.
    options = [[None] + [j for j in range(4) if j != i] for i in range(4)]
    hist = Counter()
    for targets in product(*options):
        edges = [(i, j) for i, j in enumerate(targets) if j is not None]
        hist[len(cone([edges]*4)[-1])] += 1
    complete = [(i, j) for i in range(4) for j in range(4) if i != j]
    assert cone([complete]*4)[0] == [0, 1, 2, 3]
    return {"same_static_graph_different_temporal_cones": {"early": cone(early), "late": cone(late)},
            "four_round_static_one_recipient_routing_count": 256,
            "boundary_exposed_peer_histogram": dict(sorted(hist.items())),
            "all_to_all_after_first_delivery": cone([complete]*4)[0],
            "limits": "Potential exposure, not actual semantic dependence; routing population artificial."}


def old_audit_check():
    report = json.loads((ROOT / "research/03_innovation_review/evidence/audit_results.json").read_text(encoding="utf-8"))
    source_mismatch = [r["path"] for r in report["source_manifest"]
                       if hashlib.sha256((ROOT/r["path"]).read_bytes()).hexdigest() != r["sha256"]]
    case_mismatch = [r["file"] for r in report["case_results"]
                    if hashlib.sha256((ROOT/"acl26-silo-bench/benchmarks"/r["file"]).read_bytes()).hexdigest() != r["sha256"]]
    assert not source_mismatch and not case_mismatch
    return {"all_prior_json_records_parsed": True, "source_records": len(report["source_manifest"]),
            "case_records": len(report["case_results"]), "source_hash_mismatches": source_mismatch,
            "case_hash_mismatches": case_mismatch,
            "prior_summary_read_not_newly_reproduced": report["summary"]}


def main():
    pairs = []
    a = [1, 3] + [2]*30
    b = [3, 1] + [2]*30
    pairs.append(array_pair("prefix_missing_before_value", "prefix", a, b, 0, 4, 3))
    a = [10, 20] + [0]*8 + [30]*22
    b = [20, 10] + [0]*8 + [30]*22
    pairs.append(array_pair("sort_record_identity_lost", "sort", a, b, 0, 40, 1))
    a = [10, 30] + [0]*8 + [20]*7 + [40]*15
    b = [10, 31] + [0]*8 + [20]*7 + [40]*15
    pairs.append(array_pair("sort_local_boundary_missing_even_with_delta", "sort", a, b, 0, 50, 1))
    a = [99, 98] + [20]*30
    b = [99, 97] + [20]*30
    pairs.append(array_pair("max_missing_reserve_even_with_delta", "max", a, b, 0, 0, 3))
    a = list(range(99, 89, -1)) + [89] + [20]*21
    b = list(range(99, 89, -1)) + [88] + [20]*21
    pairs.append(array_pair("topk_missing_reserve_even_with_delta", "topk", a, b, 0, 0, 3))
    histories = [aggregate_only_history_pair("prefix", [1, 3]+[2]*30, [3, 1]+[2]*30, 3, 4),
                 aggregate_only_history_pair("sort", [10, 20]+[0]*8+[30]*22,
                                             [20, 10]+[0]*8+[30]*22, 1, 40)]
    result = {"status": "all deterministic assertions passed", "array_information_witnesses": pairs,
              "scripted_full_B_history_witnesses": histories,
              "graph_information_witness": graph_pair(), "delta_transport": delta_transport_checks(),
              "exposure": exposure_checks(), "prior_audit_integrity": old_audit_check(),
              "spec_sha256": hashlib.sha256((ROOT/"PROJECT_SPECIFICATION.md").read_bytes()).hexdigest().upper(),
              "claim_boundary": "CPU constructions/identities only; no inference, novelty certificate, or natural failure rate."}
    target = Path(__file__).with_name("protocol_probe_results.json")
    target.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("status", "delta_transport", "exposure", "prior_audit_integrity", "spec_sha256")}, indent=2))


if __name__ == "__main__":
    main()
