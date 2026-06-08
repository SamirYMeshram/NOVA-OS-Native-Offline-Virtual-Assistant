from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json, time

@dataclass(slots=True)
class Evaluation:
    workflow: str
    score: int
    strengths: list[str]
    weaknesses: list[str]
    next_improvements: list[str]
    created_at: float


def evaluate_run(workflow: str, result: dict[str, object]) -> Evaluation:
    weaknesses = []
    strengths = []
    if result.get("report", {}).get("ok") is True: strengths.append("execution report ok")
    if result.get("report", {}).get("blocked") is True: weaknesses.append("blocked by safety or missing confirmation")
    if not result.get("plan", {}).get("steps"): weaknesses.append("no plan steps generated")
    if result.get("critique", {}).get("issues"): weaknesses.extend(result["critique"]["issues"])
    if not weaknesses: strengths.append("no issues found by critic")
    score = max(0, min(100, 80 + 5*len(strengths) - 15*len(weaknesses)))
    nexts = ["Add stronger entity extraction", "Add workflow-specific tests", "Improve UI for reviewing outputs"] if weaknesses else ["Save as successful workflow pattern"]
    return Evaluation(workflow, score, strengths, weaknesses, nexts, time.time())

class ImprovementJournal:
    def __init__(self, path: Path) -> None:
        self.path = path; self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, evaluation: Evaluation) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(evaluation), ensure_ascii=False) + "\n")

    def list(self) -> list[Evaluation]:
        if not self.path.exists(): return []
        out=[]
        for line in self.path.read_text(encoding="utf-8").splitlines():
            try: out.append(Evaluation(**json.loads(line)))
            except Exception: pass
        return out
