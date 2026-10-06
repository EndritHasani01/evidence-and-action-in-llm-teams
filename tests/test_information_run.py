"""Saved record joins, literal visibility, acquisition and offline CLI checks."""

import copy
import gzip
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recovery.evaluate import read_records
from recovery.information import information_records, information_run
from recovery.tasks import Task
from tests.information_fixture import CharacterTokenizer, fixture, set_sources
from tests.outcome_fixture import ROOT, encode, write_worker


class InformationRunTests(unittest.TestCase):
    def test_all_prefix_rounds_actual_exposure_history_counts_and_offline_strata(self):
        w, b, r, i, a, c = fixture()
        tables = information_records(w, b, r, i, a, committed=c, tokenizer=CharacterTokenizer())
        self.assertEqual(len(tables["prefix"]), 16)
        self.assertTrue(tables["owner_exposure"][0]["owner_v1_exposure"])
        self.assertEqual(len(tables["owner_exposure"][0]["exposed_call_ids"]), 4)
        self.assertEqual(tables["prefix"][0]["history_content_tokens"], 0)
        self.assertTrue(any(p["history_content_tokens"] > 0 for p in tables["prefix"]))
        self.assertTrue(all(p["old_gold_correct"] == 1 for p in tables["prefix"]))
        self.assertTrue(all(s["old_candidate_correct"] == 1 and s["prefix_round_four_joint"] == 1 for s in tables["receipt_strata"]))
        delta = [s for s in tables["receipt_information"] if s["policy"].endswith("_delta")]
        self.assertTrue(all(s["visibility"]["visible"] for s in delta))
        self.assertTrue(all(s["complete_current_raw"] for s in delta))
        self.assertTrue(all(s["boundary"]["excluded_record_id"] == w[0].main_edit.record_id for s in tables["boundary_acquisition"]))

    def test_token_counts_unavailable_without_matching_tokenizer_and_mismatch_rejected(self):
        w, b, r, i, a, c = fixture()
        tables = information_records(w, b, r, i, a, committed=c)
        self.assertTrue(any(p["history_content_tokens"] is None for p in tables["prefix"]))
        saved = next(iter(i.values()))
        saved["requests"]["tokenized"][0]["input_ids"][-1] += 1
        with self.assertRaisesRegex(ValueError, "exact saved input"):
            information_records(w, b, r, i, a, committed=c, tokenizer=CharacterTokenizer())

    def test_cleared_candidate_cannot_be_used_for_reconstruction_but_compact_wrong_one_can(self):
        w, b, r, i, a, c = fixture(wrong_prefix=True)
        tables = information_records(w, b, r, i, a, committed=c)
        cleared = [row for row in tables["receipt_information"] if row["policy"] in ("C", "C_delta")]
        self.assertTrue(all(row["old_candidate_in_view"] is False for row in cleared))
        self.assertTrue(all(row["reconstructibility"]["status"] == "old_candidate_unavailable_in_view" for row in cleared))
        compact = [row for row in tables["receipt_information"] if row["policy"] in ("K", "K_delta")]
        self.assertTrue(all(row["old_candidate_in_view"] for row in compact))
        self.assertTrue(all(row["old_candidate_correct"] == 0 for row in compact))
        references = [row for row in tables["transport_references"] if row["available"]]
        self.assertTrue(all(row["residual_identity"] and row["transported_correct"] == 0 for row in references))

    def test_rendering_drift_is_rejected_even_when_state_is_correct(self):
        w, b, r, i, a, c = fixture()
        saved = next(iter(i.values()))
        before = saved["requests"]["rendered"][0]["content"]
        saved["requests"]["rendered"][0]["content"] = before.replace('"version":1', '"version":2', 1)
        with self.assertRaisesRegex(ValueError, "actual rendered"):
            information_records(w, b, r, i, a, committed=c)

    def test_repeated_delivery_attempts_and_unique_acquisitions_and_final_boundary(self):
        w, b, r, i, a, c = fixture(policies=("C",))
        branch = next(b for b in b if b.phase == "continuation")
        call = next(call for call in branch.calls if call.round_number == 4 and call.peer == 0)
        source = json.loads(i[branch.branch_id, 4]["requests"]["before"])["peers"][0]["sources"][0]
        recipient_sources = json.loads(i[branch.branch_id, 4]["requests"]["before"])["peers"][1]["sources"]
        set_sources(i[branch.branch_id, 4], 1, [s for s in recipient_sources if s["record_id"] != source["record_id"]])
        validation = json.loads(r[call.call_id]["validation_json"])
        raw = json.loads(r[call.call_id]["raw_json"])
        raw["text"] = encode({"candidate": validation["candidate"]["value"], "send": [{"to": 1,
            "source_refs": [{"record_id": source["record_id"], "version": source["version"]}] * 2}]})
        validation.update(generated=raw, messages=[dict(recipient=1, sender=0, slot=validation["candidate"]["slot"], sources=[source, source], text=None)])
        r[call.call_id].update(raw_json=encode(raw), validation_json=encode(validation))
        for index in range(2):
            c[branch.branch_id]["state"]["deliveries"].append(dict(delivery_id=f"{call.call_id}/to1/source{index}",
                message_id=f"{call.call_id}/to1", recipient=1, sender=0, origin="peer", generated=validation["candidate"]["slot"],
                source=source, text=None, first_usable=dict(phase="recovery", round_number=5), acquired=index == 0))
        tables = information_records(w, b, r, i, a, committed=c)
        acquired = next(row for row in tables["boundary_acquisition"] if row["peer"] == 1)
        self.assertEqual((acquired["unique_acquired_count"], acquired["all_validated_delivery_attempts"], acquired["observed_delivery_attempts"]), (1, 2, 2))
        self.assertEqual([a["acquired"] for a in tables["delivery_attempts"]], [True, False])
        self.assertTrue(all(a["first_usable"]["round_number"] == 5 for a in tables["delivery_attempts"]))
        # A final committed horizon cannot silently lose a delivery.
        c[branch.branch_id]["state"]["deliveries"].pop()
        with self.assertRaisesRegex(ValueError, "lacks a validated delivery"):
            information_records(w, b, r, i, a, committed=c)

    def test_final_validation_alone_does_not_prove_delivery_or_acquisition(self):
        w, b, r, i, a, _ = fixture(policies=("C",))
        tables = information_records(w, b, r, i, a)
        self.assertTrue(all(s["unique_acquired_count"] is None and not s["complete_delivery_horizon"] for s in tables["boundary_acquisition"]))

    def test_boundary_checkpoint_before_calls_is_evidence_without_fabricating_outcomes(self):
        w, b, r, i, a, c = fixture(policies=("C",))
        branch = next(branch for branch in b if branch.phase == "continuation")
        start = json.loads(i[branch.branch_id, 1]["requests"]["before"])
        start["last_slot"] = dict(phase="prefix", round_number=4)
        c[branch.branch_id]["state"] = start
        for call in branch.calls:
            del r[call.call_id]
        a = [attempt for attempt in a if attempt["call_id"] in r]
        i = {key: value for key,value in i.items() if key[0] != branch.branch_id}
        tables = information_records(w, b, r, i, a, committed=c)
        self.assertTrue(all(s["boundary"] is not None and s["boundary_origin"] == "committed_pre_call_boundary"
                            for s in tables["boundary_acquisition"]))
        self.assertTrue(all(s["unique_acquired_count"] is None for s in tables["boundary_acquisition"]))

    def test_invalid_last_candidate_has_no_transport_despite_earlier_correct_candidate(self):
        w, b, r, i, a, c = fixture(policies=("B",))
        call = next(call for branch in b if branch.phase == "prefix" for call in branch.calls if call.round_number == 4 and call.peer == 0)
        validation = json.loads(r[call.call_id]["validation_json"])
        validation["candidate"].update(status="invalid", value=None)
        validation["schema_valid"] = False
        r[call.call_id]["validation_json"] = encode(validation)
        tables = information_records(w, b, r, i, a, committed=c)
        reference = next(s for s in tables["transport_references"] if s["peer"] == 0)
        self.assertFalse(reference["available"])
        self.assertIsNone(reference["candidate"])
        self.assertTrue(tables["owner_exposure"][0]["owner_v1_exposure"])
        self.assertTrue(any(s["old_candidate_correct"] == 0 for s in tables["receipt_strata"]))

    def test_committed_scope_and_unknown_outcomes_and_source_drift_are_rejected(self):
        w, b, r, i, a, c = fixture()
        bad = copy.deepcopy(c)
        bid = next(iter(c))
        bad[bid]["state"]["branch_id"] = "other"
        with self.assertRaisesRegex(ValueError, "committed diagnostic"):
            information_records(w, b, r, i, a, committed=bad)
        missing = next(call.call_id for branch in b if branch.branch_id == bid for call in branch.calls)
        del r[missing]
        a = [row for row in a if row["call_id"] != missing]
        with self.assertRaisesRegex(ValueError, "unexecuted"):
            information_records(w, b, r, i, a, committed=c)

    def test_worker_read_only_duplicate_protection_and_optional_estimands(self):
        w, b, r, i, a, _ = fixture(policies=("B", "C", "K"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "worker.sqlite"
            write_worker(path, r, i, a)
            before = path.read_bytes()
            tables = information_run(w, b, [path])
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(tables["coverage"]["unknown"], 0)
            with self.assertRaisesRegex(ValueError, "once"):
                read_records(w, b, [path, path], include_committed=True)
            missing = path.with_name("missing.sqlite")
            self.assertEqual(information_run(w, b, [missing])["coverage"]["unknown"], len(r))
            self.assertFalse(missing.exists())

    def test_cli_unknown_schedule_and_combined_estimands_and_exclusive_export(self):
        with tempfile.TemporaryDirectory() as directory:
            output, missing = Path(directory) / "tables.json.gz", Path(directory) / "missing.sqlite"
            command = [sys.executable, "-S", "-m", "recovery", "analyze", "--stage", "development", "--diagnostics", "--estimands",
                "--manifest", str(ROOT / "tests/fixtures/population_target.json"),
                "--schedule", str(ROOT / "tests/fixtures/schedules_target.json"), "--worker", str(missing), "--output", str(output)]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            tables = json.loads(gzip.decompress(output.read_bytes()))
            self.assertEqual(tables["coverage"]["unknown"], 1178)
            self.assertIn("estimands", tables)
            self.assertTrue(all(p["owner_v1_exposure"] is None for p in tables["information"]["owner_exposure"]))
            self.assertTrue(all(s["visibility"]["status"] == "boundary_unknown" for s in tables["information"]["receipt_information"]))
            self.assertTrue(all(s["reconstructibility"]["information_view"] and s["reconstructibility"]["correctness_assumption"]
                                for s in tables["information"]["receipt_information"]))
            before = output.read_bytes()
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_bytes(), before)
            self.assertFalse(missing.exists())

    def test_pure_diagnostics_do_not_import_runner_or_model_or_protocol(self):
        code = '''
import sys, importlib.abc
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in ('torch','transformers','pydantic','langgraph'):
            raise AssertionError(fullname)
sys.meta_path.insert(0, Block())
from tests.information_fixture import fixture
from recovery.information import information_records
w,b,r,i,a,c = fixture()
information_records(w,b,r,i,a,committed=c)
assert all(n not in sys.modules for n in ('recovery.runner','recovery.protocol','recovery.rounds','recovery.inference'))
'''
        result = subprocess.run([sys.executable, "-S", "-c", code], cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


@unittest.skipUnless(importlib.util.find_spec("langgraph"), "saved checkpoint decoder needs declared CPU dependencies")
class InformationArchiveTests(unittest.TestCase):
    def test_public_checkpoint_decoder_reads_same_snapshot_and_protects_original_bytes(self):
        from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
        import sqlite3
        w, b, r, i, a, committed = fixture(policies=("B",))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "worker.sqlite"
            write_worker(path, r, i, a)
            con = sqlite3.connect(path)
            try:
                con.execute("CREATE TABLE checkpoints(thread_id TEXT, checkpoint_ns TEXT, checkpoint_id TEXT, type TEXT, checkpoint BLOB)")
                for branch in b:
                    values = {"branch_json": i[branch.branch_id, 1]["branch_json"], "settings_json": "{}",
                              "committed": encode(committed[branch.branch_id]["state"]).encode()}
                    kind, payload = JsonPlusSerializer().dumps_typed({"channel_values": values})
                    con.execute("INSERT INTO checkpoints VALUES (?, '', 'checkpoint-1', ?, ?)", (branch.branch_id, kind, payload))
                con.commit()
            finally:
                con.close()
            before = path.read_bytes()
            tables = information_run(w, b, [path])
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(len(tables["information"]["prefix"]), 16)
            # Duplicate restored worker files must not duplicate checkpoints or outcomes.
            backup = path.with_name("backup.sqlite")
            backup.write_bytes(before)
            with self.assertRaisesRegex(ValueError, "duplicate"):
                information_run(w, b, [path, backup])

    def test_original_workers_full_unknown_populations_and_final_acquisitions(self):
        from tests.information_archive import FIXTURE, reconstruct
        actual = reconstruct()
        with gzip.open(FIXTURE, "rt", encoding="utf-8") as saved:
            expected = json.load(saved)
        # unittest's automatic whole-dictionary text diff is quadratic for
        # these multi-megabyte tables. Identify the table/row before comparing.
        self.assertTrue(actual.keys() == expected.keys(), "archive top-level fields differ")
        self.assertTrue(actual["cases"].keys() == expected["cases"].keys(), "archive cases differ")
        for name, case in actual["cases"].items():
            self.assertTrue(case.keys() == expected["cases"][name].keys(), f"{name}: table keys differ")
            for key, value in case.items():
                saved_value = expected["cases"][name][key]
                if isinstance(value, list):
                    self.assertEqual(len(value), len(saved_value), f"{name}/{key}: row count")
                    for index, (row, saved_row) in enumerate(zip(value, saved_value)):
                        self.assertTrue(row == saved_row, f"{name}/{key}/{index}: fields " +
                            str([k for k in row.keys() | saved_row.keys() if row.get(k) != saved_row.get(k)]))
                else:
                    self.assertTrue(value == saved_value, f"{name}/{key} differs")
        self.assertTrue(actual["atlas_examples"] == expected["atlas_examples"], "atlas examples differ")
        full = actual["cases"]["full-main-target-60"]
        self.assertEqual(full["coverage"]["unknown"], 15486)
        self.assertEqual(len(full["prefix"]), 960)
        self.assertTrue(any(s["unique_acquired_count"] is None for s in full["boundary_acquisition"]))
        self.assertTrue(any(s["category"] == "receipt_or_outcome_censored" for s in full["receipt_timing"]))
        complete = next(v for k,v in actual["cases"].items() if k.endswith('/target'))
        self.assertTrue(all(s["complete_delivery_horizon"] for s in complete["boundary_acquisition"]))
        self.assertTrue(all(a["delivered"] for a in complete["delivery_attempts"]))
        self.assertTrue(all(s["owner_v1_exposure"] for s in complete["owner_exposure"]))


if __name__ == "__main__":
    unittest.main()
