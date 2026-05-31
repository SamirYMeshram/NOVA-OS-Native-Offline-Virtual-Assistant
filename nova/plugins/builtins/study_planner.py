from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class StudyPlannerPlugin:
    manifest = PluginManifest(name='study_planner', version='1.0.0', description='Generate study plans and flashcards', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'study_planner', 'message': 'Generate study plans and flashcards', 'command': command, 'context_keys': sorted(context.keys())}
