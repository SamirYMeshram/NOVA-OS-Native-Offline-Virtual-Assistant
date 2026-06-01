from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
from .paths import logs_dir
from .redaction import redact

@dataclass(slots=True)
class AuditEvent:
    action: str
    outcome: str
    details: dict
    ts: str

class AuditLog:
    def __init__(self, path: Path | None = None):
        self.path = path or logs_dir() / "audit.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, action: str, outcome: str, **details):
        safe_details = json.loads(redact(json.dumps(details, default=str)))
        event = AuditEvent(action=action, outcome=outcome, details=safe_details, ts=datetime.now(timezone.utc).isoformat())
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")

    def tail(self, limit: int = 50) -> list[dict]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8", errors="ignore").splitlines()[-limit:]
        return [json.loads(x) for x in lines if x.strip()]
