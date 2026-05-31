from __future__ import annotations

from pathlib import Path


class CodebaseAnalyzer:
    def summarize(self, root: str | Path) -> dict[str, object]:
        base = Path(root).expanduser().resolve()
        files = [p for p in base.rglob("*") if p.is_file() and not any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in p.parts)]
        by_ext: dict[str, int] = {}
        todo_count = 0
        test_files = 0
        for p in files:
            by_ext[p.suffix.lower() or "<none>"] = by_ext.get(p.suffix.lower() or "<none>", 0) + 1
            if p.name.startswith("test_") or "/tests/" in str(p):
                test_files += 1
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")[:200_000]
                todo_count += text.lower().count("todo") + text.lower().count("fixme")
            except Exception:
                pass
        suggestions = []
        if test_files == 0:
            suggestions.append("No obvious tests found. Add unit tests for core logic.")
        if "README.md" not in {p.name for p in files}:
            suggestions.append("No README.md found. Add setup and usage documentation.")
        if todo_count:
            suggestions.append(f"Found {todo_count} TODO/FIXME markers. Review them before release.")
        return {"root": str(base), "files": len(files), "by_extension": by_ext, "test_files": test_files, "todo_markers": todo_count, "suggestions": suggestions}
