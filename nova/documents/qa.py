from __future__ import annotations

from ..llm.manager import LocalModelManager
from ..llm.prompts import DOCUMENT_QA_PROMPT
from ..paths import NovaPaths
from .models import Citation, QAAnswer
from .vector_store import VectorStore


class DocumentQA:
    def __init__(self, paths: NovaPaths | None = None, model_manager: LocalModelManager | None = None) -> None:
        self.paths = paths or NovaPaths.create()
        self.model_manager = model_manager or LocalModelManager()
        self.store = VectorStore(self.paths.index / "documents.sqlite3")

    def ask(self, question: str, limit: int = 6) -> QAAnswer:
        query_embedding = self.model_manager.embed(question)
        chunks = self.store.search(query_embedding, limit=limit)
        if not chunks:
            return QAAnswer("I could not find relevant content in the local document index. Index documents first with `nova docs index <path>`.", [], 0.0)
        context = "\n\n".join(
            f"[Chunk {idx + 1} | id={chunk['id']} | source={chunk['source_path']} | score={chunk['score']:.3f}]\n{chunk['text']}"
            for idx, chunk in enumerate(chunks)
        )
        prompt = f"Question: {question}\n\nLocal context:\n{context}\n\nAnswer with citations."
        answer = self.model_manager.complete(prompt, system=DOCUMENT_QA_PROMPT)
        citations = [Citation(chunk["id"], chunk["source_path"], chunk["text"][:240].replace("\n", " ")) for chunk in chunks]
        return QAAnswer(answer, citations, confidence=max(float(chunks[0].get("score", 0.0)), 0.1))
