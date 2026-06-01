from __future__ import annotations
from dataclasses import dataclass, field
from .intents import Intent

@dataclass(slots=True)
class PlanStep:
    name: str
    description: str
    safe: bool = True
    requires_confirmation: bool = False

@dataclass(slots=True)
class AgentPlan:
    intent: Intent
    summary: str
    steps: list[PlanStep] = field(default_factory=list)

class AgentPlanner:
    def plan(self, intent: Intent, command: str) -> AgentPlan:
        if intent == Intent.FILE_CLEAN_PLAN:
            return AgentPlan(intent, 'Safely clean/organize files without deleting anything first', [
                PlanStep('scan', 'Scan selected folder and collect metadata'),
                PlanStep('classify', 'Classify files by type, risk, size, age'),
                PlanStep('plan', 'Create move-only cleanup plan and undo log'),
                PlanStep('confirm', 'Ask for confirmation before applying file changes', True, True),
            ])
        if intent == Intent.DOCUMENT_QA:
            return AgentPlan(intent, 'Answer from local indexed document chunks', [PlanStep('retrieve', 'Find relevant local chunks'), PlanStep('answer', 'Answer with citations')])
        if intent == Intent.AUTOMATION:
            return AgentPlan(intent, 'Evaluate automation safety before execution', [PlanStep('policy', 'Apply safety policy'), PlanStep('confirm', 'Require confirmation for risky action', True, True)])
        return AgentPlan(intent, 'Route command to the appropriate NOVA subsystem', [PlanStep('classify', 'Classify intent'), PlanStep('dispatch', 'Call tool/provider')])
