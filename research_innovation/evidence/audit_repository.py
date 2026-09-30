"""CPU-only audit of supplied SILO data and native protocol/metric functions.

Run from any cwd. Writes only research_innovation/evidence/audit_results.json.
Does not call an LLM or edit the specification or benchmark checkout.
Protocol functions use the native implementation with a standard-library JSON
persistence shim because srsly is not installed; this limitation is explicit.
"""
from __future__ import annotations

import ast
from collections import Counter, deque
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import re
import statistics
import sys
import tempfile
import types
import zipfile

# Keep CPU inspection from generating new bytecode caches in the audited tree.
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT / "acl26-silo-bench"
EVIDENCE = Path(__file__).resolve().parent


def canonical(value):
    """Match JSON representations, including tuple/list and int/string dict keys."""
    return json.loads(json.dumps(value))


def independent_answer(case):
    shards = [a["input_shard"] for a in case["agent_configs"]]
    n = len(shards)
    task = int(case["case_id"].split("-")[1])
    segmented = task in {11, 14, 20, 21}
    flat = list(itertools.chain.from_iterable(shards))
    if task == 1:
        answer = max(flat)
    elif task == 2:
        answer = Counter(flat)["apple"]
    elif task == 3:
        counts = Counter(flat)
        answer = min(counts, key=lambda c: (-counts[c], c))
    elif task == 4:
        answer = any("ERROR" in s for s in flat)
    elif task == 5:
        answer = len([v for v in flat if 100 <= v <= 500])
    elif task == 6:
        answer = 0
        for value in flat:
            answer ^= value
    elif task == 7:
        answer = round(statistics.mean(flat), 2)
    elif task in {8, 26}:
        answer = len(set(flat))
    elif task == 9:
        answer = sorted(flat)[-10:][::-1]
    elif task == 10:
        answer = round(statistics.pstdev(flat), 2)
    elif task == 11:
        answer = list(itertools.accumulate(flat))
    elif task == 12:
        answer = [round(sum(window) / 3, 2) for window in zip(flat, flat[1:], flat[2:])]
    elif task == 13:
        text = "".join(shards)
        answer = 0
        for center in range(2 * len(text) - 1):
            left, right = center // 2, (center + 1) // 2
            while left >= 0 and right < len(text) and text[left] == text[right]:
                answer = max(answer, right - left + 1)
                left -= 1
                right += 1
    elif task == 14:
        answer = flat
        for _ in range(5):
            padded = [0] + answer + [0]
            answer = [int(sum(padded[j:j+3]) == 1) for j in range(len(answer))]
    elif task == 15:
        answer, state = 0, 0
        for char in "".join(shards):
            if char == "ABC"[state]:
                state += 1
                if state == 3:
                    answer += 1
                    state = 0
    elif task == 16:
        lefts = list(itertools.accumulate(flat, max))
        rights = list(itertools.accumulate(reversed(flat), max))[::-1]
        answer = sum(min(l, r) - h for l, r, h in zip(lefts, rights, flat))
    elif task == 17:
        answer = [b-a for a, b in itertools.pairwise(flat)]
    elif task == 18:
        pointers = {record["id"]: record["next"] for record in flat}
        heads = set(pointers) - set(pointers.values())
        assert len(heads) == 1
        current = heads.pop()
        answer = {}
        while current != -1:
            assert current not in answer
            answer[current] = len(answer)
            current = pointers[current]
        assert len(answer) == len(pointers)
    elif task == 19:
        answer = [key for key, _ in itertools.groupby(flat)]
    elif task == 20:
        value = 0
        answer = []
        for block in flat:
            value = ((sum(map(ord, block)) % 10000) ^ value) % 10000
            answer.append(value)
    elif task == 21:
        answer = sorted(flat)
    elif task == 22:
        answer = sorted(flat)[len(flat) // 2]
    elif task in {23, 24}:
        size = n * (10 if task == 23 else 8)
        neighbors = {node: set() for node in range(size)}
        for a, b in flat:
            neighbors[a].add(b)
            neighbors[b].add(a)
        if task == 23:
            unseen = set(neighbors)
            answer = 0
            while unseen:
                todo = [unseen.pop()]
                answer += 1
                while todo:
                    node = todo.pop()
                    new = neighbors[node] & unseen
                    unseen -= new
                    todo.extend(new)
        else:
            answer = {node: -1 for node in neighbors}
            answer[0] = 0
            todo = deque([0])
            while todo:
                node = todo.popleft()
                for other in neighbors[node]:
                    if answer[other] == -1:
                        answer[other] = answer[node] + 1
                        todo.append(other)
    elif task == 25:
        line = case["task_description"].split("Initial centroids: ", 1)[1].splitlines()[0]
        centers = ast.literal_eval(line)
        groups = [[], [], []]
        for point in flat:
            winner = min(range(3), key=lambda k: sum((x-y)**2 for x, y in zip(point, centers[k])))
            groups[winner].append(point)
        answer = [[round(statistics.mean(p[dim] for p in group), 2) for dim in (0, 1)]
                  if group else [round(v, 2) for v in centers[k]]
                  for k, group in enumerate(groups)]
    elif task == 27:
        users, items = {}, {}
        for shard in shards:
            users.update({int(k): v for k, v in shard["users"].items()})
            items.update({int(k): v for k, v in shard["items"].items()})
        scores = [(u, i, round(sum(a*b for a, b in zip(users[u], items[i])), 4))
                  for u in sorted(users) for i in sorted(items)]
        answer = sorted(scores, key=lambda v: -v[2])[:3]
    elif task == 28:
        size = n * 8
        degree = Counter(a for a, b in flat)
        ranks = {node: (1-0.85)/size for node in range(size)}
        for a, b in flat:
            ranks[b] += 0.85 / size / degree[a]
        answer = {k: round(v, 6) for k, v in ranks.items()}
    elif task == 29:
        loads = [0]*n
        for record in sorted(flat, key=lambda t: (-t["duration"], t["id"])):
            destination = min(range(n), key=lambda i: (loads[i], i))
            loads[destination] += record["duration"]
        answer = {"variance": round(statistics.pvariance(loads), 2), "max_load": max(loads), "min_load": min(loads)}
    elif task == 30:
        b = shards[0]["B_matrix"]
        assert all(shard["B_matrix"] == b for shard in shards)
        rows = {i: row for shard in shards for i, row in zip(shard["A_row_indices"], shard["A_rows"])}
        columns = list(zip(*b))
        answer = [[sum(a*x for a, x in zip(rows[i], column)) for column in columns] for i in sorted(rows)]
    else:
        raise ValueError(task)
    if segmented:
        size = len(answer)//n
        per_agent = [answer[i*size:(i+1)*size] for i in range(n)]
    else:
        per_agent = [answer]*n
    return canonical(per_agent)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def protocol_checks():
    # No srsly installation or native engine/API calls: inject only JSON I/O.
    sys.path.insert(0, str(REPO))
    persistence = types.ModuleType("src.utils.persistence")
    persistence.read_json = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))

    def write_json(path, data):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    persistence.write_json = write_json
    sys.modules["src.utils.persistence"] = persistence
    from src.models import AgentState
    from src.msg import tools as p2p
    from src.broadcast import tools as broadcast
    from src.sfs import tools as sfs
    result = {"persistence_dependency": "standard-library JSON shim, native protocol functions unchanged"}
    with tempfile.TemporaryDirectory(prefix="silo_research_audit_") as temporary:
        case = Path(temporary)
        rounds = {r: case / "rounds" / f"round-{r:06d}" for r in range(5)}
        for path in rounds.values():
            path.mkdir(parents=True)
        sender = AgentState(agent_id=0)
        p2p.tool_send_message(0, 1, "v1-old", rounds[1], 1, sender, 2)
        msgfile = next((rounds[1]/"env"/"messages").glob("*.json"))
        before = persistence.read_json(msgfile)
        first = p2p.tool_receive_messages(1, case, 2, rounds[2])
        after = persistence.read_json(msgfile)
        second = p2p.tool_receive_messages(1, case, 2, rounds[2])
        result["p2p_historical_file_mutation"] = {
            "before_read": before["read"], "after_read": after["read"],
            "first_delivery_count": len(first["messages"]), "second_delivery_count": len(second["messages"])}
        broadcast.tool_broadcast_message(0, "old-broadcast", rounds[1], 1, sender)
        first = broadcast.tool_receive_messages(1, case, 2, rounds[2])
        # The engine does not copy last_received_round.json when no receive occurs in round 3.
        later = broadcast.tool_receive_messages(1, case, 4, rounds[4])
        result["broadcast_redelivery_after_skipped_receive"] = {
            "first_count": len(first["messages"]), "after_skip_count": len(later["messages"]),
            "same_payload": first["messages"] == later["messages"]}
        sfs.tool_write_file(rounds[2], 0, 2, "shared", "agent0", sender)
        reader = AgentState(agent_id=1)
        sfs.tool_write_file(rounds[2], 1, 2, "shared", "agent1", reader)
        result["sfs_last_writer_wins"] = sfs.tool_read_file(rounds[2], "shared")
        result["sfs_prior_round_read"] = sfs.tool_read_file(rounds[1], "shared")
        result["sfs_current_round_delete"] = sfs.tool_delete_file(rounds[2], "shared")
    return result


def main():
    metrics = load_module("silo_audit_metrics", REPO/"src"/"utils"/"metrics.py")
    paths = sorted((REPO/"benchmarks").glob("*_*n*.json"))
    rows = []
    stored = {}
    for path in paths:
        if not re.fullmatch(r"I{1,3}-\d+_n\d+\.json", path.name):
            continue
        raw = path.read_text(encoding="utf-8")
        case = json.loads(raw)
        n = case["metadata"]["num_agents"]
        gold = case["expected_output"]["per_agent_values"]
        submissions = [{"agent_id": i, "answer": value} for i, value in enumerate(gold)]
        level = case["case_id"].split("-")[0]
        row = {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
               "case_id": case["case_id"], "name": case["case_name"], "n": n,
               "agent_count_matches": len(case["agent_configs"]) == n == len(gold),
               "agent_ids_sequential": [a["agent_id"] for a in case["agent_configs"]] == list(range(n)),
               "agent_gold_matches": [a["expected_output"] for a in case["agent_configs"]] == gold,
               "segmented": case["metadata"]["is_segmented"],
               "unresolved_input_placeholder": any("{input_shard}" in a["user_prompt"] for a in case["agent_configs"]),
               "replacement_character_count": raw.count("\ufffd"),
               "native_exact_selfscore": metrics.compute_success_rate(submissions, case["expected_output"])}
        try:
            computed = independent_answer(case)
            row["independent_oracle_matches"] = computed == gold
            if case["case_id"] == "III-28":
                differences = [{"node": k, "independent": v, "stored": gold[0][k]}
                               for k, v in computed[0].items() if v != gold[0][k]]
                row["pagerank_rounding_differences"] = differences
                row["pagerank_max_absolute_difference"] = max((abs(d["independent"]-d["stored"]) for d in differences), default=0)
                # Supplemental reproduction of generator float-operation ordering,
                # kept separate from independent computation rather than hiding it.
                size = n * 8
                edges = [tuple(edge) for agent in case["agent_configs"] for edge in agent["input_shard"]]
                degree = Counter(a for a, b in edges)
                ranks = {node: (1-0.85)/size for node in range(size)}
                for a, b in sorted(edges):
                    ranks[b] += 0.85 * (1.0 / size) / degree[a]
                compatible = {str(k): round(v, 6) for k, v in ranks.items()}
                row["pagerank_generator_arithmetic_matches"] = compatible == gold[0]
        except Exception as exc:
            row["oracle_exception"] = f"{type(exc).__name__}: {exc}"
        try:
            row["native_partial_selfscore"] = metrics.compute_partial_correctness(submissions, case["expected_output"], level)
        except Exception as exc:
            row["partial_exception"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
        stored[(case["case_id"], n)] = case
    combined = json.loads((REPO/"benchmarks"/"silo_bench_full.json").read_text(encoding="utf-8"))
    summary = json.loads((REPO/"benchmarks"/"benchmark_summary.json").read_text(encoding="utf-8"))
    inventory = {"stored_case_count": len(rows), "tasks": len(set(row["case_id"] for row in rows)),
                 "agent_counts": sorted(set(row["n"] for row in rows)),
                 "combined_metadata": combined["metadata"],
                 "combined_cases_match_individual": all(case == stored[(case["case_id"], case["metadata"]["num_agents"])] for case in combined["cases"]),
                 "summary_num_agents": summary["num_agents"], "summary_total_cases": summary["total_cases"]}
    archives = []
    for path in sorted((REPO/"benchmarks").glob("*.zip")):
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                if name.endswith("/"):
                    continue
                local = path.parent/Path(name).name
                archived_raw = archive.read(name)
                archived = json.loads(archived_raw)
                current = json.loads(local.read_text(encoding="utf-8")) if local.exists() else None
                archives.append({"archive": path.name, "entry": name,
                                 "matches_uncompressed_bytes": local.exists() and archived_raw == local.read_bytes(),
                                 "matches_uncompressed_semantics": archived == current,
                                 "changed_top_level_keys": [k for k in archived if current and archived[k] != current.get(k)],
                                 "archived_first_shard_keys": list(archived["agent_configs"][0]["input_shard"]),
                                 "current_first_shard_keys": list(current["agent_configs"][0]["input_shard"]) if current else None,
                                 "archived_sha256": hashlib.sha256(archived_raw).hexdigest()})
    source_manifest = []
    for path in sorted(REPO.rglob("*")):
        if path.is_file() and path.suffix in {".py", ".md", ".toml", ".yaml", ".sh"}:
            raw = path.read_bytes()
            source_manifest.append({"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(),
                                    "lines": len(raw.splitlines())})
    result = {"spec_sha256": hashlib.sha256((ROOT/"PROJECT_SPECIFICATION.md").read_bytes()).hexdigest().upper(),
              "python": sys.version, "inventory": inventory, "archives": archives,
              "summary": {"oracle_matches": sum(row.get("independent_oracle_matches") is True for row in rows),
                          "oracle_mismatches": [row["file"] for row in rows if row.get("independent_oracle_matches") is False],
                          "oracle_errors": [row for row in rows if "oracle_exception" in row],
                          "exact_selfscores_one": sum(row["native_exact_selfscore"] == 1 for row in rows),
                          "partial_errors": sum("partial_exception" in row for row in rows),
                          "partial_undercredit": sum(row.get("native_partial_selfscore", 1) < 1 for row in rows)},
              "protocol_checks": protocol_checks(), "case_results": rows, "source_manifest": source_manifest}
    (EVIDENCE/"audit_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("spec_sha256", "inventory", "archives", "summary", "protocol_checks")}, indent=2))


if __name__ == "__main__":
    main()
