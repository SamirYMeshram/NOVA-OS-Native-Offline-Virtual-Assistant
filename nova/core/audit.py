from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .redaction import redact
from ..paths import NovaPaths


@dataclass(slots=True)
class AuditEvent:
    event_type: str
    actor: str = "user"
    message: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class AuditLog:
    def __init__(self, path: Path | None = None, redact_secrets: bool = True) -> None:
        self.path = path or (NovaPaths.create().logs / "audit.jsonl")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.redact_secrets = redact_secrets

    def record(self, event: AuditEvent) -> None:
        payload = asdict(event)
        if self.redact_secrets:
            payload = json.loads(redact(json.dumps(payload, default=str)))
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")

    def tail(self, limit: int = 50) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").splitlines()[-limit:]
        return [json.loads(line) for line in lines if line.strip()]
