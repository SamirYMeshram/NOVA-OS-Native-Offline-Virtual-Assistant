from __future__ import annotations
from pathlib import Path
from .base import Extractor
from nova.documents.models import Document

class ImageExtractor(Extractor):
    extensions = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'}

    def extract(self, path: Path) -> Document:
        # Optional OCR hook. No network, no hidden surveillance. User installs local OCR if desired.
        text = f"[Image file indexed by metadata only. Local OCR extension point: {path.name}]"
        return Document(path=path, text=text, metadata={'type': 'image', 'ocr': 'not_configured'})
