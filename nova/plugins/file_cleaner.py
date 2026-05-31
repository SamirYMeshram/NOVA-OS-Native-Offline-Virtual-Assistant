from __future__ import annotations

from dataclasses import asdict

from ..core.types import Intent, PluginManifest, RoutedCommand, ToolResult
from ..files.organizer import FileOrganizer
from ..files.scanner import FileScanner


class Plugin:
    manifest = PluginManifest("file_cleaner", "1.0.0", "Safe folder scanning and reversible cleanup plans", ["files:read", "files:plan"], ["scan folder", "organize folder"])

    def can_handle(self, command: RoutedCommand) -> bool:
        return command.intent in {Intent.FILE_SCAN, Intent.FILE_ORGANIZE}

    def handle(self, command: RoutedCommand) -> ToolResult:
        path = (command.entities.get("paths") or ["."])[0]
        if command.intent == Intent.FILE_ORGANIZE:
            plan = FileOrganizer().plan_by_category(path)
            return ToolResult(True, f"Created plan with {len(plan.actions)} actions. Review before applying.", {"actions": [asdict(a) for a in plan.actions]})
        report = FileScanner().scan(path)
        return ToolResult(True, report.summary(), report.to_dict())
