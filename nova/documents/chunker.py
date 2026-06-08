from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True)
class Chunk:
    id: str
    source: str
    index: int
    text: str
    start: int
    end: int


def chunk_text(text: str, source: str, chunk_size: int = 900, overlap: int = 150) -> list[Chunk]:
    clean = text.replace("\r\n", "\n")
    chunks: list[Chunk] = []
    i = 0
    idx = 0
    while i < len(clean):
        end = min(len(clean), i + chunk_size)
        # prefer paragraph boundary near end
        boundary = clean.rfind("\n\n", i, end)
        if boundary > i + chunk_size // 2:
            end = boundary
        piece = clean[i:end].strip()
        if piece:
            chunks.append(Chunk(f"{Path(source).name}:{idx}", source, idx, piece, i, end))
            idx += 1
        if end >= len(clean):
            break
        i = max(end - overlap, i + 1)
    return chunks
