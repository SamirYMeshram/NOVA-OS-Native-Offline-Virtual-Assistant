from __future__ import annotations
from pathlib import Path
from .models import Document
from .extractors.text import TextExtractor
from .extractors.pdf import PDFExtractor
from .extractors.docx import DocxExtractor
from .extractors.excel import ExcelExtractor
from .extractors.image import ImageExtractor

class ExtractorRegistry:
    def __init__(self):
        self.extractors = [TextExtractor(), PDFExtractor(), DocxExtractor(), ExcelExtractor(), ImageExtractor()]

    def extract(self, path: str | Path) -> Document:
        p = Path(path).expanduser().resolve()
        for extractor in self.extractors:
            if extractor.supports(p):
                return extractor.extract(p)
        # fallback: try text
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            text = f"[Unsupported binary file: {p.name}]"
        return Document(path=p, text=text, metadata={'type': 'unknown'})
