from __future__ import annotations
from pathlib import Path
import os

APP_NAME = "nova-sovereign-ai"

def expand(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()

def default_data_dir() -> Path:
    raw = os.environ.get("NOVA_DATA_DIR")
    if raw:
        return expand(raw)
    return Path.home() / ".nova"

def ensure_dir(path: str | Path) -> Path:
    p = expand(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def project_root() -> Path:
    return Path(__file__).resolve().parents[2]
