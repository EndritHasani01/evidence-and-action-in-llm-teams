"""Planning arithmetic only; no model inference or measured performance."""
import json
from math import sqrt
from pathlib import Path

rows = []
for n in (48, 36):
    core = n * (16 + 64 + 32 + 2) + 12 * 32
    focal_n = n // 3
    receipt = focal_n * 32
    for name, extra in (("core", 0), ("focused_receipt", receipt),
                        ("all_six_receipt_rejected_default", n * 32)):
        total = core + extra
        rows.append({"worlds": n, "schedule": name, "core_calls": core,
                     "additional_calls": extra, "main_calls": total,
                     "main_24h_break_even_allocated_seconds_per_call": 86400 / total,
                     "illustrative_total_hours_with_6h_reserve": {
                         str(s): 6 + total * s / 3600 for s in (10, 15, 20)}})
assert [r["main_calls"] for r in rows] == [5856, 6368, 7392, 4488, 4872, 5640]
out = {
    "status": "planning arithmetic; not measured feasibility or power",
    "main_schedules": rows,
    "pilot": {"existing_pilot": 588, "extra_two_focal_worlds": 64,
              "pilot_total": 652, "smoke_upper_calls": 24, "combined_upper_calls": 676,
              "three_hour_break_even_s_per_call_without_other_overhead": 10800 / 676},
    "eta_rough_80pct_power_reference": {
        str(n): {str(sd): 2.8 * sd / sqrt(n) for sd in (0.35, 0.60)}
        for n in (12, 16, 24, 36)},
    "se_ratio_36_vs_48_if_variance_equal": sqrt(48 / 36),
    "incremental_hours": {str(calls): {str(s): calls * s / 3600 for s in (10, 15, 20)}
                          for calls in (384, 512, 768, 1152, 1536)},
}
Path(__file__).with_name("budget_and_precision_results.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, indent=2))
