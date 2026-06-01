from __future__ import annotations
from pathlib import Path
from dataclasses import asdict
from .scanner import FileScanner
from .organizer import build_organization_plan
from .duplicates import duplicate_groups
from .undo import UndoLog

class FileCleanupPlanner:
    def __init__(self, scanner: FileScanner | None = None):
        self.scanner = scanner or FileScanner()

    def plan(self, folder: str | Path, destination: str | Path | None = None) -> dict:
        files = self.scanner.scan(folder, hashes=True)
        destination = destination or Path(folder).expanduser().resolve() / 'NOVA_Organized'
        actions = build_organization_plan(files, destination)
        dupes = duplicate_groups(files)
        log_path = UndoLog().save_plan(actions)
        return {
            'files_scanned': len(files),
            'actions': [asdict(a) for a in actions[:250]],
            'actions_total': len(actions),
            'duplicates': [[f.path for f in group] for group in dupes[:50]],
            'undo_plan': str(log_path),
            'note': 'No files were changed. Review the plan before applying any move/delete action.'
        }
