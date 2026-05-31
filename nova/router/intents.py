from __future__ import annotations
from enum import Enum

class Intent(str, Enum):
    CHAT = 'chat'
    MEMORY_SAVE = 'memory_save'
    MEMORY_SEARCH = 'memory_search'
    DOCUMENT_INDEX = 'document_index'
    DOCUMENT_QA = 'document_qa'
    FILE_SCAN = 'file_scan'
    FILE_ORGANIZE = 'file_organize'
    DATA_PROFILE = 'data_profile'
    CODE_CREATE = 'code_create'
    TASK_CREATE = 'task_create'
    REMINDER_CREATE = 'reminder_create'
    SYSTEM_STATUS = 'system_status'
    PLUGIN_EXECUTE = 'plugin_execute'
    AUTOMATION = 'automation'
    UNKNOWN = 'unknown'
