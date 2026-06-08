from __future__ import annotations

from pathlib import Path
import re

DANGEROUS_PATTERNS = [
    (re.compile(r"subprocess\.(run|Popen|call)\([^\)]*shell\s*=\s*True"), "shell=True subprocess usage"),
    (re.compile(r"eval\s*\("), "eval usage"),
    (re.compile(r"exec\s*\("), "exec usage"),
    (re.compile(r"pickle\.loads?\s*\("), "pickle load usage"),
    (re.compile(r"requests\.(get|post|put|delete)\("), "network call"),
]

def security_review(path: str | Path) -> dict[str, object]:
    root = Path(path).expanduser().resolve(strict=False)
    findings = []
    for p in root.rglob("*.py"):
        if ".git" in p.parts: continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for pat, label in DANGEROUS_PATTERNS:
            for m in pat.finditer(text):
                line = text[:m.start()].count("\n") + 1
                findings.append({"file": str(p), "line": line, "issue": label})
    return {"root": str(root), "findings": findings, "risk": "review" if findings else "low"}
