from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class TableExtractor:
    """Extract simple markdown/CSV style tables."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'TableExtractor', 'description': 'Extract simple markdown/CSV style tables', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Extract simple markdown/CSV style tables. This module is intentionally policy-aware and safe-by-default.'
