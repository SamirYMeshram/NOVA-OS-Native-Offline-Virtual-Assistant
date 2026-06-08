from __future__ import annotations

from pathlib import Path
import re
from nova.core.models import Intent, IntentScore, EntitySet

KEYWORDS: dict[Intent, list[str]] = {
    Intent.MEMORY_SAVE: ["remember", "save memory", "note that", "from now on"],
    Intent.MEMORY_SEARCH: ["what did i say", "recall", "search memory", "remember about"],
    Intent.TASK_CREATE: ["remind", "task", "todo", "deadline"],
    Intent.DOCUMENT_INDEX: ["index", "read these docs", "add documents"],
    Intent.DOCUMENT_QA: ["ask document", "in the pdf", "from the document", "what does the file say", "question about"],
    Intent.FILE_SCAN: ["scan", "inspect folder", "large files", "old files"],
    Intent.FILE_SEARCH: ["find file", "search files", "where is", "locate"],
    Intent.FILE_CLEANUP_PLAN: ["clean", "organize", "cleanup", "downloads folder"],
    Intent.DATA_PROFILE: ["csv", "excel", "dataset", "profile data", "analyze data"],
    Intent.CODE_ANALYZE: ["analyze code", "review code", "project folder", "codebase", "bugs"],
    Intent.PROJECT_FORGE: ["build project", "create project", "generate app", "flask", "fastapi", "cli project"],
    Intent.SYSTEM_STATUS: ["status", "doctor", "system monitor", "cpu", "ram"],
    Intent.PLUGIN_RUN: ["plugin"],
    Intent.WORKFLOW_RUN: ["workflow", "study pack", "research pack"],
    Intent.AUTOMATION: ["open folder", "launch", "create file", "move file"],
}

PATH_RE = re.compile(r"(?:~|\.|/|[A-Za-z]:\\)[^\s\"']+")
URL_RE = re.compile(r"https?://[^\s]+")


def classify(text: str) -> list[IntentScore]:
    low = text.lower()
    scores: list[IntentScore] = []
    for intent, keys in KEYWORDS.items():
        evidence = [k for k in keys if k in low]
        if evidence:
            conf = min(0.95, 0.35 + 0.2 * len(evidence))
            scores.append(IntentScore(intent, conf, evidence))
    if not scores:
        scores.append(IntentScore(Intent.CHAT, 0.45, ["default chat/fallback"] ))
    scores.sort(key=lambda s: s.confidence, reverse=True)
    return scores


def extract_entities(text: str) -> EntitySet:
    paths = PATH_RE.findall(text)
    urls = URL_RE.findall(text)
    project_name = None
    m = re.search(r"called\s+([A-Za-z][\w-]+)", text)
    if m: project_name = m.group(1)
    question = text if "?" in text or any(w in text.lower() for w in ["what", "why", "how", "when", "where"]) else None
    return EntitySet(paths=paths, urls=urls, project_name=project_name, question=question, raw={"length": len(text)})
