from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json, time
from .scanner import FileInfo, scan_folder
from nova.security.path_guard import decide_path

@dataclass(slots=True)
class MoveAction:
    source: str
    destination: str
    reason: str
    risk: str = "review"

@dataclass(slots=True)
class CleanupPlan:
    root: str
    created_at: float
    actions: list[MoveAction]
    warnings: list[str]

    def to_dict(self):
        return {"root": self.root, "created_at": self.created_at, "actions": [asdict(a) for a in self.actions], "warnings": self.warnings}

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")


def build_cleanup_plan(path: str | Path, max_files: int = 20000) -> CleanupPlan:
    dec = decide_path(path, "cleanup-plan")
    if not dec.allowed: raise PermissionError(dec.reason)
    root = dec.path
    files = scan_folder(root, max_files=max_files, with_hash=False)
    actions: list[MoveAction] = []
    warnings: list[str] = []
    for f in files:
        p = Path(f.path)
        if p.parent != root:
            continue
        if f.category in {"other"}:
            continue
        dest_dir = root / f"NOVA_Organized/{f.category}"
        dest = dest_dir / p.name
        if dest.exists():
            warnings.append(f"Destination already exists, skipped: {dest}")
            continue
        actions.append(MoveAction(f.path, str(dest), f"Classified as {f.category}; move-only reversible cleanup"))
    if len(actions) > 500:
        warnings.append("Large cleanup plan; review carefully before applying")
    return CleanupPlan(str(root), time.time(), actions, warnings)
