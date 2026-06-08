from __future__ import annotations

from pathlib import Path
from nova.config import NovaConfig
from dataclasses import asdict
from nova.core.models import Observation
from .planner import plan
from .executor import PlanExecutor
from .critic import critique

class AutonomousCore:
    def __init__(self, config: NovaConfig) -> None:
        self.config = config
        self.executor = PlanExecutor(config)

    def think(self, text: str, cwd: str | Path | None = None) -> dict[str, object]:
        obs = Observation(text=text, cwd=Path(cwd or Path.cwd()).resolve())
        p = plan(obs, dry_run=True)
        c = critique(p)
        return {"observation": {"text": text, "cwd": str(obs.cwd)}, "plan": p.to_dict(), "critique": asdict(c)}

    def run(self, text: str, cwd: str | Path | None = None, dry_run: bool = True, confirm: str | None = None) -> dict[str, object]:
        obs = Observation(text=text, cwd=Path(cwd or Path.cwd()).resolve())
        p = plan(obs, dry_run=dry_run)
        report = self.executor.execute(p, confirm=confirm)
        c = critique(p, report)
        return {"plan": p.to_dict(), "report": report.to_dict(), "critique": asdict(c)}
