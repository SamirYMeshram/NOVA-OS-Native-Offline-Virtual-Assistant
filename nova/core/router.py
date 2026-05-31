from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .types import Intent, RoutedCommand


@dataclass(frozen=True)
class IntentRule:
    intent: Intent
    keywords: tuple[str, ...]
    patterns: tuple[str, ...] = ()
    weight: float = 1.0


RULES: tuple[IntentRule, ...] = (
    IntentRule(Intent.MEMORY_SAVE, ("remember", "save memory", "store this", "note that"), (r"\bremember\b",), 1.3),
    IntentRule(Intent.MEMORY_SEARCH, ("what do you remember", "recall", "search memory", "memory about"), (), 1.2),
    IntentRule(Intent.DOCUMENT_INDEX, ("index", "ingest", "scan document", "add document", "read folder"), (), 1.1),
    IntentRule(Intent.DOCUMENT_ASK, ("ask document", "chat with", "from pdf", "according to document", "summarize pdf", "document question"), (), 1.2),
    IntentRule(Intent.FILE_SCAN, ("scan folder", "find duplicates", "large files", "old files", "search files"), (), 1.2),
    IntentRule(Intent.FILE_ORGANIZE, ("organize", "clean downloads", "clean my", "clean folder", "move files", "sort files"), (), 1.35),
    IntentRule(Intent.DATA_PROFILE, ("csv", "excel", "dataset", "data analysis", "profile data", "missing values"), (), 1.2),
    IntentRule(Intent.CODE_GENERATE, ("create project", "generate project", "build app", "fastapi", "flask", "write tests"), (), 1.25),
    IntentRule(Intent.STUDY_PLAN, ("study", "exam", "flashcards", "quiz", "prepare me"), (), 1.15),
    IntentRule(Intent.TASK_ADD, ("add task", "todo", "to-do", "task"), (r"\bremind me\b",), 1.0),
    IntentRule(Intent.REMINDER_ADD, ("reminder", "remind me", "deadline", "due"), (), 1.2),
    IntentRule(Intent.SYSTEM_STATUS, ("cpu", "ram", "disk", "system status", "monitor system", "battery"), (), 1.1),
    IntentRule(Intent.AUTOMATION, ("open app", "launch", "create folder", "create file", "take screenshot"), (), 1.0),
    IntentRule(Intent.HELP, ("help", "commands", "what can you do"), (), 1.0),
)


class CommandRouter:
    """Deterministic local intent router with transparent reasons."""

    def route(self, text: str) -> RoutedCommand:
        normalized = " ".join(text.lower().strip().split())
        if not normalized:
            return RoutedCommand(text=text, intent=Intent.HELP, confidence=1.0, reasons=["empty command"])
        scores: dict[Intent, float] = {}
        reasons: dict[Intent, list[str]] = {}
        for rule in RULES:
            for kw in rule.keywords:
                if kw in normalized:
                    scores[rule.intent] = scores.get(rule.intent, 0.0) + rule.weight
                    reasons.setdefault(rule.intent, []).append(f"keyword:{kw}")
            for pattern in rule.patterns:
                if re.search(pattern, normalized):
                    scores[rule.intent] = scores.get(rule.intent, 0.0) + rule.weight
                    reasons.setdefault(rule.intent, []).append(f"pattern:{pattern}")
        path_entities = self._extract_paths(text)
        if path_entities and not scores:
            scores[Intent.FILE_SCAN] = 0.8
            reasons[Intent.FILE_SCAN] = ["path detected"]
        if not scores:
            return RoutedCommand(text=text, intent=Intent.CHAT, confidence=0.55, entities={"paths": path_entities}, reasons=["default chat"])
        intent, score = max(scores.items(), key=lambda item: item[1])
        confidence = min(0.98, 0.45 + score / 3.0)
        return RoutedCommand(text=text, intent=intent, confidence=confidence, entities={"paths": path_entities}, reasons=reasons[intent])

    def _extract_paths(self, text: str) -> list[str]:
        tokens = re.findall(r"(?:~|/|\./|\.\./)[^\s]+|[A-Za-z]:\\[^\s]+", text)
        return [str(Path(token.strip('"\'')).expanduser()) for token in tokens]
