"""Original-worker joins, trace fidelity, portable exports and offline imports."""

import copy
import gzip
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

from recovery.report import report_run, trace_records, write_report
from tests.cost_fixture import clock, write_cost_worker
from tests.information_fixture import fixture
from tests.outcome_fixture import ROOT


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        self.links.extend(attrs[k] for k in ("href", "src") if k in attrs)


def audit_links(directory):
    parsed = {}
    for path in directory.glob("*.html"):
        parser = Links()
        parser.feed(path.read_text(encoding="utf-8"))
        if len(parser.ids) != len(set(parser.ids)):
            raise AssertionError("duplicate HTML anchors: "+path.name)
        parsed[path.name] = parser
    count = 0
    for name, parser in parsed.items():
        for link in parser.links:
            parts = urlsplit(link)
            if parts.scheme:
                continue
            target = parts.path or name
            if not (directory/target).is_file():
                raise AssertionError("missing report link: "+link)
            if parts.fragment and unquote(parts.fragment) not in parsed[target].ids:
                raise AssertionError("missing report anchor: "+link)
            count += 1
    return count


def measured_fixture():
    worlds, branches, records, inputs, attempts, committed = fixture()
    for n, row in enumerate(attempts):
        row.update(elapsed_seconds=2, observed_seconds=2, started_at=clock(2*n), finished_at=clock(2*n+2),
                   recovered_at=None, device="synthetic:0", peak_memory_bytes=1000)
    return worlds, branches, records, inputs, attempts


class ReportRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.root = Path(cls.directory.name)
        cls.worlds, cls.branches, cls.records, cls.inputs, attempts = measured_fixture()
        cls.worker = cls.root/"worker.sqlite"
        write_cost_worker(cls.worker, cls.records, cls.inputs, attempts)
        cls.before = cls.worker.read_bytes()
        cls.result = report_run(cls.worlds, cls.branches, [cls.worker], now=clock(400))

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_all_m4_outputs_share_original_snapshot_and_worker_is_unchanged(self):
        tables = self.result["tables"]
        self.assertTrue(all(k in tables for k in ("outcomes", "coordinates", "estimands", "information", "costs", "uncertainty")))
        self.assertEqual(self.worker.read_bytes(), self.before)
        self.assertEqual(tables["coverage"]["unknown"], 0)
        self.assertTrue(self.result["report"]["settings"]["generation_settings"])
        self.assertEqual(len(self.result["report"]["exhibits"]), 7)
        self.assertIn("not model capability", self.result["report"]["kind"])

    def test_cards_link_actual_last_prefix_and_component_calls_and_preserve_raw_text(self):
        report = self.result["report"]
        self.assertEqual(report["selection"]["fallback"]["reason"], "all_zero_smallest_complete")
        for card in report["cases"]:
            self.assertTrue(card["trajectories"])
            self.assertTrue(card["availability"])
            self.assertTrue(card["preservation"])
            self.assertEqual(card["edit"]["before"]["version"], 1)
            self.assertEqual(card["edit"]["after"]["version"], 2)
            self.assertTrue(any("/prefix/" in r["call_id"] and "/r4/" in r["call_id"] for r in card["excerpts"]))
            for excerpt in card["excerpts"]:
                original = self.records[excerpt["generation_id"]]
                self.assertEqual(excerpt["raw_reply"], json.loads(original["raw_json"]))

    def test_repeat_one_contrasts_cannot_replace_original_case_card_joins(self):
        from recovery.report import case_cards
        tables = copy.deepcopy(self.result["tables"])
        rows = tables["estimands"]["world_contrasts"]
        repeated = copy.deepcopy(next(row for row in rows if row["estimand"] == "C-B"
            and row["event"] == "revision" and row["endpoint"] == "auc" and row["replicate"] == 0))
        repeated["replicate"] = 1
        for component in repeated["components"]:
            component["branch_id"] += "/repeat-one"
        rows.append(repeated)
        actual = case_cards(self.worlds, tables, self.result["traces"], self.result["report"]["selection"])
        self.assertEqual(actual, self.result["report"]["cases"])

    def test_literal_trace_preserves_control_characters_unicode_and_raw_whitespace(self):
        records = copy.deepcopy(self.records)
        row = next(iter(records.values()))
        raw = json.loads(row["raw_json"])
        raw["text"] = "\r\n\t "+raw["text"]+"\n \u03b4 <script>"
        row["raw_json"] = json.dumps(raw)
        traces = trace_records(self.result["tables"], records, self.inputs)
        excerpt = next(r for r in traces["calls"] if r["call_id"] == row["call_id"])
        self.assertEqual(excerpt["raw_reply"]["text"], raw["text"])
        from recovery.report import _calls_html
        html = _calls_html(traces)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>", html)

    def test_full_information_control_uses_its_single_rendered_request(self):
        tables = copy.deepcopy(self.result["tables"])
        row = tables["outcomes"][0]
        row["peer"] = None
        tables["outcomes"] = [row]
        inputs = {(row["branch_id"], row["round"]): {"requests": {"rendered": {"content": "literal control request\n"}}}}
        actual = trace_records(tables, self.records, inputs)
        self.assertEqual(actual["calls"][0]["request_text"], "literal control request\n")
        self.assertEqual(actual["calls"][0]["peer"], None)

    def test_non_scalar_raw_unicode_is_reversibly_displayed_without_repair(self):
        from recovery.report import _literal_html
        # Keep the two surrogates unpaired. JSON legitimately decodes an adjacent
        # high/low pair into its scalar, as required by the protocol contract.
        raw = "literal\r\n\ud800 | \udfff <script> \\ud800"
        html = _literal_html(raw)
        self.assertIn("Non-scalar Unicode", html)
        self.assertNotIn("\ud800", html)
        encoded = unescape(html.split("<pre>", 1)[1].split("</pre>", 1)[0])
        self.assertEqual(json.loads(encoded), raw)

    def test_branchless_prose_delivery_links_original_message_and_sender_call_ids(self):
        tables = copy.deepcopy(self.result["tables"])
        sender = tables["outcomes"][0]
        message_id = sender["call_id"]+"/to1"
        delivery = dict(message_id=message_id, delivery_id=message_id+"/text", text="literal\r\nprose",
            recipient=1, first_usable=dict(phase="prefix", round_number=2))
        tables["costs"]["validated_deliveries"] = [delivery]
        actual = trace_records(tables, self.records, self.inputs)["deliveries"][0]
        self.assertEqual(actual["call_id"], sender["call_id"])
        self.assertEqual(actual["branch_id"], sender["branch_id"])
        self.assertEqual(actual["message_id"], message_id)
        self.assertEqual(actual["text"], delivery["text"])
        tables["costs"]["validated_deliveries"][0]["message_id"] = "unscheduled/r1/p0/to1"
        with self.assertRaisesRegex(ValueError, "original scheduled sender"):
            trace_records(tables, self.records, self.inputs)

    def test_two_reconstructions_exports_and_plotting_inputs_match_exactly(self):
        repeated = report_run(self.worlds, self.branches, [self.worker], now=clock(400))
        for key in self.result:
            self.assertTrue(self.result[key] == repeated[key], key)
        left, right = self.root/"first", self.root/"second"
        write_report(left, self.result)
        write_report(right, repeated)
        self.assertEqual(sorted(p.name for p in left.iterdir()), sorted(p.name for p in right.iterdir()))
        for path in left.iterdir():
            self.assertEqual(path.read_bytes(), (right/path.name).read_bytes(), path.name)
        self.assertGreater(audit_links(left), 20)
        with gzip.open(left/"tables.json.gz", "rt", encoding="utf-8") as source:
            self.assertTrue(json.load(source) == self.result["tables"])

    def test_existing_export_is_protected_and_accounting_clock_is_required(self):
        directory = self.root/"protected"
        directory.mkdir()
        (directory/"sentinel").write_text("original")
        with self.assertRaises(FileExistsError):
            write_report(directory, self.result)
        self.assertEqual((directory/"sentinel").read_text(), "original")
        with self.assertRaisesRegex(ValueError, "explicit zoned"):
            report_run(self.worlds, self.branches, [self.worker], now=None)

    def test_absolute_quality_cost_axes_do_not_mix_in_paired_policy_differences(self):
        from recovery.report import _quality_plot_rows
        source = self.result["tables"]["uncertainty"]["policy_display_summaries"]
        self.assertTrue(any(r["display"].startswith("boundary_rule-always_") for r in source))
        plotted = _quality_plot_rows(source)
        self.assertTrue(plotted)
        self.assertFalse(any(r["display"].startswith("boundary_rule-always_") for r in plotted))
        self.assertTrue(any(r["display"] == "boundary_rule" for r in plotted))
        for row in plotted:
            for field in ("cost_estimate", "complete_case_cost_estimate"):
                self.assertTrue(row[field] is None or all(v >= 0 for v in row[field]))

    def test_missing_workers_stay_absent_and_cases_are_unavailable(self):
        missing = self.root/"missing.sqlite"
        result = report_run(self.worlds, self.branches, [missing], now=clock(400))
        self.assertFalse(missing.exists())
        self.assertEqual(result["tables"]["coverage"]["unknown"], sum(len(b.calls) for b in self.branches))
        self.assertEqual(result["report"]["selection"]["status"], "unavailable")
        self.assertFalse(result["report"]["cases"])
        self.assertTrue(all(r["raw_reply"] is None for r in result["traces"]["calls"]))

    def test_offline_export_blocks_inference_execution_and_plotting_imports(self):
        script = '''
import importlib.abc,sys,tempfile
from pathlib import Path
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, *args):
        if fullname.split('.')[0] in {'torch','transformers','accelerate','bitsandbytes','matplotlib'} or fullname in {'recovery.runner','recovery.workers','recovery.inference','recovery.storage'}:
            raise AssertionError('offline report crossed into execution/plotting: '+fullname)
sys.meta_path.insert(0,Block())
from recovery.report import report_run,write_report
from tests.test_report_run import measured_fixture
from tests.cost_fixture import clock,write_cost_worker
w,b,r,i,a=measured_fixture()
with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'worker.sqlite'
    write_cost_worker(p,r,i,a)
    before=p.read_bytes()
    result=report_run(w,b,[p],now=clock(400))
    write_report(Path(d)/'report',result)
    assert p.read_bytes()==before
'''
        run = subprocess.run([sys.executable, "-S", "-c", script], cwd=ROOT, capture_output=True, text=True, timeout=60)
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_cli_report_all_unknown_export_and_invalid_options(self):
        with tempfile.TemporaryDirectory() as directory:
            output, missing = Path(directory)/"report", Path(directory)/"missing.sqlite"
            args = [sys.executable, "-S", "-m", "recovery", "analyze", "--stage", "development",
                "--manifest", str(ROOT/"tests/fixtures/population_target.json"), "--schedule", str(ROOT/"tests/fixtures/schedules_target.json"),
                "--worker", str(missing), "--output", str(output), "--report"]
            invalid = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=60)
            self.assertEqual(invalid.returncode, 2)
            self.assertIn("explicit zoned", invalid.stderr)
            self.assertFalse(output.exists())
            args += ["--as-of", clock(400), "--resampling-seed", "37"]
            run = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=90)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn("0/1178 recorded", run.stdout)
            report = json.loads((output/"report.json").read_bytes())
            self.assertEqual(report["settings"]["uncertainty"]["seed"], 37)
            self.assertFalse(report["cases"])
            self.assertFalse(missing.exists())
            self.assertGreater(audit_links(output), 0)
            repeat = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=90)
            self.assertEqual(repeat.returncode, 2)
            self.assertIn("already exists", repeat.stderr)


if __name__ == "__main__":
    unittest.main()
