from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol


@dataclass(slots=True)
class ModelStatus:
    backend: str
    available: bool
    model: str
    message: str


class ChatBackend(Protocol):
    def status(self) -> ModelStatus: ...
    def complete(self, prompt: str, system: str | None = None) -> str: ...
    def stream(self, prompt: str, system: str | None = None) -> Iterable[str]: ...


class EmbeddingBackend(Protocol):
    def embed(self, text: str) -> list[float]: ...
