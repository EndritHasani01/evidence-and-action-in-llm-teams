"""Thesis regime thesis-recovery-v1: two-agent recovery after one private change.

Specification: PROJECT_SPECIFICATION.md section 13 and its annex,
docs/proposals/thesis-project-specification.md. Importing this package uses only
the standard library and never loads a model.
"""

import hashlib
import json
from pathlib import Path

REGIME = "thesis-recovery-v1"
CELLS = ("RV", "CV", "RN", "CN")
REVISION_CELLS = ("RV", "CV")
RETAIN_CELLS = ("RV", "RN")
MODELS = ("qwen", "granite")
SOURCE_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = "configs/thesis.json"
WORLDS_PATH = "configs/thesis-worlds.json"
SEPARATION_PATH = "configs/thesis-worlds-separation.json"
LOCK_PATH = "configs/i01-runtime.lock"
SCOPES = ("cpu", "rehearsal", "development", "main")


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def digest_file(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load_config(source=None):
    """Read and validate the adopted configuration; no silent defaults."""
    path = Path(source or SOURCE_ROOT) / CONFIG_PATH
    config = json.loads(path.read_text(encoding="utf-8"))
    if config.get("regime") != REGIME or config.get("schema") != 1:
        raise ValueError("configs/thesis.json is not the adopted thesis-recovery-v1 configuration")
    if tuple(config["cells"]) != CELLS or tuple(config["models"]) != MODELS:
        raise ValueError("cells and models must match the adopted specification")
    if (config["development_worlds"], config["main_worlds"], config["fallback_main_worlds"],
            config["strata"]) != (16, 192, 128, 8):
        raise ValueError("population sizes must match the adopted specification")
    return config
