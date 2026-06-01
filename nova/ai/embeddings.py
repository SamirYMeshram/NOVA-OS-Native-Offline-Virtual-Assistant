from __future__ import annotations
import hashlib, math
from collections import Counter
from nova.core.text import tokens

class HashEmbedding:
    """Dependency-free local embedding fallback using hashed bag-of-words."""
    def __init__(self, dims: int = 384):
        self.dims = dims

    def embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dims
        counts = Counter(tokens(text))
        for tok, c in counts.items():
            h = int(hashlib.blake2b(tok.encode(), digest_size=8).hexdigest(), 16)
            idx = h % self.dims
            sign = 1.0 if (h >> 9) & 1 else -1.0
            vec[idx] += sign * (1.0 + math.log(c))
        norm = math.sqrt(sum(v*v for v in vec)) or 1.0
        return [v / norm for v in vec]

    @staticmethod
    def cosine(a: list[float], b: list[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        return sum(x*y for x, y in zip(a, b))
