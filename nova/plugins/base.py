from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PluginManifest:
    name: str
    description: str
    permissions: list[str] = field(default_factory=list)
    enabled_by_default: bool = True


@dataclass(slots=True)
class PluginResult:
    ok: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)


class NovaPlugin(ABC):
    manifest: PluginManifest

    @abstractmethod
    def commands(self) -> dict[str, str]:
        """Return command-name -> description."""

    @abstractmethod
    def run(self, command: str, argument: str) -> PluginResult:
        """Execute a plugin command."""
