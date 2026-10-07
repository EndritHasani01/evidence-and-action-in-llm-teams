"""Optional local native-tokenizer checks; no model weights or inference.

Run with the existing pinned metadata directory using a tokenizer-enabled
Python. The retained scripted M3 input IDs are synthetic and must not be
misreported as native measurements; this harness supplies real saved inputs.
"""

import argparse
from dataclasses import asdict
import importlib.metadata
import json
from pathlib import Path

from recovery.evaluate import write_evaluation
from recovery.information import information_records
from recovery.prompts import RenderedRequest, rendered_data, tokenize_request
from recovery.tasks import Size, Task
from tests.information_fixture import fixture
from tests.outcome_fixture import ROOT

FIXTURE = ROOT / "tests/fixtures/information_tokens.json"


def native_counts(tokenizer):
    rows, compact = [], []
    for size in Size:
        for task in Task:
            w, b, r, inputs, attempts, committed = fixture(task, policies=("B", "K"), size=size.value)
            for saved in inputs.values():
                saved["requests"]["tokenized"] = [json.loads(json.dumps(
                    asdict(tokenize_request(RenderedRequest(request["content"]), tokenizer))))
                    for request in saved["requests"]["rendered"]]
            information = information_records(w, b, r, inputs, attempts, committed=committed, tokenizer=tokenizer)
            for row in information["prefix"]:
                saved = inputs[row["branch_id"], row["round"]]
                data = rendered_data(RenderedRequest(saved["requests"]["rendered"][row["peer"]]["content"]))
                assert len(data["history"]) == (0 if row["round"] == 1 else 1)
                expected = 0 if not data["history"] else len(tokenizer.backend_tokenizer.encode(
                    data["history"][0]["text"], add_special_tokens=False).ids)
                assert row["history_content_tokens"] == expected
                rows.append({k: row[k] for k in ("family", "size", "round", "peer", "input_tokens", "history_content_tokens")})
            for branch in b:
                if branch.policy == "K":
                    for peer in range(4):
                        saved = inputs[branch.branch_id, 1]
                        data = rendered_data(RenderedRequest(saved["requests"]["rendered"][peer]["content"]))
                        assert data["latest_candidate"]["historical"] is True
                        text = json.dumps(data["latest_candidate"], ensure_ascii=True, separators=(",", ":"))
                        expected = len(tokenizer.backend_tokenizer.encode(text, add_special_tokens=False).ids)
                        measured = next(row["history_content_tokens"] for row in information["communication"]
                                        if row["branch_id"] == branch.branch_id and row["round"] == 1 and row["peer"] == peer)
                        assert measured == expected
                        compact.append({"family": task.value, "size": size.value, "peer": peer,
                            "history_content_tokens": measured})
            # Replacing the native request IDs with synthetic measurements must fail.
            saved = next(iter(inputs.values()))
            saved["requests"]["tokenized"][0]["input_ids"][-1] += 1
            try:
                information_records(w, b, r, inputs, attempts, committed=committed, tokenizer=tokenizer)
            except ValueError as error:
                assert "exact saved input" in str(error)
            else:
                raise AssertionError("mismatching tokenizer inputs were accepted")
            print(f"Native history counts verified: {size.value}/{task.value}", flush=True)
    return {"kind": "CPU native history-content token validation, not inference or an M5 freeze",
            "definition": "Sum of independently encoded displayed retained content; excludes layout headers, not marginal request tokens",
            "packages": {name: importlib.metadata.version(name) for name in ("transformers", "tokenizers")},
            "prefix": rows, "compact_boundary": compact}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--write-fixture", type=Path)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    actual = native_counts(tokenizer)
    if args.write_fixture:
        write_evaluation(args.write_fixture, actual)
    else:
        with args.fixture.open(encoding="utf-8") as source:
            assert actual == json.load(source), "native history counts differ from retained expectations"
    print(f"Verified {len(actual['prefix'])} prefix peer-round and {len(actual['compact_boundary'])} compact-boundary counts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
