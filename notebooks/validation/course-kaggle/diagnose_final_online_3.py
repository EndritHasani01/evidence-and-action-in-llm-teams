"""Read-only incident diagnosis and disposable CPU continuation proof.

Run from the repository root. No weights/provider are loaded, no GPU is used,
and submitted files are never modified. The optional pinned wheel is read as
source; only its configuration-preparation function runs, with no model.
"""

import argparse
import ast
from collections import Counter
import copy
from dataclasses import asdict
import gzip
import hashlib
import inspect
import json
from pathlib import Path
import statistics
import sys
import tempfile
from types import SimpleNamespace
import zipfile


def diagnose(incident, wheel=None):
    from tokenizers import Tokenizer
    from recovery.attempts import ProcessProvider
    from recovery.prompts import COURSE_LIMITS, RenderedRequest, TokenizedRequest
    from recovery.protocol import GeneratedReply, validate_reply
    from recovery.storage import WorkerStore, record_json, settings_json
    from scripts.m5_course_preparation import peer_view
    from scripts.m5_course_smoke import hardware_plan, smoke_branch

    class NativeTokenizer:
        def __init__(self, native): self.native = native
        def encode(self, text, add_special_tokens=False):
            return self.native.encode(text, add_special_tokens=add_special_tokens).ids
        def decode(self, ids, **kwargs):
            return self.native.decode(ids, skip_special_tokens=kwargs.get("skip_special_tokens", False))

    files = {p.name: dict(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
             for p in sorted(incident.iterdir()) if p.is_file()}
    with zipfile.ZipFile(incident / "course-resume.payload") as archive:
        assert archive.testzip() is None
        manifest = json.loads(archive.read("source/source-manifest.json"))
        for name, expected in manifest["members"].items():
            raw = archive.read("source/" + name)
            assert len(raw) == expected["bytes"]
            assert hashlib.sha256(raw).hexdigest() == expected["sha256"], name
        config = json.loads(archive.read("operator-config.json"))
        gate = json.loads(archive.read("hardware-gate.json"))
        report = json.loads(archive.read("hardware/report.json"))
        packet = json.loads(gzip.decompress(archive.read(
            "source/notebooks/validation/course-m5-preparation/inputs/smoke-requests.json.gz")))
        tokenizer = NativeTokenizer(Tokenizer.from_str(archive.read("source/metadata/4B/tokenizer.json").decode()))
        original_plan = json.loads(archive.read("hardware/executed-plan.json"))["rows"]
        rows = hardware_plan(packet, tokenizer)
        assert rows == original_plan
        failures = []
        for row in rows:
            try: RenderedRequest(**row["rendered"])
            except TypeError as error:
                failures.append(dict(call_id=row["smoke_call_id"], error=str(error)))
        assert len(failures) == 2
        fixed = [dict(r, rendered={"content": r["rendered"]["content"]})
                 if r.get("hardware_diagnostic") else r for r in rows]
        for row in fixed: RenderedRequest(**row["rendered"])
        plan_by_id = {r["smoke_call_id"]: r for r in rows}
        counts, details, processes, allocation_rows = Counter(), [], [], []
        identical, reused, pending = 0, 0, []
        with tempfile.TemporaryDirectory() as directory:
            stores = []
            try:
                for index in range(2):
                    path = Path(directory) / f"worker-{index}.sqlite"
                    path.write_bytes(archive.read(f"hardware/worker-{index}.sqlite"))
                    store = WorkerStore(path); stores.append(store)
                    assert store.connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
                    allocation_rows.extend(dict(a) for a in store.connection.execute("SELECT * FROM allocations"))
                    for process in store.connection.execute("SELECT * FROM provider_processes"):
                        backend = json.loads(process["backend_json"])
                        processes.append(dict(worker=index, pid=process["pid"], started_at=process["started_at"],
                            ready_at=process["ready_at"], stopped_at=process["stopped_at"],
                            actual_tensor_devices=backend["actual_tensor_devices"], device_map=backend["device_map"],
                            recurrent_fast_path=backend["recurrent_fast_path"], attention_checks=len(backend["candidate_attention"])))
                    for call in store.connection.execute("SELECT * FROM calls"):
                        generated = json.loads(call["raw_json"]); generated["token_ids"] = tuple(generated["token_ids"])
                        row = plan_by_id[call["call_id"]]
                        validation = validate_reply(peer_view(row["view"]), GeneratedReply(**generated), tokenizer, limits=COURSE_LIMITS)
                        assert record_json(asdict(validation)) == call["validation_json"]
                        identical += 1
                        value = json.loads(call["validation_json"])
                        feedback = (value.get("feedback") or {}).get("code")
                        counts[(value["candidate"]["status"], feedback, generated["termination"])] += 1
                        attempt = store.attempts(call["call_id"])[0]
                        details.append(dict(call_id=call["call_id"], worker=index, input_tokens=row["input_tokens"],
                            generated_tokens=len(generated["token_ids"]), elapsed_seconds=attempt["elapsed_seconds"],
                            status=attempt["status"], validation=value["candidate"]["status"], feedback=feedback))
                bindings = [s.connection.execute("SELECT inputs_json FROM run_inputs").fetchone()[0] for s in stores]
                original_calls = {c["call_id"]: dict(c) for s in stores for c in s.connection.execute("SELECT * FROM calls")}
                def forbidden(*args): raise AssertionError("No provider/admission is allowed in this CPU proof")
                providers = [ProcessProvider(forbidden, before_attempt=forbidden) for s in stores]
                for row in fixed:
                    index = row["intended_worker"]; store = stores[index]
                    view = peer_view(row["view"]); rendered = RenderedRequest(**row["rendered"])
                    value = row["tokenized"]
                    tokens = TokenizedRequest(value["text"], tuple(value["input_ids"]), tuple(value["attention_mask"]))
                    store.prepare_control(smoke_branch(row), settings_json(packet["settings"]), view, rendered, tokens)
                    if row["smoke_call_id"] in original_calls:
                        providers[index].obtain(store, row["smoke_call_id"], view, rendered, tokens,
                            seed=row["seed"], settings=packet["settings"])
                        assert dict(store.call(row["smoke_call_id"])) == original_calls[row["smoke_call_id"]]
                        reused += 1
                    else: pending.append(row["smoke_call_id"])
                assert bindings == [s.connection.execute("SELECT inputs_json FROM run_inputs").fetchone()[0] for s in stores]
                assert sum(s.connection.execute("SELECT COUNT(*) FROM attempts").fetchone()[0] for s in stores) == 21
            finally:
                for store in stores: store.close()
        eos = None
        if wheel:
            from transformers import GenerationConfig
            pinned = next(w for w in manifest["candidate_wheels"] if w["name"] == "transformers")
            assert hashlib.sha256(wheel.read_bytes()).hexdigest() == pinned["sha256"]
            with zipfile.ZipFile(wheel) as distribution:
                assert Path(inspect.getfile(GenerationConfig)).read_bytes() == distribution.read("transformers/generation/configuration_utils.py")
                tree = ast.parse(distribution.read("transformers/generation/utils.py"))
            method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "_prepare_generation_config")
            for arg in method.args.args + method.args.kwonlyargs: arg.annotation = None
            method.args.kwarg.annotation = None; method.returns = None
            namespace = dict(copy=copy, GenerationConfig=GenerationConfig,
                             logger=SimpleNamespace(warning_once=lambda *args: None))
            exec(compile(ast.Module(body=[method], type_ignores=[]), "pinned-generation/utils.py", "exec"), namespace)
            native_config = json.loads(archive.read("source/metadata/4B/config.json"))
            default_eos = native_config["text_config"]["eos_token_id"]
            owner = SimpleNamespace(generation_config=GenerationConfig(eos_token_id=default_eos))
            requested = GenerationConfig(max_new_tokens=256, min_new_tokens=256, eos_token_id=None)
            inherited, _ = namespace["_prepare_generation_config"](owner, requested)
            requested.eos_token_id = []
            explicit, _ = namespace["_prepare_generation_config"](owner, requested)
            assert inherited.eos_token_id == default_eos and explicit.eos_token_id == []
            eos = dict(wheel_sha256=pinned["sha256"], native_config_implementation_identical=True,
                       model_config_eos=default_eos, current_prepared_eos=inherited.eos_token_id,
                       proposed_prepared_eos=explicit.eos_token_id, min_new_tokens=explicit.min_new_tokens,
                       max_new_tokens=explicit.max_new_tokens, scope="Actual pinned configuration function; no model or Torch execution")
        return dict(analysis_date="2026-10-13", source_commit=manifest["source_baseline_commit"],
                    incident_files=files, source_members_verified=len(manifest["members"]),
                    observed_stop_reason=report["smoke"]["stop_reason"], planner_constructor_failures=failures,
                    corrected_plan_rows_constructible=len(fixed), hardware_gate=gate,
                    recorded_attempts=len(details), raw_validations_reproduced=identical,
                    validation_groups=[dict(status=s, feedback=f, termination=t, count=n) for (s,f,t),n in counts.items()],
                    attempt_details=details, attempt_seconds_total=sum(d["elapsed_seconds"] for d in details),
                    attempt_seconds_median=statistics.median(d["elapsed_seconds"] for d in details),
                    processes=processes, observed_allocations=allocation_rows,
                    retained_prior_attempts=config["budget"]["prior_smoke_attempts"], attempt_limit=config["smoke_attempt_limit"],
                    remaining_attempts=config["smoke_attempt_limit"]-config["budget"]["prior_smoke_attempts"]-len(details),
                    disposable_continuation=dict(reused_without_provider=reused, pending_only=pending,
                                                run_bindings_unchanged=True, completed_rows_unchanged=True, new_attempts=0),
                    eos_configuration_contract=eos, investigation_gpu_calls=0, investigation_weights_loaded=False,
                    limitations=["Continuation is proven only at storage/request level; source-provenance repair is not implemented or authorized",
                                 "No full-envelope generation, pilot, freeze or main experiment in the submitted run",
                                 "EOS masking/finite-check conflict is a pinned-code prediction for the unexecuted diagnostic path"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--incident", type=Path, default=Path("notebooks/run/final-online-3"))
    parser.add_argument("--transformers-wheel", type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    print(json.dumps(diagnose(args.incident, args.transformers_wheel), indent=2))
