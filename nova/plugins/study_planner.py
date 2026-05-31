from __future__ import annotations

from ..core.types import Intent, PluginManifest, RoutedCommand, ToolResult


class Plugin:
    manifest = PluginManifest("study_planner", "1.0.0", "Study plan and flashcard workflow", ["memory:write", "documents:read"], ["study", "flashcards", "exam"])

    def can_handle(self, command: RoutedCommand) -> bool:
        return command.intent == Intent.STUDY_PLAN

    def handle(self, command: RoutedCommand) -> ToolResult:
        plan = [
            "Index your PDFs/notes: nova docs index <folder>",
            "Generate summaries: nova docs ask 'summarize key concepts for exam'",
            "Create flashcards from retrieved chunks",
            "Review weak topics daily and save progress in tasks",
        ]
        return ToolResult(True, "Study workflow prepared", {"plan": plan})
