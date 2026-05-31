from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class DocumentComparator:
    """Compare extracted local documents."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'DocumentComparator', 'description': 'Compare extracted local documents', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Compare extracted local documents. This module is intentionally policy-aware and safe-by-default.'
