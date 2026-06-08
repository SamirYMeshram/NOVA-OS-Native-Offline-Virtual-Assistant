from __future__ import annotations

from dataclasses import dataclass
from .sdk import PluginContext, PluginResult

@dataclass
class SimplePlugin:
    name: str
    description: str
    permissions: set[str]

    def run(self, command: str, context: PluginContext) -> PluginResult:
        return PluginResult(True, f"{self.name} received command in dry_run={context.dry_run}", {"command": command})

BUILTINS = [
    SimplePlugin("notes", "Local notes workflow", {"memory:write"}),
    SimplePlugin("tasks", "Task manager workflow", {"tasks:write"}),
    SimplePlugin("reminders", "Reminder planner", {"tasks:write"}),
    SimplePlugin("file_cleaner", "Safe cleanup planner", {"files:read", "files:plan"}),
    SimplePlugin("study_planner", "Study notes and flashcards", {"documents:read", "tasks:write"}),
    SimplePlugin("code_forge", "Project generator", {"files:write"}),
    SimplePlugin("document_summarizer", "Document summary", {"documents:read"}),
    SimplePlugin("csv_analyst", "CSV analysis", {"data:read"}),
    SimplePlugin("system_monitor", "Local system status", {"system:read"}),
    SimplePlugin("local_search", "Local search", {"files:read"}),
    SimplePlugin("voice_assistant", "Offline voice bridge", {"audio:local"}),
    SimplePlugin("automation_manager", "Safe automation manager", {"automation:review"}),
    SimplePlugin("knowledge_base", "Knowledge base manager", {"documents:read", "memory:read"}),
    SimplePlugin("report_generator", "Local report generator", {"files:write"}),
]
