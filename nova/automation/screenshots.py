from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class ScreenshotTool:
    """User-approved screenshot extension point."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'ScreenshotTool', 'description': 'User-approved screenshot extension point', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'User-approved screenshot extension point. This module is intentionally policy-aware and safe-by-default.'
