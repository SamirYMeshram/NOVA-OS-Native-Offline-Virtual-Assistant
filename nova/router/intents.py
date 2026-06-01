from __future__ import annotations
from enum import Enum

class Intent(str, Enum):
    CHAT = 'chat'
    MEMORY_ADD = 'memory.add'
    MEMORY_SEARCH = 'memory.search'
    DOCUMENT_INDEX = 'document.index'
    DOCUMENT_QA = 'document.qa'
    FILE_SCAN = 'file.scan'
    FILE_CLEAN_PLAN = 'file.clean.plan'
    DATA_PROFILE = 'data.profile'
    CODE_ANALYZE = 'code.analyze'
    PROJECT_CREATE = 'project.create'
    TASK_CREATE = 'task.create'
    SYSTEM_STATUS = 'system.status'
    AUTOMATION = 'automation'
    PLUGIN = 'plugin'
    SETTINGS = 'settings'
    UNKNOWN = 'unknown'
