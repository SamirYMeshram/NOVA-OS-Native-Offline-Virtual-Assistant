from __future__ import annotations
from pathlib import Path
import shutil
from dataclasses import asdict
from nova.core.security import validate_user_path
from nova.core.audit import AuditLog
from .models import FileAction

class FileActionExecutor:
    def __init__(self, audit: AuditLog | None = None):
        self.audit = audit or AuditLog()

    def apply(self, actions: list[FileAction], *, confirmed: bool = False) -> dict:
        if not confirmed:
            return {'applied': 0, 'refused': len(actions), 'reason': 'confirmation_required'}
        applied, failed = 0, []
        for a in actions:
            try:
                if a.action != 'move':
                    raise ValueError('Only safe move is supported by default')
                src = validate_user_path(a.source)
                dst = validate_user_path(a.target, allow_missing=True)
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists():
                    dst = dst.with_name(dst.stem + '.nova-copy' + dst.suffix)
                shutil.move(str(src), str(dst))
                applied += 1
                self.audit.write('file.move', 'ok', source=str(src), target=str(dst))
            except Exception as exc:
                failed.append({'action': asdict(a), 'error': str(exc)})
                self.audit.write('file.move', 'failed', source=a.source, target=a.target, error=str(exc))
        return {'applied': applied, 'failed': failed}
