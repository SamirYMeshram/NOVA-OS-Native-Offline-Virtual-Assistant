from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class CsvAnalystPlugin:
    manifest = PluginManifest(name='csv_analyst', version='1.0.0', description='Profile CSV files locally', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'csv_analyst', 'message': 'Profile CSV files locally', 'command': command, 'context_keys': sorted(context.keys())}
