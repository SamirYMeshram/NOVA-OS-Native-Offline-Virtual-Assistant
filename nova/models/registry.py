from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json, time
from nova.llm.ollama import OllamaModel

@dataclass(slots=True)
class ModelProfile:
    name: str
    provider: str
    purpose: str
    context: int = 4096
    enabled: bool = True
    last_checked: float | None = None
    healthy: bool | None = None

class ModelRegistry:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            self.save([
                ModelProfile("llama3.2:3b", "ollama", "general chat", 8192),
                ModelProfile("qwen2.5-coder:7b", "ollama", "coding", 8192, enabled=False),
                ModelProfile("nomic-embed-text", "ollama", "embeddings", 2048),
                ModelProfile("nova-offline-fallback", "fallback", "offline deterministic fallback", 2048),
            ])

    def load(self) -> list[ModelProfile]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [ModelProfile(**item) for item in data]

    def save(self, models: list[ModelProfile]) -> None:
        self.path.write_text(json.dumps([asdict(m) for m in models], indent=2), encoding="utf-8")

    def add(self, profile: ModelProfile) -> None:
        models = [m for m in self.load() if not (m.name == profile.name and m.provider == profile.provider)]
        models.append(profile); self.save(models)

    def choose(self, purpose: str = "general") -> ModelProfile:
        models = [m for m in self.load() if m.enabled]
        for m in models:
            if purpose.lower() in m.purpose.lower(): return m
        return models[0]

    def health_check(self, base_url: str = "http://127.0.0.1:11434") -> list[ModelProfile]:
        models = self.load()
        health = OllamaModel(base_url=base_url).health()
        available = set(health.get("models", [])) if health.get("ok") else set()
        now = time.time()
        for m in models:
            m.last_checked = now
            m.healthy = True if m.provider == "fallback" else m.name in available
        self.save(models)
        return models
