from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json
from .time import utc_now
from nova.security.redaction import redact_secrets

@dataclass(slots=True)
class AuditEvent:
    event_type: str
    message: str
    actor: str = "user"
    risk: str = "low"
    metadata: dict | None = None
    created_at: str = ""

    def to_json(self) -> str:
        data = asdict(self)
        data["created_at"] = self.created_at or utc_now()
        data["message"] = redact_secrets(data["message"])
        if data.get("metadata"):
            data["metadata"] = json.loads(redact_secrets(json.dumps(data["metadata"], default=str)))
        return json.dumps(data, ensure_ascii=False)

class AuditLog:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: AuditEvent) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(event.to_json() + "\n")

    def tail(self, limit: int = 50) -> list[dict]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8", errors="ignore").splitlines()[-limit:]
        out: list[dict] = []
        for line in lines:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return out
