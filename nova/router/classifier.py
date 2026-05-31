from __future__ import annotations
from .intents import Intent

class IntentClassifier:
    def classify(self, text: str) -> Intent:
        t = text.lower().strip()
        if t.startswith('remember') or 'remember that' in t or 'save memory' in t:
            return Intent.MEMORY_SAVE
        if 'what do you remember' in t or t.startswith('recall') or 'search memory' in t:
            return Intent.MEMORY_SEARCH
        if 'index' in t and ('document' in t or 'folder' in t or 'pdf' in t):
            return Intent.DOCUMENT_INDEX
        if ('ask' in t or '?' in t) and ('document' in t or 'pdf' in t or 'indexed' in t):
            return Intent.DOCUMENT_QA
        if 'scan' in t and ('file' in t or 'folder' in t or 'downloads' in t):
            return Intent.FILE_SCAN
        if 'clean' in t or 'organize' in t:
            return Intent.FILE_ORGANIZE
        if 'csv' in t or 'dataset' in t or 'profile data' in t:
            return Intent.DATA_PROFILE
        if 'create project' in t or 'generate project' in t or 'fastapi' in t or 'python cli' in t:
            return Intent.CODE_CREATE
        if t.startswith('task') or 'add task' in t:
            return Intent.TASK_CREATE
        if 'remind' in t or 'reminder' in t:
            return Intent.REMINDER_CREATE
        if 'system' in t or 'cpu' in t or 'ram' in t or 'status' in t:
            return Intent.SYSTEM_STATUS
        if t.startswith('plugin'):
            return Intent.PLUGIN_EXECUTE
        if 'open app' in t or 'launch' in t or 'create folder' in t:
            return Intent.AUTOMATION
        return Intent.CHAT
