from __future__ import annotations
from collections import Counter
from .models import FileInfo

def scan_report(files: list[FileInfo]) -> str:
    by_cat = Counter(f.category for f in files)
    total = sum(f.size for f in files)
    lines = [f"Files scanned: {len(files)}", f"Total size: {total/1024/1024:.2f} MB", "Categories:"]
    lines += [f"- {k}: {v}" for k, v in by_cat.most_common()]
    risky = [f for f in files if f.risk_flags]
    if risky:
        lines.append("Risk flags:")
        for f in risky[:20]:
            lines.append(f"- {f.path}: {', '.join(f.risk_flags)}")
    return "\n".join(lines)
