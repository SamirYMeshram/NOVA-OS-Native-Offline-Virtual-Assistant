from dataclasses import asdict
from nova.plugins.sdk import PluginManifest
from nova.core.config import NovaConfig
class SettingsPlugin:
    manifest = PluginManifest('settings','1.0','Show local NOVA settings')
    def run(self, command='', **kwargs): return {'ok': True, 'config': asdict(NovaConfig.load())}
def create_plugin(): return SettingsPlugin()
