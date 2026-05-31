from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class CodeProjectWorkflow:
    """Generate code project workflow."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'CodeProjectWorkflow', 'description': 'Generate code project workflow', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Generate code project workflow. This module is intentionally policy-aware and safe-by-default.'
