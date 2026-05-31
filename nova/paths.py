from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

APP_NAME = "nova-sovereign-ai"


def user_home() -> Path:
    return Path.home().expanduser().resolve()


def data_root() -> Path:
    override = os.environ.get("NOVA_HOME")
    if override:
        return Path(override).expanduser().resolve()
    return user_home() / ".nova"


@dataclass(frozen=True)
class NovaPaths:
    root: Path
    config: Path
    database: Path
    index: Path
    logs: Path
    exports: Path
    workspaces: Path
    plugins: Path
    cache: Path

    @classmethod
    def create(cls, root: Path | None = None) -> "NovaPaths":
        base = (root or data_root()).expanduser().resolve()
        item = cls(
            root=base,
            config=base / "config.toml",
            database=base / "nova.sqlite3",
            index=base / "indexes",
            logs=base / "logs",
            exports=base / "exports",
            workspaces=base / "workspaces",
            plugins=base / "plugins",
            cache=base / "cache",
        )
        for folder in [item.root, item.index, item.logs, item.exports, item.workspaces, item.plugins, item.cache]:
            folder.mkdir(parents=True, exist_ok=True)
        return item
