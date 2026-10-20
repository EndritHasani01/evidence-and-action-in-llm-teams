"""Recompute reported outcomes and effort from canonical records; standard library only."""
import argparse
from collections import Counter
import csv
import json
import random

from evidence import ROOT, checkpoints, derived_destination, read_checkpoint


def bootstrap(rows, field, seed, final):
    strata = {}
    ordered = sorted(rows, key=lambda r: (r["owner"], r["first"], r["world"])) if final else rows
    for row in ordered:
        strata.setdefault((row["owner"], row["first"]), []).append(row[f"clear_{field}"] - row[f"retain_{field}"])
    rng = random.Random(seed)
    draws = sorted(sum(rng.choice(group) for group in strata.values() for _ in group) / len(rows)
                   for _ in range(10000))
    return {"mean": sum(sum(group) for group in strata.values()) / len(rows),
            "low": draws[250], "high": draws[9750], "seed": seed, "draws": 10000}


def reconstruct(name, directory):
    run, calls, episodes, attempts = read_checkpoint(directory)
    if any(outcome["outcome"] is None for outcome in calls.values()):
        raise ValueError("An unresolved outcome requires explicit missingness handling")
    if any(status != "completed" or number != 1 for _, status, number in attempts):
        raise ValueError("Unexpected retry or incomplete attempt in this fixed release")
    rows, ledger = [], []
    stats = {phase: Counter() for phase in ("prefix", "retain", "clear")}
    for world in run["worlds"]:
        old = max(sum(world["original"], []))
        revised = max(sum(world["revised"], []))
        assert old == world["original_truth"] and revised == world["revised_truth"] < old
        assert [(a, i) for a in range(2) for i in range(20)
                if world["original"][a][i] != world["revised"][a][i]] == [(world["owner"], world["row"])]
        if world["group"] != "main":
            continue
        row = {"world": world["id"], "owner": world["owner"], "first": world["first"], "old_maximum": old, "revised_maximum": revised}
        for phase in stats:
            episode = episodes[world["id"] + "/" + phase]
            assert episode["terminal"]
            target = old if phase == "prefix" else revised
            events = episode["events"]
            outcomes = [calls[event["call"]]["outcome"] for event in events]
            success = int(episode["submissions"] == [target, target])
            counter = stats[phase]
            counter["success"] += success
            counter["both_submitted"] += all(value is not None for value in episode["submissions"])
            counter["calls"] += len(events)
            illegal = sum(event["error"] is not None for event in events)
            counter["illegal"] += illegal
            counter["legal_failed_episodes"] += int(not success and illegal == 0)
            for value in episode["submissions"]:
                counter["absent" if value is None else "correct" if value == target else "wrong"] += 1
            for agent in range(2):
                messages = [event["action"]["message"] for event in events
                            if event["agent"] == agent and event["error"] is None and event["action"]["message"] is not None]
                counter["messages"] += len(messages)
                counter["duplicates"] += len(messages) - len(set(messages))
                counter["triple_repeat_agents"] += int(len(messages) == 3 and len(set(messages)) == 1)
            for key, field in (("ready", "ready_seconds"), ("input", "input_tokens"), ("generated", "generated_tokens")):
                value = sum(outcome[field] for outcome in outcomes)
                counter[key] += value
                row[f"{phase}_{key}"] = value
            row.update({f"{phase}_success": success, f"{phase}_submissions": episode["submissions"],
                        f"{phase}_end": episode["terminal"], f"{phase}_calls": len(events), f"{phase}_illegal": illegal})
        rows.append(row)
    assert len(rows) == 20
    for cid, call in sorted(calls.items()):
        outcome = call["outcome"]
        ledger.append({"call_id": cid, "seed_exact_decimal": str(call["request"]["seed"]),
                       "input_tokens": outcome["input_tokens"], "generated_tokens": outcome["generated_tokens"],
                       "ready_seconds": outcome["ready_seconds"]})
    final = name == "assisted-experiment"
    seed = 2026101602 if final else run["config"]["bootstrap_seed"]
    intervals = {field: bootstrap(rows, field, seed, final) for field in ("success", "ready")}
    pair_counts = Counter((row["retain_success"], row["clear_success"]) for row in rows)
    result = {"study_id": run["study_id"], "main_worlds": len(rows), "physical_attempts": len(attempts),
              "statistics": stats, "intervals": intervals,
              "paired_outcomes": {"both": pair_counts[1, 1], "retain_only": pair_counts[1, 0],
                                  "clear_only": pair_counts[0, 1], "neither": pair_counts[0, 0]},
              "physical_totals": {field: sum(call["outcome"][field] for call in calls.values())
                                  for field in ("ready_seconds", "input_tokens", "generated_tokens")}}
    if final:
        seed_record = json.loads((ROOT / "scripts/analysis/support/ledger-seed-labels.json").read_text("utf-8"))
        labels = [(entry["call_id"], entry["printed_seed"]) for entry in seed_record["labels"]]
        assert len(labels) == len(calls) == 356
        result["prose_ledger_seed_discrepancies"] = sum(int(seed) != calls[cid]["request"]["seed"] for cid, seed in labels)
        assert result["prose_ledger_seed_discrepancies"] == 354
        assert [stats[p]["success"] for p in stats] == [10, 2, 3]
        assert [intervals["success"][k] for k in ("mean", "low", "high")] == [.05, -.15, .25]
    else:
        assert len(calls) == len(attempts) == 252
        assert [stats[p]["success"] for p in stats] == [3, 2, 2]
        assert [intervals["success"][k] for k in ("mean", "low", "high")] == [0, -.1, .1]
    return result, rows, ledger


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows({key: json.dumps(value) if isinstance(value, (list, dict)) else value
                          for key, value in row.items()} for row in rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=ROOT / "results")
    args = parser.parse_args()
    output = derived_destination(args.output)
    summary = {}
    with checkpoints() as paths:
        for name, directory in paths.items():
            summary[name], rows, ledger = reconstruct(name, directory)
            write_csv(output / f"{name}-main-outcomes.csv", rows)
            write_csv(output / f"{name}-call-ledger.csv", ledger)
    (output / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", "utf-8")
    print(json.dumps({name: {"attempts": result["physical_attempts"], "success_interval": result["intervals"]["success"]}
                      for name, result in summary.items()}, indent=2))


if __name__ == "__main__":
    main()
