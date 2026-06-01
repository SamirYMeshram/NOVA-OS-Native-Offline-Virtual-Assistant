from __future__ import annotations
import re, math
from collections import Counter

_WORD = re.compile(r"[A-Za-z0-9_]+")

def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()

def tokens(text: str) -> list[str]:
    return [m.group(0).lower() for m in _WORD.finditer(text or "")]

def keyword_score(query: str, text: str) -> float:
    q = Counter(tokens(query))
    t = Counter(tokens(text))
    if not q or not t:
        return 0.0
    return sum(min(t[k], v) for k, v in q.items()) / max(1, sum(q.values()))

def chunk_text(text: str, size: int = 1000, overlap: int = 150) -> list[str]:
    text = normalize(text)
    if len(text) <= size:
        return [text] if text else []
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        cut = text.rfind(". ", start, end)
        if cut > start + size // 2:
            end = cut + 1
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return [c for c in chunks if c]
