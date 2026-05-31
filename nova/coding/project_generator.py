from __future__ import annotations

from pathlib import Path

from ..core.safety import SafetyGuard
from ..core.types import FileAction, OperationPlan, RiskLevel


class ProjectGenerator:
    """Generates local project templates without running unsafe commands."""

    def __init__(self, safety: SafetyGuard | None = None) -> None:
        self.safety = safety or SafetyGuard()

    def create_python_cli(self, root: str | Path, name: str, confirmed: bool = False) -> Path:
        dest = Path(root).expanduser().resolve() / name
        files = self._python_cli_files(name)
        plan = OperationPlan(
            f"Create Python CLI project {name}",
            RiskLevel.MEDIUM,
            [FileAction("write", dest / rel, dest / rel, RiskLevel.MEDIUM, "Generate project file") for rel in files],
            True,
        )
        self.safety.validate_plan(plan, confirmed=confirmed)
        for rel, content in files.items():
            p = dest / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            if p.exists():
                raise FileExistsError(p)
            p.write_text(content, encoding="utf-8")
        return dest

    def create_fastapi_app(self, root: str | Path, name: str, confirmed: bool = False) -> Path:
        dest = Path(root).expanduser().resolve() / name
        files = self._fastapi_files(name)
        plan = OperationPlan(
            f"Create FastAPI project {name}",
            RiskLevel.MEDIUM,
            [FileAction("write", dest / rel, dest / rel, RiskLevel.MEDIUM, "Generate FastAPI file") for rel in files],
            True,
        )
        self.safety.validate_plan(plan, confirmed=confirmed)
        for rel, content in files.items():
            p = dest / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            if p.exists():
                raise FileExistsError(p)
            p.write_text(content, encoding="utf-8")
        return dest

    def _python_cli_files(self, name: str) -> dict[str, str]:
        pkg = name.replace("-", "_")
        return {
            "pyproject.toml": f'''[build-system]\nrequires=["setuptools>=68"]\nbuild-backend="setuptools.build_meta"\n\n[project]\nname="{name}"\nversion="0.1.0"\nrequires-python=">=3.11"\n\n[project.scripts]\n{pkg}="{pkg}.cli:main"\n''',
            f"{pkg}/__init__.py": "__version__ = '0.1.0'\n",
            f"{pkg}/cli.py": "def main():\n    print('Hello from generated project')\n",
            "tests/test_cli.py": f"from {pkg}.cli import main\n\ndef test_main_exists():\n    assert callable(main)\n",
            "README.md": f"# {name}\n\nGenerated locally by NOVA Sovereign AI.\n",
        }

    def _fastapi_files(self, name: str) -> dict[str, str]:
        pkg = name.replace("-", "_")
        return {
            "pyproject.toml": f'''[build-system]\nrequires=["setuptools>=68"]\nbuild-backend="setuptools.build_meta"\n\n[project]\nname="{name}"\nversion="0.1.0"\nrequires-python=">=3.11"\ndependencies=["fastapi", "uvicorn"]\n''',
            f"{pkg}/main.py": "from fastapi import FastAPI\n\napp = FastAPI(title='Generated App')\n\n@app.get('/health')\ndef health():\n    return {'ok': True}\n",
            "README.md": f"# {name}\n\nRun: `uvicorn {pkg}.main:app --reload`\n",
        }
