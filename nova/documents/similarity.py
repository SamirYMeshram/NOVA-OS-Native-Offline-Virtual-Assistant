from __future__ import annotations
import math

def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    n = min(len(a), len(b))
    dot = sum(a[i] * b[i] for i in range(n))
    na = math.sqrt(sum(x*x for x in a[:n])) or 1.0
    nb = math.sqrt(sum(x*x for x in b[:n])) or 1.0
    return dot / (na * nb)
