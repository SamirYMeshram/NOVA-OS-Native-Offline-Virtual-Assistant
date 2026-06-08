from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True)
class AgentOpinion:
    role: str
    advice: str
    risk: str

ROLES = {
    "architect": "Check architecture, boundaries, extension points, maintainability.",
    "security": "Check safety, permissions, path protection, secret handling.",
    "product": "Check whether the workflow feels useful to the user.",
    "qa": "Check tests, validation, edge cases, failure modes.",
    "local_ai": "Check local model, fallback, retrieval, offline behavior.",
}


def council(goal: str) -> list[AgentOpinion]:
    low = goal.lower()
    opinions=[]
    for role, focus in ROLES.items():
        risk = "review" if any(w in low for w in ["clean", "move", "write", "delete", "launch"]) and role == "security" else "safe"
        opinions.append(AgentOpinion(role, f"{focus} For this goal: {goal[:120]}", risk))
    return opinions
