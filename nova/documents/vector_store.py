from __future__ import annotations

import json
import math
import sqlite3
import time
from pathlib import Path
from typing import Any

from .models import Chunk


def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    denom = math.sqrt(sum(x*x for x in a)) * math.sqrt(sum(y*y for y in b))
    if denom == 0:
        return 0.0
    return sum(x*y for x, y in zip(a, b)) / denom


class VectorStore:
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
                CREATE TABLE IF NOT EXISTS indexed_files (
                    path TEXT PRIMARY KEY,
                    mtime REAL NOT NULL,
                    size INTEGER NOT NULL,
                    chunks INTEGER NOT NULL,
                    metadata TEXT NOT NULL DEFAULT '{}',
                    indexed_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    source_path TEXT NOT NULL,
                    text TEXT NOT NULL,
                    start INTEGER NOT NULL,
                    end INTEGER NOT NULL,
                    metadata TEXT NOT NULL DEFAULT '{}',
                    embedding TEXT NOT NULL,
                    created_at REAL NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_chunks_source ON chunks(source_path);
                """
            )

    def upsert_file(self, path: Path, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        stat = path.stat()
        with self.connect() as conn:
            conn.execute("DELETE FROM chunks WHERE source_path=?", (str(path),))
            for chunk, emb in zip(chunks, embeddings):
                conn.execute(
                    "INSERT OR REPLACE INTO chunks(id, source_path, text, start, end, metadata, embedding, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (chunk.id, str(chunk.source_path), chunk.text, chunk.start, chunk.end, json.dumps(chunk.metadata), json.dumps(emb), time.time()),
                )
            conn.execute(
                "INSERT OR REPLACE INTO indexed_files(path, mtime, size, chunks, metadata, indexed_at) VALUES (?, ?, ?, ?, ?, ?)",
                (str(path), stat.st_mtime, stat.st_size, len(chunks), json.dumps(chunks[0].metadata if chunks else {}), time.time()),
            )

    def is_current(self, path: Path) -> bool:
        if not path.exists():
            return False
        stat = path.stat()
        with self.connect() as conn:
            row = conn.execute("SELECT mtime, size FROM indexed_files WHERE path=?", (str(path),)).fetchone()
        return bool(row and float(row["mtime"]) == stat.st_mtime and int(row["size"]) == stat.st_size)

    def search(self, query_embedding: list[float], limit: int = 6) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM chunks").fetchall()
        scored: list[tuple[float, dict[str, Any]]] = []
        for row in rows:
            emb = json.loads(row["embedding"])
            score = cosine(query_embedding, emb)
            if score > 0:
                item = dict(row)
                item["metadata"] = json.loads(item.get("metadata") or "{}")
                item["score"] = score
                item.pop("embedding", None)
                scored.append((score, item))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [item for _, item in scored[:limit]]

    def stats(self) -> dict[str, Any]:
        with self.connect() as conn:
            files = conn.execute("SELECT COUNT(*) FROM indexed_files").fetchone()[0]
            chunks = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        return {"indexed_files": files, "chunks": chunks}
