from __future__ import annotations
from pathlib import Path
from collections import Counter
import hashlib, os
from nova.security.path_policy import PathPolicy
from .classifier import classify_extension
from .models import FileInfo, FileScanReport

class FileScanner:
    def __init__(self, path_policy: PathPolicy):
        self.path_policy = path_policy

    def digest(self, path: Path, max_bytes: int = 1024 * 1024 * 128) -> str | None:
        if path.stat().st_size > max_bytes:
            return None
        h = hashlib.sha256()
        with path.open('rb') as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                h.update(chunk)
        return h.hexdigest()

    def scan(self, root: str | Path, hash_files: bool = False) -> FileScanReport:
        base = self.path_policy.ensure_allowed(root, write=False)
        files: list[FileInfo] = []
        if base.is_file():
            candidates = [base]
        else:
            candidates = [p for p in base.rglob('*') if p.is_file()]
        for p in candidates:
            try:
                st = p.stat()
            except OSError:
                continue
            ext = p.suffix.lower()
            category = classify_extension(ext)
            risk = 'medium' if category in {'executables', 'scripts'} else 'low'
            files.append(FileInfo(p, st.st_size, st.st_mtime, ext, category, self.digest(p) if hash_files else None, risk))
        counts = Counter(f.category for f in files)
        return FileScanReport(base, files, sum(f.size for f in files), dict(counts))
