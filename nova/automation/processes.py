from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ProcessInspector:
    """Inspect processes safely."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ProcessInspector', 'description': 'Inspect processes safely', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Inspect processes safely. This module is intentionally policy-aware and safe-by-default.'
