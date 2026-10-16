"""Isolated I-01 course study. Importing this package never loads a model."""

REGIME = "i01-course-v1"
ASSISTED_REGIME = "i01-course-assisted-v2"


def assisted(config):
    return config.get("regime") == ASSISTED_REGIME


def config_name(config):
    if config.get("regime") not in (REGIME, ASSISTED_REGIME):
        raise ValueError("Unknown I-01 scientific regime")
    return "i01-course-assisted.json" if assisted(config) else "i01-course.json"

