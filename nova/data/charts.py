from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ChartPlanner:
    """Plan charts without unsafe code execution."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ChartPlanner', 'description': 'Plan charts without unsafe code execution', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Plan charts without unsafe code execution. This module is intentionally policy-aware and safe-by-default.'
