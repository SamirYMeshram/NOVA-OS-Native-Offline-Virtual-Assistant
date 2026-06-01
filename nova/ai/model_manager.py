from __future__ import annotations
from .messages import Message
from .fallback import FallbackChatProvider
from .ollama import OllamaProvider
from .prompts import SYSTEM_PROMPT
from nova.core.config import NovaConfig
from nova.core.audit import AuditLog

class ModelManager:
    def __init__(self, config: NovaConfig | None = None, audit: AuditLog | None = None):
        self.config = config or NovaConfig.load()
        self.audit = audit or AuditLog()
        self.providers = [OllamaProvider(), FallbackChatProvider()]

    def provider_status(self) -> list[dict]:
        return [{"name": p.name, "available": p.available()} for p in self.providers]

    def chat(self, user_text: str, *, system: str | None = None, history: list[Message] | None = None) -> str:
        messages = [Message("system", system or SYSTEM_PROMPT)]
        messages.extend(history or [])
        messages.append(Message("user", user_text))
        for provider in self.providers:
            if not provider.available():
                continue
            try:
                out = provider.chat(messages, model=self.config.model)
                self.audit.write("ai.chat", "ok", provider=provider.name, model=self.config.model)
                return out
            except Exception as exc:
                self.audit.write("ai.chat", "fallback", provider=provider.name, error=str(exc))
        return FallbackChatProvider().chat(messages)
