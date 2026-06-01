from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json, os
from .paths import data_dir

@dataclass(slots=True)
class NovaConfig:
    model: str = "llama3.2:3b"
    embedding_model: str = "nomic-embed-text"
    offline_only: bool = True
    low_resource_mode: bool = True
    require_confirmation_for_file_changes: bool = True
    enable_voice_transcript_storage: bool = False
    allowed_roots: list[str] | None = None
    blocked_roots: list[str] | None = None

    @classmethod
    def default(cls) -> "NovaConfig":
        return cls(allowed_roots=[str(Path.home())], blocked_roots=["/", "/etc", "/usr", "/bin", "/sbin", "/var", "/boot"])

    @classmethod
    def load(cls, path: Path | None = None) -> "NovaConfig":
        path = path or data_dir() / "config.json"
        if not path.exists():
            cfg = cls.default()
            cfg.save(path)
            return cfg
        data = json.loads(path.read_text(encoding="utf-8"))
        base = asdict(cls.default())
        base.update(data)
        return cls(**base)

    def save(self, path: Path | None = None) -> None:
        path = path or data_dir() / "config.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
