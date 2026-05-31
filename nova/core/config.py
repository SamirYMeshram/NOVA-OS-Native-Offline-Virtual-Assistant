from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import os
from .paths import default_data_dir, ensure_dir

@dataclass(slots=True)
class AIConfig:
    provider: str = "ollama"
    default_model: str = field(default_factory=lambda: os.environ.get("NOVA_MODEL", "llama3.2:3b"))
    embedding_model: str = field(default_factory=lambda: os.environ.get("NOVA_EMBED_MODEL", "nomic-embed-text"))
    ollama_host: str = field(default_factory=lambda: os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"))
    timeout_seconds: float = 10.0
    allow_network: bool = False

@dataclass(slots=True)
class SecurityConfig:
    require_confirmation_for_file_writes: bool = True
    require_confirmation_for_shell: bool = True
    protected_paths: tuple[str, ...] = (
        "/", "/etc", "/usr", "/bin", "/sbin", "/boot", "/proc", "/sys", "/dev",
        "C:/Windows", "C:/Program Files", "C:/Program Files (x86)",
    )
    max_file_read_mb: int = 25

@dataclass(slots=True)
class NovaConfig:
    data_dir: Path = field(default_factory=default_data_dir)
    profile: str = "normal"  # low-resource | normal | high-performance
    ai: AIConfig = field(default_factory=AIConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    audit_log: bool = True

    def prepare(self) -> "NovaConfig":
        ensure_dir(self.data_dir)
        ensure_dir(self.data_dir / "indexes")
        ensure_dir(self.data_dir / "logs")
        ensure_dir(self.data_dir / "reports")
        ensure_dir(self.data_dir / "undo")
        return self

def load_config() -> NovaConfig:
    # Standard-library config loader; pyproject optional TOML parsing can be added later.
    return NovaConfig().prepare()
