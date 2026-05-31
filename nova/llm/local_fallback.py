from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from typing import Iterable

from .base import ModelStatus


class LocalFallbackChat:
    """Deterministic no-network fallback when Ollama is unavailable."""

    def status(self) -> ModelStatus:
        return ModelStatus("fallback", True, "deterministic-local", "Ollama unavailable; using safe deterministic local fallback.")

    def complete(self, prompt: str, system: str | None = None) -> str:
        prompt = prompt.strip()
        if not prompt:
            return "I am NOVA. Give me a command, document question, file scan request, task, or automation plan."
        if "organize" in prompt.lower() or "clean" in prompt.lower():
            return "I can scan the folder, classify files, create a reversible move plan, and ask for confirmation before changing anything."
        if "document" in prompt.lower() or "pdf" in prompt.lower():
            return "Index documents with `nova docs index <path>`, then ask with `nova docs ask <question>`. Answers cite local chunks."
        return (
            "Local model is not connected, so this is NOVA's deterministic fallback. "
            "Install/start Ollama and pull a model for full AI responses: `ollama pull llama3.2:3b`. "
            f"Your request was: {prompt}"
        )

    def stream(self, prompt: str, system: str | None = None) -> Iterable[str]:
        for word in self.complete(prompt, system).split():
            yield word + " "


class HashingEmbedder:
    """Small local embedding fallback using hashing TF features. No model download needed."""

    def __init__(self, dims: int = 384) -> None:
        self.dims = dims

    def embed(self, text: str) -> list[float]:
        tokens = re.findall(r"[a-zA-Z0-9_]+", text.lower())
        vec = [0.0] * self.dims
        counts = Counter(tokens)
        for token, count in counts.items():
            h = int(hashlib.sha256(token.encode()).hexdigest(), 16)
            idx = h % self.dims
            sign = -1.0 if (h >> 8) % 2 else 1.0
            vec[idx] += sign * (1.0 + math.log(count))
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]
