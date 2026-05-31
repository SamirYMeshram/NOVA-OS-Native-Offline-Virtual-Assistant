from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Any

from ..core.types import RiskLevel, ToolResult

ToolCallable = Callable[..., ToolResult]


@dataclass(slots=True)
class ToolSpec:
    name: str
    description: str
    risk: RiskLevel
    permissions: list[str]
    handler: ToolCallable | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)

    def list(self) -> list[dict[str, Any]]:
        return [
            {
                "name": spec.name,
                "description": spec.description,
                "risk": spec.risk.value,
                "permissions": spec.permissions,
                "metadata": spec.metadata,
            }
            for spec in self._tools.values()
        ]

    @classmethod
    def default(cls) -> "ToolRegistry":
        reg = cls()
        reg.register(ToolSpec("memory.search", "Search local memory", RiskLevel.SAFE, ["memory:read"]))
        reg.register(ToolSpec("memory.write", "Write local memory", RiskLevel.LOW, ["memory:write"]))
        reg.register(ToolSpec("documents.index", "Index local documents", RiskLevel.LOW, ["documents:read"]))
        reg.register(ToolSpec("documents.qa", "Answer from local document chunks", RiskLevel.SAFE, ["documents:read"]))
        reg.register(ToolSpec("files.scan", "Scan local files without changing them", RiskLevel.SAFE, ["files:read"]))
        reg.register(ToolSpec("files.plan", "Create reversible file organization plan", RiskLevel.LOW, ["files:read"]))
        reg.register(ToolSpec("files.apply", "Apply file move/copy plan after confirmation", RiskLevel.MEDIUM, ["files:write-confirmed"]))
        reg.register(ToolSpec("automation.launch_app", "Launch approved local apps", RiskLevel.LOW, ["apps:launch"]))
        return reg
