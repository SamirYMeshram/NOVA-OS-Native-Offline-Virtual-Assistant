from __future__ import annotations
from pathlib import Path
from .models import FileInfo, FileAction

SAFE_CATEGORY_DIRS = {
    'documents': 'Documents', 'spreadsheets': 'Spreadsheets', 'presentations': 'Presentations',
    'images': 'Images', 'audio': 'Audio', 'video': 'Video', 'archives': 'Archives', 'code': 'Code',
    'installers': 'Installers', 'other': 'Other'
}

def build_organization_plan(files: list[FileInfo], destination_root: str | Path) -> list[FileAction]:
    dest = Path(destination_root).expanduser().resolve()
    actions = []
    for f in files:
        target_dir = dest / SAFE_CATEGORY_DIRS.get(f.category, 'Other')
        target = target_dir / f.name
        if Path(f.path).resolve() == target.resolve():
            continue
        risk = 'medium' if f.risk_flags else 'low'
        actions.append(FileAction('move', f.path, str(target), f'Organize as {f.category}', risk, True))
    return actions
