from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from ..core.router import CommandRouter
from ..core.types import Intent, RiskLevel


class StepStatus(str, Enum):
    PENDING = "pending"
    NEEDS_CONFIRMATION = "needs_confirmation"
    READY = "ready"
    DONE = "done"


@dataclass(slots=True)
class PlanStep:
    title: str
    tool: str
    risk: RiskLevel = RiskLevel.SAFE
    status: StepStatus = StepStatus.PENDING
    details: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class AgentPlan:
    goal: str
    intent: Intent
    summary: str
    steps: list[PlanStep]
    requires_confirmation: bool


class AgentPlanner:
    """Creates transparent multi-step plans before NOVA acts."""

    def __init__(self, router: CommandRouter | None = None) -> None:
        self.router = router or CommandRouter()

    def plan(self, goal: str) -> AgentPlan:
        command = self.router.route(goal)
        if command.intent == Intent.FILE_ORGANIZE:
            steps = [
                PlanStep("Scan target folder", "files.scan", RiskLevel.SAFE, StepStatus.READY),
                PlanStep("Classify files by type/project/date", "files.classify", RiskLevel.SAFE),
                PlanStep("Detect duplicates and risky files", "files.scan", RiskLevel.SAFE),
                PlanStep("Create reversible move plan", "files.plan", RiskLevel.MEDIUM, StepStatus.NEEDS_CONFIRMATION),
                PlanStep("Apply only after explicit confirmation", "files.apply", RiskLevel.MEDIUM, StepStatus.NEEDS_CONFIRMATION),
            ]
            return AgentPlan(goal, command.intent, "Safe folder cleanup plan with no deletion and undo logs.", steps, True)
        if command.intent == Intent.DOCUMENT_ASK:
            steps = [
                PlanStep("Check document index", "documents.stats"),
                PlanStep("Retrieve relevant chunks", "documents.search"),
                PlanStep("Answer only from retrieved context", "documents.qa"),
                PlanStep("Return citations", "documents.citations"),
            ]
            return AgentPlan(goal, command.intent, "Document question answering plan with citations.", steps, False)
        if command.intent == Intent.CODE_GENERATE:
            steps = [
                PlanStep("Create project file plan", "code.plan", RiskLevel.LOW),
                PlanStep("Write files only with confirmation", "code.generate", RiskLevel.MEDIUM, StepStatus.NEEDS_CONFIRMATION),
                PlanStep("Run safe tests", "code.test", RiskLevel.LOW),
                PlanStep("Create README", "code.docs", RiskLevel.LOW),
            ]
            return AgentPlan(goal, command.intent, "Local code generation plan with confirmation gates.", steps, True)
        return AgentPlan(goal, command.intent, "General response plan.", [PlanStep("Answer safely and locally", "chat")], False)
