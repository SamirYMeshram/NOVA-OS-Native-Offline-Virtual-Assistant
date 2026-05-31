from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class FilePlanExecutor:
    """Execute confirmed file plans safely."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'FilePlanExecutor', 'description': 'Execute confirmed file plans safely', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Execute confirmed file plans safely. This module is intentionally policy-aware and safe-by-default.'
