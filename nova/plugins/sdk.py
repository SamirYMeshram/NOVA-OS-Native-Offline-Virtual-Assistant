from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol, Any

@dataclass(slots=True)
class PluginPermission:
    name: str
    description: str
    risk: str = 'low'

@dataclass(slots=True)
class PluginManifest:
    name: str
    version: str
    description: str
    permissions: list[PluginPermission] = field(default_factory=list)

class Plugin(Protocol):
    manifest: PluginManifest
    def run(self, command: str = '', **kwargs: Any) -> dict: ...
