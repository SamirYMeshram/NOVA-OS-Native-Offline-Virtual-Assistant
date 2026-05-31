from __future__ import annotations

import importlib
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from ..core.types import NovaPlugin, RoutedCommand, ToolResult
from ..exceptions import PluginError

BUILTIN_PLUGIN_MODULES = [
    "nova.plugins.notes",
    "nova.plugins.tasks",
    "nova.plugins.file_cleaner",
    "nova.plugins.system_monitor",
    "nova.plugins.study_planner",
    "nova.plugins.code_generator",
    "nova.plugins.report_generator",
]


class PluginManager:
    def __init__(self) -> None:
        self.plugins: list[NovaPlugin] = []

    def load_builtins(self) -> "PluginManager":
        for module_name in BUILTIN_PLUGIN_MODULES:
            module = importlib.import_module(module_name)
            plugin = module.Plugin()
            self.plugins.append(plugin)
        return self

    def list_manifests(self) -> list[dict[str, object]]:
        return [asdict(p.manifest) for p in self.plugins]

    def dispatch(self, command: RoutedCommand) -> ToolResult | None:
        for plugin in self.plugins:
            if plugin.can_handle(command):
                return plugin.handle(command)
        return None
