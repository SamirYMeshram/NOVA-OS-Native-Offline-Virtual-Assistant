from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Iterable


@dataclass(slots=True)
class ChatMessage:
    role: str
    content: str


@dataclass(slots=True)
class ModelReply:
    text: str
    model: str
    provider: str
    fallback: bool = False


class ChatModel(Protocol):
    def complete(self, messages: list[ChatMessage], system: str | None = None) -> ModelReply: ...
    def stream(self, messages: list[ChatMessage], system: str | None = None) -> Iterable[str]: ...
