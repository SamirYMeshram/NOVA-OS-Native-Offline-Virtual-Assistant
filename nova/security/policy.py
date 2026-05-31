from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from nova.core.result import Result

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass(slots=True)
class SafetyDecision:
    allowed: bool
    requires_confirmation: bool
    risk: RiskLevel
    reason: str

class SafetyPolicy:
    destructive_words = {"delete", "remove", "wipe", "format", "rm -rf", "destroy", "erase"}

    def assess_text_command(self, command: str) -> SafetyDecision:
        low = command.lower()
        if any(word in low for word in self.destructive_words):
            return SafetyDecision(True, True, RiskLevel.HIGH, "Potentially destructive command requires confirmation")
        if "password" in low or "token" in low or "secret" in low:
            return SafetyDecision(True, True, RiskLevel.MEDIUM, "Command may include sensitive data")
        return SafetyDecision(True, False, RiskLevel.LOW, "Safe natural language command")

    def result_for(self, decision: SafetyDecision) -> Result:
        return Result.success(decision.reason, requires_confirmation=decision.requires_confirmation, risk=decision.risk.value)
