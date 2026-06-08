from __future__ import annotations

from pathlib import Path
import json, datetime as dt


def render_report(title: str, sections: dict[str, object]) -> str:
    lines = [f"# {title}", "", f"Generated: {dt.datetime.now().isoformat(timespec='seconds')}", ""]
    for name, content in sections.items():
        lines.append(f"## {name}")
        lines.append("")
        if isinstance(content, str):
            lines.append(content)
        else:
            lines.append("```json")
            lines.append(json.dumps(content, indent=2, ensure_ascii=False, default=str))
            lines.append("```")
        lines.append("")
    return "\n".join(lines)


def save_report(path: str | Path, title: str, sections: dict[str, object]) -> str:
    p = Path(path).expanduser().resolve(strict=False)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render_report(title, sections), encoding="utf-8")
    return str(p)
