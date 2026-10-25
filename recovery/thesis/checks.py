"""CPU acceptance checks run before any GPU stage (specification section 5).

They need no GPU and no weights. Real tokenizer files (small) are downloaded
for the capacity proof unless the study is a scripted rehearsal.
"""

from copy import deepcopy
import json
from pathlib import Path
import tempfile

from ..i01.core import canonical, next_agent
from . import CELLS, CHANGE_CELLS, MODELS, PRESERVING_CELLS, REGIME, RETAIN_CELLS, REVISION_CELLS
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
            retained = cell in RETAIN_CELLS
            assert state["history"] == (prefix["history"] if retained else [[], []])
            assert state["earlier"] == ([len(h) for h in prefix["history"]] if retained else [0, 0])
            assert (state["turns"], state["submissions"], state["waiting"], state["next"]) == (
                [0, 0], [None, None], [False, False], world["first"])
            for agent in (0, 1):
                v = protocol.view(world, state, agent)
                assert set(v) == {"agent", "phase", "invocation", "partner_finished", "history", "earlier", "notice", "shard"}
                expected = (world["revised"] if cell in REVISION_CELLS else
                            world["preserving"] if cell in PRESERVING_CELLS else world["original"])[agent]
                assert v["shard"] == expected and v["partner_finished"] is False and v["phase"] == "new"
                if cell in CHANGE_CELLS:
                    row = world["row"] if cell in REVISION_CELLS else world["preserving_row"]
                    assert v["notice"]["kind"] == "change" and v["notice"]["record"] == row
                    assert ("value" in v["notice"]) == (agent == world["owner"])
                else:
                    assert v["notice"] == {"kind": "none"}
                rendered = protocol.messages(v)
                text = rendered[1]["content"]
                assert rendered[0]["content"] == protocol.THESIS_SYSTEM and f"agent {agent} record 0:" in text
                assert ("Replacement value" in text) == (cell in CHANGE_CELLS and agent == world["owner"])
                lowered = (rendered[0]["content"] + text).lower()
                for forbidden in ("demote", "stratum", "holder", "runner", "answer changed", "retain", "clear",
                                  "preserv", "irrelevant", "unchanged answer", "still valid"):
                    assert forbidden not in lowered, forbidden
                for word in CELLS:
                    assert f" {word} " not in text and f"{word}:" not in text
        # Retained earlier-phase blocks of RV, RP and RN are byte-identical.
        blocks = {cell: protocol.messages(protocol.view(world, starts[cell], 0))[1]["content"].split(
            "VISIBLE HISTORY: THIS PHASE")[0] for cell in RETAIN_CELLS}
        assert len(set(blocks.values())) == 1
        # Both change notices share one form; only the record (and the owner's value) differ.
        for agent in (0, 1):
            rv, rp = (protocol.view(world, starts[cell], agent)["notice"] for cell in ("RV", "RP"))
            assert set(rv) == set(rp) and (rv["kind"], rv["owner"]) == (rp["kind"], rp["owner"])
            assert protocol.notice_text(dict(rv, **{k: rp[k] for k in ("record", "value") if k in rp})) == \
                protocol.notice_text(rp)
            for cell, notice in (("RV", rv), ("RP", rp)):
                text = protocol.messages(protocol.view(world, starts[cell], agent))[1]["content"]
                assert "ENVIRONMENT NOTICE\n" + protocol.notice_text(notice) + "\n\n" in text
                assert protocol.notice_text(notice).startswith(protocol.NOTICE_CHANGE)
        # The preserving change keeps the original answer.
        assert protocol.cell_truth(world, "RP") == protocol.cell_truth(world, "CN") == world["original_truth"]
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
    # Preserving witness: the non-owner's first RV and RP views differ only in the
    # named record index, although only RV changes the answer.
    rv, rp = (protocol.view(base, protocol.start(base, "qwen", cell, prefix), other) for cell in ("RV", "RP"))
    unnamed = lambda v: canonical(dict(v, notice=dict(v["notice"], record=None)))  # noqa: E731
    assert rv["notice"]["record"] != rp["notice"]["record"] and unnamed(rv) == unnamed(rp)
    assert protocol.cell_truth(base, "RV") != protocol.cell_truth(base, "RP")
    # Invalid action: turn consumed, nothing delivered, feedback text recorded.
    world = worlds["dev-01"]
    state = protocol.start(world, "qwen", "prefix")
    agent = next_agent(state)
    after = protocol.apply(state, agent, None, "malformed_action", "x", "Invalid: output one JSON object.")
    assert after["turns"][agent] == 1 and after["history"][1 - agent] == [] and \
        after["history"][agent][-1] == dict(kind="feedback", text="Invalid: output one JSON object.")
    return ["literal retain/clear starts (six cells)", "notices and owner-only replacement", "view keys and privacy",
            "byte-identical retained history", "one change-notice form for both edits",
            "information witness (demote vs keep; revision vs preserving)", "invalid action"]


HAND_TABLE = [  # the hand-scored example of specification section 3.10
    dict(prefix=1, RV=0, CV=1, RP=1, CP=1, RN=1, CN=1), dict(prefix=1, RV=0, CV=0, RP=1, CP=0, RN=1, CN=0),
    dict(prefix=1, RV=1, CV=0, RP=0, CP=1, RN=1, CN=1), dict(prefix=0, RV=0, CV=0, RP=0, CP=0, RN=0, CN=0),
    dict(prefix=1, RV=0, CV=1, RP=1, CP=1, RN=1, CN=1), dict(prefix=1, RV=0, CV=0, RP=0, CP=1, RN=1, CN=1),
    dict(prefix=0, RV=0, CV=0, RP=1, CP=0, RN=1, CN=0), dict(prefix=1, RV=1, CV=1, RP=1, CP=1, RN=1, CN=1)]


def check_analysis():
    """The hand-scored example of specification section 3.10, including the decomposition identity."""
    from .analysis import LINEAR, stratified_mean, world_value
    table = [dict(ys) for ys in HAND_TABLE]
    strata = list(range(8))
    values = {n: stratified_mean([world_value(LINEAR[n][0], ys) for ys in table], strata)
              for n in ("delta_H", "delta_E", "theta", "delta_announce", "delta_answer", "reopening")}
    assert values == dict(delta_H=0.125, delta_E=0.4375, theta=0.375, delta_announce=0.125, delta_answer=0.3125,
                          reopening=0.125), values
    for ys in table:  # delta_E = delta_announce + delta_answer holds world by world
        assert world_value(LINEAR["delta_E"][0], ys) == (world_value(LINEAR["delta_announce"][0], ys) +
                                                         world_value(LINEAR["delta_answer"][0], ys))
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
    return ["hand-scored estimands", "decomposition identity", "missingness bounds", "interval indices",
            "Hoeffding companion"]


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
