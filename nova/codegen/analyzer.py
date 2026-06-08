from __future__ import annotations

from pathlib import Path
import ast, json

IMPORTANT = {"pyproject.toml", "requirements.txt", "setup.py", "README.md", "Dockerfile", "package.json"}


def analyze_codebase(path: str | Path) -> dict[str, object]:
    root = Path(path).expanduser().resolve(strict=False)
    files = [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    py_files = [p for p in files if p.suffix == ".py"]
    tests = [p for p in files if "test" in p.name.lower() or "tests" in p.parts]
    imports: dict[str, int] = {}
    functions = 0; classes = 0; syntax_errors: list[str] = []
    for p in py_files[:500]:
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError as exc:
            syntax_errors.append(f"{p}: {exc}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)): functions += 1
            elif isinstance(node, ast.ClassDef): classes += 1
            elif isinstance(node, ast.Import):
                for n in node.names: imports[n.name.split('.')[0]] = imports.get(n.name.split('.')[0], 0)+1
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports[node.module.split('.')[0]] = imports.get(node.module.split('.')[0], 0)+1
    recommendations = []
    if not tests: recommendations.append("Add tests; no obvious test files found")
    if not (root / "README.md").exists(): recommendations.append("Add README.md")
    if not any((root / name).exists() for name in ["pyproject.toml", "requirements.txt", "setup.py"]): recommendations.append("Add dependency/project metadata")
    if syntax_errors: recommendations.append("Fix Python syntax errors before running automation")
    return {
        "root": str(root), "files": len(files), "python_files": len(py_files), "test_files": len(tests),
        "functions": functions, "classes": classes, "top_imports": sorted(imports.items(), key=lambda kv: kv[1], reverse=True)[:20],
        "important_files": [str(root / x) for x in IMPORTANT if (root / x).exists()], "syntax_errors": syntax_errors,
        "recommendations": recommendations,
    }
