from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class MemoryItem:
    id: int | None
    kind: str
    text: str
    tags: str = ""
    importance: int = 3
    created_at: str = ""
    updated_at: str = ""
