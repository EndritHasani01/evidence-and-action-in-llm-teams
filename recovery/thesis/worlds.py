"""World generation, the committed manifest and historical input separation.

Specification section 3.3. Worlds depend only on the master seed and the world
identifier; no model outcome can select, replace or reorder a world. Each world
carries two planned edits of the same owner: the answer-changing revision of
its stratum and an answer-preserving change of one non-winning record, drawn
from a separate seed stream so neither edit depends on the other.
"""

from copy import deepcopy
import json
from pathlib import Path
from random import Random
import re
import zipfile

from ..i01.core import canonical, check_disjoint_inputs, seed_for
from . import (CELLS, MODELS, REGIME, SEPARATION_PATH, SOURCE_ROOT, WORLDS_PATH,
               digest_bytes, digest_file, load_config)

GENERATOR = "thesis-worlds-v2"
EDITS = ("demote", "keep")
LOW, HIGH = -1000, 1000
INPUTS = ("original", "revised", "preserving")


def stratum(index):
    """Index i -> stratum i mod 8 = edit type x changed owner x first speaker."""
    s = index % 8
    return dict(stratum=s, edit=EDITS[s // 4], owner=(s // 2) % 2, first=s % 2)


def world_id(group, index):
    if group == "development":
        return f"dev-{index:02d}"
    if group == "main":
        return f"main-{index:03d}"
    raise ValueError("group must be development or main")


def holders(shards, answer):
    return [agent for agent in (0, 1) if answer in shards[agent]]


def model_seeds(master, wid):
    """Exact 63-bit per-call seeds; the six continuation cells share theirs."""
    return {model: {
        "prefix": [[seed_for(master, model, wid, "prefix", a, k) for k in range(3)] for a in range(2)],
        "continuation": [[seed_for(master, model, wid, "continuation", a, k) for k in range(3)] for a in range(2)],
        "control": {phase: seed_for(master, model, wid, "control", phase) for phase in ("original", "revised")},
    } for model in MODELS}


def make_world(master, group, index, *, max_proposals=1000):
    wid = world_id(group, index)
    st = stratum(index)
    owner, edit = st["owner"], st["edit"]
    rng = Random(seed_for(master, wid, "world"))
    rejections = dict(nonunique_maximum=0, runner_up_at_floor=0, no_keep_value=0, owner_block=0)
    for proposal in range(1, max_proposals + 1):
        shards = [[rng.randint(LOW, HIGH) for _ in range(20)] for _ in range(2)]
        values = shards[0] + shards[1]
        m1 = max(values)
        if values.count(m1) != 1:
            rejections["nonunique_maximum"] += 1
            continue
        m2 = max(v for v in values if v != m1)
        if m2 <= LOW:
            rejections["runner_up_at_floor"] += 1
            continue
        if m2 == HIGH - 1:
            rejections["no_keep_value"] += 1
            continue
        if m1 not in shards[owner]:
            rejections["owner_block"] += 1
            continue
        row = shards[owner].index(m1)
        if edit == "demote":
            replacement = rng.randint(LOW, m2 - 1)
        else:
            replacement = rng.choice([v for v in range(m2 + 1, HIGH + 1) if v != m1])
        revised = deepcopy(shards)
        revised[owner][row] = replacement
        revised_truth = max(revised[0] + revised[1])
        # Answer-preserving change: one non-winning record of the same owner gets a
        # different value below M1, so the answer and both local maxima are unchanged.
        prng = Random(seed_for(master, wid, "preserving"))
        preserving_row = prng.choice([j for j in range(20) if j != row])
        preserving_before = shards[owner][preserving_row]
        preserving_after = prng.choice([v for v in range(LOW, m1) if v != preserving_before])
        preserving = deepcopy(shards)
        preserving[owner][preserving_row] = preserving_after
        order = list(CELLS)
        Random(seed_for(master, wid, "order")).shuffle(order)
        return dict(id=wid, group=group, index=index, **st,
                    original=shards, revised=revised, row=row, before=m1, after=replacement,
                    runner_up=m2, original_truth=m1, revised_truth=revised_truth,
                    holders_original=holders(shards, m1), holders_revised=holders(revised, revised_truth),
                    preserving=preserving, preserving_row=preserving_row, preserving_before=preserving_before,
                    preserving_after=preserving_after,
                    order=order, proposals=proposal, rejections=rejections,
                    seeds=model_seeds(master, wid))
    raise ValueError(f"mathematical proposal limit exhausted: {wid}")


def build_manifest(config=None):
    config = config or load_config()
    master = config["master_seed"]
    worlds = [make_world(master, "development", i, max_proposals=config["max_proposals"])
              for i in range(config["development_worlds"])]
    worlds += [make_world(master, "main", i, max_proposals=config["max_proposals"])
               for i in range(config["main_worlds"])]
    return dict(regime=REGIME, generator=GENERATOR, master_seed=master, worlds=worlds)


def manifest_bytes(manifest):
    return (json.dumps(manifest, sort_keys=True, indent=1, ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def check_world(world):
    """Independent recomputation of the mathematical contract for one world."""
    original, revised, preserving = world["original"], world["revised"], world["preserving"]
    if any(len(s) != 20 or any(type(v) is not int or not LOW <= v <= HIGH for v in s)
           for s in original + revised + preserving):
        raise ValueError(f"{world['id']}: shard shape or range")
    values = sorted(original[0] + original[1], reverse=True)
    m1, m2 = values[0], values[1]
    st = stratum(world["index"])
    owner, row = world["owner"], world["row"]
    if (m1 == m2 or m2 <= LOW or m2 == HIGH - 1 or world["original_truth"] != m1
            or world["runner_up"] != m2 or original[owner][row] != m1
            or {k: world[k] for k in st} != st):
        raise ValueError(f"{world['id']}: eligibility or stratum")
    changed = [(a, j) for a in (0, 1) for j in range(20) if original[a][j] != revised[a][j]]
    if changed != [(owner, row)] or revised[owner][row] != world["after"]:
        raise ValueError(f"{world['id']}: exactly the winning record must change")
    x = world["after"]
    if world["edit"] == "demote" and not (LOW <= x < m2 and world["revised_truth"] == m2):
        raise ValueError(f"{world['id']}: demote edit")
    if world["edit"] == "keep" and not (m2 < x <= HIGH and x != m1 and world["revised_truth"] == x):
        raise ValueError(f"{world['id']}: keep edit")
    if world["revised_truth"] != max(revised[0] + revised[1]):
        raise ValueError(f"{world['id']}: revised truth")
    p_row, p_value = world["preserving_row"], world["preserving_after"]
    changed = [(a, j) for a in (0, 1) for j in range(20) if original[a][j] != preserving[a][j]]
    if (changed != [(owner, p_row)] or p_row == row or preserving[owner][p_row] != p_value
            or world["preserving_before"] != original[owner][p_row] or not LOW <= p_value < m1):
        raise ValueError(f"{world['id']}: exactly one non-winning record must change below the winner")
    preserved = preserving[0] + preserving[1]
    if (max(preserved) != m1 or preserved.count(m1) != 1
            or [max(s) for s in preserving] != [max(s) for s in original]):
        raise ValueError(f"{world['id']}: the preserving change must keep the answer and both local maxima")
    if sorted(world["order"]) != sorted(CELLS):
        raise ValueError(f"{world['id']}: cell order")
    return True


def strata_counts(worlds):
    counts = {}
    for world in worlds:
        counts.setdefault(world["group"], [0] * 8)[world["stratum"]] += 1
    return counts


def verify_manifest(source=None, config=None):
    """Regenerate every world and require byte equality with the committed file."""
    source = Path(source or SOURCE_ROOT)
    config = config or load_config(source)
    expected = manifest_bytes(build_manifest(config))
    path = source / WORLDS_PATH
    if not path.is_file() or path.read_bytes() != expected:
        raise ValueError("configs/thesis-worlds.json differs from regenerated worlds; never edit inputs by hand")
    manifest = json.loads(expected)
    for world in manifest["worlds"]:
        check_world(world)
    counts = strata_counts(manifest["worlds"])
    main = [w for w in manifest["worlds"] if w["group"] == "main"]
    fallback = strata_counts([w for w in main if w["index"] < config["fallback_main_worlds"]])["main"]
    if counts["development"] != [2] * 8 or counts["main"] != [24] * 8 or fallback != [16] * 8:
        raise ValueError("strata are not balanced 2/16/24 per stratum")
    keys = set()
    for world in manifest["worlds"]:
        for phase in INPUTS:
            key = canonical(world[phase])
            if key in keys:
                raise ValueError("duplicate input within the thesis manifest")
            keys.add(key)
    return dict(passed=True, sha256=digest_bytes(expected), worlds=len(manifest["worlds"]),
                strata=dict(development=counts["development"], main=counts["main"], fallback=fallback))


def load_manifest(source=None):
    source = Path(source or SOURCE_ROOT)
    data = (source / WORLDS_PATH).read_bytes()
    return json.loads(data), digest_bytes(data)


def _historical_worlds(source):
    """Every exposed two-agent I-01 input committed in the repository."""
    exposed, sources = [], []

    def collect(data, location):
        count = 0
        candidates = [data]
        if isinstance(data, dict) and isinstance(data.get("manifest"), dict):
            candidates.append(data["manifest"])
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            for world in candidate.get("worlds", []):
                if (isinstance(world, dict) and {"original", "revised"} <= set(world)
                        and all(len(world[p]) == 2 and all(len(s) == 20 for s in world[p])
                                for p in ("original", "revised"))):
                    exposed.append(dict(original=world["original"], revised=world["revised"],
                                        id=location + ":" + str(world.get("id", "fixture"))))
                    count += 1
        return count

    roots = [source / "notebooks/run", source / "tests/fixtures", source / "notebooks/validation/i01-development"]
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (ValueError, UnicodeDecodeError):
                continue
            count = collect(data, path.relative_to(source).as_posix())
            if count:
                sources.append(dict(path=path.relative_to(source).as_posix(), sha256=digest_file(path), worlds=count))
        for path in sorted(root.rglob("*.zip")):
            count = 0
            try:
                with zipfile.ZipFile(path) as archive:
                    for member in archive.namelist():
                        if re.search(r"(^|/)run\.json$", member):
                            count += collect(json.loads(archive.read(member)),
                                             path.relative_to(source).as_posix() + "!" + member)
            except (zipfile.BadZipFile, ValueError, UnicodeDecodeError):
                continue
            if count:
                sources.append(dict(path=path.relative_to(source).as_posix(), sha256=digest_file(path), worlds=count))
    return exposed, sources


def build_separation(source=None):
    """Release-time exact whole-input audit against committed historical inputs."""
    source = Path(source or SOURCE_ROOT)
    manifest, sha = load_manifest(source)
    exposed, sources = _historical_worlds(source)
    if not exposed:
        raise ValueError("no historical I-01 inputs found; run from a complete repository checkout")
    result = check_disjoint_inputs(manifest["worlds"], exposed)
    # The reused I-01 check covers original and revised inputs; extend it exactly
    # to the answer-preserving inputs (overlap with history or any new input).
    known = {canonical(record[p]): record.get("id", "historical input") for record in exposed for p in ("original", "revised")}
    known.update((canonical(w[p]), w["id"] + "/" + p) for w in manifest["worlds"] for p in ("original", "revised"))
    for world in manifest["worlds"]:
        key = canonical(world["preserving"])
        if key in known:
            raise ValueError(f"Input overlap: {world['id']}/preserving and {known[key]}")
        known[key] = world["id"] + "/preserving"
    return dict(passed=result["passed"], worlds_sha256=sha,
                checked_new_inputs=result["checked_new_inputs"] + len(manifest["worlds"]),
                distinct_exposed_inputs=result["distinct_exposed_inputs"], sources=sources)


def verify_separation(source=None):
    """A source extract without history relies on the committed release receipt."""
    source = Path(source or SOURCE_ROOT)
    _, sha = load_manifest(source)
    path = source / SEPARATION_PATH
    if not path.is_file():
        raise ValueError("missing configs/thesis-worlds-separation.json release receipt")
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if not receipt.get("passed") or receipt.get("worlds_sha256") != sha or receipt.get("checked_new_inputs") != len(INPUTS) * 208:
        raise ValueError("input-separation receipt does not match the committed manifest")
    if (source / "notebooks/run").is_dir():
        fresh = build_separation(source)
        if fresh != receipt:
            raise ValueError("input-separation receipt differs from a fresh audit of this checkout")
    return receipt


def write_inputs(source=None):
    """Regenerate the committed manifest and separation receipt (release step)."""
    source = Path(source or SOURCE_ROOT)
    config = load_config(source)
    (source / WORLDS_PATH).write_bytes(manifest_bytes(build_manifest(config)))
    verify_manifest(source, config)
    receipt = build_separation(source)
    (source / SEPARATION_PATH).write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return receipt
