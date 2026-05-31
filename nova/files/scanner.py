from __future__ import annotations

import hashlib
import time
from pathlib import Path

from .classifier import classify_file
from .models import FileRecord, FileScanReport


class FileScanner:
    def __init__(self, hash_limit_mb: int = 80, large_mb: int = 250, old_days: int = 365) -> None:
        self.hash_limit_mb = hash_limit_mb
        self.large_mb = large_mb
        self.old_days = old_days

    def scan(self, root: str | Path) -> FileScanReport:
        base = Path(root).expanduser().resolve()
        report = FileScanReport(str(base))
        if not base.exists():
            report.errors.append(f"Path does not exist: {base}")
            return report
        files = [base] if base.is_file() else [p for p in base.rglob("*") if p.is_file()]
        now = time.time()
        hashes: dict[str, list[str]] = {}
        for p in files:
            try:
                stat = p.stat()
                sha = None
                if stat.st_size <= self.hash_limit_mb * 1024 * 1024:
                    sha = self._sha256(p)
                    hashes.setdefault(sha, []).append(str(p))
                rec = FileRecord(
                    path=str(p),
                    name=p.name,
                    suffix=p.suffix.lower(),
                    size=stat.st_size,
                    modified_at=stat.st_mtime,
                    sha256=sha,
                    category=classify_file(p.name, p.suffix),
                )
                report.files.append(rec)
                if stat.st_size >= self.large_mb * 1024 * 1024:
                    report.large_files.append(str(p))
                if now - stat.st_mtime >= self.old_days * 24 * 3600:
                    report.old_files.append(str(p))
            except Exception as exc:  # noqa: BLE001
                report.errors.append(f"{p}: {exc}")
        report.duplicates = {digest: paths for digest, paths in hashes.items() if len(paths) > 1}
        return report

    def _sha256(self, path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for block in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(block)
        return h.hexdigest()
