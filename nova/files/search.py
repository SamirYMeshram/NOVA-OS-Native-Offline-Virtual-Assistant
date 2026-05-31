from __future__ import annotations

from pathlib import Path


def filename_search(root: str | Path, query: str, limit: int = 50) -> list[str]:
    base = Path(root).expanduser().resolve()
    q = query.lower()
    result = []
    for p in base.rglob("*") if base.exists() and base.is_dir() else []:
        if p.is_file() and q in p.name.lower():
            result.append(str(p))
            if len(result) >= limit:
                break
    return result
