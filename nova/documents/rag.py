from __future__ import annotations

from dataclasses import dataclass
from nova.llm.base import ChatMessage
from nova.llm.prompts import SYSTEM_PROMPT
from nova.llm.ollama import OllamaModel
from .index import DocumentIndex, SearchHit

@dataclass(slots=True)
class Answer:
    text: str
    hits: list[SearchHit]

class RAGEngine:
    def __init__(self, index: DocumentIndex, model: OllamaModel | None = None) -> None:
        self.index = index
        self.model = model

    def answer(self, question: str, top_k: int = 5) -> Answer:
        hits = self.index.search(question, top_k)
        if not hits:
            return Answer("I did not find relevant information in the local document index.", [])
        context = "\n\n".join(f"[S{i+1}] {h.source} chunk {h.index}:\n{h.text}" for i, h in enumerate(hits))
        prompt = (
            "Answer ONLY from the local context. If the answer is not in context, say it is not found. "
            "Cite sources as [S1], [S2].\n\n"
            f"Question: {question}\n\nContext:\n{context}"
        )
        if self.model:
            text = self.model.complete([ChatMessage("user", prompt)], SYSTEM_PROMPT).text
        else:
            # deterministic extractive fallback
            text = "Based on the most relevant local chunks:\n" + "\n".join(
                f"- [S{i+1}] {h.text[:280].replace(chr(10), ' ')}" for i, h in enumerate(hits[:3])
            )
        return Answer(text, hits)
