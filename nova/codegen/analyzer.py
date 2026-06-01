from __future__ import annotations
from pathlib import Path
from collections import Counter
from nova.core.security import validate_user_path

FRAMEWORK_HINTS = {
    'fastapi': ['fastapi', 'uvicorn'], 'flask': ['flask'], 'django': ['django'],
    'react': ['react', 'vite', 'next'], 'pytest': ['pytest'], 'sqlalchemy': ['sqlalchemy']
}

class CodebaseAnalyzer:
    def analyze(self, root: str | Path) -> dict:
        rootp = validate_user_path(root)
        files = [p for p in rootp.rglob('*') if p.is_file() and '.git' not in p.parts]
        suffixes = Counter(p.suffix.lower() or '<none>' for p in files)
        texts = ''
        for p in files[:250]:
            if p.suffix.lower() in {'.py', '.toml', '.txt', '.md', '.json', '.js', '.ts'}:
                try:
                    texts += '\n' + p.read_text(encoding='utf-8', errors='ignore')[:20000].lower()
                except Exception:
                    pass
        frameworks = [name for name, hints in FRAMEWORK_HINTS.items() if any(h in texts for h in hints)]
        risks = []
        if 'eval(' in texts or 'exec(' in texts:
            risks.append('dynamic-code-execution-found')
        if 'subprocess' in texts and 'shell=true' in texts:
            risks.append('subprocess-shell-true')
        return {'root': str(rootp), 'file_count': len(files), 'suffixes': dict(suffixes), 'frameworks': frameworks, 'risks': risks, 'recommendations': self._recommend(files, frameworks, risks)}

    def _recommend(self, files, frameworks, risks):
        rec = []
        names = {p.name for p in files}
        if 'README.md' not in names:
            rec.append('Add a README.md with setup, run, and test instructions.')
        if 'pytest' not in frameworks and not any(p.name.startswith('test_') for p in files):
            rec.append('Add tests for core logic.')
        if risks:
            rec.append('Review flagged security risks before running automation.')
        return rec
