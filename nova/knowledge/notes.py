from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class NotesService:
    """Local notes service."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'NotesService', 'description': 'Local notes service', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Local notes service. This module is intentionally policy-aware and safe-by-default.'
