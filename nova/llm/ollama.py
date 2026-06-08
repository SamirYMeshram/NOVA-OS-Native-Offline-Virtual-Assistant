from __future__ import annotations

import json
import urllib.request
import urllib.error
from .base import ChatMessage, ModelReply
from .fallback import FallbackModel


class OllamaModel:
    def __init__(self, model: str = "llama3.2:3b", base_url: str = "http://127.0.0.1:11434", timeout: float = 30.0) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.fallback = FallbackModel()

    def _payload(self, messages: list[ChatMessage], system: str | None) -> bytes:
        items = []
        if system:
            items.append({"role": "system", "content": system})
        items.extend({"role": m.role, "content": m.content} for m in messages)
        return json.dumps({"model": self.model, "messages": items, "stream": False}).encode("utf-8")

    def complete(self, messages: list[ChatMessage], system: str | None = None) -> ModelReply:
        req = urllib.request.Request(
            self.base_url + "/api/chat",
            data=self._payload(messages, system),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return ModelReply(data.get("message", {}).get("content", ""), self.model, "ollama", False)
        except Exception:
            return self.fallback.complete(messages, system)

    def stream(self, messages: list[ChatMessage], system: str | None = None):
        # For reliability in core, stream the completed response if the Ollama stream endpoint is unavailable.
        for token in self.complete(messages, system).text.split():
            yield token + " "

    def health(self) -> dict[str, object]:
        try:
            with urllib.request.urlopen(self.base_url + "/api/tags", timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("name") for m in data.get("models", [])]
            return {"ok": True, "models": models, "selected": self.model}
        except Exception as exc:
            return {"ok": False, "error": str(exc), "selected": self.model}
