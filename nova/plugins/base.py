from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from ..core.types import PluginManifest, RoutedCommand, ToolResult


class BasePlugin:
    manifest = PluginManifest("base", "0.0.0", "Base plugin", [], [])

    def can_handle(self, command: RoutedCommand) -> bool:
        return False

    def handle(self, command: RoutedCommand) -> ToolResult:
        return ToolResult(False, "Plugin cannot handle this command")
