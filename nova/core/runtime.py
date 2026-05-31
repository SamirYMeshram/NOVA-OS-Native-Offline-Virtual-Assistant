from __future__ import annotations
from dataclasses import dataclass, field
from .config import NovaConfig, load_config
from .audit import AuditLog
from .events import EventBus
from .logging import setup_logging

@dataclass
class Runtime:
    config: NovaConfig = field(default_factory=load_config)
    event_bus: EventBus = field(default_factory=EventBus)

    def __post_init__(self) -> None:
        self.config.prepare()
        self.logger = setup_logging(self.config.data_dir / "logs")
        self.audit = AuditLog(self.config.data_dir / "logs" / "audit.jsonl")

_runtime: Runtime | None = None

def get_runtime() -> Runtime:
    global _runtime
    if _runtime is None:
        _runtime = Runtime()
    return _runtime
