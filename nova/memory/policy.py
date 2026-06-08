from __future__ import annotations

from dataclasses import dataclass
from nova.security.secrets import looks_secret

@dataclass(slots=True)
class MemoryDecision:
    should_save: bool
    kind: str
    reason: str


def decide_memory(text: str) -> MemoryDecision:
    low = text.lower()
    if looks_secret(text):
        return MemoryDecision(False, "secret", "Looks like a secret; do not store by default")
    if any(k in low for k in ["remember", "from now on", "preference", "i prefer", "my goal", "deadline"]):
        kind = "preference" if "prefer" in low else "goal" if "goal" in low else "note"
        return MemoryDecision(True, kind, "User provided durable preference/goal/fact")
    return MemoryDecision(False, "transient", "No durable memory signal")
