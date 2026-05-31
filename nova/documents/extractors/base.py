from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from nova.documents.models import Document

class Extractor(ABC):
    extensions: set[str] = set()

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.extensions

    @abstractmethod
    def extract(self, path: Path) -> Document: ...
