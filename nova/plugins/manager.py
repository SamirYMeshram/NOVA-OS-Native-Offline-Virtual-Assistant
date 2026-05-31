from __future__ import annotations

from dataclasses import dataclass

from nova.plugins.base import NovaPlugin, PluginResult
from nova.plugins.builtin.code_generator import CodeProjectPlugin
from nova.plugins.builtin.notes import NotesPlugin
from nova.plugins.builtin.report_generator import ReportGeneratorPlugin
from nova.plugins.builtin.study_planner import StudyPlannerPlugin
from nova.plugins.builtin.system_monitor import SystemMonitorPlugin
from nova.plugins.builtin.tasks import TasksPlugin


@dataclass(slots=True)
class RegisteredPlugin:
    plugin: NovaPlugin
    enabled: bool = True


class PluginManager:
    def __init__(self) -> None:
        self.plugins: dict[str, RegisteredPlugin] = {}
        self.register_defaults()

    def register_defaults(self) -> None:
        for plugin in [
            NotesPlugin(),
            TasksPlugin(),
            SystemMonitorPlugin(),
            StudyPlannerPlugin(),
            CodeProjectPlugin(),
            ReportGeneratorPlugin(),
        ]:
            self.register(plugin)

    def register(self, plugin: NovaPlugin) -> None:
        self.plugins[plugin.manifest.name] = RegisteredPlugin(plugin, plugin.manifest.enabled_by_default)

    def list_plugins(self) -> list[dict[str, object]]:
        return [
            {
                "name": item.plugin.manifest.name,
                "description": item.plugin.manifest.description,
                "permissions": item.plugin.manifest.permissions,
                "enabled": item.enabled,
                "commands": item.plugin.commands(),
            }
            for item in self.plugins.values()
        ]

    def set_enabled(self, name: str, enabled: bool) -> None:
        if name not in self.plugins:
            raise KeyError(f"Unknown plugin: {name}")
        self.plugins[name].enabled = enabled

    def run(self, plugin_name: str, command: str, argument: str = "") -> PluginResult:
        registered = self.plugins.get(plugin_name)
        if not registered:
            return PluginResult(False, f"Plugin not found: {plugin_name}")
        if not registered.enabled:
            return PluginResult(False, f"Plugin disabled: {plugin_name}")
        return registered.plugin.run(command, argument)
