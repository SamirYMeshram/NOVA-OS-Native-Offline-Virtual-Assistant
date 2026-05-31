from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class SystemMonitorPlugin:
    manifest = PluginManifest(name='system_monitor', version='1.0.0', description='Show local system status', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'system_monitor', 'message': 'Show local system status', 'command': command, 'context_keys': sorted(context.keys())}
