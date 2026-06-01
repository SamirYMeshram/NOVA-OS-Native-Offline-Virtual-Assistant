from nova.plugins.sdk import PluginManifest
from nova.ai.model_manager import ModelManager
class ModelStatusPlugin:
    manifest = PluginManifest('model_status','1.0','Local model provider status')
    def run(self, command='', **kwargs): return {'ok': True, 'providers': ModelManager().provider_status()}
def create_plugin(): return ModelStatusPlugin()
