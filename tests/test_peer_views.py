from dataclasses import FrozenInstanceError, asdict, fields, replace
from itertools import combinations
import json
from pathlib import Path
from random import Random
import subprocess
import sys
import tempfile
import unittest

from recovery.prompts import (COMMON_INSTRUCTION, MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS,
                              TokenizedRequest, render_request, tokenize_request)
from recovery.state import (PUBLIC_FEEDBACK, CandidateState, ContinueNotice, Feedback,
                            HistoricalReceipt, OwnReply, PeerView, PendingSource,
                            ReceivedProse, RevisionNotice, Slot, SourceDelivery,
                            held_source, initial_view)
from recovery.tasks import (PEERS, PublicSource, Size, SourceRecord, Task, World,
                            candidate_contract, generate_world)
from tests.peer_view_cases import SPECIAL_TEXT, renderer_cases

ROOT = Path(__file__).resolve().parent.parent


def data(view):
    return json.loads(render_request(view).content.split("\nPeer data (JSON):\n", 1)[1])


class RecordingTokenizer:
    """An injected spy for flags and exact accounting, not real tokenizer evidence."""

    def __init__(self, token_count=17):
        self.token_count = token_count
        self.template_calls = []
        self.encode_calls = []

    def apply_chat_template(self, messages, **kwargs):
        self.template_calls.append((messages, kwargs))
        return "<user>\n" + messages[0]["content"] + "\n<assistant>\n<think>\n\n</think>\n\n"

    def __call__(self, text, **kwargs):
        self.encode_calls.append((text, kwargs))
        return {"input_ids": list(range(self.token_count)), "attention_mask": [1] * self.token_count}


class PeerViewTests(unittest.TestCase):
    def world(self, task=Task.PREFIX, size=Size.TARGET):
        return generate_world(task, size, generation_rng=Random(7), ownership_rng=Random(11))

    def test_all_initial_shards_controls_public_metadata_and_shapes(self):
        for size in Size:
            for task in Task:
                world = self.world(task, size)
                for peer in (*PEERS, None):
                    with self.subTest(size=size, task=task, peer=peer):
                        view = initial_view(world, peer)
                        shown = data(view)
                        self.assertEqual(view.sources, tuple(r for r in world.records
                                                            if peer is None or r.owner == peer))
                        self.assertEqual(shown["public"]["output_coordinates"],
                                         list(candidate_contract(task, size, peer).coordinates))
                        self.assertEqual(len(shown["current_sources"]), len(view.sources))
                        self.assertEqual(shown["history"], [])
                        self.assertEqual(shown["latest_candidate"], {"status": "unexecuted", "candidate": None})
                        self.assertEqual(shown["feedback"], [])
                        self.assertIsNone(shown["persistent_notice"])
                        self.assertIsNone(shown["historical_receipt"])
                        self.assertTrue(render_request(view).content.startswith(COMMON_INSTRUCTION))
                        if task is Task.BFS:
                            self.assertEqual(shown["public"]["nodes"], list(range(size.node_count)))
                            self.assertEqual(shown["public"]["source_node"], 0)
                            self.assertTrue(all("endpoints" not in s and "position" not in s
                                                for s in shown["public"]["manifest"]))
                        else:
                            self.assertEqual(shown["public"]["positions"], list(range(size.numeric_length)))
                        if peer is None:
                            self.assertEqual(shown["public"]["communication"], "send must be an empty list")
                        else:
                            self.assertEqual(shown["public"]["communication"]["recipients"],
                                             [p for p in PEERS if p != peer])

    def test_hidden_values_and_private_bfs_endpoints_cannot_change_other_renderings(self):
        for size in Size:
            for task in Task:
                world = self.world(task, size)
                for peer in PEERS:
                    for remote in (r for r in world.records if r.owner != peer):
                        if task is Task.BFS:
                            edges = {r.value for r in world.records}
                            value = next(edge for edge in combinations(range(size.node_count), 2)
                                         if edge not in edges)
                        else:
                            value = (1 if remote.value != 1 else 9) if task is Task.PREFIX else (
                                0 if remote.value != 0 else 1)
                        changed = replace(world, records=tuple(replace(r, value=value) if r == remote else r
                                                               for r in world.records))
                        self.assertEqual(initial_view(world, peer), initial_view(changed, peer))
                        self.assertEqual(render_request(initial_view(world, peer)),
                                         render_request(initial_view(changed, peer)))

    def test_offline_gold_edits_conditions_and_queue_text_are_not_inputs(self):
        world = self.world()
        host = {"world": world, "gold": "HIDDEN_GOLD", "future_edit": "HIDDEN_EDIT",
                "policy": "HIDDEN_POLICY", "branch_id": "HIDDEN_BRANCH", "reset_mask": "HIDDEN_MASK",
                "subset": "HIDDEN_SUBSET", "affected_outputs": "HIDDEN_EFFECT",
                "held_prose": "HIDDEN_QUEUE_TEXT", "queue_status": "HIDDEN_QUEUE_STATUS"}
        baseline = render_request(initial_view(host["world"], 0))
        for name in host.keys() - {"world"}:
            changed = dict(host, **{name: "DIFFERENT_" + host[name]})
            self.assertEqual(render_request(initial_view(changed["world"], 0)), baseline)
            self.assertNotIn(host[name], baseline.content)
            with self.assertRaises(TypeError):
                PeerView(**(asdict(initial_view(world, 0)) | {name: host[name]}))
        for forbidden in (world, host, world.records, host["gold"]):
            with self.assertRaises(ValueError):
                render_request(forbidden)
        with self.assertRaises(ValueError):
            initial_view(host, 0)
        self.assertFalse(set(host.keys() - {"world"}) & {f.name for f in fields(PeerView)})

    def test_public_identity_order_is_payload_independent_and_canonical(self):
        for size in Size:
            for task in Task:
                world = self.world(task, size)
                view = initial_view(world, 0)
                permuted = replace(world, records=tuple(reversed(world.records)))
                self.assertEqual(render_request(view), render_request(initial_view(permuted, 0)))
                shuffled_view = replace(view, manifest=tuple(reversed(view.manifest)),
                                        sources=tuple(reversed(view.sources)),
                                        source_deliveries=tuple(reversed(view.source_deliveries)))
                self.assertEqual(view, shuffled_view)
                shown = data(view)
                for key in ("current_sources", "source_deliveries"):
                    ids = [r["record_id"] for r in shown[key]]
                    self.assertEqual(ids, sorted(ids))
                # The allowed public identity/order contains no values/endpoints.
                self.assertTrue(all(set(r) <= {"record_id", "owner", "position"}
                                    for r in shown["public"]["manifest"]))

    def test_pending_sources_tombstones_and_stale_lookup_are_distinct(self):
        cases = renderer_cases()
        pending, tombstone = cases["pending_edge"], cases["known_tombstone"]
        source_id = pending.notice.source.record_id
        pending_data, known_data = data(pending), data(tombstone)
        self.assertEqual(pending_data["persistent_notice"], known_data["persistent_notice"])
        unknown = next(r for r in pending_data["current_sources"] if r["record_id"] == source_id)
        deleted = next(r for r in known_data["current_sources"] if r["record_id"] == source_id)
        self.assertEqual(unknown["status"], "update_pending")
        self.assertNotIn("endpoints", unknown)
        self.assertNotIn("endpoints", pending_data["persistent_notice"])
        self.assertEqual(deleted["status"], "deleted")
        self.assertEqual(len(deleted["endpoints"]), 2)
        self.assertIsNone(held_source(pending, source_id, 1))
        self.assertIsNone(held_source(pending, source_id, 2))
        self.assertIsNone(held_source(tombstone, source_id, 1))
        self.assertTrue(held_source(tombstone, source_id, 2).deleted)
        for source_id, version in (("unseen", 1), (source_id, 3), (source_id, True)):
            self.assertIsNone(held_source(tombstone, source_id, version))

    def test_revision_rejects_old_usable_payload_and_checks_cpu_v1_v2_v3(self):
        base = initial_view(self.world(), 0)
        old = base.sources[0]
        public = next(s for s in base.manifest if s.record_id == old.record_id)
        before = render_request(base)
        for version in (2, 3):
            known = replace(old, version=version)
            source_tuple = tuple(known if r.record_id == old.record_id else r for r in base.sources)
            view = replace(base, slot=Slot("recovery", 1), sources=source_tuple,
                           notice=RevisionNotice(public, version - 1, version),
                           source_deliveries=tuple(d for d in base.source_deliveries if d.record_id != old.record_id))
            self.assertIsNone(held_source(view, old.record_id, version - 1))
            self.assertEqual(held_source(view, old.record_id, version), known)
            with self.assertRaises(ValueError):
                replace(view, sources=base.sources)
        self.assertEqual(render_request(base), before)

    def test_receipt_disclosure_changes_only_historical_field_and_never_current_lookup(self):
        cases = renderer_cases()
        ordinary, disclosed = cases["ordinary_receipt"], cases["disclosed_receipt"]
        first, second = data(ordinary), data(disclosed)
        self.assertEqual(first["historical_receipt"]["before_value"], "not included in this receipt")
        self.assertEqual(second["historical_receipt"]["before_value"], disclosed.receipt.before_value)
        first["historical_receipt"]["before_value"] = disclosed.receipt.before_value
        self.assertEqual(first, second)
        source_id = ordinary.receipt.source.record_id
        self.assertIsNone(held_source(disclosed, source_id, 1))
        self.assertEqual(held_source(ordinary, source_id, 2), held_source(disclosed, source_id, 2))
        self.assertEqual(disclosed.history[0].text, SPECIAL_TEXT)
        cleared = replace(disclosed, history=(), feedback=(), candidate=CandidateState())
        self.assertEqual(data(cleared)["persistent_notice"], second["persistent_notice"])
        self.assertEqual(data(cleared)["historical_receipt"], second["historical_receipt"])

    def test_receipt_layout_at_both_sizes_on_prefix_and_sort_and_invalid_receipts(self):
        for size in Size:
            for task in (Task.PREFIX, Task.SORT):
                base = initial_view(self.world(task, size), 0)
                old = base.sources[0]
                identity = next(r for r in base.manifest if r.record_id == old.record_id)
                replacement = replace(old, version=2)
                sources = (replacement,) + base.sources[1:]
                view = replace(base, slot=Slot("recovery", 1), sources=sources,
                               notice=RevisionNotice(identity, 1, 2),
                               source_deliveries=tuple(d for d in base.source_deliveries
                                                       if d.record_id != old.record_id))
                ordinary = replace(view, receipt=HistoricalReceipt(identity, 1, 2))
                disclosed = replace(view, receipt=HistoricalReceipt(identity, 1, 2, old.value))
                first, second = data(ordinary), data(disclosed)
                first["historical_receipt"]["before_value"] = old.value
                self.assertEqual(first, second)
                for receipt in (HistoricalReceipt(identity, 1, 2, True),
                                HistoricalReceipt(identity, 1, 2, -100),
                                HistoricalReceipt(identity, 2, 3, old.value),
                                HistoricalReceipt(base.manifest[-1], 1, 2, old.value)):
                    with self.assertRaises(ValueError):
                        replace(view, receipt=receipt)
                pending = replace(view, sources=(PendingSource(old.record_id, old.owner, old.position, 2),)
                                  + base.sources[1:])
                with self.assertRaises(ValueError):
                    replace(pending, receipt=disclosed.receipt)
        for name in ("pending_edge", "known_tombstone"):
            graph = renderer_cases()[name]
            with self.assertRaises(ValueError):
                replace(graph, receipt=HistoricalReceipt(graph.notice.source, 1, 2, 1))

    def test_history_preserves_literal_text_as_data_and_has_no_raw_table_archive(self):
        view = renderer_cases()["disclosed_receipt"]
        request = render_request(view)
        shown = data(view)
        self.assertEqual(request.messages(), [{"role": "user", "content": request.content}])
        self.assertEqual([entry["text"] for entry in shown["history"]], [SPECIAL_TEXT, SPECIAL_TEXT])
        for entry in shown["history"]:
            self.assertTrue(set(entry) <= {"kind", "slot", "sender", "text"})
            self.assertEqual(entry["slot"], {"phase": "prefix", "round": 4})
        self.assertNotIn("resolved_sources", request.content)
        # The renderer adds each current payload only to current_sources. Model
        # text can still mention old values, source refs, aggregates or tables.
        raw = '{"candidate":[1,2],"send":[{"to":1,"source_refs":[{"record_id":"x001","version":1}]}]}'
        changed = replace(view, history=(OwnReply(Slot("prefix", 4), raw),))
        self.assertEqual(data(changed)["history"][0]["text"], raw)
        self.assertEqual(data(changed)["current_sources"], shown["current_sources"])
        with self.assertRaises(ValueError):
            replace(view, history=(view.sources[0],))

    def test_latest_candidate_is_not_duplicated_or_reused_after_invalid_failed_slots(self):
        view = renderer_cases()["retained_valid_reply"]
        shown = data(view)
        self.assertEqual(shown["latest_candidate"], {"status": "valid",
                         "slot": {"phase": "prefix", "round": 4}, "in_own_reply": True})
        self.assertEqual(json.loads(shown["history"][0]["text"])["candidate"], [987654321] * 8)
        for status in ("invalid", "failed"):
            failed = replace(view, slot=Slot("recovery", 2),
                             candidate=CandidateState(status, Slot("recovery", 1)))
            candidate = data(failed)["latest_candidate"]
            self.assertEqual(candidate["status"], status)
            self.assertIsNone(candidate["candidate"])
            self.assertEqual(failed.history, view.history)
        plausible = replace(view, candidate=CandidateState("invalid", Slot("prefix", 4)))
        self.assertIsNone(data(plausible)["latest_candidate"]["candidate"])

    def test_compact_actual_wrong_result_and_historical_absence_are_explicit(self):
        cases = renderer_cases()
        compact = cases["compact_wrong_result"]
        shown = data(compact)
        self.assertEqual(shown["history"], [])
        self.assertEqual(shown["feedback"], [])
        self.assertEqual(shown["latest_candidate"]["candidate"], [-1234567] * 8)
        self.assertTrue(shown["latest_candidate"]["historical"])
        self.assertTrue(data(cases["compact_absence"])["latest_candidate"]["historical"])
        self.assertIsNone(data(cases["compact_absence"])["latest_candidate"]["candidate"])

    def test_bfs_candidate_copy_is_canonical_and_source_state_is_deeply_immutable(self):
        base = initial_view(self.world(Task.BFS), 0)
        candidate = {str(j): -999 for j in reversed(range(base.size.node_count))}
        state = CandidateState.valid(base.task, base.size, base.peer, Slot("prefix", 4), candidate,
                                     historical=True)
        view = replace(base, slot=Slot("recovery", 1), candidate=state)
        candidate["0"] = 999
        self.assertEqual(data(view)["latest_candidate"]["candidate"]["0"], -999)
        self.assertEqual(list(data(view)["latest_candidate"]["candidate"]),
                         [str(j) for j in range(base.size.node_count)])
        with self.assertRaises(FrozenInstanceError):
            view.sources = ()
        with self.assertRaises(FrozenInstanceError):
            view.sources[0].value = (0, 1)
        with self.assertRaises(TypeError):
            view.candidate.value[0] = ("0", 9)
        messages = render_request(view).messages()
        messages[0]["content"] = "changed external list"
        self.assertNotEqual(render_request(view).content, messages[0]["content"])

    def test_released_prose_preserves_append_order_and_source_metadata_is_queue_independent(self):
        base = initial_view(self.world(Task.SORT), 0)
        entries = (OwnReply(Slot("recovery", 2), "own round two"),
                   ReceivedProse(Slot("recovery", 1), 2, "released round one sender two"),
                   ReceivedProse(Slot("recovery", 1), 3, "released round one sender three"),
                   ReceivedProse(Slot("recovery", 2), 1, "ordinary round two"))
        view = replace(base, slot=Slot("recovery", 3), history=entries)
        shown = data(view)
        self.assertEqual([entry["text"] for entry in shown["history"]], [entry.text for entry in entries])
        ordinary = replace(view, history=entries[:1])
        self.assertEqual(data(ordinary)["source_deliveries"], shown["source_deliveries"])
        self.assertEqual(data(ordinary)["current_sources"], shown["current_sources"])
        self.assertNotIn("released round one", render_request(ordinary).content)
        remote = next(r for r in self.world(Task.SORT).records if r.owner == 1)
        delivery = SourceDelivery(remote.record_id, 1, "peer", 1, Slot("recovery", 1), Slot("recovery", 2))
        sourced = replace(view, sources=view.sources + (remote,),
                          source_deliveries=view.source_deliveries + (delivery,))
        metadata = next(r for r in data(sourced)["source_deliveries"] if r["record_id"] == remote.record_id)
        self.assertEqual(set(metadata), {"record_id", "version", "origin", "sender", "generated", "first_usable"})
        self.assertEqual(metadata["origin"], "peer")
        self.assertNotIn("text", metadata)
        self.assertNotIn("endpoints", metadata)
        with self.assertRaises(ValueError):
            replace(view, history=entries + (entries[1],))

    def test_feedback_layout_has_only_fixed_public_descriptions(self):
        base = initial_view(self.world(), 0)
        for code, description in PUBLIC_FEEDBACK.items():
            feedback = Feedback(Slot("prefix", 1), code)
            view = replace(base, slot=Slot("prefix", 2), feedback=(feedback,))
            self.assertEqual(data(view)["feedback"], [{"slot": {"phase": "prefix", "round": 1},
                                                       "text": description}])
        for hidden in (SPECIAL_TEXT, "gold", "HIDDEN_PAYLOAD", "wrong_answer"):
            with self.assertRaises(ValueError):
                Feedback(Slot("prefix", 1), hidden)
        with self.assertRaises(TypeError):
            Feedback(Slot("prefix", 1), "json", hidden_value="HIDDEN_PAYLOAD")
        with self.assertRaises(TypeError):
            PUBLIC_FEEDBACK["json"] = "HIDDEN_PAYLOAD"

    def test_malformed_or_host_enriched_peer_records_are_rejected(self):
        base = initial_view(self.world(), 0)
        first = base.sources[0]
        invalid_replacements = (
            {"peer": True}, {"sources": list(base.sources)}, {"manifest": base.manifest[:-1]},
            {"manifest": (PublicSource("HIDDEN_VALUE_ID", 0, 0),) + base.manifest[1:]},
            {"sources": base.sources + (first,)},
            {"sources": (replace(first, owner=1),) + base.sources[1:]},
            {"sources": (replace(first, version=True),) + base.sources[1:]},
            {"sources": (replace(first, value=True),) + base.sources[1:]},
            {"history": (OwnReply(Slot("prefix", 1), "future reply"),)},
            {"history": (SourceRecord(first.record_id, first.owner, first.position, first.value),)},
            {"source_deliveries": (replace(base.source_deliveries[0], origin="HIDDEN_QUEUE"),)},
            {"source_deliveries": (replace(base.source_deliveries[0], sender=1),)},
            {"source_deliveries": (replace(base.source_deliveries[0], version=2),)},
            {"source_deliveries": (replace(base.source_deliveries[0], first_usable=Slot("prefix", 2)),)},
        )
        for changes in invalid_replacements:
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    replace(base, **changes)
        for candidate in (True, [True] * 8, [1.0] * 8, ["1"] * 8, [1] * 7):
            with self.assertRaises(ValueError):
                CandidateState.valid(base.task, base.size, 0, Slot("prefix", 4), candidate)
        for status in ("invalid", "failed", "unexecuted"):
            with self.assertRaises(ValueError):
                CandidateState(status, Slot("prefix", 4), (1,) * 8)
        with self.assertRaises(ValueError):
            CandidateState("invalid", Slot("prefix", 3), historical=True)

    def test_deterministic_requests_in_fresh_hash_seeded_processes_without_optional_imports(self):
        script = '''
import importlib.abc
import json
import random
import sys
blocked = {"torch", "transformers", "accelerate", "bitsandbytes", "langgraph",
           "langchain", "numpy", "pandas", "scipy", "pydantic"}
class BlockImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in blocked:
            raise AssertionError("unexpected optional import: " + fullname)
sys.meta_path.insert(0, BlockImports())
before = random.getstate()
from recovery.prompts import render_request
from tests.peer_view_cases import renderer_cases
result = {name: render_request(view).content for name, view in renderer_cases().items()}
assert random.getstate() == before
assert not any(name.split(".")[0] in blocked for name in sys.modules)
print(json.dumps(result, sort_keys=True, ensure_ascii=True))
'''
        import os
        outputs = []
        for seed in ("1", "8347"):
            result = subprocess.run([sys.executable, "-S", "-c", script], cwd=ROOT,
                                    env=dict(os.environ, PYTHONHASHSEED=seed), capture_output=True,
                                    text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            outputs.append(result.stdout)
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(json.loads(outputs[0]), {name: render_request(view).content
                                                for name, view in renderer_cases().items()})


class RequestTokenBoundaryTests(unittest.TestCase):
    def test_exact_native_template_flags_and_serializable_token_inputs(self):
        tokenizer = RecordingTokenizer()
        request = render_request(renderer_cases()["ordinary_receipt"])
        tokenized = tokenize_request(request, tokenizer)
        self.assertEqual(tokenizer.template_calls, [(request.messages(),
                         {"tokenize": False, "add_generation_prompt": True, "enable_thinking": False})])
        self.assertEqual(tokenizer.encode_calls, [(tokenized.text,
                         {"add_special_tokens": False, "truncation": False,
                          "padding": False, "return_attention_mask": True})])
        self.assertIn(request.content, tokenized.text)
        self.assertEqual(tokenized.input_tokens, 17)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "request.json"
            payload = json.dumps({"request": asdict(request), "tokenized": asdict(tokenized)},
                                 ensure_ascii=True, separators=(",", ":")).encode("utf-8")
            path.write_bytes(payload)
            saved = json.loads(path.read_bytes())
            restored = TokenizedRequest(saved["tokenized"]["text"], tuple(saved["tokenized"]["input_ids"]),
                                       tuple(saved["tokenized"]["attention_mask"]))
            self.assertEqual(restored, tokenized)
            self.assertEqual(saved["request"]["content"], request.content)
            self.assertEqual(path.read_bytes(), payload)

    def test_full_384_token_reserve_and_no_truncation_at_or_above_context_boundary(self):
        request = render_request(renderer_cases()["ordinary_receipt"])
        limit = MAX_CONTEXT_TOKENS - MAX_OUTPUT_TOKENS
        exact = tokenize_request(request, RecordingTokenizer(limit))
        self.assertEqual(exact.input_tokens + MAX_OUTPUT_TOKENS, MAX_CONTEXT_TOKENS)
        above = RecordingTokenizer(limit + 1)
        with self.assertRaisesRegex(ValueError, "no truncation"):
            tokenize_request(request, above)
        self.assertEqual(above.template_calls[0][0], request.messages())
        self.assertIn(request.content, above.encode_calls[0][0])
        self.assertFalse(above.encode_calls[0][1]["truncation"])

    def test_retained_request_fixture_and_token_archive_match_exact_renderings(self):
        saved = json.loads((ROOT / "tests/fixtures/peer_requests.json").read_bytes())
        self.assertEqual(set(saved["cases"]), set(renderer_cases()))
        for name, view in renderer_cases().items():
            artifact = saved["cases"][name]
            self.assertEqual(artifact["request"], asdict(render_request(view)))
            tokens = artifact["tokenized"]
            self.assertIn(render_request(view).content, tokens["text"])
            self.assertEqual(len(tokens["input_ids"]), len(tokens["attention_mask"]))
            self.assertLessEqual(len(tokens["input_ids"]) + MAX_OUTPUT_TOKENS, MAX_CONTEXT_TOKENS)
            self.assertTrue(all(type(i) is int and i >= 0 for i in tokens["input_ids"]))
            self.assertEqual(tokens["attention_mask"], [1] * len(tokens["input_ids"]))


if __name__ == "__main__":
    unittest.main()
