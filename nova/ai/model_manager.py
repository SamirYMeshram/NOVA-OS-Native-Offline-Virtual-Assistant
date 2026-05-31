from __future__ import annotations
from dataclasses import dataclass
from nova.core.config import AIConfig
from .providers import ChatProvider, EmbeddingProvider
from .fallback import FallbackLocalChat, HashEmbeddingProvider
from .ollama import OllamaChatProvider, OllamaEmbeddingProvider
from .messages import Message

@dataclass(slots=True)
class ModelStatus:
    chat_provider: str
    embedding_provider: str
    model: str
    online: bool
    fallback: bool

class ModelManager:
    def __init__(self, config: AIConfig):
        self.config = config
        self.ollama = OllamaChatProvider(config.ollama_host, config.timeout_seconds)
        self.fallback = FallbackLocalChat()
        self.hash_embeddings = HashEmbeddingProvider()

    def chat_provider(self) -> ChatProvider:
        return self.ollama if self.ollama.available() else self.fallback

    def embedding_provider(self) -> EmbeddingProvider:
        if self.ollama.available():
            return OllamaEmbeddingProvider(self.config.ollama_host, self.config.embedding_model, self.config.timeout_seconds)
        return self.hash_embeddings

    def status(self) -> ModelStatus:
        available = self.ollama.available()
        return ModelStatus(
            chat_provider="ollama" if available else "fallback-local",
            embedding_provider="ollama" if available else "hash-embedding",
            model=self.config.default_model,
            online=available,
            fallback=not available,
        )

    def chat(self, messages: list[Message], model: str | None = None) -> str:
        provider = self.chat_provider()
        return provider.chat(messages, model=model or self.config.default_model)
