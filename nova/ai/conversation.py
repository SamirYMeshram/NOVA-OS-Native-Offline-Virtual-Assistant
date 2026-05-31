from __future__ import annotations
from dataclasses import dataclass, field
from .messages import Message
from .model_manager import ModelManager
from .prompts import SYSTEM_PROMPT

@dataclass
class Conversation:
    model_manager: ModelManager
    system_prompt: str = SYSTEM_PROMPT
    history: list[Message] = field(default_factory=list)
    max_turns: int = 24

    def ask(self, text: str) -> str:
        messages = [Message("system", self.system_prompt)] + self.history[-self.max_turns:] + [Message("user", text)]
        answer = self.model_manager.chat(messages)
        self.history.append(Message("user", text))
        self.history.append(Message("assistant", answer))
        return answer
