from __future__ import annotations
from collections import Counter
from nova.core.text import tokens, normalize

def summarize_text(text: str, sentences: int = 5) -> str:
    parts = [p.strip() for p in normalize(text).split('. ') if p.strip()]
    if len(parts) <= sentences:
        return '. '.join(parts)
    word_counts = Counter(t for t in tokens(text) if len(t) > 4)
    scored = []
    for idx, s in enumerate(parts):
        score = sum(word_counts[t] for t in tokens(s)) / max(1, len(tokens(s)))
        scored.append((score, idx, s))
    chosen = sorted(scored, reverse=True)[:sentences]
    return '. '.join(s for _, _, s in sorted(chosen, key=lambda x: x[1]))
