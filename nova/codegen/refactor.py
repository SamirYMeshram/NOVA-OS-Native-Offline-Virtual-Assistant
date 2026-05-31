from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class RefactorPlanner:
    """Plan safe refactors."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'RefactorPlanner', 'description': 'Plan safe refactors', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Plan safe refactors. This module is intentionally policy-aware and safe-by-default.'
