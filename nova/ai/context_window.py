from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ContextWindowManager:
    """Trim and assemble long local context."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ContextWindowManager', 'description': 'Trim and assemble long local context', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Trim and assemble long local context. This module is intentionally policy-aware and safe-by-default.'
