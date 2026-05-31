from __future__ import annotations
from pathlib import Path

class WorkspaceManager:
    def create_workspace(self, root: str | Path, name: str, confirmed: bool = False) -> dict:
        if not confirmed:
            return {'ok': False, 'requires_confirmation': True, 'message': 'Workspace creation requires confirmation'}
        base = Path(root).expanduser().resolve() / name
        for sub in ['docs', 'src', 'data', 'reports', 'notes']:
            (base / sub).mkdir(parents=True, exist_ok=True)
        (base / 'README.md').write_text(f'# {name}\n\nWorkspace created by NOVA.\n', encoding='utf-8')
        return {'ok': True, 'path': str(base)}
