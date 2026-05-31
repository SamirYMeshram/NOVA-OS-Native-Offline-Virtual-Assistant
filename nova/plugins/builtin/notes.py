from __future__ import annotations

from dataclasses import asdict

from nova.memory.store import MemoryStore
from nova.plugins.base import NovaPlugin, PluginManifest, PluginResult


class NotesPlugin(NovaPlugin):
    manifest = PluginManifest("notes", "Local private notes stored in NOVA memory", ["memory:write", "memory:read"])

    def __init__(self) -> None:
        self.memory = MemoryStore()

    def commands(self) -> dict[str, str]:
        return {"add": "Add a note", "search": "Search notes"}

    def run(self, command: str, argument: str) -> PluginResult:
        if command == "add":
            note_id = self.memory.add(argument, kind="note", tags=["notes"])
            return PluginResult(True, f"Saved note #{note_id}")
        if command == "search":
            notes = self.memory.search(argument)
            return PluginResult(True, "Search complete", {"notes": [asdict(n) for n in notes]})
        return PluginResult(False, f"Unknown notes command: {command}")
