"""Local-evidence attainability through the real protocol, without inference."""

from dataclasses import replace
import unittest

from recovery.events import start_continuation
from recovery.prompts import render_request, tokenize_request
from recovery.protocol import validate_reply
from recovery.replay import commit_continuation_round, held_prose_counts, obtain_continuation_round
from recovery.rounds import run_prefix, snapshot_bytes
from recovery.schedule import _prepare_branches
from recovery.state import PendingSource, Slot, initial_view
from recovery.tasks import PEERS, Size, Task
from recovery.truth import exact_candidate, solve_world
from recovery.witness import local_candidate, witness_provider, witness_reply
from tests.event_checks import case_world
from tests.round_checks import TOKENIZER

SETTINGS = {"enable_thinking": False, "temperature": 0.7, "top_p": 0.8,
            "top_k": 20, "min_p": 0, "repetition_penalty": 1.0,
            "max_new_tokens": 384, "do_sample": True}


def execute_witness(world, tokenizer=TOKENIZER, *, invocation_order=PEERS):
    """Run every scheduled sibling of a saved world, including exact parents.

    The host owns scheduling and offline checking, separately from the provider.
    B/C records are retained before delivery; sibling starts use the same bytes.
    """

    branches = _prepare_branches((world,))
    prefix_branch = next(b for b in branches if b.phase == "prefix")
    provider = witness_provider(tokenizer)
    prefix = run_prefix(world.world, prefix_branch.branch_id, tokenizer, provider,
                        invocation_order=invocation_order)
    parents, continuations, controls = [], [], []
    for branch in branches:
        if branch.phase == "control":
            view = initial_view(world.world if branch.event == "original" else world.event_world(branch.event), None)
            rendered = render_request(view)
            encoded = tokenize_request(rendered, tokenizer)
            reply = validate_reply(view, provider(view, rendered, encoded,
                seed=branch.calls[0].seed, settings=SETTINGS), tokenizer)
            controls.append((branch, view, encoded, reply))
        elif branch.phase == "continuation":
            state = start_continuation(prefix.snapshot, world, branch)
            saved_rounds = []
            for _ in range(4):
                saved = obtain_continuation_round(state, branch, tokenizer, provider,
                    settings=SETTINGS, parents=tuple(parents), invocation_order=invocation_order)
                if saved.barrier.requests.slot == Slot("recovery", 1) and branch.policy in ("B", "C"):
                    parents.append(saved)
                saved_rounds.append(saved)
                state = commit_continuation_round(saved).committed
            continuations.append((branch, tuple(saved_rounds), state))
    return prefix, tuple(continuations), tuple(controls)


class AttainabilityTests(unittest.TestCase):
    def test_all_families_sizes_siblings_replicates_and_controls_attain_correctness(self):
        for size in Size:
            for task in Task:
                world = case_world(task, size)
                prefix, continuations, controls = execute_witness(world)
                for result in prefix.rounds:
                    self.assertTrue(all(r.protocol_valid for r in result.barrier.replies))
                for p, outcome in enumerate(prefix.rounds[-1].barrier.replies):
                    self.assertTrue(exact_candidate(solve_world(world.world), outcome.candidate.payload(task), p))
                for branch, rounds, state in continuations:
                    with self.subTest(size=size, task=task, event=branch.event,
                                      policy=branch.policy, replicate=branch.replicate):
                        self.assertEqual(len(rounds), 4)
                        self.assertIsNone(state.next_slot)
                        self.assertFalse(state.pending)
                        self.assertTrue(all(r.protocol_valid for saved in rounds for r in saved.barrier.replies))
                        truth = solve_world(world.event_world(branch.event))
                        for p, outcome in enumerate(rounds[-1].barrier.replies):
                            self.assertTrue(exact_candidate(truth, outcome.candidate.payload(task), p))
                        if branch.policy in ("Q_B", "Q_C"):
                            self.assertEqual(held_prose_counts(state), (1, 1, 1, 1))
                for branch, view, _, reply in controls:
                    self.assertTrue(reply.protocol_valid)
                    self.assertTrue(exact_candidate(solve_world(world.world if branch.event == "original"
                                                               else world.event_world(branch.event)),
                                                    reply.candidate.payload(task)))

    def test_forwarding_visits_each_other_peer_and_uses_only_current_own_records(self):
        for size in Size:
            for task in Task:
                prefix, continuations, _ = execute_witness(case_world(task, size))
                barriers = [r.barrier for r in prefix.rounds]
                for _, rounds, _ in continuations:
                    barriers.extend(r.barrier for r in rounds)
                for barrier in barriers:
                    r = barrier.requests.slot.round_number
                    for p, reply in enumerate(barrier.replies):
                        if r == 4:
                            self.assertFalse(reply.messages)
                        else:
                            self.assertEqual(len(reply.messages), 1)
                            message = reply.messages[0]
                            self.assertEqual(message.recipient, (p + r) % 4)
                            self.assertTrue(all(s.owner == p for s in message.sources))
                            self.assertEqual(message.sources, tuple(s for s in barrier.requests.views[p].sources
                                                                   if s.owner == p))

    def test_missing_or_pending_local_evidence_cannot_be_solved_from_manifest_or_history(self):
        for size in Size:
            for task in Task:
                world = case_world(task, size)
                full = initial_view(world.world, None)
                self.assertIsNotNone(local_candidate(full))
                missing = replace(full, sources=full.sources[:-1], source_deliveries=full.source_deliveries[:-1])
                self.assertIsNone(local_candidate(missing))
                source = full.sources[-1]
                pending = PendingSource(source.record_id, source.owner, source.position, source.version)
                self.assertIsNone(local_candidate(replace(missing, sources=missing.sources + (pending,))))
                self.assertIsNone(local_candidate(initial_view(world.world, 0)))

    def test_local_delivery_waits_for_forwarding_and_fresh_restart_reacquires_all(self):
        for size in Size:
            for task in Task:
                world = case_world(task, size)
                _, continuations, _ = execute_witness(world)
                for branch, rounds, _ in continuations:
                    if branch.event != "revision" or branch.policy not in ("L", "F"):
                        continue
                    for r, saved in enumerate(rounds, 1):
                        for p, view in enumerate(saved.barrier.requests.views):
                            if r == 4:
                                self.assertIsNotNone(local_candidate(view))
                            elif branch.policy == "L":
                                owner = next(s.owner for s in view.manifest
                                             if s.record_id == world.main_edit.record_id)
                                distance = (p - owner) % 4
                                self.assertEqual(local_candidate(view) is not None, distance < r)
                            elif r == 1:
                                self.assertIsNone(local_candidate(view))

    def test_reversed_generation_order_preserves_prefix_and_every_sibling(self):
        for size in Size:
            world = case_world(Task.BFS, size)
            forward = execute_witness(world)
            reverse = execute_witness(world, invocation_order=tuple(reversed(PEERS)))
            self.assertEqual(forward[0].snapshot, reverse[0].snapshot)
            for left, right in zip(forward[1], reverse[1]):
                self.assertEqual(left[1], right[1])
                self.assertEqual(snapshot_bytes(left[2]), snapshot_bytes(right[2]))


if __name__ == "__main__":
    unittest.main()
