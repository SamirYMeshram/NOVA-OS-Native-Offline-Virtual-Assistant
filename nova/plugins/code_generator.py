from __future__ import annotations

from ..core.types import Intent, PluginManifest, RoutedCommand, ToolResult


class Plugin:
    manifest = PluginManifest("code_generator", "1.0.0", "Local project generation assistant", ["files:write-confirmed"], ["create project", "fastapi", "cli"])

    def can_handle(self, command: RoutedCommand) -> bool:
        return command.intent == Intent.CODE_GENERATE

    def handle(self, command: RoutedCommand) -> ToolResult:
        return ToolResult(True, "Use `nova code new-cli <name> --confirm` or `nova code new-fastapi <name> --confirm` to generate a safe local template.")
