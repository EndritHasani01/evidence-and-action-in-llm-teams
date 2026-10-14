"""Bounded spawned resident children with session-level load evidence.

Uses the proven parent sentinel mechanism, independently of old attempt-linked
provider registration. Only exact permitted requests enter children.
"""

import multiprocessing as mp
from multiprocessing.connection import wait
import os
from queue import Queue, Empty
from threading import Thread
from time import monotonic
import traceback

from .store import utc


def child(factory, pipe):
    import sys
    sys.stdout = sys.stderr  # Keep controller stdout exclusively JSON protocol.
    from recovery.attempts import _die_with_owner
    Thread(target=_die_with_owner, daemon=True).start()
    try:
        provider = factory()
        pipe.send(("ready", provider.load_report))
        while True:
            request = pipe.recv()
            if request is None:
                break
            try:
                pipe.send(("outcome", provider(request)))
            except Exception as error:
                pipe.send(("defect", dict(reason=str(error), traceback=traceback.format_exc())))
                break
    except (EOFError, BrokenPipeError):
        pass
    except Exception as error:
        pipe.send(("defect", dict(reason=str(error), traceback=traceback.format_exc())))
    finally:
        pipe.close()


class Resident:
    def __init__(self, factory, termination=5):
        self.factory, self.termination = factory, termination
        self.process = self.pipe = None
        self.unconfirmed = False
        self.load_report = None
        self.load_seconds = None
        self.last_stop = None

    def exchange(self, timeout, request=None, *, loading=False):
        queue = Queue()
        def io():
            try:
                if not loading:
                    self.pipe.send(request)
                queue.put(self.pipe.recv())
            except (EOFError, OSError) as error:
                queue.put(("interrupted", {"reason":str(error)}))
        Thread(target=io, daemon=True).start()
        try:
            return queue.get(timeout=timeout)
        except Empty:
            return "timeout", {"reason":f"known {timeout}s deadline"}

    def load(self, timeout=600):
        if self.unconfirmed:
            raise ValueError("preceding termination unconfirmed")
        if self.process is not None and self.process.is_alive():
            return self.load_report
        ctx = mp.get_context("spawn")
        self.last_stop=None
        self.pipe, remote = ctx.Pipe()
        self.process = ctx.Process(target=child, args=(self.factory, remote))
        started = monotonic()
        self.process.start()
        remote.close()
        kind, evidence = self.exchange(timeout, loading=True)
        self.load_seconds = monotonic()-started
        if kind != "ready":
            termination = self.close()
            raise ValueError(f"load failed: {kind}: {evidence}; {termination}")
        self.load_report = dict(evidence, pid=self.process.pid, loaded_at=utc(), load_seconds=self.load_seconds)
        return self.load_report

    def obtain(self, request, timeout):
        if self.process is None or not self.process.is_alive() or self.unconfirmed:
            raise ValueError("explicit model load required before admission")
        started = monotonic()
        kind, payload = self.exchange(timeout, request)
        if kind == "outcome":
            return dict(payload,dispatch_seconds=monotonic()-started)
        if kind == "timeout":
            # Caller persists timeout before termination acknowledgement.
            return dict(failure="timeout", reason=payload["reason"], ready_seconds=None,observed_seconds=monotonic()-started,
                        termination_pending=True, generated_tokens=None, input_tokens=len(request["input_ids"]))
        termination = self.close()
        if kind == "interrupted":
            raise InfrastructureLost(dict(payload, **termination, observed_seconds=monotonic()-started))
        return dict(failure="provider_defect", **payload, **termination, ready_seconds=None,observed_seconds=monotonic()-started,
                    generated_tokens=None, input_tokens=len(request["input_ids"]))

    def close(self):
        p = self.process
        if p is None:
            return self.last_stop or dict(termination_confirmed=not self.unconfirmed,never_loaded=True)
        if p.is_alive():
            p.terminate()
            p.join(self.termination)
        if p.is_alive():
            p.kill()
            p.join(self.termination)
        self.unconfirmed = p.is_alive()
        evidence = dict(pid=p.pid, exitcode=p.exitcode, termination_confirmed=not self.unconfirmed, stopped_at=utc())
        if self.unconfirmed:
            raise ValueError("model termination unconfirmed; replacement prohibited")
        self.pipe.close()
        p.close()
        self.pipe = self.process = None
        self.last_stop=evidence
        return evidence


class InfrastructureLost(RuntimeError):
    def __init__(self, evidence):
        self.evidence = evidence
        super().__init__(str(evidence))
