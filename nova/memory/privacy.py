from __future__ import annotations

from dataclasses import dataclass

SENSITIVE_HINTS = {"password", "secret", "token", "api key", "private key", "otp", "cvv", "seed phrase"}


@dataclass(slots=True)
class MemoryPrivacyDecision:
    should_store: bool
    reason: str


def evaluate_memory_text(text: str) -> MemoryPrivacyDecision:
    lowered = text.lower()
    if any(hint in lowered for hint in SENSITIVE_HINTS):
        return MemoryPrivacyDecision(False, "Looks like a secret or credential. NOVA will not store it automatically.")
    if len(text.strip()) < 3:
        return MemoryPrivacyDecision(False, "Too little content to store as memory.")
    return MemoryPrivacyDecision(True, "Safe to store locally.")
