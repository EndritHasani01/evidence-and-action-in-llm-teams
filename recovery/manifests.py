"""One canonical host manifest; exports/subsets derive from it, never peer views.

Gold, footprints and correctness strata are absent. Loading preserves actual
saved inputs without resampling. An existing authoritative Population is the
baseline for input/configuration equality; no checksum or identity registry.
"""

from dataclasses import asdict
import json
from pathlib import Path

from .edits import Edit
from .populations import (Eligibility, Population, PreparedWorld, Rejection, Streams,
                          validate_population)
from .schedule import Branch, CallSlot, Schedules, validate_schedules
from .tasks import Size, SourceRecord, Task, World


def manifest_bytes(population: Population) -> bytes:
    return (json.dumps(asdict(population), ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def assert_matches(candidate: Population, authoritative: Population) -> None:
    if manifest_bytes(candidate) != manifest_bytes(authoritative):
        raise ValueError("population differs from the saved authoritative manifest")


def save_population(population: Population, path: Path) -> None:
    validate_population(population)
    payload = manifest_bytes(population)
    # Exclusive creation protects the existing saved authority from replacement.
    with Path(path).open("xb") as output:
        output.write(payload)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate manifest field")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("nonfinite manifest number")


def _prepared(data: dict) -> PreparedWorld:
    world_data = data["world"]
    records = []
    for item in world_data["records"]:
        raw = dict(item)
        if type(raw["value"]) is list:
            raw["value"] = tuple(raw["value"])
        records.append(SourceRecord(**raw))
    world = World(Task(world_data["task"]), Size(world_data["size"]), tuple(records))
    streams = dict(data["streams"])
    streams["prefix"] = tuple(tuple(row) for row in streams["prefix"])
    streams["continuation"] = tuple(tuple(tuple(row) for row in replicate)
                                     for replicate in streams["continuation"])
    streams["controls"] = tuple(streams["controls"])
    fields = dict(data)
    fields.update(world=world, main_edit=Edit(**data["main_edit"]),
                  preserving_edit=Edit(**data["preserving_edit"]) if data["preserving_edit"] is not None else None,
                  partition=tuple(tuple(pair) for pair in data["partition"]),
                  streams=Streams(**streams),
                  eligibility=Eligibility(tuple(data["eligibility"]["main_records"]),
                                          data["eligibility"]["preserving_pairs"]),
                  rejections=tuple(Rejection(r["attempt"], tuple(r["reasons"])) for r in data["rejections"]))
    return PreparedWorld(**fields)


def load_population(path: Path, *, authoritative: Population | None = None) -> Population:
    data = json.loads(Path(path).read_bytes(), object_pairs_hook=_unique_object,
                      parse_constant=_invalid_constant)
    try:
        fields = dict(data)
        fields.update(size=Size(data["size"]), owner_seeds=tuple(data["owner_seeds"]),
                      development_owner_seeds=tuple(data["development_owner_seeds"]),
                      main=tuple(_prepared(w) for w in data["main"]),
                      development=tuple(_prepared(w) for w in data["development"]))
        population = Population(**fields)
        # Exact canonical representation detects extra/missing nested fields and
        # bool/float coercions that ordinary Python object equality would hide.
        encoded = (json.dumps(data, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
        if manifest_bytes(population) != encoded:
            raise ValueError("manifest contains undeclared fields or coerced values")
        validate_population(population)
        if authoritative is not None:
            assert_matches(population, authoritative)
        return population
    except (KeyError, TypeError, OverflowError) as error:
        raise ValueError("invalid population manifest structure") from error


def schedule_bytes(schedules: Schedules) -> bytes:
    return (json.dumps(asdict(schedules), ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def assert_schedules_match(candidate: Schedules, authoritative: Schedules) -> None:
    if schedule_bytes(candidate) != schedule_bytes(authoritative):
        raise ValueError("schedule differs from the saved authoritative schedule")


def save_schedules(schedules: Schedules, population: Population, path: Path) -> None:
    """Save a derived host schedule without copying actual population inputs."""
    validate_schedules(schedules, population)
    payload = schedule_bytes(schedules)
    with Path(path).open("xb") as output:
        output.write(payload)


def _branch(data: dict) -> Branch:
    fields = dict(data)
    fields.update(task=Task(data["task"]), calls=tuple(CallSlot(**c) for c in data["calls"]))
    return Branch(**fields)


def load_schedules(path: Path, population: Population, *, authoritative: Schedules | None = None) -> Schedules:
    """Load exact calls/parents and check both main counts and development.

    The population remains the input authority. Its own authoritative comparison
    is needed to detect mathematically valid changes to the saved raw inputs.
    Neither worlds nor schedules are rebuilt during loading.
    """
    data = json.loads(Path(path).read_bytes(), object_pairs_hook=_unique_object,
                      parse_constant=_invalid_constant)
    try:
        fields = dict(data)
        fields.update(size=Size(data["size"]), main=tuple(_branch(b) for b in data["main"]),
                      development=tuple(_branch(b) for b in data["development"]))
        schedules = Schedules(**fields)
        encoded = (json.dumps(data, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
        if schedule_bytes(schedules) != encoded:
            raise ValueError("schedule contains undeclared fields or coerced values")
        validate_schedules(schedules, population)
        if authoritative is not None:
            assert_schedules_match(schedules, authoritative)
        return schedules
    except (KeyError, TypeError, OverflowError) as error:
        raise ValueError("invalid schedule manifest structure") from error
