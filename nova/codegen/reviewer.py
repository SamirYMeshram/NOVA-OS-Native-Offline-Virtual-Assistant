from __future__ import annotations
from pathlib import Path

class CodeReviewer:
    risky_patterns = ['eval(', 'exec(', 'subprocess.call(', 'shell=True', 'pickle.loads', 'yaml.load(']

    def review_file(self, path: str | Path) -> list[dict]:
        p = Path(path)
        findings = []
        text = p.read_text(encoding='utf-8', errors='ignore')
        for i, line in enumerate(text.splitlines(), 1):
            for pattern in self.risky_patterns:
                if pattern in line:
                    findings.append({'file': str(p), 'line': i, 'severity': 'medium', 'pattern': pattern, 'message': 'Review risky code pattern'})
            if len(line) > 140:
                findings.append({'file': str(p), 'line': i, 'severity': 'low', 'pattern': 'long-line', 'message': 'Long line may hurt maintainability'})
        return findings

    def review_tree(self, root: str | Path) -> list[dict]:
        findings = []
        for p in Path(root).rglob('*.py'):
            if '__pycache__' in p.parts or '.venv' in p.parts:
                continue
            findings.extend(self.review_file(p))
        return findings
