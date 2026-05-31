from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class DailyBriefWorkflow:
    """Local daily brief workflow."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'DailyBriefWorkflow', 'description': 'Local daily brief workflow', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Local daily brief workflow. This module is intentionally policy-aware and safe-by-default.'
