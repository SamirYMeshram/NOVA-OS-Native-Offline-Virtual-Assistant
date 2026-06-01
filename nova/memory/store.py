from __future__ import annotations
from datetime import datetime, timezone
import json
from dataclasses import asdict
from nova.core.sqlite import SQLite
from nova.core.redaction import looks_like_secret, redact
from nova.core.text import keyword_score
from .models import MemoryItem

class MemoryStore:
    def __init__(self, db: SQLite | None = None):
        self.db = db or SQLite()
        self.init()

    def init(self) -> None:
        with self.db.connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                text TEXT NOT NULL,
                tags TEXT DEFAULT '',
                importance INTEGER DEFAULT 3,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_kind ON memories(kind)")
            conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(text, tags, content='memories', content_rowid='id')")

    def add(self, text: str, kind: str = "note", tags: str = "", importance: int = 3, *, allow_secret: bool = False) -> int:
        if looks_like_secret(text) and not allow_secret:
            text = redact(text)
        now = datetime.now(timezone.utc).isoformat()
        with self.db.connect() as conn:
            cur = conn.execute("INSERT INTO memories(kind,text,tags,importance,created_at,updated_at) VALUES(?,?,?,?,?,?)", (kind, text, tags, importance, now, now))
            mid = int(cur.lastrowid)
            conn.execute("INSERT INTO memories_fts(rowid,text,tags) VALUES(?,?,?)", (mid, text, tags))
            return mid

    def search(self, query: str, limit: int = 10) -> list[MemoryItem]:
        with self.db.connect() as conn:
            try:
                rows = conn.execute("SELECT m.* FROM memories_fts f JOIN memories m ON m.id=f.rowid WHERE memories_fts MATCH ? LIMIT ?", (query, limit)).fetchall()
            except Exception:
                rows = conn.execute("SELECT * FROM memories").fetchall()
        items = [MemoryItem(**dict(r)) for r in rows]
        if len(items) > limit:
            items = sorted(items, key=lambda i: keyword_score(query, i.text), reverse=True)[:limit]
        return items

    def list(self, kind: str | None = None, limit: int = 50) -> list[MemoryItem]:
        with self.db.connect() as conn:
            if kind:
                rows = conn.execute("SELECT * FROM memories WHERE kind=? ORDER BY id DESC LIMIT ?", (kind, limit)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM memories ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [MemoryItem(**dict(r)) for r in rows]

    def delete(self, memory_id: int) -> bool:
        with self.db.connect() as conn:
            conn.execute("DELETE FROM memories_fts WHERE rowid=?", (memory_id,))
            cur = conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
            return cur.rowcount > 0

    def export_json(self) -> str:
        return json.dumps([asdict(i) for i in self.list(limit=10000)], indent=2, ensure_ascii=False)

    def clear(self) -> None:
        with self.db.connect() as conn:
            conn.execute("DELETE FROM memories_fts")
            conn.execute("DELETE FROM memories")
