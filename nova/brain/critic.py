from __future__ import annotations

from dataclasses import dataclass
from nova.core.models import ExecutionPlan, ExecutionReport, RiskLevel

@dataclass(slots=True)
class Critique:
    score: int
    issues: list[str]
    next_actions: list[str]


def critique(plan: ExecutionPlan, report: ExecutionReport | None = None) -> Critique:
    issues: list[str] = []
    next_actions: list[str] = []
    if plan.risk.level in {RiskLevel.REVIEW, RiskLevel.DANGEROUS} and not plan.dry_run:
        next_actions.append("Verify undo/recovery path before confirmed execution")
    if not plan.steps and not plan.risk.blocked:
        issues.append("No executable steps were produced")
    if report:
        for r in report.results:
            if not r.ok:
                issues.append(f"Tool failed: {r.tool}: {r.error}")
    if plan.risk.blocked:
        issues.append("Blocked by safety policy")
    if not issues:
        next_actions.append("Review the output and run confirmed mode only if side effects are desired")
    score = max(0, 100 - 20 * len(issues))
    return Critique(score, issues, next_actions)
