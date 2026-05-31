from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

@dataclass(slots=True)
class FileInfo:
    path: Path
    size: int
    modified: float
    extension: str
    category: str
    sha256: str | None = None
    risk: str = "low"

@dataclass(slots=True)
class FileScanReport:
    root: Path
    files: list[FileInfo]
    total_bytes: int
    categories: dict[str, int] = field(default_factory=dict)

@dataclass(slots=True)
class FileAction:
    action: str
    source: Path
    target: Path | None
    reason: str
    risk: str = "low"

@dataclass(slots=True)
class CleanupPlan:
    root: Path
    actions: list[FileAction]
    requires_confirmation: bool = True
