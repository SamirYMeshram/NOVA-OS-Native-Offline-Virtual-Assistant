from __future__ import annotations
from pathlib import Path
from collections import Counter

class CodebaseAnalyzer:
    def analyze(self, root: str | Path) -> dict:
        base = Path(root).expanduser().resolve()
        files = [p for p in base.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts]
        exts = Counter(p.suffix.lower() or '<none>' for p in files)
        py_files = [p for p in files if p.suffix == '.py']
        lines = 0
        todos = []
        for p in py_files:
            text = p.read_text(encoding='utf-8', errors='ignore')
            lines += text.count('\n') + 1
            for i, line in enumerate(text.splitlines(), 1):
                if 'TODO' in line or 'FIXME' in line:
                    todos.append({'file': str(p), 'line': i, 'text': line.strip()})
        return {'root': str(base), 'files': len(files), 'extensions': dict(exts), 'python_files': len(py_files), 'python_lines': lines, 'todos': todos[:100]}
