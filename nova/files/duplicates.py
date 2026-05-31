from __future__ import annotations
from collections import defaultdict
from .models import FileInfo

class DuplicateDetector:
    def by_hash(self, files: list[FileInfo]) -> dict[str, list[FileInfo]]:
        groups: dict[str, list[FileInfo]] = defaultdict(list)
        for f in files:
            if f.sha256:
                groups[f.sha256].append(f)
        return {h: g for h, g in groups.items() if len(g) > 1}

    def by_name_size(self, files: list[FileInfo]) -> dict[str, list[FileInfo]]:
        groups: dict[str, list[FileInfo]] = defaultdict(list)
        for f in files:
            groups[f"{f.path.name}:{f.size}"].append(f)
        return {k: g for k, g in groups.items() if len(g) > 1}
