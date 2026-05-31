from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class AutomationManagerPlugin:
    manifest = PluginManifest(name='automation_manager', version='1.0.0', description='Safe automation actions', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'automation_manager', 'message': 'Safe automation actions', 'command': command, 'context_keys': sorted(context.keys())}
