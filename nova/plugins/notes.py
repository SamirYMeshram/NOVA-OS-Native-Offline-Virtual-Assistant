from __future__ import annotations

from pathlib import Path

from ..core.types import Intent, PluginManifest, RoutedCommand, ToolResult
from ..memory.store import MemoryStore
from ..paths import NovaPaths


class Plugin:
    manifest = PluginManifest("notes", "1.0.0", "Local notes and memory capture", ["memory:write", "memory:read"], ["remember", "note"])

    def __init__(self) -> None:
        self.store = MemoryStore(NovaPaths.create().database)

    def can_handle(self, command: RoutedCommand) -> bool:
        return command.intent in {Intent.MEMORY_SAVE, Intent.MEMORY_SEARCH}

    def handle(self, command: RoutedCommand) -> ToolResult:
        if command.intent == Intent.MEMORY_SAVE:
            item = self.store.add_memory(command.text, kind="note", tags=["plugin:notes"])
            return ToolResult(True, "Note saved locally", item)
        return ToolResult(True, "Notes search", {"results": self.store.search(command.text)})
