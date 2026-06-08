from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Any

@dataclass(slots=True)
class PluginContext:
    nova_home: str
    dry_run: bool = True

@dataclass(slots=True)
class PluginResult:
    ok: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)

class NovaPlugin(Protocol):
    name: str
    permissions: set[str]
    description: str
    def run(self, command: str, context: PluginContext) -> PluginResult: ...
