"""Thin CPU validation command; later milestones add other study commands."""

import argparse
from pathlib import Path
import sys
import unittest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate"])
    parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    if not (root / "tests" / "test_tasks.py").is_file():
        parser.error("CPU validation requires the source checkout and its tests")
    suite = unittest.defaultTestLoader.discover(str(root / "tests"), top_level_dir=str(root))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
