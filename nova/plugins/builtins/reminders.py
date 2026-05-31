from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class RemindersPlugin:
    manifest = PluginManifest(name='reminders', version='1.0.0', description='Manage local reminders', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'reminders', 'message': 'Manage local reminders', 'command': command, 'context_keys': sorted(context.keys())}
