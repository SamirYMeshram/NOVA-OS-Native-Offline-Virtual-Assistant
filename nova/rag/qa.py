from __future__ import annotations
from nova.ai.model_manager import ModelManager
from .vector_store import VectorStore

class DocumentQA:
    def __init__(self, store: VectorStore | None = None, model: ModelManager | None = None):
        self.store = store or VectorStore()
        self.model = model or ModelManager()

    def ask(self, question: str, limit: int = 5) -> dict:
        hits = self.store.search(question, limit=limit)
        if not hits:
            return {'answer': 'I could not find this in the indexed local documents.', 'sources': []}
        context = "\n\n".join(f"SOURCE {i+1}: {h.path}#chunk-{h.chunk_index}\n{h.text}" for i, h in enumerate(hits))
        prompt = f"Answer only from this local retrieved context. If missing, say it is not found.\n\n{context}\n\nQuestion: {question}"
        answer = self.model.chat(prompt)
        sources = [{'path': h.path, 'chunk': h.chunk_index, 'score': round(h.score, 4), 'preview': h.text[:240]} for h in hits]
        return {'answer': answer, 'sources': sources}
