from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import sqlite3, time, datetime as dt

@dataclass(slots=True)
class Reminder:
    id: int
    title: str
    remind_at: str
    status: str
    created_at: float

class ReminderStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _conn(self): return sqlite3.connect(self.db_path)

    def _init(self) -> None:
        with self._conn() as con:
            con.execute("""CREATE TABLE IF NOT EXISTS reminders(
                id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, remind_at TEXT NOT NULL, status TEXT NOT NULL, created_at REAL NOT NULL
            )""")

    def add(self, title: str, remind_at: str) -> int:
        # validate ISO-ish date/time
        try:
            dt.datetime.fromisoformat(remind_at.replace('Z','+00:00'))
        except Exception as exc:
            raise ValueError("remind_at must be ISO format like 2026-06-10T09:00:00") from exc
        with self._conn() as con:
            cur = con.execute("INSERT INTO reminders(title,remind_at,status,created_at) VALUES(?,?,?,?)", (title, remind_at, "open", time.time()))
            return int(cur.lastrowid)

    def due(self, now_iso: str | None = None) -> list[Reminder]:
        now_iso = now_iso or dt.datetime.now().isoformat(timespec="seconds")
        with self._conn() as con:
            rows = con.execute("SELECT id,title,remind_at,status,created_at FROM reminders WHERE status='open' AND remind_at <= ? ORDER BY remind_at", (now_iso,)).fetchall()
        return [Reminder(*r) for r in rows]

    def list(self) -> list[Reminder]:
        with self._conn() as con:
            rows = con.execute("SELECT id,title,remind_at,status,created_at FROM reminders ORDER BY remind_at").fetchall()
        return [Reminder(*r) for r in rows]

    def complete(self, reminder_id: int) -> bool:
        with self._conn() as con:
            cur = con.execute("UPDATE reminders SET status='done' WHERE id=?", (reminder_id,))
            return cur.rowcount > 0
