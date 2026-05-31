from __future__ import annotations
from pathlib import Path
from nova.ai.providers import EmbeddingProvider
from nova.security.path_policy import PathPolicy
from .extractor_registry import ExtractorRegistry
from .chunker import TextChunker
from .vector_store import VectorStore

class DocumentIndexer:
    def __init__(self, store: VectorStore, embedder: EmbeddingProvider, path_policy: PathPolicy):
        self.store = store
        self.embedder = embedder
        self.path_policy = path_policy
        self.extractors = ExtractorRegistry()
        self.chunker = TextChunker()

    def iter_files(self, root: Path) -> list[Path]:
        if root.is_file():
            return [root]
        ignored = {'.git', '.venv', 'node_modules', '__pycache__'}
        files: list[Path] = []
        for p in root.rglob('*'):
            if any(part in ignored for part in p.parts):
                continue
            if p.is_file():
                files.append(p)
        return files

    def index_path(self, path: str | Path) -> dict:
        root = self.path_policy.ensure_allowed(path, write=False)
        files = self.iter_files(root)
        total_chunks = 0
        indexed_files = 0
        for f in files:
            doc = self.extractors.extract(f)
            chunks = self.chunker.chunk(str(f), doc.text, doc.metadata)
            if not chunks:
                continue
            embeddings = self.embedder.embed([c.text for c in chunks])
            self.store.upsert(chunks, embeddings)
            total_chunks += len(chunks)
            indexed_files += 1
        return {'indexed_files': indexed_files, 'chunks': total_chunks, 'store_chunks': self.store.count()}
