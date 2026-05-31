from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class TasksService:
    """Local tasks service."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'TasksService', 'description': 'Local tasks service', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Local tasks service. This module is intentionally policy-aware and safe-by-default.'
