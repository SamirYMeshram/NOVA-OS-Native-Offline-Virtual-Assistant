from __future__ import annotations
import re
from .vector_store import VectorStore

class StudyToolkit:
    def __init__(self, store: VectorStore):
        self.store = store

    def make_flashcards_from_text(self, text: str, limit: int = 12) -> list[dict[str, str]]:
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 40]
        cards = []
        for s in sentences[:limit]:
            keyword = next((w for w in s.split() if len(w) > 6), s.split()[0])
            cards.append({'front': f'Explain: {keyword}', 'back': s})
        return cards

    def study_plan(self, topic: str, days: int = 7) -> list[str]:
        return [f"Day {i}: Study {topic} section {i}, create notes, solve 10 practice questions, review mistakes." for i in range(1, days+1)]
