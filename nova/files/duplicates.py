from __future__ import annotations
from collections import defaultdict
from .models import FileInfo

def duplicate_groups(files: list[FileInfo]) -> list[list[FileInfo]]:
    by_key: dict[tuple[int, str], list[FileInfo]] = defaultdict(list)
    for f in files:
        key = (f.size, f.sha256 or f.name.lower())
        by_key[key].append(f)
    return [g for g in by_key.values() if len(g) > 1]
