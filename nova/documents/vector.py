from __future__ import annotations

import hashlib, math

DIM = 256


def embed(text: str, dim: int = DIM) -> list[float]:
    vec = [0.0] * dim
    words = [w.strip(".,;:!?()[]{}<>\\/\"'").lower() for w in text.split()]
    for w in words:
        if not w:
            continue
        digest = hashlib.blake2b(w.encode("utf-8"), digest_size=8).digest()
        idx = int.from_bytes(digest[:4], "big") % dim
        sign = 1 if digest[4] % 2 == 0 else -1
        vec[idx] += sign * (1.0 + min(len(w), 12) / 12.0)
    norm = math.sqrt(sum(x*x for x in vec)) or 1.0
    return [x / norm for x in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x*y for x, y in zip(a, b))
