"""CPU controller deliberately paused at a real durable-response boundary."""

import argparse
from functools import partial
from pathlib import Path
from time import sleep

from recovery.attempts import ProcessProvider
from recovery.runner import DurableRunner
from recovery.storage import RecordedFailure
from recovery.tasks import Task
from tests.attempt_checks import append_trace, process_factory
from tests.durable_checks import prefix_branch
from tests.event_checks import case_world
from tests.replay_checks import SETTINGS
from tests.round_checks import TOKENIZER


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--point", choices=("before_raw", "after_raw", "after_timeout", "loading"), required=True)
    parser.add_argument("--timeout", type=float, default=5)
    parser.add_argument("--mode", default="normal")
    args = parser.parse_args()
    mode = "hang_first" if args.point == "after_timeout" else "hang_load" if args.point == "loading" else args.mode
    boundary = ProcessProvider(partial(process_factory, mode, str(args.trace)),
        timeout_seconds=args.timeout, termination_seconds=0.25, heartbeat_seconds=0.05)
    world = case_world(Task.SORT)
    branch = prefix_branch(world)
    with DurableRunner(args.path, TOKENIZER, boundary) as runner:
        runner.start(world, branch, settings=SETTINGS)
        finish = runner.store.finish_attempt

        def pause():
            append_trace(args.trace, {"event": "controller_point", "point": args.point})
            while True:
                sleep(1)

        def commit(call_id, response, elapsed_seconds, **kwargs):
            if call_id == branch.calls[0].call_id and args.point == "before_raw":
                pause()
            finish(call_id, response, elapsed_seconds, **kwargs)
            if call_id == branch.calls[0].call_id and (args.point == "after_raw" or
                    (args.point == "after_timeout" and isinstance(response, RecordedFailure) and response.status == "timeout")):
                pause()

        runner.store.finish_attempt = commit
        runner.run_round(branch.branch_id, 1)
    raise AssertionError("controller did not reach the requested boundary")


if __name__ == "__main__":
    main()
