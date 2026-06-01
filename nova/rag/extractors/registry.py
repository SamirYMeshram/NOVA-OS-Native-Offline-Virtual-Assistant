from __future__ import annotations
from pathlib import Path
from .plain import PlainTextExtractor
from .pdf import PDFExtractor
from .docx import DocxExtractor
from .xlsx import XlsxExtractor

class ExtractorRegistry:
    def __init__(self):
        self.extractors = [PlainTextExtractor(), PDFExtractor(), DocxExtractor(), XlsxExtractor()]

    def extract(self, path: Path) -> str:
        for extractor in self.extractors:
            if extractor.supports(path):
                return extractor.extract(path)
        return ""

    def supported_extensions(self) -> set[str]:
        out: set[str] = set()
        for extractor in self.extractors:
            out |= extractor.extensions
        return out
