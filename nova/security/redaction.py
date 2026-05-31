from __future__ import annotations
import re

PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[^'\"\s]+"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
]

def redact_secrets(text: str) -> str:
    redacted = text
    for pattern in PATTERNS:
        redacted = pattern.sub(lambda m: m.group(0).split("=")[0] + "=<REDACTED>" if "=" in m.group(0) else "<REDACTED>", redacted)
    return redacted

def looks_like_secret(text: str) -> bool:
    return any(p.search(text) for p in PATTERNS)
