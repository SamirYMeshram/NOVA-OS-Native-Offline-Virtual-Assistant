from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from nova.core.events import AuditEvent, AuditLog
from nova.core.security import SafetyGuard
from nova.files.undo import FileOperation, UndoLogStore

CATEGORY_MAP: dict[str, set[str]] = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf"},
    "Spreadsheets": {".csv", ".xlsx", ".xls", ".ods"},
    "Images": {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "Code": {".py", ".js", ".ts", ".java", ".cpp", ".c", ".rs", ".go", ".html", ".css"},
    "Audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a"},
    "Video": {".mp4", ".mkv", ".mov", ".webm", ".avi"},
}


@dataclass(slots=True)
class PlannedMove:
    source: Path
    destination: Path
    reason: str


@dataclass(slots=True)
class OrganizePlan:
    root: Path
    moves: list[PlannedMove]
    warnings: list[str]


class FileOrganizer:
    """Creates safe file-organization plans and executes only with confirmation."""

    def __init__(self, guard: SafetyGuard | None = None) -> None:
        self.guard = guard or SafetyGuard()
        self.undo = UndoLogStore()
        self.audit = AuditLog()

    def plan_by_type(self, root: str | Path, recursive: bool = False) -> OrganizePlan:
        root_path = Path(root).expanduser().resolve()
        decision = self.guard.check_path_write(root_path)
        warnings: list[str] = []
        if not decision.allowed:
            raise PermissionError(decision.reason)
        if decision.requires_confirmation:
            warnings.append(decision.reason)
        iterator = root_path.rglob("*") if recursive else root_path.glob("*")
        moves: list[PlannedMove] = []
        for item in iterator:
            if not item.is_file() or item.name.startswith("."):
                continue
            category = self._category_for(item.suffix.lower())
            destination_dir = root_path / "NOVA_Organized" / category
            destination = self._avoid_collision(destination_dir / item.name)
            if destination.parent == item.parent:
                continue
            moves.append(PlannedMove(item, destination, f"categorized as {category}"))
        return OrganizePlan(root_path, moves, warnings)

    def execute(self, plan: OrganizePlan, confirmed: bool = False) -> Path:
        if not confirmed:
            raise PermissionError("Organization writes require explicit confirmation")
        operations: list[FileOperation] = []
        for move in plan.moves:
            decision = self.guard.check_path_write(move.destination)
            if not decision.allowed:
                continue
            move.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(move.source), str(move.destination))
            operations.append(FileOperation("move", str(move.destination), str(move.source), {"reason": move.reason}))
        undo_log = self.undo.save(operations)
        self.audit.write(AuditEvent("file_organize", "success", f"Moved {len(operations)} files", {"undo_log": str(undo_log)}))
        return undo_log

    @staticmethod
    def _category_for(suffix: str) -> str:
        for category, extensions in CATEGORY_MAP.items():
            if suffix in extensions:
                return category
        return "Other"

    @staticmethod
    def _avoid_collision(destination: Path) -> Path:
        if not destination.exists():
            return destination
        stem = destination.stem
        suffix = destination.suffix
        parent = destination.parent
        counter = 1
        while True:
            candidate = parent / f"{stem} ({counter}){suffix}"
            if not candidate.exists():
                return candidate
            counter += 1
