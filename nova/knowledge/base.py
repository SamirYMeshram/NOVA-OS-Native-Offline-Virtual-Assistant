from __future__ import annotations

from pathlib import Path
from dataclasses import asdict

from ..documents.indexer import DocumentIndexer
from ..documents.qa import DocumentQA
from ..llm.manager import LocalModelManager
from ..memory.store import MemoryStore
from ..paths import NovaPaths


class KnowledgeBase:
    """Combines memory recall and document retrieval into one local knowledge interface."""

    def __init__(self, paths: NovaPaths | None = None) -> None:
        self.paths = paths or NovaPaths.create()
        self.model_manager = LocalModelManager()
        self.memory = MemoryStore(self.paths.database)
        self.indexer = DocumentIndexer(self.paths, self.model_manager)
        self.qa = DocumentQA(self.paths, self.model_manager)

    def ingest(self, path: str | Path) -> dict[str, object]:
        report = self.indexer.index_path(path)
        return asdict(report)

    def ask(self, question: str) -> dict[str, object]:
        memories = self.memory.search(question, limit=5)
        doc_answer = self.qa.ask(question)
        return {
            "question": question,
            "memory_matches": memories,
            "document_answer": doc_answer.answer,
            "citations": [asdict(c) for c in doc_answer.citations],
            "confidence": doc_answer.confidence,
        }
