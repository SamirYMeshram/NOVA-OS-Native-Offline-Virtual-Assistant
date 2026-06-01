from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable
from .messages import Message

class ChatProvider(ABC):
    name: str

    @abstractmethod
    def available(self) -> bool: ...

    @abstractmethod
    def chat(self, messages: list[Message], *, model: str | None = None, stream: bool = False) -> str: ...

    def stream_chat(self, messages: list[Message], *, model: str | None = None) -> Iterable[str]:
        yield self.chat(messages, model=model, stream=False)
