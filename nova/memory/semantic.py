from __future__ import annotations

from dataclasses import dataclass, asdict
from nova.documents.vector import embed, cosine
from nova.memory.store import MemoryStore, Memory

@dataclass(slots=True)
class SemanticMemoryHit:
    memory: Memory
    score: float


def semantic_search(store: MemoryStore, query: str, limit: int = 10, pool: int = 200) -> list[SemanticMemoryHit]:
    q = embed(query)
    hits=[]
    for m in store.list(pool):
        score = cosine(q, embed(m.text + " " + m.tags))
        hits.append(SemanticMemoryHit(m, score))
    hits.sort(key=lambda h: h.score, reverse=True)
    return hits[:limit]
