from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

_WORD_RE = re.compile(r"[A-Za-z0-9_]+")


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in _WORD_RE.finditer(text)]


def cosine_sparse(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[k] * b[k] for k in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def term_vector(text: str) -> dict[str, float]:
    counts = Counter(tokenize(text))
    if not counts:
        return {}
    total = sum(counts.values())
    return {term: count / total for term, count in counts.items()}


def summarize_text(text: str, max_sentences: int = 5) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    if len(sentences) <= max_sentences:
        return text.strip()
    terms = Counter(tokenize(text))
    scored: list[tuple[float, int, str]] = []
    for idx, sent in enumerate(sentences):
        words = tokenize(sent)
        score = sum(terms[w] for w in words) / max(1, len(words))
        scored.append((score, idx, sent))
    selected = sorted(scored, reverse=True)[:max_sentences]
    ordered = [sent for _, _, sent in sorted(selected, key=lambda x: x[1])]
    return " ".join(ordered).strip()


@dataclass(slots=True)
class SearchHit:
    id: str
    score: float
    text: str
    metadata: dict[str, str]
