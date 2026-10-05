"""CPU validation and population/schedule preparation; no inference or accepted freeze."""

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
    for count in (60, 40):
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
    for command in (validate, prepare):
        command.add_argument("--config", type=Path, default=root / "configs" / "study.toml")
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
                schedules = prepare_schedules(population)
                save_schedules(schedules, population, args.output)
            else:
                population = prepare_population(args.seed, size)
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
            print(f"Prepared schedules {args.output}: size={size.value}; not an M5 freeze.")
            _schedule_summary(schedules, population)
        else:
            print(f"Prepared {args.output}: size={size.value}, main=60 (nested 40), development=5; not an M5 freeze.")
        return 0
    if args.schedule and not args.manifest:
        parser.error("--schedule requires --manifest")
    if args.manifest:
        try:
            authority = load_population(args.authoritative) if args.authoritative else None
            population = load_population(args.manifest, authoritative=authority)
            if population.size is not size:
                raise ValueError("manifest mathematical size differs from configuration")
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
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
