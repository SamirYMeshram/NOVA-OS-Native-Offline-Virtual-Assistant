from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class LoadedDocument:
    path: Path
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Chunk:
    id: str
    source_path: Path
    text: str
    start: int
    end: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Citation:
    chunk_id: str
    source_path: str
    preview: str


@dataclass(slots=True)
class QAAnswer:
    answer: str
    citations: list[Citation]
    confidence: float
