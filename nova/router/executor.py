from __future__ import annotations
from pathlib import Path
from nova.core.runtime import get_runtime
from nova.core.audit import AuditEvent
from nova.core.result import Result
from nova.ai.model_manager import ModelManager
from nova.ai.conversation import Conversation
from nova.memory.service import MemoryService
from nova.security.path_policy import PathPolicy
from nova.documents.vector_store import VectorStore
from nova.documents.indexer import DocumentIndexer
from nova.documents.qa import DocumentQA
from nova.files.scanner import FileScanner
from nova.files.organizer import FileOrganizer
from nova.files.undo import UndoLog
from nova.data.profiler import DatasetProfiler
from nova.data.reports import DataReportBuilder
from nova.codegen.templates import ProjectTemplates
from nova.automation.system_monitor import SystemMonitor
from nova.plugins.bootstrap import load_builtin_plugins
from .intents import Intent

class CommandExecutor:
    def __init__(self):
        self.rt = get_runtime()
        self.models = ModelManager(self.rt.config.ai)
        self.memory = MemoryService(self.rt.config.data_dir)
        self.path_policy = PathPolicy(self.rt.config.security.protected_paths)
        self.vector_store = VectorStore(self.rt.config.data_dir / 'indexes' / 'documents.sqlite')
        self.plugins = load_builtin_plugins()

    def execute(self, intent: Intent, command: str, **kwargs) -> Result:
        try:
            if intent == Intent.MEMORY_SAVE:
                memory_id = self.memory.remember_from_text(command)
                result = Result.success('Saved local memory.', memory_id=memory_id)
            elif intent == Intent.MEMORY_SEARCH:
                result = Result.success(self.memory.recall(command.replace('recall', '').strip() or command))
            elif intent == Intent.SYSTEM_STATUS:
                result = Result.success('System status ready.', **SystemMonitor().snapshot())
            elif intent == Intent.FILE_SCAN:
                root = kwargs.get('path') or self._last_path(command) or '.'
                report = FileScanner(self.path_policy).scan(root)
                result = Result.success('File scan complete.', root=str(report.root), files=len(report.files), total_bytes=report.total_bytes, categories=report.categories)
            elif intent == Intent.FILE_ORGANIZE:
                root = kwargs.get('path') or self._last_path(command) or '.'
                report = FileScanner(self.path_policy).scan(root)
                plan = FileOrganizer().plan_by_category(report)
                undo_path = UndoLog(self.rt.config.data_dir / 'undo').record_plan(plan)
                result = Result.success(FileOrganizer().render_plan(plan, limit=30), actions=len(plan.actions), undo_plan=str(undo_path), requires_confirmation=True)
            elif intent == Intent.DATA_PROFILE:
                path = kwargs.get('path') or self._last_path(command)
                if not path:
                    return Result.failure('Provide a CSV or JSON path.')
                profiler = DatasetProfiler()
                profile = profiler.profile_json(path) if str(path).lower().endswith('.json') else profiler.profile_csv(path)
                result = Result.success(DataReportBuilder().markdown(profile), profile=profile)
            elif intent == Intent.CODE_CREATE:
                dest = kwargs.get('dest') or './nova_generated_project'
                name = kwargs.get('name') or 'nova-generated-project'
                kind = kwargs.get('kind') or ('fastapi' if 'fastapi' in command.lower() else 'python-cli')
                root = ProjectTemplates().fastapi_app(dest, name) if kind == 'fastapi' else ProjectTemplates().python_cli(dest, name)
                result = Result.success(f'Created {kind} project at {root}', path=str(root))
            elif intent == Intent.DOCUMENT_INDEX:
                path = kwargs.get('path') or self._last_path(command) or '.'
                embedder = self.models.embedding_provider()
                stats = DocumentIndexer(self.vector_store, embedder, self.path_policy).index_path(path)
                result = Result.success('Document index complete.', **stats)
            elif intent == Intent.DOCUMENT_QA:
                answer = DocumentQA(self.vector_store, self.models.embedding_provider(), self.models).ask(command)
                result = Result.success(answer.answer, citations=answer.citations, confidence=answer.confidence)
            elif intent == Intent.TASK_CREATE:
                task_id = self.memory.store.add_task(command.replace('add task', '').replace('task', '').strip() or command)
                result = Result.success('Task created.', task_id=task_id)
            elif intent == Intent.REMINDER_CREATE:
                rid = self.memory.store.add_reminder(command, kwargs.get('at') or 'unscheduled')
                result = Result.success('Reminder created.', reminder_id=rid)
            elif intent == Intent.PLUGIN_EXECUTE:
                parts = command.split(maxsplit=2)
                name = parts[1] if len(parts) > 1 else ''
                payload = parts[2] if len(parts) > 2 else ''
                result = Result.success('Plugin result.', **self.plugins.run(name, payload, {}))
            else:
                convo = Conversation(self.models)
                response = convo.ask(command)
                result = Result.success(response)
            self.memory.store.record_command(command, intent.value, result.message)
            self.rt.audit.write(AuditEvent('command', command, risk=result.data.get('risk','low'), metadata={'intent': intent.value, 'ok': result.ok}))
            return result
        except Exception as exc:
            return Result.failure(f'Command failed safely: {exc}', intent=intent.value)

    def _last_path(self, text: str) -> str | None:
        parts = text.split()
        for token in reversed(parts):
            if token.startswith('~') or token.startswith('.') or '/' in token or '\\' in token:
                return token.strip('"\'')
        return None
