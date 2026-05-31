from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class LocalScheduler:
    """Local reminder scheduling extension point."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'LocalScheduler', 'description': 'Local reminder scheduling extension point', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Local reminder scheduling extension point. This module is intentionally policy-aware and safe-by-default.'
