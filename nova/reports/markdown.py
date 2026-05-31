from __future__ import annotations
from pathlib import Path

class MarkdownReport:
    def __init__(self, title: str):
        self.title = title
        self.sections: list[tuple[str, str]] = []

    def add(self, heading: str, body: str) -> None:
        self.sections.append((heading, body))

    def render(self) -> str:
        parts = [f'# {self.title}', '']
        for heading, body in self.sections:
            parts.append(f'## {heading}')
            parts.append(body)
            parts.append('')
        return '\n'.join(parts)

    def save(self, path: str | Path) -> Path:
        p = Path(path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.render(), encoding='utf-8')
        return p
