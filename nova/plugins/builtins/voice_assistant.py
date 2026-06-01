from nova.plugins.sdk import PluginManifest
class VoiceAssistantPlugin:
    manifest = PluginManifest('voice_assistant','1.0','Offline voice extension point')
    def run(self, command='', **kwargs): return {'ok': True, 'message': 'Voice is an offline extension point. Install local STT/TTS adapters to enable.'}
def create_plugin(): return VoiceAssistantPlugin()
