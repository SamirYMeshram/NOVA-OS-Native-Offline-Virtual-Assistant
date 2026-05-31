from __future__ import annotations

from ..config import ModelConfig
from .base import ModelStatus
from .local_fallback import HashingEmbedder, LocalFallbackChat
from .ollama import OllamaChat, OllamaEmbedder


class LocalModelManager:
    def __init__(self, config: ModelConfig | None = None) -> None:
        self.config = config or ModelConfig()
        self.fallback = LocalFallbackChat()
        self._chat = None
        self._embedder = None

    @property
    def chat(self):
        if self._chat is None:
            if self.config.backend == "ollama":
                try:
                    backend = OllamaChat(self.config.ollama_base_url, self.config.chat_model, self.config.timeout_seconds)
                    if backend.status().available:
                        self._chat = backend
                    else:
                        self._chat = self.fallback
                except Exception:  # noqa: BLE001
                    self._chat = self.fallback
            else:
                self._chat = self.fallback
        return self._chat

    @property
    def embedder(self):
        if self._embedder is None:
            if self.config.backend == "ollama":
                try:
                    self._embedder = OllamaEmbedder(self.config.ollama_base_url, self.config.embedding_model)
                    # probe quickly; fall back if unavailable
                    vec = self._embedder.embed("probe")
                    if not vec:
                        self._embedder = HashingEmbedder()
                except Exception:  # noqa: BLE001
                    self._embedder = HashingEmbedder()
            else:
                self._embedder = HashingEmbedder()
        return self._embedder

    def status(self) -> ModelStatus:
        return self.chat.status()

    def complete(self, prompt: str, system: str | None = None) -> str:
        try:
            return self.chat.complete(prompt, system)
        except Exception as exc:  # noqa: BLE001
            return self.fallback.complete(prompt + f"\n\n[Local model failed: {exc}]", system)

    def stream(self, prompt: str, system: str | None = None):
        try:
            yield from self.chat.stream(prompt, system)
        except Exception:
            yield from self.fallback.stream(prompt, system)

    def embed(self, text: str) -> list[float]:
        return self.embedder.embed(text)
