from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json

@dataclass(slots=True)
class FolderPolicy:
    path: str
    allow_index: bool = True
    allow_search: bool = True
    allow_cleanup_plan: bool = True
    allow_move: bool = False
    notes: str = ""

class PolicyBook:
    def __init__(self, path: Path) -> None:
        self.path = path; self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists(): self.path.write_text("[]", encoding="utf-8")

    def list(self) -> list[FolderPolicy]:
        return [FolderPolicy(**x) for x in json.loads(self.path.read_text(encoding="utf-8"))]

    def set(self, policy: FolderPolicy) -> None:
        rows = [p for p in self.list() if p.path != policy.path]
        rows.append(policy)
        self.path.write_text(json.dumps([asdict(p) for p in rows], indent=2), encoding="utf-8")

    def decide(self, path: str, action: str) -> bool:
        matches = [p for p in self.list() if path.startswith(p.path)]
        if not matches: return action not in {"move", "delete"}
        p = max(matches, key=lambda x: len(x.path))
        return {
            "index": p.allow_index, "search": p.allow_search, "cleanup_plan": p.allow_cleanup_plan, "move": p.allow_move,
        }.get(action, False)
