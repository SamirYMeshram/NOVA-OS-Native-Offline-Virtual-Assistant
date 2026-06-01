from __future__ import annotations
from pathlib import Path
import os

APP_NAME = "nova-sovereign-ai"

def home_dir() -> Path:
    return Path.home()

def data_dir() -> Path:
    override = os.environ.get("NOVA_HOME")
    path = Path(override).expanduser() if override else Path.home() / ".nova"
    path.mkdir(parents=True, exist_ok=True)
    return path

def logs_dir() -> Path:
    p = data_dir() / "logs"
    p.mkdir(parents=True, exist_ok=True)
    return p

def db_path(name: str = "nova.sqlite3") -> Path:
    return data_dir() / name

def safe_resolve(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()
