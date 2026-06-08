from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib, time, os
from nova.security.path_guard import decide_path

@dataclass(slots=True)
class FileInfo:
    path: str
    name: str
    suffix: str
    size: int
    modified_at: float
    category: str
    is_large: bool
    is_old: bool
    digest: str | None = None

CATEGORY_MAP = {
    "documents": {".pdf", ".docx", ".txt", ".md", ".odt"},
    "spreadsheets": {".csv", ".xlsx", ".ods"},
    "images": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"},
    "archives": {".zip", ".tar", ".gz", ".7z", ".rar"},
    "code": {".py", ".js", ".ts", ".java", ".go", ".rs", ".cpp", ".c", ".html", ".css"},
    "installers": {".exe", ".msi", ".deb", ".rpm", ".appimage"},
    "media": {".mp4", ".mkv", ".mp3", ".wav", ".flac"},
}

def category_for(path: Path) -> str:
    suf = path.suffix.lower()
    for cat, suffixes in CATEGORY_MAP.items():
        if suf in suffixes:
            return cat
    return "other"


def digest_file(path: Path, max_bytes: int = 2_000_000) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        remaining = max_bytes
        while remaining > 0:
            data = f.read(min(65536, remaining))
            if not data: break
            h.update(data)
            remaining -= len(data)
    return h.hexdigest()


def scan_folder(path: str | Path, max_files: int = 20000, with_hash: bool = False) -> list[FileInfo]:
    decision = decide_path(path, "scan")
    if not decision.allowed:
        raise PermissionError(decision.reason)
    root = decision.path
    now = time.time()
    infos: list[FileInfo] = []
    for i, p in enumerate(root.rglob("*")):
        if i >= max_files: break
        if not p.is_file(): continue
        try:
            st = p.stat()
        except OSError:
            continue
        info = FileInfo(
            path=str(p), name=p.name, suffix=p.suffix.lower(), size=st.st_size, modified_at=st.st_mtime,
            category=category_for(p), is_large=st.st_size > 500 * 1024 * 1024,
            is_old=(now - st.st_mtime) > 180 * 24 * 3600,
            digest=digest_file(p) if with_hash and st.st_size < 100 * 1024 * 1024 else None,
        )
        infos.append(info)
    return infos


def summarize_scan(files: list[FileInfo]) -> dict[str, object]:
    by_cat: dict[str, int] = {}
    total = 0
    for f in files:
        by_cat[f.category] = by_cat.get(f.category, 0) + 1
        total += f.size
    return {"files": len(files), "total_bytes": total, "categories": by_cat, "large": sum(f.is_large for f in files), "old": sum(f.is_old for f in files)}
