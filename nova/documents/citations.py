from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class CitationFormatter:
    """Format local document citations."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'CitationFormatter', 'description': 'Format local document citations', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Format local document citations. This module is intentionally policy-aware and safe-by-default.'
