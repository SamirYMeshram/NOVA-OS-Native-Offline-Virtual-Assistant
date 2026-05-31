from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Intent(str, Enum):
    CHAT = "chat"
    MEMORY_SAVE = "memory_save"
    MEMORY_SEARCH = "memory_search"
    DOCUMENT_INDEX = "document_index"
    DOCUMENT_QA = "document_qa"
    FILE_SCAN = "file_scan"
    FILE_ORGANIZE_PLAN = "file_organize_plan"
    DATA_ANALYSIS = "data_analysis"
    TASK_CREATE = "task_create"
    TASK_LIST = "task_list"
    SYSTEM_STATUS = "system_status"
    HELP = "help"


@dataclass(slots=True)
class RoutedCommand:
    intent: Intent
    confidence: float
    argument: str
    needs_confirmation: bool = False
