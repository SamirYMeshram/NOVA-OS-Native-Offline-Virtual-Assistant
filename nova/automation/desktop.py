from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from ..core.safety import SafetyGuard
from ..core.types import FileAction, OperationPlan, RiskLevel


@dataclass(slots=True)
class AppLaunchResult:
    command: list[str]
    started: bool
    message: str


class DesktopAutomation:
    def __init__(self, safety: SafetyGuard | None = None) -> None:
        self.safety = safety or SafetyGuard()
        self.allowed_apps = {"code", "firefox", "brave-browser", "konsole", "gnome-terminal", "dolphin", "nautilus"}

    def create_folder(self, path: str | Path, confirmed: bool = False) -> Path:
        p = Path(path).expanduser().resolve()
        plan = OperationPlan("Create folder", RiskLevel.MEDIUM, [FileAction("mkdir", p, p, RiskLevel.MEDIUM, "Create requested folder")], True)
        self.safety.validate_plan(plan, confirmed=confirmed)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def create_file(self, path: str | Path, content: str = "", confirmed: bool = False) -> Path:
        p = Path(path).expanduser().resolve()
        action = FileAction("write", p, p, RiskLevel.MEDIUM, "Create/write file")
        self.safety.validate_plan(OperationPlan("Create file", RiskLevel.MEDIUM, [action], True), confirmed=confirmed)
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {p}")
        p.write_text(content, encoding="utf-8")
        return p

    def launch_app(self, app: str, args: list[str] | None = None) -> AppLaunchResult:
        if app not in self.allowed_apps:
            return AppLaunchResult([app] + (args or []), False, "App is not in the approved launch list.")
        try:
            subprocess.Popen([app] + (args or []), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return AppLaunchResult([app] + (args or []), True, "Started approved app.")
        except FileNotFoundError:
            return AppLaunchResult([app] + (args or []), False, "App executable not found.")
