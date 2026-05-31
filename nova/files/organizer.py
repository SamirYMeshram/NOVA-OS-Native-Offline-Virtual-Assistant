from __future__ import annotations

import json
import shutil
import time
from dataclasses import asdict
from pathlib import Path

from ..core.audit import AuditEvent, AuditLog
from ..core.safety import SafetyGuard
from ..core.types import FileAction, OperationPlan, RiskLevel
from .classifier import classify_file


class FileOrganizer:
    """Creates reversible file organization plans. It never deletes automatically."""

    def __init__(self, safety: SafetyGuard | None = None, audit: AuditLog | None = None) -> None:
        self.safety = safety or SafetyGuard()
        self.audit = audit or AuditLog()

    def plan_by_category(self, root: str | Path, destination: str | Path | None = None) -> OperationPlan:
        base = Path(root).expanduser().resolve()
        dest_root = Path(destination).expanduser().resolve() if destination else base / "NOVA_Organized"
        actions: list[FileAction] = []
        for p in base.iterdir() if base.exists() and base.is_dir() else []:
            if not p.is_file():
                continue
            category = classify_file(p.name, p.suffix)
            dest = dest_root / category / p.name
            if dest == p:
                continue
            actions.append(FileAction("move", p, dest, RiskLevel.MEDIUM, f"Organize as {category}"))
        return OperationPlan(
            title=f"Organize files in {base}",
            risk=RiskLevel.MEDIUM,
            actions=actions,
            requires_confirmation=True,
            explanation="Moves files into category folders. No files are deleted. Undo log is created before changes.",
        )

    def save_plan(self, plan: OperationPlan, path: str | Path) -> Path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "title": plan.title,
            "risk": plan.risk.value,
            "requires_confirmation": plan.requires_confirmation,
            "explanation": plan.explanation,
            "actions": [self._action_dict(a) for a in plan.actions],
        }
        p.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return p

    def apply(self, plan: OperationPlan, confirmed: bool = False, undo_log_path: str | Path | None = None) -> Path:
        self.safety.validate_plan(plan, confirmed=confirmed)
        undo_path = Path(undo_log_path) if undo_log_path else Path.home() / ".nova" / "logs" / f"undo_{int(time.time())}.json"
        undo_path.parent.mkdir(parents=True, exist_ok=True)
        undo: list[dict[str, str]] = []
        for action in plan.actions:
            if action.action != "move" or not action.destination:
                continue
            src = Path(action.source)
            dst = Path(action.destination)
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                stem, suffix = dst.stem, dst.suffix
                dst = dst.with_name(f"{stem}_{int(time.time())}{suffix}")
            shutil.move(str(src), str(dst))
            undo.append({"action": "move", "source": str(dst), "destination": str(src)})
            self.audit.record(AuditEvent("file.move", message=f"Moved {src} -> {dst}", data={"source": str(src), "destination": str(dst)}))
        undo_path.write_text(json.dumps({"created_at": time.time(), "actions": undo}, indent=2), encoding="utf-8")
        return undo_path

    def undo(self, undo_log_path: str | Path, confirmed: bool = False) -> None:
        p = Path(undo_log_path).expanduser().resolve()
        payload = json.loads(p.read_text(encoding="utf-8"))
        actions = [FileAction("move", Path(item["source"]), Path(item["destination"]), RiskLevel.MEDIUM, "Undo previous move") for item in payload.get("actions", [])]
        plan = OperationPlan("Undo file organization", RiskLevel.MEDIUM, actions, True, "Reverse previous moves.")
        self.safety.validate_plan(plan, confirmed=confirmed)
        for action in actions:
            if action.destination:
                Path(action.destination).parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(action.source), str(action.destination))

    def _action_dict(self, action: FileAction) -> dict[str, str]:
        return {
            "action": action.action,
            "source": str(action.source),
            "destination": str(action.destination) if action.destination else "",
            "risk": action.risk.value,
            "reason": action.reason,
        }
