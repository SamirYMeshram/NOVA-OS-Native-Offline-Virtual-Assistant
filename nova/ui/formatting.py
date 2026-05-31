from __future__ import annotations
import json

def as_json(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)

def table(rows: list[dict]) -> str:
    if not rows:
        return ''
    keys = list(rows[0].keys())
    out = [' | '.join(keys), ' | '.join(['---']*len(keys))]
    for row in rows:
        out.append(' | '.join(str(row.get(k,'')) for k in keys))
    return '\n'.join(out)
