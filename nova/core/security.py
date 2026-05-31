from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .config import SecurityConfig
from .paths import safe_resolve

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str
    requires_confirmation: bool = False


class SafetyGuard:
    """Central place for local safety decisions.

    NOVA is allowed to help the user automate their own computer, but write,
    destructive, and system-level operations are intentionally visible and
    confirmation-gated.
    """

    def __init__(self, config: SecurityConfig | None = None) -> None:
        self.config = config or SecurityConfig()

    def is_protected_path(self, path: str | Path) -> bool:
        resolved = safe_resolve(path)
        for protected in self.config.protected_roots:
            root = Path(protected).resolve()
            if resolved == root or root in resolved.parents:
                return True
        return False

    def check_path_read(self, path: str | Path) -> SafetyDecision:
        resolved = safe_resolve(path)
        if not resolved.exists():
            return SafetyDecision(False, f"Path does not exist: {resolved}")
        return SafetyDecision(True, "Read is allowed")

    def check_path_write(self, path: str | Path, destructive: bool = False) -> SafetyDecision:
        resolved = safe_resolve(path)
        if self.is_protected_path(resolved):
            return SafetyDecision(False, f"Protected system path blocked: {resolved}")
        if destructive or self.config.require_confirmation_for_write:
            return SafetyDecision(True, "Write operation requires confirmation", True)
        return SafetyDecision(True, "Write is allowed", False)

    def redact_secrets(self, text: str) -> str:
        if not self.config.secrets_redaction:
            return text
        redacted = text
        for pattern in SECRET_PATTERNS:
            redacted = pattern.sub("[REDACTED_SECRET]", redacted)
        return redacted

    def looks_like_secret(self, text: str) -> bool:
        return any(pattern.search(text) for pattern in SECRET_PATTERNS)
