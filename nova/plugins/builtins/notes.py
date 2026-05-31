from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class NotesPlugin:
    manifest = PluginManifest(name='notes', version='1.0.0', description='Create and search local notes', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'notes', 'message': 'Create and search local notes', 'command': command, 'context_keys': sorted(context.keys())}
