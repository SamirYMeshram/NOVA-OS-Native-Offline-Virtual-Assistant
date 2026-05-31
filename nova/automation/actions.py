from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True)
class ActionRequest:
    name: str
    args: dict
    risk: str = "low"
    requires_confirmation: bool = False

@dataclass(slots=True)
class ActionResult:
    ok: bool
    message: str
    data: dict | None = None

class SafeFileActions:
    def create_folder(self, path: str | Path, confirmed: bool = False) -> ActionResult:
        if not confirmed:
            return ActionResult(False, "Folder creation requires explicit confirmation", {'requires_confirmation': True})
        p = Path(path).expanduser().resolve()
        p.mkdir(parents=True, exist_ok=True)
        return ActionResult(True, f"Created folder {p}", {'path': str(p)})

    def create_text_file(self, path: str | Path, content: str, confirmed: bool = False) -> ActionResult:
        if not confirmed:
            return ActionResult(False, "File write requires explicit confirmation", {'requires_confirmation': True})
        p = Path(path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        return ActionResult(True, f"Created file {p}", {'path': str(p)})
