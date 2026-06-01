from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
from datetime import datetime, timezone
import json, uuid
from nova.core.paths import data_dir
from .models import FileAction

class UndoLog:
    def __init__(self, root: Path | None = None):
        self.root = root or data_dir() / 'undo'
        self.root.mkdir(parents=True, exist_ok=True)

    def save_plan(self, actions: list[FileAction]) -> Path:
        name = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8] + '.json'
        path = self.root / name
        payload = {'created_at': datetime.now(timezone.utc).isoformat(), 'actions': [asdict(a) for a in actions]}
        path.write_text(json.dumps(payload, indent=2), encoding='utf-8')
        return path

    def list_logs(self) -> list[Path]:
        return sorted(self.root.glob('*.json'), reverse=True)
