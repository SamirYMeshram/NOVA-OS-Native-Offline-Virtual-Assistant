from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class AudioTranscriptIndexer:
    """Index local transcripts."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'AudioTranscriptIndexer', 'description': 'Index local transcripts', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'Index local transcripts. This module is intentionally policy-aware and safe-by-default.'
