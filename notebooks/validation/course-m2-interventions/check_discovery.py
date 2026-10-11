"""Inspect actual CLI suite registration without executing unaffected checks."""

from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from recovery.__main__ import main


def flatten(suite):
    for item in suite:
        yield from flatten(item) if isinstance(item, unittest.TestSuite) else (item,)


for core in (False, True):
    def inspect(suite):
        ids = [t.id() for t in flatten(suite)]
        course = [i for i in ids if "tests.course_intervention_checks." in i]
        assert len(course) == (0 if core else 15)
        assert len(ids) == len(set(ids))
        assert not any("tokenizer_course_interventions" in i or "_FailedTest" in i for i in ids)
        print(dict(core_only=core, discovered_checks=len(ids), course_intervention_checks=len(course), tests_executed=0))
        return SimpleNamespace(wasSuccessful=lambda: True)
    arguments = ["recovery", "validate", "--regime", "course", "--config", str(ROOT / "configs/course-inputs.toml"),
                 "--manifest", str(ROOT / "tests/fixtures/population_course.json"),
                 "--schedule", str(ROOT / "tests/fixtures/schedules_course.json")]
    if core:
        arguments.append("--core-only")
    with patch.object(sys, "argv", arguments), patch.object(unittest.TextTestRunner, "run", side_effect=inspect):
        assert main() == 0
