from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..llm.manager import LocalModelManager
from ..paths import NovaPaths
from .chunker import SmartChunker
from .loaders import SUPPORTED_EXTS, DocumentLoader
from .vector_store import VectorStore


@dataclass(slots=True)
class IndexReport:
    indexed_files: int
    skipped_files: int
    failed_files: int
    chunks: int
    failures: list[str]


class DocumentIndexer:
    def __init__(self, paths: NovaPaths | None = None, model_manager: LocalModelManager | None = None) -> None:
        self.paths = paths or NovaPaths.create()
        self.model_manager = model_manager or LocalModelManager()
        self.loader = DocumentLoader()
        self.chunker = SmartChunker()
        self.store = VectorStore(self.paths.index / "documents.sqlite3")

    def index_path(self, path: str | Path, force: bool = False) -> IndexReport:
        p = Path(path).expanduser().resolve()
        files = self._iter_files(p)
        indexed = skipped = failed = chunks_total = 0
        failures: list[str] = []
        for file_path in files:
            try:
                if not force and self.store.is_current(file_path):
                    skipped += 1
                    continue
                doc = self.loader.load(file_path)
                chunks = self.chunker.chunk(doc)
                embeddings = [self.model_manager.embed(chunk.text) for chunk in chunks]
                self.store.upsert_file(file_path, chunks, embeddings)
                indexed += 1
                chunks_total += len(chunks)
            except Exception as exc:  # noqa: BLE001
                failed += 1
                failures.append(f"{file_path}: {exc}")
        return IndexReport(indexed, skipped, failed, chunks_total, failures)

    def _iter_files(self, p: Path) -> list[Path]:
        if p.is_file():
            return [p] if p.suffix.lower() in SUPPORTED_EXTS else []
        if p.is_dir():
            result: list[Path] = []
            for child in p.rglob("*"):
                if child.is_file() and child.suffix.lower() in SUPPORTED_EXTS and not any(part.startswith(".") for part in child.parts[-3:]):
                    result.append(child)
            return result
        raise FileNotFoundError(p)
