from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Iterator
from .messages import Message

class ChatProvider(ABC):
    name: str

    @abstractmethod
    def available(self) -> bool: ...

    @abstractmethod
    def chat(self, messages: list[Message], model: str | None = None) -> str: ...

    def stream(self, messages: list[Message], model: str | None = None) -> Iterator[str]:
        yield self.chat(messages, model=model)

class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]: ...
