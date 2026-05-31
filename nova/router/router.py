from __future__ import annotations
from .classifier import IntentClassifier
from .planner import Planner
from .executor import CommandExecutor
from nova.core.result import Result
from dataclasses import asdict

class CommandRouter:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.planner = Planner()
        self.executor = CommandExecutor()

    def route(self, command: str, **kwargs) -> Result:
        intent = self.classifier.classify(command)
        plan = self.planner.plan(intent, command)
        result = self.executor.execute(intent, command, **kwargs)
        result.data.setdefault('intent', intent.value)
        result.data.setdefault('plan', [asdict(step) for step in plan.steps])
        result.data.setdefault('requires_confirmation', plan.requires_confirmation)
        return result
