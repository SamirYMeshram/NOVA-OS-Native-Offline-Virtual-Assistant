from __future__ import annotations
from pathlib import Path

class FileSearch:
    def search_names(self, root: str | Path, query: str, limit: int = 50) -> list[Path]:
        base = Path(root).expanduser().resolve()
        q = query.lower()
        hits = []
        for p in base.rglob('*'):
            if q in p.name.lower():
                hits.append(p)
                if len(hits) >= limit:
                    break
        return hits

    def search_content(self, root: str | Path, query: str, limit: int = 20) -> list[tuple[Path, int, str]]:
        base = Path(root).expanduser().resolve()
        q = query.lower()
        hits: list[tuple[Path, int, str]] = []
        for p in base.rglob('*'):
            if not p.is_file() or p.stat().st_size > 2_000_000:
                continue
            try:
                lines = p.read_text(encoding='utf-8', errors='ignore').splitlines()
            except Exception:
                continue
            for i, line in enumerate(lines, 1):
                if q in line.lower():
                    hits.append((p, i, line.strip()[:300]))
                    if len(hits) >= limit:
                        return hits
        return hits
