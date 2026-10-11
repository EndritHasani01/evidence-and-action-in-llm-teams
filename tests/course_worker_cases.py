"""Saved course scope using the existing lifecycle provider and bundle helpers."""

from functools import partial
from time import sleep

from recovery.inference import QWEN_4B, candidate_settings
from recovery.prompts import COURSE_LIMITS, render_request, tokenize_request
from recovery.tasks import Task
from tests.course_intervention_cases import TOKENIZER, branches, course_inputs, scheduled
from tests.lifecycle_fixture import BOUNDS, provide as lifecycle_provide

SETTINGS = candidate_settings(TOKENIZER, QWEN_4B, limits=COURSE_LIMITS)


def tokenizer_factory():
    return TOKENIZER


def sort_world():
    return next(w for w in course_inputs()[0].main if w.world.task is Task.SORT and w.index == 1)


def provider_factory(trace=None, mode="normal", timeout=8, delay=0):
    return partial(provide, trace=trace, mode=mode, timeout=timeout, delay=delay)


def provide(view, rendered, tokenized, *, seed, settings, trace=None, mode="normal", timeout=8, delay=0):
    assert settings == SETTINGS
    assert rendered == render_request(view, limits=COURSE_LIMITS)
    assert tokenized == tokenize_request(rendered, TOKENIZER, limits=COURSE_LIMITS)
    sleep(delay)
    return lifecycle_provide(view, rendered, tokenized, seed=seed, settings=settings,
                             trace=trace, mode=mode, timeout=timeout, tokenizer=TOKENIZER)


def bind(store, worlds, selected, bounds=BOUNDS):
    store.bind_run(worlds, selected, SETTINGS, bounds, regime="course")


def prefix_branch(world):
    return next(b for b in branches(world) if b.phase == "prefix")
