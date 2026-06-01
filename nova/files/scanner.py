from __future__ import annotations
from pathlib import Path
import hashlib, time
from nova.core.security import validate_user_path, is_protected_path
from .classifier import classify
from .models import FileInfo

def sha256_file(path: Path, max_bytes: int | None = None) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        remaining = max_bytes
        while True:
            if remaining is not None and remaining <= 0:
                break
            chunk_size = 1024 * 1024 if remaining is None else min(1024 * 1024, remaining)
            data = f.read(chunk_size)
            if not data:
                break
            h.update(data)
            if remaining is not None:
                remaining -= len(data)
    return h.hexdigest()

class FileScanner:
    def scan(self, root: str | Path, *, hashes: bool = False, max_files: int = 10000) -> list[FileInfo]:
        root_path = validate_user_path(root)
        files: list[FileInfo] = []
        iterator = [root_path] if root_path.is_file() else root_path.rglob('*')
        now = time.time()
        for p in iterator:
            if len(files) >= max_files:
                break
            if not p.is_file():
                continue
            try:
                stat = p.stat()
                flags = []
                if stat.st_size > 500 * 1024 * 1024:
                    flags.append('large')
                if now - stat.st_mtime > 365 * 24 * 3600:
                    flags.append('old')
                if any(part.startswith('.') for part in p.parts[-3:]):
                    flags.append('hidden_or_config')
                if is_protected_path(p):
                    flags.append('protected_path')
                files.append(FileInfo(str(p), p.name, p.suffix.lower(), stat.st_size, stat.st_mtime, classify(p), sha256_file(p) if hashes else '', flags))
            except Exception:
                continue
        return files
