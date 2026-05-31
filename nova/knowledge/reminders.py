from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class RemindersService:
    """Local reminders service."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'RemindersService', 'description': 'Local reminders service', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Local reminders service. This module is intentionally policy-aware and safe-by-default.'
