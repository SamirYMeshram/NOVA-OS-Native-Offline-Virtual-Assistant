from __future__ import annotations
import sqlite3, json
from pathlib import Path
from nova.core.time import utc_now
from nova.security.redaction import looks_like_secret, redact_secrets
from .schema import SCHEMA_SQL
from .models import MemoryItem, TaskItem, ReminderItem

class MemoryStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA_SQL)

    def add(self, kind: str, key: str, value: str, tags: list[str] | None = None, source: str = "user") -> int:
        if looks_like_secret(value):
            value = redact_secrets(value)
            tags = list(tags or []) + ["redacted"]
        now = utc_now()
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO memories(kind,key,value,tags,source,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
                (kind, key, value, ",".join(tags or []), source, now, now),
            )
            return int(cur.lastrowid)

    def search(self, query: str, limit: int = 10) -> list[MemoryItem]:
        with self.connect() as conn:
            try:
                rows = conn.execute(
                    "SELECT m.* FROM memory_fts f JOIN memories m ON m.id=f.rowid WHERE memory_fts MATCH ? LIMIT ?",
                    (query, limit),
                ).fetchall()
            except sqlite3.OperationalError:
                like = f"%{query}%"
                rows = conn.execute(
                    "SELECT * FROM memories WHERE key LIKE ? OR value LIKE ? OR tags LIKE ? ORDER BY id DESC LIMIT ?",
                    (like, like, like, limit),
                ).fetchall()
        return [MemoryItem(**dict(r)) for r in rows]

    def list(self, kind: str | None = None, limit: int = 50) -> list[MemoryItem]:
        with self.connect() as conn:
            if kind:
                rows = conn.execute("SELECT * FROM memories WHERE kind=? ORDER BY id DESC LIMIT ?", (kind, limit)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM memories ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [MemoryItem(**dict(r)) for r in rows]

    def delete(self, memory_id: int) -> bool:
        with self.connect() as conn:
            cur = conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
            return cur.rowcount > 0

    def export_json(self, path: str | Path) -> Path:
        path = Path(path)
        data = [item.__dict__ for item in self.list(limit=100000)]
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return path

    def add_task(self, title: str, description: str = "", due_at: str | None = None) -> int:
        now = utc_now()
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO tasks(title,description,due_at,created_at,updated_at) VALUES(?,?,?,?,?)",
                (title, description, due_at, now, now),
            )
            return int(cur.lastrowid)

    def list_tasks(self, status: str | None = None) -> list[TaskItem]:
        with self.connect() as conn:
            if status:
                rows = conn.execute("SELECT id,title,description,status,due_at FROM tasks WHERE status=? ORDER BY id DESC", (status,)).fetchall()
            else:
                rows = conn.execute("SELECT id,title,description,status,due_at FROM tasks ORDER BY id DESC").fetchall()
        return [TaskItem(**dict(r)) for r in rows]

    def complete_task(self, task_id: int) -> bool:
        with self.connect() as conn:
            cur = conn.execute("UPDATE tasks SET status='done', updated_at=? WHERE id=?", (utc_now(), task_id))
            return cur.rowcount > 0

    def add_reminder(self, title: str, remind_at: str) -> int:
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO reminders(title,remind_at,created_at) VALUES(?,?,?)",
                (title, remind_at, utc_now()),
            )
            return int(cur.lastrowid)

    def list_reminders(self, status: str | None = None) -> list[ReminderItem]:
        with self.connect() as conn:
            if status:
                rows = conn.execute("SELECT id,title,remind_at,status FROM reminders WHERE status=? ORDER BY remind_at", (status,)).fetchall()
            else:
                rows = conn.execute("SELECT id,title,remind_at,status FROM reminders ORDER BY remind_at").fetchall()
        return [ReminderItem(**dict(r)) for r in rows]

    def record_command(self, command: str, intent: str, result: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO command_history(command,intent,result,created_at) VALUES(?,?,?,?)",
                (redact_secrets(command), intent, redact_secrets(result), utc_now()),
            )

    def history(self, limit: int = 25) -> list[dict]:
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM command_history ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]
