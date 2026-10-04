# State isolation, exact reply reuse, and durable recovery

Investigated 4 October 2026 against the root [specification](../../PROJECT_SPECIFICATION.md), especially §§3.1–3.2, 4.1–4.4 and 9. This is engineering research with CPU toy probes; it is neither the recovery runner nor evidence from the pilot. The specification SHA-256 was `049ff2b44bba185776423c4278bef890c2e55a27330513cb99757ac980a3ced1`.

## Decision

**Retain LangGraph with local SQLite as the supported starting choice.** The isolated probe found no blocker to explicit state replacement, independent branch threads, or durable resume. A small Python loop can express the same fixed barriers, but the specification permits that fallback when the integration cannot preserve semantics; no such incompatibility was demonstrated. Framework adoption does not provide the scientific controls automatically.

Use a small graph around host-controlled round barriers and branch-owned data. The four peers still have separate states and scheduled calls; they do not require framework agent objects, per-peer subgraphs, a supervisor, a cross-thread Store, or framework message reducers. Keep authoritative sources, derived history, candidate/feedback, and delayed prose distinguishable. Plain replacement channels and explicit host transformations are easier to audit than append reducers plus special clearing logic. A plain Python loop remains a valid contingency, with the same persistence, identity, and visibility obligations.

## Repository evidence and boundaries

The root contains no implemented recovery package. Historical [protocol evidence](../../research/04_design_extensions/evidence/PROTOCOL_AUDIT.md) is useful for information-loss examples, but its adjacent probe/results concern an earlier specification snapshot. The archived output-writing main function was not invoked and saved results were not overwritten; selected side-effect-free mathematical functions were rechecked as recorded in [repository validation](repository-and-validation.md).

Current vendored source confirms that [SILO receive](../../acl26-silo-bench/src/msg/tools.py:49) rewrites previous-round files' shared `read` flags. [SILO rounds](../../acl26-silo-bench/src/engine.py:203) skip submitted agents and carry their submission/state forward. These mechanics are unsuitable for sibling branches, provisional candidates, independent delivery cursors, and four continuously active peers. Reuse task mathematics/reference data where appropriate; do not adapt the old directory transport into the new runner. Copying only conversation text would omit channel state.

## Semantics that belong to the application

| Boundary | Engineering conclusion and failure to avoid |
|---|---|
| Source authority (§3.1) | Invalidate v1 everywhere when the public notice arrives. An undelivered v2 is an update-pending marker, not the old usable record. A delivered BFS tombstone is known current evidence, but its endpoints must not leak through the public notice before content delivery. |
| Historical information (§§3.1, 4.3) | Current sources render once outside derived history; no historical raw tables or resolved forwarding payloads accumulate there. Before-values in receipts remain outside current-source lookup/forwarding. Old values in actual model prose/candidates remain part of the treatment. |
| Reset (§4.1) | Replace history, candidate, and feedback explicitly. K keeps exactly the valid fourth-round candidate or absence; never a previous/better answer. Preserve notices/receipts outside clearable history. C/F distinctions concern acquired remote evidence, not hidden model state. |
| Prefix cut (§3.2) | Drain round-four deliveries, then serialize the complete prefix. Branches independently deserialize it into fresh thread IDs. Include queue/cursor state, not just peer text. Never mutate a shared nested object or reuse a parent thread. |
| Synchronous round (§§3.2, 9) | All four permitted views come from one immutable start-of-round state; all replies validate before any recipient sees current-round effects. GPU execution may be serial without changing this barrier. |
| Mixed first round (§4.2) | Replay each peer's exact B or C raw reply, including invalid replies and completed failure identities. Combine the selected outgoing set, then apply recipient effects inside the mixed branch. B/C post-delivery tables are not branch seeds. |
| Q first round (§4.4) | Replay parent raw replies; deliver source references normally, hold only received prose. Own replies and round-two source tables must equal the parent. Release held round-one text before round-two text at the round-three boundary, then append at release time without rewriting history already seen. |
| Rendering (§§3.1, 4.4) | Pending text must not leak through queue labels, placeholders, summaries, errors, candidate sharing, or metadata. Source-delivery metadata stays equal across Q/parent siblings; text-only held messages introduce no revealing placeholder. |

LangGraph's internal node inputs or “private” state channels are not a model-visibility security boundary. Build each request from an explicit permitted peer view; never pass the host world/state wholesale to a model adapter. Inspection of `LastValue.get()` showed it returns the stored object itself, so graph state also must be treated as immutable rather than relying on automatic deep copies. The [Graph API guide](https://docs.langchain.com/oss/python/langgraph/graph-api) documents replacement/reducer behavior and warns that private channels can appear in streaming output.

## Exact reuse is different from framework replay

LangGraph time travel reruns nodes after a selected checkpoint; it is not a cache of exact required replies. The [checkpointer guide](https://docs.langchain.com/oss/python/langgraph/checkpointers) documents this distinction, reducer-aware `update_state`, pending-write recovery, and synchronous durability. The probe independently observed node re-execution during time travel.

The experiment therefore needs explicit physical-generation and logical-call identities regardless of framework. A completed response is immutable evidence, including protocol-invalid raw output. Before required reuse, assert byte-identical rendered requests and equal settings, seed, and permitted state. Matching seeds alone is insufficient. Parent IDs/settings/condition labels belong in the offline audit, not the prompt. A new continuation replicate must obtain new physical generations; reuse parents must be scoped within its replicate.

Store both the pre-delivery barrier and committed state. Exact saved replies can be reused without borrowing another branch's recipient tables, held queue, or applied-message set. A stable delivery ID must be interpreted together with its branch: the same generated message can legitimately have one effect in each sibling. Within one branch it must never apply twice.

## Persistence recommendation and its limits

Persist each raw response in a committed call record before validation-dependent delivery effects. Checkpointer output alone is insufficient if an interruption occurs after the backend response but before a node returns. A small call ledger in the worker's SQLite file is sufficient; a separate event-sourcing platform is unnecessary. Completed invalid responses/timeouts must not become new sampling opportunities. The single permitted infrastructure retry is only for an interruption without a durable response; every attempt remains charged (§9).

Prefer `durability="sync"` at graph barriers. “Sync” means the framework waits for checkpoint writes; it does not make external inference atomic or prove exactly-once generation. A crash before reply persistence can leave an unobserved completed inference. Record the ambiguity rather than infer that the call did not run.

Keep branch delivery transitions pure and reconstructible from durable replies/state, with branch-local applied IDs. If implementation also materializes delivery effects in separate SQL rows, those rows and the authoritative effect state require an atomic transaction or explicit recoverable reconciliation. Graph checkpointing and an unrelated transaction are not automatically one atomic commit. Avoid two independently authoritative representations of the same peer state.

Installed `SqliteSaver` source sets WAL, creates checkpoints/writes tables, uses a per-instance `threading.Lock`, and opens its connection with `check_same_thread=False`. Its private `cursor()` commits in `finally`; it is **not** a general rollback-on-exception transaction wrapper. Do not use its internals for custom multi-statement call/effect transactions. Use public `sqlite3` transactions on a deliberately owned connection, serialize worker writes, and do not hold write locks during model inference. One file per worker bounds contention; multiple writers/processes sharing one file add no current scientific benefit. Source: [SQLite saver](https://github.com/langchain-ai/langgraph/blob/main/libs/checkpoint-sqlite/langgraph/checkpoint/sqlite/__init__.py), with the tested wheel identity recorded below.

The toy file reported WAL and `PRAGMA synchronous=2` (FULL). Verify those settings on the execution host. WAL supports readers alongside a writer, not multiple simultaneous writers; SQLite documents the power-loss durability difference between FULL and NORMAL. A running WAL database must be archived through SQLite backup or after a clean checkpoint/close, rather than copying only its main file. [SQLite WAL documentation](https://www.sqlite.org/wal.html) and [Python 3.11 transaction/thread behavior](https://docs.python.org/3.11/library/sqlite3.html) support these constraints. No PostgreSQL, Redis, broker, vector store, graph database, or remote tracing service is needed.

## Isolated probe: exact evidence

The host has Python 3.11.9 / SQLite 3.45.1. Its pre-existing packages were LangGraph 1.2.5, checkpoint 4.1.1 and core 1.4.7, without the SQLite saver. A fresh temporary venv was installed without changing repository dependency files or the host packages. The live PyPI metadata resolved the following combination; this is a tested candidate, not the final GPU environment lock:

| Package | Tested version | Evidence |
|---|---|---|
| `langgraph` | 1.2.12 | [Exact PyPI release](https://pypi.org/project/langgraph/1.2.12/) |
| `langgraph-checkpoint` | 4.2.0 | [Exact PyPI release](https://pypi.org/project/langgraph-checkpoint/4.2.0/) |
| `langgraph-checkpoint-sqlite` | 3.1.1 | [Exact PyPI release](https://pypi.org/project/langgraph-checkpoint-sqlite/3.1.1/) |
| `langchain-core` | 1.6.6 | Transitive resolved dependency |

Pydantic 2.13.5 and aiosqlite 0.22.1 also resolved. The SQLite package transitively installs sqlite-vec 0.1.9, but this experiment does not need or use vector search. The standard LangGraph distribution similarly includes prebuilt/SDK dependencies; their presence does not require using those abstractions or hosted services.

Exact tested wheel SHA-256 values:

- `langgraph-1.2.12-py3-none-any.whl`: `95403af7b510de8d79164742f71daaf866c69ca804a8cb72bef2cc1fa1ab9813`.
- `langgraph_checkpoint_sqlite-3.1.1-py3-none-any.whl`: `8505c54c94a658080525d7e6780fdd4e0c078ff2566b30d399c02cc9f9af1c63`.

Inspected source identities within those wheels, rather than assuming mutable upstream `main` equals the tested code:

- SQLite saver `__init__.py`: `b577c44d44e72b270d78caee4b7aacc5d2521dbbc1a33d39fb3240e20a830439`.
- `channels/binop.py`: `85dbe7cdd3cea5f2973dbf3f358ad04c61c7b8dad5dc74a579739aa328a1b54e`.
- `channels/last_value.py`: `36cbc586aeaac0f8c9b5a8d8b903039023a7d24294408391eb8c7f10aab3a308`.

Commands used: `python -m venv <temporary-directory>`; `<temporary-directory>/Scripts/python.exe -m pip install --disable-pip-version-check langgraph==1.2.12 langgraph-checkpoint-sqlite==3.1.1`; then `<temporary-directory>/Scripts/python.exe <temporary-directory>/toy.py`. No model download, inference, project pilot, or historical-result regeneration occurred.

Nine assertions passed with exit code 0:

1. Independent JSON-deserialized snapshots in fresh threads kept parent/right unchanged when left's nested source/history changed.
2. Default replacement channel cleared history with `[]`.
3. Append-reducer channel kept old history after an empty update.
4. `Overwrite([])` cleared that append channel.
5. An intentionally invalid raw string was durable before a synthetic downstream interruption.
6. Closing/reopening the disk saver and rebuilding the graph resumed downstream work without rerunning the completed reply node.
7. Time travel reran that node; the explicit call-ID ledger returned the same raw string, keeping physical generations at one.
8. A standard-library SQLite context-manager transaction rolled back its insert on an injected exception.
9. A `(branch, message_id)` uniqueness constraint accepted one effect in each sibling while ignoring repeated application within a sibling.

The resumed/time-travel counters were `node executions=2`, `physical generations=1`. The synthetic downstream marker was not a model message or protocol-validity test. This probe demonstrates library behavior and application-ledger necessity, not the final protocol's correctness.

The full temporary probe is reproduced below so its evidence does not depend on retaining a temporary directory.

```python
import hashlib, json, operator, sqlite3, sys, tempfile
from pathlib import Path
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Overwrite
from langgraph.checkpoint.sqlite import SqliteSaver

class S(TypedDict):
    history: list[str]
    sources: dict
    raw: str
    applied: list[str]
class A(TypedDict):
    history: Annotated[list[str], operator.add]

def config(label): return {"configurable": {"thread_id": label}}
def graph(schema, saver):
    b = StateGraph(schema)
    b.add_node("noop", lambda s: {})
    b.add_edge(START, "noop"); b.add_edge("noop", END)
    return b.compile(checkpointer=saver)

path = Path(tempfile.mkdtemp(prefix="lg-toy-")) / "state.sqlite"
checks = []
with SqliteSaver.from_conn_string(str(path)) as saver:
    g = graph(S, saver)
    base = {"history": ["old"], "sources": {"r": {"v": 1}}, "raw": "", "applied": []}
    g.invoke(base, config("prefix"), durability="sync")
    blob = json.dumps(g.get_state(config("prefix")).values)
    left, right = json.loads(blob), json.loads(blob)
    left["history"] = []; left["sources"]["r"]["v"] = 2
    g.invoke(left, config("left"), durability="sync")
    g.invoke(right, config("right"), durability="sync")
    assert g.get_state(config("left")).values["history"] == []
    assert g.get_state(config("right")).values["sources"]["r"]["v"] == 1
    assert g.get_state(config("prefix")).values == json.loads(blob)
    g.update_state(config("right"), {"history": []})
    assert g.get_state(config("right")).values["history"] == []
    checks += ["deserialized-new-threads-isolated", "default-channel-clears"]
    a = graph(A, saver)
    a.invoke({"history": ["old"]}, config("append"), durability="sync")
    a.update_state(config("append"), {"history": []})
    assert a.get_state(config("append")).values["history"] == ["old"]
    a.update_state(config("append"), {"history": Overwrite([])})
    assert a.get_state(config("append")).values["history"] == []
    checks += ["append-empty-does-not-clear", "overwrite-clears"]

attempts = {"nodes": 0, "generations": 0}; fail_once = [True]
# Separate connection/transactions: no dependence on saver-internal cursor.
with sqlite3.connect(path) as ledger:
    ledger.execute("create table replies(id text primary key, raw text not null)")

def reply(s):
    attempts["nodes"] += 1
    with sqlite3.connect(path) as ledger:
        row = ledger.execute("select raw from replies where id=?", ("toy-call",)).fetchone()
        if row is None:
            attempts["generations"] += 1
            raw = "{invalid"
            ledger.execute("insert into replies values (?,?)", ("toy-call", raw))
        else: raw = row[0]
    return {"raw": raw}

def effects(s):
    if fail_once[0]:
        fail_once[0] = False
        raise RuntimeError("toy interruption after durable raw reply")
    assert s["raw"] == "{invalid"
    return {"applied": list(dict.fromkeys(s["applied"] + ["toy-delivery"]))}

def resumable(saver):
    b = StateGraph(S)
    b.add_node("reply", reply); b.add_node("effects", effects)
    b.add_edge(START, "reply"); b.add_edge("reply", "effects"); b.add_edge("effects", END)
    return b.compile(checkpointer=saver)
with SqliteSaver.from_conn_string(str(path)) as saver:
    g = resumable(saver)
    try: g.invoke(base, config("durable"), durability="sync")
    except RuntimeError: pass
    before_reply = next(s for s in g.get_state_history(config("durable")) if s.next == ("reply",))
    assert g.get_state(config("durable")).values["raw"] == "{invalid"
# Close/reopen disk checkpointer and reconstruct graph.
with SqliteSaver.from_conn_string(str(path)) as saver:
    g = resumable(saver)
    assert g.invoke(None, config("durable"), durability="sync")["applied"] == ["toy-delivery"]
    assert attempts == {"nodes": 1, "generations": 1}
    g.invoke(None, before_reply.config, durability="sync")
    assert attempts == {"nodes": 2, "generations": 1}
    checks += ["invalid-raw-persists-before-effects", "reopen-resume-skips-completed-node", "time-travel-reexecutes-node-ledger-suppresses-generation"]
# stdlib transaction rollback and branch-scoped idempotence, without LangGraph.
with sqlite3.connect(path) as db:
    db.execute("create table effects(branch text, id text, primary key(branch,id))")
try:
    with sqlite3.connect(path) as db:
        db.execute("insert into effects values (?,?)", ("a", "m"))
        raise RuntimeError("rollback")
except RuntimeError: pass
with sqlite3.connect(path) as db:
    assert db.execute("select count(*) from effects").fetchone()[0] == 0
    for branch in ["a", "a", "b"]:
        db.execute("insert or ignore into effects values (?,?)", (branch, "m"))
    assert db.execute("select count(*) from effects").fetchone()[0] == 2
    checks += ["effect-transaction-rolls-back", "delivery-idempotence-is-branch-scoped"]
    print("sqlite_pragmas", db.execute("pragma journal_mode").fetchone()[0], db.execute("pragma synchronous").fetchone()[0])
print(json.dumps({"passed": checks, "attempts": attempts, "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}, indent=2))
```

## Remaining implementation validation, not further framework research

| Gate | What remains unverified |
|---|---|
| Full branch transformations | Scripted final-schema fixtures must establish B/C/K/mask evidence equality; C/F evidence differences; persistent notices/receipts; K-invalid absence; and no nested parent/sibling mutation. Include v1→v2→v3 CPU source checks without adding a second live revision. |
| Barrier and intervention delivery | Scripted source-plus-text and text-only messages must verify all four start views, branch-specific mixed assembly, Q round-two equality, no held-text leak, chronological release, and stable-ID resume. The toy graph did not implement these scientific controls. |
| Failure at actual boundaries | Inject process termination before/after raw-reply commit, during validation/staging, and before/after committed delivery. Completed invalid replies must produce zero messages/candidate credit and never be regenerated. Account for an uncertain backend completion before persistence. The probe used an exception plus disk reopen, not a killed process or power failure. |
| Execution-host compatibility | Repeat the small saver/replacement/resume probe in the accepted Linux/CUDA environment lock; verify disk persistence across worker restart and snapshot archival. Windows CPU success does not certify the GPU environment. |

Graph node granularity, SQL table names, concurrency details, and timeout enforcement remain ordinary implementation choices, provided these invariants pass. No more framework comparison is needed before planning. The unresolved work is concrete validation of the eventual small runner, not a reason to build a larger orchestration platform.
