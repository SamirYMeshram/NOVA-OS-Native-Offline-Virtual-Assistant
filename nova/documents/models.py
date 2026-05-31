from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

@dataclass(slots=True)
class Document:
    path: Path
    text: str
    metadata: dict = field(default_factory=dict)

@dataclass(slots=True)
class Chunk:
    id: str
    document_path: str
    index: int
    text: str
    start: int
    end: int
    metadata: dict = field(default_factory=dict)

@dataclass(slots=True)
class SearchHit:
    chunk: Chunk
    score: float

@dataclass(slots=True)
class Answer:
    answer: str
    citations: list[str]
    confidence: float
