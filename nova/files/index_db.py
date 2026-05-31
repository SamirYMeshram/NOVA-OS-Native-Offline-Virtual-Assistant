from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class FileIndexDB:
    """Persistent file metadata index."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'FileIndexDB', 'description': 'Persistent file metadata index', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Persistent file metadata index. This module is intentionally policy-aware and safe-by-default.'
