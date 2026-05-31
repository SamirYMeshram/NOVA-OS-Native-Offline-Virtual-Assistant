from __future__ import annotations
from pathlib import Path
from .base import Extractor
from nova.documents.models import Document

class TextExtractor(Extractor):
    extensions = {'.txt', '.md', '.rst', '.log', '.py', '.js', '.ts', '.java', '.json', '.yaml', '.yml', '.toml', '.csv', '.html', '.css'}

    def extract(self, path: Path) -> Document:
        text = path.read_text(encoding='utf-8', errors='ignore')
        return Document(path=path, text=text, metadata={'type': path.suffix.lower().lstrip('.') or 'text'})
