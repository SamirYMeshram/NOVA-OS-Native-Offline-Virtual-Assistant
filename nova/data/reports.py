from __future__ import annotations
import json

def profile_to_markdown(profile: dict) -> str:
    lines = [f"# Dataset Profile", f"Type: {profile.get('type')}", f"Rows: {profile.get('rows')}"]
    cols = profile.get('columns') or []
    lines.append(f"Columns: {', '.join(cols)}")
    if 'stats' in profile:
        lines.append('\n## Column stats')
        for name, stat in profile['stats'].items():
            lines.append(f"- **{name}**: {json.dumps(stat, ensure_ascii=False)}")
    return '\n'.join(lines)
