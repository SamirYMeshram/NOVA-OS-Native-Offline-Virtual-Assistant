from __future__ import annotations

import os
import platform
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from nova.automation.permissions import DEFAULT_PROFILE, PermissionProfile
from nova.core.events import AuditEvent, AuditLog
from nova.core.security import SafetyGuard


@dataclass(slots=True)
class ActionResult:
    ok: bool
    message: str
    data: dict[str, Any] | None = None


class AutomationEngine:
    """Permission-aware safe automation foundation."""

    def __init__(self, profile: PermissionProfile | None = None, guard: SafetyGuard | None = None) -> None:
        self.profile = profile or DEFAULT_PROFILE
        self.guard = guard or SafetyGuard()
        self.audit = AuditLog()

    def create_folder(self, path: str | Path, confirmed: bool = False) -> ActionResult:
        target = Path(path).expanduser().resolve()
        decision = self.guard.check_path_write(target)
        if not decision.allowed:
            return ActionResult(False, decision.reason)
        if decision.requires_confirmation and not confirmed:
            return ActionResult(False, f"Confirmation required before creating folder: {target}")
        target.mkdir(parents=True, exist_ok=True)
        self.audit.write(AuditEvent("create_folder", "success", str(target)))
        return ActionResult(True, f"Created folder: {target}")

    def create_file(self, path: str | Path, content: str = "", confirmed: bool = False, overwrite: bool = False) -> ActionResult:
        target = Path(path).expanduser().resolve()
        decision = self.guard.check_path_write(target, destructive=target.exists() and overwrite)
        if not decision.allowed:
            return ActionResult(False, decision.reason)
        if target.exists() and not overwrite:
            return ActionResult(False, f"File already exists, refusing overwrite: {target}")
        if decision.requires_confirmation and not confirmed:
            return ActionResult(False, f"Confirmation required before writing file: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.guard.redact_secrets(content), encoding="utf-8")
        self.audit.write(AuditEvent("create_file", "success", str(target), {"overwrite": str(overwrite)}))
        return ActionResult(True, f"Wrote file: {target}")

    def launch_app(self, command: str, confirmed: bool = False) -> ActionResult:
        if not self.profile.can_launch_apps:
            return ActionResult(False, "Current permission profile cannot launch apps")
        if not confirmed:
            return ActionResult(False, "Confirmation required before launching external programs")
        parts = command.split()
        if not parts:
            return ActionResult(False, "Empty command")
        try:
            subprocess.Popen(parts, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.audit.write(AuditEvent("launch_app", "success", command))
            return ActionResult(True, f"Launched: {command}")
        except Exception as exc:
            return ActionResult(False, f"Launch failed: {exc}")

    def system_status(self) -> ActionResult:
        data: dict[str, Any] = {"platform": platform.platform(), "cwd": os.getcwd()}
        try:
            import psutil  # type: ignore

            data.update(
                {
                    "cpu_percent": psutil.cpu_percent(interval=0.2),
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_percent": psutil.disk_usage(str(Path.home())).percent,
                }
            )
        except Exception:
            data["note"] = "Install psutil for detailed CPU/RAM/disk metrics"
        return ActionResult(True, "System status collected", data)
