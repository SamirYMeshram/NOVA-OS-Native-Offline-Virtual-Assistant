from __future__ import annotations
from nova.ai.model_manager import ModelManager
from nova.ai.messages import Message
from nova.ai.prompts import DOCUMENT_QA_PROMPT
from nova.ai.providers import EmbeddingProvider
from .vector_store import VectorStore
from .models import Answer

class DocumentQA:
    def __init__(self, store: VectorStore, embedder: EmbeddingProvider, models: ModelManager):
        self.store = store
        self.embedder = embedder
        self.models = models

    def ask(self, question: str, limit: int = 5) -> Answer:
        query_emb = self.embedder.embed([question])[0]
        hits = self.store.search(query_emb, limit=limit)
        if not hits or hits[0].score <= 0:
            return Answer("I could not find this answer in the indexed local documents.", [], 0.0)
        context_parts = []
        citations = []
        for hit in hits:
            citation = f"{hit.chunk.document_path}#chunk-{hit.chunk.index}:{hit.chunk.id}"
            citations.append(citation)
            context_parts.append(f"[citation: {citation} | score={hit.score:.3f}]\n{hit.chunk.text}")
        prompt = f"{DOCUMENT_QA_PROMPT}\n\nQuestion: {question}\n\nContext:\n" + "\n\n".join(context_parts)
        response = self.models.chat([Message('system', DOCUMENT_QA_PROMPT), Message('user', prompt)])
        confidence = max(0.0, min(1.0, hits[0].score))
        return Answer(response, citations, confidence)
