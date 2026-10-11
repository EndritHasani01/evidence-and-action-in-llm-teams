"""Local course witness through saved schedules and the real protocol; CPU only."""

from dataclasses import replace
import json
import unittest

from recovery.inference import QWEN_4B, candidate_settings
from recovery.prompts import COURSE_LIMITS
from recovery.replay import commit_continuation_round, held_prose_counts
from recovery.rounds import snapshot_bytes
from recovery.state import CandidateState, OwnReply, PendingSource, ReceivedProse, Slot, initial_view
from recovery.tasks import PEERS, SourceRecord, Task
from recovery.truth import exact_candidate, solve_world
from recovery.witness import local_candidate
from tests.attainability_checks import execute_witness
from tests.course_intervention_cases import TOKENIZER, branches, course_inputs


class CourseAttainabilityTests(unittest.TestCase):
    tokenizer = TOKENIZER

    @classmethod
    def setUpClass(cls):
        cls.settings = candidate_settings(cls.tokenizer, QWEN_4B, limits=COURSE_LIMITS)
        population, _ = course_inputs()
        cls.cases = tuple((world, *execute_witness(world, cls.tokenizer,
            limits=COURSE_LIMITS, settings=cls.settings, scheduled_branches=branches(world)))
            for world in (*population.main, *population.development))

    def test_all_saved_worlds_siblings_repeats_and_controls_reach_exact_answers(self):
        seen = set()
        for world, prefix, continuations, controls in self.cases:
            self.assertEqual(len(prefix.rounds), 4)
            truth = solve_world(world.world)
            for p, outcome in enumerate(prefix.rounds[-1].barrier.replies):
                self.assertTrue(exact_candidate(truth, outcome.candidate.payload(world.world.task), p))
            seen.update(c.call_id for b in branches(world) if b.phase == "prefix" for c in b.calls)
            for branch, rounds, state in continuations:
                with self.subTest(branch=branch.branch_id):
                    self.assertEqual(len(rounds), 4)
                    self.assertIsNone(state.next_slot)
                    self.assertFalse(state.pending)
                    truth = solve_world(world.event_world(branch.event))
                    for p, outcome in enumerate(rounds[-1].barrier.replies):
                        self.assertTrue(exact_candidate(truth, outcome.candidate.payload(world.world.task), p))
                    seen.update(c.call_id for c in branch.calls)
            for branch, view, _, reply in controls:
                self.assertTrue(reply.protocol_valid)
                truth = solve_world(world.world if branch.event == "original" else world.event_world(branch.event))
                self.assertTrue(exact_candidate(truth, reply.candidate.payload(view.task)))
                self.assertFalse(reply.messages)
                seen.add(branch.calls[0].call_id)
        _, schedule = course_inputs()
        self.assertEqual(seen, {c.call_id for b in schedule.main + schedule.development for c in b.calls})
        self.assertEqual(len(seen), 7458)

    def test_every_send_is_legal_current_own_shard_and_visits_each_other_peer(self):
        for _, prefix, continuations, controls in self.cases:
            barriers = [r.barrier for r in prefix.rounds]
            barriers += [r.barrier for _, rounds, _ in continuations for r in rounds]
            for barrier in barriers:
                number = barrier.requests.slot.round_number
                for p, outcome in enumerate(barrier.replies):
                    view = barrier.requests.views[p]
                    self.assertTrue(outcome.protocol_valid)
                    self.assertLessEqual(outcome.output_tokens, COURSE_LIMITS.output_tokens)
                    self.assertLessEqual(outcome.prose_tokens, COURSE_LIMITS.prose_tokens)
                    own = tuple(s for s in view.sources if type(s) is SourceRecord and s.owner == p)
                    if number == 4:
                        self.assertFalse(outcome.messages)
                        self.assertIsNotNone(local_candidate(view))
                    else:
                        message, = outcome.messages
                        self.assertEqual(message.recipient, (p + number) % 4)
                        self.assertEqual(message.sources, own)
                        self.assertLessEqual(len(own), COURSE_LIMITS.distinct_references)
            for _, _, _, outcome in controls:
                self.assertLessEqual(outcome.output_tokens, COURSE_LIMITS.output_tokens)

    def test_solver_uses_only_current_acquired_records_and_ignores_derived_or_receipt_text(self):
        for world, prefix, continuations, _ in self.cases:
            barriers = [r.barrier for r in prefix.rounds]
            barriers += [r.barrier for _, rounds, _ in continuations for r in rounds]
            for barrier in barriers:
                for p, view in enumerate(barrier.requests.views):
                    result = local_candidate(view)
                    # These strings can neither resolve missing evidence nor repair an answer.
                    irrelevant = replace(view, slot=Slot("recovery", 4),
                        history=(OwnReply(Slot("prefix", 1), "invented gold 987654321"),),
                        candidate=CandidateState("invalid", Slot("prefix", 1)), feedback=(), receipt=None)
                    self.assertEqual(local_candidate(irrelevant), result)
                    if result is not None:
                        payload = json.loads(barrier.replies[p].generated.text)["candidate"]
                        self.assertEqual(result, payload)
                        missing = replace(view, sources=view.sources[:-1], source_deliveries=(), notice=None, receipt=None)
                        self.assertIsNone(local_candidate(missing))
                        source = view.sources[-1]
                        pending = PendingSource(source.record_id, source.owner, source.position, source.version)
                        self.assertIsNone(local_candidate(replace(missing, sources=missing.sources + (pending,))))
            for p in PEERS:
                self.assertIsNone(local_candidate(initial_view(world.world, p)))

    def test_local_replacement_forwarding_and_fresh_reacquisition_finish_in_four_rounds(self):
        for world, _, continuations, _ in self.cases:
            for branch, rounds, _ in continuations:
                if branch.event != "revision" or branch.policy not in ("L", "F"):
                    continue
                owner = next(s.owner for s in world.world.records if s.record_id == world.main_edit.record_id)
                for number, saved in enumerate(rounds, 1):
                    for p, view in enumerate(saved.barrier.requests.views):
                        if branch.policy == "L":
                            self.assertEqual(local_candidate(view) is not None, (p - owner) % 4 < number)
                        else:
                            self.assertEqual(local_candidate(view) is not None, number == 4)

    def test_all_parent_joins_are_exact_and_q_releases_prose_once_without_solver_dependence(self):
        joins = 0
        for _, _, continuations, _ in self.cases:
            parents = {}
            for branch, rounds, state in continuations:
                for saved in rounds:
                    self.assertEqual(json.loads(saved.settings_json), self.settings)
                    for p, call in enumerate(saved.calls):
                        if call.replay_parent:
                            parent, i = parents[call.replay_parent]
                            current, original = saved.barrier.requests, parent.barrier.requests
                            for field in ("views", "rendered", "tokenized"):
                                self.assertEqual(getattr(current, field)[p], getattr(original, field)[i])
                            self.assertEqual(saved.settings_json, parent.settings_json)
                            self.assertEqual(call.seed, parent.calls[i].seed)
                            self.assertEqual(saved.barrier.replies[p], parent.barrier.replies[i])
                            joins += 1
                        parents[call.call_id] = saved, p
                if branch.policy in ("Q_B", "Q_C"):
                    self.assertEqual(held_prose_counts(state), (1, 1, 1, 1))
                    second = rounds[1].barrier.requests
                    first_parent, _ = parents[branch.calls[0].replay_parent]
                    ordinary = commit_continuation_round(first_parent).committed
                    for p, view in enumerate(second.views):
                        self.assertEqual(view.sources, ordinary.peers[p].sources)
                        self.assertEqual(view.source_deliveries, ordinary.peers[p].source_deliveries)
                        self.assertFalse(any(type(h) is ReceivedProse and h.slot == Slot("recovery", 1) for h in view.history))
                    for p, view in enumerate(rounds[2].barrier.requests.views):
                        incoming = [(h.slot.round_number, h.sender) for h in view.history
                                    if type(h) is ReceivedProse and h.slot.phase == "recovery"]
                        self.assertEqual(incoming, [(1, (p - 1) % 4), (2, (p - 2) % 4)])
        self.assertEqual(joins, 592)

    def test_reversed_invocation_preserves_every_development_sibling_and_prefix(self):
        for world, prefix, continuations, controls in self.cases:
            if not world.development:
                continue
            reverse = execute_witness(world, self.tokenizer, limits=COURSE_LIMITS, settings=self.settings,
                scheduled_branches=branches(world), invocation_order=tuple(reversed(PEERS)))
            self.assertEqual(reverse[0], prefix)
            self.assertEqual(reverse[2], controls)
            for original, repeated in zip(continuations, reverse[1]):
                self.assertEqual(original[:2], repeated[:2])
                self.assertEqual(snapshot_bytes(original[2]), snapshot_bytes(repeated[2]))

    def test_course_witness_rejects_thesis_or_contradictory_settings(self):
        world = self.cases[0][0]
        with self.assertRaisesRegex(ValueError, "contradict"):
            execute_witness(world, self.tokenizer, limits=COURSE_LIMITS)


if __name__ == "__main__":
    unittest.main()
