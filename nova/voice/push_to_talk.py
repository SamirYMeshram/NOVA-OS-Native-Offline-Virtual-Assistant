from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class PushToTalkController:
    """Push-to-talk voice mode controller."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'PushToTalkController', 'description': 'Push-to-talk voice mode controller', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Push-to-talk voice mode controller. This module is intentionally policy-aware and safe-by-default.'
