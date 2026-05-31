from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Iterable

import requests

from nova.core.config import ModelConfig

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ModelResponse:
    text: str
    provider: str
    model: str
    used_fallback: bool = False


class OllamaClient:
    """Tiny local Ollama adapter with graceful fallback behavior."""

    def __init__(self, config: ModelConfig | None = None) -> None:
        self.config = config or ModelConfig()

    def available(self) -> bool:
        try:
            response = requests.get(f"{self.config.ollama_host}/api/tags", timeout=3)
            return response.ok
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        try:
            response = requests.get(f"{self.config.ollama_host}/api/tags", timeout=5)
            response.raise_for_status()
            payload = response.json()
            return [m.get("name", "") for m in payload.get("models", []) if m.get("name")]
        except requests.RequestException:
            return []

    def generate(self, prompt: str, system: str = "", model: str | None = None) -> ModelResponse:
        selected = model or self.config.default_model
        if not self.available():
            return ModelResponse(
                text=self._fallback(prompt), provider="fallback", model="offline-rule-engine", used_fallback=True
            )
        payload = {
            "model": selected,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {"temperature": 0.35, "num_ctx": 8192},
        }
        try:
            response = requests.post(
                f"{self.config.ollama_host}/api/generate",
                json=payload,
                timeout=self.config.timeout_seconds,
            )
            response.raise_for_status()
            return ModelResponse(text=response.json().get("response", ""), provider="ollama", model=selected)
        except requests.RequestException as exc:
            logger.warning("Ollama generation failed: %s", exc)
            return ModelResponse(
                text=self._fallback(prompt), provider="fallback", model="offline-rule-engine", used_fallback=True
            )

    def stream(self, prompt: str, system: str = "", model: str | None = None) -> Iterable[str]:
        selected = model or self.config.default_model
        if not self.available():
            yield self._fallback(prompt)
            return
        payload = {"model": selected, "prompt": prompt, "system": system, "stream": True}
        try:
            with requests.post(
                f"{self.config.ollama_host}/api/generate",
                json=payload,
                timeout=self.config.timeout_seconds,
                stream=True,
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if not line:
                        continue
                    event = json.loads(line.decode("utf-8"))
                    if event.get("response"):
                        yield event["response"]
                    if event.get("done"):
                        break
        except requests.RequestException:
            yield self._fallback(prompt)

    def embed(self, text: str, model: str | None = None) -> list[float] | None:
        selected = model or self.config.embedding_model
        if not self.available():
            return None
        try:
            response = requests.post(
                f"{self.config.ollama_host}/api/embeddings",
                json={"model": selected, "prompt": text},
                timeout=60,
            )
            response.raise_for_status()
            return response.json().get("embedding")
        except requests.RequestException:
            return None

    @staticmethod
    def _fallback(prompt: str) -> str:
        return (
            "Local model is not reachable yet. NOVA can still use memory, document search, "
            "file intelligence, tasks, and safe automation. Install/start Ollama and pull a model, "
            "for example: `ollama pull llama3.1:8b`, then retry.\n\n"
            f"I received your request: {prompt[:1200]}"
        )
