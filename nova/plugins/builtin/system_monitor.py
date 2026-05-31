from __future__ import annotations

from nova.automation.actions import AutomationEngine
from nova.plugins.base import NovaPlugin, PluginManifest, PluginResult


class SystemMonitorPlugin(NovaPlugin):
    manifest = PluginManifest("system_monitor", "Local CPU/RAM/disk monitor", ["system:read"])

    def __init__(self) -> None:
        self.engine = AutomationEngine()

    def commands(self) -> dict[str, str]:
        return {"status": "Collect system metrics"}

    def run(self, command: str, argument: str) -> PluginResult:
        if command != "status":
            return PluginResult(False, f"Unknown system monitor command: {command}")
        result = self.engine.system_status()
        return PluginResult(result.ok, result.message, result.data or {})
