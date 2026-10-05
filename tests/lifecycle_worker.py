"""CPU controller paused at actual lifecycle boundaries for an external kill.

Instrumentation is confined to this test process. There are no production fault
hooks, alternate state stores or exception-based crash simulations.
"""

import argparse
from dataclasses import asdict
from functools import partial
from pathlib import Path
from time import sleep
import sys
from unittest.mock import patch

import recovery.replay as replay
import recovery.rounds as rounds
from recovery.attempts import ProcessProvider
from recovery.rounds import deserialize_state
from recovery.runner import DurableRunner
from recovery.storage import RecordedFailure
from recovery.tasks import Task
from recovery.workers import _own_file
from tests.event_checks import case_world, scheduled
from tests.lifecycle_fixture import BOUNDS, provider_factory, write_json
from tests.replay_checks import SETTINGS
from tests.round_checks import TOKENIZER


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--marker", type=Path, required=True)
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--round", type=int, required=True)
    parser.add_argument("--peer", type=int, default=0)
    parser.add_argument("--point", choices=("before_raw", "after_raw", "validation", "staging",
                        "before_checkpoint", "after_checkpoint", "after_boundary", "after_timeout"), required=True)
    args = parser.parse_args()
    world = case_world(Task.SORT)
    branch = scheduled(world, "revision", args.policy)
    timeout = 2 if args.point == "after_timeout" else BOUNDS["timeout_seconds"]
    bounds = dict(BOUNDS, timeout_seconds=timeout)
    provider = ProcessProvider(partial(provider_factory, str(args.trace),
                               "hang" if args.point == "after_timeout" else "normal", timeout), **bounds)
    with _own_file(args.path), DurableRunner(args.path, TOKENIZER, provider, dependencies=(args.parent,)) as runner:
        def pause(**detail):
            write_json(args.marker, {"point": args.point, "branch_id": branch.branch_id,
                "round": args.round, "bounds": bounds,
                "runner_module": sys.modules[DurableRunner.__module__].__file__,
                "sqlite": {"ledger": [runner.store.connection.execute("PRAGMA journal_mode").fetchone()[0],
                                      runner.store.connection.execute("PRAGMA synchronous").fetchone()[0]],
                           "checkpoint": [runner.checkpoint_connection.execute("PRAGMA journal_mode").fetchone()[0],
                                          runner.checkpoint_connection.execute("PRAGMA synchronous").fetchone()[0]]},
                **detail})
            while True:
                sleep(0.05)

        finish = runner.store.finish_attempt
        target = next((c.call_id for c in branch.calls if c.round_number == args.round and c.peer == args.peer), None)
        def commit_raw(call_id, response, elapsed, **kwargs):
            if call_id == target and args.point == "before_raw":
                pause(call_id=call_id, returned_response=asdict(response))
            finish(call_id, response, elapsed, **kwargs)
            if call_id == target and (args.point == "after_raw" or
                args.point == "after_timeout" and type(response) is RecordedFailure and response.status == "timeout"):
                pause(call_id=call_id)
        runner.store.finish_attempt = commit_raw

        validate = replay.validate_round
        def during_validation(requests, generated, tokenizer):
            if args.point == "validation" and requests.before.branch_id == branch.branch_id and requests.slot.round_number == args.round:
                one = rounds.validate_reply
                def checked(*a, **kw):
                    result = one(*a, **kw)
                    pause(validated_peer=a[0].peer)
                    return result
                with patch.object(rounds, "validate_reply", checked):
                    return validate(requests, generated, tokenizer)
            return validate(requests, generated, tokenizer)

        stage = replay.stage_effects
        def during_staging(barrier):
            result = stage(barrier)
            if args.point == "staging" and result.branch_id == branch.branch_id and result.last_slot.round_number == args.round:
                pause(staged_delivery_ids=[d.delivery_id for d in result.pending])
            return result

        put = runner.saver.put
        def checkpoint(config, saved, metadata, versions):
            values = saved["channel_values"]
            payload = values.get("committed")
            state = deserialize_state(payload) if payload else None
            selected = (state is not None and state.branch_id == branch.branch_id and
                (args.point == "after_boundary" and values["round_number"] == 0 and state.boundary_applied or
                 state.last_slot is not None and state.last_slot.phase == "recovery" and state.last_slot.round_number == args.round))
            if selected and args.point == "before_checkpoint":
                pause(computed_delivery_ids=[d.delivery_id for d in state.deliveries])
            result = put(config, saved, metadata, versions)
            if selected and args.point in ("after_checkpoint", "after_boundary"):
                pause(checkpoint_id=saved["id"])
            return result
        runner.saver.put = checkpoint
        with patch.object(replay, "validate_round", during_validation), patch.object(replay, "stage_effects", during_staging):
            runner.start(world, branch, settings=SETTINGS)
            runner.run_round(branch.branch_id, args.round)
    raise AssertionError("controller did not reach requested lifecycle boundary")


if __name__ == "__main__":
    main()
