from __future__ import annotations
import subprocess, sys
from nova.security.command_policy import CommandPolicy

class AppLauncher:
    def __init__(self):
        self.policy = CommandPolicy()

    def plan_launch(self, app: str) -> dict:
        assessment = self.policy.assess(app)
        return {'app': app, 'allowed': assessment.allowed, 'requires_confirmation': True, 'reason': assessment.reason}

    def launch(self, app: str, confirmed: bool = False) -> dict:
        plan = self.plan_launch(app)
        if not plan['allowed']:
            return {'ok': False, **plan}
        if not confirmed:
            return {'ok': False, **plan, 'message': 'App launch requires confirmation'}
        if sys.platform.startswith('linux'):
            subprocess.Popen([app])  # noqa: S603,S607
            return {'ok': True, 'message': f'Launched {app}'}
        return {'ok': False, 'message': 'Launch currently implemented for Linux PATH apps only'}
