"""CPU attainability witness, not a model tool or experimental policy (§8.2).

Only a permitted local view enters the strategy. The host never supplies gold,
an event world, a correction delta, or an unseen record. Use the existing pure
mathematical functions after acquiring all current records, including tombstones.
"""

import json

from .protocol import GeneratedReply
from .state import PeerView
from .tasks import SourceRecord, Task, candidate_contract
from .truth import bfs_distances, differences, prefix_sums, sorted_values, top_k


def local_candidate(view: PeerView) -> list[int] | dict[str, int] | None:
    """Return an answer only from complete locally held current evidence.

    Public IDs identify missing evidence; they never resolve a host payload.
    Pending replacements are insufficient. A delivered deleted edge is known
    evidence and is omitted only from the locally computed active graph.
    """

    if type(view) is not PeerView:
        raise ValueError("witness accepts only a permitted PeerView")
    if (len(view.sources) != len(view.manifest)
            or any(type(source) is not SourceRecord for source in view.sources)):
        return None
    if view.task is Task.BFS:
        return bfs_distances(view.size.node_count,
                             (s.value for s in view.sources if not s.deleted))
    raw = [s.value for s in sorted(view.sources, key=lambda s: s.position)]
    if view.task is Task.TOP_K:
        result = top_k(raw)
    elif view.task is Task.PREFIX:
        result = prefix_sums(raw)
    elif view.task is Task.DIFFERENCE:
        result = differences(raw)
    else:
        result = sorted_values(raw)
    coordinates = candidate_contract(view.task, view.size, view.peer).coordinates
    return [result[j] for j in coordinates] if view.task is not Task.DIFFERENCE else result


def witness_reply(view: PeerView, tokenizer) -> GeneratedReply:
    """Forward the own current shard to a different peer in rounds 1, 2, 3.

    Early placeholders satisfy the shape, without claiming correctness. Text
    deliberately exercises active Q holding/release but supplies no solver input.
    Controls use the complete candidate and empty send. Nothing is shortened.
    """

    candidate = local_candidate(view)
    if candidate is None:
        coordinates = candidate_contract(view.task, view.size, view.peer).coordinates
        candidate = ({str(j): 0 for j in coordinates} if view.task is Task.BFS
                     else [0] * len(coordinates))
    send = []
    if view.peer is not None and view.slot.round_number <= 3:
        own = [s for s in view.sources if type(s) is SourceRecord and s.owner == view.peer]
        send = [{"to": (view.peer + view.slot.round_number) % 4,
                 "source_refs": [{"record_id": s.record_id, "version": s.version} for s in own],
                 "text": "Current private shard."}]
    text = json.dumps({"candidate": candidate, "send": send},
                      ensure_ascii=True, allow_nan=False, separators=(",", ":"))
    return GeneratedReply(text, tuple(tokenizer.encode(text, add_special_tokens=False)), "scripted")


def witness_provider(tokenizer):
    """The ordinary provider interface; settings/seed do not alter this script."""

    def provide(view, rendered, tokenized, *, seed=None, settings=None):
        return witness_reply(view, tokenizer)
    return provide
