from __future__ import annotations
from pathlib import Path
from .base import Extractor
from nova.documents.models import Document

class PDFExtractor(Extractor):
    extensions = {'.pdf'}

    def extract(self, path: Path) -> Document:
        try:
            from pypdf import PdfReader  # type: ignore
            reader = PdfReader(str(path))
            pages = []
            for i, page in enumerate(reader.pages):
                pages.append(f"\n\n--- page {i+1} ---\n" + (page.extract_text() or ""))
            text = ''.join(pages)
        except Exception as exc:
            text = f"[PDF extraction unavailable: install pypdf. Error: {exc}]"
        return Document(path=path, text=text, metadata={'type': 'pdf'})
