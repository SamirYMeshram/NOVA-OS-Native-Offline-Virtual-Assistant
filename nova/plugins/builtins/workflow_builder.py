from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class WorkflowBuilderPlugin:
    manifest = PluginManifest(name='workflow_builder', version='1.0.0', description='Register repeatable workflows', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'workflow_builder', 'message': 'Register repeatable workflows', 'command': command, 'context_keys': sorted(context.keys())}
