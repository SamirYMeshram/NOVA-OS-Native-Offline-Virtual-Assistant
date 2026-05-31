from __future__ import annotations

from ..automation.system_monitor import SystemMonitor
from ..core.types import Intent, PluginManifest, RoutedCommand, ToolResult


class Plugin:
    manifest = PluginManifest("system_monitor", "1.0.0", "Local CPU/RAM/disk monitor", ["system:read"], ["system status", "cpu", "ram"])

    def can_handle(self, command: RoutedCommand) -> bool:
        return command.intent == Intent.SYSTEM_STATUS

    def handle(self, command: RoutedCommand) -> ToolResult:
        return ToolResult(True, "System snapshot", SystemMonitor().snapshot())
