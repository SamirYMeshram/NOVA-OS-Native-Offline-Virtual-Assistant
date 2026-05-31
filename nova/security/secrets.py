from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class SecretScanner:
    """Scan text for secrets."""
    enabled: bool = True

    def capabilities(self) -> dict:
        return {'name': 'SecretScanner', 'description': 'Scan text for secrets', 'enabled': self.enabled, 'local_first': True}

    def explain(self) -> str:
        return 'SecretScanner: Scan text for secrets. This module is intentionally policy-aware and safe-by-default.'
