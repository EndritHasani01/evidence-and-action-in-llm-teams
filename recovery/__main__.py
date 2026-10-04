"""CPU validation and population preparation; no inference or accepted freeze."""

import argparse
from pathlib import Path
import sys
import tomllib
import unittest

from .tasks import Size
from .manifests import load_population, save_population
from .populations import PopulationExhausted, prepare_population


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
    validate = commands.add_parser("validate", help="validate CPU contracts and optional saved populations")
    prepare = commands.add_parser("prepare", help="save 60 + five development worlds and nested subsets")
    for command in (validate, prepare):
        command.add_argument("--config", type=Path, default=root / "configs" / "study.toml")
    prepare.add_argument("--seed", required=True, type=int)
    prepare.add_argument("--output", required=True, type=Path, help="new canonical population JSON path")
    validate.add_argument("--manifest", type=Path, help="saved host population to validate without resampling")
    validate.add_argument("--authoritative", type=Path, help="saved authority for exact input/configuration equality")
    args = parser.parse_args()
    try:
        size = load_size(args.config)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if args.command == "prepare":
        try:
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
        print(f"Prepared {args.output}: size={size.value}, main=60 (nested 40), development=5; not an M5 freeze.")
        return 0
    if args.authoritative and not args.manifest:
        parser.error("--authoritative requires --manifest")
    if args.manifest:
        try:
            authority = load_population(args.authoritative) if args.authoritative else None
            population = load_population(args.manifest, authoritative=authority)
            if population.size is not size:
                raise ValueError("manifest mathematical size differs from configuration")
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(f"Saved population verified without resampling: {args.manifest}.", flush=True)
    if not (root / "tests" / "test_tasks.py").is_file():
        parser.error("CPU validation requires the source checkout and its tests")
    print(f"CPU validation: configured size={size.value}; checks cover target and fallback.", flush=True)
    suite = unittest.defaultTestLoader.discover(str(root / "tests"), top_level_dir=str(root))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
