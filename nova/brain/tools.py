from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Any
from nova.core.models import ToolResult, RiskLevel
from nova.config import NovaConfig
from nova.memory.store import MemoryStore
from nova.tasks.store import TaskStore
from nova.documents.index import DocumentIndex
from nova.documents.rag import RAGEngine
from nova.files.scanner import scan_folder, summarize_scan
from nova.files.organizer import build_cleanup_plan
from nova.files.search import search_files
from nova.data.profiler import profile_dataset
from nova.codegen.analyzer import analyze_codebase
from nova.codegen.reviewer import security_review
from nova.codegen.forge import blueprint as forge_blueprint, build_project
from nova.llm.ollama import OllamaModel
from nova.llm.base import ChatMessage
from nova.llm.prompts import SYSTEM_PROMPT

@dataclass(slots=True)
class ToolSpec:
    name: str
    risk: RiskLevel
    description: str
    fn: Callable[[dict[str, Any], bool], Any]

class ToolRuntime:
    def __init__(self, config: NovaConfig) -> None:
        self.config = config
        self.memory = MemoryStore(config.db_path)
        self.tasks = TaskStore(config.db_path)
        self.doc_index = DocumentIndex(config)
        self.model = OllamaModel(config.model.chat_model, config.model.ollama_base_url, config.model.timeout_seconds)
        self.tools: dict[str, ToolSpec] = {}
        self._register_core()

    def register(self, spec: ToolSpec) -> None:
        self.tools[spec.name] = spec

    def _register_core(self) -> None:
        self.register(ToolSpec("chat.complete", RiskLevel.SAFE, "Local model/fallback chat", lambda a,d: asdict(self.model.complete([ChatMessage("user", a.get("message", ""))], SYSTEM_PROMPT))))
        self.register(ToolSpec("memory.add", RiskLevel.SAFE, "Add local memory", lambda a,d: {"id": self.memory.add(a["text"], a.get("kind", "note"))}))
        self.register(ToolSpec("memory.search", RiskLevel.SAFE, "Search local memory", lambda a,d: [asdict(m) for m in self.memory.search(a.get("query", ""))]))
        self.register(ToolSpec("task.add", RiskLevel.REVIEW, "Add local task", lambda a,d: {"dry_run": d, "id": None if d else self.tasks.add(a["title"], a.get("due"))}))
        self.register(ToolSpec("file.scan", RiskLevel.SAFE, "Scan folder", lambda a,d: summarize_scan(scan_folder(a["path"], self.config.safety.max_scan_files))))
        self.register(ToolSpec("file.cleanup_plan", RiskLevel.REVIEW, "Build cleanup plan", lambda a,d: build_cleanup_plan(a["path"], self.config.safety.max_scan_files).to_dict()))
        self.register(ToolSpec("file.search", RiskLevel.SAFE, "Search files", lambda a,d: [asdict(h) for h in search_files(a["path"], a["query"])]))
        self.register(ToolSpec("document.index", RiskLevel.SAFE, "Index documents", lambda a,d: self.doc_index.add_path(a["path"])))
        self.register(ToolSpec("document.ask", RiskLevel.SAFE, "Ask local document index", lambda a,d: asdict(RAGEngine(self.doc_index, self.model).answer(a["question"]))))
        self.register(ToolSpec("data.profile", RiskLevel.SAFE, "Profile dataset", lambda a,d: profile_dataset(a["path"])))
        self.register(ToolSpec("code.analyze", RiskLevel.SAFE, "Analyze codebase", lambda a,d: analyze_codebase(a["path"])))
        self.register(ToolSpec("code.security_review", RiskLevel.SAFE, "Review code security", lambda a,d: security_review(a["path"])))
        self.register(ToolSpec("forge.blueprint", RiskLevel.SAFE, "Project blueprint", lambda a,d: forge_blueprint(a["goal"]).to_dict()))
        self.register(ToolSpec("forge.build", RiskLevel.REVIEW, "Build project safely", lambda a,d: build_project(a["goal"], a.get("output_dir", self.config.workspace_dir), dry_run=(d or a.get("dry_run", True)))))
        self.register(ToolSpec("critic.review", RiskLevel.SAFE, "Critique current plan", lambda a,d: {"review": "Check risky paths, duplicate destinations, protected folders, and require confirmation before side effects."}))

    def call(self, name: str, args: dict[str, Any], dry_run: bool = True) -> ToolResult:
        spec = self.tools.get(name)
        if not spec:
            return ToolResult(name, False, error=f"Unknown tool: {name}", risk=RiskLevel.BLOCKED)
        try:
            data = spec.fn(args, dry_run)
            side_effects = [] if dry_run or spec.risk == RiskLevel.SAFE else [spec.description]
            return ToolResult(name, True, data=data, side_effects=side_effects, risk=spec.risk)
        except Exception as exc:
            return ToolResult(name, False, error=str(exc), risk=spec.risk)
