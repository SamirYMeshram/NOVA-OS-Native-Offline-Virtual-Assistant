from __future__ import annotations
from pathlib import Path
from .base import Extractor

class DocxExtractor(Extractor):
    extensions = {'.docx'}
    def extract(self, path: Path) -> str:
        try:
            import docx
        except Exception:
            return f"[DOCX extraction requires optional dependency python-docx: {path.name}]"
        doc = docx.Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
