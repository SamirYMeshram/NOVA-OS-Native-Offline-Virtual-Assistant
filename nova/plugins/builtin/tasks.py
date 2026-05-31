from __future__ import annotations

from nova.memory.store import MemoryStore
from nova.plugins.base import NovaPlugin, PluginManifest, PluginResult


class TasksPlugin(NovaPlugin):
    manifest = PluginManifest("tasks", "Local task manager", ["tasks:write", "tasks:read"])

    def __init__(self) -> None:
        self.memory = MemoryStore()

    def commands(self) -> dict[str, str]:
        return {"add": "Add task", "list": "List tasks", "done": "Mark task done by id"}

    def run(self, command: str, argument: str) -> PluginResult:
        if command == "add":
            task_id = self.memory.create_task(argument)
            return PluginResult(True, f"Created task #{task_id}")
        if command == "list":
            return PluginResult(True, "Tasks loaded", {"tasks": self.memory.list_tasks()})
        if command == "done":
            self.memory.set_task_status(int(argument.strip()), "done")
            return PluginResult(True, f"Task #{argument.strip()} marked done")
        return PluginResult(False, f"Unknown tasks command: {command}")
