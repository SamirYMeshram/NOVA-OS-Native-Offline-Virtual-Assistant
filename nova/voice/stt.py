from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class SpeechToTextBackend:
    """Local STT backend contract."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'SpeechToTextBackend', 'description': 'Local STT backend contract', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Local STT backend contract. This module is intentionally policy-aware and safe-by-default.'
