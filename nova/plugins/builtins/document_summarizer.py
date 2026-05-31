from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class DocumentSummarizerPlugin:
    manifest = PluginManifest(name='document_summarizer', version='1.0.0', description='Summarize local documents', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'document_summarizer', 'message': 'Summarize local documents', 'command': command, 'context_keys': sorted(context.keys())}
