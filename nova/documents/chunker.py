from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TextChunk:
    chunk_id: str
    text: str
    start_char: int
    end_char: int


class TextChunker:
    def __init__(self, chunk_size: int = 1200, overlap: int = 180) -> None:
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str, prefix: str) -> list[TextChunk]:
        text = text.strip()
        if not text:
            return []
        chunks: list[TextChunk] = []
        start = 0
        index = 0
        while start < len(text):
            end = min(len(text), start + self.chunk_size)
            if end < len(text):
                # prefer breaking near a paragraph/sentence boundary
                boundary = max(text.rfind("\n\n", start, end), text.rfind(". ", start, end))
                if boundary > start + int(self.chunk_size * 0.55):
                    end = boundary + 1
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(TextChunk(f"{prefix}:chunk-{index:04d}", chunk_text, start, end))
                index += 1
            if end >= len(text):
                break
            start = max(0, end - self.overlap)
        return chunks
