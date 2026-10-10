"""Course intervention acceptance through saved inputs and real protocol paths.

Explicit CPU suite, excluded from dependency-free discovery. The native harness
runs these same assertions with the pinned local 4B tokenizer, without weights.
"""

from dataclasses import asdict, replace
import json
import unittest
from unittest.mock import patch

from recovery.events import start_continuation
from recovery.inference import QWEN_4B, candidate_settings
from recovery.prompts import COURSE_LIMITS, render_request, rendered_data, tokenize_request
from recovery.protocol import GeneratedReply, validate_reply
from recovery.replay import commit_continuation_round, held_prose_counts, obtain_continuation_round
from recovery.rounds import (deserialize_state, drain_deliveries, prefix_snapshot,
                             prepare_round, run_prefix, run_round, snapshot_bytes, stage_effects)
from recovery.state import (CandidateState, ContinueNotice, OwnReply, PendingSource,
                            ReceivedProse, RevisionNotice, Slot, held_source, revise_source)
from recovery.tasks import PEERS, SourceRecord, Task
from tests.course_intervention_cases import (TOKENIZER, branches, course_inputs,
                                            first_rounds, prefix_case, scheduled)
from tests.event_checks import views
from tests.protocol_checks import placeholder, reference
from tests.replay_checks import peer_deliveries, replay_provider
from tests.round_checks import raw_reply, reply


class CourseInterventionTests(unittest.TestCase):
    tokenizer = TOKENIZER

    @classmethod
    def setUpClass(cls):
        population, _ = course_inputs()
        cls.settings = candidate_settings(cls.tokenizer, QWEN_4B, limits=COURSE_LIMITS)
        cls.cases = []
        for world in population.main + population.development:
            prefix = prefix_case(world, cls.tokenizer)
            cls.cases.append((world, prefix, first_rounds(world, prefix, cls.tokenizer)))

    def rendered(self, view):
        return render_request(view, limits=COURSE_LIMITS)

    def test_prefix_helper_applies_course_caps_and_preserves_thesis_default(self):
        world, prefix, _ = self.cases[0]
        branch = next(b for b in branches(world) if b.phase == "prefix")
        provider = lambda view, *_: GeneratedReply(
            json.dumps(dict(candidate=placeholder(view), send=[])), (1,) * 257, "length")
        course = run_prefix(world.world, branch.branch_id, self.tokenizer, provider, limits=COURSE_LIMITS)
        thesis = run_prefix(world.world, branch.branch_id, self.tokenizer, provider)
        self.assertTrue(all(r.candidate.status == "invalid" for result in course.rounds for r in result.barrier.replies))
        self.assertTrue(all(r.protocol_valid for result in thesis.rounds for r in result.barrier.replies))
        for result in prefix.rounds:
            for view, rendered, tokens in zip(result.barrier.requests.views,
                    result.barrier.requests.rendered, result.barrier.requests.tokenized):
                self.assertEqual(rendered, self.rendered(view))
                self.assertEqual(tokens, tokenize_request(rendered, self.tokenizer, limits=COURSE_LIMITS))

    def test_all_saved_course_starts_have_literal_evidence_retention_and_original_parents(self):
        population, schedule = course_inputs()
        seen = set()
        for world, prefix, records in self.cases:
            original = deserialize_state(prefix.snapshot)
            self.assertFalse(original.pending)
            self.assertEqual(prefix_snapshot(original), prefix.snapshot)
            for saved in records.values():
                branch, state = saved.branch, saved.barrier.requests.before
                seen.add(branch.branch_id)
                with self.subTest(branch=branch.branch_id):
                    self.assertEqual(state.prefix_parent, original.branch_id)
                    self.assertEqual(state.last_slot, Slot("prefix", 4))
                    self.assertTrue(state.boundary_applied)
                    self.assertFalse(state.pending)
                    self.assertEqual(deserialize_state(snapshot_bytes(state)), state)
                    expected = {s.record_id: s for s in world.event_world(branch.event).records}
                    base = {"B_delta": "B", "C_delta": "C", "K_delta": "K", "Q_B": "B", "Q_C": "C"}.get(branch.policy, branch.policy)
                    group = world.partition[0 if base == "P_G" else 1] if base in ("P_G", "P_H") else ()
                    changed = None if branch.event == "sham" else state.peers[0].notice.source.record_id
                    for p, (old, new) in enumerate(zip(original.peers, state.peers)):
                        sources = {s.record_id: s for s in old.sources}
                        if changed is not None:
                            sources[changed] = (PendingSource(changed, expected[changed].owner, expected[changed].position, 2)
                                if base == "L" and p != expected[changed].owner else expected[changed])
                        if base == "F":
                            sources = {k: s for k, s in sources.items() if s.owner == p or k == changed}
                        self.assertEqual(new.sources, tuple(sources[k] for k in sorted(sources)))
                        if base in ("C", "F") or p in group:
                            self.assertEqual((new.history, new.feedback, new.candidate), ((), (), CandidateState()))
                        elif base == "K":
                            self.assertEqual((new.history, new.feedback), ((), ()))
                            self.assertEqual(new.candidate, replace(old.candidate, historical=True))
                        else:
                            self.assertEqual((new.history, new.feedback, new.candidate), (old.history, old.feedback, old.candidate))
                        if changed is not None:
                            self.assertIsNone(held_source(views(state)[p], changed, 1))
                        else:
                            self.assertEqual(new.notice, ContinueNotice())
                            self.assertIsNone(new.receipt)
                    if branch.replicate:
                        primary = records[scheduled(world, branch.event, branch.policy).branch_id]
                        self.assertEqual(state.peers, primary.barrier.requests.before.peers)
                    with self.assertRaises(ValueError):
                        start_continuation(snapshot_bytes(state), world, branch)
            for edit in (world.main_edit, world.preserving_edit):
                if edit is not None:
                    public = next(s for s in original.manifest if s.record_id == edit.record_id)
                    self.assertEqual(prefix.owner_v1_exposure(public), tuple(Slot("prefix", r) for r in range(1, 5)))
            self.assertEqual(snapshot_bytes(original), prefix.snapshot)
        expected = {b.branch_id for b in schedule.main + schedule.development if b.phase == "continuation"}
        self.assertEqual(seen, expected)
        self.assertEqual(len(self.cases), len(population.main + population.development))

    def test_b_c_k_masks_and_q_have_equal_sources_without_condition_leaks(self):
        for world, _, records in self.cases:
            for saved in records.values():
                b = saved.branch
                if b.policy not in ("C", "K", "P_G", "P_H", "Q_B", "Q_C"):
                    continue
                parent = records[scheduled(world, b.event, "B", b.replicate).branch_id]
                for p, (a, c) in enumerate(zip(saved.barrier.requests.views, parent.barrier.requests.views)):
                    self.assertEqual((a.sources, a.source_deliveries, a.notice, a.receipt),
                                     (c.sources, c.source_deliveries, c.notice, c.receipt))
                    content = saved.barrier.requests.rendered[p].content
                    for label in (b.branch_id, "reset_group", "replay_parent", "gold", "held_prose"):
                        self.assertNotIn(label, content)

    def test_genuine_receipts_change_only_before_field_and_cannot_forward_old_authority(self):
        for world, _, records in self.cases:
            if world.world.task not in (Task.PREFIX, Task.SORT):
                continue
            old = next(s for s in world.world.records if s.record_id == world.main_edit.record_id)
            for policy in ("B", "C", "K"):
                ordinary, disclosed = (records[scheduled(world, "revision", p).branch_id] for p in (policy, policy + "_delta"))
                for a, b in zip(ordinary.barrier.requests.views, disclosed.barrier.requests.views):
                    left, right = (rendered_data(self.rendered(v)) for v in (a, b))
                    self.assertEqual(left["historical_receipt"]["before_value"], "not included in this receipt")
                    self.assertEqual(right["historical_receipt"]["before_value"], old.value)
                    left["historical_receipt"]["before_value"] = old.value
                    self.assertEqual(left, right)
                    bad = reply(self.tokenizer, b, [{"to": (b.peer + 1) % 4, "source_refs": [reference(old)]}])
                    invalid = validate_reply(b, bad, self.tokenizer, limits=COURSE_LIMITS)
                    self.assertFalse(invalid.protocol_valid)
                    self.assertEqual(invalid.messages, ())
                    self.assertIsNone(held_source(b, old.record_id, 1))

    def test_every_prescribed_parent_matches_view_rendered_tokens_settings_seed_and_outcome(self):
        seen = set()
        for _, _, records in self.cases:
            parents = {c.call_id: (saved, p) for saved in records.values() for p, c in enumerate(saved.calls)}
            for saved in records.values():
                for p, call in enumerate(saved.calls):
                    if call.replay_parent is None:
                        continue
                    seen.add(call.call_id)
                    parent, i = parents[call.replay_parent]
                    self.assertEqual((i, parent.branch.event, parent.branch.replicate),
                                     (p, saved.branch.event, saved.branch.replicate))
                    for name in ("views", "rendered", "tokenized"):
                        self.assertEqual(getattr(saved.barrier.requests, name)[p], getattr(parent.barrier.requests, name)[i])
                    self.assertEqual(saved.settings_json, parent.settings_json)
                    self.assertEqual(call.seed, parent.calls[i].seed)
                    self.assertEqual(call.generation_id, parent.calls[i].generation_id)
                    self.assertEqual(saved.barrier.replies[p], parent.barrier.replies[i])
        _, schedule = course_inputs()
        self.assertEqual(seen, {c.call_id for b in schedule.main + schedule.development for c in b.calls if c.replay_parent})

    def test_complete_course_horizons_keep_all_opportunities_and_accumulate_new_history(self):
        for world, _, records in self.cases:
            for first in records.values():
                state = commit_continuation_round(first).committed
                persistent = tuple((p.notice, p.receipt) for p in state.peers)
                compact = tuple(p.candidate for p in first.barrier.requests.before.peers)
                calls = []
                for r in range(2, 5):
                    saved = obtain_continuation_round(deserialize_state(snapshot_bytes(state)), first.branch,
                        self.tokenizer, replay_provider(self.tokenizer, seen=calls), settings=self.settings)
                    state = commit_continuation_round(saved).committed
                    self.assertEqual(tuple((p.notice, p.receipt) for p in state.peers), persistent)
                    for p, peer in enumerate(state.peers):
                        own_slots = [e.slot.round_number for e in peer.history if type(e) is OwnReply and e.slot.phase == "recovery"]
                        self.assertEqual(own_slots, ([] if first.barrier.replies[p].own_reply is None else [1]) + list(range(2, r + 1)))
                        self.assertEqual(peer.candidate.slot, Slot("recovery", r))
                        if first.branch.policy in ("K", "K_delta"):
                            self.assertEqual([e for e in peer.history if type(e) is CandidateState], [compact[p]])
                            self.assertEqual(compact[p].status, ("valid", "invalid", "failed", "valid")[p])
                            self.assertEqual(compact[p].payload(world.world.task),
                                placeholder(first.barrier.requests.views[p]) if p in (0, 3) else None)
                self.assertEqual(len(calls), 12)
                self.assertEqual({(p, slot.round_number) for p, slot, *_ in calls}, {(p, r) for p in PEERS for r in (2, 3, 4)})
                self.assertIsNone(state.next_slot)
                self.assertFalse(state.pending)
                self.assertEqual(deserialize_state(snapshot_bytes(state)), state)
                self.assertTrue(all(d.first_usable is not None for d in state.deliveries))

    def test_q_round_two_sources_own_reply_feedback_and_metadata_match_parent(self):
        active = inactive = 0
        for _, _, records in self.cases:
            for saved in records.values():
                if saved.branch.policy not in ("Q_B", "Q_C"):
                    continue
                q = commit_continuation_round(saved).committed
                parent_id = saved.calls[0].replay_parent.rsplit("/r", 1)[0]
                parent = commit_continuation_round(records[parent_id]).committed
                counts = held_prose_counts(q)
                active += any(counts)
                inactive += not any(counts)
                for p, (a, b) in enumerate(zip(q.peers, parent.peers)):
                    self.assertEqual((a.sources, a.source_deliveries, a.candidate, a.feedback),
                                     (b.sources, b.source_deliveries, b.candidate, b.feedback))
                    self.assertEqual(a.history, tuple(e for e in b.history if not (type(e) is ReceivedProse and e.slot == Slot("recovery", 1))))
                    rendered = prepare_round(q, self.tokenizer, limits=COURSE_LIMITS).rendered[p]
                    for sender in (0, 1):
                        if sender != p:
                            self.assertNotIn(f"UNSEEN_{sender}_", rendered.content)
                self.assertTrue(all(d.source is None and d.first_usable is None for d in q.pending))
                self.assertEqual([(d.sender, d.recipient, d.source, d.acquired, d.first_usable) for d in peer_deliveries(q)],
                    [(d.sender, d.recipient, d.source, d.acquired, d.first_usable) for d in peer_deliveries(parent) if d.source is not None])
        self.assertGreater(active, 0)
        self.assertGreater(inactive, 0)

    def test_q_release_is_ordered_idempotent_and_preserves_already_seen_history(self):
        for _, _, records in self.cases:
            for saved in records.values():
                if saved.branch.policy not in ("Q_B", "Q_C"):
                    continue
                state = commit_continuation_round(saved).committed
                counts, held = held_prose_counts(state), state.pending
                before = tuple(p.history for p in state.peers)
                second = obtain_continuation_round(state, saved.branch, self.tokenizer,
                    replay_provider(self.tokenizer), settings=self.settings)
                after = commit_continuation_round(second).committed
                for p, peer in enumerate(after.peers):
                    self.assertEqual(peer.history[:len(before[p])], before[p])
                    added = peer.history[len(before[p]):]
                    self.assertIs(type(added[0]), OwnReply)
                    prose = [(e.slot.round_number, e.sender) for e in added if type(e) is ReceivedProse]
                    self.assertEqual(prose, sorted(prose))
                self.assertFalse(after.pending)
                released = [d for d in after.deliveries if d.delivery_id in {d.delivery_id for d in held}]
                self.assertEqual(len(released), len(held))
                self.assertTrue(all(d.first_usable == Slot("recovery", 3) for d in released))
                self.assertEqual(held_prose_counts(deserialize_state(snapshot_bytes(after))), counts)
                self.assertEqual(drain_deliveries(after, tuple(d.delivery_id for d in released) * 2), after)
                with self.assertRaises(ValueError):
                    held_prose_counts(stage_effects(second.barrier))

    def test_mixed_effects_assemble_branch_locally_with_duplicate_attempt_metadata(self):
        for _, _, records in self.cases:
            for saved in records.values():
                if saved.branch.policy not in ("P_G", "P_H"):
                    continue
                state = commit_continuation_round(saved).committed
                messages = sorted((m for r in saved.barrier.replies for m in r.messages), key=lambda m: (m.sender, m.recipient))
                self.assertEqual(saved.barrier.messages, tuple(messages))
                for p, peer in enumerate(state.peers):
                    self.assertEqual([e.text for e in peer.history if type(e) is ReceivedProse and e.slot == Slot("recovery", 1)],
                                     [m.text for m in messages if m.recipient == p and m.text is not None])
                effects = peer_deliveries(state)
                self.assertEqual(len(effects), sum(len(m.sources) + (m.text is not None) for m in messages))
                self.assertTrue(all(d.delivery_id.startswith(state.branch_id + "/") for d in effects))
                self.assertTrue(all(d.first_usable == Slot("recovery", 2) for d in effects))
                for message in messages:
                    attempts = [d for d in effects if d.sender == message.sender and d.recipient == message.recipient and d.source is not None]
                    if len(attempts) == 2 and attempts[0].source == attempts[1].source:
                        self.assertNotEqual(attempts[0].delivery_id, attempts[1].delivery_id)
                        self.assertFalse(attempts[1].acquired)
                self.assertEqual(commit_continuation_round(saved).committed, state)

    def test_replay_mismatches_missing_parents_and_corrupt_outcomes_fail_before_effects(self):
        world, prefix, records = next(c for c in self.cases if c[0].world.task is Task.SORT)
        parent = records[scheduled(world, "revision", "B").branch_id]
        branch = scheduled(world, "revision", "Q_B")
        state = start_continuation(prefix.snapshot, world, branch)
        before = snapshot_bytes(state)
        def forbidden(*args, **kwargs):
            self.fail("required replay cannot generate")
        request = parent.barrier.requests
        altered = [replace(parent, settings_json=parent.settings_json + " ")]
        for name, first in (("views", replace(request.views[0], history=())),
                            ("rendered", replace(request.rendered[0], content=request.rendered[0].content + " ")),
                            ("tokenized", replace(request.tokenized[0], input_ids=request.tokenized[0].input_ids + (1,)))):
            altered.append(replace(parent, barrier=replace(parent.barrier, requests=replace(request,
                **{name: (first,) + getattr(request, name)[1:]}))))
        altered.append(replace(parent, branch=replace(parent.branch, calls=(replace(parent.branch.calls[0], seed=parent.calls[0].seed + 1),) + parent.branch.calls[1:])))
        altered.append(replace(parent, barrier=replace(parent.barrier, replies=(replace(parent.barrier.replies[0], prose_tokens=999),) + parent.barrier.replies[1:])))
        for parents in ((), (parent, parent), *((p,) for p in altered)):
            with self.assertRaises(ValueError):
                obtain_continuation_round(state, branch, self.tokenizer, forbidden, settings=self.settings, parents=parents)
        thesis = candidate_settings(self.tokenizer, QWEN_4B)
        mismatch = json.loads(json.dumps(self.settings))
        mismatch["generation"]["max_new_tokens"] = 384
        for settings in (thesis, mismatch):
            with self.assertRaises(ValueError):
                obtain_continuation_round(state, branch, self.tokenizer, forbidden, settings=settings, parents=(parent,))
        others = [records[scheduled(world, "sham", "B").branch_id],
                  records[scheduled(world, "revision", "B", 1).branch_id],
                  records[scheduled(world, "revision", "C").branch_id]]
        other_world, _, other_records = next(c for c in self.cases if c[0].development and c[0].world.task is Task.SORT)
        others.append(other_records[scheduled(other_world, "revision", "B").branch_id])
        for other in others:
            changed = replace(branch, calls=tuple(replace(c, replay_parent=other.calls[c.peer].call_id) if c.round_number == 1 else c for c in branch.calls))
            with self.assertRaises(ValueError):
                obtain_continuation_round(state, changed, self.tokenizer, forbidden, settings=self.settings, parents=(other,))
        self.assertEqual(snapshot_bytes(state), before)

    def test_invalid_failed_parent_absence_is_literal_and_whole_reply_failure_has_no_effects(self):
        world, prefix, records = next(c for c in self.cases if c[0].world.task is Task.SORT)
        for saved in records.values():
            if saved.branch.policy in ("P_G", "P_H", "Q_B", "Q_C"):
                self.assertEqual([r.candidate.status for r in saved.barrier.replies], ["valid", "valid", "invalid", "failed"])
                self.assertEqual(saved.barrier.replies[2].generated.text, "invalid first reply with private prose")
                self.assertIsNone(saved.barrier.replies[3].generated)
                self.assertTrue(all(r.candidate.value is None and not r.messages for r in saved.barrier.replies[2:]))
        b, q = (scheduled(world, "revision", p) for p in ("B", "Q_B"))
        for mode in ("invalid", "failed", "unicode", "stale", "empty"):
            def provide(view, *args, **kwargs):
                if mode == "failed":
                    return None
                if mode == "invalid":
                    return raw_reply(self.tokenizer, "")
                sends = [{"to": (view.peer + 1) % 4, "source_refs": [reference(view.sources[0])], "text": ""}]
                if mode == "unicode":
                    sends.append({"to": (view.peer + 2) % 4, "text": "\ud800"})
                elif mode == "stale":
                    sends[0]["source_refs"] = [{"record_id": view.notice.source.record_id, "version": 1}]
                return reply(self.tokenizer, view, sends)
            parent = obtain_continuation_round(start_continuation(prefix.snapshot, world, b), b, self.tokenizer,
                provide, settings=self.settings)
            saved = obtain_continuation_round(start_continuation(prefix.snapshot, world, q), q, self.tokenizer,
                settings=self.settings, parents=(parent,))
            self.assertEqual(saved.barrier.replies, parent.barrier.replies)
            state = commit_continuation_round(saved).committed
            self.assertEqual(held_prose_counts(state), (0,) * 4)
            if mode != "empty":
                self.assertFalse(state.pending)
                self.assertFalse(peer_deliveries(state))
                self.assertTrue(all(p.candidate.value is None for p in state.peers))
            else:
                self.assertEqual(len(state.pending), 4)
                second = obtain_continuation_round(state, q, self.tokenizer, provide, settings=self.settings)
                released = commit_continuation_round(second).committed
                self.assertFalse(released.pending)
                self.assertEqual(held_prose_counts(released), (0,) * 4)

    def test_prefix_parent_raw_replies_and_siblings_are_deeply_independent(self):
        for world, prefix, records in self.cases:
            policy = "P_G" if any(b.policy == "P_G" for b in branches(world)) else "K"
            branch = scheduled(world, "revision", policy)
            parents = tuple(records[scheduled(world, "revision", p).branch_id] for p in ("B", "C"))
            original = tuple(asdict(p) for p in parents)
            siblings = [obtain_continuation_round(start_continuation(prefix.snapshot, world, branch), branch,
                self.tokenizer, replay_provider(self.tokenizer), settings=self.settings, parents=parents) for _ in range(2)]
            frozen = asdict(siblings[1])
            state = commit_continuation_round(siblings[0]).committed
            object.__setattr__(state.peers[0].sources[0], "value", 123456789)
            object.__setattr__(siblings[0].barrier.replies[0].generated, "text", "nested mutation")
            object.__setattr__(siblings[0].barrier.requests.before.peers[0].notice.source, "owner", 99)
            self.assertEqual(asdict(siblings[1]), frozen)
            self.assertEqual(tuple(asdict(p) for p in parents), original)
            self.assertEqual(snapshot_bytes(deserialize_state(prefix.snapshot)), prefix.snapshot)

    def test_reversed_invocation_is_synchronous_and_never_uses_offline_truth(self):
        for world, prefix, records in self.cases:
            with patch("recovery.truth.solve_world", side_effect=AssertionError("offline truth")):
                reverse = prefix_case(world, self.tokenizer, invocation_order=reversed(PEERS))
                self.assertEqual(prefix, reverse)
                reversed_records = first_rounds(world, reverse, self.tokenizer, invocation_order=reversed(PEERS))
                self.assertEqual(records, reversed_records)
                branch = scheduled(world, "revision", "B")
                state = commit_continuation_round(records[branch.branch_id]).committed
                normal = obtain_continuation_round(state, branch, self.tokenizer, replay_provider(self.tokenizer), settings=self.settings)
                reversed_round = obtain_continuation_round(state, branch, self.tokenizer, replay_provider(self.tokenizer),
                    settings=self.settings, invocation_order=reversed(PEERS))
                self.assertEqual(normal, reversed_round)
                self.assertEqual(commit_continuation_round(normal), commit_continuation_round(reversed_round))

    def test_pending_hidden_fields_tombstones_and_cpu_third_version_preserve_authority(self):
        for task in (Task.PREFIX, Task.BFS):
            first = next(c[0] for c in self.cases if c[0].world.task is task)
            key = first.main_edit.record_id
            old = next(s for s in first.world.records if s.record_id == key)
            other = next(s for s in first.world.records if s.owner == old.owner and s.value != old.value
                         and (task is Task.BFS or s.value != first.main_edit.replacement))
            changed = tuple(replace(s, value=other.value if s == old else old.value) if s in (old, other) else s for s in first.world.records)
            second = replace(first, world=replace(first.world, records=changed))
            states = []
            for world in (first, second):
                prefix = prefix_case(world, self.tokenizer, quiet=True)
                states.append(start_continuation(prefix.snapshot, world, scheduled(world, "revision", "L")))
            for p in PEERS:
                if p != old.owner:
                    self.assertEqual(self.rendered(views(states[0])[p]), self.rendered(views(states[1])[p]))
                    pending = next(s for s in views(states[0])[p].sources if s.record_id == key)
                    self.assertEqual(asdict(pending), dict(record_id=key, owner=old.owner, position=old.position, version=2))
            local = states[0]
            if first.preserving_edit is not None:
                altered = replace(first, preserving_edit=first.main_edit)
                original_prefix = prefix_case(first, self.tokenizer, quiet=True)
                self.assertEqual(start_continuation(original_prefix.snapshot, first, scheduled(first, "revision", "B")),
                    start_continuation(original_prefix.snapshot, altered, scheduled(altered, "revision", "B")))
            owner, receiver = old.owner, (old.owner + 1) % 4
            def forward(view, *_):
                return reply(self.tokenizer, view, [{"to": receiver, "source_refs": [{"record_id": key, "version": 2}]}] if view.peer == owner else [])
            delivered = run_round(local, self.tokenizer, forward, limits=COURSE_LIMITS).committed
            current = held_source(views(delivered)[receiver], key, 2)
            self.assertIsNotNone(current)
            if task is Task.BFS:
                self.assertTrue(current.deleted)
                self.assertEqual(current.value, old.value)
            for view in (views(local)[owner], views(local)[receiver]):
                third_notice = RevisionNotice(view.notice.source, 2, 3)
                for content in (None, replace(current, version=3)):
                    new = revise_source(replace(view, slot=Slot("recovery", 2)), third_notice, content)
                    self.assertEqual((new.history, new.candidate, new.feedback), (view.history, view.candidate, view.feedback))
                    self.assertIsNone(held_source(new, key, 1))
                    self.assertIsNone(held_source(new, key, 2))
                    self.assertEqual(held_source(new, key, 3), content)
                    with self.assertRaises(ValueError):
                        revise_source(new, view.notice, current)

    def test_held_text_only_payload_or_omission_cannot_change_recipient_request(self):
        world, prefix, _ = next(c for c in self.cases if c[0].world.task is Task.SORT)
        b, q = (scheduled(world, "revision", p) for p in ("C", "Q_C"))
        requests = []
        for text in ("SECRET_ALPHA", "SECRET_BETA", None):
            parent = obtain_continuation_round(start_continuation(prefix.snapshot, world, b), b, self.tokenizer,
                lambda v, *a, **k: reply(self.tokenizer, v, [{"to": 2, "text": text}] if v.peer == 0 and text is not None else []),
                settings=self.settings)
            saved = obtain_continuation_round(start_continuation(prefix.snapshot, world, q), q, self.tokenizer,
                settings=self.settings, parents=(parent,))
            state = commit_continuation_round(saved).committed
            requests.append(prepare_round(state, self.tokenizer, limits=COURSE_LIMITS))
        for name in ("views", "rendered", "tokenized"):
            self.assertEqual([getattr(r, name)[2] for r in requests], [getattr(requests[0], name)[2]] * 3)
        self.assertNotEqual(requests[0].rendered[0], requests[1].rendered[0])


if __name__ == "__main__":
    unittest.main()
