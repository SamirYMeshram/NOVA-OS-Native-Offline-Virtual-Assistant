from __future__ import annotations

from ..core.types import Intent, PluginManifest, RoutedCommand, ToolResult


class Plugin:
    manifest = PluginManifest("report_generator", "1.0.0", "Local report generation helper", ["documents:read", "files:write-confirmed"], ["report", "summary"])

    def can_handle(self, command: RoutedCommand) -> bool:
        return "report" in command.text.lower()

    def handle(self, command: RoutedCommand) -> ToolResult:
        return ToolResult(True, "Report workflow", {"steps": ["index sources", "retrieve evidence", "draft report", "export markdown"]})
