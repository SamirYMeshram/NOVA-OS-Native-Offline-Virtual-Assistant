from __future__ import annotations

from dataclasses import dataclass, field
from .base import ChatMessage


@dataclass
class Conversation:
    max_messages: int = 30
    messages: list[ChatMessage] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self.messages.append(ChatMessage(role, content))
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
