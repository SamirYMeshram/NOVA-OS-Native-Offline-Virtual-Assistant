from __future__ import annotations
from dataclasses import dataclass
from nova.core.security import evaluate_shell_command, SafetyDecision

@dataclass(slots=True)
class AutomationRequest:
    kind: str
    command: str
    reason: str = ""

class AutomationPolicy:
    def evaluate(self, request: AutomationRequest) -> SafetyDecision:
        if request.kind == 'shell':
            return evaluate_shell_command(request.command)
        if request.kind in {'open_app', 'open_folder', 'create_file', 'create_folder'}:
            return SafetyDecision(True, 'Approved low-risk desktop action', False, 'low')
        return SafetyDecision(False, 'Unknown automation kind requires plugin permission', True, 'medium')
