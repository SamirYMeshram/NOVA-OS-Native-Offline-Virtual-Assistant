from __future__ import annotations

import os
from pathlib import Path

APP_DIR_ENV = "NOVA_HOME"


def nova_home() -> Path:
    """Return NOVA's local data directory, creating it when needed."""
    raw = os.environ.get(APP_DIR_ENV)
    base = Path(raw).expanduser() if raw else Path.home() / ".nova"
    base.mkdir(parents=True, exist_ok=True)
    for child in ["indexes", "logs", "exports", "undo", "reports", "workspaces"]:
        (base / child).mkdir(exist_ok=True)
    return base


def safe_resolve(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def relative_to_or_name(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return path.name
