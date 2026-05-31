from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ProjectWriter:
    """Write generated project files."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ProjectWriter', 'description': 'Write generated project files', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Write generated project files. This module is intentionally policy-aware and safe-by-default.'
