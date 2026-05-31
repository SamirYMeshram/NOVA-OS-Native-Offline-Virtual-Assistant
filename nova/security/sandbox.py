from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class SandboxPolicy:
    """Local sandbox policy metadata."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'SandboxPolicy', 'description': 'Local sandbox policy metadata', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Local sandbox policy metadata. This module is intentionally policy-aware and safe-by-default.'
