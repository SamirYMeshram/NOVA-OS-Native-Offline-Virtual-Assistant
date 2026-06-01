from __future__ import annotations
from pathlib import Path
from .base import Extractor

class PlainTextExtractor(Extractor):
    extensions = {'.txt', '.md', '.markdown', '.rst', '.log', '.py', '.js', '.ts', '.java', '.go', '.rs', '.json', '.yaml', '.yml', '.toml', '.csv'}
    def extract(self, path: Path) -> str:
        return path.read_text(encoding='utf-8', errors='ignore')
