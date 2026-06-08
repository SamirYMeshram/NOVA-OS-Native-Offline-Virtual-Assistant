from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json, time
from nova.security.path_guard import decide_path

@dataclass(slots=True)
class Workspace:
    name: str
    path: str
    purpose: str
    created_at: float

class WorkspaceManager:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.registry = self.root / "workspaces.json"
        if not self.registry.exists(): self.registry.write_text("[]", encoding="utf-8")

    def list(self) -> list[Workspace]:
        return [Workspace(**x) for x in json.loads(self.registry.read_text(encoding="utf-8"))]

    def create(self, name: str, purpose: str = "general", dry_run: bool = True) -> dict[str, object]:
        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name).strip("_") or "workspace"
        path = self.root / safe_name
        dec = decide_path(path, "create_workspace")
        if not dec.allowed: raise PermissionError(dec.reason)
        ws = Workspace(safe_name, str(dec.path), purpose, time.time())
        if dry_run:
            return {"dry_run": True, "workspace": asdict(ws), "folders": ["docs", "data", "reports", "projects", "logs"]}
        dec.path.mkdir(parents=True, exist_ok=True)
        for d in ["docs", "data", "reports", "projects", "logs"]:
            (dec.path / d).mkdir(exist_ok=True)
        current = [asdict(w) for w in self.list() if w.name != safe_name]
        current.append(asdict(ws))
        self.registry.write_text(json.dumps(current, indent=2), encoding="utf-8")
        return {"dry_run": False, "workspace": asdict(ws)}
