"""Compute the exact matrix and ILLUSTRATIVE budget; no GPU measurements."""
import json
from pathlib import Path
from .contracts import ExperimentConfig


def compute(config):
    rows = []
    for r in config.rows:
        worlds = r.base_worlds * r.variants
        short = worlds * (r.prefix_calls_per_world + len(r.arms) * r.recovery_calls_per_arm + r.single_calls_per_world)
        long = worlds * (r.extraction_calls_per_world + r.reviewer_calls_per_world)
        rows.append({"id": r.id, "world_variants": worlds, "short_calls": short,
                     "long_calls": long, "total_calls": short + long, "model": r.model})
    return rows


def forecast(rows, speed=1.0):
    seconds = 0
    for row in rows:
        # Proposed means: agent/single 1100 input,180 output; extraction/review 2200/300.
        inp = row["short_calls"] * 1100 + row["long_calls"] * 2200
        out = row["short_calls"] * 180 + row["long_calls"] * 300
        p, d = (300, 15) if "7B" in row["model"] else (400, 20)
        seconds += inp / (p * speed) + out / (d * speed)
    return seconds / 3600 * 1.12 + 4


def main():
    path = Path(__file__).resolve().parents[1] / "configs/experiment.json"
    cfg = ExperimentConfig.model_validate_json(path.read_text())
    rows = compute(cfg)
    result = {"rows": rows, "total_calls": sum(x["total_calls"] for x in rows),
              "short_calls": sum(x["short_calls"] for x in rows),
              "long_calls": sum(x["long_calls"] for x in rows),
              "illustrative_gpu_hours": forecast(rows),
              "half_speed_gpu_hours": forecast(rows, 0.5),
              "measured": False}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
