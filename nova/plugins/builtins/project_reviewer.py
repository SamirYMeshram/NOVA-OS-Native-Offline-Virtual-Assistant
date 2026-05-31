from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class ProjectReviewerPlugin:
    manifest = PluginManifest(name='project_reviewer', version='1.0.0', description='Analyze code projects', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'project_reviewer', 'message': 'Analyze code projects', 'command': command, 'context_keys': sorted(context.keys())}
