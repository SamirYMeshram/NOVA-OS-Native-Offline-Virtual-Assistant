from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class AnomalyDetector:
    """Detect basic invalid data patterns."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'AnomalyDetector', 'description': 'Detect basic invalid data patterns', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Detect basic invalid data patterns. This module is intentionally policy-aware and safe-by-default.'
