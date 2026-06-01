from __future__ import annotations
import re
from .intents import Intent

RULES: list[tuple[Intent, list[str]]] = [
    (Intent.FILE_CLEAN_PLAN, ['clean', 'organize', 'downloads', 'duplicate files']),
    (Intent.DOCUMENT_QA, ['pdf', 'document', 'docs', 'notes', 'ask about', 'question about']),
    (Intent.MEMORY_ADD, ['remember', 'save memory', 'note that']),
    (Intent.MEMORY_SEARCH, ['what do you remember', 'recall', 'memory search']),
    (Intent.DATA_PROFILE, ['csv', 'excel', 'dataset', 'data profile']),
    (Intent.CODE_ANALYZE, ['analyze project', 'review code', 'codebase']),
    (Intent.PROJECT_CREATE, ['create project', 'build project', 'new fastapi', 'new cli']),
    (Intent.TASK_CREATE, ['remind me', 'task', 'todo']),
    (Intent.SYSTEM_STATUS, ['status', 'system monitor', 'cpu', 'ram', 'disk']),
    (Intent.AUTOMATION, ['open app', 'create folder', 'run command', 'shell']),
]

class IntentClassifier:
    def classify(self, text: str) -> Intent:
        low = text.lower()
        for intent, terms in RULES:
            if any(term in low for term in terms):
                return intent
        return Intent.CHAT if text.strip() else Intent.UNKNOWN
