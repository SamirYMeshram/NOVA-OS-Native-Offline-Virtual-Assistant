from __future__ import annotations
from dataclasses import dataclass

DENY_SUBSTRINGS = [
    "rm -rf /", "mkfs", "dd if=", ":(){", "chmod -R 777 /", "chown -R", "shutdown", "reboot",
    "curl ", "wget ", "nc ", "ncat ", "telnet ", "base64 -d | sh", "Invoke-WebRequest",
]

@dataclass(slots=True)
class CommandAssessment:
    command: str
    allowed: bool
    requires_confirmation: bool
    reason: str

class CommandPolicy:
    def assess(self, command: str) -> CommandAssessment:
        lower = command.lower()
        for bad in DENY_SUBSTRINGS:
            if bad.lower() in lower:
                return CommandAssessment(command, False, True, f"Blocked dangerous shell pattern: {bad}")
        mutating = any(x in lower for x in [" rm ", " mv ", " cp ", " sudo ", "pip install", "dnf ", "apt "])
        return CommandAssessment(command, True, mutating, "Allowed after confirmation" if mutating else "Allowed")
