"""Thin CPU validation command; later milestones add other study commands."""

import argparse
from pathlib import Path
import sys
import tomllib
import unittest

from .tasks import Size


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
    parser.add_argument("command", choices=["validate"])
    parser.add_argument("--config", type=Path, default=root / "configs" / "study.toml")
    args = parser.parse_args()
    try:
        size = load_size(args.config)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if not (root / "tests" / "test_tasks.py").is_file():
        parser.error("CPU validation requires the source checkout and its tests")
    print(f"CPU validation: configured size={size.value}; checks cover target and fallback.", flush=True)
    suite = unittest.defaultTestLoader.discover(str(root / "tests"), top_level_dir=str(root))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
