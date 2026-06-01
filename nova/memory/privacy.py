from __future__ import annotations
from nova.core.redaction import looks_like_secret, redact

SENSITIVE_KINDS = {"password", "token", "secret", "credential"}

def should_store(kind: str, text: str, explicit: bool = False) -> tuple[bool, str]:
    if kind.lower() in SENSITIVE_KINDS and not explicit:
        return False, "Sensitive memory kind requires explicit confirmation"
    if looks_like_secret(text) and not explicit:
        return True, "Secret-like text will be redacted before storage"
    return True, "ok"

def prepare_memory_text(text: str, explicit: bool = False) -> str:
    return text if explicit else redact(text)
