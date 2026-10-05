"""Serial worker round graph with exact raw reuse and replacement checkpoints.

Call ledger inputs/outcomes precede effects; committed checkpoints exclusively
own four-peer state/queues/delivery cursors. No model or evaluator is imported.
attempts.py supplies process bounds; M3-T03 adds multi-worker scheduling.
"""

from dataclasses import asdict
import json
from pathlib import Path
from time import monotonic
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from .attempts import ProcessProvider
from .events import start_continuation
from .manifests import _branch
from .protocol import GeneratedReply
from .replay import commit_continuation_round, obtain_continuation_round
from .rounds import (RoundResult, commit_round, deserialize_state, initial_branch,
                     prefix_snapshot, prepare_round, snapshot_bytes, validate_round)
from .schedule import _prepare_branches
from .storage import WorkerStore, connect, record_json, settings_json
from .tasks import PEERS


class _Checkpoint(TypedDict):
    # All channels replace; no reducers or framework message history.
    branch_json: str
    settings_json: str
    committed: bytes
    round_number: int


class DurableRunner:
    """One serial worker and SQLite file. Providers see only permitted inputs.

    run_round takes an explicit scheduled round so replaying a completed operation
    cannot accidentally advance the experiment after a lost acknowledgement.
    """

    def __init__(self, path: Path, tokenizer, reply_provider=None, *, invocation_order=PEERS,
                 scripted=False):
        order = tuple(invocation_order)
        if len(order) != 4 or any(type(p) is not int for p in order) or set(order) != set(PEERS):
            raise ValueError("invoke every peer exactly once")
        if reply_provider is not None and not isinstance(reply_provider, ProcessProvider) and not scripted:
            raise ValueError("inference requires ProcessProvider(factory); direct CPU fixtures require scripted=True")
        self.tokenizer, self.reply_provider, self.order = tokenizer, reply_provider, order
        self.scripted = scripted
        self.store = WorkerStore(path)
        try:
            self.store.recover_processes()
            self.checkpoint_connection = connect(self.store.path)
            self.saver = SqliteSaver(self.checkpoint_connection)
            self.graph = (StateGraph(_Checkpoint)
                .add_node("prepare", self._prepare)
                .add_node("obtain", self._obtain)
                .add_node("commit", self._commit)
                .add_edge(START, "prepare").add_edge("prepare", "obtain")
                .add_edge("obtain", "commit").add_edge("commit", END)
                .compile(checkpointer=self.saver))
        except BaseException:
            if hasattr(self, "checkpoint_connection"):
                self.checkpoint_connection.close()
            self.store.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        if isinstance(self.reply_provider, ProcessProvider):
            self.reply_provider.close()
        # invoke(sync) has completed all writes before this clean checkpoint.
        self.checkpoint_connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        self.checkpoint_connection.close()
        self.store.close()

    @staticmethod
    def _config(branch_id):
        return {"configurable": {"thread_id": branch_id}}

    def _checkpoint(self, branch_id):
        # Read a committed checkpoint, not get_state's synthesized pending writes.
        saved = self.saver.get_tuple(self._config(branch_id))
        if saved is None:
            raise ValueError(f"missing branch checkpoint: {branch_id}")
        return self.graph.get_state(saved.config)

    def state(self, branch_id):
        return deserialize_state(self._checkpoint(branch_id).values["committed"])

    def start(self, world, branch, *, settings: dict):
        """Commit a new original prefix or single applied event in a fresh thread."""
        if branch not in _prepare_branches((world,)) or branch.phase not in ("prefix", "continuation"):
            raise ValueError("durable rounds require a scheduled four-peer branch")
        if branch.phase == "prefix":
            initial = initial_branch(world.world, branch.branch_id)
        else:
            prefix = prefix_snapshot(self.state(branch.prefix_parent))
            initial = start_continuation(prefix, world, branch)
        values = {"branch_json": record_json(asdict(branch)), "settings_json": settings_json(settings),
                  "committed": snapshot_bytes(initial), "round_number": 0}
        config = self._config(branch.branch_id)
        if self.saver.get_tuple(config) is not None:
            # Compare to the initial checkpoint, never transform current state again.
            initial_checkpoint = next(s for s in self.graph.get_state_history(config)
                                      if s.values.get("round_number") == 0)
            if initial_checkpoint.values != values:
                raise ValueError("existing branch start differs in input/settings/schedule")
        else:
            self.graph.update_state(config, values, as_node="commit")
        return self.state(branch.branch_id)

    def _prepare(self, checkpoint):
        state = deserialize_state(checkpoint["committed"])
        branch = _branch(json.loads(checkpoint["branch_json"]))
        if state.next_slot is None or state.next_slot.round_number != checkpoint["round_number"]:
            raise ValueError("round differs from its committed starting checkpoint")
        requests = prepare_round(state, self.tokenizer)
        self.store.prepare(branch, checkpoint["settings_json"], requests)
        return {"round_number": requests.slot.round_number}

    def _obtain(self, checkpoint):
        if isinstance(self.reply_provider, ProcessProvider):
            self.reply_provider.check_termination()
        branch = _branch(json.loads(checkpoint["branch_json"]))
        r = checkpoint["round_number"]
        saved_branch, settings, requests = self.store.inputs(branch.branch_id, r)
        if (saved_branch != branch or settings != checkpoint["settings_json"]
                or requests.before != deserialize_state(checkpoint["committed"])
                or requests != prepare_round(requests.before, self.tokenizer)):
            raise ValueError("frozen requests/settings/state/tokenization equality failed")
        calls = tuple(c for c in branch.calls if c.round_number == r)

        def provide(view, rendered, tokenized, *, seed, settings):
            call = calls[view.peer]
            if (seed != call.seed or settings_json(settings) != checkpoint["settings_json"]
                    or view != requests.views[view.peer] or rendered != requests.rendered[view.peer]
                    or tokenized != requests.tokenized[view.peer]):
                raise ValueError("provider input differs from its durable scheduled request")
            row = self.store.call(call.call_id)
            if row["status"] in ("completed", "timeout", "infrastructure_failure"):
                raw = self.store.response(call.call_id)
            else:
                if self.reply_provider is None:
                    raise ValueError("a pending physical call requires a provider")
                if isinstance(self.reply_provider, ProcessProvider):
                    raw = self.reply_provider.obtain(self.store, call.call_id, view, rendered, tokenized,
                                                     seed=seed, settings=settings)
                elif self.scripted:
                    # Explicitly restricted to deterministic CPU fixtures; no
                    # inference/model adapter may use this unbounded path.
                    self.store.begin_attempt(call.call_id)
                    started = monotonic()
                    raw = self.reply_provider(view, rendered, tokenized, seed=seed, settings=settings)
                    self.store.finish_attempt(call.call_id, raw, monotonic() - started)
                else:
                    raise ValueError("inference requires the bounded ProcessProvider")
                raw = self.store.response(call.call_id)
            return raw if type(raw) is GeneratedReply else None

        if branch.phase == "continuation":
            parent_ids = {self.store.call(c.replay_parent)["branch_id"]
                          for c in calls if c.replay_parent is not None}
            parents = tuple(self.store.saved_round(p, 1, self.tokenizer) for p in sorted(parent_ids))
            saved = obtain_continuation_round(requests.before, branch, self.tokenizer, provide,
                settings=json.loads(settings), parents=parents, invocation_order=self.order)
            barrier = saved.barrier
        else:
            generated = [None] * 4
            for p in self.order:
                generated[p] = provide(requests.views[p], requests.rendered[p], requests.tokenized[p],
                                       seed=calls[p].seed, settings=json.loads(settings))
            barrier = validate_round(requests, tuple(generated), self.tokenizer)
        self.store.save_validation(branch, barrier)
        return {"round_number": r}

    def _commit(self, checkpoint):
        branch = _branch(json.loads(checkpoint["branch_json"]))
        saved = self.store.saved_round(branch.branch_id, checkpoint["round_number"], self.tokenizer)
        result = (commit_continuation_round(saved) if branch.phase == "continuation"
                  else commit_round(saved.barrier))
        return {"committed": snapshot_bytes(result.committed)}

    def run_round(self, branch_id: str, round_number: int) -> RoundResult:
        if type(round_number) is not int or round_number not in range(1, 5):
            raise ValueError("choose one of the four explicit scheduled rounds")
        checkpoint = self._checkpoint(branch_id)
        state = deserialize_state(checkpoint.values["committed"])
        if state.last_slot is not None and state.last_slot.phase == state.phase and state.last_slot.round_number >= round_number:
            return self.result(branch_id, round_number)
        if state.next_slot is None or state.next_slot.round_number != round_number:
            raise ValueError("round is not the next scheduled opportunity")
        config = self._config(branch_id)
        if checkpoint.next:
            if checkpoint.values["round_number"] != round_number:
                raise ValueError("resume the interrupted round before advancing")
            self.graph.invoke(None, config, durability="sync")
        else:
            self.graph.invoke({"round_number": round_number}, config, durability="sync")
        return self.result(branch_id, round_number)

    def result(self, branch_id: str, round_number: int) -> RoundResult:
        for checkpoint in self.graph.get_state_history(self._config(branch_id)):
            payload = checkpoint.values.get("committed")
            if payload is None:
                continue
            state = deserialize_state(payload)
            if (state.last_slot is not None and state.last_slot.phase == state.phase
                    and state.last_slot.round_number == round_number):
                saved = self.store.saved_round(branch_id, round_number, self.tokenizer)
                return RoundResult(saved.barrier, state)
        raise ValueError("round has no committed delivery checkpoint")

    def deliveries(self, branch_id: str):
        """Export only effects in the authoritative committed state."""
        return self.state(branch_id).deliveries

    def backup(self, destination: Path):
        """Archive the whole SQLite snapshot, including a live WAL, via backup."""
        self.store.backup(destination)
