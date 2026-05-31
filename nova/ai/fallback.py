from __future__ import annotations
import hashlib, math
from .providers import ChatProvider, EmbeddingProvider
from .messages import Message

class FallbackLocalChat(ChatProvider):
    name = "fallback-local"

    def available(self) -> bool:
        return True

    def chat(self, messages: list[Message], model: str | None = None) -> str:
        user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        lowered = user.lower()
        if "what can you do" in lowered or "capabilities" in lowered:
            return (
                "I am NOVA in offline fallback mode. I can route commands, store/search memory, "
                "index local documents, scan files, create safe cleanup plans, profile CSV/JSON data, "
                "generate local project templates, manage tasks/reminders, and load plugins. Install Ollama "
                "for stronger local language reasoning."
            )
        if "remember" in lowered:
            return "I can save that locally through the memory tool."
        return (
            "NOVA fallback response: local model unavailable, but the platform is running. "
            "Use `ollama pull llama3.2:3b` and start Ollama for richer local chat. Your request was: " + user[:500]
        )

class HashEmbeddingProvider(EmbeddingProvider):
    """Deterministic offline embedding using hashed token buckets. No external dependency."""
    def __init__(self, dimensions: int = 256):
        self.dimensions = dimensions

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            vec = [0.0] * self.dimensions
            for raw in text.lower().split():
                token = ''.join(ch for ch in raw if ch.isalnum())
                if not token:
                    continue
                digest = hashlib.sha256(token.encode()).digest()
                idx = int.from_bytes(digest[:4], 'big') % self.dimensions
                sign = 1.0 if digest[4] % 2 == 0 else -1.0
                vec[idx] += sign
            norm = math.sqrt(sum(v*v for v in vec)) or 1.0
            vectors.append([v/norm for v in vec])
        return vectors
