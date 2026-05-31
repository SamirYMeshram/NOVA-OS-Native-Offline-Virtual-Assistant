from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class FileRecord:
    path: str
    name: str
    suffix: str
    size: int
    modified_at: float
    sha256: str | None = None
    category: str = "other"


@dataclass(slots=True)
class FileScanReport:
    root: str
    files: list[FileRecord] = field(default_factory=list)
    duplicates: dict[str, list[str]] = field(default_factory=dict)
    large_files: list[str] = field(default_factory=list)
    old_files: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def summary(self) -> str:
        return f"Scanned {len(self.files)} files. Duplicates: {sum(len(v) for v in self.duplicates.values())}. Large files: {len(self.large_files)}. Old files: {len(self.old_files)}. Errors: {len(self.errors)}."

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "files": [asdict(f) for f in self.files],
            "duplicates": self.duplicates,
            "large_files": self.large_files,
            "old_files": self.old_files,
            "errors": self.errors,
        }
