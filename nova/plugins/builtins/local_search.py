from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class LocalSearchPlugin:
    manifest = PluginManifest(name='local_search', version='1.0.0', description='Search local files', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'local_search', 'message': 'Search local files', 'command': command, 'context_keys': sorted(context.keys())}
