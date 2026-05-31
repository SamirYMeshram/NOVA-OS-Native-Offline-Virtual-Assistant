from __future__ import annotations
from pathlib import Path
from .models import FileScanReport, CleanupPlan, FileAction

class FileOrganizer:
    def plan_by_category(self, report: FileScanReport, destination: str | Path | None = None) -> CleanupPlan:
        dest = Path(destination).expanduser().resolve() if destination else report.root / 'NOVA_Organized'
        actions: list[FileAction] = []
        for info in report.files:
            if 'NOVA_Organized' in info.path.parts:
                continue
            target = dest / info.category / info.path.name
            risk = 'medium' if info.risk != 'low' else 'low'
            actions.append(FileAction('move', info.path, target, f"Organize as {info.category}", risk))
        return CleanupPlan(report.root, actions, requires_confirmation=True)

    def render_plan(self, plan: CleanupPlan, limit: int = 200) -> str:
        lines = [f"Cleanup plan for {plan.root}", f"Actions: {len(plan.actions)}", "Requires confirmation: yes"]
        for action in plan.actions[:limit]:
            lines.append(f"- {action.action}: {action.source} -> {action.target} [{action.risk}] {action.reason}")
        if len(plan.actions) > limit:
            lines.append(f"... {len(plan.actions)-limit} more actions")
        return '\n'.join(lines)
