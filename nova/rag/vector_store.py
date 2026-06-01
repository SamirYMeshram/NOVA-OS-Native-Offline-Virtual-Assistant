from __future__ import annotations
import json
from nova.core.sqlite import SQLite
from nova.ai.embeddings import HashEmbedding
from .models import DocumentChunk, SearchHit

class VectorStore:
    def __init__(self, db: SQLite | None = None, embedder: HashEmbedding | None = None):
        self.db = db or SQLite()
        self.embedder = embedder or HashEmbedding()
        self.init()

    def init(self):
        with self.db.connect() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS doc_chunks(
                id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT NOT NULL, chunk_index INTEGER NOT NULL,
                text TEXT NOT NULL, embedding TEXT NOT NULL, start_char INTEGER DEFAULT 0, end_char INTEGER DEFAULT 0, metadata TEXT DEFAULT '')""")
            c.execute("CREATE INDEX IF NOT EXISTS idx_doc_path ON doc_chunks(path)")

    def clear_path(self, path: str):
        with self.db.connect() as c:
            c.execute("DELETE FROM doc_chunks WHERE path=?", (path,))

    def add_chunks(self, chunks: list[DocumentChunk]):
        with self.db.connect() as c:
            for chunk in chunks:
                emb = json.dumps(self.embedder.embed(chunk.text))
                c.execute("INSERT INTO doc_chunks(path,chunk_index,text,embedding,start_char,end_char,metadata) VALUES(?,?,?,?,?,?,?)", (chunk.path, chunk.chunk_index, chunk.text, emb, chunk.start_char, chunk.end_char, chunk.metadata))

    def search(self, query: str, limit: int = 6) -> list[SearchHit]:
        q = self.embedder.embed(query)
        with self.db.connect() as c:
            rows = c.execute("SELECT path,chunk_index,text,embedding FROM doc_chunks").fetchall()
        scored = []
        for r in rows:
            try:
                emb = json.loads(r['embedding'])
                score = self.embedder.cosine(q, emb)
            except Exception:
                score = 0.0
            if score > 0:
                scored.append(SearchHit(r['path'], int(r['chunk_index']), r['text'], float(score)))
        scored.sort(key=lambda h: h.score, reverse=True)
        return scored[:limit]
