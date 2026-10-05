"""Importable CPU workers: no model, native tokenizer or evaluator inputs."""

from dataclasses import asdict
from functools import partial
import os
import random
from time import sleep

from tests.attempt_checks import append_trace
from tests.event_checks import event_provider
from tests.replay_checks import replay_provider
from tests.round_checks import TOKENIZER, reply
from recovery.state import ReceivedProse, Slot


def tokenizer_factory():
    return TOKENIZER


def provider_factory(trace, delay=0, pause=None):
    import recovery.workers
    append_trace(trace, {"event": "load", "pid": os.getpid(),
        "visibility": os.environ.get("CUDA_VISIBLE_DEVICES"), "module": recovery.workers.__file__})
    return partial(provide, trace, delay, pause)


def provide(trace, delay, pause, view, rendered, tokenized, *, seed, settings):
    random.seed(seed)  # Per-call process-wide RNG ownership, independent of order.
    append_trace(trace, {"event": "generation", "pid": os.getpid(), "seed": seed,
        "rng_probe": random.randrange(2**32), "visibility": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "view": asdict(view), "rendered": asdict(rendered), "tokenized": asdict(tokenized), "settings": settings})
    held_signature = (any(e.slot.phase == "prefix" for e in view.history)
        and not any(type(e) is ReceivedProse and e.slot == Slot("recovery", 1) for e in view.history))
    if pause is not None and view.slot == Slot("recovery", 2) and view.peer == 0 and held_signature:
        # An external marker bounds this intentional interruption to one attempt.
        from pathlib import Path
        flag = Path(pause)
        if not flag.exists():
            with flag.open("x", encoding="utf-8") as output:
                output.write("provider waiting with held-prose local view")
            append_trace(trace, {"event": "paused", "pid": os.getpid(), "seed": seed})
            while True:
                sleep(0.05)
    sleep(delay)
    if view.slot.phase == "control":
        return reply(TOKENIZER, view)
    if view.slot.phase == "prefix":
        return event_provider(TOKENIZER)(view, rendered, tokenized)
    return replay_provider(TOKENIZER, "unicode")(view, rendered, tokenized, seed=seed, settings=settings)
