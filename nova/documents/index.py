from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from nova.core.paths import nova_home, relative_to_or_name
from nova.documents.chunker import TextChunker
from nova.documents.loaders import DocumentLoader, SUPPORTED_EXTENSIONS
from nova.utils.hashing import sha256_file
from nova.utils.text import SearchHit, cosine_sparse, term_vector


@dataclass(slots=True)
class IndexedFile:
    path: str
    chunks: int
    sha256: str


class DocumentIndex:
    """Local content index using SQLite FTS plus sparse semantic fallback.

    It deliberately works without cloud embedding APIs. If Ollama embeddings are added later,
    the schema can store vectors in a sidecar table without changing the public interface.
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path or nova_home() / "indexes" / "documents.sqlite3")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.loader = DocumentLoader()
        self.chunker = TextChunker()
        self._init_db()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL,
                    root TEXT NOT NULL,
                    extension TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    indexed_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    file_id INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    FOREIGN KEY(file_id) REFERENCES files(id) ON DELETE CASCADE
                )
                """
            )
            conn.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                    text, metadata, content='chunks', content_rowid='rowid'
                )
                """
            )

    def index_path(self, path: str | Path, recursive: bool = True) -> list[IndexedFile]:
        root = Path(path).expanduser().resolve()
        files = list(self._iter_supported_files(root, recursive=recursive))
        indexed: list[IndexedFile] = []
        for file_path in files:
            try:
                indexed.append(self.index_file(file_path, root=root))
            except Exception as exc:
                # Indexing should continue even when one optional loader is unavailable.
                print(f"[NOVA] skipped {file_path}: {exc}")
        return indexed

    def index_file(self, path: str | Path, root: str | Path | None = None) -> IndexedFile:
        file_path = Path(path).expanduser().resolve()
        doc = self.loader.load(file_path)
        root_path = Path(root).expanduser().resolve() if root else file_path.parent
        file_hash = sha256_file(file_path)
        chunks = self.chunker.chunk(doc.text, prefix=relative_to_or_name(file_path, root_path))
        with self.connect() as conn:
            old = conn.execute("SELECT id, sha256 FROM files WHERE path=?", (str(file_path),)).fetchone()
            if old and old["sha256"] == file_hash:
                count = conn.execute("SELECT COUNT(*) c FROM chunks WHERE file_id=?", (old["id"],)).fetchone()["c"]
                return IndexedFile(str(file_path), int(count), file_hash)
            if old:
                rowids = [r["rowid"] for r in conn.execute("SELECT rowid FROM chunks WHERE file_id=?", (old["id"],)).fetchall()]
                for rowid in rowids:
                    conn.execute("DELETE FROM chunks_fts WHERE rowid=?", (rowid,))
                conn.execute("DELETE FROM chunks WHERE file_id=?", (old["id"],))
                conn.execute("DELETE FROM files WHERE id=?", (old["id"],))
            cur = conn.execute(
                "INSERT INTO files(path, root, extension, sha256, size) VALUES(?,?,?,?,?)",
                (str(file_path), str(root_path), file_path.suffix.lower(), file_hash, file_path.stat().st_size),
            )
            file_id = int(cur.lastrowid)
            for chunk in chunks:
                meta = {
                    "path": str(file_path),
                    "source": relative_to_or_name(file_path, root_path),
                    "chunk_id": chunk.chunk_id,
                    "start_char": str(chunk.start_char),
                    "end_char": str(chunk.end_char),
                }
                conn.execute(
                    "INSERT INTO chunks(id, file_id, text, metadata) VALUES(?,?,?,?)",
                    (chunk.chunk_id, file_id, chunk.text, json.dumps(meta, ensure_ascii=False)),
                )
                rowid = conn.execute("SELECT rowid FROM chunks WHERE id=?", (chunk.chunk_id,)).fetchone()["rowid"]
                conn.execute(
                    "INSERT INTO chunks_fts(rowid, text, metadata) VALUES(?,?,?)",
                    (rowid, chunk.text, json.dumps(meta, ensure_ascii=False)),
                )
        return IndexedFile(str(file_path), len(chunks), file_hash)

    def search(self, query: str, limit: int = 8) -> list[SearchHit]:
        query = query.strip()
        if not query:
            return []
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT c.id, c.text, c.metadata, bm25(chunks_fts) AS rank
                FROM chunks_fts
                JOIN chunks c ON c.rowid = chunks_fts.rowid
                WHERE chunks_fts MATCH ?
                ORDER BY rank
                LIMIT ?
                """,
                (self._fts_query(query), limit),
            ).fetchall()
        hits = [
            SearchHit(id=r["id"], score=float(-r["rank"]), text=r["text"], metadata=json.loads(r["metadata"]))
            for r in rows
        ]
        if hits:
            return hits
        return self._sparse_search(query, limit=limit)

    def stats(self) -> dict[str, int]:
        with self.connect() as conn:
            files = conn.execute("SELECT COUNT(*) c FROM files").fetchone()["c"]
            chunks = conn.execute("SELECT COUNT(*) c FROM chunks").fetchone()["c"]
        return {"files": int(files), "chunks": int(chunks)}

    def _sparse_search(self, query: str, limit: int) -> list[SearchHit]:
        qv = term_vector(query)
        with self.connect() as conn:
            rows = conn.execute("SELECT id, text, metadata FROM chunks LIMIT 5000").fetchall()
        scored: list[SearchHit] = []
        for row in rows:
            score = cosine_sparse(qv, term_vector(row["text"]))
            if score > 0:
                scored.append(SearchHit(row["id"], score, row["text"], json.loads(row["metadata"])))
        return sorted(scored, key=lambda h: h.score, reverse=True)[:limit]

    @staticmethod
    def _fts_query(query: str) -> str:
        terms = [term.replace('"', "") for term in query.split() if term.strip()]
        return " OR ".join(f'"{term}"' for term in terms) or '""'

    def _iter_supported_files(self, root: Path, recursive: bool) -> Iterable[Path]:
        if root.is_file():
            if root.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield root
            return
        iterator = root.rglob("*") if recursive else root.glob("*")
        for path in iterator:
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield path
