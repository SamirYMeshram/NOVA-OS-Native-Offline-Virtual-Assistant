from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ChangeTracker:
    """Track folder snapshots."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ChangeTracker', 'description': 'Track folder snapshots', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Track folder snapshots. This module is intentionally policy-aware and safe-by-default.'
