from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Iterable

from .base import ModelStatus


class OllamaChat:
    """Local Ollama backend using only loopback by default."""

    def __init__(self, base_url: str, model: str, timeout_seconds: int = 120) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds
        if not (self.base_url.startswith("http://127.0.0.1") or self.base_url.startswith("http://localhost")):
            raise ValueError("Ollama base URL must be localhost unless you explicitly modify the code and safety policy.")

    def status(self) -> ModelStatus:
        try:
            req = urllib.request.Request(self.base_url + "/api/tags")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            names = [m.get("name") for m in data.get("models", [])]
            available = self.model in names or any(str(n).startswith(self.model.split(":")[0]) for n in names)
            return ModelStatus("ollama", available, self.model, "Ollama running" if available else f"Ollama running but model {self.model!r} not found")
        except Exception as exc:  # noqa: BLE001
            return ModelStatus("ollama", False, self.model, f"Ollama unavailable: {exc}")

    def complete(self, prompt: str, system: str | None = None) -> str:
        payload = {"model": self.model, "prompt": prompt, "system": system or "", "stream": False}
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url + "/api/generate", data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return str(data.get("response", "")).strip()
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Ollama request failed: {exc}") from exc

    def stream(self, prompt: str, system: str | None = None) -> Iterable[str]:
        payload = {"model": self.model, "prompt": prompt, "system": system or "", "stream": True}
        req = urllib.request.Request(self.base_url + "/api/generate", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
            for raw in resp:
                if not raw.strip():
                    continue
                item = json.loads(raw.decode("utf-8"))
                if "response" in item:
                    yield str(item["response"])


class OllamaEmbedder:
    def __init__(self, base_url: str, model: str, timeout_seconds: int = 60) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds
        if not (self.base_url.startswith("http://127.0.0.1") or self.base_url.startswith("http://localhost")):
            raise ValueError("Ollama embeddings must use localhost by default.")

    def embed(self, text: str) -> list[float]:
        payload = {"model": self.model, "prompt": text}
        req = urllib.request.Request(self.base_url + "/api/embeddings", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return [float(x) for x in data.get("embedding", [])]
