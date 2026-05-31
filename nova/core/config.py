from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .paths import nova_home


@dataclass(slots=True)
class ModelConfig:
    provider: str = "ollama"
    default_model: str = "llama3.1:8b"
    embedding_model: str = "nomic-embed-text"
    ollama_host: str = "http://127.0.0.1:11434"
    timeout_seconds: int = 120
    stream: bool = True


@dataclass(slots=True)
class SecurityConfig:
    require_confirmation_for_write: bool = True
    allow_web_open: bool = False
    protected_roots: list[str] = field(
        default_factory=lambda: ["/etc", "/bin", "/sbin", "/usr", "/var", "/boot", "/sys", "/proc"]
    )
    max_file_read_mb: int = 30
    secrets_redaction: bool = True


@dataclass(slots=True)
class AppConfig:
    app_name: str = "NOVA Sovereign AI"
    mode: str = "normal"  # low-resource | normal | high-performance
    database_path: str = ""
    model: ModelConfig = field(default_factory=ModelConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)

    def __post_init__(self) -> None:
        if not self.database_path:
            self.database_path = str(nova_home() / "nova.sqlite3")


class ConfigManager:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or nova_home() / "config.json"

    def load(self) -> AppConfig:
        if not self.path.exists():
            cfg = AppConfig()
            self.save(cfg)
            return cfg
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return AppConfig(
            app_name=data.get("app_name", "NOVA Sovereign AI"),
            mode=data.get("mode", "normal"),
            database_path=data.get("database_path", ""),
            model=ModelConfig(**data.get("model", {})),
            security=SecurityConfig(**data.get("security", {})),
        )

    def save(self, config: AppConfig) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(asdict(config), indent=2), encoding="utf-8")

    def update(self, **changes: Any) -> AppConfig:
        config = self.load()
        for key, value in changes.items():
            if hasattr(config, key):
                setattr(config, key, value)
        self.save(config)
        return config
