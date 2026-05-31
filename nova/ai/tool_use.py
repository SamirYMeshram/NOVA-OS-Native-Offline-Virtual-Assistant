from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ToolUseController:
    """Decide when a command should use tools."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ToolUseController', 'description': 'Decide when a command should use tools', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Decide when a command should use tools. This module is intentionally policy-aware and safe-by-default.'
