from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..paths import NovaPaths


@dataclass(slots=True)
class Reminder:
    id: int
    title: str
    remind_at: str
    status: str


class ReminderStore:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path) if db_path else NovaPaths.create().database
        self._init()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self) -> None:
        with self.connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS reminders(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, remind_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open', created_at REAL NOT NULL)"
            )

    def add(self, title: str, remind_at: str) -> dict[str, Any]:
        with self.connect() as conn:
            cur = conn.execute("INSERT INTO reminders(title, remind_at, created_at) VALUES (?, ?, ?)", (title, remind_at, time.time()))
            rid = cur.lastrowid
        return self.get(int(rid)) or {"id": rid, "title": title, "remind_at": remind_at}

    def get(self, reminder_id: int) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM reminders WHERE id=?", (reminder_id,)).fetchone()
            return dict(row) if row else None

    def list(self, status: str | None = None) -> list[dict[str, Any]]:
        with self.connect() as conn:
            if status:
                rows = conn.execute("SELECT * FROM reminders WHERE status=? ORDER BY remind_at", (status,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM reminders ORDER BY remind_at").fetchall()
        return [dict(r) for r in rows]
