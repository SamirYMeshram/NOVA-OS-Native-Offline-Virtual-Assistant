from __future__ import annotations
from dataclasses import asdict
from .classifier import IntentClassifier
from .planner import AgentPlanner

class CommandRouter:
    def __init__(self, classifier: IntentClassifier | None = None, planner: AgentPlanner | None = None):
        self.classifier = classifier or IntentClassifier()
        self.planner = planner or AgentPlanner()

    def route(self, command: str) -> dict:
        intent = self.classifier.classify(command)
        plan = self.planner.plan(intent, command)
        return {'intent': intent.value, 'summary': plan.summary, 'steps': [asdict(s) for s in plan.steps]}
