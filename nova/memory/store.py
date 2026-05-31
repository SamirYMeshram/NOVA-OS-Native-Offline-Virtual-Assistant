from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any


class MemoryStore:
    """Local SQLite memory with editable, searchable user memories, tasks, and command history."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    kind TEXT NOT NULL DEFAULT 'fact',
                    tags TEXT NOT NULL DEFAULT '[]',
                    importance REAL NOT NULL DEFAULT 0.5,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    expires_at REAL,
                    source TEXT,
                    is_deleted INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    notes TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'open',
                    due_at TEXT,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    metadata TEXT NOT NULL DEFAULT '{}'
                );
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT NOT NULL,
                    intent TEXT,
                    success INTEGER NOT NULL,
                    created_at REAL NOT NULL,
                    metadata TEXT NOT NULL DEFAULT '{}'
                );
                """
            )
            try:
                conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(content, kind, tags, content='memories', content_rowid='id')")
                conn.executescript(
                    """
                    CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                        INSERT INTO memories_fts(rowid, content, kind, tags) VALUES (new.id, new.content, new.kind, new.tags);
                    END;
                    CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                        INSERT INTO memories_fts(memories_fts, rowid, content, kind, tags) VALUES('delete', old.id, old.content, old.kind, old.tags);
                    END;
                    CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
                        INSERT INTO memories_fts(memories_fts, rowid, content, kind, tags) VALUES('delete', old.id, old.content, old.kind, old.tags);
                        INSERT INTO memories_fts(rowid, content, kind, tags) VALUES (new.id, new.content, new.kind, new.tags);
                    END;
                    """
                )
            except sqlite3.OperationalError:
                # FTS5 is optional; LIKE search still works.
                pass

    def add_memory(self, content: str, kind: str = "fact", tags: list[str] | None = None, importance: float = 0.5, source: str | None = None) -> dict[str, Any]:
        now = time.time()
        tags = tags or []
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO memories(content, kind, tags, importance, created_at, updated_at, source) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (content.strip(), kind, json.dumps(tags), float(importance), now, now, source),
            )
            memory_id = int(cur.lastrowid)
        return self.get_memory(memory_id) or {"id": memory_id, "content": content}

    def get_memory(self, memory_id: int) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM memories WHERE id=? AND is_deleted=0", (memory_id,)).fetchone()
            return self._row(row) if row else None

    def search(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        query = query.strip()
        if not query:
            sql = "SELECT * FROM memories WHERE is_deleted=0 ORDER BY importance DESC, updated_at DESC LIMIT ?"
            with self.connect() as conn:
                return [self._row(r) for r in conn.execute(sql, (limit,)).fetchall()]
        with self.connect() as conn:
            try:
                rows = conn.execute(
                    "SELECT m.* FROM memories_fts f JOIN memories m ON f.rowid=m.id WHERE memories_fts MATCH ? AND m.is_deleted=0 ORDER BY rank LIMIT ?",
                    (query, limit),
                ).fetchall()
                if rows:
                    return [self._row(r) for r in rows]
            except sqlite3.OperationalError:
                pass
            like = f"%{query}%"
            rows = conn.execute(
                "SELECT * FROM memories WHERE is_deleted=0 AND (content LIKE ? OR tags LIKE ? OR kind LIKE ?) ORDER BY importance DESC, updated_at DESC LIMIT ?",
                (like, like, like, limit),
            ).fetchall()
            return [self._row(r) for r in rows]

    def update_memory(self, memory_id: int, content: str | None = None, tags: list[str] | None = None, importance: float | None = None) -> bool:
        existing = self.get_memory(memory_id)
        if not existing:
            return False
        new_content = content if content is not None else existing["content"]
        new_tags = tags if tags is not None else existing["tags"]
        new_importance = importance if importance is not None else existing["importance"]
        with self.connect() as conn:
            conn.execute("UPDATE memories SET content=?, tags=?, importance=?, updated_at=? WHERE id=?", (new_content, json.dumps(new_tags), new_importance, time.time(), memory_id))
        return True

    def delete_memory(self, memory_id: int) -> bool:
        with self.connect() as conn:
            cur = conn.execute("UPDATE memories SET is_deleted=1, updated_at=? WHERE id=?", (time.time(), memory_id))
            return cur.rowcount > 0

    def export_json(self, path: str | Path) -> Path:
        path = Path(path)
        data = {"memories": self.search("", limit=10_000), "tasks": self.list_tasks(limit=10_000)}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def add_task(self, title: str, notes: str = "", due_at: str | None = None) -> dict[str, Any]:
        now = time.time()
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO tasks(title, notes, due_at, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (title, notes, due_at, now, now),
            )
            task_id = int(cur.lastrowid)
        return self.get_task(task_id) or {"id": task_id, "title": title}

    def get_task(self, task_id: int) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
            return dict(row) if row else None

    def list_tasks(self, status: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        with self.connect() as conn:
            if status:
                rows = conn.execute("SELECT * FROM tasks WHERE status=? ORDER BY created_at DESC LIMIT ?", (status, limit)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
            return [dict(r) for r in rows]

    def log_conversation(self, role: str, content: str, metadata: dict[str, Any] | None = None) -> None:
        with self.connect() as conn:
            conn.execute("INSERT INTO conversations(role, content, created_at, metadata) VALUES (?, ?, ?, ?)", (role, content, time.time(), json.dumps(metadata or {})))

    def recent_conversation(self, limit: int = 20) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM conversations ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
            return [dict(r) for r in reversed(rows)]

    def _row(self, row: sqlite3.Row) -> dict[str, Any]:
        data = dict(row)
        data["tags"] = json.loads(data.get("tags") or "[]")
        return data
