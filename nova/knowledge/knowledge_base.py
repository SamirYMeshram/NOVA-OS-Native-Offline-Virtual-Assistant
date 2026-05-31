from __future__ import annotations
from pathlib import Path
from nova.memory.store import MemoryStore

class KnowledgeBase:
    def __init__(self, data_dir: Path):
        self.store = MemoryStore(data_dir / 'nova_memory.sqlite')

    def add_note(self, title: str, body: str, tags: list[str] | None = None) -> int:
        return self.store.add('note', title, body, tags or ['knowledge'])

    def search(self, query: str) -> str:
        hits = self.store.search(query, limit=10)
        return '\n'.join(f'- {h.key}: {h.value[:300]}' for h in hits) or 'No notes found.'
