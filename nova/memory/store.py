from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3
import time
from typing import Any
from nova.security.secrets import redact, looks_secret


@dataclass(slots=True)
class Memory:
    id: int
    kind: str
    text: str
    tags: str
    created_at: float
    score: float = 0.0


class MemoryStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init(self) -> None:
        with self._conn() as con:
            con.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                text TEXT NOT NULL,
                tags TEXT DEFAULT '',
                created_at REAL NOT NULL,
                deleted INTEGER DEFAULT 0
            )
            """)
            con.execute("CREATE INDEX IF NOT EXISTS idx_mem_kind ON memories(kind)")
            con.execute("CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(text, tags, content='memories', content_rowid='id')")
            # Rebuild trigger-like consistency with simple insert/delete maintenance in code.

    def add(self, text: str, kind: str = "note", tags: list[str] | None = None) -> int:
        clean = redact(text)
        if looks_secret(text):
            clean += " [NOVA: possible secret redacted]"
        tag_text = ",".join(tags or [])
        with self._conn() as con:
            cur = con.execute("INSERT INTO memories(kind,text,tags,created_at) VALUES(?,?,?,?)", (kind, clean, tag_text, time.time()))
            mid = int(cur.lastrowid)
            con.execute("INSERT INTO memories_fts(rowid,text,tags) VALUES(?,?,?)", (mid, clean, tag_text))
            return mid

    def search(self, query: str, limit: int = 10) -> list[Memory]:
        with self._conn() as con:
            try:
                rows = con.execute(
                    """SELECT m.id,m.kind,m.text,m.tags,m.created_at,bm25(memories_fts) AS score
                       FROM memories_fts JOIN memories m ON m.id=memories_fts.rowid
                       WHERE memories_fts MATCH ? AND m.deleted=0
                       ORDER BY score LIMIT ?""",
                    (query, limit),
                ).fetchall()
            except sqlite3.OperationalError:
                like = f"%{query}%"
                rows = con.execute(
                    "SELECT id,kind,text,tags,created_at,0.0 FROM memories WHERE deleted=0 AND (text LIKE ? OR tags LIKE ?) ORDER BY created_at DESC LIMIT ?",
                    (like, like, limit),
                ).fetchall()
        return [Memory(*row) for row in rows]

    def list(self, limit: int = 50) -> list[Memory]:
        with self._conn() as con:
            rows = con.execute("SELECT id,kind,text,tags,created_at,0.0 FROM memories WHERE deleted=0 ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
        return [Memory(*row) for row in rows]

    def delete(self, memory_id: int) -> bool:
        with self._conn() as con:
            cur = con.execute("UPDATE memories SET deleted=1 WHERE id=?", (memory_id,))
            con.execute("DELETE FROM memories_fts WHERE rowid=?", (memory_id,))
            return cur.rowcount > 0

    def export_markdown(self) -> str:
        rows = self.list(limit=10000)
        lines = ["# NOVA Memory Export", ""]
        for m in rows:
            lines.append(f"## #{m.id} {m.kind}")
            lines.append(f"Tags: {m.tags or '-'}")
            lines.append("")
            lines.append(m.text)
            lines.append("")
        return "\n".join(lines)
