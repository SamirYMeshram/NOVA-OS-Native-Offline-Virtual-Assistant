from __future__ import annotations

from .sdk import PluginContext, PluginResult
from .builtin import BUILTINS

class PluginManager:
    def __init__(self, nova_home: str) -> None:
        self.nova_home = nova_home
        self.plugins = {p.name: p for p in BUILTINS}
        self.enabled = set(self.plugins)

    def list(self) -> list[dict[str, object]]:
        return [{"name": p.name, "description": p.description, "permissions": sorted(p.permissions), "enabled": p.name in self.enabled} for p in self.plugins.values()]

    def run(self, name: str, command: str, dry_run: bool = True) -> PluginResult:
        if name not in self.plugins:
            return PluginResult(False, f"Unknown plugin: {name}")
        if name not in self.enabled:
            return PluginResult(False, f"Plugin disabled: {name}")
        return self.plugins[name].run(command, PluginContext(self.nova_home, dry_run))
