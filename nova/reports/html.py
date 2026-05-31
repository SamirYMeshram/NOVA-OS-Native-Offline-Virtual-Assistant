from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class HtmlReport:
    """HTML report renderer."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'HtmlReport', 'description': 'HTML report renderer', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'HTML report renderer. This module is intentionally policy-aware and safe-by-default.'
