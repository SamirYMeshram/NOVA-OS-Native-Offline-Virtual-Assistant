from __future__ import annotations
from dataclasses import asdict
from .base import Plugin

class PluginManager:
    def __init__(self):
        self.plugins: dict[str, Plugin] = {}
        self.enabled: set[str] = set()

    def register(self, plugin: Plugin) -> None:
        self.plugins[plugin.manifest.name] = plugin
        self.enabled.add(plugin.manifest.name)

    def disable(self, name: str) -> bool:
        if name in self.enabled:
            self.enabled.remove(name)
            return True
        return False

    def enable(self, name: str) -> bool:
        if name in self.plugins:
            self.enabled.add(name)
            return True
        return False

    def list(self) -> list[dict]:
        return [
            {'enabled': name in self.enabled, **asdict(plugin.manifest)}
            for name, plugin in sorted(self.plugins.items())
        ]

    def run(self, name: str, command: str, context: dict | None = None) -> dict:
        if name not in self.plugins:
            return {'ok': False, 'message': f'Plugin not found: {name}'}
        if name not in self.enabled:
            return {'ok': False, 'message': f'Plugin disabled: {name}'}
        return self.plugins[name].run(command, context or {})
