from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import nova_home


@dataclass(slots=True)
class AuditEvent:
    action: str
    status: str
    detail: str
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AuditLog:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or nova_home() / "logs" / "audit.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: AuditEvent) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")

    def tail(self, limit: int = 50) -> list[AuditEvent]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8", errors="ignore").splitlines()[-limit:]
        events: list[AuditEvent] = []
        for line in lines:
            try:
                events.append(AuditEvent(**json.loads(line)))
            except Exception:
                continue
        return events
