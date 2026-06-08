from __future__ import annotations

from dataclasses import dataclass
from .index import DocumentIndex

@dataclass(slots=True)
class Flashcard:
    question: str
    answer: str
    source: str


def make_flashcards(index: DocumentIndex, topic: str, count: int = 10) -> list[Flashcard]:
    hits = index.search(topic, top_k=count)
    cards: list[Flashcard] = []
    for hit in hits:
        words = hit.text.split()
        answer = " ".join(words[:35])
        cards.append(Flashcard(f"Explain this key idea from {topic}: {answer[:80]}...", answer, hit.source))
    return cards


def study_notes(index: DocumentIndex, topic: str, count: int = 5) -> str:
    hits = index.search(topic, top_k=count)
    lines = [f"# Study notes: {topic}", ""]
    for i, hit in enumerate(hits, 1):
        lines.append(f"## Point {i} — {hit.source} chunk {hit.index}")
        lines.append(hit.text[:700])
        lines.append("")
    return "\n".join(lines)
