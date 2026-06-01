from __future__ import annotations
from collections import Counter
from nova.core.text import tokens

def summarize_memories(texts: list[str], max_terms: int = 12) -> str:
    counts = Counter(t for x in texts for t in tokens(x) if len(t) > 3)
    terms = [t for t, _ in counts.most_common(max_terms)]
    return "Memory themes: " + ", ".join(terms) if terms else "No strong memory themes yet."
