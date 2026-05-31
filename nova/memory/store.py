from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nova.core.config import AppConfig
from nova.core.paths import nova_home
from nova.core.security import SafetyGuard
from nova.utils.text import cosine_sparse, term_vector


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class MemoryItem:
    id: int
    kind: str
    content: str
    tags: list[str]
    importance: int
    created_at: str
    updated_at: str


class MemoryStore:
    """Local SQLite memory with editable, exportable, searchable records."""

    def __init__(self, db_path: str | Path | None = None, config: AppConfig | None = None) -> None:
        self.config = config or AppConfig()
        self.db_path = Path(db_path or self.config.database_path or nova_home() / "nova.sqlite3")
        self.guard = SafetyGuard(self.config.security)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT NOT NULL DEFAULT '[]',
                    importance INTEGER NOT NULL DEFAULT 3,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    notes TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'open',
                    due_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                    content, kind, tags, content='memories', content_rowid='id'
                )
                """
            )

    def add(self, content: str, kind: str = "note", tags: list[str] | None = None, importance: int = 3) -> int:
        content = content.strip()
        if not content:
            raise ValueError("Memory content cannot be empty")
        content = self.guard.redact_secrets(content)
        now = utc_now()
        tag_json = json.dumps(tags or [])
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO memories(kind, content, tags, importance, created_at, updated_at) VALUES(?,?,?,?,?,?)",
                (kind, content, tag_json, importance, now, now),
            )
            mem_id = int(cur.lastrowid)
            conn.execute(
                "INSERT INTO memories_fts(rowid, content, kind, tags) VALUES(?,?,?,?)",
                (mem_id, content, kind, tag_json),
            )
            return mem_id

    def update(self, memory_id: int, content: str | None = None, tags: list[str] | None = None, importance: int | None = None) -> None:
        current = self.get(memory_id)
        if current is None:
            raise KeyError(f"Memory not found: {memory_id}")
        new_content = self.guard.redact_secrets(content.strip()) if content is not None else current.content
        new_tags = tags if tags is not None else current.tags
        new_importance = importance if importance is not None else current.importance
        tag_json = json.dumps(new_tags)
        now = utc_now()
        with self.connect() as conn:
            conn.execute(
                "UPDATE memories SET content=?, tags=?, importance=?, updated_at=? WHERE id=?",
                (new_content, tag_json, new_importance, now, memory_id),
            )
            conn.execute("DELETE FROM memories_fts WHERE rowid=?", (memory_id,))
            conn.execute(
                "INSERT INTO memories_fts(rowid, content, kind, tags) VALUES(?,?,?,?)",
                (memory_id, new_content, current.kind, tag_json),
            )

    def delete(self, memory_id: int) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
            conn.execute("DELETE FROM memories_fts WHERE rowid=?", (memory_id,))

    def get(self, memory_id: int) -> MemoryItem | None:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM memories WHERE id=?", (memory_id,)).fetchone()
        return self._row_to_memory(row) if row else None

    def list_recent(self, limit: int = 20) -> list[MemoryItem]:
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM memories ORDER BY updated_at DESC LIMIT ?", (limit,)).fetchall()
        return [self._row_to_memory(r) for r in rows]

    def search(self, query: str, limit: int = 8) -> list[MemoryItem]:
        query = query.strip()
        if not query:
            return self.list_recent(limit)
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT m.* FROM memories_fts f
                JOIN memories m ON m.id = f.rowid
                WHERE memories_fts MATCH ?
                ORDER BY bm25(memories_fts)
                LIMIT ?
                """,
                (self._fts_query(query), limit),
            ).fetchall()
        results = [self._row_to_memory(r) for r in rows]
        if results:
            return results
        # fallback semantic-ish sparse scoring when FTS query syntax is too narrow
        all_items = self.list_recent(500)
        qv = term_vector(query)
        scored = [(cosine_sparse(qv, term_vector(item.content)), item) for item in all_items]
        return [item for score, item in sorted(scored, reverse=True, key=lambda x: x[0])[:limit] if score > 0]

    def add_conversation(self, role: str, content: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO conversations(role, content, created_at) VALUES(?,?,?)",
                (role, self.guard.redact_secrets(content), utc_now()),
            )

    def recent_conversation(self, limit: int = 12) -> list[dict[str, str]]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT role, content, created_at FROM conversations ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in reversed(rows)]

    def create_task(self, title: str, notes: str = "", due_at: str | None = None) -> int:
        now = utc_now()
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO tasks(title, notes, due_at, created_at, updated_at) VALUES(?,?,?,?,?)",
                (title.strip(), notes.strip(), due_at, now, now),
            )
            return int(cur.lastrowid)

    def list_tasks(self, status: str | None = None) -> list[dict[str, Any]]:
        with self.connect() as conn:
            if status:
                rows = conn.execute("SELECT * FROM tasks WHERE status=? ORDER BY created_at DESC", (status,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

    def set_task_status(self, task_id: int, status: str) -> None:
        with self.connect() as conn:
            conn.execute("UPDATE tasks SET status=?, updated_at=? WHERE id=?", (status, utc_now(), task_id))

    def export_json(self, path: str | Path) -> Path:
        output = Path(path).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "memories": [asdict(m) for m in self.list_recent(10_000)],
            "tasks": self.list_tasks(),
            "exported_at": utc_now(),
        }
        output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return output

    def _row_to_memory(self, row: sqlite3.Row) -> MemoryItem:
        return MemoryItem(
            id=int(row["id"]),
            kind=row["kind"],
            content=row["content"],
            tags=json.loads(row["tags"] or "[]"),
            importance=int(row["importance"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _fts_query(query: str) -> str:
        terms = [part.replace('"', "") for part in query.split() if part.strip()]
        return " OR ".join(f'"{term}"' for term in terms) or '""'
