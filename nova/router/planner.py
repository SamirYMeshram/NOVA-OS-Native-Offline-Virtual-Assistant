from __future__ import annotations
from dataclasses import dataclass
from .intents import Intent
from nova.security.policy import SafetyPolicy

@dataclass(slots=True)
class PlanStep:
    order: int
    tool: str
    description: str
    risk: str = 'low'
    requires_confirmation: bool = False

@dataclass(slots=True)
class ExecutionPlan:
    intent: Intent
    steps: list[PlanStep]
    requires_confirmation: bool

class Planner:
    def __init__(self):
        self.safety = SafetyPolicy()

    def plan(self, intent: Intent, command: str) -> ExecutionPlan:
        decision = self.safety.assess_text_command(command)
        steps = [PlanStep(1, intent.value, f"Handle intent {intent.value}", decision.risk.value, decision.requires_confirmation)]
        if intent == Intent.FILE_ORGANIZE:
            steps = [
                PlanStep(1, 'file_scan', 'Scan folder and classify files', 'low', False),
                PlanStep(2, 'cleanup_plan', 'Generate non-destructive cleanup plan', 'medium', False),
                PlanStep(3, 'confirmation_gate', 'Ask before moving anything', 'high', True),
            ]
        elif intent == Intent.DOCUMENT_QA:
            steps = [
                PlanStep(1, 'vector_search', 'Retrieve relevant local chunks', 'low', False),
                PlanStep(2, 'local_model', 'Answer with citations from chunks', 'low', False),
            ]
        return ExecutionPlan(intent, steps, any(s.requires_confirmation for s in steps) or decision.requires_confirmation)
