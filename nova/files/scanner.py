from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from nova.core.security import SafetyGuard
from nova.utils.hashing import sha256_file


@dataclass(slots=True)
class FileInfo:
    path: Path
    size: int
    suffix: str
    modified_at: str
    sha256: str | None = None


@dataclass(slots=True)
class ScanReport:
    root: Path
    file_count: int
    total_bytes: int
    largest_files: list[FileInfo]
    duplicates: dict[str, list[Path]]
    by_extension: dict[str, int]


class FileScanner:
    def __init__(self, guard: SafetyGuard | None = None) -> None:
        self.guard = guard or SafetyGuard()

    def scan(self, root: str | Path, recursive: bool = True, hash_files: bool = False, limit: int = 20_000) -> ScanReport:
        root_path = Path(root).expanduser().resolve()
        decision = self.guard.check_path_read(root_path)
        if not decision.allowed:
            raise PermissionError(decision.reason)
        iterator = root_path.rglob("*") if recursive else root_path.glob("*")
        files: list[FileInfo] = []
        by_ext: dict[str, int] = defaultdict(int)
        seen = 0
        for item in iterator:
            if not item.is_file():
                continue
            seen += 1
            if seen > limit:
                break
            stat = item.stat()
            suffix = item.suffix.lower() or "[no extension]"
            by_ext[suffix] += 1
            digest = sha256_file(item) if hash_files and stat.st_size <= 200 * 1024 * 1024 else None
            files.append(
                FileInfo(
                    path=item,
                    size=stat.st_size,
                    suffix=suffix,
                    modified_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    sha256=digest,
                )
            )
        duplicates: dict[str, list[Path]] = defaultdict(list)
        if hash_files:
            for info in files:
                if info.sha256:
                    duplicates[info.sha256].append(info.path)
        duplicates = {h: p for h, p in duplicates.items() if len(p) > 1}
        return ScanReport(
            root=root_path,
            file_count=len(files),
            total_bytes=sum(f.size for f in files),
            largest_files=sorted(files, key=lambda f: f.size, reverse=True)[:10],
            duplicates=duplicates,
            by_extension=dict(sorted(by_ext.items(), key=lambda x: x[1], reverse=True)),
        )
