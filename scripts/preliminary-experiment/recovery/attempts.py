"""Bounded serial inference subprocess; the parent owns all durable records.

The importable factory loads one provider/model in the spawned child. Only the
permitted view, exact request, seed and settings cross into its generation call.
Weights may stay resident; conversation/KV/recurrent state may not cross calls.
No inference dependency is imported here. M5 supplies and verifies the adapter.
"""

import multiprocessing as mp
from dataclasses import dataclass
from multiprocessing.connection import wait
import os
import traceback
from queue import Empty, Queue
from threading import Thread
from time import monotonic

from .protocol import GeneratedReply
from .storage import RecordedFailure, UnresolvedAttempt, record_json, seconds


class InfrastructureInterruption(RuntimeError):
    """An interrupted backend with no durable response; never answer invalidity."""


class ProviderDefect(ValueError):
    """An adapter/protocol error requiring diagnosis, not another sample."""


@dataclass(frozen=True)
class MeasuredReply:
    """Optional adapter measurement, outside the literal scientific reply."""

    response: GeneratedReply | RecordedFailure
    peak_memory_bytes: int
    backend: dict | None = None

    def __post_init__(self):
        if (type(self.response) not in (GeneratedReply, RecordedFailure)
                or type(self.peak_memory_bytes) is not int or self.peak_memory_bytes < 0
                or self.backend is not None and type(self.backend) is not dict):
            raise ValueError("record an exact outcome and measured peak device bytes")
        if self.backend is not None:
            record_json(self.backend)  # Reject unsavable evidence before transmission.


def _die_with_owner():
    # terminate() does not terminate descendants. Monitor the actual owner
    # sentinel, including during loading/generation, rather than a reused PID.
    parent = mp.parent_process()
    wait([parent.sentinel])
    os._exit(72)


def _serve(factory, connection):
    Thread(target=_die_with_owner, daemon=True).start()
    phase = "provider_startup"
    try:
        provider = factory()
        if not callable(provider):
            raise ProviderDefect("provider factory must return a callable")
        connection.send(("ready", getattr(provider, "load_report", None)))
        while True:
            request = connection.recv()
            if request is None:
                return
            view, rendered, tokenized, seed, settings = request
            phase = "generation"
            response = provider(view, rendered, tokenized, seed=seed, settings=settings)
            if response is None:
                response = RecordedFailure("infrastructure_failure", "provider recorded an exhausted failed slot")
            if type(response) not in (GeneratedReply, RecordedFailure, MeasuredReply):
                raise ProviderDefect("provider must return exact generated output or a recorded final failure")
            connection.send(("response", response))
    except InfrastructureInterruption as error:
        connection.send(("interrupted", str(error)))
    except (EOFError, BrokenPipeError):
        pass
    except Exception as error:
        # Keep the original child stack in the existing durable attempt reason.
        # A string payload remains compatible with previous provider messages.
        connection.send(("error", f"{type(error).__name__}: {error}\nphase={phase}\n{traceback.format_exc()}"))
    finally:
        connection.close()


class ProcessProvider:
    """One resident serial model process, reloaded after termination.

    Timeout includes startup/loading and communication. Terminate and kill each
    have a bounded grace; an unconfirmed kill stops instead of admitting a retry.
    A small I/O thread keeps partial/hung pipe transfers off the controller.
    Heartbeats update only existing attempt/process records, never peer views.
    The caller must exclusively own the worker file and stop its preceding owner
    before reopening it. A factory must be picklable under Python's spawn method.
    """

    def __init__(self, factory, *, timeout_seconds=120, termination_seconds=1,
                 heartbeat_seconds=1, before_attempt=None):
        self.timeout_seconds = seconds(timeout_seconds)
        self.termination_seconds = seconds(termination_seconds)
        self.heartbeat_seconds = seconds(heartbeat_seconds)
        if (not callable(factory) or min(self.timeout_seconds, self.termination_seconds,
                                        self.heartbeat_seconds) == 0
                or self.heartbeat_seconds > 60):
            raise ValueError("use a callable factory, positive bounds and a heartbeat within 60 seconds")
        self.factory = factory
        if before_attempt is not None and not callable(before_attempt):
            raise ValueError("physical-attempt admission must be callable or absent")
        self.before_attempt = before_attempt
        self._process = self._connection = self._owner = self._store = None
        self._termination_unconfirmed = False
        self._idle = False

    def _start(self, store, call_id, number):
        context = mp.get_context("spawn")
        self._connection, child_connection = context.Pipe()
        self._process = context.Process(target=_serve, args=(self.factory, child_connection))
        try:
            self._process.start()
        finally:
            child_connection.close()
        self._owner, self._store = (call_id, number), store
        store.process_started(call_id, number, self._process.pid)

    def _stop(self, reason):
        process, connection = self._process, self._connection
        if process is None:
            return
        if process.pid is not None:
            deadline = monotonic() + self.termination_seconds
            if reason == "controller_close" and self._idle and process.is_alive() and connection is not None:
                # Idle children can release their resources through the existing
                # stop sentinel. Never block pipe I/O or extend the TERM/KILL
                # bounds, and never give an in-flight/hung call this grace.
                def stop_idle():
                    try:
                        connection.send(None)
                    except (EOFError, OSError):
                        pass
                Thread(target=stop_idle, daemon=True).start()
                process.join(self.termination_seconds/2)
            if process.is_alive():
                process.terminate()
            process.join(max(0, deadline-monotonic()))
            if process.is_alive():
                process.kill()
                process.join(self.termination_seconds)
            if process.is_alive():
                self._termination_unconfirmed = True
                raise UnresolvedAttempt("provider termination could not be confirmed; do not retry")
        if connection is not None:
            connection.close()
        if self._owner is not None:
            self._store.process_stopped(*self._owner, f"{reason}; exitcode={process.exitcode}")
        process.close()
        self._process = self._connection = self._owner = self._store = None
        self._termination_unconfirmed = False
        self._idle = False

    def close(self):
        self._stop("controller_close")

    def check_termination(self):
        if self._termination_unconfirmed:
            raise UnresolvedAttempt("preceding provider termination remains unconfirmed")

    def _execute(self, store, call_id, number, request, started):
        self._idle = False
        fresh = self._process is None
        if fresh:
            self._start(store, call_id, number)
        elif self._store is not store:
            raise ProviderDefect("a resident provider belongs to one worker store")
        messages = Queue()
        connection = self._connection

        def exchange():
            try:
                if fresh:
                    kind, payload = connection.recv()
                    messages.put((kind, payload, monotonic()))
                    if kind != "ready":
                        return
                connection.send(request)
                kind, payload = connection.recv()
                messages.put((kind, payload, monotonic()))
            except (EOFError, OSError) as error:
                messages.put(("interrupted", f"provider transport/exit: {type(error).__name__}", monotonic()))
            except Exception as error:
                messages.put(("error", f"request transport defect: {type(error).__name__}: {error}", monotonic()))

        io = Thread(target=exchange, daemon=True)
        io.start()
        deadline = started + self.timeout_seconds
        try:
            while True:
                store.observe_attempt(call_id, number, monotonic() - started, self._process.pid)
                try:
                    kind, payload, received = messages.get(timeout=max(0, min(
                        self.heartbeat_seconds, deadline - monotonic())))
                except Empty:
                    if monotonic() < deadline:
                        continue
                    kind, payload, received = "deadline", None, monotonic()
                if received > deadline or kind == "deadline":
                    failure = RecordedFailure("timeout", f"known {self.timeout_seconds:g}-second attempt deadline")
                    # Persist the known deadline before termination: owner death
                    # during kill/acknowledgement must never make it retryable.
                    store.finish_attempt(call_id, failure, monotonic() - started,
                                         termination_reason="timeout_termination_pending")
                    self._stop("attempt_timeout")
                    store.confirm_timeout_termination(call_id, monotonic() - started)
                    return failure
                if kind == "ready":
                    store.process_ready(*self._owner, backend=payload)
                elif kind == "response":
                    return payload
                elif kind == "interrupted":
                    self._stop("infrastructure_interruption")
                    raise InfrastructureInterruption(payload)
                else:
                    self._stop("provider_defect")
                    raise ProviderDefect(payload)
        finally:
            # Never wait indefinitely for pipe I/O, even after an OS-level fault.
            io.join(self.termination_seconds)

    def obtain(self, store, call_id, view, rendered, tokenized, *, seed, settings):
        """Return a final durable outcome; at most two infrastructure attempts."""
        self.check_termination()
        row = store.call(call_id)
        if row["status"] == "running":
            if self._process is not None:
                raise UnresolvedAttempt("same owner has an unresolved active call; close/restart before recovery")
            store.interrupt_attempt(call_id, "preceding exclusive worker owner interrupted before durable response")
        while True:
            row = store.call(call_id)
            if row["status"] in ("completed", "timeout", "infrastructure_failure"):
                return store.response(call_id)
            if self.before_attempt is not None:
                # Recheck physical allowance before retries as well as first calls.
                # The controller owns this callback; it never enters a peer view.
                self.before_attempt(store, call_id, len(store.attempts(call_id)) + 1)
            number = store.begin_attempt(call_id, timeout_seconds=self.timeout_seconds,
                                         termination_seconds=self.termination_seconds)
            started = monotonic()
            try:
                response = self._execute(store, call_id, number,
                    (view, rendered, tokenized, seed, settings), started)
                self._idle = True
            except InfrastructureInterruption as error:
                store.interrupt_attempt(call_id, str(error), elapsed_seconds=monotonic() - started,
                                        termination_reason="infrastructure_interruption")
                continue
            except UnresolvedAttempt:
                raise  # Still-live/unknown worker must never admit a second call.
            except Exception as error:
                self._stop("provider_defect")
                store.block_attempt(call_id, str(error), monotonic() - started)
                raise
            except BaseException:
                self._stop("controller_interruption")
                # A later restart records ambiguity; do not infer non-completion.
                raise
            if store.call(call_id)["status"] == "running":
                memory = response.peak_memory_bytes if type(response) is MeasuredReply else None
                backend = response.backend if type(response) is MeasuredReply else None
                if type(response) is MeasuredReply:
                    response = response.response
                store.finish_attempt(call_id, response, monotonic() - started,
                                     peak_memory_bytes=memory, backend=backend)
            return store.response(call_id)
