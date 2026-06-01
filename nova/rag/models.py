from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class DocumentChunk:
    id: int | None
    path: str
    chunk_index: int
    text: str
    start_char: int = 0
    end_char: int = 0
    metadata: str = ""

@dataclass(slots=True)
class SearchHit:
    path: str
    chunk_index: int
    text: str
    score: float
