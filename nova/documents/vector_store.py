from __future__ import annotations
import json, sqlite3
from pathlib import Path
from nova.documents.models import Chunk, SearchHit
from nova.documents.similarity import cosine

SCHEMA = """
CREATE TABLE IF NOT EXISTS chunks (
  id TEXT PRIMARY KEY,
  document_path TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  text TEXT NOT NULL,
  start INTEGER NOT NULL,
  end INTEGER NOT NULL,
  metadata TEXT NOT NULL,
  embedding TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_chunks_document_path ON chunks(document_path);
"""

class VectorStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            conn.executescript(SCHEMA)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def upsert(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        with self.connect() as conn:
            for chunk, emb in zip(chunks, embeddings):
                conn.execute(
                    """INSERT OR REPLACE INTO chunks(id,document_path,chunk_index,text,start,end,metadata,embedding)
                    VALUES(?,?,?,?,?,?,?,?)""",
                    (chunk.id, chunk.document_path, chunk.index, chunk.text, chunk.start, chunk.end, json.dumps(chunk.metadata), json.dumps(emb)),
                )

    def count(self) -> int:
        with self.connect() as conn:
            return int(conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0])

    def documents(self) -> list[str]:
        with self.connect() as conn:
            rows = conn.execute("SELECT DISTINCT document_path FROM chunks ORDER BY document_path").fetchall()
        return [r[0] for r in rows]

    def search(self, query_embedding: list[float], limit: int = 5) -> list[SearchHit]:
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM chunks").fetchall()
        hits: list[SearchHit] = []
        for r in rows:
            emb = json.loads(r['embedding'])
            chunk = Chunk(
                id=r['id'], document_path=r['document_path'], index=r['chunk_index'], text=r['text'],
                start=r['start'], end=r['end'], metadata=json.loads(r['metadata'])
            )
            hits.append(SearchHit(chunk, cosine(query_embedding, emb)))
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:limit]
