"""Verify course durable parent/replay requests with local pinned native metadata."""

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from recovery.inference import QWEN_4B, candidate_settings
from recovery.prompts import COURSE_LIMITS, render_request, tokenize_request
from recovery.replay import held_prose_counts
from recovery.runner import DurableRunner
from tests.course_worker_cases import BOUNDS, branches, prefix_branch, scheduled, sort_world
from tests.durable_checks import forbidden
from tests.event_checks import event_provider
from tests.lifecycle_archive import retain
from tests.lifecycle_fixture import scientific_records, write_json
from tests.replay_checks import replay_provider

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--native-packages", type=Path, help="existing auxiliary CPU tokenizer packages; no study environment change")
    args = parser.parse_args()
    assert not args.output.exists() and not args.bundle.exists()
    if args.native_packages:
        sys.path.append(str(args.native_packages.resolve()))
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(str(args.tokenizer), local_files_only=True)
    settings = candidate_settings(tokenizer, QWEN_4B, limits=COURSE_LIMITS)
    world = sort_world()
    prefix = prefix_branch(world)
    selected = (prefix, *(scheduled(world, "revision", p) for p in ("B", "C", "P_G", "Q_B")),
                *(b for b in branches(world) if b.phase == "control"))
    with tempfile.TemporaryDirectory(prefix="course-native-workers-") as temporary:
        root = Path(temporary)
        parent, child = root / "parent.sqlite", root / "child.sqlite"
        prefix_provider = event_provider(tokenizer)
        def provide_prefix(view, rendered, tokenized, *, seed, settings):
            return prefix_provider(view, rendered, tokenized)
        with DurableRunner(parent, tokenizer, provide_prefix, scripted=True) as runner:
            runner.store.bind_run((world,), selected, settings, BOUNDS, regime="course")
            runner.start(world, prefix, settings=settings)
            for r in range(1, 5): runner.run_round(prefix.branch_id, r)
            runner.reply_provider = replay_provider(tokenizer, "unicode")
            for branch in selected[1:3]:
                runner.start(world, branch, settings=settings)
                runner.run_round(branch.branch_id, 1)
        original = scientific_records((parent,))
        with DurableRunner(child, tokenizer, forbidden, scripted=True, dependencies=(parent,)) as runner:
            runner.store.bind_run((world,), selected, settings, BOUNDS, regime="course")
            for branch in selected[3:5]:
                runner.start(world, branch, settings=settings)
                result = runner.run_round(branch.branch_id, 1)
                assert [r.candidate.status for r in result.barrier.replies] == ["valid", "valid", "invalid", "failed"]
                for call in branch.calls[:4]:
                    assert runner.store.response(call.call_id) == runner.store.response(call.replay_parent)
                    assert not runner.store.attempts(call.call_id)
                assert any(held_prose_counts(result.committed)) == (branch.policy == "Q_B")
            runner.reply_provider = replay_provider(tokenizer, "rich")
            q = selected[4]
            for r in range(2, 5): runner.run_round(q.branch_id, r)
            runner.backup(root / "backup.sqlite")
            for branch in selected[3:5]:
                for r in range(1, 5 if branch.policy == "Q_B" else 2):
                    _, saved_settings, requests = runner.store.inputs(branch.branch_id, r)
                    assert json.loads(saved_settings) == settings
                    for view, rendered, tokens in zip(requests.views, requests.rendered, requests.tokenized):
                        assert rendered == render_request(view, limits=COURSE_LIMITS)
                        assert tokens == tokenize_request(rendered, tokenizer, limits=COURSE_LIMITS)
        assert original == scientific_records((parent,))
        assert scientific_records((child,)) == scientific_records((root / "backup.sqlite",))
        with DurableRunner(root / "backup.sqlite", tokenizer, forbidden, scripted=True, dependencies=(parent,)) as runner:
            runner.start(world, selected[4], settings=settings)
            runner.run_round(selected[4].branch_id, 4)
        assert scientific_records((child,)) == scientific_records((root / "backup.sqlite",))
        (root / "inputs").mkdir()
        for source, name in (("population_course.json", "population.json"), ("schedules_course.json", "schedules.json")):
            shutil.copyfile(ROOT / "tests/fixtures" / source, root / "inputs" / name)
        record = dict(model=QWEN_4B.model, revision=QWEN_4B.revision, tokenizer_directory=str(args.tokenizer.resolve()),
            files={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in args.tokenizer.iterdir() if p.is_file()},
            native_packages=str(args.native_packages.resolve()) if args.native_packages else None,
            packages={p: importlib.metadata.version(p) for p in ("pydantic", "transformers", "tokenizers", "langgraph", "langgraph-checkpoint-sqlite")},
            prefix_rounds=4, parent_rounds=2, replay_uses=8, q_rounds=4,
            exact_native_request_checks=20, parent_unchanged=True, backup_reopen_equal=True, model_calls=0)
        write_json(root / "evidence.json", record)
        retain(root, args.bundle)
        write_json(args.output, record)
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
