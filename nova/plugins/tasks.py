from __future__ import annotations

from ..core.types import Intent, PluginManifest, RoutedCommand, ToolResult
from ..memory.store import MemoryStore
from ..paths import NovaPaths


class Plugin:
    manifest = PluginManifest("tasks", "1.0.0", "Local task manager", ["tasks:write", "tasks:read"], ["task", "todo", "list tasks"])

    def __init__(self) -> None:
        self.store = MemoryStore(NovaPaths.create().database)

    def can_handle(self, command: RoutedCommand) -> bool:
        return command.intent in {Intent.TASK_ADD, Intent.TASK_LIST}

    def handle(self, command: RoutedCommand) -> ToolResult:
        if command.intent == Intent.TASK_ADD:
            item = self.store.add_task(command.text)
            return ToolResult(True, "Task added", item)
        return ToolResult(True, "Task list", {"tasks": self.store.list_tasks()})
