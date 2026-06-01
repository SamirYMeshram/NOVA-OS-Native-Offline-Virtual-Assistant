from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from nova.core.sqlite import SQLite

@dataclass(slots=True)
class Task:
    id: int | None
    title: str
    status: str = "open"
    due_at: str = ""
    project: str = ""
    created_at: str = ""

class TaskStore:
    def __init__(self, db: SQLite | None = None):
        self.db = db or SQLite()
        self.init()

    def init(self):
        with self.db.connect() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, status TEXT NOT NULL,
                due_at TEXT DEFAULT '', project TEXT DEFAULT '', created_at TEXT NOT NULL)""")

    def add(self, title: str, due_at: str = "", project: str = "") -> int:
        now = datetime.now(timezone.utc).isoformat()
        with self.db.connect() as c:
            cur = c.execute("INSERT INTO tasks(title,status,due_at,project,created_at) VALUES(?,?,?,?,?)", (title, "open", due_at, project, now))
            return int(cur.lastrowid)

    def list(self, status: str | None = None) -> list[Task]:
        with self.db.connect() as c:
            rows = c.execute("SELECT * FROM tasks WHERE status=? ORDER BY id DESC", (status,)).fetchall() if status else c.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
        return [Task(**dict(r)) for r in rows]

    def complete(self, task_id: int) -> bool:
        with self.db.connect() as c:
            cur = c.execute("UPDATE tasks SET status=? WHERE id=?", ("done", task_id))
            return cur.rowcount > 0
