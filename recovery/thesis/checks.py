"""CPU acceptance checks run before any GPU stage (specification section 5).

They need no GPU and no weights. Real tokenizer files (small) are downloaded
for the capacity proof unless the study is a scripted rehearsal.
"""

from copy import deepcopy
import json
from pathlib import Path
import tempfile

from ..i01.core import canonical, next_agent
from . import CELLS, MODELS, REGIME
from . import protocol
from .worlds import load_manifest, verify_manifest, verify_separation


def scripted_prefix(world, model="qwen"):
    """A fixed legal prefix: agent reports, partner submits, agent submits."""
    state = protocol.start(world, model, "prefix")
    first, other = world["first"], 1 - world["first"]
    local = [max(s) for s in world["original"]]
    script = {first: [dict(message=f"My local maximum is {local[first]}.", submit=None, wait=False),
                      dict(message=None, submit=world["original_truth"], wait=False)],
              other: [dict(message=f"Mine is {local[other]}; submitting {world['original_truth']}.",
                           submit=world["original_truth"], wait=False)]}
    used = {0: 0, 1: 0}
    while (agent := next_agent(state)) is not None:
        action = script[agent][used[agent]]
        used[agent] += 1
        state = protocol.apply(state, agent, action, None, f"scripted/{agent}/{used[agent]}")
    return state


def check_protocol(manifest):
    """Literal retention, notices, privacy of views, scoring and the information witness."""
    worlds = {w["id"]: w for w in manifest["worlds"]}
    for wid in ("dev-00", "dev-04", "main-005"):
        world = worlds[wid]
        prefix = scripted_prefix(world)
        assert prefix["terminal"] == "both_submitted" and protocol.score(world, prefix) == 1
        starts = {cell: protocol.start(world, "qwen", cell, prefix) for cell in CELLS}
        for cell, state in starts.items():
            retained = cell in ("RV", "RN")
            assert state["history"] == (prefix["history"] if retained else [[], []])
            assert state["earlier"] == ([len(h) for h in prefix["history"]] if retained else [0, 0])
            assert (state["turns"], state["submissions"], state["waiting"], state["next"]) == (
                [0, 0], [None, None], [False, False], world["first"])
            for agent in (0, 1):
                v = protocol.view(world, state, agent)
                assert set(v) == {"agent", "phase", "invocation", "partner_finished", "history", "earlier", "notice", "shard"}
                expected = (world["revised"] if cell in ("RV", "CV") else world["original"])[agent]
                assert v["shard"] == expected and v["partner_finished"] is False and v["phase"] == "new"
                if cell in ("RV", "CV"):
                    assert v["notice"]["kind"] == "change" and ("value" in v["notice"]) == (agent == world["owner"])
                else:
                    assert v["notice"] == {"kind": "none"}
                rendered = protocol.messages(v)
                text = rendered[1]["content"]
                assert rendered[0]["content"] == protocol.THESIS_SYSTEM and f"agent {agent} record 0:" in text
                assert ("Replacement value" in text) == (cell in ("RV", "CV") and agent == world["owner"])
                lowered = (rendered[0]["content"] + text).lower()
                for forbidden in ("demote", "stratum", "holder", "runner", "answer changed", "retain", "clear"):
                    assert forbidden not in lowered, forbidden
                for word in CELLS:
                    assert f" {word} " not in text and f"{word}:" not in text
        # Retained earlier-phase blocks of RV and RN are byte-identical.
        rv = protocol.messages(protocol.view(world, starts["RV"], 0))[1]["content"]
        rn = protocol.messages(protocol.view(world, starts["RN"], 0))[1]["content"]
        assert rv.split("VISIBLE HISTORY: THIS PHASE")[0] == rn.split("VISIBLE HISTORY: THIS PHASE")[0]
    # Information witness: same non-owner view, different answers (demote vs keep).
    base = deepcopy(worlds["dev-00"])
    owner, row = base["owner"], base["row"]
    other = 1 - owner
    demote, keep = deepcopy(base), deepcopy(base)
    demote["revised"][owner][row] = base["runner_up"] - 1
    demote["revised_truth"] = base["runner_up"]
    keep["revised"][owner][row] = base["runner_up"] + 1 if base["runner_up"] + 1 != base["before"] else base["runner_up"] + 2
    keep["revised_truth"] = keep["revised"][owner][row]
    for w, value in ((demote, demote["revised"][owner][row]), (keep, keep["revised"][owner][row])):
        w["after"] = value
    prefix = scripted_prefix(base)
    views = [protocol.view(w, protocol.start(w, "qwen", "RV", prefix), other) for w in (demote, keep)]
    assert canonical(views[0]) == canonical(views[1]) and demote["revised_truth"] != keep["revised_truth"]
    # Invalid action: turn consumed, nothing delivered, feedback text recorded.
    world = worlds["dev-01"]
    state = protocol.start(world, "qwen", "prefix")
    agent = next_agent(state)
    after = protocol.apply(state, agent, None, "malformed_action", "x", "Invalid: output one JSON object.")
    assert after["turns"][agent] == 1 and after["history"][1 - agent] == [] and \
        after["history"][agent][-1] == dict(kind="feedback", text="Invalid: output one JSON object.")
    return ["literal retain/clear starts", "notices and owner-only replacement", "view keys and privacy",
            "byte-identical retained history", "information witness (demote vs keep)", "invalid action"]


def check_analysis():
    """The hand-scored example of specification section 3.10."""
    from .analysis import LINEAR, stratified_mean, world_value
    table = [dict(RV=0, CV=1, RN=1, CN=1), dict(RV=0, CV=0, RN=1, CN=0), dict(RV=1, CV=0, RN=1, CN=1),
             dict(RV=0, CV=0, RN=0, CN=0), dict(RV=0, CV=1, RN=1, CN=1), dict(RV=0, CV=0, RN=1, CN=1),
             dict(RV=0, CV=0, RN=1, CN=0), dict(RV=1, CV=1, RN=1, CN=1)]
    strata = list(range(8))
    values = {n: stratified_mean([world_value(LINEAR[n][0], ys) for ys in table], strata)
              for n in ("delta_H", "delta_E", "theta")}
    assert values == dict(delta_H=0.125, delta_E=0.4375, theta=0.375), values
    missing = [dict(ys) for ys in table]
    missing[3]["CV"] = None
    low = stratified_mean([world_value(LINEAR["delta_H"][0], ys, "min") for ys in missing], strata)
    high = stratified_mean([world_value(LINEAR["delta_H"][0], ys, "max") for ys in missing], strata)
    e_low = stratified_mean([world_value(LINEAR["delta_E"][0], ys, "min") for ys in missing], strata)
    e_high = stratified_mean([world_value(LINEAR["delta_E"][0], ys, "max") for ys in missing], strata)
    assert (low, high, e_low, e_high) == (0.125, 0.25, 0.375, 0.4375)
    from .analysis import hoeffding, interval_indices
    assert interval_indices(10000, 0.975) == (125, 9874) and interval_indices(10000, 0.95) == (250, 9749)
    assert round(hoeffding([s for s in range(8) for _ in range(24)], 2, 0.025), 3) == 0.214
    return ["hand-scored estimands", "missingness bounds", "interval indices", "Hoeffding companion"]


def check_checkpoint():
    """Export, verify and restore a tiny store in a temporary directory."""
    from ..i01.store import Store
    from . import checkpoint as ckpt
    with tempfile.TemporaryDirectory(prefix="thesis-check-") as temp:
        run = Path(temp) / "run"
        run.mkdir()
        (run / "inputs").mkdir()
        (run / "inputs" / "note.txt").write_text("inputs", encoding="utf-8")
        binding = dict(regime=REGIME, study="selfcheck")
        store = Store(run / "study.sqlite", binding, create=True)
        store.start("e", dict(terminal=None))
        receipt = ckpt.export(run, store, study="selfcheck", session="s", reason="check")
        store.close()
        target = Path(temp) / "restored"
        manifest = ckpt.restore(Path(receipt["path"]), target)
        assert manifest["seq"] == 1 and (target / "study.sqlite").exists()
        restored = Store(target / "study.sqlite", binding)
        assert restored.meta("checkpoint_seq") == 1 and restored.state("e") == dict(terminal=None)
        restored.close()
    return ["checkpoint export/verify/restore"]


def capacity(config, scripted, scratch, receipts, progress=print):
    """Worst reachable request per model; fixes the uniform input limit."""
    from .models import ScriptedTokenizer, capacity_bound, load_tokenizer
    bounds, templates = {}, {}
    for model in MODELS:
        if scripted:
            tokenizer = ScriptedTokenizer()
        else:
            from .assets import download
            receipt = download(model, scratch, receipts, weights=False, config=config, progress=progress)
            tokenizer = load_tokenizer(config, model, receipt["snapshot"])
        bounds[model] = capacity_bound(config, model, tokenizer, config["input_tokens"])
        templates[model] = bounds[model]["chat_template_sha256"]
    limit = (config["input_tokens"] if all(b["fits"] for b in bounds.values())
             else config["alternative_input_tokens"])
    if limit != config["input_tokens"]:
        for model in MODELS:
            tokenizer = ScriptedTokenizer() if scripted else None
            if tokenizer is None:
                from .assets import download
                receipt = download(model, scratch, receipts, weights=False, config=config, progress=progress)
                tokenizer = load_tokenizer(config, model, receipt["snapshot"])
            bounds[model] = capacity_bound(config, model, tokenizer, limit)
            if not bounds[model]["fits"]:
                raise ValueError(f"{model}: worst request exceeds even the 12,288 alternative; stop for an amendment")
    return dict(input_limit=limit, bounds=bounds, templates=templates)


def run_checks(source, config, *, scripted, scratch, receipts, progress=print):
    manifest_receipt = verify_manifest(source, config)
    separation = verify_separation(source)
    manifest, _ = load_manifest(source)
    done = ["manifest regenerated byte for byte; strata 2/16/24", "input separation receipt"]
    done += check_protocol(manifest)
    done += check_analysis()
    done += check_checkpoint()
    cap = capacity(config, scripted, scratch, receipts, progress)
    done.append(f"capacity bounds: " + ", ".join(f"{m} {b['conservative_input_bound']}" for m, b in cap["bounds"].items())
                + f" -> input limit {cap['input_limit']}")
    return dict(passed=True, checks=done, manifest=manifest_receipt, separation_checked=separation["checked_new_inputs"],
                input_limit=cap["input_limit"], bounds=cap["bounds"], templates=cap["templates"], model_attempts=0)
