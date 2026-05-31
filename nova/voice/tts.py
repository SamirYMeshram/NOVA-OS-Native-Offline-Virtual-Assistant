from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class TextToSpeechBackend:
    """Local TTS backend contract."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'TextToSpeechBackend', 'description': 'Local TTS backend contract', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Local TTS backend contract. This module is intentionally policy-aware and safe-by-default.'
