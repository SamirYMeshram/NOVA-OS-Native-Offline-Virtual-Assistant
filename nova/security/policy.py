from __future__ import annotations

from dataclasses import dataclass
from nova.core.models import RiskAssessment, RiskLevel

BLOCKED_TERMS = [
    "stealth", "hide process", "keylogger", "credential", "password dump", "bypass", "disable antivirus",
    "exfiltrate", "spy", "surveillance", "ransomware", "wipe disk", "format drive", "rm -rf /",
]
DANGEROUS_TERMS = ["delete", "remove permanently", "wipe", "kill process", "overwrite", "sudo", "chmod 777", "format"]
REVIEW_TERMS = ["move", "rename", "create", "write", "launch", "open app", "organize", "cleanup", "clean"]


def assess_goal(text: str) -> RiskAssessment:
    low = text.lower()
    reasons: list[str] = []
    if any(term in low for term in BLOCKED_TERMS):
        return RiskAssessment(RiskLevel.BLOCKED, ["Request contains blocked security/destructive behavior"], True, True)
    if any(term in low for term in DANGEROUS_TERMS):
        reasons.append("Potential destructive or privileged action")
        return RiskAssessment(RiskLevel.DANGEROUS, reasons, True, False)
    if any(term in low for term in REVIEW_TERMS):
        reasons.append("Action can change local files or system state")
        return RiskAssessment(RiskLevel.REVIEW, reasons, True, False)
    return RiskAssessment(RiskLevel.SAFE, ["Read-only or local computation"])


@dataclass(slots=True)
class Approval:
    confirmed: bool
    reason: str


def check_confirmation(required: bool, token: str | None, expected: str) -> Approval:
    if not required:
        return Approval(True, "No confirmation required")
    if token == expected:
        return Approval(True, "Confirmation token accepted")
    return Approval(False, f"Confirmation required. Pass --confirm {expected}")
