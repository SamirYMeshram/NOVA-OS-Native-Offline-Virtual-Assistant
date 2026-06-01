from __future__ import annotations
from nova.core.text import chunk_text
from .models import DocumentChunk

def chunk_document(path: str, text: str, size: int = 1200, overlap: int = 180) -> list[DocumentChunk]:
    chunks = []
    pos = 0
    for idx, chunk in enumerate(chunk_text(text, size=size, overlap=overlap)):
        start = text.find(chunk[:40], pos) if chunk else pos
        if start < 0:
            start = pos
        end = start + len(chunk)
        chunks.append(DocumentChunk(None, path, idx, chunk, start, end))
        pos = max(pos, end - overlap)
    return chunks
