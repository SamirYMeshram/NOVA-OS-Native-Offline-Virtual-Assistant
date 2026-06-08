from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from nova.documents.extractors import supported, extract_text
from nova.security.path_guard import decide_path

@dataclass(slots=True)
class FileSearchHit:
    path: str
    reason: str
    snippet: str


def search_files(path: str | Path, query: str, max_files: int = 2000) -> list[FileSearchHit]:
    dec = decide_path(path, "search")
    if not dec.allowed:
        raise PermissionError(dec.reason)
    root = dec.path
    q = query.lower()
    hits: list[FileSearchHit] = []
    files = root.rglob("*") if root.is_dir() else [root]
    for i, f in enumerate(files):
        if i >= max_files: break
        if not f.is_file(): continue
        if q in f.name.lower():
            hits.append(FileSearchHit(str(f), "filename", f.name))
            continue
        if supported(f):
            try:
                text = extract_text(f)
            except Exception:
                continue
            pos = text.lower().find(q)
            if pos >= 0:
                hits.append(FileSearchHit(str(f), "content", text[max(0,pos-120):pos+220].replace("\n", " ")))
        if len(hits) >= 50: break
    return hits
