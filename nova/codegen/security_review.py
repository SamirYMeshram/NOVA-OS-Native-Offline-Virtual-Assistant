from __future__ import annotations
import re
from pathlib import Path
from nova.core.security import validate_user_path

PATTERNS = {
    'hardcoded-secret': re.compile(r'(?i)(password|secret|token|api_key)\s*=\s*["\'][^"\']{6,}["\']'),
    'shell-true': re.compile(r'subprocess\.[a-z_]+\([^\n]*shell\s*=\s*True'),
    'pickle-load': re.compile(r'pickle\.load'),
    'eval-exec': re.compile(r'\b(eval|exec)\s*\('),
}

class SecurityReviewer:
    def review(self, root: str | Path) -> dict:
        rootp = validate_user_path(root)
        findings = []
        for p in rootp.rglob('*'):
            if not p.is_file() or p.suffix.lower() not in {'.py', '.js', '.ts', '.env', '.txt'}:
                continue
            try:
                text = p.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            for name, pattern in PATTERNS.items():
                for m in pattern.finditer(text):
                    line = text[:m.start()].count('\n') + 1
                    findings.append({'rule': name, 'path': str(p), 'line': line})
        return {'findings': findings, 'finding_count': len(findings)}
