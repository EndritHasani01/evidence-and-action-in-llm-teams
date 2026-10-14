"""Two canonical WAL/FULL databases; raw replies precede atomic episode effects.

The old WorkerStore's four-peer registration is intentionally not used. SQLite
transactions/backup and the existing exclusive writer discipline are retained.
"""

from contextlib import contextmanager, closing
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import threading

from .core import canonical

SCHEMA = "i01-episodes-v1"


def utc():
    return datetime.now(timezone.utc).isoformat()


def connection(path, readonly=False, *, create=False):
    db = sqlite3.connect(Path(path).resolve().as_uri() + ("?mode=rwc" if create else "?mode=ro" if readonly else "?mode=rw"),
                         uri=True, check_same_thread=False, timeout=30)
    db.row_factory = sqlite3.Row
    if readonly:
        db.execute("PRAGMA query_only=ON")
    else:
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
    db.execute("PRAGMA foreign_keys=ON")
    return db


class Store:
    @staticmethod
    def validate(path, binding):
        if not Path(path).is_file():
            raise ValueError(f"Missing canonical database: {path}; restore a verified complete checkpoint")
        with closing(connection(path,True)) as db:
            tables={r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not {'meta','episodes','calls','attempts','sessions','annotations'} <= tables:
                raise ValueError(f"Incomplete canonical schema: {path}; no tables were recreated")
            columns={'meta':{'key','value'},'episodes':{'id','state'},'calls':{'id','episode','request','outcome','effect_committed'},
                     'attempts':{'id','call_id','number','stage','contingency','admitted_at','finished_at','status','evidence'},
                     'sessions':{'id','evidence'},'annotations':{'id','evidence'}}
            for table,expected in columns.items():
                if {r['name'] for r in db.execute('PRAGMA table_info('+table+')')}!=expected:
                    raise ValueError(f'Incompatible canonical columns: {path}: {table}')
            if db.execute('PRAGMA quick_check').fetchone()[0]!='ok':
                raise ValueError(f"Corrupt canonical database: {path}")
            metadata={r['key']:json.loads(r['value']) for r in db.execute("SELECT * FROM meta WHERE key IN ('schema','binding')")}
            if metadata.get('schema')!=SCHEMA or metadata.get('binding')!=binding:
                raise ValueError("source/config/input/schema mismatch; read-only inspection only")

    def __init__(self, path, binding, *, readonly=False, create=False):
        self.path, self.readonly = Path(path), readonly
        self.lock = threading.RLock()
        if create and (readonly or self.path.exists()):
            raise ValueError('Schema creation requires a fresh database path')
        if not create: self.validate(path,binding)
        self.db = connection(path, readonly,create=create)
        if create:
            self.db.executescript('''
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS episodes(id TEXT PRIMARY KEY, state TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS calls(id TEXT PRIMARY KEY, episode TEXT NOT NULL,
              request TEXT NOT NULL, outcome TEXT, effect_committed INTEGER NOT NULL DEFAULT 0);
            CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY, call_id TEXT NOT NULL,
              number INTEGER NOT NULL, stage TEXT NOT NULL, contingency INTEGER NOT NULL,
              admitted_at TEXT NOT NULL, finished_at TEXT, status TEXT NOT NULL,
              evidence TEXT, UNIQUE(call_id,number));
            CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, evidence TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS annotations(id TEXT PRIMARY KEY, evidence TEXT NOT NULL);
            ''')
            self.db.commit()
            self.bind("schema", SCHEMA)
            self.bind("binding", binding)
        if self.meta("schema") != SCHEMA or self.meta("binding") != binding:
            raise ValueError("source/config/input/schema mismatch; read-only inspection only")

    @contextmanager
    def transaction(self):
        with self.lock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                yield
                self.db.commit()
            except BaseException:
                self.db.rollback()
                raise

    def meta(self, key, default=None):
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else default

    def put_meta(self, key, value):
        with self.transaction():
            self.db.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (key, canonical(value)))

    def bind(self, key, value):
        if self.meta(key) is not None:
            if self.meta(key) != value:
                raise ValueError("immutable binding differs: " + key)
        else:
            self.put_meta(key, value)

    def state(self, episode):
        row = self.db.execute("SELECT state FROM episodes WHERE id=?", (episode,)).fetchone()
        return json.loads(row[0]) if row else None

    def start(self, episode, state):
        with self.transaction():
            self.db.execute("INSERT OR IGNORE INTO episodes VALUES (?,?)", (episode, canonical(state)))
        return self.state(episode)

    def call(self, identity):
        row = self.db.execute("SELECT * FROM calls WHERE id=?", (identity,)).fetchone()
        return dict(row) if row else None

    def register(self, identity, episode, request):
        with self.transaction():
            row = self.call(identity)
            if row:
                if row["episode"] != episode or row["request"] != canonical(request):
                    raise ValueError("exact saved request/settings/seed differs")
            else:
                self.db.execute("INSERT INTO calls(id,episode,request) VALUES (?,?,?)", (identity, episode, canonical(request)))

    def raw(self, identity, attempt, outcome):
        with self.transaction():
            if self.call(identity)["outcome"] is not None:
                raise ValueError("durable outcome already exists")
            self.db.execute("UPDATE calls SET outcome=? WHERE id=?", (canonical(outcome), identity))
            self.db.execute("UPDATE attempts SET status=?,finished_at=?,evidence=? WHERE id=?",
                            ("completed" if outcome.get("failure") is None else "failed", utc(), canonical(outcome), attempt))

    def effects(self, identity, episode, state):
        with self.transaction():
            row = self.call(identity)
            if row["outcome"] is None:
                raise ValueError("persist raw outcome first")
            if not row["effect_committed"]:
                self.db.execute("UPDATE episodes SET state=? WHERE id=?", (canonical(state), episode))
                self.db.execute("UPDATE calls SET effect_committed=1 WHERE id=?", (identity,))

    def rows(self, table):
        if table not in ("episodes", "calls", "attempts", "sessions", "annotations", "meta"):
            raise ValueError("explicit table required")
        with self.lock:
            return [dict(r) for r in self.db.execute("SELECT * FROM " + table)]

    def backup(self, destination):
        with self.lock, closing(sqlite3.connect(destination)) as target:
            self.db.backup(target)
            target.execute("PRAGMA journal_mode=DELETE")
            if target.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("backup integrity failed")

    def close(self):
        self.db.close()


class Admission:
    """One controller lock serializes admission across both canonical writers."""
    def __init__(self, stores, limit=500, contingency=28):
        self.stores, self.limit, self.contingency = stores, limit, contingency
        self.lock = threading.RLock()

    def usage(self):
        attempts = [r for store in self.stores for r in store.rows("attempts")]
        gap = self.stores[0].meta("lost_spending", {"upper": 0, "resolved": True})
        extra = gap.get("upper") if gap.get("resolved") else None
        return dict(attempts=len(attempts), in_flight=sum(r["status"] == "admitted" for r in attempts),
                    contingency=sum(r["contingency"] for r in attempts) + (extra or 0),
                    lost_spending=gap, remaining=None if extra is None else self.limit - len(attempts) - extra)

    def admit(self, store, call_id, stage, *, contingency=False):
        with self.lock:
            usage = self.usage()
            if usage["remaining"] is None or usage["remaining"] <= 0:
                raise ValueError("whole-study allowance exhausted or lost spending unresolved")
            rows = [r for r in store.rows("attempts") if r["call_id"] == call_id]
            if store.call(call_id)["outcome"] is not None:
                raise ValueError("completed call cannot regenerate")
            if rows and (len(rows) >= 2 or rows[-1]["status"] != "interrupted_confirmed"):
                raise ValueError("unresolved attempt or retry allowance exhausted")
            contingency = bool(contingency or rows)
            if contingency and usage["contingency"] >= self.contingency:
                raise ValueError("28-attempt contingency exhausted")
            ceilings = {"main": 380, "pilot": 60, "direct": 12, "thinking": 12, "hardware": 8}
            first = sum(r["stage"] == stage and not r["contingency"] for s in self.stores for r in s.rows("attempts"))
            if not contingency and (stage not in ceilings or first >= ceilings[stage]):
                raise ValueError("stage first-attempt ceiling exhausted")
            with store.transaction():
                cur = store.db.execute("INSERT INTO attempts(call_id,number,stage,contingency,admitted_at,status) VALUES (?,?,?,?,?,?)",
                                       (call_id, len(rows)+1, stage, int(contingency), utc(), "admitted"))
            return cur.lastrowid

    def reconcile(self, store, attempt, evidence):
        if not evidence.get("termination_confirmed") or not evidence.get("reason"):
            raise ValueError("prior process exit and reason are required")
        with self.lock, store.transaction():
            row = store.db.execute("SELECT * FROM attempts WHERE id=?", (attempt,)).fetchone()
            if row is None or row["status"] != "admitted" or store.call(row["call_id"])["outcome"]:
                raise ValueError("only an admitted call lacking raw output may be reconciled")
            store.db.execute("UPDATE attempts SET status='interrupted_confirmed',finished_at=?,evidence=? WHERE id=?",
                             (utc(), canonical(evidence), attempt))
