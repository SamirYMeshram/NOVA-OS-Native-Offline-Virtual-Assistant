from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ToolContract:
    """Typed tool contract metadata."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ToolContract', 'description': 'Typed tool contract metadata', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Typed tool contract metadata. This module is intentionally policy-aware and safe-by-default.'
