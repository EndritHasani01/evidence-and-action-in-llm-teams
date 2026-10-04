"""Scripted exact-parent and prose-delay acceptance; no inference or capacity claim."""

from dataclasses import replace
import json
import unittest
from unittest.mock import patch

from recovery.events import start_continuation
from recovery.replay import (commit_continuation_round, held_prose_counts,
                             obtain_continuation_round)
from recovery.rounds import (deserialize_state, drain_deliveries, prepare_round,
                             snapshot_bytes, stage_effects)
from recovery.state import OwnReply, ReceivedProse, Slot
from recovery.tasks import PEERS, Size, SourceRecord, Task
from tests.event_checks import build_prefix, case_world, scheduled, start, views
from tests.protocol_checks import reference
from tests.round_checks import TOKENIZER, raw_reply, reply

# Scripted CPU settings, not the accepted model/environment configuration.
SETTINGS = {"backend": "scripted", "do_sample": True, "temperature": 0.6,
            "max_new_tokens": 384, "stop": ["scripted_stop"]}


def replay_provider(tokenizer, mode="rich", seen=None):
    def provide(view, rendered, tokenized, *, seed, settings):
        if seen is not None:
            seen.append((view.peer, view.slot, seed, settings))
        p, r = view.peer, view.slot.round_number
        own = [s for s in view.sources if type(s) is SourceRecord and s.owner == p]
        if mode in ("silent", "empty"):
            send = [{"to": (p + 1) % 4, "source_refs": [reference(own[0])]}]
            if mode == "empty":
                send[0]["text"] = ""
            return reply(tokenizer, view, send)
        if r == 1:
            if p == 2:
                return raw_reply(tokenizer, "invalid first reply with private prose")
            if p == 3:
                return None
            retained = bool(view.history)
            source = own[0 if retained else 1]
            label = "prior" if retained else "fresh"
            send = [{"to": 1 - p, "source_refs": [reference(source)] * 2,
                     "text": f"UNSEEN_{p}_{label} mixed prose"},
                    {"to": 2, "text": f"UNSEEN_{p}_{label} text only"}]
            if p == 0:
                tombstone = next((s for s in view.sources if type(s) is SourceRecord and s.deleted), None)
                send.append({"to": 3, "source_refs": [reference(tombstone or source)]})
            return reply(tokenizer, view, send)
        incoming = any(type(e) is ReceivedProse and e.slot == Slot("recovery", 1) for e in view.history)
        # Later acquisition is allowed to diverge, based only on the local view.
        recipient = (p + (1 if incoming else 2)) % 4
        return reply(tokenizer, view, [{"to": recipient, "source_refs": [reference(own[2])],
                                        "text": f"round {r} sender {p}"}])
    return provide


def parent_records(world, prefix, tokenizer=TOKENIZER, event="revision", replicate=0, mode="rich"):
    return tuple(obtain_continuation_round(start(world, prefix, policy, event, replicate),
                    scheduled(world, event, policy, replicate), tokenizer,
                    replay_provider(tokenizer, mode), settings=SETTINGS)
                 for policy in ("B", "C"))


def replay_start(world, prefix, parents, policy, event="revision", replicate=0, tokenizer=TOKENIZER):
    return obtain_continuation_round(start(world, prefix, policy, event, replicate),
            scheduled(world, event, policy, replicate), tokenizer, settings=SETTINGS, parents=parents)


def peer_deliveries(state, round_number=1):
    return tuple(d for d in state.deliveries if d.generated == Slot("recovery", round_number))


class ReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = case_world(Task.SORT)
        cls.prefix = build_prefix(cls.world)
        cls.parents = parent_records(cls.world, cls.prefix)

    def test_both_masks_all_families_sizes_events_and_extra_replicate_parents(self):
        for size in Size:
            for task in Task:
                world = case_world(task, size)
                prefix = build_prefix(world)
                for event in ("revision", "sham"):
                    for replicate in (0, 1):
                        parents = parent_records(world, prefix, event=event, replicate=replicate)
                        for policy in ("P_G", "P_H"):
                            with self.subTest(size=size, task=task, event=event, replicate=replicate, policy=policy):
                                saved = replay_start(world, prefix, parents, policy, event, replicate)
                                group = world.partition[0 if policy == "P_G" else 1]
                                for p, call in enumerate(saved.calls):
                                    parent = parents[1 if p in group else 0]
                                    self.assertEqual(call.replay_parent, parent.calls[p].call_id)
                                    self.assertEqual(call.seed, parent.calls[p].seed)
                                    self.assertEqual(saved.settings_json, parent.settings_json)
                                    self.assertEqual(saved.barrier.requests.views[p], parent.barrier.requests.views[p])
                                    self.assertEqual(saved.barrier.requests.rendered[p], parent.barrier.requests.rendered[p])
                                    self.assertEqual(saved.barrier.requests.tokenized[p], parent.barrier.requests.tokenized[p])
                                    self.assertEqual(saved.barrier.replies[p], parent.barrier.replies[p])
                                self.assertEqual(commit_continuation_round(saved).committed.next_slot, Slot("recovery", 2))

    def test_mixed_assembly_is_branch_local_and_repeated_commit_is_idempotent(self):
        parent_states = tuple(commit_continuation_round(p).committed for p in self.parents)
        before = tuple(snapshot_bytes(s) for s in parent_states)
        siblings = []
        for policy in ("P_G", "P_H"):
            saved = replay_start(self.world, self.prefix, self.parents, policy)
            state = commit_continuation_round(saved).committed
            siblings.append(state)
            expected = tuple(sorted((m for r in saved.barrier.replies for m in r.messages),
                                    key=lambda m: (m.sender, m.recipient)))
            self.assertEqual(saved.barrier.messages, expected)
            for p in PEERS:
                self.assertEqual([e.text for e in state.peers[p].history if type(e) is ReceivedProse
                                  and e.slot == Slot("recovery", 1)],
                                 [m.text for m in expected if m.recipient == p and m.text is not None])
            effects = peer_deliveries(state)
            self.assertEqual(len(effects), sum(len(m.sources) + (m.text is not None) for m in expected))
            self.assertTrue(all(d.delivery_id.startswith(state.branch_id + "/") for d in effects))
            self.assertEqual(commit_continuation_round(saved).committed, state)
            self.assertEqual(drain_deliveries(state, tuple(d.delivery_id for d in effects) * 2), state)
        self.assertEqual(tuple(snapshot_bytes(s) for s in parent_states), before)
        left_ids, right_ids = ({d.delivery_id for d in peer_deliveries(s)} for s in siblings)
        self.assertFalse(left_ids & right_ids)
        self.assertNotEqual(siblings[0].peers, siblings[1].peers)

    def test_q_revision_sham_sources_own_reply_metadata_and_no_incoming_sentinel(self):
        for task in (Task.SORT, Task.BFS):
            for size in Size:
                world = case_world(task, size)
                prefix = build_prefix(world)
                for event in ("revision", "sham"):
                    parents = parent_records(world, prefix, event=event)
                    for i, policy in enumerate(("Q_B", "Q_C")):
                        q = commit_continuation_round(replay_start(world, prefix, parents, policy, event)).committed
                        parent = commit_continuation_round(parents[i]).committed
                        self.assertEqual(held_prose_counts(q), (1, 1, 2, 0))
                        self.assertEqual(held_prose_counts(parent), (0, 0, 0, 0))
                        for p, (a, b) in enumerate(zip(q.peers, parent.peers)):
                            self.assertEqual((a.sources, a.source_deliveries, a.candidate, a.feedback),
                                             (b.sources, b.source_deliveries, b.candidate, b.feedback))
                            self.assertEqual(a.history, tuple(e for e in b.history
                                if not (type(e) is ReceivedProse and e.slot == Slot("recovery", 1))))
                            content = prepare_round(q, TOKENIZER).rendered[p].content
                            for sender in (0, 1):
                                if sender != p:
                                    self.assertNotIn(f"UNSEEN_{sender}_", content)
                            self.assertNotIn(q.branch_id, content)
                            self.assertNotIn("pending_prose", content)
                        self.assertTrue(all(d.source is None and d.first_usable is None for d in q.pending))
                        self.assertEqual([(d.sender, d.recipient, d.source, d.acquired, d.first_usable)
                                          for d in peer_deliveries(q)],
                                         [(d.sender, d.recipient, d.source, d.acquired, d.first_usable)
                                          for d in peer_deliveries(parent) if d.source is not None])

    def test_release_order_existing_history_horizon_and_later_source_divergence(self):
        saved = replay_start(self.world, self.prefix, self.parents, "Q_B")
        q = commit_continuation_round(saved).committed
        parent = commit_continuation_round(self.parents[0]).committed
        held_ids = {d.delivery_id for d in q.pending}
        seen_history = tuple(p.history for p in q.peers)
        for r in range(2, 5):
            q = deserialize_state(snapshot_bytes(q))
            current = obtain_continuation_round(q, saved.branch, TOKENIZER,
                        replay_provider(TOKENIZER), settings=SETTINGS, parents=self.parents)
            q = commit_continuation_round(current).committed
            original = obtain_continuation_round(parent, self.parents[0].branch, TOKENIZER,
                        replay_provider(TOKENIZER), settings=SETTINGS)
            parent = commit_continuation_round(original).committed
            self.assertFalse(q.pending)
            self.assertEqual(held_prose_counts(q), (1, 1, 2, 0))
            if r == 2:
                self.assertNotEqual(tuple(p.sources for p in q.peers), tuple(p.sources for p in parent.peers))
                for p, peer in enumerate(q.peers):
                    self.assertEqual(peer.history[:len(seen_history[p])], seen_history[p])
                    appended = peer.history[len(seen_history[p]):]
                    self.assertIs(type(appended[0]), OwnReply)  # own round two precedes delayed incoming one
                    prose = [e for e in appended if type(e) is ReceivedProse]
                    self.assertEqual([(e.slot.round_number, e.sender) for e in prose],
                                     sorted((e.slot.round_number, e.sender) for e in prose))
            held = [d for d in q.deliveries if d.delivery_id in held_ids]
            self.assertEqual(len(held), len(held_ids))
            self.assertTrue(all(d.first_usable == Slot("recovery", 3) for d in held))
            for p, peer in enumerate(q.peers):
                self.assertEqual(sum(type(e) is ReceivedProse and e.slot == Slot("recovery", 1)
                                     for e in peer.history), held_prose_counts(q)[p])
        self.assertIsNone(q.next_slot)
        self.assertEqual(len({d.delivery_id for d in q.deliveries}), len(q.deliveries))
        with self.assertRaises(ValueError):
            obtain_continuation_round(q, saved.branch, TOKENIZER, settings=SETTINGS)

    def test_no_prose_and_explicit_empty_prose_remain_inactive_complete_branches(self):
        for mode in ("silent", "empty"):
            parents = parent_records(self.world, self.prefix, mode=mode)
            for policy in ("Q_B", "Q_C"):
                saved = replay_start(self.world, self.prefix, parents, policy)
                state = commit_continuation_round(saved).committed
                self.assertEqual(len(state.pending), 4 if mode == "empty" else 0)
                self.assertEqual(held_prose_counts(state), (0,) * 4)
                for _ in range(3):
                    current = obtain_continuation_round(state, saved.branch, TOKENIZER,
                        replay_provider(TOKENIZER, mode), settings=SETTINGS)
                    state = commit_continuation_round(current).committed
                self.assertIsNone(state.next_slot)
                self.assertFalse(state.pending)
                self.assertEqual(held_prose_counts(state), (0,) * 4)

    def test_invalid_failed_parents_are_literal_and_never_regenerated_or_backfilled(self):
        provider = lambda *a, **k: self.fail("replay cannot generate")
        for policy in ("P_G", "P_H", "Q_B", "Q_C"):
            saved = obtain_continuation_round(start(self.world, self.prefix, policy),
                scheduled(self.world, "revision", policy), TOKENIZER, provider,
                settings=SETTINGS, parents=self.parents)
            self.assertEqual(tuple(r.candidate.status for r in saved.barrier.replies),
                             ("valid", "valid", "invalid", "failed"))
            state = commit_continuation_round(saved).committed
            for p in (2, 3):
                self.assertIsNone(state.peers[p].candidate.value)
                self.assertEqual(state.peers[p].candidate.slot, Slot("recovery", 1))
                self.assertFalse(saved.barrier.replies[p].messages)
            self.assertEqual(saved.barrier.replies[2].generated.text, "invalid first reply with private prose")
            self.assertIsNone(saved.barrier.replies[3].generated)

    def test_all_failed_or_all_invalid_parent_round_still_satisfies_four_q_slots(self):
        for failed in (False, True):
            parent = obtain_continuation_round(start(self.world, self.prefix, "B"),
                scheduled(self.world, "revision", "B"), TOKENIZER,
                lambda *a, **k: None if failed else raw_reply(TOKENIZER, ""), settings=SETTINGS)
            saved = replay_start(self.world, self.prefix, (parent,), "Q_B")
            state = commit_continuation_round(saved).committed
            self.assertEqual(saved.barrier.replies, parent.barrier.replies)
            self.assertFalse(state.pending)
            self.assertFalse(peer_deliveries(state))
            self.assertEqual(held_prose_counts(state), (0,) * 4)
            self.assertTrue(all(p.candidate.status == ("failed" if failed else "invalid") for p in state.peers))

    def test_invalid_source_plus_prose_parent_has_no_partial_effects_or_held_text(self):
        def invalid(view, *args, **kwargs):
            return reply(TOKENIZER, view, [{"to": (view.peer + 1) % 4,
                "source_refs": [{"record_id": view.notice.source.record_id, "version": 1}],
                "text": "never delivered"}])
        parent = obtain_continuation_round(start(self.world, self.prefix, "B"),
            scheduled(self.world, "revision", "B"), TOKENIZER, invalid, settings=SETTINGS)
        q = replay_start(self.world, self.prefix, (parent,), "Q_B")
        self.assertEqual(q.barrier.replies, parent.barrier.replies)
        self.assertTrue(all(r.candidate.status == "invalid" for r in q.barrier.replies))
        state = commit_continuation_round(q).committed
        self.assertFalse(state.pending)
        self.assertFalse(peer_deliveries(state))
        self.assertEqual(held_prose_counts(state), (0,) * 4)
        with self.assertRaisesRegex(ValueError, "only after"):
            held_prose_counts(stage_effects(q.barrier))

    def test_complete_mixed_and_q_runs_use_four_replays_and_twelve_new_calls(self):
        for event in ("revision", "sham"):
            parents = parent_records(self.world, self.prefix, event=event)
            for policy in ("P_G", "P_H", "Q_B", "Q_C"):
                saved = replay_start(self.world, self.prefix, parents, policy, event)
                state = commit_continuation_round(saved).committed
                seen = []
                for _ in range(3):
                    current = obtain_continuation_round(state, saved.branch, TOKENIZER,
                        replay_provider(TOKENIZER, seen=seen), settings=SETTINGS, parents=parents)
                    state = commit_continuation_round(current).committed
                self.assertEqual(len(seen), 12)
                self.assertEqual({(p, slot.round_number) for p, slot, _, _ in seen},
                                 {(p, r) for p in PEERS for r in (2, 3, 4)})
                self.assertIsNone(state.next_slot)
                self.assertFalse(state.pending)

    def test_request_native_tokens_settings_seeds_and_permitted_views_must_match(self):
        parent = self.parents[0]
        requests = parent.barrier.requests
        altered = [replace(parent, settings_json=parent.settings_json.replace("0.6", "0.7")),
                   replace(parent, branch=replace(parent.branch, calls=(replace(parent.branch.calls[0],
                       seed=parent.branch.calls[0].seed + 1),) + parent.branch.calls[1:]))]
        for name, first in (
                ("rendered", replace(requests.rendered[0], content=requests.rendered[0].content + " ")),
                ("tokenized", replace(requests.tokenized[0], input_ids=requests.tokenized[0].input_ids + (1,))),
                ("views", replace(requests.views[0], history=()))):
            value = (first,) + getattr(requests, name)[1:]
            altered.append(replace(parent, barrier=replace(parent.barrier, requests=replace(requests, **{name: value}))))
        for wrong in altered:
            with self.subTest(wrong=wrong.settings_json), self.assertRaisesRegex(ValueError, "equality failed"):
                replay_start(self.world, self.prefix, (wrong,), "Q_B")

    def test_wrong_event_replicate_world_policy_peer_and_round_are_protocol_defects(self):
        branch = scheduled(self.world, "revision", "Q_B")
        start_state = start(self.world, self.prefix, "Q_B")
        others = [parent_records(self.world, self.prefix, event="sham")[0],
                  parent_records(self.world, self.prefix, replicate=1)[0], self.parents[1]]
        other_world = case_world(Task.BFS)
        others.append(parent_records(other_world, build_prefix(other_world))[0])
        second = commit_continuation_round(self.parents[0]).committed
        others.append(obtain_continuation_round(second, self.parents[0].branch, TOKENIZER,
                                                replay_provider(TOKENIZER), settings=SETTINGS))
        for other in others:
            changed_calls = tuple(replace(c, replay_parent=other.calls[c.peer].call_id)
                                  if c.round_number == 1 else c for c in branch.calls)
            with self.assertRaisesRegex(ValueError, "parent differs"):
                obtain_continuation_round(start_state, replace(branch, calls=changed_calls), TOKENIZER,
                    settings=SETTINGS, parents=(other,))
        changed = (replace(branch.calls[0], replay_parent=self.parents[0].calls[1].call_id),) + branch.calls[1:]
        with self.assertRaisesRegex(ValueError, "parent differs"):
            obtain_continuation_round(start_state, replace(branch, calls=changed), TOKENIZER,
                                       settings=SETTINGS, parents=self.parents)

    def test_missing_parent_is_unexecuted_not_failed_and_duplicate_records_are_rejected(self):
        for parents, pattern in (((), "missing prescribed"), ((self.parents[1],), "missing prescribed"),
                                 ((self.parents[0], self.parents[0]), "duplicate")):
            with self.assertRaisesRegex(ValueError, pattern):
                replay_start(self.world, self.prefix, parents, "Q_B")
        branch = scheduled(self.world, "revision", "Q_B")
        changed = replace(branch, calls=tuple(replace(c, replay_parent=None) for c in branch.calls))
        with self.assertRaisesRegex(ValueError, "required replay"):
            obtain_continuation_round(start(self.world, self.prefix, "Q_B"), changed, TOKENIZER,
                                       replay_provider(TOKENIZER), settings=SETTINGS)

    def test_changed_recorded_validation_is_rejected_without_repair(self):
        parent = self.parents[0]
        replies = (replace(parent.barrier.replies[0], prose_tokens=999),) + parent.barrier.replies[1:]
        wrong = replace(parent, barrier=replace(parent.barrier, replies=replies))
        with self.assertRaisesRegex(ValueError, "recorded parent outcome"):
            replay_start(self.world, self.prefix, (wrong,), "Q_B")

    def test_new_slots_never_use_unrelated_cache_and_receive_saved_seed_settings(self):
        seen = []
        parent = self.parents[0]
        state = commit_continuation_round(parent).committed
        saved = obtain_continuation_round(state, parent.branch, TOKENIZER, replay_provider(TOKENIZER, seen=seen),
                    settings=SETTINGS, parents=self.parents, invocation_order=reversed(PEERS))
        self.assertEqual([p for p, _, _, _ in seen], list(reversed(PEERS)))
        self.assertEqual({p: seed for p, _, seed, _ in seen}, {c.peer: c.seed for c in saved.calls})
        self.assertTrue(all(settings == SETTINGS for _, _, _, settings in seen))
        self.assertTrue(all(c.replay_parent is None for c in saved.calls))
        seen[0][3]["stop"].append("mutation")
        self.assertEqual(json.loads(saved.settings_json), SETTINGS)
        self.assertEqual(seen[1][3], SETTINGS)
        with self.assertRaisesRegex(ValueError, "new scheduled generation"):
            obtain_continuation_round(state, parent.branch, TOKENIZER, settings=SETTINGS, parents=self.parents)

    def test_q_tombstones_and_duplicate_attempts_preserve_normal_source_authority(self):
        world = case_world(Task.BFS)
        prefix = build_prefix(world)
        parents = parent_records(world, prefix)
        q = commit_continuation_round(replay_start(world, prefix, parents, "Q_B")).committed
        tombstones = [d for d in peer_deliveries(q) if d.source.deleted]
        self.assertTrue(tombstones)
        self.assertTrue(all(d.source.version == 2 and not d.acquired for d in tombstones))
        repeated = [d for d in peer_deliveries(q) if d.sender == 0 and d.recipient == 1]
        self.assertEqual(len(repeated), 2)
        self.assertEqual(repeated[0].source, repeated[1].source)
        self.assertNotEqual(repeated[0].delivery_id, repeated[1].delivery_id)
        self.assertFalse(repeated[1].acquired)

    def test_text_only_send_has_no_placeholder_and_held_payload_cannot_change_recipient_view(self):
        states = []
        for text in ("SECRET_ALPHA", "SECRET_BETA", None):
            parent = obtain_continuation_round(start(self.world, self.prefix, "C"),
                scheduled(self.world, "revision", "C"), TOKENIZER,
                lambda view, *a, **k: reply(TOKENIZER, view,
                    [{"to": 2, "text": text}] if view.peer == 0 and text is not None else []), settings=SETTINGS)
            states.append(commit_continuation_round(replay_start(self.world, self.prefix, (parent,), "Q_C")).committed)
        requests = [prepare_round(s, TOKENIZER) for s in states]
        self.assertEqual(requests[0].views[2], requests[1].views[2])
        self.assertEqual(requests[0].views[2], requests[2].views[2])
        self.assertEqual(requests[0].rendered[2], requests[2].rendered[2])
        self.assertEqual(requests[0].tokenized[2], requests[2].tokenized[2])
        for request in requests:
            self.assertNotIn("SECRET_", request.rendered[2].content)
        self.assertNotEqual(requests[0].rendered[0], requests[1].rendered[0])  # own reply remains literal

    def test_parent_prefix_sibling_and_saved_raw_records_are_independent(self):
        originals = tuple(snapshot_bytes(p.barrier.requests.before) for p in self.parents)
        left = replay_start(self.world, self.prefix, self.parents, "Q_B")
        right = replay_start(self.world, self.prefix, self.parents, "Q_B")
        frozen_right = snapshot_bytes(commit_continuation_round(right).committed)
        object.__setattr__(left.barrier.replies[0].generated, "text", "mutated raw")
        state = commit_continuation_round(left).committed
        object.__setattr__(state.peers[0].sources[0], "value", 1234567)
        object.__setattr__(state.peers[0].candidate, "value", (1234567,) * self.world.world.size.shard_size)
        self.assertEqual(tuple(snapshot_bytes(p.barrier.requests.before) for p in self.parents), originals)
        self.assertEqual(snapshot_bytes(commit_continuation_round(right).committed), frozen_right)
        self.assertNotEqual(self.parents[0].barrier.replies[0].generated.text, "mutated raw")
        self.assertEqual(build_prefix(self.world).snapshot, self.prefix.snapshot)

    def test_reversed_order_and_no_offline_truth_access(self):
        parent_before = tuple(snapshot_bytes(p.barrier.requests.before) for p in self.parents)
        with patch("recovery.truth.solve_world", side_effect=AssertionError("offline truth access")):
            for policy in ("P_G", "Q_C"):
                forward = replay_start(self.world, self.prefix, self.parents, policy)
                reverse = obtain_continuation_round(start(self.world, self.prefix, policy),
                    scheduled(self.world, "revision", policy), TOKENIZER, settings=SETTINGS,
                    parents=self.parents, invocation_order=reversed(PEERS))
                self.assertEqual(forward, reverse)
                self.assertEqual(commit_continuation_round(forward), commit_continuation_round(reverse))
        self.assertEqual(tuple(snapshot_bytes(p.barrier.requests.before) for p in self.parents), parent_before)


if __name__ == "__main__":
    unittest.main()
