from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class TasksPlugin:
    manifest = PluginManifest(name='tasks', version='1.0.0', description='Manage local tasks', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'tasks', 'message': 'Manage local tasks', 'command': command, 'context_keys': sorted(context.keys())}
