from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(slots=True)
class FileInfo:
    path: str
    name: str
    suffix: str
    size: int
    modified: float
    category: str
    sha256: str = ""
    risk_flags: list[str] = field(default_factory=list)

@dataclass(slots=True)
class FileAction:
    action: str
    source: str
    target: str = ""
    reason: str = ""
    risk: str = "low"
    requires_confirmation: bool = True
