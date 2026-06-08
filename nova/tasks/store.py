from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3, time

@dataclass(slots=True)
class Task:
    id: int
    title: str
    due: str | None
    status: str
    created_at: float

class TaskStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _conn(self): return sqlite3.connect(self.db_path)

    def _init(self) -> None:
        with self._conn() as con:
            con.execute("""CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, due TEXT, status TEXT NOT NULL, created_at REAL NOT NULL
            )""")

    def add(self, title: str, due: str | None = None) -> int:
        with self._conn() as con:
            cur = con.execute("INSERT INTO tasks(title,due,status,created_at) VALUES(?,?,?,?)", (title, due, "open", time.time()))
            return int(cur.lastrowid)

    def list(self, status: str | None = None) -> list[Task]:
        with self._conn() as con:
            if status:
                rows = con.execute("SELECT id,title,due,status,created_at FROM tasks WHERE status=? ORDER BY COALESCE(due,''), created_at DESC", (status,)).fetchall()
            else:
                rows = con.execute("SELECT id,title,due,status,created_at FROM tasks ORDER BY status, COALESCE(due,''), created_at DESC").fetchall()
        return [Task(*r) for r in rows]

    def set_status(self, task_id: int, status: str) -> bool:
        with self._conn() as con:
            cur = con.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
            return cur.rowcount > 0
