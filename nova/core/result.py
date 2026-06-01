from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class Result:
    ok: bool
    message: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    @classmethod
    def success(cls, message: str = "", **data: Any) -> "Result":
        return cls(True, message, data)

    @classmethod
    def failure(cls, message: str, **data: Any) -> "Result":
        return cls(False, message, data)

    def as_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "message": self.message, "data": self.data, "warnings": self.warnings}
