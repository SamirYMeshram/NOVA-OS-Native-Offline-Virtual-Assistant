from __future__ import annotations

from dataclasses import dataclass

from nova.ai.ollama import OllamaClient
from nova.ai.prompts import DOCUMENT_QA_PROMPT
from nova.documents.index import DocumentIndex
from nova.utils.text import summarize_text


@dataclass(slots=True)
class DocumentAnswer:
    answer: str
    citations: list[str]
    used_model: str


class DocumentQA:
    def __init__(self, index: DocumentIndex | None = None, llm: OllamaClient | None = None) -> None:
        self.index = index or DocumentIndex()
        self.llm = llm or OllamaClient()

    def ask(self, question: str, limit: int = 6) -> DocumentAnswer:
        hits = self.index.search(question, limit=limit)
        if not hits:
            return DocumentAnswer(
                answer="I could not find this answer in the indexed local documents.",
                citations=[],
                used_model="none",
            )
        context = "\n\n".join(
            f"SOURCE: {h.metadata.get('source')} | CHUNK: {h.metadata.get('chunk_id')}\n{h.text}"
            for h in hits
        )
        prompt = f"{DOCUMENT_QA_PROMPT}\n\nCONTEXT:\n{context}\n\nQUESTION:\n{question}"
        response = self.llm.generate(prompt=prompt, system=DOCUMENT_QA_PROMPT)
        if response.used_fallback:
            # deterministic offline answer when no local LLM is running
            answer = summarize_text("\n".join(h.text for h in hits), max_sentences=6)
            answer = "Local model unavailable. Best extracted context summary:\n\n" + answer
        else:
            answer = response.text
        citations = [f"{h.metadata.get('source')} ({h.metadata.get('chunk_id')})" for h in hits]
        return DocumentAnswer(answer=answer, citations=citations, used_model=response.model)
