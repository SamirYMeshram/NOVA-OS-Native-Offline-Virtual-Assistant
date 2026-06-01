from __future__ import annotations
from pathlib import Path
from .base import Extractor

class PDFExtractor(Extractor):
    extensions = {'.pdf'}
    def extract(self, path: Path) -> str:
        try:
            from pypdf import PdfReader
        except Exception:
            return f"[PDF extraction requires optional dependency pypdf: {path.name}]"
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or '' for page in reader.pages)
