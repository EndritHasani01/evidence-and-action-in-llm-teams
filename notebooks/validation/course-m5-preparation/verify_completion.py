"""Audit course preparation completion, unchanged prerequisites and pending hardware gates."""

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import runpy
import sys
from urllib.parse import unquote

from verify_preparation import ROOT, FOLDER, read, git

DOCUMENTS = {"README.md", "docs/IMPLEMENTATION_PLAN.md", "docs/todos/course/README.md",
    "docs/planning/course-study-session-handoff.md",
    "docs/todos/course/M5/M5-T01-course-inference-and-smoke-preparation.md",
    "docs/todos/course/M5/M5-T02-course-hardware-smoke-and-memory.md",
    "docs/validation/course-m5-inference-and-smoke-preparation.md",
    "docs/validation/course-m5-r7-offline-review.md",
    "docs/validation/course-m5-preparation-completion.md"}
CHANGED_CODE = {"scripts/build_course_smoke_packet.py", "tests/test_course_smoke_preparation.py",
    "notebooks/validation/course-m5-preparation/verify_notebook.py"}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def passed_suite(folder, label, count, skips=0):
    receipt = read(folder/(label+"-command.json"))
    log = gzip.decompress((folder/receipt["log"]).read_bytes()).decode("utf-8")
    assert receipt["exit_code"] == 0 and re.findall(r"Ran (\d+) tests?", log) == [str(count)], label
    actual_skips = int(re.search(r"OK \(skipped=(\d+)\)", log)[1]) if "OK (skipped=" in log else 0
    assert actual_skips == skips, label
    return dict(methods=count, skips=skips, source_head=receipt["source_head"], exit_code=0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists(), "Preserve previous evidence"
    r7 = ROOT/"notebooks/validation/course-m5-r7"
    baseline = read(r7/"baseline-files.json.gz")
    protected = {p:h for p,h in baseline["files"].items() if p not in DOCUMENTS | CHANGED_CODE}
    for path, expected in protected.items():
        assert digest(ROOT/path) == expected, path
    assert not git("diff", "a1ae47b", "--name-only", "--", "notebooks/validation/course-m5-r7")
    plan = (ROOT/"docs/IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")
    previous_plan = git("show", baseline["head"]+":docs/IMPLEMENTATION_PLAN.md")
    assert plan.split("## 11. Course living handoff")[0] == previous_plan.split("## 11. Course living handoff")[0]
    installed = read(FOLDER/"installed-provenance.json")
    assert installed["matching_modules"] == len(installed["modules"]) == 29 and not installed["source_pythonpath"]
    for name, expected in installed["modules"].items():
        assert digest(ROOT/"recovery"/name) == expected, name
    prior = read(ROOT/"notebooks/validation/course-m4-report/completion-audit.json")
    assert prior["status"] == "passed" and prior["plan_rows"] == 22 and prior["consistency_categories"] == 7
    assert all(v == "passed and unchanged" for v in prior["prerequisite_audits"].values())
    reused = {label:passed_suite(FOLDER,label,count) for label,count in (
        ("source-final",64),("installed-corrected",64),("native-course-final",4),("native-installed",4))}
    reused.update({label:passed_suite(r7,label,5) for label in (
        "native-tightening-source", "outside-native", "loading-review-source")})
    focused = passed_suite(FOLDER, "completion-focused-final", 11)
    for label in ("completion-packet-build-final", "completion-notebook-final"):
        assert read(FOLDER/(label+"-command.json"))["exit_code"] == 0
    packet = FOLDER/"completion-packet"
    manifest, receipt, report = [read(packet/name) for name in (
        "source-manifest.json.gz", "verification.json", "report.json")]
    assert manifest["source_baseline_commit"] == receipt["source_commit"] == focused["source_head"]
    sys.path.insert(0, str(ROOT))
    from scripts.build_course_smoke_packet import SOURCE_PATHS, preparation_review
    assert not git("diff", manifest["source_baseline_commit"], "--name-only", "--", *SOURCE_PATHS)
    assert manifest["preparation"] == report["preparation"] == preparation_review(ROOT)
    assert report["status"] == "prepared" and receipt["preparation_complete"] and report["prepared_requests"] == 24
    assert receipt["notebook_cells_executed"] == 3 and len(receipt["reopened_closed_exports"]) == 2
    assert receipt["wrong_source_rejected"] and receipt["existing_output_preserved"]
    assert manifest["archive_sha256"] == receipt["payload_sha256"] == digest(ROOT/"dist/course-m5-preparation-v3"/manifest["payload_filename"])
    assert digest(packet/"preflight-results.zip") == receipt["export_zip_sha256"]
    assert not report["gpu_admission"] and not report["runtime_freeze"] and not report["pretrained_weights_staged"]
    assert report["model_generations"] == 0
    assert all(report[k] is None for k in ("provider_quota", "provider_duration", "prior_allocation", "provider_release"))
    for folder, filename in ((ROOT/"dist/m5-kaggle-source-v2", "source-manifest.json"),
                             (FOLDER/"packet", "source-manifest.json.gz")):
        old = read(folder/filename)
        location = ROOT/"dist/course-m5-preparation-v1" if folder == FOLDER/"packet" else folder
        assert digest(location/old["payload_filename"]) == old["archive_sha256"], location
    states = {p.stem[:6]:re.search(r"\*\*Status:\*\* (\w+)",p.read_text(encoding="utf-8"))[1]
        for p in (ROOT/"docs/todos/course").glob("M*/*.md")}
    index = (ROOT/"docs/todos/course/README.md").read_text(encoding="utf-8")
    assert dict(re.findall(r"\| \[(M\d-T\d\d)[^\n]+?\| (ready|active|blocked|done) \|",index)) == states
    assert Counter(states.values()) == dict(done=12,blocked=9)
    assert states["M5-T01"] == "done" and states["M5-T02"] == "blocked"
    assert all(states[k] == "done" for k in ("M2-T03", "M3-T02", "M4-T04"))
    assert all(states[k] == "blocked" for k in states if k.startswith("M6"))
    for milestone,done,total,active,ready,blocked in re.findall(r"\| (M\d) \| (\d+)/(\d+) \| (\d+) \| (\d+) \| (\d+) \|",index):
        counts = Counter(v for k,v in states.items() if k.startswith(milestone))
        assert sum(counts.values()) == int(total)
        assert tuple(map(int,(done,active,ready,blocked))) == tuple(counts[k] for k in ("done","active","ready","blocked"))
    assert tuple(map(int,re.search(r"\*\*(\d+)/21 course tasks done; (\d+) remaining; (\d+) active; (\d+) ready; (\d+) blocked",index).groups())) == (12,9,0,0,9)
    helper = ROOT/"notebooks/validation/m5-attention-memory/check_document_links.py"
    sys.path.insert(0,str(helper.parent))
    anchors = runpy.run_path(str(helper))["anchors"]
    changed = {(ROOT/name).resolve() for name in DOCUMENTS}
    links = fragments = inbound = 0
    for source in sorted(set(ROOT.glob("docs/**/*.md")) | {ROOT/"README.md",ROOT/"tests/fixtures/README.md"}):
        for target in re.findall(r"\[[^\]]+\]\(([^()\n]+)\)", source.read_text(encoding="utf-8")):
            target = target.strip().strip("<>")
            if re.match(r"[a-z]+://|mailto:",target):
                continue
            name,_,fragment = target.partition("#")
            name = re.sub(r":\d+(?:-\d+)?$","",unquote(name))
            resolved = (source.parent/name).resolve() if name else source.resolve()
            if source.resolve() not in changed and resolved not in changed:
                continue
            assert resolved.exists() or resolved == args.output.resolve(), (source,target)
            links += 1
            inbound += source.resolve() not in changed
            if fragment and resolved.suffix == ".md":
                assert unquote(fragment) in anchors(resolved), (source,target)
                fragments += 1
    assert not git("diff","--check")
    result = dict(status="passed",task_status="done",audited_head=git("rev-parse","HEAD"),
        protected_files_identical=len(protected),plan_sections_1_to_10_identical=True,
        installed_production_modules_identical=29,prior_m1_m4_gate_unchanged=True,
        r7_checkpoint_artifacts_unchanged=True,historical_source_packets_preserved=True,
        reused_suites=reused,focused_suite=focused,course_task_states=dict(Counter(states.values())),
        packet_source_commit=manifest["source_baseline_commit"],payload_sha256=manifest["archive_sha256"],
        source_members=receipt["source_members"],closed_exports_reopened=2,preparation=report["preparation"],
        local_references=links,markdown_fragments=fragments,inbound_references=inbound,
        model_generations=0,gpu_execution=False,weights_staged=False,runtime_freeze=False)
    with args.output.open("x",encoding="utf-8",newline="\n") as output:
        json.dump(result,output,indent=2)
        output.write("\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
