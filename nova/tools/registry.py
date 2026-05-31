from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ToolRegistry:
    """Register and invoke safe local tools."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ToolRegistry', 'description': 'Register and invoke safe local tools', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Register and invoke safe local tools. This module is intentionally policy-aware and safe-by-default.'
