from __future__ import annotations
import subprocess, os
from dataclasses import asdict
from pathlib import Path
from nova.core.audit import AuditLog
from nova.core.security import validate_user_path
from .policy import AutomationRequest, AutomationPolicy

class AutomationExecutor:
    def __init__(self, policy: AutomationPolicy | None = None, audit: AuditLog | None = None):
        self.policy = policy or AutomationPolicy()
        self.audit = audit or AuditLog()

    def run_shell(self, command: str, *, confirmed: bool = False) -> dict:
        decision = self.policy.evaluate(AutomationRequest('shell', command))
        if not decision.allowed or decision.requires_confirmation and not confirmed:
            return {'ok': False, 'decision': asdict(decision)}
        proc = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=30)
        self.audit.write('automation.shell', 'ok' if proc.returncode == 0 else 'failed', command=command, returncode=proc.returncode)
        return {'ok': proc.returncode == 0, 'stdout': proc.stdout, 'stderr': proc.stderr, 'returncode': proc.returncode}

    def create_folder(self, path: str | Path) -> dict:
        p = validate_user_path(path, allow_missing=True)
        p.mkdir(parents=True, exist_ok=True)
        self.audit.write('automation.create_folder', 'ok', path=str(p))
        return {'ok': True, 'path': str(p)}

    def create_file(self, path: str | Path, content: str = '') -> dict:
        p = validate_user_path(path, allow_missing=True)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        self.audit.write('automation.create_file', 'ok', path=str(p))
        return {'ok': True, 'path': str(p)}
