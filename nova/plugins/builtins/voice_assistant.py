from __future__ import annotations
from nova.plugins.base import PluginManifest
from nova.security.permissions import PermissionSet

class VoiceAssistantPlugin:
    manifest = PluginManifest(name='voice_assistant', version='1.0.0', description='Offline voice extension point', permissions=PermissionSet())

    def run(self, command: str, context: dict) -> dict:
        return {'ok': True, 'plugin': 'voice_assistant', 'message': 'Offline voice extension point', 'command': command, 'context_keys': sorted(context.keys())}
