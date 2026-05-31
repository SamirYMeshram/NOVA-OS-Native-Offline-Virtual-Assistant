from __future__ import annotations

from dataclasses import asdict

from .audit import AuditEvent
from .context import AppContext
from .types import Intent, ToolResult
from ..llm.manager import LocalModelManager
from ..memory.store import MemoryStore
from ..documents.qa import DocumentQA
from ..files.scanner import FileScanner
from ..automation.system_monitor import SystemMonitor


class NovaOrchestrator:
    """High-level command orchestrator. It keeps routing explicit and auditable."""

    def __init__(self, context: AppContext | None = None) -> None:
        self.context = context or AppContext.create()
        self.memory = MemoryStore(self.context.paths.database)
        self.llm = LocalModelManager(self.context.config.model)

    def handle(self, text: str) -> ToolResult:
        cmd = self.context.router.route(text)
        self.context.audit.record(AuditEvent("command.received", message=text, data={"intent": cmd.intent.value, "confidence": cmd.confidence}))
        if cmd.intent == Intent.MEMORY_SAVE:
            content = text.replace("remember", "", 1).strip(" :") or text
            item = self.memory.add_memory(content, kind="preference", tags=["user"])
            return ToolResult(True, f"Saved memory #{item['id']}", item)
        if cmd.intent == Intent.MEMORY_SEARCH:
            q = text.replace("search memory", "").replace("recall", "").strip() or text
            return ToolResult(True, "Memory search complete", {"results": self.memory.search(q, limit=10)})
        if cmd.intent == Intent.FILE_SCAN:
            paths = cmd.entities.get("paths") or ["."]
            report = FileScanner().scan(paths[0])
            return ToolResult(True, report.summary(), {"report": report.to_dict()})
        if cmd.intent == Intent.SYSTEM_STATUS:
            return ToolResult(True, "System status", SystemMonitor().snapshot())
        if cmd.intent == Intent.DOCUMENT_ASK:
            qa = DocumentQA(self.context.paths, self.llm)
            answer = qa.ask(text)
            return ToolResult(True, answer.answer, {"citations": [asdict(c) for c in answer.citations]})
        # Chat fallback uses local model when available, deterministic local fallback otherwise.
        reply = self.llm.complete(text, system="You are NOVA, a private local AI assistant. Be direct, safe, and useful.")
        return ToolResult(True, reply, {"intent": cmd.intent.value, "reasons": cmd.reasons})
