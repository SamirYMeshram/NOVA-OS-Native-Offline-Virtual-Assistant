from __future__ import annotations

from pathlib import Path

from nova.documents.index import DocumentIndex


class LocalSearch:
    def __init__(self, index: DocumentIndex | None = None) -> None:
        self.index = index or DocumentIndex()

    def by_name(self, root: str | Path, pattern: str, limit: int = 50) -> list[Path]:
        root_path = Path(root).expanduser().resolve()
        matches: list[Path] = []
        needle = pattern.lower()
        for path in root_path.rglob("*"):
            if path.is_file() and needle in path.name.lower():
                matches.append(path)
                if len(matches) >= limit:
                    break
        return matches

    def by_content(self, query: str, limit: int = 10):
        return self.index.search(query, limit=limit)
