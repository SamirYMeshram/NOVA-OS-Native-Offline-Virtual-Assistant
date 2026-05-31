from __future__ import annotations
from pathlib import Path
from .store import MemoryStore

class MemoryService:
    def __init__(self, data_dir: Path):
        self.store = MemoryStore(data_dir / "nova_memory.sqlite")

    def remember_from_text(self, text: str) -> int:
        lowered = text.lower()
        key = "note"
        value = text
        if "remember that" in lowered:
            value = text[lowered.index("remember that") + len("remember that"):].strip()
            key = value.split(" ", 5)[:5]
            key = " ".join(key) or "memory"
        return self.store.add("fact", str(key), value, tags=["chat"])

    def recall(self, query: str, limit: int = 5) -> str:
        hits = self.store.search(query, limit=limit)
        if not hits:
            return "No matching local memories found."
        return "\n".join(f"- [{m.kind}] {m.key}: {m.value}" for m in hits)
