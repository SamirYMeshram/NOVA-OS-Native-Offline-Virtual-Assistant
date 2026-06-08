from __future__ import annotations

from collections import defaultdict
from .scanner import FileInfo, scan_folder

def duplicate_groups(path: str, max_files: int = 20000) -> list[list[FileInfo]]:
    files = scan_folder(path, max_files=max_files, with_hash=True)
    groups: dict[tuple[int, str], list[FileInfo]] = defaultdict(list)
    for f in files:
        if f.digest:
            groups[(f.size, f.digest)].append(f)
    return [g for g in groups.values() if len(g) > 1]
