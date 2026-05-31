from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ReportExporter:
    """Export local reports."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ReportExporter', 'description': 'Export local reports', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Export local reports. This module is intentionally policy-aware and safe-by-default.'
