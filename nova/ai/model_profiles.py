from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ModelProfileRegistry:
    """Low/normal/high performance model profiles."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ModelProfileRegistry', 'description': 'Low/normal/high performance model profiles', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Low/normal/high performance model profiles. This module is intentionally policy-aware and safe-by-default.'
