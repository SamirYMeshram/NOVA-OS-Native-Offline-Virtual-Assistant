from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from nova.core.paths import nova_home


@dataclass(slots=True)
class FileOperation:
    action: str
    source: str
    destination: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class UndoLog:
    id: str
    operations: list[FileOperation]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class UndoLogStore:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or nova_home() / "undo"
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, operations: list[FileOperation]) -> Path:
        log = UndoLog(id=datetime.now(timezone.utc).strftime("undo-%Y%m%d-%H%M%S"), operations=operations)
        path = self.root / f"{log.id}.json"
        path.write_text(json.dumps(asdict(log), indent=2), encoding="utf-8")
        return path

    def list_logs(self) -> list[Path]:
        return sorted(self.root.glob("undo-*.json"), reverse=True)
