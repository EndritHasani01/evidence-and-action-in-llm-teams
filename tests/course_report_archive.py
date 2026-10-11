"""Reproduce course reports twice from original workers and accepted M4 joins."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
from zipfile import ZipFile

from recovery.evaluate import write_evaluation
from recovery.manifests import load_population, load_schedules
from recovery.report import report_run, write_report
from tests.course_analysis_archive import RUN, extract
from tests.course_diagnostics_archive import ScriptedWordCounter
from tests.course_uncertainty_archive import AS_OF, SEED, FIXTURE as UNCERTAINTY
from tests.outcome_fixture import ROOT
from tests.test_report_run import audit_links

FIXTURE = ROOT / "tests/fixtures/course_report_tables.json.gz"
PORTABLE = ROOT / "tests/fixtures/course_scripted_reports.zip"
RETAINED_SCOPES = {
    "test_every_family_intervention_control_repeat_and_branch_local_prose": "complete-selected-scope",
    "full-main-20": "incomplete-main-20",
    "test_budget_deadline_preserves_unknowns_releases_and_resumes_original_course_scope/stopped": "stopped-prefix",
    "unexecuted-development": "unexecuted-development",
    "terminal-feasibility": "terminal-feasibility",
}
TERMINAL = dict(source="synthetic-terminal-feasibility.md",
    text="Synthetic terminal feasibility fixture; not an actual model/GPU failure.\r\n"
         "The example gate has no accepted course runtime, memory/headroom or model capability evidence.\n"
         "Main execution and freeze are unavailable; all unexecuted main slots remain unknown.\n")


def load(path):
    with gzip.open(path, "rt", encoding="utf-8") as source:
        return json.load(source)


def reconstruct(bundle=RUN, *, export=None, figures=False):
    prior_analysis = load(ROOT / "tests/fixtures/course_analysis_tables.json.gz")["cases"]
    prior_diagnostics = load(ROOT / "tests/fixtures/course_diagnostic_cost_tables.json.gz")["cases"]
    prior_uncertainty = load(UNCERTAINTY)["cases"]
    cases = {}
    if export is not None:
        export = Path(export)
        export.mkdir()  # Protect existing exports.
    with tempfile.TemporaryDirectory(prefix="course-report-reproduction-") as temporary, ZipFile(bundle) as archive:
        root = Path(temporary)
        evidence = json.loads(archive.read("evidence.json"))
        extract(archive, root, ("inputs/population.json", "inputs/schedules.json"))
        population = load_population(root / "inputs/population.json")
        schedules = load_schedules(root / "inputs/schedules.json", population)
        assert population.regime == schedules.regime == "course"
        by_world = {w.world_id: w for w in population.main + population.development}
        by_branch = {b.branch_id: b for b in schedules.main + schedules.development}

        def reproduce(name, worlds, branches, paths, *, terminal=None):
            before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.exists()}
            provenance = dict(source_bundle=Path(bundle).name, source_scope=name,
                workers=[p.name for p in paths], accounting_as_of=AS_OF,
                history_counter="Original scripted word counter; not native Qwen tokens")
            left = report_run(worlds, branches, paths, now=AS_OF, seed=SEED, regime="course",
                provenance=provenance, terminal_feasibility=terminal, tokenizer=ScriptedWordCounter())
            right = report_run(worlds, branches, paths, now=AS_OF, seed=SEED, regime="course",
                provenance=provenance, terminal_feasibility=terminal, tokenizer=ScriptedWordCounter())
            for key in left:
                assert left[key] == right[key], "repeated course report: " + name + "/" + key
            prior_name = "unexecuted-main-20" if terminal is not None else name
            for key, value in prior_analysis[prior_name].items():
                assert left["tables"][key] == value, "accepted outcomes/estimands changed: " + name + "/" + key
            for key, value in prior_diagnostics[prior_name].items():
                assert left["tables"][key] == value, "accepted diagnostics/costs changed: " + name + "/" + key
            for key, value in left["tables"]["uncertainty"].items():
                assert value == prior_uncertainty[prior_name][key], "accepted uncertainty changed: " + name + "/" + key
            assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in before.items())
            assert all(p.exists() == (p in before) for p in paths), "missing worker was created"
            index = str(len(cases))
            (root / "first").mkdir(exist_ok=True)
            (root / "second").mkdir(exist_ok=True)
            first, second = root / "first" / index, root / "second" / index
            write_report(first, left)
            write_report(second, right)
            for path in first.iterdir():
                assert path.read_bytes() == (second / path.name).read_bytes(), "export bytes: " + name + "/" + path.name
            links = audit_links(first)
            if export is not None and name in RETAINED_SCOPES:
                write_report(export / RETAINED_SCOPES[name], left, figures=figures)
            cases[name] = dict(report=json.loads(json.dumps(left["report"])), links_checked=links,
                table_rows={k: len(v) for k, v in left["tables"].items() if isinstance(v, list)},
                repeated_outputs=sorted(p.name for p in first.iterdir()),
                prerequisite_joins="accepted outcomes, estimands, diagnostics, costs and uncertainty identical")
            coverage = left["tables"]["coverage"]
            print(f"Verified twice: {name}; {coverage['recorded']}/{coverage['scheduled']} recorded, "
                  f"{coverage['unknown']} unknown; {left['report']['execution']['status']}.", flush=True)

        for case in evidence["cases"]:
            base = case["directory"]
            selected = json.loads(archive.read(base + "/selection.json"))
            extract(archive, root, [base + "/" + name for name in selected["workers"]])
            worlds = tuple(by_world[name] for name in selected["world_ids"])
            branches = tuple(by_branch[name] for name in selected["branch_ids"])
            paths = tuple(root / base / name for name in selected["workers"])
            reproduce(base, worlds, branches, paths)
            if "stopped_worker" in case:
                extract(archive, root, [base + "/" + case["stopped_worker"]])
                reproduce(base + "/stopped", worlds, branches, (root / base / case["stopped_worker"],))
            if len(worlds) == 5:
                reproduce("full-main-20", population.main, schedules.main, paths)
        missing = (root / "absent.sqlite",)
        reproduce("unexecuted-main-20", population.main, schedules.main, missing)
        reproduce("unexecuted-development", population.development, schedules.development, missing)
        reproduce("terminal-feasibility", population.main, schedules.main, missing, terminal=TERMINAL)
        assert not missing[0].exists()
    assert len(cases) == 8
    return dict(kind="Course M4 synthetic CPU reports; no pretrained-model or empirical result",
        source_bundle=Path(bundle).name, seed=SEED, accounting_as_of=AS_OF, cases=cases)


def summary(actual):
    return {name: dict(coverage=case["report"]["coverage"], status=case["report"]["execution"]["status"],
        coverage_status=case["report"]["execution"]["coverage_status"],
        selected_ids=[r["world_id"] for r in case["report"]["cases"]],
        exhibits=len(case["report"]["exhibits"]), links=case["links_checked"])
        for name, case in actual["cases"].items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-fixture", type=Path)
    parser.add_argument("--export", type=Path)
    parser.add_argument("--figures", action="store_true")
    args = parser.parse_args()
    if args.figures and args.export is None:
        parser.error("--figures requires --export")
    actual = reconstruct(export=args.export, figures=args.figures)
    if args.write_fixture:
        write_evaluation(args.write_fixture, actual)
    else:
        saved = load(FIXTURE)
        assert actual.keys() == saved.keys()
        for name, case in actual["cases"].items():
            assert case == saved["cases"][name], "retained course report differs: " + name
    print(json.dumps(summary(actual), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
