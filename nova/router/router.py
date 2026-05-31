from __future__ import annotations

import re
from pathlib import Path

from nova.ai.brain import NovaBrain
from nova.automation.actions import AutomationEngine
from nova.data.analyst import DatasetAnalyst
from nova.documents.index import DocumentIndex
from nova.documents.qa import DocumentQA
from nova.files.organizer import FileOrganizer
from nova.files.scanner import FileScanner
from nova.memory.store import MemoryStore
from nova.router.intents import Intent, RoutedCommand

PATH_PATTERN = re.compile(r"(?:/|~|\.\.?/)[^\s]+|[A-Za-z]:\\[^\s]+")


class CommandRouter:
    """Intent router for the first working NOVA agent loop.

    This is deliberately deterministic and inspectable. Later versions can let a local LLM
    propose tool calls, but critical action boundaries remain rule/permission guarded.
    """

    def __init__(self) -> None:
        self.memory = MemoryStore()
        self.brain = NovaBrain(memory=self.memory)
        self.index = DocumentIndex()
        self.docqa = DocumentQA(index=self.index)
        self.scanner = FileScanner()
        self.organizer = FileOrganizer()
        self.analyst = DatasetAnalyst()
        self.automation = AutomationEngine()

    def route(self, message: str) -> RoutedCommand:
        text = message.strip()
        lower = text.lower()
        if lower in {"help", "what can you do", "commands"}:
            return RoutedCommand(Intent.HELP, 1.0, "")
        if lower.startswith(("remember ", "save memory ", "note that ")):
            return RoutedCommand(Intent.MEMORY_SAVE, 0.95, self._strip_prefix(text))
        if "search memory" in lower or "recall" in lower:
            return RoutedCommand(Intent.MEMORY_SEARCH, 0.85, self._clean_query(text, ["search memory", "recall"]))
        if lower.startswith("index ") or "index folder" in lower or "index documents" in lower:
            return RoutedCommand(Intent.DOCUMENT_INDEX, 0.9, self._extract_path_or_rest(text))
        if lower.startswith("ask docs ") or "document" in lower and ("?" in text or "answer" in lower):
            return RoutedCommand(Intent.DOCUMENT_QA, 0.82, self._clean_query(text, ["ask docs", "ask documents"]))
        if lower.startswith("scan ") or "scan folder" in lower:
            return RoutedCommand(Intent.FILE_SCAN, 0.85, self._extract_path_or_rest(text))
        if "organize" in lower or "clean downloads" in lower or "clean folder" in lower:
            return RoutedCommand(Intent.FILE_ORGANIZE_PLAN, 0.88, self._extract_path_or_rest(text) or str(Path.home() / "Downloads"), True)
        if lower.endswith(".csv") or "analyze csv" in lower or "dataset" in lower:
            return RoutedCommand(Intent.DATA_ANALYSIS, 0.78, self._extract_path_or_rest(text))
        if lower.startswith(("task ", "add task ", "todo ")):
            return RoutedCommand(Intent.TASK_CREATE, 0.9, self._strip_prefix(text))
        if "list tasks" in lower or "show tasks" in lower:
            return RoutedCommand(Intent.TASK_LIST, 0.9, "")
        if "system status" in lower or "cpu" in lower or "ram" in lower:
            return RoutedCommand(Intent.SYSTEM_STATUS, 0.9, "")
        return RoutedCommand(Intent.CHAT, 0.5, text)

    def handle(self, message: str) -> str:
        cmd = self.route(message)
        try:
            if cmd.intent == Intent.HELP:
                return self.help_text()
            if cmd.intent == Intent.MEMORY_SAVE:
                mem_id = self.memory.add(cmd.argument, kind="user_note", tags=["manual"])
                return f"Saved local memory #{mem_id}."
            if cmd.intent == Intent.MEMORY_SEARCH:
                hits = self.memory.search(cmd.argument)
                if not hits:
                    return "No matching local memories found."
                return "\n".join(f"#{m.id} [{m.kind}] {m.content}" for m in hits)
            if cmd.intent == Intent.DOCUMENT_INDEX:
                path = cmd.argument or "."
                indexed = self.index.index_path(path)
                stats = self.index.stats()
                return f"Indexed {len(indexed)} files. Current document index: {stats['files']} files, {stats['chunks']} chunks."
            if cmd.intent == Intent.DOCUMENT_QA:
                result = self.docqa.ask(cmd.argument)
                cite_text = "\n".join(f"- {c}" for c in result.citations[:8])
                return f"{result.answer}\n\nCitations:\n{cite_text or '(none)'}"
            if cmd.intent == Intent.FILE_SCAN:
                report = self.scanner.scan(cmd.argument or ".", hash_files=False)
                largest = "\n".join(f"- {f.path.name}: {f.size/1024/1024:.2f} MB" for f in report.largest_files[:5])
                exts = ", ".join(f"{k}:{v}" for k, v in list(report.by_extension.items())[:8])
                return f"Scanned {report.root}\nFiles: {report.file_count}\nTotal: {report.total_bytes/1024/1024:.2f} MB\nExtensions: {exts}\nLargest:\n{largest}"
            if cmd.intent == Intent.FILE_ORGANIZE_PLAN:
                plan = self.organizer.plan_by_type(cmd.argument or ".")
                preview = "\n".join(f"- {m.source.name} -> {m.destination.parent.name}/" for m in plan.moves[:20])
                return (
                    f"Created a safe organization plan for {plan.root}.\n"
                    f"Planned moves: {len(plan.moves)}. Nothing was moved yet.\n"
                    f"Warnings: {'; '.join(plan.warnings) or 'none'}\n\n{preview}\n\n"
                    "To execute from Python, call FileOrganizer.execute(plan, confirmed=True). CLI execution stays confirmation-gated."
                )
            if cmd.intent == Intent.DATA_ANALYSIS:
                report = self.analyst.profile_csv(cmd.argument)
                return report.to_markdown()
            if cmd.intent == Intent.TASK_CREATE:
                task_id = self.memory.create_task(cmd.argument)
                return f"Created local task #{task_id}: {cmd.argument}"
            if cmd.intent == Intent.TASK_LIST:
                tasks = self.memory.list_tasks()
                return "\n".join(f"#{t['id']} [{t['status']}] {t['title']}" for t in tasks) or "No tasks yet."
            if cmd.intent == Intent.SYSTEM_STATUS:
                result = self.automation.system_status()
                return f"{result.message}: {result.data}"
            answer = self.brain.answer(message)
            suffix = "\n\n[Fallback mode: start Ollama for full local LLM replies.]" if answer.used_fallback else ""
            return answer.text + suffix
        except Exception as exc:
            return f"NOVA handled this safely and stopped because of an error: {exc}"

    @staticmethod
    def _strip_prefix(text: str) -> str:
        return re.sub(r"^(remember|save memory|note that|task|add task|todo)\s+", "", text, flags=re.I).strip()

    @staticmethod
    def _clean_query(text: str, prefixes: list[str]) -> str:
        cleaned = text
        for prefix in prefixes:
            cleaned = re.sub(re.escape(prefix), "", cleaned, flags=re.I)
        return cleaned.strip(" :-")

    @staticmethod
    def _extract_path_or_rest(text: str) -> str:
        match = PATH_PATTERN.search(text)
        if match:
            return match.group(0).strip('"\'')
        parts = text.split(maxsplit=1)
        return parts[1].strip() if len(parts) > 1 else ""

    @staticmethod
    def help_text() -> str:
        return """
NOVA Sovereign AI commands:
- chat naturally: explain, plan, brainstorm, code with local model
- remember <fact>: save editable local memory
- search memory <query>: recall local memory
- index <folder-or-file>: build local document index
- ask docs <question>: answer from indexed documents with citations
- scan <folder>: file intelligence report
- organize <folder>: create safe cleanup/organization plan, no deletion
- analyze csv <file.csv>: local dataset report
- task <title>: create task
- list tasks: show task list
- system status: CPU/RAM/disk/platform status
- dashboard: run `nova dashboard`
""".strip()
