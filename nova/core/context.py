from __future__ import annotations

from dataclasses import dataclass

from ..config import NovaConfig
from ..paths import NovaPaths
from .audit import AuditLog
from .router import CommandRouter
from .safety import SafetyGuard


@dataclass(slots=True)
class AppContext:
    paths: NovaPaths
    config: NovaConfig
    audit: AuditLog
    safety: SafetyGuard
    router: CommandRouter

    @classmethod
    def create(cls) -> "AppContext":
        paths = NovaPaths.create()
        config = NovaConfig.load(paths)
        return cls(
            paths=paths,
            config=config,
            audit=AuditLog(paths.logs / "audit.jsonl", redact_secrets=config.safety.audit_redaction),
            safety=SafetyGuard(config),
            router=CommandRouter(),
        )
