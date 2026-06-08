from __future__ import annotations

from nova.core.models import ExecutionPlan, ExecutionReport, ToolResult
from nova.config import NovaConfig
from nova.security.policy import check_confirmation
from nova.security.audit import AuditLog
from .tools import ToolRuntime

class PlanExecutor:
    def __init__(self, config: NovaConfig, runtime: ToolRuntime | None = None) -> None:
        self.config = config
        self.runtime = runtime or ToolRuntime(config)
        self.audit = AuditLog(config.log_dir / "audit.jsonl")

    def execute(self, plan: ExecutionPlan, confirm: str | None = None) -> ExecutionReport:
        approval = check_confirmation(plan.risk.requires_confirmation and not plan.dry_run, confirm, self.config.safety.confirm_token)
        if plan.risk.blocked:
            self.audit.write("plan.blocked", plan=plan.to_dict())
            return ExecutionReport(plan.id, plan.dry_run, [], blocked=True, summary="Plan blocked by safety policy")
        if not approval.confirmed:
            return ExecutionReport(plan.id, plan.dry_run, [], blocked=True, summary=approval.reason)
        results: list[ToolResult] = []
        completed: set[str] = set()
        for step in plan.steps:
            if any(dep not in completed for dep in step.depends_on):
                results.append(ToolResult(step.tool, False, error="Dependency not completed", risk=step.risk))
                continue
            result = self.runtime.call(step.tool, step.args, dry_run=plan.dry_run)
            results.append(result)
            if result.ok:
                completed.add(step.id)
        report = ExecutionReport(plan.id, plan.dry_run, results, summary=f"Executed {len(results)} step(s); dry_run={plan.dry_run}")
        self.audit.write("plan.executed", plan_id=plan.id, dry_run=plan.dry_run, ok=report.ok)
        return report
