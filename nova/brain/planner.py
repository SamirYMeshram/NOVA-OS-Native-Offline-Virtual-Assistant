from __future__ import annotations

from pathlib import Path
from nova.core.models import Observation, ExecutionPlan, PlanStep, RiskLevel, Intent, new_id
from nova.security.policy import assess_goal
from .nlu import classify, extract_entities


def plan(observation: Observation, dry_run: bool = True) -> ExecutionPlan:
    intents = classify(observation.text)
    entities = extract_entities(observation.text)
    risk = assess_goal(observation.text)
    steps: list[PlanStep] = []
    primary = intents[0].intent
    goal = observation.text
    target = entities.paths[0] if entities.paths else str(observation.cwd)

    def step(title: str, tool: str, args: dict, risk_level: RiskLevel = RiskLevel.SAFE, deps: list[str] | None = None):
        sid = f"s{len(steps)+1}"
        steps.append(PlanStep(sid, title, tool, args, deps or [], risk_level))
        return sid

    if primary == Intent.FILE_CLEANUP_PLAN:
        a = step("Scan target folder", "file.scan", {"path": target})
        step("Build reversible cleanup plan", "file.cleanup_plan", {"path": target}, RiskLevel.REVIEW, [a])
        step("Critique plan for risky moves", "critic.review", {"topic": "cleanup"}, RiskLevel.SAFE, [a])
    elif primary == Intent.FILE_SCAN:
        step("Scan target folder", "file.scan", {"path": target})
    elif primary == Intent.FILE_SEARCH:
        query = observation.text
        step("Search filenames and supported content", "file.search", {"path": target, "query": query})
    elif primary == Intent.DOCUMENT_INDEX:
        step("Index local documents", "document.index", {"path": target})
    elif primary == Intent.DOCUMENT_QA:
        step("Search local document index", "document.ask", {"question": observation.text})
    elif primary == Intent.DATA_PROFILE:
        step("Profile dataset", "data.profile", {"path": target})
    elif primary == Intent.CODE_ANALYZE:
        a = step("Analyze codebase", "code.analyze", {"path": target})
        step("Run security review", "code.security_review", {"path": target}, RiskLevel.SAFE, [a])
    elif primary == Intent.PROJECT_FORGE:
        step("Create project blueprint", "forge.blueprint", {"goal": goal})
        step("Dry-run project file generation", "forge.build", {"goal": goal, "output_dir": str(observation.cwd), "dry_run": True}, RiskLevel.REVIEW)
    elif primary == Intent.MEMORY_SAVE:
        step("Save durable memory", "memory.add", {"text": observation.text, "kind": "note"})
    elif primary == Intent.MEMORY_SEARCH:
        step("Search memory", "memory.search", {"query": observation.text})
    elif primary == Intent.TASK_CREATE:
        step("Create task", "task.add", {"title": observation.text}, RiskLevel.REVIEW)
    else:
        step("Generate local assistant response", "chat.complete", {"message": observation.text})
    if risk.blocked:
        steps = []
    return ExecutionPlan(new_id("plan"), goal, intents, entities, risk, steps, dry_run=dry_run)
