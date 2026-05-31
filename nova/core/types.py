from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, Protocol


class Intent(str, Enum):
    CHAT = "chat"
    MEMORY_SAVE = "memory.save"
    MEMORY_SEARCH = "memory.search"
    DOCUMENT_INDEX = "documents.index"
    DOCUMENT_ASK = "documents.ask"
    FILE_SCAN = "files.scan"
    FILE_ORGANIZE = "files.organize"
    DATA_PROFILE = "data.profile"
    CODE_GENERATE = "code.generate"
    STUDY_PLAN = "study.plan"
    TASK_ADD = "tasks.add"
    TASK_LIST = "tasks.list"
    REMINDER_ADD = "reminders.add"
    SYSTEM_STATUS = "system.status"
    AUTOMATION = "automation"
    PLUGIN = "plugin"
    HELP = "help"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    DANGEROUS = "dangerous"


@dataclass(slots=True)
class RoutedCommand:
    text: str
    intent: Intent
    confidence: float
    entities: dict[str, Any] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ToolResult:
    ok: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class FileAction:
    action: str
    source: Path
    destination: Path | None = None
    risk: RiskLevel = RiskLevel.LOW
    reason: str = ""


@dataclass(slots=True)
class OperationPlan:
    title: str
    risk: RiskLevel
    actions: list[FileAction] = field(default_factory=list)
    requires_confirmation: bool = True
    explanation: str = ""


class CommandHandler(Protocol):
    def __call__(self, command: RoutedCommand) -> ToolResult: ...


@dataclass(slots=True)
class PluginManifest:
    name: str
    version: str
    description: str
    permissions: list[str]
    commands: list[str]
    enabled_by_default: bool = True


class NovaPlugin(Protocol):
    manifest: PluginManifest

    def can_handle(self, command: RoutedCommand) -> bool: ...

    def handle(self, command: RoutedCommand) -> ToolResult: ...
