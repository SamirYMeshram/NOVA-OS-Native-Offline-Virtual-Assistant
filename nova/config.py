from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os


def _default_home() -> Path:
    return Path(os.environ.get("NOVA_HOME", Path.home() / ".nova")).expanduser().resolve()


@dataclass(slots=True)
class ModelConfig:
    provider: str = "ollama"
    chat_model: str = "llama3.2:3b"
    embed_model: str = "nomic-embed-text"
    ollama_base_url: str = "http://127.0.0.1:11434"
    timeout_seconds: float = 30.0


@dataclass(slots=True)
class SafetyConfig:
    confirm_token: str = "YES_NOVA_ACT"
    max_file_read_bytes: int = 2_000_000
    max_scan_files: int = 20_000
    allow_open_websites: bool = False
    allow_app_launch: bool = True
    allow_file_write: bool = True
    allow_file_move: bool = True
    allow_delete: bool = False


@dataclass(slots=True)
class NovaConfig:
    home: Path = field(default_factory=_default_home)
    model: ModelConfig = field(default_factory=ModelConfig)
    safety: SafetyConfig = field(default_factory=SafetyConfig)

    @property
    def db_path(self) -> Path:
        return self.home / "nova.sqlite3"

    @property
    def index_dir(self) -> Path:
        return self.home / "indexes"

    @property
    def log_dir(self) -> Path:
        return self.home / "logs"

    @property
    def workspace_dir(self) -> Path:
        return self.home / "workspace"

    def ensure_dirs(self) -> None:
        for path in [self.home, self.index_dir, self.log_dir, self.workspace_dir]:
            path.mkdir(parents=True, exist_ok=True)


def load_config() -> NovaConfig:
    cfg = NovaConfig()
    cfg.ensure_dirs()
    return cfg
