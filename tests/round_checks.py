"""Deterministic barrier/delivery/prefix checks; no model or native-capacity claim.

Included by full CPU validation, explicitly excluded by --core-only because
these rounds use the real Pydantic reply validator. Native execution is tested
separately by tokenizer_rounds with the pinned local Qwen metadata.
"""

from dataclasses import FrozenInstanceError, asdict, replace
import json
from random import Random
import unittest
from unittest.mock import patch

from recovery.prompts import render_request
from recovery.protocol import GeneratedReply
import recovery.rounds as rounds
from recovery.rounds import (Delivery, commit_round, deserialize_state, drain_deliveries,
                             fork_prefix, initial_branch, prefix_snapshot, prepare_round,
                             run_prefix, run_round, snapshot_bytes, stage_effects, validate_round)
from recovery.state import (DeliveryBoundary, OwnReply, PendingSource, ReceivedProse,
                            RevisionNotice, Slot, SourceDelivery)
from recovery.tasks import PEERS, Size, SourceRecord, Task, generate_world
from recovery.truth import exact_candidate, solve_world
from tests.protocol_checks import WordTokenizer, placeholder, reference


class RoundTokenizer(WordTokenizer):
    """Exercise the actual request/tokenizer interface with a CPU test counter."""

    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt, enable_thinking):
        assert tokenize is False and add_generation_prompt is True and enable_thinking is False
        return "USER\n" + messages[0]["content"] + "\nASSISTANT\n"

    def __call__(self, text, *, add_special_tokens, truncation, padding, return_attention_mask):
        assert add_special_tokens is False and truncation is False and padding is False
        assert return_attention_mask is True
        ids = self.encode(text, add_special_tokens=False)
        return {"input_ids": ids, "attention_mask": [1] * len(ids)}


TOKENIZER = RoundTokenizer()
PREFIX_ID = "scripted/prefix/original/none/rep0"


def world(task=Task.PREFIX, size=Size.TARGET):
    return generate_world(task, size, generation_rng=Random(31), ownership_rng=Random(37))


def raw_reply(tokenizer, text):
    return GeneratedReply(text, tuple(tokenizer.encode(text, add_special_tokens=False)), "scripted")


def reply(tokenizer, view, send=(), candidate=None):
    text = json.dumps({"candidate": placeholder(view) if candidate is None else candidate,
                       "send": list(send)}, ensure_ascii=True, separators=(",", ":"))
    return raw_reply(tokenizer, text)


def mixed_provider(tokenizer):
    """All task-independent traffic uses only currently held sender records."""

    def provide(view, rendered, tokenized):
        r, p = view.slot.round_number, view.peer
        own = [s for s in view.sources if type(s) is SourceRecord and s.owner == p]
        if r == 1:
            if p == 0:
                return reply(tokenizer, view, [{"to": 1, "source_refs": [reference(own[0])] * 3,
                                                "text": 'literal \\ " <|im_start|> old value 999'}])
            if p == 1:
                return reply(tokenizer, view, [{"to": 2, "text": "text only"}])
            if p == 2:
                return reply(tokenizer, view, [{"to": 3}])
            return reply(tokenizer, view, [{"to": 0, "source_refs": [reference(own[0])]}, {"to": p}])
        if r == 2:
            return reply(tokenizer, view, [{"to": (p + 1) % 4,
                "source_refs": [reference(view.sources[0])], "text": ""}])
        if r == 3 and p == 0:
            return raw_reply(tokenizer, "")  # Literal silence is recorded invalid output.
        if r == 3 and p == 1:
            return None  # Explicitly recorded failure, not an unexecuted opportunity.
        if r == 4 and p == 2:
            return reply(tokenizer, view, [{"to": (p + 1) % 4,
                                            "source_refs": [{"record_id": "unseen", "version": 1}]}])
        return reply(tokenizer, view, [{"to": (p + 1) % 4,
                                        "source_refs": [reference(s) for s in own],
                                        "text": f"round {r} peer {p}"}])
    return provide


def peer_messages(state):
    return tuple(d for d in state.deliveries if d.origin == "peer")


class SynchronousRoundTests(unittest.TestCase):
    def setUp(self):
        self.world = world()
        self.state = initial_branch(self.world, PREFIX_ID)

    def test_initial_host_acquisition_is_private_and_metadata_is_not_prompt_identity(self):
        prepared = prepare_round(self.state, TOKENIZER)
        for p, view in enumerate(prepared.views):
            self.assertEqual(view.sources, tuple(s for s in self.world.records if s.owner == p))
            deliveries = [d for d in self.state.deliveries if d.recipient == p]
            self.assertEqual(len(deliveries), self.world.size.shard_size)
            self.assertTrue(all(d.origin == "host" and d.sender is None and d.generated is None
                                and d.acquired and d.first_usable == Slot("prefix", 1) for d in deliveries))
            self.assertNotIn(PREFIX_ID, prepared.rendered[p].content)
            self.assertNotIn("delivery_id", prepared.rendered[p].content)
            self.assertNotIn("message_id", prepared.rendered[p].content)

    def test_all_rendering_and_generation_precede_validation_and_recipient_effects(self):
        events = []
        originals = (rounds.render_request, rounds.tokenize_request, rounds.validate_reply)
        def render(view):
            events.append(("render", view.peer))
            return originals[0](view)
        def tokenize(request, tokenizer):
            events.append(("tokenize", None))
            return originals[1](request, tokenizer)
        def validate(view, generated, tokenizer):
            events.append(("validate", view.peer))
            self.assertEqual(snapshot_bytes(self.state), before)
            return originals[2](view, generated, tokenizer)
        def provider(view, rendered, tokenized):
            events.append(("generate", view.peer))
            self.assertEqual(rendered, originals[0](view))
            self.assertEqual(snapshot_bytes(self.state), before)
            self.assertEqual(view.history, ())
            self.assertFalse(any(s.owner != view.peer for s in view.sources))
            return reply(TOKENIZER, view, [{"to": (view.peer + 1) % 4,
                "source_refs": [reference(view.sources[0])], "text": "current output"}])
        before = snapshot_bytes(self.state)
        with patch.object(rounds, "render_request", render), patch.object(rounds, "tokenize_request", tokenize), \
                patch.object(rounds, "validate_reply", validate):
            result = run_round(self.state, TOKENIZER, provider, invocation_order=(3, 2, 1, 0))
        self.assertEqual([e[0] for e in events], ["render"] * 4 + ["tokenize"] * 4
                         + ["generate"] * 4 + ["validate"] * 4)
        for peer in result.committed.peers:
            self.assertEqual(len(peer.sources), self.world.size.shard_size + 1)
            self.assertEqual(len(peer.history), 2)
        self.assertEqual(snapshot_bytes(self.state), before)

    def test_source_plus_text_text_only_empty_and_wholly_invalid_commit_together(self):
        result = run_round(self.state, TOKENIZER, mixed_provider(TOKENIZER))
        state = result.committed
        attempts = peer_messages(state)
        sources = [d for d in attempts if d.source is not None]
        self.assertEqual(len(sources), 3)
        self.assertEqual([d.acquired for d in sources], [True, False, False])
        self.assertEqual(len({d.delivery_id for d in sources}), 3)
        self.assertEqual(len({d.message_id for d in sources}), 1)
        self.assertTrue(all(d.sender == 0 and d.recipient == 1 and d.generated == Slot("prefix", 1)
                            and d.first_usable == Slot("prefix", 2) for d in attempts if d.sender == 0))
        self.assertEqual(state.peers[1].sources[0], self.state.peers[0].sources[0])
        self.assertEqual(state.peers[1].history[-1].text, 'literal \\ " <|im_start|> old value 999')
        self.assertEqual(state.peers[2].sources, self.state.peers[2].sources)  # Text does not become evidence.
        self.assertEqual(state.peers[2].history[-1].text, "text only")
        self.assertFalse(any(d.sender in (2, 3) for d in attempts))
        self.assertEqual(result.barrier.replies[3].candidate.status, "invalid")
        self.assertIsNone(state.peers[3].candidate.value)
        self.assertEqual(state.pending, ())

    def test_explicit_empty_text_is_archived_but_omitted_text_has_no_component(self):
        def provider(view, *_):
            return reply(TOKENIZER, view, [{"to": (view.peer + 1) % 4, "text": ""}])
        result = run_round(self.state, TOKENIZER, provider)
        self.assertEqual(len(peer_messages(result.committed)), 4)
        self.assertTrue(all(d.text == "" and d.source is None for d in peer_messages(result.committed)))
        self.assertTrue(all(p.history[-1].text == "" for p in result.committed.peers))

    def test_repeated_resends_remain_attempts_without_new_acquisitions_or_duplicate_effects(self):
        first = run_round(self.state, TOKENIZER, mixed_provider(TOKENIZER))
        def provider(view, *_):
            return reply(TOKENIZER, view, [{"to": 1, "source_refs": [reference(view.sources[0])] * 3}]
                         if view.peer == 0 else [])
        second = run_round(first.committed, TOKENIZER, provider)
        extra = peer_messages(second.committed)[len(peer_messages(first.committed)):]
        self.assertEqual(len(extra), 3)
        self.assertTrue(all(d.acquired is False for d in extra))
        self.assertEqual(second.committed.peers[1].source_deliveries,
                         first.committed.peers[1].source_deliveries)
        self.assertEqual(commit_round(second.barrier), second)
        self.assertEqual(drain_deliveries(second.committed), second.committed)
        self.assertEqual(drain_deliveries(second.committed, tuple(d.delivery_id for d in extra)), second.committed)
        with self.assertRaises(ValueError):
            drain_deliveries(second.committed, ("unknown",))

    def test_uncommitted_stage_cannot_schedule_and_source_text_components_release_independently(self):
        prepared = prepare_round(self.state, TOKENIZER)
        generated = tuple(mixed_provider(TOKENIZER)(v, r, t)
                          for v, r, t in zip(prepared.views, prepared.rendered, prepared.tokenized))
        barrier = validate_round(prepared, generated, TOKENIZER)
        staged = stage_effects(barrier)
        self.assertEqual(staged.peers[1].sources, self.state.peers[1].sources)
        self.assertEqual(len(staged.peers[1].history), 1)  # Only its own reply, never incoming prose.
        with self.assertRaises(ValueError):
            prepare_round(staged, TOKENIZER)
        with self.assertRaisesRegex(ValueError, "every validated source"):
            drain_deliveries(staged, ())
        source_ids = tuple(d.delivery_id for d in staged.pending if d.source is not None)
        source_committed = drain_deliveries(staged, source_ids)
        self.assertTrue(source_committed.committed)
        self.assertEqual(len(source_committed.pending), 2)
        next_requests = prepare_round(source_committed, TOKENIZER)
        self.assertNotIn("literal", next_requests.rendered[1].content)
        self.assertNotIn("text only", next_requests.rendered[2].content)
        data = json.loads(next_requests.rendered[1].content.split("\nPeer data (JSON):\n", 1)[1])
        self.assertNotIn("pending", data)
        self.assertNotIn("queue", data)
        self.assertEqual(drain_deliveries(source_committed), commit_round(barrier).committed)
        self.assertEqual(deserialize_state(snapshot_bytes(staged)), staged)

    def test_invalid_and_recorded_failed_slots_never_backfill_candidates_and_feedback_is_next_call(self):
        first = run_round(self.state, TOKENIZER, lambda v, *_: reply(TOKENIZER, v))
        second = run_round(first.committed, TOKENIZER, lambda v, *_: None if v.peer == 0 else raw_reply(TOKENIZER, "bad"))
        self.assertEqual(second.committed.peers[0].candidate.status, "failed")
        self.assertIsNone(second.committed.peers[0].candidate.value)
        self.assertEqual(second.committed.peers[0].feedback, ())
        self.assertEqual(len(second.committed.peers[0].history), 1)
        for peer in second.committed.peers[1:]:
            self.assertEqual(peer.candidate.status, "invalid")
            self.assertIsNone(peer.candidate.value)
            self.assertEqual(peer.feedback[-1].slot, Slot("prefix", 2))
        self.assertTrue(all(not v.feedback for v in second.barrier.requests.views))
        next_views = prepare_round(second.committed, TOKENIZER).views
        self.assertEqual(next_views[1].feedback[-1].slot, Slot("prefix", 2))

    def test_bad_order_missing_reply_overflow_and_provider_exception_never_commit(self):
        before = snapshot_bytes(self.state)
        for order in ((0, 1, 2), (0, 1, 2, 2), (False, 1, 2, 3)):
            with self.assertRaises(ValueError):
                run_round(self.state, TOKENIZER, lambda *_: self.fail("must not call"), invocation_order=order)
        with self.assertRaises(ValueError):
            validate_round(prepare_round(self.state, TOKENIZER), (None,) * 3, TOKENIZER)
        class Oversized(RoundTokenizer):
            def __call__(self, *args, **kwargs):
                return {"input_ids": [1] * 8192, "attention_mask": [1] * 8192}
        with self.assertRaisesRegex(ValueError, "no truncation"):
            run_round(self.state, Oversized(), lambda *_: self.fail("must not call"))
        calls = []
        def interrupted(view, *_):
            calls.append(view.peer)
            if view.peer == 1:
                raise RuntimeError("recording interrupted")
            return reply(TOKENIZER, view)
        with self.assertRaises(RuntimeError):
            run_round(self.state, TOKENIZER, interrupted)
        self.assertEqual(calls, [0, 1])
        self.assertEqual(snapshot_bytes(self.state), before)

    def test_tombstone_is_exact_known_current_acquisition_and_pending_has_no_endpoints(self):
        original = world(Task.BFS)
        prefix = run_prefix(original, PREFIX_ID, TOKENIZER, lambda v, *_: reply(TOKENIZER, v))
        state = fork_prefix(prefix.snapshot, "scripted/recovery/revision/L/rep0")
        old = original.records[0]
        public = next(s for s in state.manifest if s.record_id == old.record_id)
        tombstone = replace(old, version=2, deleted=True)
        peers = []
        for p, peer in enumerate(state.peers):
            current = [s for s in peer.sources if s.record_id != old.record_id]
            current.append(tombstone if p == old.owner else PendingSource(
                old.record_id, old.owner, old.position, 2))
            metadata = tuple(d for d in peer.source_deliveries if d.record_id != old.record_id)
            if p == old.owner:
                metadata += (SourceDelivery(old.record_id, 2, "host", None, None, Slot("recovery", 1)),)
            peers.append(replace(peer, sources=tuple(sorted(current, key=lambda s: s.record_id)),
                                 notice=RevisionNotice(public, 1, 2), source_deliveries=metadata))
        state = replace(state, peers=tuple(peers))
        self.assertEqual(deserialize_state(snapshot_bytes(state)), state)
        before = prepare_round(state, TOKENIZER)
        recipient = (old.owner + 1) % 4
        data = json.loads(before.rendered[recipient].content.split("\nPeer data (JSON):\n")[1])
        changed = next(s for s in data["current_sources"] if s["record_id"] == old.record_id)
        self.assertEqual(changed["status"], "update_pending")
        self.assertNotIn("endpoints", changed)
        result = run_round(state, TOKENIZER, lambda v, *_: reply(TOKENIZER, v,
            [{"to": recipient, "source_refs": [reference(tombstone)]}] if v.peer == old.owner else []))
        delivered = next(s for s in result.committed.peers[recipient].sources if s.record_id == old.record_id)
        self.assertEqual(delivered, tombstone)
        attempt = peer_messages(result.committed)[-1]
        self.assertTrue(attempt.acquired)
        self.assertEqual(attempt.first_usable, Slot("recovery", 2))
        self.assertEqual(prepare_round(result.committed, TOKENIZER).views[recipient].sources,
                         result.committed.peers[recipient].sources)

    def test_recipient_newer_version_or_conflicting_payload_fails_without_partial_effects(self):
        prepared = prepare_round(self.state, TOKENIZER)
        generated = tuple(reply(TOKENIZER, v, [{"to": 1, "source_refs": [reference(v.sources[0])]}]
                                if v.peer == 0 else []) for v in prepared.views)
        staged = stage_effects(validate_round(prepared, generated, TOKENIZER))
        source = staged.pending[0].source
        for existing in (PendingSource(source.record_id, source.owner, source.position, 2),
                         replace(source, value=1 if source.value != 1 else 2)):
            peers = list(staged.peers)
            peers[1] = replace(peers[1], sources=peers[1].sources + (existing,))
            corrupt = replace(staged, peers=tuple(peers))
            before = snapshot_bytes(corrupt)
            with self.assertRaisesRegex(ValueError, "current source authority"):
                drain_deliveries(corrupt)
            self.assertEqual(snapshot_bytes(corrupt), before)


class SharedPrefixTests(unittest.TestCase):
    def test_reversed_invocation_identical_requests_raw_replies_messages_states_and_snapshots_all_contracts(self):
        for task in Task:
            for size in Size:
                with self.subTest(task=task, size=size):
                    original = world(task, size)
                    normal = run_prefix(original, PREFIX_ID, TOKENIZER, mixed_provider(TOKENIZER))
                    reverse = run_prefix(original, PREFIX_ID, TOKENIZER, mixed_provider(TOKENIZER),
                                         invocation_order=(3, 2, 1, 0))
                    self.assertEqual(normal, reverse)
                    self.assertEqual(asdict(normal), asdict(reverse))
                    state = deserialize_state(normal.snapshot)
                    self.assertEqual(state, normal.rounds[-1].committed)
                    self.assertEqual(snapshot_bytes(state), normal.snapshot)
                    self.assertEqual(state.pending, ())
                    for source in state.manifest:
                        self.assertEqual(normal.owner_v1_exposure(source), tuple(Slot("prefix", r) for r in range(1, 5)))

    def test_round_four_source_and_prose_are_drained_before_prefix_freeze(self):
        original = world()
        prefix = run_prefix(original, PREFIX_ID, TOKENIZER, mixed_provider(TOKENIZER))
        state = deserialize_state(prefix.snapshot)
        fourth = [d for d in peer_messages(state) if d.generated == Slot("prefix", 4)]
        self.assertTrue(fourth)
        self.assertTrue(all(d.first_usable == Slot("recovery", 1) for d in fourth))
        for d in fourth:
            peer = state.peers[d.recipient]
            if d.source is not None:
                self.assertIn(d.source, peer.sources)
            else:
                self.assertIn(ReceivedProse(d.generated, d.sender, d.text), peer.history)
        for r, trace in enumerate(prefix.rounds, 1):
            self.assertEqual(trace.barrier.requests.slot, Slot("prefix", r))
            self.assertEqual(len(trace.barrier.requests.rendered), 4)
            self.assertEqual(len(trace.barrier.replies), 4)
            for validation in trace.barrier.replies:
                if validation.generated is not None:
                    self.assertEqual(validation.own_reply.text, validation.generated.text)

    def test_deep_deserialization_and_mutable_payload_exports_never_share_nested_state(self):
        for task in (Task.PREFIX, Task.BFS):
            prefix = run_prefix(world(task), PREFIX_ID, TOKENIZER, mixed_provider(TOKENIZER))
            parent = deserialize_state(prefix.snapshot)
            first = fork_prefix(prefix.snapshot, "scripted/recovery/sham/B/rep0")
            second = fork_prefix(prefix.snapshot, "scripted/recovery/sham/C/rep0")
            for i in PEERS:
                self.assertIsNot(first.peers[i], parent.peers[i])
                self.assertIsNot(first.peers[i].sources[0], second.peers[i].sources[0])
                self.assertIsNot(first.peers[i].candidate, second.peers[i].candidate)
            original_second, original_parent = snapshot_bytes(second), snapshot_bytes(parent)
            with self.assertRaises(FrozenInstanceError):
                first.peers[0].sources[0].version = 999
            # Deliberately bypass frozen records to demonstrate deep isolation,
            # not just protection from the public mutation API.
            object.__setattr__(first.peers[0].sources[0], "version", 999)
            object.__setattr__(first.peers[0].history[0], "text", "mutated sibling")
            object.__setattr__(first.peers[0].candidate, "value", ())
            object.__setattr__(first.peers[0].source_deliveries[0], "origin", "mutated")
            self.assertEqual(snapshot_bytes(second), original_second)
            self.assertEqual(snapshot_bytes(parent), original_parent)
            self.assertEqual(prefix.snapshot, original_parent)
            exported = asdict(second)
            exported["peers"][0]["history"][0]["text"] = "export mutation"
            candidate = second.peers[0].candidate.payload(task)
            if type(candidate) is dict:
                candidate["0"] = 999
            else:
                candidate[0] = 999
            self.assertEqual(snapshot_bytes(second), original_second)

    def test_four_opportunities_each_phase_survive_early_correctness_invalidity_and_failure(self):
        original = world()
        truth = solve_world(original)
        early = {p: truth.candidate(p) for p in PEERS}  # Scripted inputs, scored only offline.
        calls = []
        def provider(view, *_):
            calls.append((view.slot, view.peer))
            if view.slot.round_number == 1:
                return reply(TOKENIZER, view, candidate=early[view.peer])
            if view.slot.round_number == 2:
                return None
            return raw_reply(TOKENIZER, "")
        prefix = run_prefix(original, PREFIX_ID, TOKENIZER, provider)
        for p, validation in enumerate(prefix.rounds[0].barrier.replies):
            self.assertTrue(exact_candidate(truth, validation.candidate.payload(original.task), p))
        state = fork_prefix(prefix.snapshot, "scripted/recovery/sham/B/rep0")
        for _ in range(4):
            state = run_round(state, TOKENIZER, provider).committed
        self.assertEqual(calls, [(Slot(phase, r), p) for phase in ("prefix", "recovery")
                                for r in range(1, 5) for p in PEERS])
        self.assertTrue(all(p.candidate.status == "invalid" and p.candidate.value is None for p in state.peers))
        self.assertIsNone(state.next_slot)
        with self.assertRaisesRegex(ValueError, "four scheduled"):
            run_round(state, TOKENIZER, provider)
        self.assertEqual(len(calls), 32)

    def test_final_continuation_deliveries_are_drained_without_scheduling_round_five(self):
        prefix = run_prefix(world(), PREFIX_ID, TOKENIZER, lambda v, *_: reply(TOKENIZER, v))
        state = fork_prefix(prefix.snapshot, "scripted/recovery/sham/B/rep0")
        for _ in range(4):
            state = run_round(state, TOKENIZER, mixed_provider(TOKENIZER)).committed
        self.assertEqual(state.pending, ())
        self.assertIsNone(state.next_slot)
        final = [d for d in peer_messages(state) if d.generated == Slot("recovery", 4)]
        self.assertTrue(final)
        self.assertTrue(all(d.first_usable == DeliveryBoundary() for d in final))
        self.assertEqual(deserialize_state(snapshot_bytes(state)), state)
        with self.assertRaises(ValueError):
            Slot("recovery", 5)

    def test_branch_scoped_new_messages_share_parent_records_without_prompt_leaks(self):
        prefix = run_prefix(world(), PREFIX_ID, TOKENIZER, mixed_provider(TOKENIZER))
        branches = [fork_prefix(prefix.snapshot, f"scripted/recovery/sham/{name}/rep0") for name in ("B", "C")]
        results = [run_round(s, TOKENIZER, mixed_provider(TOKENIZER)) for s in branches]
        self.assertEqual(results[0].barrier.requests.rendered, results[1].barrier.requests.rendered)
        self.assertEqual(results[0].barrier.replies, results[1].barrier.replies)
        count = len(branches[0].deliveries)
        for before, result in zip(branches, results):
            self.assertEqual(result.committed.deliveries[:count], before.deliveries)
            self.assertTrue(all(d.delivery_id.startswith(before.branch_id + "/r1/p")
                                for d in result.committed.deliveries[count:]))
            for rendered in result.barrier.requests.rendered:
                self.assertNotIn(before.branch_id, rendered.content)
                self.assertNotIn("acquired", rendered.content)
                self.assertNotIn("queue", rendered.content)
        self.assertTrue({d.delivery_id for d in results[0].committed.deliveries[count:]}.isdisjoint(
                        {d.delivery_id for d in results[1].committed.deliveries[count:]}))

    def test_prefix_freeze_rejects_incomplete_uncommitted_queued_and_continuation_states(self):
        initial = initial_branch(world(), PREFIX_ID)
        with self.assertRaises(ValueError):
            prefix_snapshot(initial)
        prefix = run_prefix(world(), PREFIX_ID, TOKENIZER, mixed_provider(TOKENIZER))
        final = prefix.rounds[-1]
        staged = stage_effects(final.barrier)
        for invalid in (staged, replace(final.committed, committed=False),
                        fork_prefix(prefix.snapshot, "scripted/recovery/sham/B/rep0")):
            with self.assertRaises(ValueError):
                prefix_snapshot(invalid)
        with self.assertRaises(ValueError):
            fork_prefix(prefix.snapshot, PREFIX_ID)
        with self.assertRaises(ValueError):
            fork_prefix(snapshot_bytes(staged), "scripted/recovery/sham/B/rep0")


if __name__ == "__main__":
    unittest.main()
