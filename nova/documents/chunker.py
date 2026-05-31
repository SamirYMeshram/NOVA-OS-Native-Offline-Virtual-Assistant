from __future__ import annotations
from hashlib import sha1
from .models import Chunk

class TextChunker:
    def __init__(self, chunk_size: int = 1200, overlap: int = 180):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, path: str, text: str, metadata: dict | None = None) -> list[Chunk]:
        chunks: list[Chunk] = []
        if not text.strip():
            return chunks
        start = 0
        idx = 0
        while start < len(text):
            end = min(len(text), start + self.chunk_size)
            snippet = text[start:end].strip()
            if snippet:
                digest = sha1(f"{path}:{idx}:{snippet[:64]}".encode()).hexdigest()[:12]
                chunks.append(Chunk(digest, path, idx, snippet, start, end, metadata or {}))
            if end >= len(text):
                break
            start = max(end - self.overlap, start + 1)
            idx += 1
        return chunks
