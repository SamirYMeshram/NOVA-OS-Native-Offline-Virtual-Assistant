from __future__ import annotations
from dataclasses import dataclass
from .config import NovaConfig
from .audit import AuditLog
from .events import EventBus
from .status import StatusService

@dataclass(slots=True)
class NovaApp:
    config: NovaConfig
    audit: AuditLog
    events: EventBus
    status: StatusService

    @classmethod
    def bootstrap(cls) -> "NovaApp":
        return cls(config=NovaConfig.load(), audit=AuditLog(), events=EventBus(), status=StatusService())
