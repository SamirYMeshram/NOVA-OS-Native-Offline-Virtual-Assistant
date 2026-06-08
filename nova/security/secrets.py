from __future__ import annotations

import re

SECRET_PATTERNS = [
    re.compile(r"(?i)(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*['\"]?[^\s'\"]+"),
    re.compile(r"\b[A-Za-z0-9_\-]{32,}\b"),
]


def redact(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(lambda m: m.group(0).split("=")[0] + "=[REDACTED]" if "=" in m.group(0) else "[REDACTED]", redacted)
    return redacted


def looks_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)
