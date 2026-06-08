from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json, time

@dataclass(slots=True)
class IndexedSource:
    path: str
    chunks: int
    indexed_at: float
    index_name: str

class SourceRegistry:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists(): path.write_text("[]", encoding="utf-8")

    def list(self) -> list[IndexedSource]:
        return [IndexedSource(**x) for x in json.loads(self.path.read_text(encoding="utf-8"))]

    def record(self, source_path: str, chunks: int, index_name: str = "default") -> None:
        current = [x for x in self.list() if not (x.path == source_path and x.index_name == index_name)]
        current.append(IndexedSource(source_path, chunks, time.time(), index_name))
        self.path.write_text(json.dumps([asdict(x) for x in current], indent=2), encoding="utf-8")

    def remove(self, source_path: str, index_name: str = "default") -> int:
        current = self.list()
        filtered = [x for x in current if not (x.path == source_path and x.index_name == index_name)]
        self.path.write_text(json.dumps([asdict(x) for x in filtered], indent=2), encoding="utf-8")
        return len(current) - len(filtered)
