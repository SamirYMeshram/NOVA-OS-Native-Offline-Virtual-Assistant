from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ToolSandbox:
    """Policy-controlled tool execution boundary."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ToolSandbox', 'description': 'Policy-controlled tool execution boundary', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Policy-controlled tool execution boundary. This module is intentionally policy-aware and safe-by-default.'
