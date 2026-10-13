"""Read-only incident, mathematical and CPU meta-architecture review; no GPU.

Only pinned configuration and Hub metadata are fetched. No checkpoint weights
are downloaded and meta tensors allocate no model parameter storage.
"""

import argparse
import ast
from collections import Counter
from contextlib import closing
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
from urllib.request import urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))


def analyse():
    from recovery.manifests import load_population
    from recovery.truth import solve_world
    from recovery.evaluate import score_candidate
    from tests.references import numeric_reference, relaxation_distances
    from tokenizers import Tokenizer
    incident = ROOT/"notebooks/run/final-online-4"
    executed = json.loads((incident/"notebook-exec.ipynb").read_bytes())
    delivered = json.loads((ROOT/"notebooks/run/final-online-3/notebook-fixed.ipynb").read_bytes())
    code = lambda notebook: [ast.dump(ast.parse("".join(c["source"])))
                             for c in notebook["cells"] if c["cell_type"] == "code"]
    assert code(executed) == code(delivered)
    with zipfile.ZipFile(incident/"course-results.zip") as results:
        assert results.testzip() is None
    with zipfile.ZipFile(incident/"course-resume.payload") as archive, \
         zipfile.ZipFile(ROOT/"notebooks/run/final-online-3/course-resume.payload") as original, \
         tempfile.TemporaryDirectory() as directory:
        assert archive.testzip() is None
        manifest = json.loads(archive.read("source/source-manifest.json"))
        for name, expected in manifest["members"].items():
            raw = archive.read("source/"+name)
            assert len(raw) == expected["bytes"] and hashlib.sha256(raw).hexdigest() == expected["sha256"]
        rows = {r["smoke_call_id"]:r for r in json.loads(archive.read("hardware/executed-plan.json"))["rows"]}
        tokenizer = Tokenizer.from_str(archive.read("source/metadata/4B/tokenizer.json").decode())
        population_path = Path(directory)/"population.json"
        population_path.write_bytes(archive.read("source/tests/fixtures/population_course.json"))
        worlds = {w.world_id:w for w in load_population(population_path).development}
        calls, attempts, processes, old_equal, compact, checked, controls = [], [], [], [], [], [], []
        outcomes = Counter()
        for index in range(2):
            path, old_path = Path(directory)/f"worker-{index}.sqlite", Path(directory)/f"old-{index}.sqlite"
            path.write_bytes(archive.read(f"hardware/worker-{index}.sqlite"))
            old_path.write_bytes(original.read(f"hardware/worker-{index}.sqlite"))
            with closing(sqlite3.connect(path.as_uri()+"?mode=ro",uri=True)) as db, \
                 closing(sqlite3.connect(old_path.as_uri()+"?mode=ro",uri=True)) as previous:
                db.row_factory = previous.row_factory = sqlite3.Row
                assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
                current = [dict(r) for r in db.execute("SELECT * FROM calls")]
                physical = [dict(r) for r in db.execute("SELECT * FROM attempts")]
                old_equal.append(all(next(c for c in current if c["call_id"] == r["call_id"]) == dict(r)
                                     for r in previous.execute("SELECT * FROM calls")))
                old_equal.append(all(next(c for c in physical if (c["call_id"],c["number"]) ==
                                     (r["call_id"],r["number"])) == dict(r) for r in previous.execute("SELECT * FROM attempts")))
                calls.extend(current); attempts.extend(physical)
                processes.extend(dict(r) for r in db.execute("SELECT * FROM provider_processes"))
        assert all(old_equal)
        for call in calls:
            if call["raw_json"] is None:
                continue
            row = rows[call["call_id"]]
            raw, validation = json.loads(call["raw_json"]), json.loads(call["validation_json"])
            status = validation["candidate"]["status"]
            outcomes[(status,(validation.get("feedback") or {}).get("code"))] += 1
            if (validation.get("feedback") or {}).get("code") == "json":
                assert len(raw["token_ids"]) == 256
            try:
                parsed = json.loads(raw["text"])
            except json.JSONDecodeError:
                continue
            compact.append(dict(call_id=call["call_id"], recorded_output_tokens=len(raw["token_ids"]),
                compact_same_content_tokens=len(tokenizer.encode(json.dumps(parsed,separators=(",",":")),
                                                                 add_special_tokens=False).ids)))
            if row["view"]["slot"]["phase"] == "control":
                sources = row["view"]["sources"]
                task = row["view"]["task"]
                if task == "bfs_distance":
                    expected = relaxation_distances(8, [s["value"] for s in sources if not s["deleted"]])
                else:
                    expected = numeric_reference(task,[s["value"] for s in sorted(sources,key=lambda s:s["position"])])
                controls.append(dict(call_id=call["call_id"], task=task, visible_source_records=len(sources),
                    live_source_records=sum(not s["deleted"] for s in sources),
                    recorded_candidate=parsed["candidate"], expected=expected,
                    protocol_status=status, accepted_exact_correct=False))
            if status == "valid":
                assert row["view"]["slot"]["phase"] == "prefix"
                world = worlds[row["development_world_id"]].world
                truth = solve_world(world)
                values = [r.value for r in sorted(world.records,key=lambda r:r.position)]
                assert truth.candidate(None) == numeric_reference(world.task.value,values)
                candidate = parsed["candidate"]
                checked.append(dict(call_id=call["call_id"], expected=truth.candidate(row["view"]["peer"]),
                    candidate=candidate, exact_correct=bool(score_candidate(truth,status,candidate,row["view"]["peer"])),
                    visible_sources=len(row["view"]["sources"])))
        timed = [r for r in attempts if r["call_id"].startswith("course-hardware/")]
        assert len(timed) == 1 and timed[0]["status"] == "timeout" and not timed[0]["backend_json"]
        process = next(r for r in processes if r["call_id"] == timed[0]["call_id"])
        startup = (datetime.fromisoformat(process["ready_at"])-datetime.fromisoformat(process["started_at"])).total_seconds()
        config = json.loads(archive.read("operator-config.json"))
        coverage = json.loads(archive.read("analyses/20261013T115050859262Z/report.json"))["coverage"]
        assert coverage == dict(protocol_outcomes={"unknown":6280},recorded=0,scheduled=6280,unknown=6280)
        report = dict(analysis_date="2026-10-13", source_commit=manifest["source_baseline_commit"],
            incident_files={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                            for p in incident.iterdir() if p.is_file()}, source_members_verified=len(manifest["members"]),
            original_21_call_and_attempt_rows_identical=True, physical_attempts_current=len(attempts),
            delivered_code_cells_ast_equal=True, submitted_archives_crc_passed=True,
            cumulative_attempts=len(attempts)+config["budget"]["prior_smoke_attempts"], attempt_limit=config["smoke_attempt_limit"],
            native_timeout=timed[0], provider_startup_seconds=startup,
            available_after_ready_before_deadline_seconds=120-startup, provider_termination_confirmed=bool(process["stopped_at"]),
            hardware_gate=json.loads(archive.read("hardware-gate.json")),
            native_preflight=json.loads(archive.read("environment-receipts/gpu-environment/hardware-plan-contract.json")),
            protocol_outcomes=[dict(status=s,reason=f,count=n) for (s,f),n in outcomes.items()],
            valid_candidates_checked=checked, accepted_correct_smoke_replies=sum(r["exact_correct"] for r in checked),
            full_information_controls=controls,
            compact_serialization_diagnostic=compact,
            compact_diagnostic_scope="Same parsed content, re-encoded on CPU; no repaired/rescored replies or new model outputs",
            full_envelope_memory_peak=None, full_envelope_decode_steps=None,
            native_failure_scope="Known 120-second terminal timeout; no OOM or full-envelope memory/headroom result established",
            original_model_quality_scope="Stress witnesses are not the first-90 capability sample; initial private views can be underinformed",
            main_coverage=coverage, investigation_gpu_calls=0)
        four = json.loads(archive.read("source/metadata/4B/config.json"))
    revision = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"
    url = f"https://huggingface.co/Qwen/Qwen3.5-9B/resolve/{revision}/config.json"
    with urlopen(url,timeout=30) as response:
        raw = response.read()
    assert hashlib.sha256(raw).hexdigest() == "d0883072e01861ed0b2d47be3c16c36a8e81c224c7ffaa310c6558fb3f932b05"
    nine = json.loads(raw)
    with urlopen(f"https://huggingface.co/api/models/Qwen/Qwen3.5-9B/revision/{revision}?blobs=true",timeout=30) as response:
        hub = json.load(response)
    assert hub["sha"] == revision
    import torch
    from transformers import Qwen3_5TextConfig, Qwen3_5ForCausalLM
    estimates = []
    for label, outer in (("4B",four),("9B",nine)):
        text = dict(outer["text_config"],tie_word_embeddings=outer["tie_word_embeddings"])
        with torch.device("meta"):
            model = Qwen3_5ForCausalLM(Qwen3_5TextConfig(**text))
        parameters = dict(model.named_parameters())
        quantized = {n+".weight" for n,m in model.named_modules() if isinstance(m,torch.nn.Linear) and n != "lm_head"}
        packed = sum((parameters[n].numel()+1)//2 for n in quantized)
        other = sum(p.numel()*2 for n,p in parameters.items() if n not in quantized)
        assert all(p.device.type == "meta" for p in parameters.values())
        kv = 2*sum(t=="full_attention" for t in text["layer_types"])*text["num_key_value_heads"]*text["head_dim"]*2*110107
        estimates.append(dict(model=label, language_parameters=sum(p.numel() for p in parameters.values()),
            quantized_matrices=len(quantized), ideal_packed_nf4_bytes=packed, nonquantized_fp16_bytes=other,
            full_envelope_kv_bytes=kv, conditional_subtotal_gib=(packed+other+kv)/2**30,
            scope="Meta architecture only; excludes quantization metadata, FP32 exceptions, live workspace, transient buffers and fragmentation"))
        del model
    report["model_review"] = dict(recommended_candidate="Qwen/Qwen3.5-9B",revision=revision,
        official_config_url=url, config_sha256=hashlib.sha256(raw).hexdigest(), config=nine,
        checkpoint_bytes=sum(s["lfs"]["size"] for s in hub["siblings"] if s["rfilename"].endswith(".safetensors") and s.get("lfs")),
        estimates=estimates, reference_envelope_tokens=110107, new_renderer_envelope_requires_recomputation=True,
        native_9B_acceptance=False, checkpoint_weights_downloaded=False, meta_only=True,
        torch=torch.__version__)
    return report


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result=analyse()
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("cumulative_attempts","provider_startup_seconds","accepted_correct_smoke_replies")}))
