from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class KnowledgeBasePlugin:
    manifest = PluginManifest(name='knowledge_base', version='1.0.0', description='Local knowledge base', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'knowledge_base', 'message': 'Local knowledge base', 'command': command, 'context_keys': sorted(context.keys())}
