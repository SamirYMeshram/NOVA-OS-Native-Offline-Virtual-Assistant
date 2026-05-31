from __future__ import annotations

from pathlib import Path

from ..llm.manager import LocalModelManager
from .chunker import SmartChunker
from .loaders import DocumentLoader


class DocumentSummarizer:
    def __init__(self, model_manager: LocalModelManager | None = None) -> None:
        self.model_manager = model_manager or LocalModelManager()
        self.loader = DocumentLoader()
        self.chunker = SmartChunker(target_chars=2200, overlap_chars=120)

    def summarize(self, path: str | Path) -> str:
        doc = self.loader.load(path)
        chunks = self.chunker.chunk(doc)[:12]
        notes = []
        for chunk in chunks:
            prompt = f"Summarize this local document chunk into key points, tasks, dates, and definitions:\n\n{chunk.text}"
            notes.append(self.model_manager.complete(prompt))
        combined = "\n\n".join(notes)
        return self.model_manager.complete("Create one clean final summary with bullet points and important dates:\n\n" + combined)
