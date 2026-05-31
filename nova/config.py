from __future__ import annotations

import tomllib
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from .paths import NovaPaths


def _toml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(v) for v in value) + "]"
    return repr(str(value))


def _write_simple_toml(path: Path, data: dict[str, Any]) -> None:
    lines: list[str] = []
    for section, values in data.items():
        lines.append(f"[{section}]")
        for key, value in values.items():
            lines.append(f"{key} = {_toml_value(value)}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


@dataclass(slots=True)
class ModelConfig:
    backend: str = "ollama"
    chat_model: str = "llama3.2:3b"
    embedding_model: str = "nomic-embed-text"
    ollama_base_url: str = "http://127.0.0.1:11434"
    timeout_seconds: int = 120
    allow_network: bool = False


@dataclass(slots=True)
class SafetyConfig:
    require_confirmation_for_file_changes: bool = True
    protected_paths: list[str] = field(default_factory=lambda: ["/", "/bin", "/boot", "/dev", "/etc", "/proc", "/root", "/sys", "/usr", "/var"])
    max_file_read_mb: int = 30
    allow_shell: bool = False
    audit_redaction: bool = True


@dataclass(slots=True)
class DashboardConfig:
    host: str = "127.0.0.1"
    port: int = 8501


@dataclass(slots=True)
class NovaConfig:
    model: ModelConfig = field(default_factory=ModelConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)
    dashboard: DashboardConfig = field(default_factory=DashboardConfig)

    @classmethod
    def load(cls, paths: NovaPaths | None = None) -> "NovaConfig":
        paths = paths or NovaPaths.create()
        if not paths.config.exists():
            cfg = cls()
            cfg.save(paths)
            return cfg
        raw = tomllib.loads(paths.config.read_text(encoding="utf-8"))
        return cls(
            model=ModelConfig(**raw.get("model", {})),
            safety=SafetyConfig(**raw.get("safety", {})),
            dashboard=DashboardConfig(**raw.get("dashboard", {})),
        )

    def save(self, paths: NovaPaths | None = None) -> None:
        paths = paths or NovaPaths.create()
        data = asdict(self)
        _write_simple_toml(paths.config, data)
