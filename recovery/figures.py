"""Render the seven fixed report exhibits from saved deterministic inputs.

Matplotlib is optional; this module imports it only when rendering. No worker,
inference, evaluation or resampling runs here.
"""

import argparse
from collections import defaultdict
import json
from pathlib import Path


COLORS = ("#176c91", "#ce783c", "#247e68", "#815ba0", "#768999", "#c4515b")


def _empty(ax, text="Unavailable for this supplied population"):
    ax.text(0.5, 0.5, text, transform=ax.transAxes, ha="center", va="center", color="#546575", wrap=True)


def _forest(ax, rows, title):
    from matplotlib.lines import Line2D
    rows = sorted(rows, key=lambda r: (r["estimand"], r["event"]))
    for i, row in enumerate(rows):
        ci, value = row["interval"], row["estimate"]
        sensitivity = row["sensitivity"]["interval"]
        if sensitivity:
            ax.plot(sensitivity, [i, i], color="#a3b0ba", linewidth=5, alpha=0.45)
        if ci:
            ax.plot(ci, [i, i], color=COLORS[0], linewidth=2)
        if value is not None:
            ax.scatter([value], [i], color=COLORS[0], zorder=4)
        else:
            value = row["complete_case_estimate"]
            if value is not None:
                ax.scatter([value], [i], edgecolors=COLORS[0], facecolors="white", zorder=4)
        companion = row["hoeffding"] if row["estimate"] is not None else row["complete_case_hoeffding"]
        if companion:
            ax.plot(companion["interval"], [i, i], color=COLORS[1], linestyle="--", linewidth=1)
    labels = [f"{r['estimand']} ({r['event']})\nN={r['observed_worlds']}/{r['eligible_worlds']}" for r in rows]
    ax.set_yticks(range(len(rows)), labels, fontsize=8)
    ax.axvline(0, color="#8293a0", linewidth=0.7)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("Mean exact-peer correctness" if rows and all(r["range"] == [0, 1] for r in rows)
                  else "Paired exact-correctness contrast")
    ax.invert_yaxis()
    if not rows:
        _empty(ax)
    ax.legend(handles=[Line2D([0], [0], color=COLORS[0], marker="o", label="Population percentile"),
        Line2D([0], [0], color=COLORS[1], linestyle="--", label="Bounded-mean companion"),
        Line2D([0], [0], color="#a3b0ba", linewidth=4, label="Missingness sensitivity"),
        Line2D([0], [0], color=COLORS[0], marker="o", markerfacecolor="white", linestyle="none", label="Complete-case description")],
        fontsize=7, loc="best")


def _lines(ax, rows, series, value, *, x="round", ylim=(-0.03, 1.03)):
    groups = defaultdict(list)
    for row in rows:
        groups[series(row)].append(row)
    plotted = False
    for i, (name, group) in enumerate(sorted(groups.items())):
        group.sort(key=lambda r: r[x])
        points = [(r[x], r[value]) for r in group]
        if not any(v is not None for _, v in points):
            continue
        # None becomes a gap, never zero or an interpolated missing observation.
        ax.plot([n for n, _ in points], [float("nan") if v is None else v for _, v in points],
                marker="o", markersize=3, label=name, color=COLORS[i % len(COLORS)], linestyle=("-", "--", ":")[i//len(COLORS) % 3])
        plotted = True
    ax.set_xticks((1, 2, 3, 4))
    ax.set_xlabel("Scheduled round")
    ax.set_ylim(*ylim)
    if plotted:
        ax.legend(fontsize=7)
    else:
        _empty(ax)


def _quality(ax, rows, metric):
    plotted = False
    for i, row in enumerate(r for r in rows if r["metric"] == metric):
        cc = row["estimate"] is None or row["cost_estimate"] is None
        prefix = "complete_case_" if cc else ""
        quality, cost = row[prefix+"estimate"], row[prefix+"cost_estimate"]
        if quality is None or cost is None:
            continue
        color = COLORS[i % len(COLORS)]
        # Uncertain measured means remain segments, not asserted point values.
        ax.plot(cost, [quality[0]]*2, color=color)
        ax.plot([cost[0]]*2, quality, color=color)
        ax.scatter([cost[0]], [quality[0]], edgecolors=color, facecolors="white" if cc else color,
            label=f"{row['display']} N={row['paired_observed_worlds']}/{row['eligible_worlds']}"+(" (complete cases)" if cc else ""))
        qci, cci = row[prefix+"interval"], row[prefix+"cost_interval"]
        if qci:
            ax.plot([cost[0]]*2, qci, color=color, alpha=0.6, linewidth=1)
        if cci:
            ax.plot(cci, [quality[0]]*2, color=color, alpha=0.6, linewidth=1)
        plotted = True
    ax.set_xlabel("Policy-accounted seconds (prefix + all continuation calls)")
    ax.set_ylabel("Exact-peer recovery AUC" if metric == "auc" else "Final preservation of eligible U")
    ax.set_ylim(-0.05, 1.05)
    if plotted:
        ax.legend(fontsize=7, loc="best")
    else:
        _empty(ax, "Paired quality / measured policy cost unavailable")


def render_figures(directory):
    """Create SVG/PNG artifacts once; bytes are stable in the same plot environment."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from .report import LABEL, _report_html
    directory = Path(directory)
    report = json.loads((directory/"report.json").read_bytes())
    data = json.loads((directory/"plotting.json").read_bytes())
    output = directory/"figures"
    if output.exists():
        raise FileExistsError(f"figure output already exists: {output}")
    output.mkdir()
    with matplotlib.rc_context({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "recovery-report",
            "axes.spines.top": False, "axes.spines.right": False}):
        for exhibit in report["exhibits"]:
            eid = exhibit["id"]
            columns = 3 if eid in ("context", "effects", "repair", "collaborators") else 2
            fig, axes = plt.subplots(1, columns, figsize=(15, 6), layout="constrained")
            try:
                if eid == "context":
                    _lines(axes[0], data["context"], lambda r: r["family"], "old_gold_correctness")
                    axes[0].set_title("Prefix old-gold correctness (fixed peer/world counts)")
                    _lines(axes[1], data["context"], lambda r: r["family"], "remote_record_coverage")
                    axes[1].set_title("Acquired remote current-record coverage")
                    grouped = defaultdict(list)
                    for row in data["controls"]:
                        grouped[row["family"], row["event"]].append(row["correct"])
                    for n, ((family, event), values) in enumerate(sorted(grouped.items())):
                        if None not in values:
                            axes[2].barh(n, sum(values)/len(values), color=COLORS[n % len(COLORS)])
                            axes[2].text(0.02, n, f"{sum(values)}/{len(values)} correct", va="center", fontsize=7,
                                color="#182a39" if sum(values) == 0 else "white")
                        else:
                            axes[2].text(0.02, n, "N/A", va="center", color="#546575")
                    axes[2].set_yticks(range(len(grouped)), [f"{f} / {e}\nN={sum(v is not None for v in values)}/{len(values)}"
                        for (f, e), values in sorted(grouped.items())], fontsize=8)
                    axes[2].set_xlim(0, 1.05)
                    axes[2].set_title("Full-information capability controls")
                    axes[2].set_xlabel("Fraction exact-correct; N is recorded / scheduled")
                    if not grouped:
                        _empty(axes[2])
                elif eid == "effects":
                    _forest(axes[0], [r for r in data[eid] if r["primary"]], "Primaries: 97.5% percentile intervals")
                    _forest(axes[1], [r for r in data[eid] if not r["primary"] and r["endpoint"] == "auc"], "Revised policy AUC: descriptive 95%")
                    primary_names = ("theta", "E_keep")
                    for n, name in enumerate(primary_names):
                        rows = [r for r in data["world_effects"] if r["estimand"] == name and r["value"] is not None]
                        for j, row in enumerate(rows):
                            axes[2].scatter(row["value"], n + (j % 7-3)*0.025, color=COLORS[n], alpha=0.45, s=15)
                        for j, row in enumerate(r for r in data["family_effects"] if r["estimand"] == name and r["estimate"] is not None):
                            axes[2].scatter(row["estimate"], n+0.15+j*0.04, color=COLORS[j % len(COLORS)], marker="|", s=150,
                                label=row["family"] if n == 0 else None)
                    axes[2].set_yticks((0, 1), ("theta worlds / family means", "phi worlds / family means"))
                    axes[2].axvline(0, color="#8293a0", linewidth=0.7)
                    axes[2].set_title("Raw world contrasts; ticks are family means")
                    axes[2].set_xlabel("Exact contrast (unknown worlds omitted only here)")
                    if any(r["estimate"] is not None for r in data["family_effects"]):
                        axes[2].legend(fontsize=7, loc="best")
                elif eid == "repair":
                    for ax, metrics, title in zip(axes, (("changed_accuracy", "old_value_persistence"),
                            ("preservation", "collateral_damage"), ("old_error_repair", "changed_malformed_or_missing")),
                            ("Repair / explicit old values on D", "Preservation / collateral damage on eligible U", "Old U error repair / malformed changed answers")):
                        rows = [r for r in data[eid] if r["policy"] in ("B", "C", "K") and r["metric"] in metrics]
                        _lines(ax, rows, lambda r: r["policy"]+" / "+r["metric"], "rate")
                        ax.set_title(title, fontsize=10)
                        ax.set_ylabel("Eligible peers → worlds → equal eligible families")
                elif eid == "receipts":
                    _forest(axes[0], [r for r in data[eid] if r["estimand"].startswith("receipt_cell_")], "Six first-response representation / receipt cells")
                    _forest(axes[1], [r for r in data[eid] if r["estimand"] == "eta" or r["estimand"] in ("B_delta-B", "C_delta-C", "K_delta-K")], "Direct receipt effects and eta: descriptive 95%")
                elif eid == "collaborators":
                    rows = [r for r in data[eid] if r["round"] is not None and r["estimand"] in ("E_keep", "E_clear")]
                    _lines(axes[0], rows, lambda r: r["estimand"]+" / "+r["event"], "estimate", ylim=(-1.05, 1.05))
                    axes[0].axhline(0, color="#8293a0", linewidth=0.7)
                    axes[0].set_title("Other-group reset effects; round 1 is construction")
                    for ax, group in zip(axes[1:], ("G", "H")):
                        rows = [r for r in data[eid] if r["round"] is not None and r["event"] == "revision" and r["estimand"].startswith("M_"+group+"_")]
                        _lines(ax, rows, lambda r: r["estimand"], "estimate")
                        ax.set_title("Revised subgroup "+group+" across all four masks")
                elif eid == "prose":
                    _forest(axes[0], [r for r in data[eid] if r["round"] == 2], "Immediate Q effect (round 2): descriptive 95%")
                    grouped = defaultdict(lambda: defaultdict(int))
                    for row in data["synchronization"]:
                        if row["phase"] == "continuation" and row["event"] == "revision" and row["replicate"] == 0 and row["policy"] in ("B", "C", "K", "P_G", "P_H"):
                            for category, count in row["observed_category_counts"].items():
                                grouped[row["policy"]][category] += count
                            grouped[row["policy"]]["incomplete"] += row["incomplete_trajectories"]
                    categories = ("continuously_correct", "correct_at_end_after_delay_or_regression", "temporarily_correct_but_incorrect_at_end", "never_jointly_correct", "incomplete")
                    for n, (policy, counts) in enumerate(sorted(grouped.items())):
                        left = 0
                        for j, category in enumerate(categories):
                            axes[1].barh(n, counts[category], left=left, color=COLORS[j], label=category if n == 0 else None)
                            left += counts[category]
                    axes[1].set_yticks(range(len(grouped)), [f"{p} N={sum(c.values())}" for p, c in sorted(grouped.items())])
                    axes[1].set_xlabel("Scheduled worlds; incomplete is a separate category")
                    axes[1].set_title("Four-round joint trajectories")
                    if grouped:
                        axes[1].legend(fontsize=6, loc="best")
                    else:
                        _empty(axes[1])
                else:
                    _quality(axes[0], data[eid], "auc")
                    _quality(axes[1], data[eid], "final_preservation")
                    axes[0].set_title("Paired quality / original policy cost: 95%")
                    axes[1].set_title("Paired preservation / its eligible-world cost: 95%")
                label = LABEL
                if report["scope"].get("regime") == "course":
                    label += "\nExploratory course: "+report["execution"]["status"]+"; "+report["execution"]["coverage_status"]+" supplied scope"
                fig.suptitle(exhibit["title"]+"\n"+label, fontsize=14)
                fig.savefig(output/(eid+".svg"), metadata={"Date": None, "Creator": "recovery offline report"})
                fig.savefig(output/(eid+".png"), dpi=180, metadata={"Software": "recovery offline report"})
            finally:
                plt.close(fig)
    (directory/"report.html").write_text(_report_html(report, True), encoding="utf-8", newline="\n")
    (output/"environment.json").write_text(json.dumps(dict(matplotlib=matplotlib.__version__, backend="Agg",
        font="DejaVu Sans", png_dpi=180, svg_metadata_date=None,
        scope="Plotting environment only; not an accepted model/inference freeze."), sort_keys=True)+"\n", encoding="utf-8", newline="\n")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    try:
        output = render_figures(args.report)
    except (OSError, ValueError, ImportError) as error:
        parser.error(str(error))
    print(f"Seven synthetic-validation SVG/PNG exhibits: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
