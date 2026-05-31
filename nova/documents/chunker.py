from __future__ import annotations

import hashlib
from pathlib import Path

from .models import Chunk, LoadedDocument


class SmartChunker:
    def __init__(self, target_chars: int = 1400, overlap_chars: int = 180) -> None:
        self.target_chars = target_chars
        self.overlap_chars = overlap_chars

    def chunk(self, doc: LoadedDocument) -> list[Chunk]:
        text = doc.text.replace("\r\n", "\n")
        chunks: list[Chunk] = []
        start = 0
        while start < len(text):
            end = min(len(text), start + self.target_chars)
            if end < len(text):
                # Prefer paragraph or sentence boundary near the target.
                window = text[start:end]
                split_at = max(window.rfind("\n\n"), window.rfind(". "), window.rfind("\n"))
                if split_at > self.target_chars * 0.55:
                    end = start + split_at + 1
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunk_id = self._id(doc.path, start, chunk_text)
                chunks.append(Chunk(chunk_id, doc.path, chunk_text, start, end, dict(doc.metadata)))
            if end >= len(text):
                break
            start = max(0, end - self.overlap_chars)
        return chunks

    def _id(self, path: Path, start: int, text: str) -> str:
        digest = hashlib.sha256((str(path) + str(start) + text[:80]).encode()).hexdigest()[:16]
        return f"chk_{digest}"
