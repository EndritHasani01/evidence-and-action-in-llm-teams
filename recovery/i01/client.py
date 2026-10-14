"""Notebook-owned retained subprocess; explicit finite commands and live events."""

import json
import os
from pathlib import Path
from queue import Queue, Empty
import subprocess
import threading
import time
import uuid
from collections import deque

from .core import canonical
from .runtime import command as runtime_command


def child_environment(hf_cache):
    """Keep notebook startup hooks/renderers out of the pinned child runtime."""
    env={k:v for k,v in os.environ.items() if not k.startswith(('PYTHON','PIP_','VIRTUAL_ENV','MPL'))}
    env.update(HF_HUB_CACHE=str(hf_cache),HF_HUB_ETAG_TIMEOUT='30',HF_HUB_DOWNLOAD_TIMEOUT='60',
               PYTHONUNBUFFERED='1',PYTHONNOUSERSITE='1',PYTHONUTF8='1',MPLBACKEND='Agg')
    return env


class ControllerStartupError(ValueError):
    def __init__(self,message,tail):
        self.tail=tail
        if tail:message+='\n'+tail.splitlines()[-1]
        super().__init__(message)

    def _render_traceback_(self):
        return [str(self),'Controller stderr:',self.tail or '(No stderr was produced.)']


class Client:
    def __init__(self, python, source, run, hf_cache, callback=None, *, startup_timeout=30):
        self.callback=callback or (lambda event:None)
        self.responses={}; self.results={}; self.events=[]
        self.lock=threading.RLock(); self.write_lock=threading.Lock()
        self.run=Path(run)
        logs=self.run/"receipts"; logs.mkdir(exist_ok=True)
        self.log_path=logs/"controller-stderr.log"
        self.log=self.log_path.open("a",encoding="utf-8")
        self.log_start=self.log.tell()
        self.log.write('\nController startup\n'); self.log.flush()
        try:
            self.process=subprocess.Popen(runtime_command(python,source,'-m','recovery.i01.cli','--source',source,'--run',run,'serve'),
                                          stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.log,
                                          text=True,encoding='utf-8',bufsize=1,env=child_environment(hf_cache),cwd=Path(run).resolve())
        except Exception:
            self.log.close()
            raise
        self.ready=threading.Event()
        self.exited=threading.Event()
        self.reader=threading.Thread(target=self._read,daemon=True)
        self.reader.start()
        deadline=time.monotonic()+startup_timeout
        while not self.ready.wait(.1):
            if self.exited.is_set() or self.process.poll() is not None:
                self._startup_failed('Controller exited before ready')
            if time.monotonic()>=deadline:
                self._startup_failed('Controller startup deadline exceeded')

    def _startup_failed(self, reason):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            try: self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                try: self.process.wait(timeout=5)
                except subprocess.TimeoutExpired: reason+='; process exit unconfirmed, do not start a replacement'
        code=self.process.poll()
        if code is not None:
            self.reader.join(timeout=5)
            self.process.stdout.close()
            self.log.close()
        else: self.log.flush()
        with self.log_path.open(encoding='utf-8',errors='replace') as stream:
            stream.seek(self.log_start)
            tail=''.join(deque(stream,maxlen=80)).strip()
        raise ControllerStartupError(f'{reason} (exit={code}). Full log: {self.log_path}',tail)

    def _read(self):
        for line in self.process.stdout:
            try:
                item=json.loads(line)
            except ValueError:
                self.callback(dict(kind="transport_log",text=line)); continue
            if item.get("ready"):
                self.ready.set()
            if "event" in item:
                with self.lock: self.events.append(item["event"])
                self.callback(item["event"])
            if "done" in item:
                with self.lock: self.results[item["done"]]=item["result"]
            if "id" in item:
                with self.lock: queue=self.responses.get(item["id"])
                if queue: queue.put(item)
        self.exited.set()
        self.callback(dict(kind="controller_exit",exitcode=self.process.poll()))

    def command(self, op, timeout=30, **args):
        if self.process.poll() is not None:
            raise ValueError(f"controller exited; inspect {self.log_path}; explicit restore/reopen required")
        identity=str(uuid.uuid4()); queue=Queue()
        with self.lock: self.responses[identity]=queue
        try:
            with self.write_lock:
                self.process.stdin.write(canonical(dict(id=identity,op=op,**args))+"\n")
                self.process.stdin.flush()
            response=queue.get(timeout=timeout)
            if response.get("error"):
                raise ValueError(response["error"])
            return response["result"]
        except Empty as exc:
            raise ValueError("management response deadline; do not start a replacement controller until old exit is confirmed") from exc
        finally:
            with self.lock: self.responses.pop(identity,None)

    def start(self, action, **args):
        receipt=self.command("start",action=action,args=args,authorization="Explicit operator finite-action command/button")
        return receipt.get("started") or receipt["attached"]

    def wait(self, identity, timeout=None):
        started=time.monotonic()
        last_progress=started
        try:
            while True:
                with self.lock: result=self.results.get(identity)
                if result is not None:
                    return result
                if self.process.poll() is not None:
                    raise ValueError("controller exited; admitted attempts remain spent/unknown until reconciled")
                if timeout is not None and time.monotonic()-started>timeout:
                    raise ValueError("client wait ended; action may still be running, request pause/status")
                if time.monotonic()-last_progress>=15:
                    lines=self.log_path.read_text(encoding="utf-8",errors="replace").splitlines()
                    self.callback(dict(kind="worker_progress",elapsed_seconds=round(time.monotonic()-started),
                                       text=lines[-1][-500:] if lines else "bounded action still active"))
                    last_progress=time.monotonic()
                time.sleep(.15)
        except KeyboardInterrupt:
            self.command("pause")
            raise

    def action(self, action, **args):
        return self.wait(self.start(action,**args))

    def close(self):
        self.command("close",timeout=120)
        self.process.stdin.close()
        code=self.process.wait(timeout=20)
        self.reader.join(timeout=5)
        self.process.stdout.close()
        self.log.close()
        if code:
            raise ValueError(f"controller shutdown exit={code}; inspect {self.log_path}")

