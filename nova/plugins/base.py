from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol
from nova.security.permissions import PermissionSet

@dataclass(slots=True)
class PluginManifest:
    name: str
    version: str
    description: str
    permissions: PermissionSet = field(default_factory=PermissionSet)

class Plugin(Protocol):
    manifest: PluginManifest
    def run(self, command: str, context: dict) -> dict: ...
