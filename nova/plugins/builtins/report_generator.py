from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class ReportGeneratorPlugin:
    manifest = PluginManifest(name='report_generator', version='1.0.0', description='Generate local reports', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'report_generator', 'message': 'Generate local reports', 'command': command, 'context_keys': sorted(context.keys())}
