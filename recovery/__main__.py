"""CPU validation, preparation and offline analysis; no inference or accepted freeze."""

import argparse
import json
from pathlib import Path
import sys
import tomllib
import unittest

from .tasks import Size
from .manifests import load_population, load_schedules, save_population, save_schedules
from .populations import PopulationExhausted, prepare_population
from .schedule import SMOKE_MAX_CALLS, component_counts, prepare_schedules


def _schedule_summary(schedules, population) -> None:
    for count in population.main_counts:
        rows = component_counts(schedules.main_for(population, count)).values()
        distinct, logical = (sum(row[i] for row in rows) for i in (0, 1))
        print(f"Main {count}: {distinct:,} distinct / {logical:,} logical slots.")
    rows = component_counts(schedules.development).values()
    distinct, logical = (sum(row[i] for row in rows) for i in (0, 1))
    print(f"Development: {distinct:,} distinct / {logical:,} logical; first {len(schedules.capability)} capability calls.")
    print(f"Smoke is separate: at most {SMOKE_MAX_CALLS} additional calls ({distinct + SMOKE_MAX_CALLS:,} combined).")


def load_size(path: Path) -> Size:
    """Read only the declared mathematical size; no pilot/model choice is frozen."""

    with path.open("rb") as source:
        config = tomllib.load(source)
    if set(config) != {"size"}:
        raise ValueError("configuration requires exactly the size field")
    return Size(config["size"])


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="validate CPU contracts and optional saved populations/schedules")
    prepare = commands.add_parser("prepare", help="prepare populations, or complete schedules from saved inputs")
    status = commands.add_parser("status", help="read-only progress/accounting from saved schedules and worker files")
    status.add_argument("--manifest", required=True, type=Path)
    status.add_argument("--schedule", required=True, type=Path)
    status.add_argument("--worker", action="append", required=True, type=Path, help="one path per physical worker; missing files remain unknown")
    status.add_argument("--prior-worker", action="append", default=[], type=Path, help="previous measured run files, charged once")
    status.add_argument("--stage", choices=("development", "main"), default="development")
    status.add_argument("--count", choices=(60, 40), type=int, default=60)
    status.add_argument("--json", action="store_true", help="include every scheduled slot, parent, cost and resumable branch")
    analyze = commands.add_parser("analyze", help="offline exact outcomes, coordinate diagnostics and trajectories")
    analyze.add_argument("--manifest", required=True, type=Path)
    analyze.add_argument("--schedule", required=True, type=Path)
    analyze.add_argument("--worker", action="append", required=True, type=Path, help="authoritative workers only; missing files leave unknown slots")
    analyze.add_argument("--stage", choices=("development", "main"), default="main")
    analyze.add_argument("--count", choices=(60, 40), type=int, default=60)
    analyze.add_argument("--output", required=True, type=Path, help="new derived JSON or JSON.gz table export")
    analyze.add_argument("--estimands", action="store_true", help="include prespecified contrasts and conditional repeatability")
    analyze.add_argument("--diagnostics", action="store_true", help="include information/work inventories and deterministic references")
    analyze.add_argument("--costs", action="store_true", help="include original measured costs and the frozen C/K boundary rule")
    analyze.add_argument("--uncertainty", action="store_true", help="include paired intervals/missingness; also includes estimands and costs")
    analyze.add_argument("--report", action="store_true", help="export seven synthetic-validation exhibits, all M4 tables and exact cases to a new directory; requires --as-of")
    analyze.add_argument("--figures", action="store_true", help="render report SVG/PNG figures with optional Matplotlib; requires --report")
    analyze.add_argument("--resampling-seed", type=int, help="saved nonnegative world-bootstrap seed; requires --uncertainty or --report (default 20261006)")
    analyze.add_argument("--as-of", help="explicit zoned accounting timestamp for reproducible costs; required for --report")
    analyze.add_argument("--tokenizer", type=Path, help="local matching tokenizer metadata for exact diagnostic history counts; no weights/downloads")
    for command in (validate, prepare):
        command.add_argument("--config", type=Path, default=root / "configs" / "study.toml")
        command.add_argument("--regime", choices=("thesis", "course"), default="thesis",
                             help="explicit population scope; course requires fallback size; default thesis")
        command.add_argument("--authoritative", type=Path, help="saved population authority for exact input/configuration equality")
    source = prepare.add_mutually_exclusive_group(required=True)
    source.add_argument("--seed", type=int, help="prepare a new population with this seed")
    source.add_argument("--manifest", type=Path, help="prepare all schedules from this saved population, without resampling")
    prepare.add_argument("--output", required=True, type=Path, help="new population or schedule JSON path")
    validate.add_argument("--manifest", type=Path, help="saved host population to validate without resampling")
    validate.add_argument("--schedule", type=Path, help="saved complete schedules to validate against --manifest")
    validate.add_argument("--core-only", action="store_true",
                          help="run dependency-free core checks only; excludes strict reply validation")
    args = parser.parse_args()
    if args.command == "analyze":
        from .evaluate import evaluate_run, write_evaluation
        from sqlite3 import Error as SQLiteError
        try:
            population = load_population(args.manifest)
            schedules = load_schedules(args.schedule, population)
            worlds = population.development if args.stage == "development" else population.worlds(args.count)
            branches = schedules.development if args.stage == "development" else schedules.main_for(population, args.count)
            if args.tokenizer and not (args.diagnostics or args.report):
                raise ValueError("--tokenizer requires --diagnostics or --report")
            if args.as_of and not (args.costs or args.uncertainty or args.report):
                raise ValueError("--as-of requires --costs or --uncertainty or --report")
            if args.resampling_seed is not None and not (args.uncertainty or args.report):
                raise ValueError("--resampling-seed requires --uncertainty or --report")
            if args.figures and not args.report:
                raise ValueError("--figures requires --report")
            tokenizer = None
            if args.tokenizer:
                from transformers import AutoTokenizer
                tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
            if args.report:
                from .report import report_run, write_report
                from .uncertainty import DEFAULT_SEED
                result = report_run(worlds, branches, args.worker, now=args.as_of,
                    seed=DEFAULT_SEED if args.resampling_seed is None else args.resampling_seed, tokenizer=tokenizer,
                    provenance=dict(manifest=args.manifest.name, schedule=args.schedule.name,
                        workers=[p.name for p in args.worker], stage=args.stage, count=args.count if args.stage == "main" else None))
                write_report(args.output, result, figures=args.figures)
                tables = result["tables"]
            elif args.uncertainty:
                from .uncertainty import DEFAULT_SEED, uncertainty_run
                tables = uncertainty_run(worlds, branches, args.worker, now=args.as_of,
                    seed=DEFAULT_SEED if args.resampling_seed is None else args.resampling_seed,
                    diagnostics=args.diagnostics, tokenizer=tokenizer)
            elif args.costs:
                from .costs import costs_run
                tables = costs_run(worlds, branches, args.worker, now=args.as_of,
                    diagnostics=args.diagnostics, estimands=args.estimands, tokenizer=tokenizer)
            elif args.diagnostics:
                from .information import information_run
                tables = information_run(worlds, branches, args.worker, tokenizer=tokenizer, estimands=args.estimands)
            elif args.estimands:
                from .analysis import analyze_run
                tables = analyze_run(worlds, branches, args.worker)
            else:
                tables = evaluate_run(worlds, branches, args.worker)
            if not args.report:
                write_evaluation(args.output, tables)
        except (OSError, ValueError, ImportError, SQLiteError) as error:
            parser.error(str(error))
        print(f"Offline tables: {args.output}; {tables['coverage']['recorded']}/{tables['coverage']['scheduled']} recorded; "
              f"{tables['coverage']['unknown']} unknown. No inference; scripted data are validation evidence.")
        return 0
    if args.command == "status":
        from .accounting import format_status, progress_snapshot
        try:
            population = load_population(args.manifest)
            schedules = load_schedules(args.schedule, population)
            worlds = population.development if args.stage == "development" else population.worlds(args.count)
            branches = schedules.development if args.stage == "development" else schedules.main_for(population, args.count)
            snapshot = progress_snapshot(worlds, branches, args.worker, prior_paths=args.prior_worker)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(json.dumps(snapshot, ensure_ascii=True, allow_nan=False, sort_keys=True) if args.json else format_status(snapshot))
        return 0
    try:
        size = load_size(args.config)
        if args.regime == "course" and size is not Size.FALLBACK:
            raise ValueError("course requires the fallback mathematical size")
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if args.authoritative and not args.manifest:
        parser.error("--authoritative requires --manifest")
    if args.command == "prepare":
        try:
            if args.manifest:
                authority = load_population(args.authoritative) if args.authoritative else None
                population = load_population(args.manifest, authoritative=authority)
                if population.size is not size:
                    raise ValueError("manifest mathematical size differs from configuration")
                if population.regime != args.regime:
                    raise ValueError("manifest regime differs from configuration")
                schedules = prepare_schedules(population)
                save_schedules(schedules, population, args.output)
            else:
                population = prepare_population(args.seed, size, regime=args.regime)
                save_population(population, args.output)
        except PopulationExhausted as error:
            # Fail explicitly and emit every failed attempt; no accepted manifest
            # is written and the caller can retain stderr as rejection evidence.
            print(str(error), file=sys.stderr)
            for rejection in error.rejections:
                print(f"attempt {rejection.attempt}: {','.join(rejection.reasons)}", file=sys.stderr)
            return 1
        except (OSError, ValueError) as error:
            parser.error(str(error))
        if args.manifest:
            print(f"Prepared schedules {args.output}: size={size.value}, regime={args.regime}; not an M5 freeze.")
            _schedule_summary(schedules, population)
        else:
            main_scope = "20" if args.regime == "course" else "60 (nested 40)"
            print(f"Prepared {args.output}: size={size.value}, regime={args.regime}, main={main_scope}, development=5; not an M5 freeze.")
        return 0
    if args.schedule and not args.manifest:
        parser.error("--schedule requires --manifest")
    if args.manifest:
        try:
            authority = load_population(args.authoritative) if args.authoritative else None
            population = load_population(args.manifest, authoritative=authority)
            if population.size is not size:
                raise ValueError("manifest mathematical size differs from configuration")
            if population.regime != args.regime:
                raise ValueError("manifest regime differs from configuration")
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(f"Saved population verified without resampling: {args.manifest}.", flush=True)
        if args.schedule:
            try:
                schedules = load_schedules(args.schedule, population)
            except (OSError, ValueError) as error:
                parser.error(str(error))
            print(f"Saved schedules and CPU dependencies verified: {args.schedule}.", flush=True)
            _schedule_summary(schedules, population)
    if not (root / "tests" / "test_tasks.py").is_file():
        parser.error("CPU validation requires the source checkout and its tests")
    if not args.core_only:
        try:
            # A declared CPU dependency, never the optional inference stack.
            import recovery.protocol
            import recovery.runner
        except ImportError:
            parser.error("full CPU validation requires Pydantic 2 and LangGraph/SQLite; install the package, or use --core-only for the core subset")
    scope = ("core subset (strict replies, rounds, events, replay, attainability, durability, attempts, workers, accounting and lifecycle excluded)" if args.core_only
             else "core, strict replies, rounds, events, replay, attainability, durability, bounded attempts, local workers, accounting and killed-process lifecycle")
    print(f"CPU validation ({scope}): configured size={size.value}; checks cover target and fallback.", flush=True)
    suite = unittest.defaultTestLoader.discover(str(root / "tests"), top_level_dir=str(root))
    if not args.core_only:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.protocol_checks"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.round_checks"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.event_checks"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.replay_checks"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.attainability_checks"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.durable_checks"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.attempt_checks"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.worker_checks"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.accounting_checks"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.lifecycle_checks"))
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName("tests.inference_checks"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
