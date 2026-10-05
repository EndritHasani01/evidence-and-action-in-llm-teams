"""CPU event/retention differentials through real prefix, reply and view code.

The injected tokenizer is a test counter, not native capacity admission.
"""

from dataclasses import asdict, replace
from functools import cache
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from recovery.events import start_continuation
from recovery.manifests import load_population
from recovery.prompts import render_request, rendered_data
from recovery.protocol import validate_reply
from recovery.rounds import (deserialize_state, fork_prefix, initial_branch,
                             run_prefix, run_round, snapshot_bytes)
from recovery.schedule import _prepare_branches
from recovery.state import (CandidateState, ContinueNotice, OwnReply,
                            PendingSource, RevisionNotice, Slot, held_source, revise_source)
from recovery.tasks import PEERS, Size, SourceRecord, Task
from tests.protocol_checks import placeholder, reference
from tests.round_checks import TOKENIZER, raw_reply, reply

ROOT = Path(__file__).resolve().parent.parent


@cache
def population(size):
    return load_population(ROOT / f"tests/fixtures/population_{size.value}.json")


def case_world(task=Task.PREFIX, size=Size.TARGET):
    return next(w for w in population(size).main if w.world.task is task and w.index == 1)


def event_provider(tokenizer):
    def provide(view, rendered, tokenized):
        p, r = view.peer, view.slot.round_number
        own = [s for s in view.sources if s.owner == p and type(s) is SourceRecord]
        if view.slot.phase == "prefix":
            if r == 2 and p == 3:
                return raw_reply(tokenizer, "invalid earlier reply")
            if r == 4 and p == 1:
                return reply(tokenizer, view, [{"to": p}], candidate=placeholder(view))
            if r == 4 and p == 2:
                return None
            texts = {1: f"old raw values {[s.value for s in own]}",
                     2: "retained intermediate work",
                     3: "EARLIER_RICH_RESULT must never replace the fourth-slot outcome",
                     4: "final prefix prose"}
            return reply(tokenizer, view, [{"to": (p + 1) % 4,
                "source_refs": [reference(s) for s in own] if r in (1, 4) else [],
                "text": texts[r]}])
        return reply(tokenizer, view, [{"to": (p + 1) % 4,
            "source_refs": [reference(own[0])], "text": f"new work at recovery {r}"}])
    return provide


def build_prefix(world, tokenizer=TOKENIZER):
    branches = _prepare_branches((world,))
    prefix = next(b for b in branches if b.phase == "prefix")
    return run_prefix(world.world, prefix.branch_id, tokenizer, event_provider(tokenizer))


def scheduled(world, event, policy, replicate=0):
    return next(b for b in _prepare_branches((world,))
                if (b.phase, b.event, b.policy, b.replicate)
                == ("continuation", event, policy, replicate))


def start(world, prefix, policy, event="revision", replicate=0):
    return start_continuation(prefix.snapshot, world, scheduled(world, event, policy, replicate))


def views(state):
    return tuple(p.view(state.task, state.size, i, state.next_slot, state.manifest)
                 for i, p in enumerate(state.peers))


def data(view):
    return rendered_data(render_request(view))


class EventBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = [(w, build_prefix(w)) for size in Size for task in Task
                     for w in (case_world(task, size),)]

    def test_all_scheduled_events_subsets_and_repeats_start_from_original(self):
        # Includes both complete populations, development, late indices without
        # preserving/repeat arms, every selected owner/partition and Q starts.
        for size in Size:
            pop = population(size)
            for world in pop.main + pop.development:
                prefix = build_prefix(world)
                original = deserialize_state(prefix.snapshot)
                for branch in _prepare_branches((world,)):
                    if branch.phase != "continuation":
                        continue
                    state = start_continuation(prefix.snapshot, world, branch)
                    self.assertEqual(state.prefix_parent, original.branch_id)
                    self.assertEqual(state.branch_id, branch.branch_id)
                    self.assertEqual(state.last_slot, Slot("prefix", 4))
                    self.assertEqual(state.next_slot, Slot("recovery", 1))
                    self.assertTrue(state.boundary_applied)
                    self.assertFalse(state.pending)
                    self.assertEqual(state.deliveries[:len(original.deliveries)], original.deliveries)
                    expected = {s.record_id: s for s in world.event_world(branch.event).records}
                    for view in views(state):
                        for source in view.sources:
                            if type(source) is SourceRecord:
                                self.assertEqual(source, expected[source.record_id])
                            else:
                                self.assertEqual(source.version, 2)
                    if branch.replicate:
                        first = start(world, prefix, branch.policy, branch.event)
                        self.assertEqual(first.peers, state.peers)
                self.assertEqual(snapshot_bytes(original), prefix.snapshot)

    def test_local_broadcast_differ_only_in_replacement_content_and_its_delivery(self):
        for world, prefix in self.cases:
            local, broadcast = (start(world, prefix, p) for p in ("L", "B"))
            key = world.main_edit.record_id
            for p, (left, right) in enumerate(zip(views(local), views(broadcast))):
                self.assertEqual(left.notice, right.notice)
                self.assertEqual(left.receipt, right.receipt)
                a, b = data(left), data(right)
                a["current_sources"] = [s for s in a["current_sources"] if s["record_id"] != key]
                b["current_sources"] = [s for s in b["current_sources"] if s["record_id"] != key]
                a["source_deliveries"] = [d for d in a["source_deliveries"] if d["record_id"] != key]
                b["source_deliveries"] = [d for d in b["source_deliveries"] if d["record_id"] != key]
                self.assertEqual(a, b)
                self.assertIsNone(held_source(left, key, 1))
                self.assertIsNone(held_source(right, key, 1))
                self.assertIsNotNone(held_source(right, key, 2))
                if p == world.edited_owner:
                    self.assertEqual(left, right)
                else:
                    self.assertIsNone(held_source(left, key, 2))
                    pending = next(s for s in left.sources if s.record_id == key)
                    self.assertIs(type(pending), PendingSource)
                    self.assertFalse(hasattr(pending, "value"))
            for state, count in ((local, 1), (broadcast, 4)):
                added = state.deliveries[len(deserialize_state(prefix.snapshot).deliveries):]
                self.assertEqual(len(added), count)
                self.assertTrue(all(d.origin == "host" and d.acquired and d.source.version == 2
                                    and d.first_usable == Slot("recovery", 1) for d in added))

    def test_b_c_k_masks_have_identical_evidence_and_literal_retention(self):
        for world, prefix in self.cases:
            original = deserialize_state(prefix.snapshot)
            for event in ("revision", "sham"):
                starts = {p: start(world, prefix, p, event) for p in ("B", "C", "K", "P_G", "P_H")}
                for i in PEERS:
                    b, c, k = (starts[p].peers[i] for p in ("B", "C", "K"))
                    old = original.peers[i]
                    self.assertEqual(b.history, old.history)
                    self.assertEqual(b.candidate, old.candidate)
                    self.assertEqual(b.feedback, old.feedback)
                    self.assertEqual((c.history, c.feedback, c.candidate), ((), (), CandidateState()))
                    self.assertEqual((k.history, k.feedback), ((), ()))
                    self.assertEqual(k.candidate, replace(old.candidate, historical=True))
                    for policy, state in starts.items():
                        peer = state.peers[i]
                        self.assertEqual((peer.sources, peer.source_deliveries, peer.notice, peer.receipt),
                                         (b.sources, b.source_deliveries, b.notice, b.receipt))
                        if policy in ("P_G", "P_H"):
                            group = world.partition[0 if policy == "P_G" else 1]
                            self.assertEqual(peer, c if i in group else b)
                            self.assertEqual(render_request(views(state)[i]),
                                render_request(views(starts["C" if i in group else "B"])[i]))

    def test_k_keeps_wrong_fourth_result_or_invalid_failed_absence_without_backfill(self):
        for world, prefix in self.cases:
            for policy in (("K", "K_delta") if world.world.task in (Task.PREFIX, Task.SORT) else ("K",)):
                compact = start(world, prefix, policy)
                for p, view in enumerate(views(compact)):
                    expected = ("valid", "invalid", "failed", "valid")[p]
                    self.assertEqual(view.candidate.status, expected)
                    self.assertTrue(view.candidate.historical)
                    shown = data(view)["latest_candidate"]
                    self.assertEqual(shown["candidate"], placeholder(view) if expected == "valid" else None)
                    self.assertNotIn("EARLIER_RICH_RESULT", render_request(view).content)
                    self.assertEqual(shown["slot"], {"phase": "prefix", "round": 4})

    def test_c_f_differ_only_by_acquired_remote_sources_and_corresponding_metadata(self):
        for world, prefix in self.cases:
            c, f = (start(world, prefix, p) for p in ("C", "F"))
            changed = world.main_edit.record_id
            for p, (left, right) in enumerate(zip(views(c), views(f))):
                expected = tuple(s for s in left.sources if s.owner == p or s.record_id == changed)
                self.assertEqual(right.sources, expected)
                self.assertTrue(all(s in right.sources for s in world.event_world("revision").records if s.owner == p))
                self.assertIsNotNone(held_source(right, changed, 2))
                a, b = data(left), data(right)
                for name in ("current_sources", "source_deliveries"):
                    del a[name], b[name]
                self.assertEqual(a, b)
            self.assertTrue(any(len(a.sources) > len(b.sources) for a, b in zip(c.peers, f.peers)))

    def test_sham_keeps_all_raw_sources_and_neutral_notice_without_receipt(self):
        for world, prefix in self.cases:
            original = deserialize_state(prefix.snapshot)
            for policy in ("B", "C", "K", "P_G", "P_H"):
                sham = start(world, prefix, policy, "sham")
                self.assertEqual(sham.deliveries, original.deliveries)
                for old, new in zip(original.peers, sham.peers):
                    self.assertEqual(old.sources, new.sources)
                    self.assertEqual(old.source_deliveries, new.source_deliveries)
                    self.assertEqual(new.notice, ContinueNotice())
                    self.assertIsNone(new.receipt)

    def test_preserving_is_separate_original_sibling_and_does_not_change_candidates(self):
        for world, prefix in self.cases:
            if world.world.task not in (Task.TOP_K, Task.BFS):
                continue
            main = start(world, prefix, "B")
            for policy in ("B", "C", "K"):
                preserve = start(world, prefix, policy, "preserving")
                self.assertEqual(preserve.peers[0].notice.source.record_id, world.preserving_edit.record_id)
                original = deserialize_state(prefix.snapshot)
                if policy == "B":
                    self.assertEqual(tuple(p.candidate for p in preserve.peers),
                                     tuple(p.candidate for p in original.peers))
                self.assertEqual(sum(s.version == 2 for s in world.event_world("preserving").records), 1)
                self.assertEqual(main, start(world, prefix, "B"))
                self.assertEqual(preserve, start(world, prefix, policy, "preserving"))

    def test_receipts_only_disclose_archived_before_field_and_never_forward_it(self):
        for world, prefix in self.cases:
            if world.world.task not in (Task.PREFIX, Task.SORT):
                continue
            key = world.main_edit.record_id
            old = next(s for s in world.world.records if s.record_id == key)
            for policy in ("B", "C", "K"):
                ordinary, disclosed = (start(world, prefix, p) for p in (policy, policy + "_delta"))
                for a, b in zip(views(ordinary), views(disclosed)):
                    left, right = data(a), data(b)
                    self.assertEqual(left["historical_receipt"]["before_value"], "not included in this receipt")
                    self.assertEqual(right["historical_receipt"], {"record_id": key, "owner": old.owner,
                        "position": old.position, "previous_version": 1, "new_version": 2, "before_value": old.value})
                    left["historical_receipt"]["before_value"] = old.value
                    self.assertEqual(left, right)
                    self.assertIsNone(held_source(b, key, 1))
                    self.assertEqual(held_source(a, key, 2), held_source(b, key, 2))
                    invalid = validate_reply(b, reply(TOKENIZER, b, [{"to": (b.peer + 1) % 4,
                        "source_refs": [{"record_id": key, "version": 1}]}]), TOKENIZER)
                    self.assertFalse(invalid.protocol_valid)
                    self.assertFalse(invalid.messages)

    def test_old_values_in_actual_prose_survive_but_raw_archive_never_enters_history(self):
        world, prefix = self.cases[0]
        old = deserialize_state(prefix.snapshot)
        # Every sender forwarded a literal old raw value; retain it as prose.
        for policy in ("B", "L"):
            state = start(world, prefix, policy)
            for p in PEERS:
                self.assertEqual(state.peers[p].history, old.peers[p].history)
                self.assertIn("old raw", render_request(views(state)[p]).content)
                self.assertTrue(all(set(entry) <= {"kind", "slot", "text", "sender"}
                                    for entry in data(views(state)[p])["history"]))
        for policy in ("C", "K", "F"):
            self.assertTrue(all(not p.history for p in start(world, prefix, policy).peers))

    def test_bfs_pending_hides_endpoints_until_exact_tombstone_delivery(self):
        world = case_world(Task.BFS)
        # No prefix sends: the nonowner has never seen the deleted endpoints.
        prefix_id = scheduled(world, "revision", "L").prefix_parent
        prefix = run_prefix(world.world, prefix_id, TOKENIZER, lambda v, r, t: reply(TOKENIZER, v))
        local = start(world, prefix, "L")
        key = world.main_edit.record_id
        owner = world.edited_owner
        receiver = (owner + 1) % 4
        shown = data(views(local)[receiver])
        pending = next(s for s in shown["current_sources"] if s["record_id"] == key)
        self.assertEqual(set(pending), {"record_id", "owner", "version", "status"})
        self.assertNotIn("endpoints", shown["persistent_notice"])
        def forward(view, rendered, tokenized):
            return reply(TOKENIZER, view, [{"to": receiver, "source_refs": [{"record_id": key, "version": 2}]}]
                         if view.peer == owner else [])
        result = run_round(local, TOKENIZER, forward)
        acquired = held_source(views(result.committed)[receiver], key, 2)
        self.assertTrue(acquired.deleted)
        self.assertEqual(acquired.value, next(s.value for s in world.world.records if s.record_id == key))
        self.assertEqual(result.committed.peers[receiver].candidate, result.barrier.replies[receiver].candidate)

    def test_all_policies_accumulate_new_history_and_notices_receipts_survive(self):
        for world, prefix in self.cases:
            for branch in _prepare_branches((world,)):
                if (branch.phase != "continuation" or branch.replicate
                        or branch.policy in ("P_G", "P_H", "Q_B", "Q_C")):
                    continue  # First-round mixed/Q reuse belongs to T05.
                state = start_continuation(prefix.snapshot, world, branch)
                persistent = tuple((p.notice, p.receipt) for p in state.peers)
                before_history = tuple(p.history for p in state.peers)
                for r in range(1, 5):
                    result = run_round(state, TOKENIZER, event_provider(TOKENIZER))
                    state = result.committed
                    self.assertEqual(tuple((p.notice, p.receipt) for p in state.peers), persistent)
                    for i, p in enumerate(state.peers):
                        self.assertEqual(p.history[:len(before_history[i])], before_history[i])
                        self.assertEqual(sum(type(e) is OwnReply and e.slot.phase == "recovery" for e in p.history), r)
                        self.assertFalse(p.candidate.historical)
                        self.assertEqual(p.candidate.slot, Slot("recovery", r))
                self.assertIsNone(state.next_slot)
                self.assertFalse(state.pending)
                self.assertTrue(state.boundary_applied)

    def test_boundary_marker_roundtrips_and_reapplication_or_nonoriginal_input_is_rejected(self):
        world, prefix = self.cases[0]
        branch = scheduled(world, "revision", "B")
        fork = fork_prefix(prefix.snapshot, branch.branch_id)
        self.assertFalse(fork.boundary_applied)
        state = start_continuation(prefix.snapshot, world, branch)
        loaded = deserialize_state(snapshot_bytes(state))
        self.assertEqual(state, loaded)
        self.assertTrue(loaded.boundary_applied)
        for payload in (snapshot_bytes(state), snapshot_bytes(fork),
                        snapshot_bytes(initial_branch(world.world, branch.prefix_parent))):
            with self.assertRaises(ValueError):
                start_continuation(payload, world, branch)
        original = deserialize_state(prefix.snapshot)
        for peer in (replace(original.peers[0], candidate=CandidateState("failed", Slot("prefix", 3))),
                     replace(original.peers[0], sources=()),
                     replace(original.peers[0], notice=ContinueNotice())):
            with self.assertRaises(ValueError):
                start_continuation(snapshot_bytes(replace(original, peers=(peer,) + original.peers[1:])), world, branch)

    def test_compact_historical_result_survives_new_valid_invalid_and_failed_slots_exactly_once(self):
        for world, prefix in self.cases:
            state = start(world, prefix, "K")
            retained = tuple(p.candidate for p in state.peers)
            for r in range(1, 5):
                def provide(view, rendered, tokenized):
                    if view.peer == 1:
                        return raw_reply(TOKENIZER, "invalid current reply")
                    if view.peer == 2:
                        return None
                    candidate = placeholder(view)
                    if type(candidate) is list:
                        candidate = [-555] * len(candidate)
                    else:
                        candidate = {k: -555 for k in candidate}
                    return reply(TOKENIZER, view, candidate=candidate)
                state = run_round(state, TOKENIZER, provide).committed
                self.assertEqual(deserialize_state(snapshot_bytes(state)), state)
                for p, peer in enumerate(state.peers):
                    self.assertEqual([e for e in peer.history if type(e) is CandidateState], [retained[p]])
                    self.assertEqual(peer.candidate.slot, Slot("recovery", r))
                    self.assertFalse(peer.candidate.historical)
                    self.assertEqual(peer.candidate.status, ("valid", "invalid", "failed", "valid")[p])
                    if r < 4:
                        shown = data(views(state)[p])
                        history = [e for e in shown["history"] if e["kind"] == "historical_candidate"]
                        self.assertEqual(len(history), 1)
                        self.assertEqual(history[0]["candidate"], retained[p].payload(world.world.task))
                        self.assertTrue(history[0]["historical"])
                        if p in (1, 2):
                            self.assertIsNone(shown["latest_candidate"]["candidate"])
            # Reject a duplicated result or a host-invented nonhistorical entry.
            view = replace(views(start(world, prefix, "K"))[0], slot=Slot("recovery", 2),
                           candidate=CandidateState("failed", Slot("recovery", 1)))
            for history in ((retained[0], retained[0]), (replace(retained[0], historical=False),),
                            (retained[0], OwnReply(Slot("prefix", 4), "invented full reply"))):
                with self.assertRaises(ValueError):
                    replace(view, history=history)

    def test_boundary_never_calls_gold_or_eligibility_evaluators(self):
        world, prefix = self.cases[0]
        with patch("recovery.truth.solve_world", side_effect=AssertionError("offline truth")), \
                patch("recovery.edits.bfs_distances", side_effect=AssertionError("offline BFS")), \
                patch("recovery.populations.legal_edits", side_effect=AssertionError("eligibility")):
            state = start(world, prefix, "K")
            self.assertTrue(state.boundary_applied)

    def test_invalid_schedule_parent_world_or_undeclared_arm_fails_without_mutation(self):
        world, prefix = self.cases[0]
        branch = scheduled(world, "revision", "B")
        for invalid in (replace(branch, world_id="other"), replace(branch, phase="control"),
                        replace(branch, prefix_parent="other"), replace(branch, replicate=99),
                        replace(branch, event="sham", policy="F"), replace(branch, event="preserving"),
                        replace(branch, policy="invented")):
            with self.assertRaises(ValueError):
                start_continuation(prefix.snapshot, world, invalid)
        other = next(w for w in population(world.world.size).main
                     if w.world.task is world.world.task and w.index == 2)
        wrong_id = replace(deserialize_state(prefix.snapshot), branch_id=scheduled(other, "revision", "B").prefix_parent)
        with self.assertRaisesRegex(ValueError, "original"):
            start_continuation(snapshot_bytes(wrong_id), other, scheduled(other, "revision", "B"))
        graph = case_world(Task.BFS)
        prefix = build_prefix(graph)
        self.assertEqual(views(start(graph, prefix, "Q_B")), views(start(graph, prefix, "B")))

    def test_unexposed_hidden_before_values_endpoints_and_future_edit_cannot_change_local_requests(self):
        for task in (Task.PREFIX, Task.BFS):
            first = case_world(task)
            key = first.main_edit.record_id
            a = next(s for s in first.world.records if s.record_id == key)
            b = next(s for s in first.world.records if s.owner == a.owner and s.value != a.value
                     and (task is Task.BFS or s.value != first.main_edit.replacement))
            # Swap payloads inside the hidden owner's shard, preserving public
            # identities and the exact replacement notice. No prefix traffic.
            records = tuple(replace(s, value=b.value if s == a else a.value) if s in (a, b) else s
                            for s in first.world.records)
            second = replace(first, world=replace(first.world, records=records))
            results = []
            for world in (first, second):
                branch = scheduled(world, "revision", "L")
                prefix = run_prefix(world.world, branch.prefix_parent, TOKENIZER,
                                    lambda v, r, t: reply(TOKENIZER, v))
                state = start_continuation(prefix.snapshot, world, branch)
                results.append(state)
            for p in PEERS:
                if p != a.owner:
                    self.assertEqual(render_request(views(results[0])[p]), render_request(views(results[1])[p]))
            # An unused future preserving edit never enters main/sham prompts.
            if first.preserving_edit is not None:
                altered = replace(first, preserving_edit=first.main_edit)
                prefix = build_prefix(first)
                self.assertEqual(views(start(first, prefix, "B")), views(start(altered, prefix, "B")))

    def test_nested_mutations_cannot_change_original_or_siblings_or_saved_world(self):
        for world, prefix in self.cases:
            siblings = [start(world, prefix, "B"), start(world, prefix, "C"), start(world, prefix, "K")]
            archived = [snapshot_bytes(s) for s in siblings]
            original = asdict(world)
            victim = siblings[0]
            key = world.main_edit.record_id
            source = next(s for s in victim.peers[0].sources if s.record_id == key)
            object.__setattr__(source, "value", -123456789)
            object.__setattr__(victim.peers[0].history[0], "text", "nested mutation")
            object.__setattr__(victim.peers[0].candidate, "status", "failed")
            object.__setattr__(victim.peers[0].notice.source, "owner", 99)
            object.__setattr__(victim.deliveries[0].source, "value", -987654321)
            self.assertEqual([snapshot_bytes(s) for s in siblings[1:]], archived[1:])
            self.assertEqual(asdict(world), original)
            self.assertEqual(snapshot_bytes(start(world, prefix, "B")), archived[0])
            self.assertEqual(snapshot_bytes(deserialize_state(prefix.snapshot)), prefix.snapshot)

    def test_cpu_v1_v2_v3_authority_invalidation_preserves_derived_work(self):
        for task in (Task.PREFIX, Task.BFS):
            world = case_world(task)
            prefix = build_prefix(world)
            local = start(world, prefix, "L")
            key = world.main_edit.record_id
            owner = world.edited_owner
            known = views(local)[owner]
            pending = views(local)[(owner + 1) % 4]
            current = held_source(known, key, 2)
            notice = RevisionNotice(known.notice.source, 2, 3)
            third = replace(current, version=3)
            for old in (known, pending):
                for content in (None, third):
                    new = revise_source(replace(old, slot=Slot("recovery", 2)), notice, content)
                    self.assertEqual((new.history, new.candidate, new.feedback), (old.history, old.candidate, old.feedback))
                    self.assertIsNone(held_source(new, key, 1))
                    self.assertIsNone(held_source(new, key, 2))
                    self.assertEqual(held_source(new, key, 3), content)
                    self.assertIsNone(new.receipt)
                    with self.assertRaises(ValueError):
                        revise_source(new, old.notice, current)
                    with self.assertRaises(ValueError):
                        revise_source(new, notice, third)
            with self.assertRaises(ValueError):
                revise_source(known, notice, current)

    def test_boundary_bytes_are_hash_seed_independent_with_optional_stack_blocked(self):
        script = '''
import importlib.abc, json, random, sys
class BlockImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'torch','transformers','langgraph','langchain','numpy','pandas'}:
            raise AssertionError(fullname)
sys.meta_path.insert(0, BlockImports())
before = random.getstate()
from tests.event_checks import case_world, build_prefix, start
from recovery.rounds import snapshot_bytes
w = case_world()
p = build_prefix(w)
print(snapshot_bytes(start(w, p, 'K_delta')).decode())
assert before == random.getstate()
'''
        outputs = []
        for seed in ("1", "37", "999"):
            result = subprocess.run([sys.executable, "-c", script], cwd=ROOT,
                                    env=dict(os.environ, PYTHONHASHSEED=seed), capture_output=True,
                                    text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            outputs.append(result.stdout)
        self.assertEqual(outputs, [outputs[0]] * 3)


if __name__ == "__main__":
    unittest.main()
