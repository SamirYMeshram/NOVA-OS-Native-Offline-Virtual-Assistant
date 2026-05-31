from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class TestWriter:
    """Generate basic tests for generated projects."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'TestWriter', 'description': 'Generate basic tests for generated projects', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Generate basic tests for generated projects. This module is intentionally policy-aware and safe-by-default.'
