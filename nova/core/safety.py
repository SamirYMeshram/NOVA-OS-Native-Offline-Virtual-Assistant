from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from ..config import NovaConfig
from ..exceptions import SafetyError
from .types import FileAction, OperationPlan, RiskLevel


@dataclass(slots=True)
class SafetyDecision:
    allowed: bool
    risk: RiskLevel
    reason: str
    requires_confirmation: bool = False


class SafetyGuard:
    """Central local safety policy for file and automation actions."""

    def __init__(self, config: NovaConfig | None = None) -> None:
        self.config = config or NovaConfig.load()

    def normalize(self, path: str | Path) -> Path:
        return Path(path).expanduser().resolve()

    def is_protected_path(self, path: str | Path) -> bool:
        candidate = self.normalize(path)
        for raw in self.config.safety.protected_paths:
            protected = Path(raw).expanduser().resolve()
            try:
                if candidate == protected or candidate.is_relative_to(protected):
                    return True
            except ValueError:
                continue
        return False

    def validate_read(self, path: str | Path) -> SafetyDecision:
        candidate = self.normalize(path)
        if not candidate.exists():
            return SafetyDecision(False, RiskLevel.LOW, f"Path does not exist: {candidate}")
        if candidate.is_file():
            size_mb = candidate.stat().st_size / (1024 * 1024)
            if size_mb > self.config.safety.max_file_read_mb:
                return SafetyDecision(False, RiskLevel.MEDIUM, f"File is larger than allowed read limit: {size_mb:.1f} MB")
        return SafetyDecision(True, RiskLevel.SAFE, "Read is allowed")

    def validate_file_action(self, action: FileAction) -> SafetyDecision:
        source = self.normalize(action.source)
        destination = self.normalize(action.destination) if action.destination else None
        if action.action in {"delete", "remove", "overwrite"}:
            return SafetyDecision(False, RiskLevel.DANGEROUS, "Destructive deletion/overwrite is blocked by default", True)
        if self.is_protected_path(source) or (destination and self.is_protected_path(destination)):
            return SafetyDecision(False, RiskLevel.DANGEROUS, "System/protected path is blocked", True)
        if action.action in {"move", "rename", "copy", "write", "mkdir"}:
            return SafetyDecision(True, max(action.risk, RiskLevel.MEDIUM, key=lambda r: list(RiskLevel).index(r)), "File change requires confirmation", True)
        return SafetyDecision(True, action.risk, "Action allowed", action.risk != RiskLevel.SAFE)

    def validate_plan(self, plan: OperationPlan, confirmed: bool = False) -> None:
        if plan.requires_confirmation and not confirmed:
            raise SafetyError("This operation requires explicit confirmation. Re-run with --confirm after reviewing the plan.")
        for action in plan.actions:
            decision = self.validate_file_action(action)
            if not decision.allowed:
                raise SafetyError(decision.reason)
            if decision.requires_confirmation and not confirmed:
                raise SafetyError(decision.reason + " Confirm required.")
