from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class CodeGeneratorPlugin:
    manifest = PluginManifest(name='code_generator', version='1.0.0', description='Create local project templates', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'code_generator', 'message': 'Create local project templates', 'command': command, 'context_keys': sorted(context.keys())}
