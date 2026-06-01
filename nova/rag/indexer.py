from __future__ import annotations
from pathlib import Path
from nova.core.security import validate_user_path
from .extractors.registry import ExtractorRegistry
from .chunker import chunk_document
from .vector_store import VectorStore

class DocumentIndexer:
    def __init__(self, store: VectorStore | None = None, registry: ExtractorRegistry | None = None):
        self.store = store or VectorStore()
        self.registry = registry or ExtractorRegistry()

    def iter_files(self, root: Path):
        supported = self.registry.supported_extensions()
        if root.is_file() and root.suffix.lower() in supported:
            yield root
        elif root.is_dir():
            for p in root.rglob('*'):
                if p.is_file() and p.suffix.lower() in supported and not any(part.startswith('.') for part in p.parts[-3:]):
                    yield p

    def index(self, path: str | Path) -> dict:
        root = validate_user_path(path)
        files = list(self.iter_files(root))
        chunks_added = 0
        failed = []
        for file in files:
            try:
                text = self.registry.extract(file)
                chunks = chunk_document(str(file), text)
                self.store.clear_path(str(file))
                self.store.add_chunks(chunks)
                chunks_added += len(chunks)
            except Exception as exc:
                failed.append({'path': str(file), 'error': str(exc)})
        return {'files': len(files), 'chunks': chunks_added, 'failed': failed}
