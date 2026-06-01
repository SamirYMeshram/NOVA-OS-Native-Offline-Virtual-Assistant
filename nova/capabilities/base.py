from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass(slots=True)
class CapabilitySpec:
    name: str
    domain: str
    description: str
    commands: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    risk: str = 'low'
    offline: bool = True

class Capability:
    spec: CapabilitySpec
    def describe(self) -> dict[str, Any]:
        return asdict(self.spec)
    def plan(self, request: str) -> dict[str, Any]:
        return {'capability': self.spec.name, 'request': request, 'steps': self.spec.commands, 'risk': self.spec.risk, 'offline': self.spec.offline}
