from __future__ import annotations
from pathlib import Path
import json
from nova.core.time import utc_now
from .models import CleanupPlan

class UndoLog:
    def __init__(self, dir_path: str | Path):
        self.dir_path = Path(dir_path)
        self.dir_path.mkdir(parents=True, exist_ok=True)

    def record_plan(self, plan: CleanupPlan) -> Path:
        path = self.dir_path / f"undo-plan-{utc_now().replace(':','-')}.json"
        data = {
            'root': str(plan.root),
            'created_at': utc_now(),
            'actions': [
                {'action': a.action, 'source': str(a.source), 'target': str(a.target) if a.target else None, 'reason': a.reason, 'risk': a.risk}
                for a in plan.actions
            ],
        }
        path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        return path
