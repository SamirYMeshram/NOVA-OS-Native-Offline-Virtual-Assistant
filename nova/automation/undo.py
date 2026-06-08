from __future__ import annotations

from pathlib import Path
import json, time
from dataclasses import dataclass, asdict

@dataclass(slots=True)
class UndoEntry:
    action: str
    source: str
    destination: str | None = None

class UndoManifest:
    def __init__(self, entries: list[UndoEntry] | None = None) -> None:
        self.entries = entries or []
        self.created_at = time.time()

    def add(self, action: str, source: str, destination: str | None = None) -> None:
        self.entries.append(UndoEntry(action, source, destination))

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps({"created_at": self.created_at, "entries": [asdict(e) for e in self.entries]}, indent=2), encoding="utf-8")
