from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class DocumentDigestWorkflow:
    """Generate document digest workflow."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'DocumentDigestWorkflow', 'description': 'Generate document digest workflow', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Generate document digest workflow. This module is intentionally policy-aware and safe-by-default.'
