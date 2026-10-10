"""Saved course inputs with existing scripted traffic and real exact settings.

These finite fixtures test interventions, not a locally informed witness or the
complete retained-context bound. No evaluator enters the reply providers.
"""

from functools import cache

from recovery.events import start_continuation
from recovery.inference import QWEN_4B, candidate_settings
from recovery.manifests import load_schedules
from recovery.prompts import COURSE_LIMITS
from recovery.replay import obtain_continuation_round
from recovery.rounds import run_prefix
from recovery.tasks import Task
from tests.course_protocol_cases import ROOT, course_population
from tests.event_checks import event_provider
from tests.inference_mocks import Tokenizer
from tests.replay_checks import replay_provider
from tests.round_checks import RoundTokenizer


class CourseTokenizer(RoundTokenizer, Tokenizer):
    """Existing word counter plus pinned-ID/settings metadata double."""


TOKENIZER = CourseTokenizer()


@cache
def course_inputs():
    population = course_population()
    schedule = load_schedules(ROOT / "tests/fixtures/schedules_course.json", population)
    return population, schedule


def branches(world):
    _, schedule = course_inputs()
    return tuple(b for b in schedule.main + schedule.development if b.world_id == world.world_id)


def scheduled(world, event, policy, replicate=0):
    return next(b for b in branches(world) if (b.phase, b.event, b.policy, b.replicate)
                == ("continuation", event, policy, replicate))


def prefix_case(world, tokenizer=TOKENIZER, *, invocation_order=range(4), quiet=False):
    branch = next(b for b in branches(world) if b.phase == "prefix")
    provider = event_provider(tokenizer)
    if quiet:
        from tests.round_checks import reply
        provider = lambda view, *_: reply(tokenizer, view)
    return run_prefix(world.world, branch.branch_id, tokenizer, provider,
                      invocation_order=invocation_order, limits=COURSE_LIMITS)


def first_rounds(world, prefix, tokenizer=TOKENIZER, *, invocation_order=range(4)):
    invocation_order = tuple(invocation_order)
    settings = candidate_settings(tokenizer, QWEN_4B, limits=COURSE_LIMITS)
    saved = {}
    # A second Sort/BFS world has source-only Q traffic: inactive treatments
    # retain unique scheduled IDs rather than duplicating a rich parent record.
    traffic = "silent" if world.index == 2 and world.world.task in (Task.SORT, Task.BFS) else "rich"
    continuations = [b for b in branches(world) if b.phase == "continuation"]
    for branch in sorted(continuations, key=lambda b: b.calls[0].replay_parent is not None):
        parents = tuple(p for p in saved.values() if p.branch.policy in ("B", "C")
                        and (p.branch.event, p.branch.replicate) == (branch.event, branch.replicate))
        state = start_continuation(prefix.snapshot, world, branch)
        record = obtain_continuation_round(state, branch, tokenizer, replay_provider(tokenizer, traffic),
            settings=settings, parents=parents, invocation_order=invocation_order)
        saved[branch.branch_id] = record
    return saved
