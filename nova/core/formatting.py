from __future__ import annotations

from typing import Iterable, Mapping, Any


def bullet(items: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def table(rows: list[Mapping[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "(no rows)"
    columns = columns or list(rows[0].keys())
    widths = {c: max(len(str(c)), *(len(str(r.get(c, ''))) for r in rows)) for c in columns}
    header = " | ".join(str(c).ljust(widths[c]) for c in columns)
    sep = "-+-".join("-" * widths[c] for c in columns)
    body = [" | ".join(str(r.get(c, '')).ljust(widths[c]) for c in columns) for r in rows]
    return "\n".join([header, sep, *body])
