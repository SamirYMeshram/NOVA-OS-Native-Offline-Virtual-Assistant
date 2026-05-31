from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class FileCleanerPlugin:
    manifest = PluginManifest(name='file_cleaner', version='1.0.0', description='Plan safe file cleanup', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'file_cleaner', 'message': 'Plan safe file cleanup', 'command': command, 'context_keys': sorted(context.keys())}
