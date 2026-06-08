from __future__ import annotations

from pathlib import Path
import shutil, subprocess, sys, os
from nova.security.path_guard import decide_path
from nova.config import NovaConfig

class SafeActions:
    def __init__(self, config: NovaConfig) -> None:
        self.config = config

    def create_folder(self, path: str | Path, dry_run: bool = True) -> dict[str, object]:
        dec = decide_path(path, "create_folder")
        if not dec.allowed: raise PermissionError(dec.reason)
        if not dry_run: dec.path.mkdir(parents=True, exist_ok=True)
        return {"action": "create_folder", "path": str(dec.path), "dry_run": dry_run}

    def create_file(self, path: str | Path, content: str = "", dry_run: bool = True) -> dict[str, object]:
        dec = decide_path(path, "create_file")
        if not dec.allowed: raise PermissionError(dec.reason)
        if dec.path.exists() and not dry_run: raise FileExistsError(f"Refusing overwrite: {dec.path}")
        if not dry_run:
            dec.path.parent.mkdir(parents=True, exist_ok=True)
            dec.path.write_text(content, encoding="utf-8")
        return {"action": "create_file", "path": str(dec.path), "bytes": len(content.encode()), "dry_run": dry_run}

    def move_file(self, source: str | Path, destination: str | Path, dry_run: bool = True) -> dict[str, object]:
        s = decide_path(source, "move_source"); d = decide_path(destination, "move_destination")
        if not s.allowed: raise PermissionError(s.reason)
        if not d.allowed: raise PermissionError(d.reason)
        if not dry_run:
            d.path.parent.mkdir(parents=True, exist_ok=True)
            if d.path.exists(): raise FileExistsError(f"Refusing overwrite: {d.path}")
            shutil.move(str(s.path), str(d.path))
        return {"action": "move_file", "source": str(s.path), "destination": str(d.path), "dry_run": dry_run}

    def open_folder(self, path: str | Path, dry_run: bool = True) -> dict[str, object]:
        dec = decide_path(path, "open_folder")
        if not dec.allowed: raise PermissionError(dec.reason)
        if not dry_run:
            if sys.platform.startswith("linux"): subprocess.Popen(["xdg-open", str(dec.path)])
            elif sys.platform == "darwin": subprocess.Popen(["open", str(dec.path)])
            elif os.name == "nt": os.startfile(str(dec.path))  # type: ignore[attr-defined]
        return {"action": "open_folder", "path": str(dec.path), "dry_run": dry_run}
