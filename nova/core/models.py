from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Iterable
import json
import time
import uuid


class RiskLevel(str, Enum):
    SAFE = "safe"
    REVIEW = "review"
    DANGEROUS = "dangerous"
    BLOCKED = "blocked"


class Intent(str, Enum):
    CHAT = "chat"
    MEMORY_SAVE = "memory.save"
    MEMORY_SEARCH = "memory.search"
    TASK_CREATE = "task.create"
    TASK_LIST = "task.list"
    DOCUMENT_INDEX = "document.index"
    DOCUMENT_QA = "document.qa"
    FILE_SCAN = "file.scan"
    FILE_SEARCH = "file.search"
    FILE_CLEANUP_PLAN = "file.cleanup_plan"
    DATA_PROFILE = "data.profile"
    CODE_ANALYZE = "code.analyze"
    PROJECT_FORGE = "project.forge"
    SYSTEM_STATUS = "system.status"
    PLUGIN_RUN = "plugin.run"
    WORKFLOW_RUN = "workflow.run"
    AUTOMATION = "automation"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class Observation:
    text: str
    cwd: Path
    created_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class IntentScore:
    intent: Intent
    confidence: float
    evidence: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EntitySet:
    paths: list[str] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)
    project_name: str | None = None
    question: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RiskAssessment:
    level: RiskLevel
    reasons: list[str]
    requires_confirmation: bool = False
    blocked: bool = False


@dataclass(slots=True)
class PlanStep:
    id: str
    title: str
    tool: str
    args: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    risk: RiskLevel = RiskLevel.SAFE
    optional: bool = False


@dataclass(slots=True)
class ExecutionPlan:
    id: str
    goal: str
    intents: list[IntentScore]
    entities: EntitySet
    risk: RiskAssessment
    steps: list[PlanStep]
    dry_run: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "goal": self.goal,
            "intents": [{"intent": i.intent.value, "confidence": i.confidence, "evidence": i.evidence} for i in self.intents],
            "entities": asdict(self.entities),
            "risk": {"level": self.risk.level.value, "reasons": self.risk.reasons, "requires_confirmation": self.risk.requires_confirmation, "blocked": self.risk.blocked},
            "steps": [{"id": s.id, "title": s.title, "tool": s.tool, "args": s.args, "depends_on": s.depends_on, "risk": s.risk.value, "optional": s.optional} for s in self.steps],
            "dry_run": self.dry_run,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


@dataclass(slots=True)
class ToolResult:
    tool: str
    ok: bool
    data: Any = None
    error: str | None = None
    side_effects: list[str] = field(default_factory=list)
    risk: RiskLevel = RiskLevel.SAFE


@dataclass(slots=True)
class ExecutionReport:
    plan_id: str
    dry_run: bool
    results: list[ToolResult]
    blocked: bool = False
    summary: str = ""

    @property
    def ok(self) -> bool:
        return (not self.blocked) and all(r.ok for r in self.results)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "dry_run": self.dry_run,
            "blocked": self.blocked,
            "ok": self.ok,
            "summary": self.summary,
            "results": [asdict(r) | {"risk": r.risk.value} for r in self.results],
        }


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"
